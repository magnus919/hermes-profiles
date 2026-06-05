#!/usr/bin/env bash
# spec-quality-check.sh - Validates that a SPEC.md has all required sections.
# Usage: spec-quality-check.sh [path/to/SPEC.md]
# Returns 0 if all required sections are present, 1 if any are missing.

set -euo pipefail

SPEC="${1:-SPEC.md}"

if [ ! -f "$SPEC" ]; then
  echo "ERROR: $SPEC not found"
  exit 1
fi

REQUIRED_SECTIONS=(
  "Problem Statement"
  "Success Criteria"
  "In Scope"
  "Out of Scope"
  "User Stories"
  "Acceptance Criteria"
  "Edge Cases"
  "Non-Functional Requirements"
  "Assumptions"
)

MISSING=0
for section in "${REQUIRED_SECTIONS[@]}"; do
  if ! grep -qi "^##\s*$section\|^###\s*$section" "$SPEC"; then
    echo "MISSING: $section section"
    MISSING=$((MISSING + 1))
  else
    echo "FOUND: $section"
  fi
done

echo ""
if [ "$MISSING" -eq 0 ]; then
  echo "PASS: All required sections present in $SPEC"
  exit 0
else
  echo "FAIL: $MISSING required section(s) missing from $SPEC"
  exit 1
fi
