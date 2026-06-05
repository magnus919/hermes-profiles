# Root Cause Analysis

## The Five Whys

For each symptom, ask "why" until you reach a fundamental system or process cause:

1. **Symptom:** What went wrong?
2. **Direct cause:** What event triggered the failure?
3. **Contributing cause:** What conditions made the trigger possible?
4. **Systemic cause:** What process or design gap allowed the conditions to exist?
5. **Root cause:** What would need to change to prevent recurrence?

## Common Root Cause Categories

| Category | Example |
|----------|---------|
| **Logic error** | Incorrect condition, wrong variable, off-by-one |
| **Race condition** | Unprotected shared state, incorrect ordering assumption |
| **Configuration** | Wrong setting, missing environment variable, incorrect routing |
| **Data assumption** | Unexpected null, wrong type, malformed input |
| **Timeout/latency** | Missing timeout, insufficient wait, blocking call |
| **Resource exhaustion** | Memory leak, connection pool exhaustion, disk full |
| **Version mismatch** | Incompatible dependency versions, API contract drift |

## Verification

After identifying the root cause, verify by:
1. Creating a minimal reproduction that demonstrates the root cause
2. Applying the fix and confirming the reproduction no longer fails
3. Checking that the fix doesn't break related functionality
