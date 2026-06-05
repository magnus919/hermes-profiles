---
name: sdd-verification
description: "SDD acceptance criteria verification — maps specification acceptance criteria to tests, validates implementation output against spec requirements, and produces artifact-pyramid-compliant VERIFICATION.md reports. Trigger when implementation needs to be verified against its specification."
version: 1.0.0
author: Hermes Agent community
license: MIT
metadata:
  hermes:
    tags: [sdd, verification, acceptance-criteria, testing, compliance, quality]
    related_skills: [sdd-authoring, sdd-work-decomposition, sdd-review]
---

# SDD Verification

Validating that implementation output satisfies every acceptance criterion defined in the specification. This skill owns the **Verify** phase of the SDD pipeline — the final gate before delivery.

## SDD Pipeline Position

```
SPECIFY → PLAN → TASKS → IMPLEMENT → [VERIFY]
                                           ↑
                                     You are here
```

Verification is the phase that closes the loop. If specification is the question ("what should the system do?") and implementation is the answer ("this is what the system does"), verification is the judgment ("does the answer satisfy the question?").

## Core Principle: Every AC Produces a Binary Verdict

An acceptance criterion that cannot produce a CLEAR PASS or CLEAR FAIL is not a well-defined AC. Verification exposes spec defects: if a criterion is ambiguous and cannot be tested, it is a spec bug, not an implementation failure. Verification findings thus flow in two directions — implementation failures (code doesn't meet the spec) and spec failures (the spec is untestable or ambiguous).

## Artifact-Pyramid Output: VERIFICATION.md

Verification reports follow the artifact-pyramid structure:

| Layer | Content | File |
|-------|---------|------|
| L1 | Pass/fail summary — total ACs tested, pass count, fail count, compliance score, blocking verdict | `00-index.md` (entry point) |
| L2 | Verification matrix — per-story or per-feature-area AC status grouped for navigation | Individual `*.verification.md` files |
| L3 | Individual failure dossiers — what failed, expected behavior (from spec), actual behavior (from implementation), evidence, severity | `dossiers/` directory |
| SOURCES | Cross-reference from each AC back to its SPEC.md section | Footer of each file |

## Loading Guidance

| Reference | When to load | File |
|-----------|-------------|------|
| Acceptance Criteria Verification | Before running verification — methodology for testing ACs that may not have dedicated test infrastructure | `references/acceptance-criteria-verification.md` |
| Spec-to-Test Mapping | When existing tests exist — how to map test coverage back to spec ACs and identify gaps | `references/spec-to-test-mapping.md` |
| Escalation Protocol | When an AC is ambiguous or an implementation finding needs escalation — what to do when verification can't produce a clean verdict | `references/escalation-protocol.md` |

| Template | When to use | File |
|----------|-------------|------|
| VERIFICATION.md | Producing a verification report after implementation | `templates/VERIFICATION.md` |

| Script | When to run | File |
|--------|-------------|------|
| `verification-report.sh` | After verification — generates the AC pass/fail matrix from structured input | `scripts/verification-report.sh` |

## Trigger Conditions

Invoke this skill when:
- An implementation agent has completed its task and claims acceptance criteria are met
- A PR or MR needs spec-compliance verification before merge
- A spec amendment needs to be verified against existing test coverage
- An integration test suite needs mapping back to the specification's acceptance criteria

## Verification Dimensions

### Functional Correctness
Does the implementation produce the correct output for each specified input? Test against all normal cases, edge cases, and error conditions from the spec.

### Behavioral Completeness
Does the implementation handle every scenario the spec describes? An implementation that handles all normal cases but crashes on a documented edge case is functionally correct for some inputs but behaviorally incomplete.

### Contract Compliance
Does the implementation honor the data contracts, interface signatures, and protocol definitions from the spec? A function that returns the right value with the wrong type or shape is not compliant.

### Non-Functional Requirements
Does the implementation meet the performance, security, observability, and compliance requirements from the spec? An NFR failure may not produce wrong output but may produce unacceptable behavior in production.

### Negative Testing
Does the implementation correctly reject invalid inputs per the spec? A system that accepts what it should reject is a security and correctness risk, even if it handles valid inputs perfectly.

## Severity Classification

| Severity | Definition | Disposition |
|----------|-----------|-------------|
| BLOCKING | An AC is failed and no workaround exists — the system does not meet a core requirement | Gate does not pass |
| CRITICAL | An AC is failed but a feasible workaround exists | Gate does not pass without documented exception |
| MINOR | An AC passes but with suboptimal behavior, or a non-functional requirement is partially met | Gate can pass with remediation plan |
| INFO | An observation that does not affect pass/fail status — spec improvement suggestion, test gap | Informational |

## Gate Verdict Calculation

After classifying each AC by severity, produce a single gate verdict that determines whether the implementation passes to the next SDD phase. The verdict is computed deterministically from severity counts:

| Condition | Verdict |
|-----------|---------|
| 0 BLOCKING, 0 CRITICAL, all ACs tested | APPROVED — the implementation satisfies the specification |
| 0 BLOCKING, ≤2 CRITICAL with remediation plans documented | CONDITIONS — implementation passes but requires tracked remediation of CRITICAL failures |
| Any BLOCKING failure | REJECTED — core requirement unmet; remediation must be completed and re-verified |
| ≥3 CRITICAL failures without documented remediation plans | REJECTED — unacceptable failure density without resolution path |
| < 90% compliance score without documented exception | REJECTED — overall quality below threshold |

The Gate Verdict MUST be included in the L1 summary of every VERIFICATION.md. This makes the verification output directly consumable by the downstream sdd-review phase gate.

### Remediation Recommendation Format

Each BLOCKING, CRITICAL, and MINOR finding in the L3 dossiers SHOULD include a remediation recommendation following this structure:

- **What to fix:** The specific code, config, or behavior that needs to change
- **Why this severity:** The impact that justifies the severity classification
- **Verification for the fix:** How to confirm the fix satisfies the AC (specific test or check)

Remediation recommendations are guidance for the implementation agent — they are NOT spec amendments. If the remediation suggests a spec change (ambiguous AC, missing AC), escalate per the Escalation Protocol instead.
