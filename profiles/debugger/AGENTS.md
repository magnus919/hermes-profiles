# Debugger Profile — Agent Guidance

## Trigger Patterns

| User Says | What It Means |
|---|---|
| "Debug this error" | Full investigation: reproduce → isolate → root cause → fix → verify |
| "Investigate this crash" | Crash analysis with stack trace and reproduction steps |
| "Why is X slow?" | Performance investigation with profiling and bottleneck identification |
| "This test is flaky" | Flaky test diagnosis with pattern analysis |

## Loading Order

```python
skill_view('artifact-pyramids')  # 1. Output format
```

## Output Contract

Artifact pyramid. Response is the absolute path to `00-index.md`.
