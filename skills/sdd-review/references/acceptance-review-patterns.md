# Acceptance Review Patterns

Reviewing verification results to determine whether the SDD pipeline delivers a passing verdict.

## What Acceptance Review Evaluates

### 1. Coverage Completeness
Is every AC from the spec present in the verification matrix? Missing ACs mean untested requirements. The review checks that the verification report covers 100% of ACs.

### 2. Verdict Accuracy
Are failure verdicts correctly classified? A BLOCKING failure misclassified as MINOR will be accepted when it should block the gate. The reviewer samples failures and validates the severity classification.

### 3. Remediation Plans
For each BLOCKING and CRITICAL failure, does a credible remediation plan exist? "Will fix later" is not a plan. "Will address by updating the spec to remove this AC and replacing with a narrower requirement" is a plan.

### 4. Overall Compliance
Does the overall compliance score meet the delivery bar? The standard bar is 90%+ pass rate across all ACs. A lower bar requires documented exception approval.

## Gate Decision Criteria

| Condition | Verdict |
|-----------|---------|
| 0 BLOCKING, 0 CRITICAL, 100% pass | APPROVED |
| 0 BLOCKING, ≤2 CRITICAL with remediation plans | CONDITIONS |
| Any BLOCKING failure | REJECTED |
| ≥3 CRITICAL failures without remediation plans | REJECTED |
| < 90% pass rate without exception | REJECTED |
