# Spec-Driven Development Specialist

A Hermes Agent profile for AI-native, specification-driven software development.

This profile is a specialist agent that owns the entire SDD lifecycle: writing formal specifications, decomposing them into executable task plans, generating CLAUDE.md directives for implementation agents, verifying output against acceptance criteria, and enforcing phase gates at every stage.

## Pipeline

```
INCEPTION → SPECIFY → REVIEW → PLAN → REVIEW → TASKS → REVIEW → IMPLEMENT → REVIEW → VERIFY
              ↑         ↑       ↑       ↑       ↑        ↑         ↑          ↑
          Gate 1    Gate 2   Gate 3          Gate 4
         (Spec)    (Plan)    (Implementation) (Acceptance)
```

## Skills

This profile ships with:

| Skill | Purpose |
|-------|---------|
| `sdd-authoring` | Writing formal specifications (SPEC.md) — Gherkin, acceptance criteria, quality gates |
| `sdd-work-decomposition` | Translating specs into dependency-aware task plans (TASK-PLAN.md) with CLAUDE.md generation |
| `sdd-verification` | Validating implementation against spec ACs — producing pass/fail matrices (VERIFICATION.md) |
| `sdd-review` | Enforcing phase gates — reviewing artifacts before downstream phases proceed (REVIEW.md) |
| `artifact-pyramids` | Progressive disclosure output format — L1 summary → L2 analysis → L3 dossiers |

## Usage

### As a dedicated agent:
```
hermes --profile spec-driven-development
```

### As a specialist delegate:
Delegate specific SDD phases from an orchestrator workflow. See `AGENTS.md` for delegation patterns.

## Philosophy

This profile is opinionated. It does not implement from vague prompts. It enforces phase gates. Every acceptance criterion produces a binary verdict. The spec is the single source of truth — no downstream artifact is valid unless it traces back to a spec requirement.

See `SOUL.md` for full first principles.
