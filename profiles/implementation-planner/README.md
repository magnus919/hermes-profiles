# Implementation Planner — Hermes Profile

Breaks architecture into implementable units, sequences build phases, identifies dependency chains and critical paths, and produces milestone plans with risk buffers and rollback strategies.

## What This Profile Provides

- **Work breakdown** — decompose architecture into estimable, sequenced tasks
- **Dependency analysis** — surface hidden dependencies, distinguish structural from discretionary
- **Critical path identification** — find the sequence that determines the timeline
- **Risk assessment** — score each risk with probability, impact, mitigation, contingency
- **Rollback planning** — every deployment plan includes a rollback strategy

## Installation

```bash
git clone https://github.com/magnus919/hermes-profiles.git ~/hermes-profiles
ln -s ~/hermes-profiles/profiles/implementation-planner ~/.hermes/profiles/
hermes --profile implementation-planner
```

## Quick Start

> "Plan the implementation of a payment processing system. The architecture is in /tmp/architect-workflow/payment-system/00-index.md."

The profile will:
1. Decompose the architecture into implementable work units
2. Identify dependency chains and the critical path
3. Assign risk scores and mitigations
4. Sequence build phases with project-level buffer
5. Output an artifact pyramid at `/tmp/planner-workflow/<project>/00-index.md`

## Skill Dependencies

| Skill | Provides |
|---|---|
| `artifact-pyramids` | Progressive disclosure output format |

## Related Profiles

- **technical-architect** — produces the architecture pyramid this profile consumes
- **data-architect** — data pipeline dependencies feed into the work breakdown

## Output Format

Artifact pyramid. Response is the absolute path to `00-index.md`.
