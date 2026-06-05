#!/usr/bin/env bash
# test_references_completeness.sh — Validate the researched code integration references
# 
# Checks:
# - All three reference files exist
# - Each covers the required topic areas
# - Each cross-references the parent skill
# - Source URLs are documented

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
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
echo "Code Integration References Test Suite"
echo "══════════════════════════════════════════════"
echo ""

# ── File existence ───────────────────────────────────────────────
echo "── File Existence ──────────────────────────"
echo ""

test_case "pytorch-integration.md exists" \
    test -f "$REPO_DIR/references/pytorch-integration.md"
test_case "sklearn-integration.md exists" \
    test -f "$REPO_DIR/references/sklearn-integration.md"
test_case "data-science-coding-workflow.md exists" \
    test -f "$REPO_DIR/references/data-science-coding-workflow.md"

# ── PyTorch reference coverage ─────────────────────────────────
echo ""
echo "── PyTorch Reference Coverage ─────────────"
echo ""

PT="$REPO_DIR/references/pytorch-integration.md"

for topic in "Device Management" "Training Loop" "DataLoader" "AMP" "Mixed Precision" \
             "torch.compile" "Transfer Learning" "LoRA" "Knowledge Distillation" \
             "Model Pruning" "DDP" "Distributed Data" "Reproducibility"; do
    test_case "Covers: $topic" grep -qi "$topic" "$PT"
done

test_case "Has device pattern (cuda/mps/cpu)" \
    grep -q "torch.device" "$PT"
test_case "Has gradient clipping" \
    grep -q "clip_grad_norm" "$PT"
test_case "Has model saving/loading pattern" \
    grep -q "torch.save\|model.state_dict" "$PT"
test_case "Has loss function table" \
    grep -q "CrossEntropyLoss\|BCEWithLogitsLoss\|MSELoss" "$PT"
test_case "Has learning rate schedulers" \
    grep -q "ReduceLROnPlateau\|CosineAnnealingLR\|OneCycleLR" "$PT"
test_case "Has debugging section" \
    grep -q "Debugging\|Common Failure" "$PT"
test_case "Source validated date present" \
    grep -q "Last reviewed\|Source validated" "$PT"
test_case "References pytorch.org" \
    grep -q "pytorch.org" "$PT"
test_case "References experimental-campaign-protocol" \
    grep -q "experimental-campaign-protocol" "$PT"

# ── sklearn reference coverage ─────────────────────────────────
echo ""
echo "── Scikit-Learn Reference Coverage ────────"
echo ""

SK="$REPO_DIR/references/sklearn-integration.md"

for topic in "Pipeline" "ColumnTransformer" "Preprocessing" "Model Selection" \
             "Cross-Validation" "GridSearchCV" "Ensemble" "Calibration" \
             "Imbalanced" "Feature Selection" "PCA" "Custom Estimator" \
             "Persistence" "Reproducibility"; do
    test_case "Covers: $topic" grep -qi "$topic" "$SK"
done

test_case "Has ColumnTransformer example" \
    grep -q "ColumnTransformer" "$SK"
test_case "Has OneHotEncoder + StandardScaler" \
    grep -q "OneHotEncoder\|StandardScaler" "$SK"
test_case "Has imputation (SimpleImputer/IterativeImputer)" \
    grep -q "SimpleImputer\|IterativeImputer" "$SK"
test_case "Has HalvingGridSearchCV" \
    grep -q "HalvingGridSearchCV" "$SK"
test_case "Has Random Forest example" \
    grep -q "RandomForest" "$SK"
test_case "Has XGBoost/LightGBM integration" \
    grep -q "XGBClassifier\|LGBMClassifier" "$SK"
test_case "Source validated date present" \
    grep -q "Last reviewed\|Source validated" "$SK"
test_case "References scikit-learn.org" \
    grep -q "scikit-learn.org" "$SK"
test_case "References experimental-campaign-protocol" \
    grep -q "experimental-campaign-protocol" "$SK"

# ── DS Coding Workflow coverage ────────────────────────────────
echo ""
echo "── DS Coding Workflow Coverage ────────────"
echo ""

WF="$REPO_DIR/references/data-science-coding-workflow.md"

for topic in "Project Directory" "Configuration" "Experiment Logging" \
             "MLflow" "Result Serialization" "Reproducibility" \
             "Data Versioning" "Unit Testing" "Docker" "Seed"; do
    test_case "Covers: $topic" grep -qi "$topic" "$WF"
done

test_case "Has directory structure layout" \
    grep -q "data/raw/\|data/processed/" "$WF"
test_case "Has MLflow example" \
    grep -q "mlflow" "$WF"
test_case "Has DVC reference" \
    grep -q "dvc\|DVC" "$WF"
test_case "Has JSON experiment log pattern" \
    grep -q "experiment_log\.json\|json" "$WF"
test_case "Has reproducibility section" \
    grep -q "Reproducibility\|random_state\|set_all_seeds" "$WF"
test_case "Has pitfalls table" \
    grep -q "Pitfall\|pitfall" "$WF"
test_case "Source validated date present" \
    grep -q "Last reviewed\|Source validated" "$WF"
test_case "References experimental-campaign-protocol" \
    grep -q "experimental-campaign-protocol" "$WF"

# ── Summary ──────────────────────────────────────────────────────
echo ""
echo "══════════════════════════════════════════════"
echo "Results: $PASS passed, $FAIL failed"
echo "══════════════════════════════════════════════"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
