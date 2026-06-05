---
name: sdd-review
description: "SDD phase-gate review — enforces the SDD pipeline's gated structure by reviewing specification artifacts before the next phase can proceed. Produces artifact-pyramid-compliant gate decision reports. No phase passes without reviewed, approved artifacts."
version: 1.0.0
author: Hermes Agent community
license: MIT
metadata:
  hermes:
    tags: [sdd, review, phase-gate, quality, governance, approval]
    related_skills: [sdd-authoring, sdd-work-decomposition, sdd-verification]
---

# SDD Phase-Gate Review

Enforcing the SDD pipeline's gated structure: every artifact is reviewed before the next phase proceeds. This skill owns the **Review** gates between every pair of SDD phases.

## SDD Pipeline Position

```
[SPECIFY] → REVIEW → [PLAN] → REVIEW → [TASKS] → REVIEW → [IMPLEMENT] → REVIEW → [VERIFY]
     ↑         ↑        ↑        ↑         ↑         ↑           ↑          ↑
     └─────────┘        └────────┘         └─────────┘           └──────────┘
   Gate 1: Spec      Gate 2: Plan      Gate 3: Tasks          Gate 4: Implementation
```

Every gate asks the same question: **"Is the artifact for this phase complete, correct, and unambiguous enough for the next phase to proceed safely?"**

## Core Principle: The Gate Is the Quality Mechanism

In SDD, quality is not enforced by code review — that's too late. Quality is enforced by the phase gate. A defect caught at Gate 1 (spec review) costs minutes to fix. The same defect caught at Gate 4 (implementation review) costs hours — the implementation may need to be discarded and rewritten against a corrected spec.

This skill is deliberately strict. Its job is not to be agreeable; its job is to protect downstream phases from upstream artifacts that would waste their time.

## Artifact-Pyramid Output: REVIEW.md

Phase-gate review reports follow the artifact-pyramid structure:

| Layer | Content | File |
|-------|---------|------|
| L1 | Gate decision — APPROVED / CONDITIONS / REJECTED, one-line rationale, blocking findings count | `00-index.md` (entry point) |
| L2 | Review findings by category — spec completeness, task correctness, implementation compliance, verification gaps | Individual `*.findings.md` files |
| L3 | Per-finding dossiers — severity, location (artifact + section), recommendation, evidence, escalation path | `dossiers/` directory |
| SOURCES | Cross-reference from each finding to the artifact section it evaluates | Footer of each file |

## Loading Guidance

| Reference | When to load | File |
|-----------|-------------|------|
| Phase Gate Methodology | Before running any review — the four-gate structure, decision criteria, escalation paths | `references/phase-gate-methodology.md` |
| Spec Review Patterns | Reviewing a SPEC.md — completeness checks, ambiguity detection, testability assessment | `references/spec-review-patterns.md` |
| Implementation Review Patterns | Reviewing code against a spec — not general code review, but spec-compliance review | `references/implementation-review-patterns.md` |
| Acceptance Review Patterns | Reviewing verification results — assessing whether the verification report justifies a pass verdict | `references/acceptance-review-patterns.md` |

| Template | When to use | File |
|----------|-------------|------|
| REVIEW.md | Producing a phase-gate review report | `templates/REVIEW.md` |

## Trigger Conditions

Invoke this skill when:
- A SPEC.md has been authored and needs review before work decomposition begins (Gate 1)
- A TASK-PLAN.md has been produced and needs review before implementation starts (Gate 2)
- Implementation output needs spec-compliance review (Gate 3)
- A VERIFICATION.md report needs review before the pipeline delivers (Gate 4)
- An escalation has been raised about an earlier gate decision and needs re-review

## The Four Gates

### Gate 1: Spec Review
Reviews SPEC.md against the quality gates defined in `sdd-authoring`. Questions asked:
- Is every acceptance criterion testable?
- Are edge cases enumerated, not just implied?
- Are non-functional requirements specified with measurable thresholds?
- Is the scope boundary clear (explicit in-scope and out-of-scope)?
- Are data contracts and interface definitions sufficiently precise?
- Does any section leave room for the implementation agent to make an unguided assumption?

**Verdict:** APPROVED only if every question produces a clear "yes" or has an explicit remediation plan.

### Gate 2: Plan Review
Reviews TASK-PLAN.md against the specification. Questions asked:
- Does every specification requirement map to at least one task?
- Are dependencies real and spec-derived, not invented?
- Is each task independently verifiable?
- Are task sizes appropriate for a single implementation session?
- Does the CLAUDE.md / AGENTS.md handoff accurately represent the spec and plan?

**Verdict:** APPROVED only if spec traceability is complete and dependency mapping is honest.

### Gate 3: Implementation Review
Reviews implementation output against the task plan. This is NOT a general code review — it does not assess code style, test coverage, or architectural elegance. It asks only:
- Does the implementation satisfy the acceptance criteria for each completed task?
- Are there any deviations from the spec that were not documented?
- Does the implementation produce correct results for all specified inputs?
- Are error states handled per the spec?

**Verdict:** APPROVED only if all completed task ACs are satisfied.

### Gate 4: Acceptance Review
Reviews the VERIFICATION.md report. Questions asked:
- Are all spec ACs accounted for in the verification matrix (none missing)?
- Are FAIL verdicts correctly classified by severity?
- Are BLOCKING and CRITICAL failures accompanied by remediation plans?
- Is the overall compliance score sufficient for delivery?

**Verdict:** APPROVED only if no BLOCKING failures exist and all CRITICAL failures have documented exceptions or remediation plans.

## Gate Decision Format

Every gate produces one of three verdicts:

| Verdict | Meaning | What happens next |
|---------|---------|-------------------|
| APPROVED | Artifact passes all criteria. The next phase may proceed. | Deliver artifact to next phase |
| CONDITIONS | Artifact passes subject to specific remediations that do not require a full re-review | Deliver artifact + conditions list; next phase may proceed while conditions are resolved |
| REJECTED | Artifact fails one or more criteria. The current phase must produce a revised artifact. | Return artifact to current phase; no downstream work starts |

## Escalation

When a reviewer and artifact author disagree on a finding, the escalation path is:
1. Document the disagreement clearly — what the artifact says, what the reviewer found, why the author disagrees
2. Escalate to the orchestrator or human if the finding is BLOCKING or CRITICAL
3. MINOR and INFO disagreements are resolved by the reviewer's determination — the gate is not delayed for editorial preferences
