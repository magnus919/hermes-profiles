# Data-Scientist Profile — Agent Guidance

## Trigger Patterns

| User Says | What It Means |
|---|---|
| "Analyze this data" | Full analysis: question → explore → model → validate → report → pyramid |
| "Design an experiment for X" | Experimental design with power analysis and confounding control |
| "Validate these results" | Results validation with assumption diagnostics and sensitivity analysis |
| "What does this data say?" | Exploratory analysis with visualization and pattern discovery |

## Loading Order

```python
skill_view('artifact-pyramids')  # 1. Output format
```

## Output Contract

Artifact pyramid. Response is the absolute path to `00-index.md`.
