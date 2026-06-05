# Verifier — Hermes Profile

Pass/fail gatekeeper assessing work against completion criteria and evidence standards.

## Installation

```bash
git clone https://github.com/magnus919/hermes-profiles.git ~/hermes-profiles
ln -s ~/hermes-profiles/profiles/verifier ~/.hermes/profiles/
hermes --profile verifier
```

## Skill Dependencies

| Skill | Provides |
|---|---|
| artifact-pyramids | Output format |
| verification-methodology | Criteria assessment, evidence standards, verdict templates |

## Output Format

Artifact pyramid. Response is the absolute path to `00-index.md`.
