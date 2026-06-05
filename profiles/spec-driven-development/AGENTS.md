# AGENTS.md — Spec-Driven Development Specialist

## How to Use This Profile

This profile is designed for two modes:

### Mode 1: Dedicated Agent
Run with `hermes --profile spec-driven-development` to have a persistent agent that manages the full SDD pipeline — from specification through implementation and verification.

### Mode 2: Specialist Delegate (Recommended)
Delegate specific SDD phases to this profile from an orchestrator:

```
delegate_task(
  goal="Write a specification for [feature] and produce SPEC.md",
  role="orchestrator",
  context="..."  # background, requirements, user needs
)
```

The profile handles the full pipeline internally — spec → plan → delegate implementation → verify → review — and returns the path to the final artifact pyramid.

## Delegation Patterns

### Full Pipeline (spec through verification)
```
delegate_task(
  goal="Implement [feature] from specification through verification",
  profile="spec-driven-development",
  context="..."
)
```

The profile will: write SPEC.md → decompose into TASK-PLAN.md → generate CLAUDE.md → delegate implementation → verify against ACs → produce REVIEW.md.

### Partial Pipeline (start from existing spec)
If a SPEC.md already exists, pass the path in the context:
```
delegate_task(
  goal="Implement from existing spec and verify",
  profile="spec-driven-development",
  context="SPEC.md at path/to/SPEC.md"
)
```

### Review Gate Only
To run a phase gate on existing artifacts:
```
delegate_task(
  goal="Review [artifact] for Gate [N]",
  profile="spec-driven-development",
  context="Artifact at path/to/artifact.md"
)
```

## Output

The profile delivers a single filesystem path to the artifact pyramid's `00-index.md`. That file contains:
- **L1:** Executive summary, phase status, key findings
- **L2:** Per-dimension analysis (spec, plan, verification dimensions)
- **L3:** Detailed dossiers (full AC matrices, failure evidence)

Navigate down as needed. No summary is returned in the delegation response.
