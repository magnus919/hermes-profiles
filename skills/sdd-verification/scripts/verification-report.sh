#!/usr/bin/env bash
# verification-report.sh - Generates an acceptance criteria pass/fail matrix
# from structured input. Reads a JSON file with AC results and produces a
# formatted markdown report.
# Usage: verification-report.sh [path/to/results.json]

set -euo pipefail

RESULTS="${1:-}"

if [ -n "$RESULTS" ] && [ ! -f "$RESULTS" ]; then
  echo "ERROR: $RESULTS not found"
  exit 1
fi

if [ -n "$RESULTS" ]; then
  # Read from JSON file with format:
  # {"results": [{"id": "AC-001.1", "status": "PASS", "evidence": "..."}, ...]}
  PLAN=$(cat "$RESULTS" | python3 -c "
import sys, json
data = json.load(sys.stdin)
results = data.get('results', [])
total = len(results)
passed = sum(1 for r in results if r.get('status') == 'PASS')
failed = sum(1 for r in results if r.get('status') == 'FAIL')
blocked = sum(1 for r in results if r.get('status') == 'BLOCKING')

print(f'TOTAL={total}')
print(f'PASS={passed}')
print(f'FAIL={failed}')
print(f'BLOCKING={blocked}')

# Print per-AC details
for r in results:
  ac_id = r.get('id', '???')
  status = r.get('status', 'UNKNOWN')
  evidence = r.get('evidence', '').replace('\n', ' | ')
  print(f'AC:{ac_id}\t{status}\t{evidence}')
" 2>/dev/null || echo "ERROR=parse_failure"
  )
else:
  echo "Reading from stdin..."
  PLAN=$(cat)
fi

# Parse the results
TOTAL=$(echo "$PLAN" | grep "^TOTAL=" | cut -d= -f2)
PASSED=$(echo "$PLAN" | grep "^PASS=" | cut -d= -f2)
FAILED=$(echo "$PLAN" | grep "^FAIL=" | cut -d= -f2)
BLOCKING=$(echo "$PLAN" | grep "^BLOCKING=" | cut -d= -f2)

echo "## Verification Matrix"
echo ""
echo "| Metric | Value |"
echo "|--------|-------|"
echo "| Total ACs | ${TOTAL:-N/A} |"
echo "| Pass | ${PASSED:-0} |"
echo "| Fail | ${FAILED:-0} |"
echo "| Blocking | ${BLOCKING:-0} |"
echo "| Compliance | $(echo "scale=1; ${PASSED:-0} * 100 / ${TOTAL:-1}" | bc 2>/dev/null)% |"
echo ""
echo "### Per-AC Results"
echo ""
echo "| AC | Status | Evidence |"
echo "|----|--------|----------|"
echo "$PLAN" | grep "^AC:" | while IFS=$'\t' read -r ac_id status evidence; do
  ac_id="${ac_id#AC:}"
  echo "| $ac_id | $status | $(echo "$evidence" | head -c 100) |"
done
