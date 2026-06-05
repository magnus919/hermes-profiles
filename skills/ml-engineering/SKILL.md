---
name: ml-engineering
description: "Machine learning engineering methodology — model training, fine-tuning (LoRA/QLoRA), evaluation, quantization, deployment, and MLOps pipeline design. Grounded in practical engineering patterns for production ML systems."
version: 1.0.0
author: Hermes Agent community
license: MIT
metadata:
  hermes:
    tags: [ml, machine-learning, fine-tuning, training, evaluation, quantization, mlops]
    related_skills: [data-scientist, platform-engineering, site-reliability-engineering]
---

# ML Engineering Methodology

Machine learning engineering is the bridge between model research and production systems. This methodology covers the engineering disciplines needed to train, evaluate, deploy, and maintain ML models reliably.

## The ML Engineer's Domain

| You own | You don't own |
|---------|--------------|
| Model training — LoRA/QLoRA fine-tuning, full fine-tuning, distributed training | Statistical modeling and experimental design — that's the data scientist |
| Model evaluation — benchmark suites, custom eval sets, regression testing | Causal inference and hypothesis testing — that's the data scientist |
| Quantization — GGUF, GPTQ, AWQ, bitsandbytes | Training data collection and labeling — that's the data/ML ops team |
| Inference serving — vLLM, llama.cpp, TGI, Triton | Business metrics and KPI definition — that's the product manager |
| Evaluation harness — lm-eval-harness, custom pipelines | Data pipeline architecture — that's the data engineer |
| Model deployment — containerization, versioning, A/B testing | Infrastructure provisioning — that's the platform engineer |

## Reference Files

| Reference | When to load |
|-----------|-------------|
| `references/fine-tuning.md` | Setting up a LoRA/QLoRA/ full fine-tuning run — data prep, hyperparameters, validation strategy |
| `references/evaluation.md` | Evaluating a model — benchmark selection, custom eval sets, regression tracking, comparison methodology |
| `references/quantization.md` | Quantizing a model — GGUF conversion, GPTQ/AWQ, calibration data, quality-impact assessment |
| `references/inference-serving.md` | Deploying a model for inference — vLLM, llama.cpp, TGI, batch vs streaming, concurrency |
| `references/training-infrastructure.md` | Selecting and provisioning training infrastructure — GPU selection, multi-GPU training, cloud vs on-prem |

## Core Principles

**Measure before you optimize** — Never quantize, prune, or distill a model without first measuring its baseline performance. Optimization without measurement is guessing.

**Reproducibility is non-negotiable** — Every training run needs a reproducible config: seed, data version, hyperparameters, and evaluation methodology. If you can't reproduce it, you can't ship it.

**Baseline first** — Before running an expensive fine-tuning run, establish a baseline with the base model. If the base model is already good enough, the fine-tuning budget is better spent elsewhere.

**Test at the boundary** — Model evaluation is most informative at the edges of the capability distribution, not at the center. Hard examples reveal more than easy ones.

**The evaluation set is a liability** — Every example in your eval set is a potential test-set leak. Use held-out sets, rotate examples, and periodically audit for contamination.
