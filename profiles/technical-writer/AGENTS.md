# Technical Writer Profile — Agent Guidance

## Trigger Patterns

| User Says | What It Means |
|---|---|
| "Write a README for X" | Full README: overview → quickstart → install → config → usage → contributing |
| "Document this API" | API reference: endpoints → parameters → examples → errors → auth |
| "Write an AGENTS.md" | Agent-facing docs: trigger patterns → loading order → output contract |
| "Write CLI help text" | CLI documentation: usage line → flags → env vars → exit codes → examples |
| "Restructure the docs" | Documentation audit: information architecture → cross-referencing → gaps |
| "Write a developer guide" | How-to guide: prerequisites → steps → verification → troubleshooting |

## Loading Order

```python
skill_view('artifact-pyramids')          # 1. Output format
skill_view('technical-documentation')    # 2. Methodology
```

## Output Contract

Artifact pyramid. Response is the absolute path to `00-index.md`.
