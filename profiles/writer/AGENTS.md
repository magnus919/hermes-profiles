# Writer Profile — Agent Guidance

## Trigger Patterns

| User Says | What It Means |
|---|---|
| "Draft a post about X" | Full writing engagement: outline → draft → revise → pyramid |
| "Write documentation for Y" | Technical writing with audience-appropriate depth |
| "Edit this draft" | Revision pass focused on structure, clarity, and voice |
| "Write a spec for Z" | Structured requirements document |

## Loading Order

```python
skill_view('artifact-pyramids')  # 1. Output format
```

## Output Contract

Artifact pyramid. Response is the absolute path to `00-index.md`.
