# Technical Writer — Hermes Profile

Technical writer — API documentation, README authorship, CLI help text, agent-facing docs (AGENTS.md), developer guides, and reference documentation.

## Installation

```bash
git clone https://github.com/magnus919/hermes-profiles.git ~/hermes-profiles
ln -s ~/hermes-profiles/profiles/technical-writer ~/.hermes/profiles/
hermes --profile technical-writer
```

## Skill Dependencies

| Skill | Provides |
|---|---|
| `artifact-pyramids` | Progressive disclosure output format |
| `technical-documentation` | README patterns, API docs, agent-facing docs, CLI help methodology |

## Output Format

Artifact pyramid. Response is the absolute path to `00-index.md`.
