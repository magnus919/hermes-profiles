# Reviewer Profile — Agent Guidance

## Trigger Patterns

| User Says | What It Means |
|---|---|
| "Review this PR" | Full review: understand → evaluate → verify → report → pyramid |
| "Audit this for security" | Security-focused review with vulnerability assessment |
| "Check this for regressions" | Regression-focused review against known patterns |
| "Verify this against standards" | Compliance review against documented conventions |

## Loading Order

```python
skill_view('artifact-pyramids')  # 1. Output format
```

## Output Contract

Artifact pyramid. Response is the absolute path to `00-index.md`.
