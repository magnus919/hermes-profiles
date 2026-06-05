# Curator — Hermes Profile

Knowledge curator — manages notes, creates and cross-links atomic content, ingests sources, and maintains knowledge graph connectivity.

## Installation

```bash
git clone https://github.com/magnus919/hermes-profiles.git ~/hermes-profiles
ln -s ~/hermes-profiles/profiles/curator ~/.hermes/profiles/
hermes --profile curator
```

## Skill Dependencies

| Skill | Provides |
|---|---|
| `artifact-pyramids` | Progressive disclosure output format |

## Output Format

Artifact pyramid. Response is the absolute path to `00-index.md`.
