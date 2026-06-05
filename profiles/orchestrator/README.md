# Orchestrator — Hermes Profile

Decomposes complex questions into specialist workflows, routes work to the right profile in the right sequence, and synthesizes outputs.

## Installation

```bash
git clone https://github.com/magnus919/hermes-profiles.git ~/hermes-profiles
ln -s ~/hermes-profiles/profiles/orchestrator ~/.hermes/profiles/
hermes --profile orchestrator
```

## Skill Dependencies

| Skill | Provides |
|---|---|
| artifact-pyramids | Output format |
| orchestration-methodology | Task decomposition, specialist routing, synthesis patterns |

## Output Format

Artifact pyramid. Response is the absolute path to `00-index.md`.
