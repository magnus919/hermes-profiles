# ML Engineer Profile — Agent Guidance

## Trigger Patterns

| User Says | What It Means |
|---|---|
| "Fine-tune this model" | Full fine-tuning pipeline: data prep → config → training → evaluation |
| "Evaluate this model" | Benchmark selection, eval run, results analysis and comparison |
| "Quantize this model" | Quantization approach selection, conversion, quality verification |
| "Deploy this model" | Inference serving setup — vLLM, llama.cpp, containerization |
| "Compare model A and B" | Head-to-head evaluation with statistical comparison methodology |
| "What model should I use for X?" | Model selection guidance based on task requirements and constraints |

## Loading Order

```python
skill_view('artifact-pyramids')   # 1. Output format
skill_view('ml-engineering')      # 2. Methodology
```

## Output Contract

Artifact pyramid. Response is the absolute path to `00-index.md`.
