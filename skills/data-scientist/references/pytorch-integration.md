# PyTorch Integration Reference

**Source validated against:** PyTorch 2.12 documentation (pytorch.org/docs/stable)  
**Last reviewed:** 2026-05-23  
**When to load:** The campaign protocol (Phase 3-7) or any task requires implementing, training, or deploying a PyTorch model.

---

## Device Management

### Canonical Device Pattern

Always parameterize the device. Never hardcode `"cuda"`.

```python
import torch

device = torch.device(
    "cuda" if torch.cuda.is_available()
    else "mps" if torch.backends.mps.is_available()
    else "cpu"
)
# Usage: model.to(device); tensor.to(device)
```

### Checking Device Properties

```python
if torch.cuda.is_available():
    print(f"Device: {torch.cuda.get_device_name(0)}")
    print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    print(f"CUDA Capability: {torch.cuda.get_device_capability(0)}")
```

**MPS (Apple Silicon):** Available on macOS 12.3+. Not all operations are supported — check `torch.backends.mps.is_available()` and `torch.backends.mps.is_built()`. Some operations fall back to CPU automatically.

---

## Training Loop Patterns

### Basic Supervised Training Loop

```python
model.train()
for epoch in range(num_epochs):
    running_loss = 0.0
    for batch_x, batch_y in dataloader:
        batch_x, batch_y = batch_x.to(device), batch_y.to(device)

        optimizer.zero_grad()
        outputs = model(batch_x)
        loss = criterion(outputs, batch_y)
        loss.backward()

        # Gradient clipping (essential for stability)
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

        optimizer.step()

        running_loss += loss.item()

    avg_loss = running_loss / len(dataloader)
    print(f"Epoch {epoch}: loss={avg_loss:.4f}")
```

### Gradient Accumulation (for large models on limited VRAM)

```python
accumulation_steps = 4  # Effective batch_size = physical_batch * accumulation

for i, (batch_x, batch_y) in enumerate(dataloader):
    outputs = model(batch_x)
    loss = criterion(outputs, batch_y) / accumulation_steps
    loss.backward()

    if (i + 1) % accumulation_steps == 0:
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        optimizer.zero_grad()
```

### Validation Loop

```python
model.eval()
val_loss = 0.0
correct = 0
total = 0

with torch.no_grad():
    for batch_x, batch_y in val_loader:
        batch_x, batch_y = batch_x.to(device), batch_y.to(device)
        outputs = model(batch_x)
        val_loss += criterion(outputs, batch_y).item()
        _, predicted = torch.max(outputs, 1)
        total += batch_y.size(0)
        correct += (predicted == batch_y).sum().item()

print(f"Val Loss: {val_loss/len(val_loader):.4f}, Acc: {100*correct/total:.2f}%")
```

---

## Dataset & DataLoader

### Custom Dataset Class

```python
from torch.utils.data import Dataset, DataLoader

class CustomDataset(Dataset):
    def __init__(self, features, labels, transform=None):
        self.features = torch.tensor(features, dtype=torch.float32)
        self.labels = torch.tensor(labels, dtype=torch.long)
        self.transform = transform

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        x = self.features[idx]
        y = self.labels[idx]
        if self.transform:
            x = self.transform(x)
        return x, y
```

### DataLoader Configuration

```python
dataloader = DataLoader(
    dataset,
    batch_size=32,
    shuffle=True,
    num_workers=4,          # Set to 0 on Windows if multiprocessing issues
    pin_memory=True,        # Speeds up GPU transfer (only with CUDA)
    persistent_workers=True if num_workers > 0 else False,  # PyTorch 2.0+
    collate_fn=None,        # Custom collation for variable-length data
)
```

**Note on `num_workers`:** On Linux, 4-8 workers is typical. On macOS, keep at 0-2. On Windows, 0 is safest. The optimal value depends on the data loading speed vs GPU speed.

### Collate Function for Variable-Length Data

```python
def collate_fn(batch):
    """Pad sequences in a batch to the same length."""
    inputs, labels = zip(*batch)
    # Pad to max length in this batch
    inputs_padded = torch.nn.utils.rnn.pad_sequence(inputs, batch_first=True)
    return inputs_padded, torch.tensor(labels)
```

---

## Model Saving & Loading

### Save/Load State Dict (Recommended)

```python
# Save
torch.save({
    "epoch": epoch,
    "model_state_dict": model.state_dict(),
    "optimizer_state_dict": optimizer.state_dict(),
    "loss": loss,
    "config": {"n_layers": 4, "hidden_dim": 256},  # metadata
}, "checkpoint.pt")

# Load
checkpoint = torch.load("checkpoint.pt", map_location=device)
model.load_state_dict(checkpoint["model_state_dict"])
optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
start_epoch = checkpoint["epoch"] + 1
```

