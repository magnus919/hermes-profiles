#!/usr/bin/env bash
# verification-report.sh - Generates an AC pass/fail matrix with gate verdict
# from structured input. Reads a JSON file with AC results and produces a
# formatted markdown report with auto-classified gate verdict.
# Usage: verification-report.sh [path/to/results.json]

set -euo pipefail

RESULTS="${1:-}"

if [ -n "$RESULTS" ] && [ ! -f "$RESULTS" ]; then
  echo "ERROR: $RESULTS not found"
  exit 1
fi

if [ -n "$RESULTS" ]; then
  PLAN=$(cat "$RESULTS" | python3 -c "
import sys, json
data = json.load(sys.stdin)
results = data.get('results', [])
total = len(results)
passed = sum(1 for r in results if r.get('status') == 'PASS')
failed = sum(1 for r in results if r.get('status') == 'FAIL')
blocked = sum(1 for r in results if r.get('status') == 'BLOCKING')
critical = sum(1 for r in results if r.get('status') == 'CRITICAL')
minor = sum(1 for r in results if r.get('status') == 'MINOR')

# Calculate compliance
if total > 0:
    compliance = round(passed * 100 / total, 1)
else:
    compliance = 0.0

# Determine gate verdict
verdict = 'APPROVED'
verdict_reason = 'All ACs pass.'
if blocked > 0:
    verdict = 'REJECTED'
    verdict_reason = f'{blocked} BLOCKING failure(s) — core requirement(s) unmet.'
elif critical > 2 and failed > 0:
    verdict = 'REJECTED'
    verdict_reason = f'{critical} CRITICAL failure(s) without documented remediation plans.'
elif compliance < 90 and blocked == 0:
    verdict = 'REJECTED'
    verdict_reason = f'Compliance {compliance}% below 90% threshold without documented exception.'
elif critical > 0:
    verdict = 'CONDITIONS'
    verdict_reason = f'{critical} CRITICAL failure(s) — requires documented remediation plan.'

print(f'TOTAL={total}')
print(f'PASS={passed}')
print(f'FAIL={failed}')
print(f'BLOCKING={blocked}')
print(f'CRITICAL={critical}')
print(f'MINOR={minor}')
print(f'COMPLIANCE={compliance}')
print(f'VERDICT={verdict}')
print(f'VERDICT_REASON={verdict_reason}')

# Print per-AC details
for r in results:
  ac_id = r.get('id', '???')
  status = r.get('status', 'UNKNOWN')
  evidence = r.get('evidence', '').replace('\n', ' | ')
  print(f'AC:{ac_id}\t{status}\t{evidence}')
" 2>/dev/null || echo "ERROR=parse_failure"
  )
else
  echo "Reading from stdin..."
  PLAN=$(cat)
fi

# Parse the results
TOTAL=$(echo "$PLAN" | grep "^TOTAL=" | cut -d= -f2)
PASSED=$(echo "$PLAN" | grep "^PASS=" | cut -d= -f2)
FAILED=$(echo "$PLAN" | grep "^FAIL=" | cut -d= -f2)
BLOCKING=$(echo "$PLAN" | grep "^BLOCKING=" | cut -d= -f2)
CRITICAL=$(echo "$PLAN" | grep "^CRITICAL=" | cut -d= -f2)
MINOR=$(echo "$PLAN" | grep "^MINOR=" | cut -d= -f2)
COMPLIANCE=$(echo "$PLAN" | grep "^COMPLIANCE=" | cut -d= -f2)
VERDICT=$(echo "$PLAN" | grep "^VERDICT=" | cut -d= -f2)
VERDICT_REASON=$(echo "$PLAN" | grep "^VERDICT_REASON=" | cut -d= -f2)

echo "## Verification Matrix"
echo ""
echo "| Metric | Value |"
echo "|--------|-------|"
echo "| Total ACs | ${TOTAL:-N/A} |"
echo "| Pass | ${PASSED:-0} |"
echo "| Fail | ${FAILED:-0} |"
echo "| Blocking | ${BLOCKING:-0} |"
echo "| Critical | ${CRITICAL:-0} |"
echo "| Compliance | ${COMPLIANCE:-0}% |"
echo "| **Gate Verdict** | **${VERDICT:-N/A}** |"
echo ""
echo "### Gate Verdict Rationale"
echo ""
if [ -n "$VERDICT_REASON" ]; then
  echo "${VERDICT_REASON}"
fi
echo ""
echo "### Per-AC Results"
echo ""
echo "| AC | Status | Evidence |"
echo "|----|--------|----------|"
echo "$PLAN" | grep "^AC:" | while IFS=$'\t' read -r ac_id status evidence; do
  ac_id="${ac_id#AC:}"
  echo "| $ac_id | $status | $(echo "$evidence" | head -c 100) |"
done
