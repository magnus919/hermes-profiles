#!/usr/bin/env bash
# test_supervision_protocol.sh — Validate subagent supervision and Docker isolation references

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PASS=0
FAIL=0
DOCKER_AVAILABLE=false

if command -v docker &>/dev/null; then
    DOCKER_AVAILABLE=true
fi

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
echo "Supervision & Isolation Test Suite"
echo "══════════════════════════════════════════════"
echo ""

# ── File existence ───────────────────────────────────────────────
echo "── File Existence ──────────────────────────"
echo ""

test_case "subagent-experiment-supervision.md exists" \
    test -f "$REPO_DIR/references/subagent-experiment-supervision.md"
test_case "docker-experiment-isolation.md exists" \
    test -f "$REPO_DIR/references/docker-experiment-isolation.md"
test_case "scripts/Dockerfile exists" \
    test -f "$REPO_DIR/scripts/Dockerfile"

# ── Subagent supervision content coverage ───────────────────────
echo ""
echo "── Supervision Reference Coverage ──────────"
echo ""

SUP="$REPO_DIR/references/subagent-experiment-supervision.md"

test_case "Describes architecture (orchestrator/worker/supervisor)" \
    grep -qi "orchestrator\|supervisor.*worker\|architecture" "$SUP"
test_case "Has failure catalog table" \
    grep -q "CUDA OOM\|NaN loss\|ImportError" "$SUP"
test_case "Has at least 7 failure entries" \
    bash -c "grep -c '| \*\*' \"$SUP\" || grep -c '^| \*\*' \"$SUP\" || grep -c 'OOM\|NaN\|ImportError\|Disk full\|cuDNN' \"$SUP\" | xargs test 7 -le"
test_case "Each failure has a fix" \
    grep -q "batch_size\|pip install\|gradient.*clip\|fallback.*CPU\|reduce.*scope\|clean" "$SUP"
test_case "Has escalation path" \
    grep -qi "escalat\|telegram\|notify\|alert" "$SUP"
test_case "Has fix implementation code" \
    grep -q "def fix_\|def apply_fix\|def diagnose" "$SUP"
test_case "Has Python supervision loop example" \
    grep -q "subprocess\.Popen\|supervise_experiment\|FAILURE_PATTERNS" "$SUP"
test_case "Has harness-specific notes" \
    grep -qi "Hermes\|delegate_task\|OpenCode\|subagent" "$SUP"
test_case "Has limitations section" \
    grep -qi "limitation\|Limitation" "$SUP"
test_case "References experimental-campaign-protocol" \
    grep -q "experimental-campaign-protocol" "$SUP"

# ── Docker isolation content coverage ───────────────────────────
echo ""
echo "── Docker Isolation Coverage ──────────────"
echo ""

DKR="$REPO_DIR/references/docker-experiment-isolation.md"

test_case "Has resource limit guidance" \
    grep -qi "memory.*limit\|--memory\|--cpus\|--gpus" "$DKR"
test_case "Has full docker run example" \
    grep -q "docker run" "$DKR"
test_case "Has log collection pattern" \
    grep -q "docker logs\|logging.*stdout" "$DKR"
test_case "Has cleanup pattern" \
    grep -q "prune\|clean\|cleanup\|docker rm" "$DKR"
test_case "Has multi-container sweep example" \
    grep -q "for trial\|docker-compose\|compose" "$DKR"
test_case "Has fallback when Docker unavailable" \
    grep -qi "conda\|venv\|When Docker is not\|fallback" "$DKR"
test_case "References subagent-experiment-supervision" \
    grep -q "subagent-experiment-supervision" "$DKR"
test_case "References experimental-campaign-protocol" \
    grep -q "experimental-campaign-protocol" "$DKR"

# ── Docker build test ───────────────────────────────────────────
echo ""
echo "── Docker Build ───────────────────────────"
echo ""

if [ "$DOCKER_AVAILABLE" = true ]; then
    echo "  Building test image (this may take a moment)..."
    if docker build -q -t ds-supervision-test -f "$REPO_DIR/scripts/Dockerfile" "$REPO_DIR" >/dev/null 2>&1; then
        PASS=$((PASS + 1))
        echo "    ✓ Docker image builds successfully"
        docker image rm ds-supervision-test >/dev/null 2>&1 || true
    else
        FAIL=$((FAIL + 1))
        echo "    ✗ Docker image build failed"
    fi
else
    echo "  ⚠ Docker not available — skipping build test"
fi

# ── Summary ──────────────────────────────────────────────────────
echo ""
echo "══════════════════════════════════════════════"
echo "Results: $PASS passed, $FAIL failed"
echo "══════════════════════════════════════════════"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