### Save for Inference (weights only)

```python
torch.save(model.state_dict(), "model_weights.pt")

# Load for inference
model = YourModel()
model.load_state_dict(torch.load("model_weights.pt", map_location="cpu"))
model.eval()
```

### TorchScript / torch.export (for production deployment)

```python
# torch.export (PyTorch 2.x preferred, producesExportedProgram)
exported_program = torch.export.export(model, (example_input,))
torch.export.save(exported_program, "model.pt2")

# TorchScript (legacy, still widely supported)
scripted_model = torch.jit.script(model)
scripted_model.save("model_scripted.pt")
```

---

## Mixed Precision (AMP)

Automatic Mixed Precision trains with `float16` (or `bfloat16`) where safe and `float32` where needed. Typically 1.5-2x faster with minimal accuracy loss.

```python
from torch.amp import autocast, GradScaler

scaler = GradScaler("cuda")  # "cuda" or "cpu"

for batch_x, batch_y in dataloader:
    batch_x, batch_y = batch_x.to(device), batch_y.to(device)

    optimizer.zero_grad()

    # Autocast context manager
    with autocast(device_type="cuda"):  # or "cpu"
        outputs = model(batch_x)
        loss = criterion(outputs, batch_y)

    # Scale loss, backward, unscale, step
    scaler.scale(loss).backward()
    scaler.unscale_(optimizer)
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
    scaler.step(optimizer)
    scaler.update()
```

**Key points:**
- `autocast` wraps forward pass + loss computation only
- `GradScaler` prevents underflow in small gradients
- Use `bfloat16` on Ampere+ GPUs (less numerical issues than `float16`)
- AMP is most beneficial for large models (CNNs, Transformers) — small models may not see speedup

---

## torch.compile (PyTorch 2.x JIT Compilation)

`torch.compile` compiles model graphs for faster execution with minimal code changes.

```python
# Basic usage (reduces model — returns a compiled wrapper)
compiled_model = torch.compile(model)

# With options
compiled_model = torch.compile(
    model,
    mode="reduce-overhead",  # "default", "reduce-overhead", "max-autotune"
    fullgraph=True,          # Fail if graph breaks
    dynamic=True,            # Support dynamic tensor shapes
)

# Training is identical:
output = compiled_model(batch_x)  # First call compiles, subsequent calls are fast
```

**When to use:** Models with large tensor operations (CNNs, Transformers). Not beneficial for very small models or heavy data loading bottlenecks.

**When not to use:** Dynamic control flow, custom CUDA extensions, models compiled for TorchScript export.

**Mode selection:**
- `"default"` — conservative, works for most models
- `"reduce-overhead"` — good for inference, reduces Python overhead
- `"max-autotune"` — benchmarks and picks the best backend (slow first run)

---

## Loss Functions

| Problem Type | Loss Function | Import |
|---|---|---|
| Binary classification | `BCEWithLogitsLoss` | `torch.nn.BCEWithLogitsLoss` |
| Multi-class classification | `CrossEntropyLoss` | `torch.nn.CrossEntropyLoss` |
| Multi-label classification | `BCEWithLogitsLoss` | Combines sigmoid + BCELoss |
| Regression (MSE) | `MSELoss` | `torch.nn.MSELoss` |
| Regression (MAE) | `L1Loss` | `torch.nn.L1Loss` |
| Regression (Huber) | `HuberLoss` | `torch.nn.HuberLoss` (delta parameter) |
| Contrastive / Siamese | `TripletMarginLoss` / `ContrastiveLoss` | `torch.nn.TripletMarginLoss` |
| Imbalanced classes | Weighted `CrossEntropyLoss` | Pass `weight` tensor to constructor |
| Sequence (CTC) | `CTCLoss` | `torch.nn.CTCLoss` |

```python
# Weighted loss for imbalanced data
class_weights = torch.tensor([0.2, 0.8]).to(device)  # inverse frequency
criterion = torch.nn.CrossEntropyLoss(weight=class_weights)
```

---

## Optimizers & Schedulers

| Optimizer | When | Learning Rate |
|---|---|---|
| `AdamW` | Default for most models (Transformers, CNNs) | 1e-4 to 3e-4 |
| `Adam` | Legacy; prefer AdamW (proper weight decay) | 1e-4 to 3e-4 |
| `SGD` + momentum | When Adam overfits; vision models | 1e-2 to 1e-1 |
| `AdamW` (LoRA) | Fine-tuning with LoRA | 2e-4 to 5e-4 |

```python
import torch.optim as optim

# AdamW — the default
optimizer = optim.AdamW(model.parameters(), lr=1e-4, weight_decay=0.01)

# SGD with momentum (for vision fine-tuning)
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9, weight_decay=1e-4)
```

### Learning Rate Schedulers

