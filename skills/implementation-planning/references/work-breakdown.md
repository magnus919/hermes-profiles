# Work Breakdown

## Principles

- **Decompose until each task is estimable.** If a task feels like "2-3 weeks," split it. Small tasks produce accurate estimates.
- **Component decomposition.** Break by architectural component, then by functional unit within each component.
- **Integration tasks are first-class.** Don't hide integration work inside component tasks.

## Task Template

Each task in the breakdown should have:
- **Name** — a specific, actionable description
- **Component** — which architectural component it touches
- **Depends on** — tasks that must complete before this one starts
- **Estimate** — in days or story points
- **Output** — what deliverable or artifact proves the task is complete
- **Verification** — how to verify the output is correct

## Example

| Task | Component | Depends on | Est. | Output |
|------|-----------|-----------|------|--------|
| Set up payment service scaffold | payments | repo structure | 1d | Service responds on health endpoint |
| Implement payment auth middleware | payments | service scaffold | 2d | Auth middleware validates tokens |
| Design user notification schema | notifications | - | 1d | Schema document with validation rules |
