# Escalation Protocol

What to do when verification or review encounters a situation that cannot produce a clean pass/fail verdict.

## When to Escalate

Escalate when:
1. **Ambiguous AC** — The acceptance criterion is not testable. The spec says something that cannot be translated into a pass/fail check.
2. **Missing AC** — The implementation behaves correctly but no AC covers the behavior, or the implementation reveals a scenario the spec did not anticipate.
3. **Conflicting ACs** — Two acceptance criteria from different spec sections produce contradictory requirements when implemented together.
4. **Spec gap** — The implementation requires a decision the spec does not make (technology choice, default behavior, error handling strategy).
5. **Blocking failure without obvious fix** — A BLOCKING failure exists and the remediation path is unclear.

## Escalation Format

Each escalation is a structured report:

```markdown
## Escalation: <Summary>

**From:** <verification / review / implementation agent>
**Phase:** <Gate 1-4>
**Finding type:** ambiguous AC / missing AC / conflicting AC / spec gap / blocking failure
**Spec ref:** SPEC.md — Section <X>, AC-<ID>
**Status:** unresolved / resolved

### What the spec says:
<Exact text from the specification>

### What was observed:
<What the implementation does, or what the ambiguity is>

### Why a verdict cannot be produced:
<Clear explanation of why this cannot be evaluated as pass/fail>

### Suggested resolution:
<Recommendation — should the spec be amended? the implementation changed? a decision made?>

### Impact if unresolved:
<What happens to the gate if this is not resolved>
```

## Resolution Paths

| Finding Type | Default Resolution | Who Resolves |
|-------------|-------------------|--------------|
| Ambiguous AC | Spec author clarifies, spec is amended | sdd-authoring |
| Missing AC | Spec is amended to include the missing AC | sdd-authoring |
| Conflicting ACs | Spec author resolves the conflict, spec is amended | sdd-authoring + human |
| Spec gap | Decision is made, spec is updated | Human decision-maker |
| Blocking failure | Implementation is fixed or spec is adjusted | sdd-work-decomposition + implementation |

## The Golden Rule

**When in doubt, escalate.** The cost of a 10-minute clarification conversation at escalation time is lower than the cost of implementing against an incorrect assumption. The implementation agent defaults to forging ahead — this protocol exists to override that default.
