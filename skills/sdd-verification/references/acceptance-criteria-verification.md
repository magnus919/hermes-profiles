# Acceptance Criteria Verification

Methodology for testing implementation output against specification acceptance criteria.

## The Verification Modes

### Mode 1: Automated Testing (CI Integration)

When the implementation includes tests that map to spec ACs, verification runs those tests and maps results to the AC matrix. Each test output is traced to a specific AC via test naming conventions or metadata.

**Input:** Test suite output (JSON, JUnit XML, TAP)
**Output:** AC pass/fail matrix with test evidence

### Mode 2: Manual Validation (No Test Infrastructure)

When no dedicated test infrastructure exists for the implementation, verification is performed by:
1. Reading the implementation output (code, configuration, or running system)
2. Tracing each AC against the observable behavior
3. Documenting the verdict with evidence from code inspection

**Input:** Implementation source, running system, or documentation
**Output:** AC pass/fail matrix with code references as evidence

### Mode 3: Interactive Probing (Running System)

When the implementation is a running service or application, verification probes the running system with inputs derived from the spec's ACs and edge cases, recording actual vs expected behavior.

**Input:** Running system URL or access
**Output:** AC pass/fail matrix with request/response evidence

## The AC Verification Checklist

For each AC, verify:

1. **Does the input produce the expected output?** (functional correctness)
2. **Does the system handle valid inputs without error?** (stability)
3. **Does the system correctly reject invalid inputs?** (negative testing — the spec defines rejection behavior)
4. **Does the behavior match the spec's data contracts?** (interface compliance)
5. **Is the behavior reproducible?** (determinism — same input, same output)

## Severity Classification

| Severity | Definition | Disposition |
|----------|-----------|-------------|
| BLOCKING | AC fails, no workaround — core requirement unmet | Gate blocked |
| CRITICAL | AC fails, workaround exists | Gate passes only with documented exception |
| MINOR | AC passes with suboptimal behavior | Informational, tracking |
| INFO | Observation, not a pass/fail issue | Reference for spec improvement |

## Verdict Recommendation

After classifying each AC by severity, the verification report SHOULD include a gate verdict recommendation using this mapping:

| Condition | Recommended Verdict |
|-----------|-------------------|
| 0 BLOCKING, 0 CRITICAL | APPROVED |
| 0 BLOCKING, ≤2 CRITICAL with remediation plans | CONDITIONS |
| Any BLOCKING | REJECTED |
| ≥3 CRITICAL without remediation plans | REJECTED |
| < 90% pass rate without exception | REJECTED |
