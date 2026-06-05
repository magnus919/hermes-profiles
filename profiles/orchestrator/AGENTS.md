# Orchestrator Profile — Agent Guidance

## Trigger Patterns

| User Says | What It Means |
|---|---|
| "Orchestrate this work" | Full orchestration: decompose → route → monitor → synthesize |
| "How should I sequence these specialists?" | Routing assessment focused on specialist ordering |
| "Combine these findings" | Synthesis-focused: merge multiple specialist outputs |

## Loading Order

```python
skill_view('artifact-pyramids')
skill_view('orchestration-methodology')
```

## Output Contract

Artifact pyramid. Response is the absolute path to `00-index.md`.
