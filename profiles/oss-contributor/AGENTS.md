# OSS-Contributor Profile — Agent Guidance

## Trigger Patterns

| User Says | What It Means |
|---|---|
| "Contribute to this project" | Full workflow: assess → fork → branch → implement → PR |
| "File a bug report for X" | Issue-focused: reproduction, environment, expected behavior |
| "Review their CONTRIBUTING.md" | Project norms assessment |
| "Open a cross-fork PR" | Fork name differs from upstream — requires API workaround |

## Loading Order

```python
skill_view('artifact-pyramids')
skill_view('opensource-contributions')
```

## Output Contract

Artifact pyramid. Response is the absolute path to `00-index.md`.
