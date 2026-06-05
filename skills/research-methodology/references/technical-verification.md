# Technical Verification Track

For claims that can be tested by doing — running code, querying APIs, checking benchmarks, measuring yourself. The most credible evidence is evidence you can reproduce.

## The Core Principle

If a claim rests on a number, benchmark, or observable behavior, and you have the tools to test it, do not rely on the source's claim. Test it yourself. Your own measurement, properly conducted, is a tier-1 source.

## What to Verify by Testing

| Claim type | Test method | Tool |
|------------|-------------|------|
| **Performance numbers** (latency, throughput, VRAM usage) | Reproduce the benchmark with the same parameters | Terminal, Python scripts |
| **API behavior** ("the API returns X when Y") | Call the API with the documented parameters | curl, Python httpx |
| **Model outputs** ("Model A beats Model B on X") | Run the same prompt through both models | llama.cpp, OpenRouter API |
| **Configuration claims** ("Set flag X for best results") | Try it with and without the flag, compare | Terminal, A/B testing |
| **Memory/disk usage** ("This uses less than X") | Build the system, measure actual usage | `du`, `ps`, `nvidia-smi`, `htop` |
| **Availability claims** ("The protocol supports Y") | Read the spec, then try to do it | Source code, protocol docs, actual implementation |
| **Compatibility claims** ("Works on macOS and Linux") | Test on both platforms or verify per-platform CI results | CI logs, Docker |

## The Reproduction Standard

### Step 1: Read the claim carefully
What, exactly, does the source claim? Write down the specific numbers, flags, parameters, and conditions.

### Step 2: Replicate the conditions
Use the same:
- Model version / software version
- Hardware (or comparable)
- Configuration flags
- Input data (or equivalent)
- Measurement methodology

If the source doesn't specify conditions fully, note what's missing. A benchmark that doesn't specify GPU driver version, CUDA version, or `nvidia-smi` output is incomplete.

### Step 3: Run the test
Run it once and observe. Then run it again. Then a third time. Variability across runs is itself data.

### Step 4: Compare results

| Situation | What it means |
|-----------|--------------|
| Your result matches the claim within expected variance | Claim verified — high confidence |
| Your result differs significantly | Either the claim is wrong, or your conditions differ. Check conditions, then report the discrepancy |
| You can't reproduce at all | Claim is unverifiable with available resources. Flag it |
| Your result is better than the claim | Interesting — may mean setup differences, or the claim was conservative |

### Step 5: Document the reproduction

```
## Verification

- Claim tested: [exact claim from source]
- My results: [numbers]
- Conditions: [hardware, software, flags, methodology]
- Variance across runs: [min/max/mean across N runs]
- Verdict: Verified / Partially supported / Contradicted / Unverifiable
- Notes: [any caveats about the test conditions]
```

## When Testing Isn't Feasible

Some claims can't be tested with available resources (requires $10K of cloud credits, proprietary hardware, or access to a system you don't have). In these cases:

1. **Find independent reproductions.** Has someone else tested the same claim? Look for replication studies, community benchmarks, or forum discussions.
2. **Read the methodology critically.** If you can't test it yourself, audit the testing methodology. Was the sample size adequate? Were confounding variables controlled? Was there a conflict of interest?
3. **Flag untested claims in the draft.** "This benchmark was conducted by the vendor and has not been independently verified" is honest and keeps you protected.

## The "I Built It" Standard

For technical tutorials and walkthroughs (like "Running a 35B MoE Model on a 16GB Consumer GPU"):

- Every configuration flag in the article must have been tested by the author
- Every command in the article must produce the stated output
- Every screenshot or terminal output must be from the author's own system
- No "should work" — only "worked for me under these conditions"
- If a configuration didn't work, say so and explain why

This is the standard that distinguishes Magnus's technical writing from generic tutorials. The mistakes and dead ends are the value.
