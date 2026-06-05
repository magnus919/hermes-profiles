# Task Plan: <Project / Feature Name>

## Source Specification

- **Spec:** `SPEC.md` (version <x.y.z>)
- **Spec review gate:** <approved / conditions>
- **Plan author:** <name>
- **Plan version:** 0.1.0

## Phase Overview

| Metric | Value |
|--------|-------|
| Total tasks | <N> |
| Task groups | <N> |
| Critical path | <N> tasks |
| Estimated total effort | <estimate> |
| Dependencies | <N> real dependencies |

## Execution Order

<Recommended execution order for the phase groups. Start with foundational tasks (contracts, schemas, interfaces), then core logic, then integration, then edge cases and error handling.>

## Task Groups

### Group 1: <Name>

**Spec reference:** `SPEC.md` — Section <X>
**Preconditions:** <none or reference to prerequisite groups>
**Dependencies:** <none or list of prerequisite tasks>

| ID | Task | Spec Ref | Est. Size | Preconditions |
|----|------|----------|-----------|---------------|
| T-001 | <task name> | AC-001.x | S/M/L | <none or T-XXX> |
| T-002 | <task name> | AC-001.x | S/M/L | T-001 |

### Group 2: <Name>

...

## Critical Path

<Diagram or list showing the chain of dependent tasks that determine the overall timeline. Tasks on the critical path have zero float — delay in any one of them delays the entire plan.>

## Task Cards

Each task card is an independent work unit. Copy this structure for each task.

---

### T-001: <Task Name>

- **Type:** feature / refactor / test / docs / config
- **Spec reference:** `SPEC.md` — US-001, AC-001.1, AC-001.2
- **Dependencies:** <none or T-XXX>
- **Estimated size:** Small (<1h) / Medium (1-2h) / Large (2-4h)
- **Preconditions:** <what must exist before this task starts>

**Description:**

<What this task implements, derived from the spec.>

**Acceptance Criteria:**

- [ ] AC-001.1: <condition — directly from SPEC.md>
- [ ] AC-001.2: <condition — directly from SPEC.md>

**Implementation Agent Directives:**

<This section becomes the CLAUDE.md context for the implementation agent running this task.>
- Load SEPC.md section <X> for behavioral requirements
- Load the interface contract from SPEC.md section <Y>
- Implement in this commit: <commit scope>
- Do NOT implement: <explicit out-of-scope for this task>

---

## Revision History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 0.1.0 | <date> | <name> | Initial plan from SPEC.md v0.x |
