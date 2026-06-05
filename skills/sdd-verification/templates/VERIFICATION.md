# Verification Report: <Project / Feature Name>

## Source Specification

- **Spec:** `SPEC.md` (version <x.y.z>)
- **Spec review gate:** <approved / conditions>
- **Plan reference:** `TASK-PLAN.md` (version <x.y.z>)
- **Verification author:** <name>
- **Verification date:** <date>
- **Verification mode:** automated / manual / interactive

## L1: Summary

| Metric | Value |
|--------|-------|
| Total ACs tested | <N> |
| Pass | <N> |
| Fail | <N> |
| Blocking | <N> |
| Critical | <N> |
| Minor | <N> |
| Compliance score | <XX.X%> |
| **Gate Verdict** | **APPROVED / CONDITIONS / REJECTED** |

### Gate Verdict Rationale

<One paragraph explaining why the gate verdict was reached, referencing the severity classification rules: 0 BLOCKING + 0 CRITICAL = APPROVED; 0 BLOCKING + ≤2 CRITICAL with remediation plans = CONDITIONS; any BLOCKING = REJECTED; <90% pass rate without exception = REJECTED.>

## L2: Verification Matrix

### Per-Story Results

| Story / Feature | ACs | Pass | Fail | Blocking | Verdict |
|-----------------|-----|------|------|----------|---------|
| <US-001> | <N> | <N> | <N> | <N> | PASS / FAIL |
| <US-002> | <N> | <N> | <N> | <N> | PASS / FAIL |

### Verification Dimensions Coverage

| Dimension | Score | Notes |
|-----------|-------|-------|
| Functional Correctness | <N/N> | |
| Behavioral Completeness | <N/N> | |
| Contract Compliance | <N/N> | |
| Non-Functional Requirements | <N/N> | |
| Negative Testing | <N/N> | |

## L3: Failure Dossiers

### <AC-ID>: <Description>

- **Severity:** BLOCKING / CRITICAL / MINOR / INFO
- **Story:** <US-00X>
- **Verification dimension:** <Functional / Behavioral / Contract / NFR / Negative>

**Expected behavior (from spec):**
<What the acceptance criterion says should happen>

**Actual behavior (from implementation):**
<What actually happens>

**Evidence:**
<Test output, code inspection, observation>

**Remediation recommendation:**
<What to fix, why this severity, and how to verify the fix passes the AC>

---

### <AC-ID>: <Description>
...

## SOURCES

| Reference | Description |
|-----------|-------------|
| `SPEC.md` | Source specification document |
| <AC-specific ref> | Section X — user story for this AC |

## Revision History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | <date> | <name> | Initial verification |
