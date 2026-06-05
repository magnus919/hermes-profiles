# Reviewer — Hermes Profile

Code and architecture reviewer — reviews PRs, runs quality gates, audits for regressions, and verifies against standards.

## Installation

```bash
git clone https://github.com/magnus919/hermes-profiles.git ~/hermes-profiles
ln -s ~/hermes-profiles/profiles/reviewer ~/.hermes/profiles/
hermes --profile reviewer
```

## Skill Dependencies

| Skill | Provides |
|---|---|
| `artifact-pyramids` | Progressive disclosure output format |

## Output Format

Artifact pyramid. Response is the absolute path to `00-index.md`.
