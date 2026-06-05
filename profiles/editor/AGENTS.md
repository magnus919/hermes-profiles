# Editor Profile — Agent Guidance

## Trigger Patterns

| User Says | What It Means |
|---|---|
| "Edit this draft" | Full editorial review: structure → argument → voice → engagement → report |
| "Fact-check this" | Targeted fact-checking pass |
| "Check the voice consistency" | Voice audit focused on register and tone |
| "Review for engagement" | Engagement assessment focused on reader attention |

## Loading Order

```python
skill_view('artifact-pyramids')
skill_view('editor-methodology')
skill_view('editor-review-methodology')
```

## Output Contract

Artifact pyramid. Response is the absolute path to `00-index.md`.
