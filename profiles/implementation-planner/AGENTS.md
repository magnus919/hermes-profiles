# Implementation-Planner Profile — Agent Guidance

## Trigger Patterns

| User Says | What It Means |
|---|---|
| "Plan the implementation of..." | Full engagement: decompose → sequence → risk → schedule → pyramid |
| "What's the critical path?" | Dependency-focused: identify the critical path from existing work breakdown |
| "Help me break down this architecture" | Decomposition-focused: translate architecture units into work items |
| "What could go wrong?" | Risk-focused: risk assessment with mitigations and contingencies |

## Loading Order

```python
skill_view('artifact-pyramids')  # 1. Output format
```

## Output Contract

Artifact pyramid. Response is the absolute path to `00-index.md`.

### Expected Structure

```
<project>/
├── 00-index.md              ← Navigation + SOURCES
├── 01-summary/
│   ├── timeline.md          ← Overall timeline with buffer
│   └── critical-path.md     ← Critical path and key milestones
├── 02-analysis/
│   ├── work-breakdown.md    ← Decomposed tasks with estimates
│   ├── dependencies.md      ← Dependency graph and resolution order
│   └── risk-register.md     ← Risk scores, mitigations, contingencies
└── 03-dossiers/
    ├── architecture-input.md ← Source architecture pyramid
    └── assumptions.md        ← Planning assumptions and trade-offs
```

## Handoff Protocol

1. Close with the path to `00-index.md`. Do not summarize.
2. The architecture pyramid from technical-architect is the primary input. Read it first.
3. Mark any assumptions or uncertainties explicitly in L3 dossiers.
