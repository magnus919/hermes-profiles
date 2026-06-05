# ML Model Quantization & Inference Serving — Reference Manual

> **Purpose:** Engineering methodology reference for production ML serving. Covers quantization approaches, calibration strategies, quality assessment, mixed precision, KV cache optimization, and inference serving architectures.
>
> **Last updated:** 2025-06-05

---

## Table of Contents

1. [Quantization Fundamentals](#1-quantization-fundamentals)
2. [Quantization Approaches Compared](#2-quantization-approaches-compared)
   - 2.1 GGUF
   - 2.2 GPTQ
   - 2.3 AWQ
   - 2.4 bitsandbytes NF4
   - 2.5 EXL2
   - 2.6 HQQ
   - 2.7 Comparison Table
3. [Calibration Data Strategies](#3-calibration-data-strategies)
4. [Quality Impact Assessment](#4-quality-impact-assessment)
5. [Mixed Precision Patterns](#5-mixed-precision-patterns)
6. [KV Cache Quantization](#6-kv-cache-quantization)
7. [Quantization Workflow](#7-quantization-workflow)
8. [Inference Serving Architecture](#8-inference-serving-architecture)
   - 8.1 vLLM
   - 8.2 llama.cpp Server
   - 8.3 Text Generation Inference (TGI)
   - 8.4 Triton Inference Server
   - 8.5 Serving Framework Comparison Table
9. [Production Considerations](#9-production-considerations)
10. [References & Further Reading](#10-references--further-reading)

---

## 1. Quantization Fundamentals

**Quantization** reduces the numerical precision of model weights (and optionally activations / KV cache) from full-precision (FP32, BF16) to lower-bit representations (INT8, INT4, FP8, NF4). This shrinks memory footprint, reduces memory bandwidth pressure, and accelerates inference — especially on bandwidth-bound decode steps.

### Key concepts

| Concept | Description |
|---|---|
| **Weight quantization** | Map each weight tensor's values from a high-precision range into a low-bit grid. Reduces model size by 2-4x at common bit widths. |
| **Activation quantization** | Quantize intermediate activations at runtime. Harder than weight quantization due to dynamic range variation. Common in INT8 pipelines (e.g., TensorRT). |
| **KV cache quantization** | Quantize the key-value cache during autoregressive generation. Critical for long-context serving where KV cache dominates GPU memory. |
| **Symmetric vs. asymmetric** | Symmetric: zero point = 0, range is [-max, max]. Asymmetric: zero point can shift. Asymmetric generally preserves more info for non-normalized distributions. |
| **Per-tensor vs. per-channel (per-group)** | Finer granularity (per-channel or per-group) captures outlier distributions better at the cost of storing more scale/zero-point metadata. |
| **Post-training quantization (PTQ)** | Quantize after training. Dominant paradigm for LLMs given cost of training. |
| **Quantization-aware training (QAT)** | Simulate quantization during training (e.g., FakeQuant ops). More accurate but expensive. Used in some production pipelines (e.g., NVIDIA TensorRT). |

### Why quantize LLMs?

- **Memory:** A 70B model at FP16 requires ~140 GB VRAM. At INT4, ~35 GB — fitting on a single H100/A100-80GB.
- **Throughput:** Lower-precision weights reduce memory bandwidth consumption, which is the primary bottleneck for autoregressive token generation (memory-bound, not compute-bound).
- **Cost:** Enables deployment on cheaper/consumer hardware (RTX 4090, Apple Silicon unified memory, CPU-only).

---

## 2. Quantization Approaches Compared

### 2.1 GGUF

**Type:** File format + quantization scheme  
**Ecosystem:** llama.cpp, Ollama, LM Studio  
**Bit widths:** Q2_K through Q8_0, plus Q4_K_M, Q5_K_M, Q6_K, etc.

GGUF (GPT-Generated Unified Format) is the successor to GGML. It packages a model's weights, tokenizer, and metadata into a single file. The quantization variants use a **k-quant** scheme that assigns different bit widths to different layers based on their importance:

- **Q4_K_M** — recommended sweet spot. Mixture of 4-bit and 6-bit quantization across layers. ~4.5 bits/weight effective.
- **Q5_K_M** — higher quality, ~5.5 bits/weight effective.
- **Q8_0** — near-lossless 8-bit, ~8.5 GB for a 7B model.
- **Q2_K** — aggressive 2-3 bit mix, significant quality loss.

**Key features:**
- Supports CPU inference natively (no GPU required for modest models).
- Can offload layers to GPU via `--n-gpu-layers`.
- Single-file distribution simplifies deployment.
- Supports a wide range of architectures (Llama, Mistral, Falcon, Gemma, etc.).
- **Imatrix** (importance matrix) quantization: weights are quantized with per-layer importance scores, improving quality at a given bit rate.

**Strengths:** Universal format, best CPU/edge support, large pre-quantized Hub ecosystem (TheBloke, etc.), excellent for local/offline use.

**Weaknesses:** Not natively supported by HuggingFace `transformers` or vLLM (though vLLM added GGUF support in 2025). GPU performance trails AWQ/GPTQ on NVIDIA hardware.

---

### 2.2 GPTQ

**Type:** Post-training quantization (weight only)  
**Ecosystem:** AutoGPTQ, HuggingFace optimum, vLLM, TGI  
**Bit widths:** 2-8 bits (most common: 4-bit), supports group size 32/64/128

GPTQ (GPT Post-Training Quantization) uses approximate second-order optimization (Hessian-based) to find weight quantizations that minimize output error. It was the first widely adopted 4-bit LLM quantization method.

**How it works:**
1. Sample a calibration dataset (typically 128 sequences from the training distribution).
2. Compute the approximate Hessian (Fisher information) for each weight column.
3. Quantize weights column-by-column, using the Hessian to prioritize preserving important weights.
4. Update remaining unquantized weights to compensate for quantization error (optimal brain quantization / OBC family).

**Key parameters:**
- **Group size** (g128, g64, g32): Smaller groups = higher accuracy but more scale storage overhead. g128 is common. g64 preferred for quality.
- **Desc_act / act_order** (activation order): When True, reorders columns by activation magnitude. Increases accuracy significantly but reduces speed in older implementations. vLLM's Marlin kernel makes desc_act fast.

**Strengths:** Strong quality at 4-bit, mature ecosystem, widely supported in serving frameworks.

**Weaknesses:** Calibration dataset required (cannot quantize a model from scratch without data). Quantization is slower than AWQ or NF4 due to Hessian computation.

---

### 2.3 AWQ

**Type:** Post-training quantization (weight only)  
**Ecosystem:** AutoAWQ, vLLM, TGI, TensorRT-LLM  
**Bit widths:** 4-bit (most common), also 2-bit, 3-bit variants

AWQ (Activation-Aware Weight Quantization) observes that a small fraction (~1%) of weight channels are "salient" — they handle large activations and are disproportionately important. AWQ protects these channels by scaling them up before quantization, then scaling the output down.

**How it works:**
1. Run a few calibration samples to collect activation statistics.
2. Identify salient channels (those with large activation magnitudes).
3. Apply per-channel scaling factors to redistribute quantization error from salient → non-salient channels.
4. Quantize with simple round-to-nearest.

**Key advantages:**
- **No group size dependency:** AWQ INT4 often matches GPTQ g128 quality without requiring groups, simplifying kernel implementation.
- **Very fast quantization:** Minutes instead of hours. No Hessian computation needed.
- **Excellent GPU kernel support:** Marlin kernel (for GPTQ-compatible AWQ) and AWQ-specific kernels in vLLM achieve near-peak hardware utilization.
- **Good hardware compatibility:** Works well on NVIDIA, AMD, and Apple Silicon via MLX.

**Strengths:** Best quality-to-speed tradeoff at 4-bit, fastest quantize time, strong production support in vLLM.

**Weaknesses:** Primarily designed for 4-bit (less flexible than GGUF's range of bit widths). Requires activation statistics → needs calibration data.

---

### 2.4 bitsandbytes NF4

**Type:** Post-training quantization (weight only)  
**Ecosystem:** HuggingFace `bitsandbytes`, `transformers`, PEFT/LoRA  
**Bit widths:** 4-bit (NF4), 8-bit (INT8)

Bitsandbytes (BnB) is a library from Tim Dettmers that implements efficient GPU quantization kernels. Its 4-bit variant uses **NormalFloat (NF4)** — a non-uniform quantization grid that assumes normally distributed weights.

**Key concepts:**
- **NF4:** A 4-bit data type with 16 levels, non-uniformly spaced to match the cumulative distribution function (CDF) of a normal distribution. This gives higher resolution near zero where most weight values cluster.
- **Double quantization:** Quantizes the quantization constants (scale/offset) themselves to save additional memory. Reduces the 4-bit overhead from ~0.5 bits/weight to ~0.127 bits/weight.
- **QLoRA:** Fine-tune quantized models with LoRA adapters. The base model stays in NF4; only the LoRA parameters are updated in FP16.

**Key features:**
- Native `transformers` integration via `BitsAndBytesConfig` — load any model in 4-bit with a single config object.
- Best for fine-tuning (QLoRA) and rapid prototyping.
- No calibration data needed — quantization is "on the fly" at load time.

**Strengths:** Simplest API, no calibration required, excellent for fine-tuning, HuggingFace-native.

**Weaknesses:** Slower inference than AWQ/GPTQ (dequantization at every forward pass). Kernels are less optimized for serving throughput. Not suitable for high-throughput production serving on its own.

---

### 2.5 EXL2

**Type:** Post-training quantization  
**Ecosystem:** ExLlamaV2  
**Bit widths:** Mixed 2-8 bits per layer

EXL2 is the quantization format for ExLlamaV2, a high-throughput inference engine. It supports mixed-precision within a single model — different layers can use different bit widths.

**Key features:**
- Fine-grained per-layer bit allocation for optimal quality/size tradeoffs.
- Very fast GPU inference — ExLlamaV2 kernels are among the fastest for single-batch inference.
- Less widely supported than GGUF/GPTQ/AWQ but excellent for local GPU use.

**Strengths:** Fastest local GPU inference for many models, flexible per-layer bit allocation.

**Weaknesses:** Smaller ecosystem, primarily desktop/local use. Not widely supported in production serving frameworks.

---

### 2.6 HQQ

**Type:** Post-training quantization  
**Ecosystem:** HuggingFace, independent  
**Bit widths:** 1-8 bits

HQQ (Half-Quadratic Quantization) uses a half-quadratic splitting approach to compute optimal quantization. It's notable for being extremely fast to quantize (no calibration data, no Hessian) and supporting very low bit widths (2-bit, 3-bit).

**Strengths:** Fastest PTQ (no data needed), supports 1-3 bits, good quality at lower bits.

**Weaknesses:** Needs `torch.compile` for reasonable inference speed; otherwise dequantization overhead is high. Less mature ecosystem.

---

### 2.7 Quantization Method Comparison Table

| Property | GGUF (Q4_K_M) | GPTQ (g128) | AWQ | BnB NF4 | EXL2 | HQQ |
|---|---|---|---|---|---|---|
| **Effective bits/weight** | ~4.5 | ~4.125 | ~4.0 | ~4.127 | Variable | 1-8 |
| **File format** | Single .gguf | HF safetensors | HF safetensors | HF safetensors | Custom | HF safetensors |
| **Calibration data req.** | No* | Yes (128 seq) | Yes (128 seq) | No | Yes | No |
| **Quantize speed** | Fast** | Slow (hrs) | Fast (min) | Instant (load) | Moderate | Very fast |
| **GPU inference speed** | Moderate | Fast (Marlin) | Very fast (Marlin) | Slow | Very fast | Moderate |
| **CPU inference** | Native | No | No | No | No | No |
| **Apple Silicon** | Native (MLX) | Via MLX | Via MLX | No | No | Possible |
| **Serving support** | vLLM, llama.cpp | vLLM, TGI | vLLM, TGI, TRT-LLM | Limited | ExLlamaV2 | Limited |
| **Fine-tuning support** | No | No | No | Yes (QLoRA) | No | Possible |
| **Ecosystem maturity** | Very high | High | High | Very high | Moderate | Low |
| **Typical PPL increase (7B)** | +0.15 | +0.10 | +0.10 | +0.20 | +0.10 | +0.12 |

\* GGUF quantization typically does not use calibration data; imatrix quantization does.  
\** Quantization is an explicit step via `llama-quantize` or similar tools (not on-the-fly).

---

## 3. Calibration Data Strategies

Some quantization methods (GPTQ, AWQ, EXL2, imatrix) require a **calibration dataset** — a small set of representative text samples used to compute activation statistics or Hessian information.

### Recommended calibration datasets

| Dataset | Typical Size | Use Case |
|---|---|---|
| **Wikitext-2** | 128 seq × 2048 tokens | Standard benchmark, general text |
| **C4 (Colossal Clean Crawled Corpus)** | 128-256 seq | General web text, diverse |
| **Pile** | 128-256 seq | General, diverse (books, code, academic) |
| **Custom task-specific** | 128-512 seq | Domain adaptation (medical, legal, code) |
| **Random from training data** | 128 seq | Best if available (closest to training distribution) |

### Best practices

1. **Size:** 128-256 sequences of 2048 tokens is typically sufficient. More calibration data has diminishing returns and can even harm quality (overfitting the calibration set).
2. **Diversity:** Calibration data should broadly match the model's training distribution. A model trained on code + text benefits from a calibration mix of both.
3. **Sequences vs. random tokens:** Always use natural text sequences, not random tokens. Random tokens produce meaningless activation statistics.
4. **Avoid duplication:** Deduplicate calibration data. Repeated samples can skew Hessian estimates.
5. **Prompt-like structure:** For instruction-tuned models, including representative prompts in calibration data can improve downstream quality.
6. **Multiple calibration runs:** Some advanced pipelines run calibration on multiple small datasets and average the quantized parameters.

### When calibration data matters most

- **GPTQ** — critically important. Poor calibration data leads to significantly higher perplexity.
- **AWQ** — important but more robust than GPTQ. The scaling factor approach is less sensitive to calibration data quality.
- **GGUF imatrix** — uses importance matrices computed from calibration data. Worth the effort for best-quality GGUF quants.
- **NF4 / HQQ** — no calibration data needed.

---

## 4. Quality Impact Assessment

### Quantization degradation patterns

| Bit Width | Quality Impact |
|---|---|
| **FP16 / BF16** | Baseline (lossless reference) |
| **INT8 (Q8_0, BnB INT8)** | Near-lossless. Negligible PPL increase (<0.01). Output-level differences often undetectable. |
| **6-bit (Q6_K)** | Very minor PPL increase (~0.02). Safe for production. |
| **5-bit (Q5_K_M, Q5_0)** | Small PPL increase (~0.05-0.15). Generally safe. |
| **4-bit (Q4_K_M, GPTQ, AWQ, NF4)** | Moderate PPL increase (~0.10-0.35). Noticeable on complex reasoning tasks. AWS/GPTQ typically best, NF4 worst at same bit width. |
| **3-bit (Q3_K_S, HQQ int3)** | Significant degradation. PPL +0.5-1.5. Tasks requiring multi-step reasoning (CoT) degrade notably. |
| **2-bit (Q2_K)** | Heavy degradation. Only usable for very tolerant tasks. |

### Task-level sensitivity

Not all tasks degrade equally:

| Task Type | Sensitivity | Notes |
|---|---|---|
| **Perplexity / next-token prediction** | Low | Relatively robust to quantization. |
| **Single-token classification (MMLU)** | Low-Moderate | 4-bit typically loses 1-2% accuracy. |
| **Multi-step reasoning (CoT, MATH)** | High | 4-bit can lose 3-5%+ on math reasoning. 3-bit often fails entirely. |
| **Code generation** | Moderate | Functional correctness degrades at aggressive quantization. |
| **Creative writing** | Low | Quality differences are subtle at 4-bit; 3-bit may produce incoherence. |
| **Instruction following** | Moderate | Longer, multi-step instructions become harder at lower precision. |
| **Few-shot learning** | Moderate | Degrades faster than zero-shot performance. |

### Empirical data (Llama 3 8B, from LessWrong benchmarks)

| Method | MMLU (0-shot) | WMDP | The Pile PPL |
|---|---|---|---|
| BF16 (baseline) | 63.87% | 54.99% | 8.283 |
| BnB INT8 | 63.05% | 54.96% | 8.305 |
| HQQ INT8 | 63.87% | 54.66% | 8.298 |
| AWQ INT4 | 61.84% | 54.55% | 8.483 |
| HQQ INT4 | 62.29% | 54.23% | 8.482 |
| GPTQ INT4 | 61.58% | 53.30% | 8.575 |
| BnB NF4 | 61.44% | 54.42% | 8.499 |
| BnB INT4 | 60.80% | 52.73% | 8.633 |
| HQQ INT3 | 62.26% | 51.23% | 8.872 |

> **Key takeaway:** AWQ = GPTQ > HQQ > NF4 > BnB INT4 at 4-bit. At 8-bit, all methods are essentially lossless. Differential sensitivity across tasks means eval should always be task-specific.

### Recommended evaluation framework

1. **Perplexity** — quick sanity check. Compute on withheld validation split (100k tokens minimum).
2. **Task-specific accuracy** — MMLU, HumanEval, GSM8K, or domain-specific benchmarks.
3. **A/B comparison** — Run paired generations from FP16 and quantized model. Human eval or LLM-as-judge for quality differences.
4. **Downstream metric** — For RAG systems, measure retrieval precision. For chatbots, measure response acceptability.

---

## 5. Mixed Precision Patterns

Mixed precision assigns different numerical precisions to different parts of the model or computation graph. This is distinct from per-layer variable-width quantization.

### Common mixed precision patterns

#### 5.1 Weight quantization + high-precision compute

```
Weights: INT4 / NF4
Activations: FP16 / BF16
Gradients (training): FP32
```

- Most common pattern for LLM inference.
- Weights are dequantized on-the-fly to FP16 for computation.
- Offered by AWQ, GPTQ, BnB, GGUF.
- **Tradeoff:** Dequantization overhead. AWQ/GPTQ minimize this via fused kernels (Marlin).

#### 5.2 Low-precision compute (FP8 matmul)

```
Weights: FP8
Activations: FP8
Accumulation: FP16/FP32
```

- NVIDIA H100/H200 supports native FP8 tensor cores (2x throughput vs. FP16).
- TensorRT-LLM and vLLM (FP8 support) use this for high-throughput serving.
- Activation ranges are calibrated (per-tensor or per-channel) at export time.
- Quantization-aware scaling (QTS) ensures accuracy.

#### 5.3 INT8 compute with INT4 weights (W4A8)

```
Weights: INT4
Activations: INT8
Compute: INT8 tensor cores
```

- Emerging pattern for maximum throughput on hardware with INT8 tensor cores (all NVIDIA GPUs since Volta).
- Requires activation quantization at inference time — more complex.
- Used by TensorRT-LLM and some custom serving stacks.

#### 5.4 Per-layer variable precision

```
Layer 1: Q4_K
Layer 5: Q6_K
Layer 14: Q5_K
...
```

- GGUF k-quant and EXL2 use this pattern.
- Sensitive layers (e.g., embedding, lm_head, early/late transformer layers) get higher precision.
- Reduces average bit width without sacrificing critical layers.

#### 5.5 FP16 weights + INT8 KV cache

```
Weights: FP16
KV Cache: INT8/FP8
Compute: FP16/BF16
```

- KV cache is the memory bottleneck for long contexts.
- Quantizing only the KV cache (not weights) saves 50-75% of KV cache memory.
- Supported by vLLM and TensorRT-LLM.

### Precision selection decision tree

```
Is model size > GPU VRAM?
├── YES → Can we tolerate quality loss?
│   ├── YES → INT4 weight quantization (AWQ/GPTQ) + optional KV cache quant
│   └── NO  → FP8 weight quant (if H100) or BF16 with tensor parallelism
└── NO  → Is latency critical?
    ├── YES → INT4 weights + FP16 activations (Marlin kernel)
    └── NO  → BF16 baseline is fine
```

---

## 6. KV Cache Quantization

### The KV cache problem

During autoregressive generation, each transformer layer computes Key (K) and Value (V) tensors that are cached for all previous tokens. For a batch of size `b`, `n_layers` layers, `n_heads` attention heads, sequence length `s`, and dimension `d_per_head`:

```
KV cache size = 2 × b × n_layers × n_heads × s × d_per_head × precision_bytes
```

At FP16, a 32K-token sequence with Llama 3 70B (80 layers, 8 KV heads, d=128) requires ~320 GB for the KV cache alone. Quantizing to INT8 halves this; to INT4 quarters it.

### Attention architecture impact

| Architecture | KV Cache per token (FP16) | Notes |
|---|---|---|
| **MHA** (Multi-Head Attention) | 2 × n_layers × n_heads × d | Largest cache. Every layer has full key/value for all heads. |
| **MQA** (Multi-Query Attention) | 2 × n_layers × 1 × d | One KV head shared across all query heads. 8-32x smaller than MHA. |
| **GQA** (Grouped-Query Attention) | 2 × n_layers × n_kv_heads × d | Middle ground. Llama 2/3 uses 8 KV heads for 32+ query heads. |
| **MLA** (Multi-Head Latent Attention) | 2 × n_layers × d_latent | DeepSeek's approach. Compresses KV into a low-rank latent space. ~2-4x smaller than GQA. |

### KV cache quantization methods

| Method | Bit Width | Strategy |
|---|---|---|
| **KVTuner** | INT4/INT8 | Sensitivity-aware per-layer mixed-precision. Key layers get 8-bit, others 4-bit. |
| **KVQuant** | INT4/FP8 | Per-channel + per-token quantization with non-uniform grids. Targets 10M+ context. |
| **FP8 KV cache** (H100 native) | FP8 | Uses H100 FP8 tensor cores. Minimal quality loss. |
| **INT8 KV cache** (vLLM) | INT8 | Per-tensor symmetric quantization. Standard vLLM feature. |
| **INT4 KV cache** (experimental) | INT4 | Per-channel asymmetric. Quality loss noticeable at very long contexts. |

### Production guidelines

1. **Start with GQA/MLA architecture** — architecture-level KV cache reduction is more impactful than quantization.
2. **FP8 KV cache on H100** — essentially lossless, 2x memory reduction. Enable in vLLM with `--kv-cache-dtype fp8`.
3. **INT8 KV cache** — good tradeoff for A100/H100. Minimal quality impact for contexts under 32K tokens.
4. **INT4 KV cache** — quality impact grows with sequence length. Evaluate carefully for long-context applications.
5. **Layer-wise KV quantization** — tools like KVTuner offer better quality at same average bit width by allocating higher precision to critical layers.

---

## 7. Quantization Workflow

The canonical workflow for applying and validating quantization in production:

### Step 1: Establish Baseline

- Load the model in FP16/BF16.
- Run evaluation benchmark (MMLU, perplexity, domain-specific tasks).
- Record latency and throughput at relevant batch sizes.
- Record VRAM usage.
- This is the reference against which all quantized variants are compared.

### Step 2: Select Quantization Method

Use the comparison table (Section 2.7) to choose based on:
- **Target hardware** (CPU? GPU? Apple Silicon? Cloud instance type?)
- **Deployment framework** (vLLM? llama.cpp? TGI? TensorRT-LLM?)
- **Quality constraints** (must match FP16 within X%?)
- **Compute budget** (time available for quantization)

### Step 3: Quantize

```bash
# GGUF (via llama.cpp)
python3 convert.py --outtype f16 --model ./model --outpath model-f16.gguf
./llama-quantize model-f16.gguf model-q4km.gguf Q4_K_M

# GPTQ (via AutoGPTQ)
python3 -m auto_gptq --model ./model --quantize --bits 4 --group-size 128 --dataset c4

# AWQ (via AutoAWQ)
python3 -m awq.quantize --model_path ./model --quant_path ./awq-model --calib-data wikitext

# BnB NF4 (via transformers — on-the-fly)
# Simply load with BitsAndBytesConfig
```

### Step 4: Evaluate Quality

- **Primary metric:** Same evaluation benchmark as baseline (Step 1).
- **Secondary metric:** Perplexity on a held-out validation set (e.g., The Pile test split).
- **Tertiary metric:** A/B test with LLM-as-judge for generative tasks.
- **Threshold:** Define acceptable degradation (e.g., < 0.5% MMLU drop, < 0.3 PPL increase).

### Step 5: Benchmark Performance

- Measure tokens/second at batch size 1 (latency-sensitive).
- Measure throughput at max batch size (throughput-sensitive).
- Record peak VRAM usage.
- Compare to baseline and to alternative quantization methods.

### Step 6: Select the Winner

| Criteria | Decision |
|---|---|
| Quality within threshold, best throughput | Choose that method |
| Quality outside threshold | Try higher-precision variant (Q4_K_M → Q5_K_M; g128 → g64) |
| All methods fail threshold | Consider FP16 with tensor parallelism, or switch to a different architecture |
| Throughput insufficient | Consider FP8 (if H100) or lower-precision quant with faster kernel |

### Step 7: Production Deployment

- Store quantized model in model registry.
- Configure inference server with appropriate settings.
- Monitor quality metrics continuously (drift detection).
- Set up A/B test vs. previous version.

---

## 8. Inference Serving Architecture

### 8.1 vLLM

**Developed by:** UC Berkeley (Kwatra, Stoica)  
**Language:** Python/C++/CUDA  
**GitHub:** github.com/vllm-project/vllm  
**License:** Apache 2.0

vLLM is the most widely adopted open-source LLM serving framework, known for its combination of throughput and flexibility.

#### Core innovations

**PagedAttention**
- Inspired by OS virtual memory paging.
- KV cache is divided into fixed-size **blocks** (typically 16 or 32 tokens each).
- Blocks are stored in a non-contiguous page table, eliminating fragmentation.
- Enables near-zero memory waste vs. the 60-80% waste in traditional pre-allocated KV cache.
- Allows memory sharing across sequences for techniques like beam search and parallel sampling.

**Continuous Batching**
- Also called **in-flight batching** or **iteration-level batching**.
- Traditional servers wait for all sequences in a batch to finish before starting a new batch.
- Continuous batching adds/removes sequences from the batch **after every iteration** (every decoding step).
- Dramatically improves GPU utilization, especially when sequences have variable lengths.
- vLLM achieves up to **24x higher throughput** than HuggingFace Transformers on the same hardware.

**Chunked Prefill**
- Splits long prefill (prompt processing) into smaller chunks that can interleave with decode steps.
- Prevents long prompts from blocking decode-only sequences.
- Reduces time-to-first-token (TTFT) variability.

**Speculative Decoding**
- Uses a small draft model to propose multiple tokens, verified by the target model in one forward pass.
- 1.5-2.5x latency improvement on latency-sensitive workloads.

#### Key features

| Feature | Status | Notes |
|---|---|---|
| AWQ quantization | ✅ Native | Marlin kernel support |
| GPTQ quantization | ✅ Native | Marlin kernel support |
| GGUF quantization | ✅ Added 2025 | Via llama.cpp backend |
| FP8 (H100) | ✅ Native | Requires H100 |
| KV cache INT8/FP8 | ✅ Native | `--kv-cache-dtype` flag |
| Tensor parallelism | ✅ | Across GPU nodes |
| Pipeline parallelism | ✅ | Limited |
| Prefix caching | ✅ | Automatic KV cache reuse |
| OpenAI-compatible API | ✅ | Drop-in replacement |
| Multi-LoRA serving | ✅ | Efficient LoRA adapter switching |
| Guided decoding | ✅ | JSON schema, grammar |
| Disaggregated prefill/decode | ✅ | 2025 feature |

#### Typical deployment

```bash
# Start vLLM server
python3 -m vllm.entrypoints.openai.api_server \
    --model /path/to/model \
    --quantization awq \
    --dtype auto \
    --max-model-len 8192 \
    --gpu-memory-utilization 0.90 \
    --tensor-parallel-size 2 \
    --enable-prefix-caching
```

#### When to choose vLLM

- **High-throughput production serving** (chatbots, API endpoints).
- **Multi-model or multi-LoRA setups**.
- **OpenAI-compatible API needed**.
- **Heterogeneous GPU setups** (supports various NVIDIA GPUs, AMD ROCm).
- **Need for speculative decoding or prefix caching**.

---

### 8.2 llama.cpp Server

**Developed by:** Georgi Gerganov & community  
**Language:** C/C++  
**GitHub:** github.com/ggml-org/llama.cpp  
**License:** MIT

llama.cpp is a C/C++ inference engine focused on local/edge deployment with minimal dependencies. The `llama-server` component provides an HTTP API.

#### Architecture

- **No external dependencies** — pure C/C++ implementation with BLAS-optimized matrix operations.
- **ggml backend** — custom tensor library supporting CPU, CUDA, Metal, Vulkan, SYCL, and more.
- **Pure CPU inference** — unique among major serving frameworks. Can run 7B models at 10-20 tok/s on modern CPUs with AVX2.
- **GPU offloading** — `--n-gpu-layers N` offloads N transformer layers to GPU. The rest runs on CPU.
- **Quantization-native** — designed from the ground up for GGUF quantized models.

#### Key features

| Feature | Status | Notes |
|---|---|---|
| GGUF quantization | ✅ Native | Full k-quant suite |
| AWQ/GPTQ | ❌ Not native | Via conversions |
| CPU inference | ✅ Best-in-class | AVX2, AVX-512, NEON |
| GPU offloading | ✅ | CUDA, Metal, Vulkan |
| Batch inference | ✅ | Server mode with continuous batching |
| KV cache reuse | ✅ | Automatic |
| OpenAI-compatible API | ✅ | Built into `llama-server` |
| Grammar sampling | ✅ | GBNF grammar engine |
| Embedding endpoint | ✅ | Via `/v1/embeddings` |
| Vision (multimodal) | ✅ | Llava, etc. |
| Structured output | ✅ | JSON schema mode |

#### Typical deployment

```bash
./llama-server \
    --model /path/to/model.gguf \
    --host 0.0.0.0 \
    --port 8080 \
    --n-gpu-layers 32 \
    --threads $(nproc) \
    --ctx-size 8192 \
    --rope-scaling yarn \
    --cache-type-k q8_0 \
    --cache-type-v q8_0
```

#### When to choose llama.cpp

- **CPU-only or hybrid CPU/GPU deployments**.
- **Apple Silicon** (Metal backend is excellent).
- **Local/edge inference** (privacy-sensitive, offline).
- **Single-user or low-concurrency serving**.
- **Experimentation** (fastest iteration for trying different quant levels).
- **No dependency on Python or CUDA toolkit**.

---

### 8.3 Text Generation Inference (TGI)

**Developed by:** Hugging Face  
**Language:** Rust/Python  
**GitHub:** github.com/huggingface/text-generation-inference  
**License:** Apache 2.0

TGI is Hugging Face's production-grade inference server, used to power HuggingChat and the Hugging Face Inference API.

#### Architecture

- **Rust core** for HTTP routing and request management (high concurrency, low overhead).
- **Python/CUDA backend** for model execution.
- **Flash Attention 2** integration for efficient attention computation.
- **PagedAttention** added in v2.x (also called "Paged Attention in TGI").
- **Continuous batching** similar to vLLM.
- **Safetensors** and `transformers` integration — loads models directly from Hugging Face Hub.

#### Key features

| Feature | Status | Notes |
|---|---|---|
| AWQ quantization | ✅ | Via optimum |
| GPTQ quantization | ✅ | Via optimum |
| FP8 quantization | ✅ | H100 support |
| Bitsandbytes | ✅ | Via transformers |
| Tensor parallelism | ✅ | |
| Flash Attention 2 | ✅ | Default |
| PagedAttention (v2.x) | ✅ | Added after vLLM |
| Watermarking | ✅ | SynthID-Text |
| Message API | ✅ | Native chat templates |
| Streaming | ✅ | Server-Sent Events |
| Speculative decoding | ✅ | |

#### Typical deployment

```bash
docker run --gpus all \
    -p 8080:80 \
    -v /path/to/models:/data \
    ghcr.io/huggingface/text-generation-inference:latest \
    --model-id /data/model \
    --max-total-tokens 8192 \
    --quantize awq \
    --num-shard 2
```

#### When to choose TGI

- **Deep HuggingFace ecosystem integration** (Hub, optimum, tokenizers).
- **Production serving with AWS Inferentia** (TGI has native Inferentia2 support).
- **Message-based chat APIs** (native chat template handling).
- **When watermarking or model-level guardrails are needed**.

---

### 8.4 Triton Inference Server

**Developed by:** NVIDIA  
**Language:** C++/CUDA (backend), Python (frontend)  
**GitHub:** github.com/triton-inference-server/server  
**License:** BSD-3-Clause

Triton is NVIDIA's production inference server. It is model-framework-agnostic and designed for enterprise-grade deployments.

#### Architecture

- **Multi-framework backend:** Supports TensorRT, TensorRT-LLM, PyTorch, ONNX Runtime, vLLM, Python, and custom backends.
- **Concurrent model serving:** Multiple models (and multiple versions of the same model) served from a single instance.
- **Ensemble scheduler:** Chain multiple models together without custom code (e.g., embedding → re-rank → LLM).
- **Dynamic batching:** Client-side and server-side batching with configurable timeouts.
- **GPU/CPU/accelerator support:** Concurrent serving across heterogeneous hardware.
- **Prometheus metrics:** Native monitoring endpoint.

#### TensorRT-LLM backend

The TensorRT-LLM backend is the primary LLM serving path within Triton:

1. **Model optimization phase:** Convert model to TensorRT engine (FP16, INT8, INT4, FP8).
2. **Graph optimizations:** Kernel fusion, layer fusion, attention optimization.
3. **In-flight batching:** Equivalent to continuous batching.
4. **PagedAttention:** Adopted from vLLM's approach.
5. **Multi-node tensor parallelism:** Up to hundreds of GPUs.

#### Key features

| Feature | Status | Notes |
|---|---|---|
| Multi-framework | ✅ | Not just LLMs |
| TensorRT-LLM backend | ✅ | Highest throughput on H100 |
| INT4/FP8/INT8 quantization | ✅ | Through TensorRT |
| PagedAttention | ✅ | Via TensorRT-LLM |
| In-flight batching | ✅ | |
| Dynamic batching | ✅ | Server-side |
| Ensemble inference | ✅ | Pipeline multiple models |
| Concurrent model versions | ✅ | A/B test, gradual rollout |
| Model repository | ✅ | Pull models at startup |
| Prometheus monitoring | ✅ | |
| Custom metrics | ✅ | |
| Decoupled API | ✅ | Streaming responses |
| Request prioritization | ✅ | QoS support |

#### Typical deployment

```yaml
# Model repository structure
model_repository/
  ensemble_model/
    1/
      model.py (ensemble definition)
  tensorrt_llm/
    1/
      config.pbtxt
      model.engine
  embedding_model/
    1/
      config.pbtxt
      model.plan
```

```bash
docker run --gpus all --shm-size=4g \
    -p 8000:8000 -p 8001:8001 -p 8002:8002 \
    -v /path/to/model_repo:/models \
    nvcr.io/nvidia/tritonserver:24.12-trtllm-python-py3 \
    tritonserver --model-repository=/models
```

#### When to choose Triton

- **Enterprise production serving** (SLOs, multi-model, heterogeneous hardware).
- **Multi-model pipelines** (embed → re-rank → generate).
- **Multi-framework environments** (mixing TensorRT, PyTorch, ONNX).
- **High-performance LLM serving on H100/H200 clusters** (TensorRT-LLM path).
- **Need for request prioritization, A/B testing, multi-version serving**.
- **Kubernate-native deployments** (Triton has first-class K8s support).

---

### 8.5 Serving Framework Comparison

| Property | vLLM | llama.cpp Server | TGI | Triton + TRT-LLM |
|---|---|---|---|---|
| **Language** | Python/C++/CUDA | C/C++ | Rust/Python/CUDA | C++/CUDA |
| **Primary hardware** | NVIDIA GPU (+ AMD, Intel) | CPU, Apple, any GPU | NVIDIA GPU | NVIDIA GPU |
| **Best quantization** | AWQ, GPTQ, FP8 | GGUF (all k-quants) | AWQ, GPTQ, FP8 | INT4/FP8 via TRT |
| **Throughput (7B)** | Very high | Moderate | High | Highest (on H100) |
| **Latency (single request)** | Low | Low | Low | Very low |
| **CPU-only support** | No | Yes (best) | No | No |
| **Apple Silicon** | No | Yes (Metal) | No | No |
| **Multi-model serving** | Limited | No (one model) | No (one model) | Yes (full) |
| **Ensemble pipelines** | No | No | No | Yes |
| **OpenAI API compat** | ✅ Native | ✅ Built-in | ✅ Native | Requires NIM |
| **Ecosystem** | OSS community | OSS community | HuggingFace | NVIDIA |
| **License** | Apache 2.0 | MIT | Apache 2.0 | BSD-3 |

---

## 9. Production Considerations

### Model registry & versioning

- Store quantized models alongside their FP16 originals in a model registry (e.g., MLflow, HuggingFace Hub, S3).
- Tag each quantized model with: base model version, quantization method, bit width, calibration dataset, validation metrics.
- Never overwrite a quantized model — always create a new version.

### A/B testing in production

- Serve both FP16 and quantized variants simultaneously.
- Route a fraction of traffic to each variant.
- Compare quality (user feedback, downstream metrics), latency (p50, p95, p99), and throughput.
- Gradual rollout: 5% → 25% → 50% → 100%.

### Monitoring

| Metric | What to Watch | Alert Threshold |
|---|---|---|
| **p50/p99 TTFT** | Time to first token | +30% from baseline |
| **p50/p99 TPOT** | Time per output token | +20% from baseline |
| **Throughput** | Tokens/second | <80% of expected |
| **GPU memory utilization** | VRAM usage | >95% persistent |
| **KV cache utilization** | vs. allocated | >90% (good) |
| **Error rate** | 4xx/5xx responses | >1% |
| **Perplexity (eval)** | Quality drift | +0.5 from baseline |
| **Generation quality** | LLM-as-judge or human eval | Periodic |

### Hardware selection guide

| Deployment | Recommended Hardware | Recommended Setup |
|---|---|---|
| **Single user, local** | RTX 4090 (24 GB) | 7-13B, Q4_K_M GGUF, llama.cpp |
| **Low concurrency API** | A100-40GB or RTX 6000 | 7-13B, AWQ, vLLM |
| **Mid-scale production** | A100-80GB (x2-4) | 70B, AWQ/GPTQ, vLLM, TP=2-4 |
| **High-scale production** | H100-80GB (x8+) | 70B-405B, FP8/INT4, TRT-LLM, TP=8 |
| **Edge / CPU-only** | Modern x86 with AVX-512 | 7B, Q4_K_M, llama.cpp |
| **Apple Silicon** | M2 Ultra / M4 Ultra | 7-13B, GGUF, llama.cpp Metal |
| **Cost-sensitive** | L4 (24 GB) | 7-13B, AWQ, vLLM |

### Memory budget calculation

For a model with `P` parameters, quantized to `B` bits/weight:

```
Model weights:   P × B / 8 bytes
KV cache:        2 × n_layers × n_kv_heads × head_dim × max_seq_len × 2 (FP16) bytes
Activations:     ~20% of model weights (rough estimate)
Overhead:        CUDA context, framework, ~1-2 GB
```

Example — Llama 3 70B, AWQ INT4, seq_len 8192, batch_size 1:
```
Weights:   70B × 0.5 = ~35 GB
KV cache:  2 × 80 × 8 × 128 × 8192 × 2 = ~2.7 GB
Activations + overhead: ~8 GB
Total:     ~46 GB → fits on a single A100-80GB or H100
```

### Cold start / warm-up

- Quantized models may produce garbage tokens for the first few inference steps (cold-start artifacts).
- Always run a warm-up prompt (e.g., "Hello") before production traffic.
- For serverless deployments, keep a warm standby or use model repository pre-loading.

### Throughput vs. latency tradeoffs

| Configuration | TTFT | TPOT | Throughput | Use Case |
|---|---|---|---|---|
| Batch size 1 | Lowest | Moderate | Lowest | Real-time chat |
| Max batch, parallel | Higher | Higher | Highest | Offline batch |
| Chunked prefill | Moderate | Moderate | High | Mixed workloads |
| Speculative decoding | Low | Low | Moderate | Latency-sensitive |

### Security considerations

- **GGUF models are executable files** — only load from trusted sources. A malicious GGUF can execute arbitrary code.
- **Safetensors** (used by AWQ/GPTQ) are safer but not invulnerable.
- Validate model provenance:
  - Check SHA256 hashes against published values.
  - Only load from trusted registries (HuggingFace verified orgs, internal registry).
- Harden the inference server:
  - Run as non-root user.
  - Use network isolation (no external access for the server).
  - Rate-limit API endpoints.

---

## 10. References & Further Reading

### Foundational papers

- **GPTQ:** Frantar et al., "GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers" (2023) — [arXiv:2210.17323](https://arxiv.org/abs/2210.17323)
- **AWQ:** Lin et al., "AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration" (2024) — [arXiv:2306.00978](https://arxiv.org/abs/2306.00978)
- **Bitsandbytes / NF4 / QLoRA:** Dettmers et al., "QLoRA: Efficient Finetuning of Quantized Language Models" (2023) — [arXiv:2305.14314](https://arxiv.org/abs/2305.14314)
- **PagedAttention:** Kwon et al., "Efficient Memory Management for Large Language Model Serving with PagedAttention" (2023) — [arXiv:2309.06180](https://arxiv.org/abs/2309.06180)
- **vLLM performance analysis:** "Anatomy of a High-Throughput LLM Inference System" (2025) — [vLLM Blog](https://vllm.ai/blog/2025-09-05-anatomy-of-vllm)
- **KV cache quantization (KVTuner):** Liu et al., "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization" (2025) — [OpenReview](https://openreview.net/forum?id=zDwipF6h06)
- **MLA:** "TransMLA: Multi-head Latent Attention Is All You Need" (2025) — [arXiv:2502.07864](https://arxiv.org/abs/2502.07864)

### Guides & benchmarks

- "Which Quantization Method is Right for You (GPTQ vs. GGUF vs. AWQ)" — [Maarten Grootendorst](https://newsletter.maartengrootendorst.com/p/which-quantization-method-is-right)
- "Comparing Quantized Performance in Llama Models" (2024) — [LessWrong](https://www.lesswrong.com/posts/qmPXQbyYA66DuJbht/comparing-quantized-performance-in-llama-models)
- "The Complete Guide to LLM Quantization with vLLM" (2026) — [Jarvis Labs](https://jarvislabs.ai/blog/vllm-quantization-complete-guide-benchmarks)
- "An Empirical Study of Qwen3 Quantization" (2025) — [arXiv:2505.02214](https://arxiv.org/abs/2505.02214)
- "LLM Inference at scale with TGI" (2024) — [HuggingFace Blog](https://huggingface.co/blog/martinigoyanes/llm-inference-at-scale-with-tgi)
- "Continuous Batching: The Single Biggest GPU Utilization Unlock" (2026) — [Tian Pan](https://tianpan.co/blog/2026-04-09-continuous-batching-llm-inference)

### Tools & repositories

- **vLLM** — [github.com/vllm-project/vllm](https://github.com/vllm-project/vllm)
- **llama.cpp** — [github.com/ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)
- **TGI** — [github.com/huggingface/text-generation-inference](https://github.com/huggingface/text-generation-inference)
- **TensorRT-LLM** — [github.com/NVIDIA/TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM)
- **Triton Inference Server** — [github.com/triton-inference-server/server](https://github.com/triton-inference-server/server)
- **AutoGPTQ** — [github.com/PanQiWei/AutoGPTQ](https://github.com/PanQiWei/AutoGPTQ)
- **AutoAWQ** — [github.com/casper-hansen/AutoAWQ](https://github.com/casper-hansen/AutoAWQ)
- **bitsandbytes** — [github.com/bitsandbytes-foundation/bitsandbytes](https://github.com/bitsandbytes-foundation/bitsandbytes)
- **ExLlamaV2** — [github.com/turboderp/exllamav2](https://github.com/turboderp/exllamav2)
- **Awesome LLM Quantization** — [github.com/pprp/awesome-llm-quantization](https://github.com/pprp/awesome-llm-quantization)

---

> **End of reference document.** This is a living document — update benchmarks and framework versions as the ecosystem evolves.
