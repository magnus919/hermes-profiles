#!/usr/bin/env bash
# pyramid-status.sh — Audit a research project directory for Artifact Pyramid coverage
#
# Usage:
#   pyramid-status.sh [--layer 1|2|3] [--json] <project-directory>
#
# Scans the directory for:
#   Layer 1: files matching 01-*, *summary*, *dossier*
#   Layer 2: files matching 02-*, *analysis*, *market*, *competitive*, *technical*
#   Layer 3: files matching 03-*, *dossier*, *source*, *transcript*, *raw*, *data*
#
# Checks naming convention, content structure, and cross-references.

set -euo pipefail

# --- Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# --- Defaults ---
LAYER_FILTER=""
JSON_MODE=false

# --- Parse arguments ---
while [[ $# -gt 0 ]]; do
    case "$1" in
        --layer)
            LAYER_FILTER="$2"
            shift 2
            ;;
        --json)
            JSON_MODE=true
            shift
            ;;
        --help|-h)
            echo "Usage: pyramid-status.sh [--layer 1|2|3] [--json] <project-directory>"
            exit 0
            ;;
        *)
            PROJECT_DIR="$1"
            shift
            ;;
    esac
done

if [[ -z "${PROJECT_DIR:-}" ]]; then
    echo "Error: project directory required"
    echo "Usage: pyramid-status.sh [--layer 1|2|3] [--json] <project-directory>"
    exit 1
fi

if [[ ! -d "$PROJECT_DIR" ]]; then
    echo "Error: '$PROJECT_DIR' is not a directory"
    exit 1
fi

# --- Search patterns by layer ---
L1_PATTERNS=("01-*" "1-*" "*summary*" "*dossier*")
L2_PATTERNS=("02-*" "2-*" "*analysis*" "*market*" "*competitive*" "*technical*" "*feasibility*")
L3_PATTERNS=("03-*" "3-*" "*dossier*" "*source*" "*transcript*" "*raw*" "*data*")

