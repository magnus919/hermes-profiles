# Fine-Tuning

## Approach Selection

| Approach | When to use | VRAM | Data needed |
|----------|-------------|------|-------------|
| LoRA | Adapting to a new domain/task, limited VRAM | 8-16 GB for 7B | 100-10K examples |
| QLoRA | Very limited VRAM, large base model | 6-12 GB for 7B | 100-10K examples |
| Full fine-tune | Maximum capability shift, sufficient VRAM | 40-80 GB for 7B | 10K+ examples |
| DoRA | Weight-decomposed adaptation, better than LoRA | +5% over LoRA | Same as LoRA |

## Training Config Checklist

- [ ] Seed set for reproducibility
- [ ] Learning rate schedule selected (cosine, linear, constant)
- [ ] Warmup steps configured (typically 5-10% of total)
- [ ] Gradient accumulation steps set
- [ ] Mixed precision (bf16/fp16) enabled if hardware supports
- [ ] Evaluation during training (every N steps)
- [ ] Checkpoint saving with best-model tracking (eval loss)
- [ ] WandB or local logging configured
- [ ] Data shuffled before each epoch
- [ ] Train/validation split verified (no cross-contamination)

## Validation Strategy

| Data regime | Validation approach |
|-------------|-------------------|
| < 500 examples | K-fold cross-validation (k=5) |
| 500-10K | 80/10/10 train/val/test split |
| 10K+ | 90/5/5 split with stratified sampling |
| Imbalanced classes | Stratified split by class distribution |
