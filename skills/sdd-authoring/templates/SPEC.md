# Specification: <Project / Feature Name>

## Status

- **Author:** <name>
- **Version:** 0.1.0 (draft)
- **Status:** Draft / Under Review / Approved
- **Reviewed by:** <reviewer>
- **Gate verdict:** Pending / Approved / Conditions / Rejected
- **Frameworks:** <e.g., SDD Four-Phase, GSD, BMAD, Spec Kit>

## Problem Statement

<One to three sentences describing the problem this specification addresses. What gap exists in the current system? What user need is unmet? Why is this worth building?>

## Success Criteria

<Measurable outcomes that define success. These are NOT the acceptance criteria for individual features — they are the overall outcomes that justify the investment. Example: "Reduce account creation time from 90s to under 30s.">

## Scope

### In Scope

- <Capability or behavior included>
- <Capability or behavior included>

### Out of Scope (Explicit)

- <Capability explicitly excluded — prevents scope creep>
- <Capability explicitly excluded>

## User Stories

### US-001: <Story Title>

**Priority:** P0 / P1 / P2 / P3
**Description:** As a <role>, I want <capability> so that <benefit>.

**Acceptance Criteria:**

1. [AC-001.1] <Given/When/Then or pass/fail condition>
2. [AC-001.2] <Given/When/Then or pass/fail condition>

**Edge Cases:**

- <Edge case description — what happens when>
- <Edge case description>

### US-002: <Story Title>

...

## Non-Functional Requirements

| ID | Requirement | Threshold | Verification Method |
|----|-------------|-----------|-------------------|
| NFR-001 | Response time | < 200ms at P95 | Load test |
| NFR-002 | Availability | 99.9% uptime | Monitoring |
| NFR-003 | Security | <describe requirement> | <describe how verified> |

## Data Contracts & Interfaces

<Schemas, API signatures, event definitions. Stubs are acceptable at this phase — the spec should identify what contracts exist even if they are refined in later phases.>

### <Interface Name>

```
<Schema or signature>
```

## Assumptions & Open Questions

| # | Assumption / Question | Impact if Wrong | Resolution |
|---|----------------------|----------------|------------|
| 1 | <assumption> | <what breaks> | <how/when resolved> |
| 2 | <open question> | <what blocks> | <how/when resolved> |

## Revision History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 0.1.0 | <date> | <name> | Initial draft |
