# Model Evaluation

## Benchmark Selection

| What you want to measure | Recommended benchmarks |
|--------------------------|----------------------|
| General reasoning | MMLU-Pro, GPQA, ARC-Challenge |
| Code generation | HumanEval+, SWE-Bench, BigCodeBench |
| Instruction following | MT-Bench, AlpacaEval, Arena-Hard |
| Tool calling | BFCL, ToolBench, jdhodges tool-call eval |
| Safety | TruthfulQA, BBQ, ToxiGen |
| Math | GSM8K, MATH, AIME |

## Custom Eval Design

When off-the-shelf benchmarks don't capture your domain:

1. **Collect 50-200 representative examples** from your actual use cases
2. **Define a scoring rubric** — what constitutes correct, partially correct, and incorrect
3. **Include adversarial examples** — edge cases, ambiguous inputs, known failure modes
4. **Run baseline (base model) first** — establish the ceiling before fine-tuning
5. **Track per-example** — aggregate scores hide regressions in specific capabilities

## Regression Tracking

| Before change | After change | Interpretation |
|---|---|---|
| Score A | Score A ± noise | No detectable effect |
| Score A | Score A - delta | Regression — investigate |
| Score A | Score A + delta | Improvement — verify on held-out set |
| Score A, B regressed | Score A + delta, B regressed | Tradeoff — intentional? |
