# Experimental Campaign Protocol

**When to load this reference:** The user has asked you to find the best approach to a problem, run a research campaign, or optimize a model — not just answer a single question. The question classifier in the parent skill routes `CAMPAIGN`-type questions here.

**Core philosophy:** Start boring, end smart. Establish a heuristic baseline first, then apply bleeding-edge research, then iterate. Never skip directly to the fancy method.

---

## Protocol Overview

```
┌─────────────────────────────────────────────────────────┐
│  1. Problem Formulation       (What are we solving?)     │
├─────────────────────────────────────────────────────────┤
│  2. Baseline Heuristic        (What's the floor?)        │
├─────────────────────────────────────────────────────────┤
│  3. Bleeding-Edge Survey      (What's the SOTA?)         │
├─────────────────────────────────────────────────────────┤
│  4. Moonshot Experiments      (What works on our data?)  │
├─────────────────────────────────────────────────────────┤
│  5. Transfer Learning         (What's already learned?)  │
├─────────────────────────────────────────────────────────┤
│  6. Hyperparameter Search     (What are best params?)    │
├─────────────────────────────────────────────────────────┤
│  7. Distillation              (What can we trim?)        │
├─────────────────────────────────────────────────────────┤
│  8. Synthesis & Handoff       (What did we learn?)       │
└─────────────────────────────────────────────────────────┘
```

---

## Phase 1: Problem Formulation

**Goal:** Translate a vague request into a well-defined question with measurable success criteria.

**Entry criteria:** User has a data science ask. Level of specificity varies.

**Steps:**