count_layer() {
    local search_dir="$1"
    shift
    local files=()
    for pattern in "$@"; do
        while IFS= read -r -d '' f; do
            files+=("$f")
        done < <(find "$search_dir" -maxdepth 3 -type f -name "$pattern" -not -path '*/\.*' -print0 2>/dev/null || true)
    done
    if [[ ${#files[@]} -eq 0 ]]; then
        echo "0"
        return 0
    fi
    declare -a unique=()
    local f rp u
    for f in "${files[@]}"; do
        rp=$(realpath "$f" 2>/dev/null || echo "$f")
        local seen=false
        for u in "${unique[@]-}"; do
            if [[ "$u" == "$rp" ]]; then
                seen=true
                break
            fi
        done
        if ! $seen; then
            unique+=("$rp")
        fi
    done
    echo "${#unique[@]}"
    return 0
}

check_md_quality() {
    local dir="$1"
    local issues=0
    local findings=""
    while IFS= read -r -d '' f; do
        local has_yaml=false
        if head -1 "$f" 2>/dev/null | grep -q '^---$'; then
            has_yaml=true
        fi
        if ! $has_yaml; then
            local lines
            lines=$(wc -l < "$f" 2>/dev/null || echo 0)
            if [[ "$lines" -gt 5 ]]; then
                findings="${findings}  ${f##*/}: no frontmatter (${lines} lines, ${f})\n"
                issues=$((issues + 1))
            fi
        fi
    done < <(find "$dir" -maxdepth 3 -name '*.md' -not -name 'README.md' -print0 2>/dev/null || true)
    printf '%s\n' "$findings"
    echo "$issues"
}

check_cross_references() {
    local dir="$1"
    local missing_refs=0
    local findings=""
    while IFS= read -r -d '' f; do
        while IFS= read -r match; do
            local ref
            ref=$(echo "$match" | sed -n 's/.*\[\[\(.*\)\]\].*/\1/p' 2>/dev/null || true)
            if [[ -z "$ref" ]]; then
                ref=$(echo "$match" | sed -n 's/.*\[\(atom-[0-9]*\)\].*/\1/p' 2>/dev/null || true)
            fi
            if [[ -n "$ref" ]]; then
                local found_ref
                found_ref=$(grep -rl "$ref" "$dir" --include='*.md' 2>/dev/null | head -1 || true)
                if [[ -z "$found_ref" ]]; then
                    findings="${findings}  ${f##*/} references '${ref}' which is not found\n"
                    missing_refs=$((missing_refs + 1))
                fi
            fi
        done < <(grep -oP '\[\[.*?\]\]|\[atom-\d+\]' "$f" 2>/dev/null || true)
    done < <(find "$dir" -maxdepth 3 -name '*.md' -print0 2>/dev/null || true)
    printf '%s\n' "$findings"
    echo "$missing_refs"
}

# --- Gather stats ---
L1_COUNT=$(count_layer "$PROJECT_DIR" "${L1_PATTERNS[@]}")
L2_COUNT=$(count_layer "$PROJECT_DIR" "${L2_PATTERNS[@]}")
L3_COUNT=$(count_layer "$PROJECT_DIR" "${L3_PATTERNS[@]}")

L1_RESULTS=$(check_md_quality "$PROJECT_DIR" 2>/dev/null || true)
L1_FINDINGS="${L1_RESULTS%$'\n'*}"
L1_ISSUES="${L1_RESULTS##*$'\n'}"

REF_RESULTS=$(check_cross_references "$PROJECT_DIR" 2>/dev/null || true)
REF_FINDINGS="${REF_RESULTS%$'\n'*}"
MISSING_REFS="${REF_RESULTS##*$'\n'}"

# Fallback if parsing fails
if ! [[ "$L1_ISSUES" =~ ^[0-9]+$ ]]; then L1_ISSUES=0; fi
if ! [[ "$MISSING_REFS" =~ ^[0-9]+$ ]]; then MISSING_REFS=0; fi

if [[ "$L1_COUNT" -gt 0 ]]; then L1_PASS=true; else L1_PASS=false; fi
if [[ "$L2_COUNT" -gt 0 ]]; then L2_PASS=true; else L2_PASS=false; fi
if [[ "$L3_COUNT" -gt 0 ]]; then L3_PASS=true; else L3_PASS=false; fi

# --- JSON output ---
if $JSON_MODE; then
    cat <<EOF
{
  "project": "$(basename "$PROJECT_DIR")",
  "layers": {
    "1": { "name": "Summary", "count": $L1_COUNT, "present": $L1_PASS, "quality_issues": $L1_ISSUES },
    "2": { "name": "Analysis Collection", "count": $L2_COUNT, "present": $L2_PASS, "quality_issues": 0 },
    "3": { "name": "Detailed Dossiers", "count": $L3_COUNT, "present": $L3_PASS, "quality_issues": 0 }
  },
  "missing_references": $MISSING_REFS,
  "pyramid_health": $(if $L1_PASS && $L2_PASS && $L3_PASS; then echo '"complete"'; else echo '"incomplete"'; fi)
}
EOF
    exit 0
fi

# --- Human output ---
echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║  Artifact Pyramid Status Report                  ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "  Project: $(basename "$PROJECT_DIR")"
echo ""
echo "  Layer 1 — Summary"
if $L1_PASS; then
    echo -e "    ${GREEN}✓ Present${NC} (${L1_COUNT} file(s))"
else
    echo -e "    ${RED}✗ Missing${NC}"
fi
if [[ "$L1_ISSUES" -gt 0 ]]; then
    echo -e "    ${YELLOW}⚠  ${L1_ISSUES} quality issue(s)${NC}"
fi
echo ""
echo "  Layer 2 — Analysis Collection"
if $L2_PASS; then
  echo -e "    ${GREEN}✓ Present${NC} (${L2_COUNT} file(s))"
else
  echo -e "    ${RED}✗ Missing${NC}"
fi
echo ""
echo "  Layer 3 — Detailed Dossiers"
if $L3_PASS; then
    echo -e "    ${GREEN}✓ Present${NC} (${L3_COUNT} file(s))"
else
    echo -e "    ${RED}✗ Missing${NC}"
fi
echo ""
echo "  Cross-Reference Health"
if [[ "$MISSING_REFS" -gt 0 ]]; then
    echo -e "    ${YELLOW}⚠  ${MISSING_REFS} broken reference(s)${NC}"
else
    echo -e "    ${GREEN}✓ All references resolve${NC}"
fi
echo ""
echo "  Overall Pyramid Health"
if $L1_PASS && $L2_PASS && $L3_PASS; then
    echo -e "    ${GREEN}✓ Complete — all three layers present${NC}"
else
    echo -e "    ${YELLOW}◐ Partial — missing: $(if ! $L1_PASS; then echo -n 'L1 '; fi)$(if ! $L2_PASS; then echo -n 'L2 '; fi)$(if ! $L3_PASS; then echo -n 'L3 '; fi)${NC}"
fi
echo ""
