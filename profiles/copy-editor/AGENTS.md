# Copy-Editor Profile — Agent Guidance

## Trigger Patterns

| User Says | What It Means |
|---|---|
| "Copy-edit this draft" | Full copy-editing: style → grammar → consistency → proofread |
| "Proofread this" | Final surface check only |
| "Check this for consistency" | Consistency-focused pass (formatting, terminology, capitalization) |

## Loading Order

```python
skill_view('artifact-pyramids')
skill_view('copy-editor-methodology')
```

## Output Contract

Artifact pyramid. Response is the absolute path to `00-index.md`.
