# Copy Editor — Hermes Profile

Line-level editing — grammar, punctuation, consistency, style guide enforcement, and proofreading.

## Installation

```bash
git clone https://github.com/magnus919/hermes-profiles.git ~/hermes-profiles
ln -s ~/hermes-profiles/profiles/copy-editor ~/.hermes/profiles/
hermes --profile copy-editor
```

## Skill Dependencies

| Skill | Provides |
|---|---|
| artifact-pyramids | Output format |
| copy-editor-methodology | Style guide, copy-editing checklist, proofreading protocol |

## Output Format

Artifact pyramid. Response is the absolute path to `00-index.md`.
