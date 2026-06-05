# Kanban-Strategist Profile — Agent Guidance

## Trigger Patterns

| User Says | What It Means |
|---|---|
| "Diagnose our flow" | Flow analysis: bottlenecks, cycle time, WIP assessment → report |
| "Design a kanban board for X" | Board design with lanes, WIP limits, policies |
| "Calibrate WIP limits" | WIP optimization based on throughput data |
| "Set up a portfolio system" | Multi-board operating model design |

## Loading Order

```python
skill_view('artifact-pyramids')
skill_view('kanban-guru')
```

## Output Contract

Artifact pyramid. Response is the absolute path to `00-index.md`.
