# Implementation Review Patterns

Reviewing implementation output against the specification. This is NOT a general code review — it only evaluates spec compliance.

## What Implementation Review Is Not

This review does not assess:
- Code style, formatting, or naming conventions
- Test coverage (that's verification's job)
- Architectural elegance or design patterns
- Performance optimization (unless covered by NFRs)
- Library choices (unless constrained by the spec)

## What Implementation Review Assesses

### 1. AC Satisfaction
Does the implementation satisfy every acceptance criterion for the completed tasks? Test each AC against the actual behavior.

### 2. Spec Fidelity
Does the implementation match what the spec says, even for details not covered by explicit ACs? The spec may state "all endpoints return JSON" — if an endpoint returns HTML, it violates the spec even if no specific AC tests for it.

### 3. Contract Compliance
Do the implementation's interfaces match the spec's data contracts? Check function signatures, API responses, event payloads, error formats.

### 4. Scope Containment
Does the implementation include only what the spec requires? Unexpected features are not a bonus — they are scope creep that must be reviewed, tested, and maintained.

## Review Methodology

For each completed task:

1. Read the task's acceptance criteria from TASK-PLAN.md
2. Read the corresponding spec section from SPEC.md
3. Examine the implementation output (diff, running system, or source)
4. Assess: does the output satisfy the ACs?
5. Assess: does the output violate any spec constraint not covered by an AC?
6. Produce a finding for each deviation

## Finding Format

```
### Finding: <Summary>

**Severity:** <BLOCKING / CRITICAL / MINOR / INFO>
**Task:** T-00X
**Spec ref:** SPEC.md — Section X, AC-00X
**Description:** <What the implementation does vs what the spec requires>
**Recommendation:** <What should change>
```