```python
from torch.optim.lr_scheduler import (
    ReduceLROnPlateau,  # Reduce when metric plateaus
    CosineAnnealingLR,  # Cosine decay
    OneCycleLR,         # Warmup + cosine ("super-convergence")
)

# Reduce on plateau (works well for most tasks)
scheduler = ReduceLROnPlateau(optimizer, mode="min", patience=5, factor=0.5)

# One-cycle (fast convergence, needs max_lr)
scheduler = OneCycleLR(
    optimizer,
    max_lr=1e-3,
    steps_per_epoch=len(train_loader),
    epochs=num_epochs,
)

# Cosine annealing (good for Transformers)
scheduler = CosineAnnealingLR(optimizer, T_max=num_epochs)

# Warmup + cosine (standard for LLM fine-tuning)
# Implement manually:
def get_cosine_schedule_with_warmup(optimizer, warmup_steps, total_steps):
    def lr_lambda(current_step):
        if current_step < warmup_steps:
            return float(current_step) / float(max(1, warmup_steps))
        progress = float(current_step - warmup_steps) / float(max(1, total_steps - warmup_steps))
        return 0.5 * (1.0 + math.cos(math.pi * progress))
    return torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)
```

---

## Transfer Learning

### Feature Extraction (Freeze Backbone)

```python
import torchvision.models as models

model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)

# Freeze all layers
for param in model.parameters():
    param.requires_grad = False

# Replace classifier
num_features = model.fc.in_features
model.fc = torch.nn.Linear(num_features, num_classes)

# Only the new layer's params are trainable
optimizer = optim.AdamW(model.fc.parameters(), lr=1e-3)
```

### Full Fine-Tuning

```python
# Unfreeze all layers
for param in model.parameters():
    param.requires_grad = True

# Use lower learning rate
optimizer = optim.AdamW(model.parameters(), lr=2e-5)

# Often helps to freeze early layers, fine-tune later layers:
for name, param in model.named_parameters():
    if "layer1" in name or "layer2" in name:
        param.requires_grad = False
```

### LoRA for Transformer Models

LoRA (Low-Rank Adaptation) trains small rank-decomposition matrices while keeping the base model frozen. Requires the `peft` library.

```python
from peft import LoraConfig, get_peft_model

lora_config = LoraConfig(
    r=8,                    # Rank — higher = more expressiveness, more params
    lora_alpha=32,          # Scaling factor
    target_modules=["q_proj", "v_proj"],  # Which modules to apply LoRA to
    lora_dropout=0.1,
    bias="none",            # Don't train bias terms
    task_type="SEQ_CLS",    # Task type (SEQ_CLS, CAUSAL_LM, TOKEN_CLS, etc.)
)

model = get_peft_model(base_model, lora_config)

# Train with slightly higher LR
optimizer = optim.AdamW(model.parameters(), lr=3e-4)

# LoRA adds very few params (< 1% of base model)
model.print_trainable_parameters()  # e.g., "trainable params: 294,912 || all params: 110,080,512 || %: 0.2679"
```

---

## Knowledge Distillation

```python
import torch.nn.functional as F

def distillation_loss(student_logits, teacher_logits, labels, temperature=4.0, alpha=0.7):
    """
    Combined distillation + supervised loss.

    Args:
        temperature: Higher = softer probability distribution (more information from teacher)
        alpha: Weight for distillation loss (vs standard cross-entropy)
    """
    # Soft target loss (distillation)
    soft_student = F.log_softmax(student_logits / temperature, dim=-1)
    soft_teacher = F.softmax(teacher_logits.detach() / temperature, dim=-1)
    distill_loss = F.kl_div(soft_student, soft_teacher, reduction="batchmean")
    distill_loss *= temperature ** 2  # Scale to keep gradients in right range

    # Hard target loss
    hard_loss = F.cross_entropy(student_logits, labels)

    return alpha * distill_loss + (1 - alpha) * hard_loss


# Training loop with distillation
teacher_model.eval()
for batch_x, batch_y in dataloader:
    with torch.no_grad():
        teacher_logits = teacher_model(batch_x)

    student_logits = student_model(batch_x)
    loss = distillation_loss(student_logits, teacher_logits, batch_y)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
```

**Temperature tuning:** Start with T=4.0. Higher values produce softer targets (more small-class information). Lower values (T=1.0) collapse to standard cross-entropy.

**Alpha tuning:** α=0.7 (weight on distillation) is a common starting point. Increase α when the teacher is much better than the student.

---

## Model Pruning

