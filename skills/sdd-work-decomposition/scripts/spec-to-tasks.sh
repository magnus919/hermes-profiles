#!/usr/bin/env bash
# spec-to-tasks.sh - Validates that every spec requirement has a covering task.
# Usage: spec-to-tasks.sh [path/to/TASK-PLAN.md] [path/to/SPEC.md]
# Returns 0 if all spec sections are covered, 1 if any are uncovered.

set -euo pipefail

TASK_PLAN="${1:-TASK-PLAN.md}"
SPEC="${2:-SPEC.md}"

if [ ! -f "$TASK_PLAN" ]; then
  echo "ERROR: $TASK_PLAN not found"
  exit 1
fi

if [ ! -f "$SPEC" ]; then
  echo "WARNING: $SPEC not found — checking task self-consistency only"
  SPEC=""
fi

echo "Checking task coverage..."

# Extract spec section references from the task plan
# Look for patterns like "SPEC.md — Section X" or "Spec ref:"
SPEC_REFS=$(grep -oP 'SPEC\.md\s*[—–-]\s*Section\s+\S+' "$TASK_PLAN" 2>/dev/null || true)

if [ -z "$SPEC_REFS" ]; then
  # Try alternative pattern: "Spec ref: <text>"
  SPEC_REFS=$(grep -oP 'Spec ref[^:]*:\s*\S+' "$TASK_PLAN" 2>/dev/null || true)
fi

echo ""
echo "Found spec references in tasks:"
echo "$SPEC_REFS" | sort -u || echo "  (none found)"

# Extract AC references from the task plan
AC_REFS=$(grep -oP 'AC-\d+(\.\d+)?' "$TASK_PLAN" 2>/dev/null || true)

if [ -n "$AC_REFS" ]; then
  UNIQUE_ACS=$(echo "$AC_REFS" | sort -u)
  AC_COUNT=$(echo "$UNIQUE_ACS" | wc -l | tr -d ' ')
  echo "Unique ACs referenced: $AC_COUNT"
fi

# If spec is provided, check that key ACs appear in the task plan
if [ -n "$SPEC" ]; then
  EXTRACTED_ACS=$(grep -oP '\[AC-\d+(\.\d+)?\]' "$SPEC" 2>/dev/null | tr -d '[]' | sort -u || true)
  if [ -n "$EXTRACTED_ACS" ]; then
    MISSING_ACS=0
    for ac in $EXTRACTED_ACS; do
      if ! echo "$AC_REFS" | grep -q "$ac"; then
        echo "UNCOVERED: $ac in spec but not referenced in task plan"
        MISSING_ACS=$((MISSING_ACS + 1))
      fi
    done
    if [ "$MISSING_ACS" -gt 0 ]; then
      echo "FAIL: $MISSING_ACS AC(s) from spec not covered by tasks"
      exit 1
    fi
  fi
fi

echo ""
echo "PASS: Task coverage validation complete"
exit 0
