# Phase-Gate Review Methodology

How the four SDD phase gates work and what each gate evaluates.

## The Gate Principle

Every gate answers one question: **"Is the artifact for this phase complete, correct, and unambiguous enough for the next phase to proceed safely?"**

A gate is not a code review. It is not a design review. It is a **readiness check** — ensuring that the artifact produced by the current phase is fit for consumption by the next phase. The reviewer is not evaluating quality in the abstract; they are evaluating whether passing this artifact downstream will waste the next phase's effort.

## Gate Structure

Each gate follows this protocol:

1. **Receive** — The artifact (SPEC.md, TASK-PLAN.md, implementation, VERIFICATION.md) is presented for review
2. **Assess** — The reviewer evaluates the artifact against the gate's specific criteria
3. **Decide** — The reviewer produces a gate verdict (APPROVED / CONDITIONS / REJECTED)
4. **Report** — The reviewer produces a REVIEW.md with findings and the gate verdict
5. **Escalate** — If the verdict is REJECTED or CONDITIONS cannot be resolved, escalate

## The Four Gates

### Gate 1: Spec Review

| Criterion | What we're checking | Fail signal |
|-----------|-------------------|-------------|
| Testability | Every AC produces CLEAR PASS or CLEAR FAIL | "handle gracefully", "be efficient" |
| Completeness | All edge cases, NFRs, out-of-scope documented | Undocumented boundary conditions |
| Precision | No ambiguous phrases that an agent would guess at | "common formats", "standard behavior" |
| Contract sufficiency | Interfaces specified at independent-implementation granularity | Two agents would need to coordinate |

### Gate 2: Plan Review

| Criterion | What we're checking | Fail signal |
|-----------|-------------------|-------------|
| Spec traceability | Every requirement maps to a task | Orphan requirement, unmapped task |
| Dependency honesty | Dependencies are real, not invented | "depends on" where a stub suffices |
| Atomicity | Each task is independently verifiable | "Can't test this until T-005 also done" |
| Size | Each task fits in one implementation session | Task estimated at "large" with no decomposition note |

### Gate 3: Implementation Review

| Criterion | What we're checking | Fail signal |
|-----------|-------------------|-------------|
| AC satisfaction | Implementation satisfies the task's ACs | Missing behavior, wrong output |
| Spec fidelity | Implementation matches spec, not just the task | Feature works but violates spec constraint |
| Contract compliance | Data contracts and interfaces match spec | Wrong type, missing field, unexpected error |
| No scope creep | Implementation does not include unrequested features | Spec doesn't mention it and it's in the code |

### Gate 4: Acceptance Review

| Criterion | What we're checking | Fail signal |
|-----------|-------------------|-------------|
| Coverage | Every spec AC is in the verification matrix | Missing ACs |
| Verdict accuracy | Failure verdicts are correctly classified | BLOCKING misclassified as MINOR |
| Remediation quality | BLOCKING/CRITICAL failures have remediation plans | "Will fix later" with no plan |
| Compliance threshold | Overall compliance meets the delivery bar | < 90% pass rate with no exception |

## Review Mindset

- **Assume nothing.** Every claim in the artifact is suspect until verified against the spec.
- **Test the artifact against the worst case.** What happens when the downstream agent encounters an ambiguity? If the answer is "the agent will guess," the artifact fails the gate.
- **Protect the pipeline.** Your job as reviewer is not to be collegial — it is to prevent downstream waste. A REJECTED gate saves more time than it costs.
