# Criteria Assessment

## The Verifier's Question

Not "is this good?" — that's a reviewer's question. The verifier asks: "does this meet the criteria?"

## Criteria Types

| Type | Example | Assessment |
|------|---------|------------|
| **Binary** | "All tests must pass" | Pass/Fail — no gray area |
| **Threshold** | "At least 80% test coverage" | Pass/Fail with a number |
| **Judgment** | "The argument must be coherent" | Requires explanation but still binary |
| **Edge case** | "Must handle null input" | Pass only if explicitly tested |

## Assessment Protocol

1. **Identify all criteria** from the original brief or quality gate
2. **Rate each criterion** independently — don't let one failure influence others
3. **Distinguish failure from uncertainty.** If you can't verify a criterion because information is missing, flag it as uncertain, not failed
4. **Report partial compliance.** If a criterion is partially met, state what's met and what's not

## Verdict Decision

- **PASS:** All criteria met. No exceptions.
- **HOLD:** Most criteria met but some require clarification or information is missing.
- **FAIL:** One or more criteria clearly not met, or evidence contradicts claims.
