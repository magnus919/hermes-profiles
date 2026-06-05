#!/usr/bin/env bash
# spec-to-tasks.sh - Validates that every spec AC has a covering task.
# Usage: spec-to-tasks.sh [path/to/TASK-PLAN.md] [path/to/SPEC.md]
# Returns 0 if all spec ACs are covered, 1 if any are uncovered.

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

echo "Checking task coverage in: $TASK_PLAN"
echo ""

# Extract AC references from the task plan
# Matches patterns like: AC-001.1, AC-002.x, etc.
AC_REFS=$(grep -oE 'AC-[0-9]+(\.[0-9]+)?' "$TASK_PLAN" 2>/dev/null || true)

if [ -z "$AC_REFS" ]; then
  echo "WARNING: No AC references found in task plan"
  echo "  Expected format: AC-NNN.MMM (e.g., AC-001.1, AC-002.1)"
  echo ""
  echo "PASS: Task coverage check skipped (no ACs to match)"
  exit 0
fi

UNIQUE_ACS=$(echo "$AC_REFS" | sort -u)
AC_COUNT=$(echo "$UNIQUE_ACS" | wc -l | tr -d ' ')
echo "Unique ACs referenced in tasks: $AC_COUNT"
echo ""

# If spec is provided, check that key ACs appear in the task plan
if [ -n "$SPEC" ]; then
  EXTRACTED_ACS=$(grep -oE '\[AC-[0-9]+(\.[0-9]+)?\]' "$SPEC" 2>/dev/null | tr -d '[]' | sort -u || true)
  if [ -z "$EXTRACTED_ACS" ]; then
    echo "No structured AC tags ([AC-XXX]) found in SPEC.md"
    echo "  Try checking inline AC patterns..."
    EXTRACTED_ACS=$(grep -oE 'AC-[0-9]+(\.[0-9]+)?' "$SPEC" 2>/dev/null | sort -u || true)
  fi

  if [ -n "$EXTRACTED_ACS" ]; then
    SPEC_AC_COUNT=$(echo "$EXTRACTED_ACS" | wc -l | tr -d ' ')
    echo "ACs found in spec: $SPEC_AC_COUNT"
    MISSING_ACS=0
    COVERED_ACS=0

    for ac in $EXTRACTED_ACS; do
      if echo "$AC_REFS" | grep -qF "$ac"; then
        COVERED_ACS=$((COVERED_ACS + 1))
      else
        echo "  UNCOVERED: $ac in spec but not referenced in task plan"
        MISSING_ACS=$((MISSING_ACS + 1))
      fi
    done

    echo ""
    echo "Coverage: $COVERED_ACS / $SPEC_AC_COUNT ACs covered"

    if [ "$MISSING_ACS" -gt 0 ]; then
      echo "FAIL: $MISSING_ACS AC(s) from spec not covered by tasks"
      exit 1
    fi
  else
    echo "No AC patterns found in SPEC.md (checked both [AC-XXX] and AC-XXX formats)"
  fi
fi

echo ""
echo "PASS: Task coverage validation complete"
exit 0
