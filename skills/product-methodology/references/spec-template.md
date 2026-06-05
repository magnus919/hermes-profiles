# Spec Template

A requirements document that engineers, designers, and stakeholders can all work from. The goal is not to specify every pixel and code path — it's to align on what we're building, what we're not building, and what we haven't figured out yet.

---

# Feature Title

**Status:** Draft / In Review / Approved
**Owner:**
**Last updated:**

## Problem Statement

What problem are we solving, and for whom? One paragraph. If you can't describe the problem without mentioning your proposed solution, you haven't thought about it enough.

**Don't write:** "We need a bulk edit feature so users can edit multiple items at once."
**Write:** "Power users managing 50+ projects spend 4+ hours per week updating individual project settings. Each setting change requires 4 clicks and a page load. This creates a ceiling on how many projects a single user can manage."

## Success Metrics

How will we know this worked? One quantitative metric and one qualitative signal.

- **Primary metric:** [e.g., Time spent per project settings update]
- **Target:** [e.g., Reduce from 4 hours to 30 minutes per week]
- **Qualitative signal:** [e.g., Users stop asking for bulk edit in support tickets]
- **Countermetric to watch:** [e.g., Don't increase accidental edits — measure undo/redo rate]

## Scope

### What we're building

3-6 bullet points describing what this feature actually does. Engineer-readable. No implementation details.

- Users can select multiple projects from a list view
- Users can apply a setting change to all selected projects at once
- Users can preview changes before applying
- Users can undo the last bulk operation
- Changes are logged per-project for audit trail

### What we're NOT building

Explicitly. This protects the team from scope creep.

- No scheduled/recurring bulk operations (future)
- No bulk operations across different item types (projects + tasks together)
- No template-based bulk operations
- No role-based permissions on bulk operations (all project editors can bulk-edit)

## Open Questions

Every spec should have open questions. If you have zero open questions, you either understand the problem perfectly or (more likely) you didn't think about the hard parts.

- [ ] What's the maximum number of items that can be selected before performance degrades?
- [ ] Should bulk operations generate separate audit entries per item, or one aggregated entry?
- [ ] Are there any permission scenarios where a user can see items they can't bulk-edit?
- [ ] How does this interact with the existing "project lock" feature?

## Deferred Decisions

Things we've explicitly decided not to decide yet, with the reasoning.

| Decision | Why deferred | When to revisit |
|----------|-------------|-----------------|
| Undo window duration | UX research needed | After first user tests |
| Mobile layout | Mobile usage is <5% of power user traffic | When mobile traffic exceeds 15% |

## Design Constraints

Hard constraints that any solution must work within. These come from the team, not from the PM.

- **Engineering:** Edit operation must complete within 5 seconds for 100 items
- **Design:** Must work on both full-width and half-width viewport configurations
- **Data/Infra:** Audit trail must maintain existing immutability guarantees
- **Accessibility:** Must meet WCAG 2.1 AA for keyboard navigation

## Edge Cases

Known edge cases the solution should handle. Addressed or deferred.

| Edge case | Status |
|-----------|--------|
| User selects items they don't have edit permission on | Skip in preview, notify user |
| Bulk operation partially fails | Roll back all, notify user |
| User navigates away during pending operation | Cancel operation, warn user |
| Items are deleted by another user mid-selection | Refresh selection, exclude deleted items |

## Technical Notes

Engineer-facing implementation guidance. The PM doesn't dictate architecture, but can surface context the team needs.

- The existing project settings API supports single-item PATCH — bulk PATCH endpoint needed
- Audit event schema already includes `action:bulk_update` — no schema migration needed
- Undo will need a new `bulk_operation_id` correlation field on audit events

## Dependencies

- Bulk PATCH endpoint (API team, sprint +1)
- Design review for preview modal
- Copy review for confirmation messages
- Accessibility audit for keyboard navigation flow

## Timeline & Milestones

| Milestone | Target | Exit criteria |
|-----------|--------|---------------|
| API endpoint ready | Sprint+2 | Bulk PATCH passes integration tests |
| Frontend prototype | Sprint+3 | Selection + preview flow works in staging |
| User test | Sprint+4 | 3/5 power users complete task without guidance |
| Release | Sprint+5 | GA with metrics tracking enabled |

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Parallel edits conflict | Medium | High | Pessimistic locking on project settings |
| Performance at 1000+ items | Low | Medium | Cap selection at 200 items for v1 |
| Users accidentally apply wrong settings | Medium | High | Preview step + undo within 30 seconds |
