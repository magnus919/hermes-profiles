# Kanban Strategist — Hermes Profile

Flow optimization — board design, WIP calibration, bottleneck diagnosis, and multi-portfolio operating models. Hermes-specific.

## Installation

```bash
git clone https://github.com/magnus919/hermes-profiles.git ~/hermes-profiles
ln -s ~/hermes-profiles/profiles/kanban-strategist ~/.hermes/profiles/
hermes --profile kanban-strategist
```

## Skill Dependencies

| Skill | Provides |
|---|---|
| artifact-pyramids | Output format |
| kanban-guru | Flow diagnostics, WIP calibration, board design, operating models |

## Output Format

Artifact pyramid. Response is the absolute path to `00-index.md`.
