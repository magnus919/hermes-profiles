---
name: debugging-methodology
description: "Systematic debugging methodology — root cause analysis, error reproduction, isolation techniques, and verification protocols."
version: 1.0.0
author: Hermes Agent community
license: MIT
metadata:
  hermes:
    tags: [debugging, root-cause, reproduction, error-investigation]
---

# Debugging Methodology

Systematic process for investigating and resolving software defects.

## The Debugging Lifecycle

```
REPRODUCE → ISOLATE → ROOT CAUSE → FIX → VERIFY
```

## Reference Files

| Reference | When to load |
|-----------|-------------|
| `references/reproduction-checklist.md` | You need to reproduce an intermittent or environment-specific failure |
| `references/root-cause-analysis.md` | You've isolated the symptom and need to trace to root cause |
| `references/isolation-techniques.md` | You need to narrow down a failure across multiple components |
| `references/performance-debugging.md` | Investigating latency, memory, or throughput issues |
