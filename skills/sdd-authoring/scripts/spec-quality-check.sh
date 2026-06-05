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

MISSING=0

# Helper: check if a section exists as a heading
section_exists() {
  local section="$1"
  grep -qi "^##\s*$section\|^###\s*$section" "$SPEC" && return 0
  return 1
}

# Helper: check if "Acceptance Criteria" appears under "User Stories"
# by looking for AC patterns ([AC-XXX] or "### Acceptance Criteria")
acceptance_criteria_under_stories() {
  # Check for [AC-XXX.YY] references under a User Stories heading
  grep -qi "\[AC-\d" "$SPEC" && return 0
  # Check for ### Acceptance Criteria sub-headings
  grep -qi "^###\s*Acceptance Criteria" "$SPEC" && return 0
  return 1
}

echo "Checking: $SPEC"
echo ""

# Problem Statement
if section_exists "Problem Statement"; then
  echo "  ✓ Problem Statement"
else
  echo "  ✗ Problem Statement"
  MISSING=$((MISSING + 1))
fi

# Success Criteria
if section_exists "Success Criteria"; then
  echo "  ✓ Success Criteria"
else
  echo "  ✗ Success Criteria"
  MISSING=$((MISSING + 1))
fi

# Scope (In Scope or Out of Scope)
if section_exists "In Scope"; then
  echo "  ✓ In Scope"
else
  echo "  ✗ In Scope"
  MISSING=$((MISSING + 1))
fi
if section_exists "Out of Scope"; then
  echo "  ✓ Out of Scope"
else
  echo "  ✗ Out of Scope"
  MISSING=$((MISSING + 1))
fi

# User Stories
if section_exists "User Stories"; then
  echo "  ✓ User Stories"
else
  echo "  ✗ User Stories"
  MISSING=$((MISSING + 1))
fi

# Acceptance Criteria — checks top-level section OR inline under user stories
if section_exists "Acceptance Criteria" || acceptance_criteria_under_stories; then
  echo "  ✓ Acceptance Criteria (found: $(grep -c '\[AC-\|Acceptance Criteria' "$SPEC" || true) references)"
else
  echo "  ✗ Acceptance Criteria"
  MISSING=$((MISSING + 1))
fi

# Edge Cases
if section_exists "Edge Cases"; then
  echo "  ✓ Edge Cases"
else
  echo "  ✗ Edge Cases"
  MISSING=$((MISSING + 1))
fi

# Non-Functional Requirements
if section_exists "Non-Functional Requirements" || section_exists "NFR"; then
  echo "  ✓ Non-Functional Requirements"
else
  echo "  ✗ Non-Functional Requirements"
  MISSING=$((MISSING + 1))
fi

# Assumptions
if section_exists "Assumptions"; then
  echo "  ✓ Assumptions & Open Questions"
else
  echo "  ✗ Assumptions & Open Questions"
  MISSING=$((MISSING + 1))
fi

echo ""
if [ "$MISSING" -eq 0 ]; then
  echo "PASS: All required sections present in $SPEC"
  exit 0
else
  echo "FAIL: $MISSING required section(s) missing from $SPEC"
  exit 1
fi