```python
import torch.nn.utils.prune as prune

# Apply pruning to specific layers
prune.l1_unstructured(module=model.fc, name="weight", amount=0.3)  # Remove 30% of weights

# Make pruning permanent (removes the pruning mask)
prune.remove(module=model.fc, name="weight")

# Structured pruning (removes entire neurons/channels)
prune.ln_structured(module=model.conv1, name="weight", amount=0.2, n=2, dim=0)

# Global pruning (prune all layers together by importance)
parameters_to_prune = [
    (model.layer1, "weight"),
    (model.layer2, "weight"),
    (model.fc, "weight"),
]
prune.global_unstructured(
    parameters_to_prune,
    pruning_method=prune.L1Unstructured,
    amount=0.2,  # Remove 20% of weights globally
)
```

**After pruning:** Fine-tune the pruned model. Pruning then fine-tuning almost always recovers accuracy. Pruning without fine-tuning degrades performance significantly.

---

## Distributed Data Parallel (DDP)

For multi-GPU training. DDP wraps the model and handles gradient synchronization.

```python
import torch.distributed as dist
import torch.multiprocessing as mp
from torch.nn.parallel import DistributedDataParallel as DDP

def setup(rank, world_size):
    """Initialize the distributed process group."""
    dist.init_process_group(
        backend="nccl",              # "nccl" for NVIDIA, "gloo" for CPU
        init_method="env://",         # Use env vars MASTER_ADDR and MASTER_PORT
        rank=rank,
        world_size=world_size,
    )

def cleanup():
    dist.destroy_process_group()

def train(rank, world_size):
    setup(rank, world_size)

    # Model must be on the correct device BEFORE wrapping
    model = YourModel().to(rank)
    ddp_model = DDP(model, device_ids=[rank])

    # DataLoader must use DistributedSampler
    sampler = torch.utils.data.distributed.DistributedSampler(
        dataset, num_replicas=world_size, rank=rank
    )
    dataloader = DataLoader(dataset, batch_size=32, sampler=sampler)

    # Training loop (same structure, use ddp_model)
    for epoch in range(num_epochs):
        sampler.set_epoch(epoch)  # Shuffle each epoch
        for batch_x, batch_y in dataloader:
            batch_x, batch_y = batch_x.to(rank), batch_y.to(rank)
            outputs = ddp_model(batch_x)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()

    cleanup()

# Launch
if __name__ == "__main__":
    world_size = torch.cuda.device_count()
    mp.spawn(train, args=(world_size,), nprocs=world_size)
```

**When DDP is worth it:** Models that take > 1 hour to train on a single GPU. For short experiments, single-GPU + AMP is often faster due to communication overhead.

---

## Debugging

### Common Failure Patterns

| Symptom | Likely Cause | Fix |
|---|---|---|
| `loss = nan` | Exploding gradients, bad learning rate | Lower LR, add gradient clipping, check for NaN in input data |
| `loss = nan` after AMP | Gradient underflow | Increase `GradScaler` init_scale, or use `bfloat16` |
| Loss doesn't decrease | Wrong LR, wrong loss function | Check LR range, verify loss function matches task |
| CUDA OOM | Batch size too large | Reduce batch size, enable gradient checkpointing, use AMP |
| `Expected all tensors to be on...` | Device mismatch | Always `.to(device)` tensors before model forward |
| `CUDA error: device-side assert` | Wrong label class (out of range) | Check label values are in `[0, num_classes)` |
| Model doesn't overfit 1 batch | Bug in model architecture | Try overfitting on a single batch (batch of 2-4 samples for 100 steps) |

### Overfit on One Batch (Diagnostic)

```python
# If model can't overfit a single batch, something is fundamentally wrong
single_batch = next(iter(dataloader))

for step in range(100):
    outputs = model(single_batch[0].to(device))
    loss = criterion(outputs, single_batch[1].to(device))
    loss.backward()
    optimizer.step()

print(f"Loss after 100 steps on 1 batch: {loss.item():.6f}")
# If loss is not near 0, model has a bug or LR is way off.
```

### Gradient Checking

```python
# Check gradient norms during training
total_norm = 0.0
for p in model.parameters():
    if p.grad is not None:
        param_norm = p.grad.data.norm(2)
        total_norm += param_norm.item() ** 2
total_norm = total_norm ** 0.5

if total_norm > 10.0:
    print(f"WARNING: Large gradient norm: {total_norm:.4f}")
```

---

## Reproducibility

```python
import random
import numpy as np
import torch

def set_seed(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False  # Trades off speed for determinism

set_seed(42)
```

**Note on `cudnn.deterministic`:** Setting this to `True` may reduce performance (5-15%). For experiments where exact reproducibility isn't critical, leave `benchmark=True` and accept minor stochastic variation.

---

## See Also

- `references/experimental-campaign-protocol.md` — where this reference fits in the campaign workflow
- `references/sklearn-integration.md` — for non-deep-learning methods
- `scripts/detect-compute.py` — check your hardware before choosing model size
- pytorch.org/docs/stable — official API documentation
