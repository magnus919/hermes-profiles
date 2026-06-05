#!/usr/bin/env bash
# test_campaign_protocol.sh — Structural validation for experimental-campaign-protocol.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REF="$REPO_DIR/references/experimental-campaign-protocol.md"
PASS=0
FAIL=0

test_case() {
    local name="$1"
    shift
    echo "  TEST: $name"
    if "$@" 2>/dev/null; then
        echo "    ✓ PASS"
        PASS=$((PASS + 1))
    else
        echo "    ✗ FAIL"
        FAIL=$((FAIL + 1))
    fi
}

echo "══════════════════════════════════════════════"
echo "Experimental Campaign Protocol Test Suite"
echo "══════════════════════════════════════════════"
echo ""

# ── File existence ───────────────────────────────────────────────
echo "── File Structure ──────────────────────────"
echo ""

test_case "Reference document exists" test -f "$REF"

# ── Phase headings ───────────────────────────────────────────────
echo ""
echo "── Phase Coverage ──────────────────────────"
echo ""

for phase_num in 1 2 3 4 5 6 7 8; do
    test_case "Phase $phase_num has heading" \
        grep -q "Phase $phase_num:" "$REF"
done

test_case "All 8 phase headings present" \
    bash -c "grep -c '^## Phase' \"$REF\" | xargs test 8 -eq"

# ── Entry/exit criteria ──────────────────────────────────────────
echo ""
echo "── Structural Elements ─────────────────────"
echo ""

test_case "Each phase has 'Entry criteria'" \
    bash -c "grep -c 'Entry criteria' \"$REF\" | xargs test 8 -eq"

test_case "Each phase has 'Exit criteria'" \
    bash -c "grep -c 'Exit criteria' \"$REF\" | xargs test 8 -eq"

test_case "Each phase has 'Failure modes'" \
    bash -c "grep -c 'Failure modes' \"$REF\" | xargs test 8 -eq"

# ── Code integration ─────────────────────────────────────────────
echo ""
echo "── Code Integration ────────────────────────"
echo ""

test_case "Contains sklearn Pipeline example" grep -q "sklearn.pipeline" "$REF"
test_case "Contains PyTorch training loop" grep -q "torch.*optim.*AdamW\|DataLoader\|model.train()" "$REF"
test_case "Contains Optuna example" grep -q "optuna" "$REF"
test_case "Contains distillation code" grep -q "distillation\|KL.*div\|teacher" "$REF"
test_case "Contains pruning reference" grep -q "prune" "$REF"

# ── Cross-references ─────────────────────────────────────────────
echo ""
echo "── Cross-References ────────────────────────"
echo ""

for ref_name in "detect-compute" "pytorch-integration" "sklearn-integration" \
                "data-science-coding-workflow" "subagent-experiment-supervision" \
                "docker-experiment-isolation"; do
    test_case "References $ref_name" \
        grep -q "$ref_name" "$REF"
done

# ── Quick reference completeness ─────────────────────────────────
echo ""
echo "── Appendix ────────────────────────────────"
echo ""

test_case "Has skip-guide table" grep -q "Skip to" "$REF"
test_case "Has directory structure" grep -q "experiments/" "$REF"
test_case "Has seed-setting code" grep -q "set_seed\|random.seed.*np.*torch" "$REF"
test_case "Has experiment logging template" grep -q "experiment_id" "$REF"

# ── Summary ──────────────────────────────────────────────────────
echo ""
echo "══════════════════════════════════════════════"
echo "Results: $PASS passed, $FAIL failed"
echo "══════════════════════════════════════════════"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