1. **Identify data type** — numeric, categorical, time series, text, spatial, hierarchical, high-dimensional
2. **Identify question type** — descriptive (what happened?), predictive (what will happen?), causal (what causes X?), mechanistic (how does X work?), exploratory (what's interesting?)
3. **Identify decision context** — what will the answer be used for? A product launch? A policy decision? An academic paper?
4. **Identify constraints** — sample size, feature count, compute budget, time budget, interpretability requirements, regulatory constraints
5. **Formalize the question** — restate in a falsifiable form. "Is model B better than model A on metric X with statistical significance?"
6. **Define success criteria** — what constitutes a win? Lift over baseline? Statistical significance? Latency budget? AUC > 0.9?

**Exit criteria:** A one-paragraph problem statement with: data description, question type, decision context, constraints, and success criteria.

**Code integration:** Write the problem statement to a `campaign.md` file at the experiment root. This becomes the source of truth that all phases reference.

**Time budget:** 15-30 minutes. If you're stuck, you haven't narrowed the scope enough.

**Failure modes:**
- Problem is too broad → "What single decision would most benefit from a better answer here?"
- No clear success criteria → "What metric would convince you to change what you're doing today?"
- User says "I don't know" → start with exploratory analysis on available data and iterate

---

## Phase 2: Baseline Heuristic

**Goal:** Establish a performance floor using simple, well-understood methods before trying anything fancy.

**Entry criteria:** Problem formulated, data accessible.

**Principles:**
- The baseline is the bar that every bleeding-edge method must clear
- If a complex method can't beat logistic regression, it's not useful
- Baselines are fast to train, interpretable, and reliable

**Steps:**

1. **Select baseline model(s) based on problem type:**

| Problem Type | Baseline Models |
|---|---|
| Binary classification | Logistic Regression, Naive Bayes, Decision Tree (max_depth=3) |
| Multi-class classification | Multinomial Logistic Regression, Random Forest (n_estimators=100) |
| Regression | Linear Regression, Ridge, Decision Tree Regressor |
| Time series forecasting | Naive forecast (last value), Seasonal Naive, ARIMA(1,1,1) |
| Recommendation | Popularity baseline, User/Item mean, KNN with Jaccard |
| Clustering | K-Means (k=sqrt(n/2)), Hierarchical with Ward linkage |
| Anomaly detection | Isolation Forest, 3-sigma rule, IQR-based |
| Text classification | TF-IDF + Logistic Regression |
| Image classification | Simple CNN (2 conv layers + 2 dense), or raw pixel + RF |

2. **Implement using scikit-learn pipelines:**
```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

# Build pipeline with preprocessing
numeric_features = [...]  # column names
categorical_features = [...]  # column names

preprocessor = ColumnTransformer([
    ("num", StandardScaler(), numeric_features),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
])

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
])

# Cross-validated evaluation
scores = cross_val_score(pipeline, X, y, cv=5, scoring="f1_macro")
print(f"Baseline F1: {scores.mean():.4f} ± {scores.std():.4f}")
```

3. **Record baseline metrics** — accuracy, F1, precision/recall, RMSE, MAE, or domain-specific metric. Store in experiment log.

4. **Diagnose baseline failures** — if the baseline fails (e.g., logistic regression returns chance-level performance), investigate before proceeding:
   - Is there signal in the data at all? (Check class balance, feature-target correlations)
   - Is preprocessing correct? (Missing values? Scaling issues? Leakage?)
   - Is the metric appropriate? (Imbalanced classes? Asymmetric costs?)

**Exit criteria:** Baseline metrics recorded. A clear "this is the bar to beat" value.

**Extension (when baselines are known to be insufficient):**
- Ensemble baseline: Random Forest with 500 trees
- Tuned baseline: `GridSearchCV` over a small grid on the pipeline

**Failure modes:**
- Baseline performs at chance → check data quality, label sanity, feature engineering
- Baseline takes too long → subsample data for baseline, use faster estimator
- Multiple baselines disagree → use the best one as reference, document all

---

## Phase 3: Bleeding-Edge Survey

**Goal:** Identify the most promising recent approaches from research that could outperform the baseline.

**Entry criteria:** Baseline established. We know what "good enough" looks like.

**Steps:**

1. **Construct search queries** based on problem + data type:
   - `"<problem type>" AND "<data type>" AND SOTA OR state-of-the-art`
   - `"<dataset name>" benchmark leaderboard`
   - `"<problem type>" 2025 2026`
   - `best practices <problem type> <data type>`

2. **Search venues:**
   - **arXiv** — use the agent's arXiv search tool with filters for recent papers (last 2 years)
   - **Papers With Code** — benchmark leaderboards with code links
   - **HuggingFace Papers** — huggingface.co/papers
   - **GitHub** — search by topic for recent repos with high stars
   - **Model Zoos** — HuggingFace Models, PyTorch Hub, TensorFlow Hub

3. **Evaluate each candidate** — for each paper/repo found, assess:
   - **Code available?** (paper without code is 10x harder to reproduce)
   - **Benchmarked on similar data?** (same domain, size, characteristics)
   - **Computational cost?** (GPU hours, model size, inference latency)
   - **Reproducibility?** (clear hyperparameters, seeded runs, open dataset)
   - **Recency?** (within 2 years for cutting edge, 3-5 for well-established)

4. **Select top 2-3 candidates** — choose methods that:
   - Have public code (priority)
   - Match our compute budget
   - Show meaningful improvement over baseline on comparable benchmarks
   - Cover different approaches (don't pick 3 variants of the same method)

**Exit criteria:** Shortlist of 2-3 methods to try, each with: paper link, code link (or "no code available — reimplement from paper"), expected compute cost, expected improvement over baseline, and risk assessment.

**Code integration:**
```python
# Phases 3-4 typically use PyTorch for deep learning methods.
# See references/pytorch-integration.md for training loop templates.
```

**Failure modes:**
- No relevant papers found → expand search to adjacent domains, or use ensemble of baselines (stacking, boosting, bagging)
- Papers found but no code → assess reimplementation cost; skip if > 2 days
- Papers require 8x our compute → note as aspirational, focus on methods within budget
- Field moves fast (NLP/CV) → prioritize papers from last 6 months

---

## Phase 4: Moonshot Experiments

**Goal:** Implement the most promising approaches and compare to baseline.

**Entry criteria:** 2-3 candidate methods selected and understood. Compute available.

**Steps:**

1. **For each candidate method:**
   a. Clone/setup the codebase or implement the approach
   b. Configure for your data (input format, preprocessing, output mapping)
   c. Run with recommended hyperparameters from the paper
   d. Evaluate on the same metrics as the baseline

2. **Compare results:**
   - Create a comparison table (method | metric | vs baseline | compute cost | notes)
   - Flag methods that underperform baseline (common and informative!)
   - Flag methods that exceed baseline — these proceed to Phase 5

3. **Document failures:** For each method that didn't work, note:
   - What was tried? (hyperparameters, data splits, preprocessing variations)
   - What went wrong? (convergence issues, OOM, poor generalization, data mismatch)
   - Could it work with more tuning? More data? Different preprocessing?

**Exit criteria:** For each candidate, a clear "pass/fail/worth-more-tuning" assessment with evidence.

**Code integration:**
```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from torch.utils.tensorboard import SummaryWriter

# Canonical PyTorch training loop (see pytorch-integration.md for details)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = YourModel().to(device)
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=3)
writer = SummaryWriter(log_dir="runs/experiment_1")

for epoch in range(num_epochs):
    model.train()
    for batch_x, batch_y in train_loader:
        batch_x, batch_y = batch_x.to(device), batch_y.to(device)
        optimizer.zero_grad()
        loss = criterion(model(batch_x), batch_y)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        writer.add_scalar("train/loss", loss.item(), epoch)
```

**Failure modes:**
- All methods fail → revisit Phase 3 with broader search. Consider ensemble of baselines.
- Method works but needs 10x compute → note as future work, use with smaller data
- Code doesn't run → spend max 2 hours debugging; if not fixed, move to next candidate

---

## Phase 5: Transfer Learning

**Goal:** Leverage pre-trained models to improve performance with less data and compute.

**Entry criteria:** At least one promising method identified. Data is compatible with pre-trained models.

**Steps:**

1. **Identify pre-trained candidates:**
   - **Images:** `torchvision.models` (ResNet, EfficientNet, ViT, ConvNeXt)
   - **Text:** `transformers` (BERT, RoBERTa, DeBERTa, Llama, GPT)
   - **Audio:** `torchaudio` models, `transformers` (Wav2Vec2, Whisper)
   - **Time series:** PatchTST, TimesNet (less standardized; check papers)
   - **Tabular:** No strong TL tradition; skip or use FT-Transformer

2. **Choose adaptation strategy:**

| Strategy | When | Compute | Data Needed |
|---|---|---|---|
| **Feature extraction** | Target domain close to source | Low | Small |
| **Fine-tuning (full)** | Target domain diverges | High | Medium |
| **Fine-tuning (LoRA)** | Target diverges, limited VRAM | Medium | Medium |
| **Fine-tuning (last layers)** | Target domain similar | Low | Small |
| **Adapter modules** | Multi-task or parameter-efficient | Low | Small |

3. **Implement feature extraction:**
```python
import torchvision.models as models

# Load pre-trained backbone, freeze it
backbone = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
for param in backbone.parameters():
    param.requires_grad = False

# Replace the head
backbone.fc = nn.Linear(backbone.fc.in_features, num_classes)
```

4. **Implement fine-tuning with LoRA** (when VRAM-constrained):
```python
from peft import LoraConfig, get_peft_model

lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["query", "value"],  # for transformer models
    lora_dropout=0.1,
)

model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")
model = get_peft_model(model, lora_config)
# Only LoRA params are trainable
```

5. **Compare to non-transfer version:** Does TL actually help on your data? Sometimes it doesn't — especially if the pre-training distribution is very different from your target.

**Exit criteria:** Transfer-learned model metrics recorded alongside non-transfer results. Decision on whether TL is worth the complexity.

**Failure modes:**
- Pre-trained model too large for VRAM → use LoRA/QLoRA, smaller variant (DistilBERT vs BERT), or CPU offloading
- Pre-training domain too different → try a different foundation model, or skip TL
- No improvement from TL → the dataset may not benefit from pre-trained features; use Phase 4 results

---

## Phase 6: Hyperparameter Optimization

**Goal:** Systematically find the best hyperparameters for the most promising model(s).

**Entry criteria:** At least one model performing above baseline. Hyperparameter search space defined.

**Steps:**

1. **Define search space:**
   - Include model architecture choices (layers, hidden size, activation)
   - Training hyperparameters (learning rate, batch size, optimizer, scheduler)
   - Data preprocessing parameters (sequence length, augmentation, normalization)
   - Regularization (dropout, weight decay, label smoothing)

2. **Choose search strategy:**

| Strategy | When | Trials Needed | Notes |
|---|---|---|---|
| Grid search | <= 3 params, discrete values | Product of values | Exhaustive but expensive |
| Random search | 3-10 params, mixed types | 30-100 | Good default — 60 random trials covers most of the space |
| Bayesian (Optuna) | 5-20 params, complex interactions | 50-300 | Best for neural networks. TPESampler by default. |
| Hyperband / ASHA | Many trials, early stopping | 100-1000 | Prunes poor trials early. Great for deep learning. |

3. **Implement with Optuna:**
```python
import optuna
from optuna.pruners import MedianPruner
from optuna.samplers import TPESampler

def objective(trial):
    lr = trial.suggest_float("lr", 1e-5, 1e-2, log=True)
    dropout = trial.suggest_float("dropout", 0.1, 0.5)
    batch_size = trial.suggest_categorical("batch_size", [16, 32, 64])
    weight_decay = trial.suggest_float("weight_decay", 1e-6, 1e-3, log=True)
    n_layers = trial.suggest_int("n_layers", 1, 4)

    model = create_model(dropout=dropout, n_layers=n_layers)
    loader = create_loader(batch_size=batch_size)
    val_score = train_and_eval(model, loader, lr, weight_decay, trial=trial)
    return val_score  # e.g., validation F1

study = optuna.create_study(
    direction="maximize",
    sampler=TPESampler(seed=42),
    pruner=MedianPruner(n_startup_trials=10, n_warmup_steps=5),
)
study.optimize(objective, n_trials=100)

print(f"Best params: {study.best_params}")
print(f"Best value: {study.best_value:.4f}")
```

4. **Analyze results:** Use `optuna.visualization` to understand parameter importance.
   - Which params matter most? (Parameter importance plot)
   - Is there overfitting? (Train vs val performance across trials)
   - Should you expand the search space in a promising region?

**Exit criteria:** Best hyperparameters identified and validated. At least one configuration significantly exceeding baseline.

**Failure modes:**
- Random search finds no good region → expand search space, use wider ranges, add more trials
- Best parameters overfit → increase regularization, use early stopping, reduce model capacity
- Optuna study takes too long → reduce trials, use Hyperband pruner, subsample training data
- All trials converge to same value → the model may have plateaued; revisit architecture or data

---

## Phase 7: Distillation

**Goal:** Compress the best-performing model into a smaller, faster, cheaper version.

**Entry criteria:** A high-performing (but likely large) model exists. There's a need for smaller model (latency, cost, edge deployment).

**When to skip:** If the best model is already small (< 100M params), or there's no deployment constraint, skip distillation.

**Steps:**

1. **Knowledge distillation** (teacher → student):
```python
import torch.nn.functional as F

def distillation_loss(student_logits, teacher_logits, labels, T=4.0, alpha=0.7):
    """
    T: temperature - higher = softer probability distribution
    alpha: weight for distillation loss vs. standard loss
    """
    soft_loss = F.kl_div(
        F.log_softmax(student_logits / T, dim=-1),
        F.softmax(teacher_logits.detach() / T, dim=-1),
        reduction="batchmean"
    ) * (T * T)  # Scale factor to keep gradients in right range
    
    hard_loss = F.cross_entropy(student_logits, labels)
    return alpha * soft_loss + (1 - alpha) * hard_loss

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

2. **Pruning** (remove low-magnitude weights):
```python
import torch.nn.utils.prune as prune

# Apply L1 unstructured pruning to all linear layers
for name, module in model.named_modules():
    if isinstance(module, nn.Linear):
        prune.l1_unstructured(module, name="weight", amount=0.3)  # Remove 30% of weights
        prune.remove(module, "weight")  # Make pruning permanent
```

3. **Quantization** (reduce precision):
```python
# Post-training quantization (simplest, often good enough)
import torch.quantization as quant
quantized_model = quant.quantize_dynamic(
    model, {nn.Linear, nn.LSTM, nn.GRU}, dtype=torch.qint8
)

# Or: QAT (Quantization-Aware Training)
# model.qconfig = quant.get_default_qat_qconfig('fbgemm')
# quant.prepare_qat(model, inplace=True)
# ... train further ...
# quant.convert(model, inplace=True)
```

4. **Validate distilled model:** Compare distilled vs full model on the same test set. Document the tradeoff: size, speed, and accuracy.

**Exit criteria:** Distilled model metrics, size comparison, inference speed comparison. Decision: is the tradeoff acceptable?

**Failure modes:**
- Student model can't match teacher → increase student capacity, try softer targets (higher T), more epochs
- Pruning degrades performance → lower pruning amount, use structured pruning, fine-tune after pruning
- Quantization errors > 1% → use QAT instead of PTQ, keep higher precision on sensitive layers
- Model is already optimal → skip distillation. Document that the full model is the final artifact.

---

## Phase 8: Synthesis & Handoff

**Goal:** Package everything learned into a clear, actionable summary.

**Entry criteria:** At least one model meets success criteria. All experiments documented.

**Steps:**

1. **Summarize findings:**

| Model | Metric | vs Baseline | Compute Cost | Model Size | Notes |
|---|---|---|---|---|---|
| Baseline (LogReg) | F1=0.82 | — | 30s | 2KB | Training only |
| Paper Method A | F1=0.89 | +8.5% | 4h (GPU) | 340MB | Best accuracy |
| Paper Method B | F1=0.87 | +6.1% | 1h (GPU) | 220MB | Good tradeoff |
| Distilled (Student) | F1=0.88 | +7.3% | 6h (distill) | 89MB | 4x smaller |

2. **Recommend production path:**
   - Which model to use and why
   - Deployment requirements (GPU vs CPU, RAM, latency)
   - Monitoring plan (performance drift, data drift)
   - Retraining cadence

3. **Document what didn't work:**
   - Methods tried that underperformed baseline
   - Experiments that failed and why
   - This is often as valuable as what worked

4. **Produce final artifacts:**
   - Trained model file(s) with version
   - Reproducible training script (with seeds)
   - Requirements file with pinned versions
   - Short README for the model card

**Exit criteria:** A written report covering: what was tried, what worked, what didn't, and what to do next.

**Failure modes:**
- Nobody reads the report → keep it to one page. Use the comparison table as the centerpiece.
- No clear winner → present the tradeoffs honestly. Sometimes the answer is "it depends."
- User wants more experiments → document what the next iteration should test and why.
- Results not reproducible → check seed settings, library versions, data splits. Use pinned requirements.

---

## Appendix: Quick Reference

### When to Skip Phases

| If... | Skip to... |
|---|---|
| User only needs a quick answer, not a campaign | Don't use this protocol at all. Use the parent skill's ADVICE or ANALYSIS path. |
| Baseline already beats production | Phase 4 (skip directly to moonshots) |
| Problem is well-studied with known best practice | Phase 4 (skip survey, known method) |
| Model is for edge deployment | Phase 7 (distillation is mandatory) |
| No labeled data available | Phase 1 (reformulate as unsupervised or few-shot) |

### Experiment Directory Structure

```
experiments/
├── campaign.md                   # Problem statement (Phase 1)
├── baselines/                    # Baseline models (Phase 2)
│   └── sklearn_pipeline.pkl
├── survey/                       # Research notes (Phase 3)
│   └── candidate_papers.md
├── runs/                         # Experiment logs (Phase 4-6)
│   ├── run_001_method_a/
│   ├── run_002_method_b/
│   └── optuna_study.db           # HP search results (Phase 6)
├── distillation/                 # Distilled models (Phase 7)
│   └── student_model.pt
├── final/                        # Production artifacts (Phase 8)
│   ├── model.pt
│   ├── model_card.md
│   └── requirements.txt
└── logs/                         # Experiment tracking
    └── experiment_log.json
```

### Always Set Your Seeds

```python
import random, numpy as np, torch

def set_seed(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
```

### Experiment Logging Template

Record every experiment as a structured entry:

```json
{
  "experiment_id": "run_006",
  "date": "2026-05-23",
  "phase": 4,
  "method": "Method B with dropout=0.3",
  "model_class": "TransformerClassifier",
  "params": {"n_layers": 4, "hidden_dim": 256, "dropout": 0.3, "lr": 3e-4, "batch_size": 32},
  "dataset": {"train_size": 10000, "val_size": 2000, "test_size": 2000},
  "results": {"val_f1": 0.871, "test_f1": 0.865, "val_loss": 0.34, "train_time_s": 3600},
  "hardware": {"gpu": "RTX 5070 Ti", "vram_mb": 16384},
  "notes": "Performs well but training is slow. Try reducing hidden_dim."
}
```

---

## See Also

- `scripts/detect-compute.py` — know your hardware before starting Phase 2
- `references/pytorch-integration.md` — training loops, device management, mixed precision
- `references/sklearn-integration.md` — pipelines, model selection, preprocessing
- `references/data-science-coding-workflow.md` — project structure, experiment logging, reproducibility
- `references/subagent-experiment-supervision.md` — self-healing experiment pattern
- `references/docker-experiment-isolation.md` — safe containerized execution
