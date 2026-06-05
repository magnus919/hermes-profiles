#!/usr/bin/env bash
# test_detect_compute.sh — Test suite for detect-compute.py
#
# Usage:
#   bash scripts/test_detect_compute.sh          # Full test suite
#   bash scripts/test_detect_compute.sh --local  # Local host only (no Docker)
#   bash scripts/test_detect_compute.sh --docker # Docker tests only

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
DETECT_SCRIPT="$REPO_DIR/scripts/detect-compute.py"
TMPDIR="${TMPDIR:-/tmp}/ds-test-$$"
PASS=0
FAIL=0
DOCKER_AVAILABLE=false

if command -v docker &>/dev/null; then
    DOCKER_AVAILABLE=true
fi

mkdir -p "$TMPDIR"

cleanup() {
    rm -rf "$TMPDIR" 2>/dev/null || true
}
trap cleanup EXIT

# ── Helpers ───────────────────────────────────────────────────────

run_captured() {
    # Run a command, capture its stdout and stderr to files, return its exit code
    local name="$1"
    shift
    "$@" > "$TMPDIR/$name.stdout" 2>"$TMPDIR/$name.stderr"
    return $?
}

read_stdout() {
    cat "$TMPDIR/$1.stdout" 2>/dev/null
}

read_stderr() {
    cat "$TMPDIR/$1.stderr" 2>/dev/null
}

test_case() {
    local name="$1"
    shift
    local safe_name="${name// /_}"
    safe_name="${safe_name//\//_}"
    echo "  TEST: $name"
    if run_captured "$safe_name" "$@"; then
        echo "    ✓ PASS"
        PASS=$((PASS + 1))
    else
        local ec=$?
        echo "    ✗ FAIL (exit code $ec)"
        echo "    stdout: $(head -c 500 < "$TMPDIR/$safe_name.stdout")"
        echo "    stderr: $(head -c 500 < "$TMPDIR/$safe_name.stderr")"
        FAIL=$((FAIL + 1))
    fi
}

assert_json_valid() {
    local name="$1"
    python3 -c "import json; json.load(open('$TMPDIR/$name.stdout'))" 2>/dev/null
}

echo "══════════════════════════════════════════════"
echo "detect-compute.py Test Suite"
echo "══════════════════════════════════════════════"
echo ""

# ── Phase 1: Local host tests ────────────────────────────────────
echo "── Phase 1: Local Host ──────────────────────"
echo ""

test_case "Script runs without error" python3 "$DETECT_SCRIPT"
assert_json_valid "Script_runs_without_error" && echo "    ✓ Default output is JSON" || true

test_case "Python version detected" python3 -c "
import json
d = json.loads(open('$TMPDIR/Script_runs_without_error.stdout').read())
assert 'python_version' in d, 'Missing python_version'
print(d['python_version'])
"

test_case "--json produces valid JSON" python3 "$DETECT_SCRIPT" --json
assert_json_valid "--json_produces_valid_JSON" && echo "    ✓ --json output is valid JSON" || true

test_case "--json output has all required keys" python3 -c "
import json
d = json.loads(open('$TMPDIR/--json_produces_valid_JSON.stdout').read())
required = ['python_version', 'platform', 'has_cuda', 'torch', 'sklearn', 'recommendations']
for k in required:
    assert k in d, f'Missing key: {k}'
print(f'All {len(required)} required keys present')
"

test_case "--minimal returns only recommendations" python3 "$DETECT_SCRIPT" --minimal
assert_json_valid "--minimal_returns_only_recommendations" && echo "    ✓ --minimal output is valid JSON" || true

test_case "--minimal output has recommendation keys" python3 -c "
import json
d = json.loads(open('$TMPDIR/--minimal_returns_only_recommendations.stdout').read())
assert 'model_size_tier' in d, 'Missing model_size_tier'
assert 'feasible_techniques' in d, 'Missing feasible_techniques'
assert 'batch_size_guide' in d, 'Missing batch_size_guide'
print(f'Tier: {d[\"model_size_tier\"]}, techniques: {d[\"feasible_techniques\"]}')
"

test_case "--list-gpus runs without error" python3 "$DETECT_SCRIPT" --list-gpus

# ── Phase 2: Docker tests (no GPU, no torch) ────────────────────
echo ""
echo "── Phase 2: Docker (no GPU, no torch) ───────"
echo ""

if [ "$DOCKER_AVAILABLE" = true ] && [ "${1:-}" != "--local" ]; then
    DOCKER_TAG="ds-detect-test-$$"

    cat > "$TMPDIR/Dockerfile.nogpu" << 'DOCKERFILE'
FROM python:3.12-slim
RUN pip install --quiet --no-cache-dir scikit-learn numpy psutil
COPY scripts/detect-compute.py /scripts/detect-compute.py
WORKDIR /
DOCKERFILE

    mkdir -p "$TMPDIR/context/scripts"
    cp "$DETECT_SCRIPT" "$TMPDIR/context/scripts/detect-compute.py"
    cp "$TMPDIR/Dockerfile.nogpu" "$TMPDIR/context/Dockerfile"

    echo "  Building Docker test image (no GPU, no torch)..."
    docker build -t "$DOCKER_TAG" -f "$TMPDIR/context/Dockerfile" "$TMPDIR/context" >/dev/null 2>&1

    test_case "Docker: script runs" \
        docker run --rm "$DOCKER_TAG" python3 /scripts/detect-compute.py --json

    test_case "Docker: has_cuda is false" \
        docker run --rm "$DOCKER_TAG" python3 -c "
import json, subprocess, sys
r = subprocess.run([sys.executable, '/scripts/detect-compute.py', '--json'], capture_output=True, text=True)
d = json.loads(r.stdout)
assert d['has_cuda'] == False, 'GPU should not be detected in plain container'
assert d['nvidia'] == {}, 'nvidia should be empty'
print('OK: has_cuda=false, nvidia={}')
"

    test_case "Docker: torch is not available" \
        docker run --rm "$DOCKER_TAG" python3 -c "
import json, subprocess, sys
r = subprocess.run([sys.executable, '/scripts/detect-compute.py', '--json'], capture_output=True, text=True)
d = json.loads(r.stdout)
assert d['torch']['available'] == False, 'torch should not be available'
print('OK: torch not available')
"

    test_case "Docker: sklearn is available" \
        docker run --rm "$DOCKER_TAG" python3 -c "
import json, subprocess, sys
r = subprocess.run([sys.executable, '/scripts/detect-compute.py', '--json'], capture_output=True, text=True)
d = json.loads(r.stdout)
assert d['sklearn']['available'] == True, 'sklearn should be available'
print(f'sklearn {d[\"sklearn\"][\"version\"]}')
"

    test_case "Docker: recommendations reflect CPU-only" \
        docker run --rm "$DOCKER_TAG" python3 -c "
import json, subprocess, sys
r = subprocess.run([sys.executable, '/scripts/detect-compute.py', '--json'], capture_output=True, text=True)
d = json.loads(r.stdout)
rec = d['recommendations']
assert rec['model_size_tier'] == 'cpu_only', f'Expected cpu_only, got {rec[\"model_size_tier\"]}'
assert 'sklearn' in str(rec['feasible_techniques']), 'Should recommend sklearn'
print(f'Tier: {rec[\"model_size_tier\"]}, techniques: {rec[\"feasible_techniques\"]}')
"

    docker image rm "$DOCKER_TAG" >/dev/null 2>&1 || true
else
    echo "  (skipping — Docker not available or --local flag)"
fi

# ── Summary ──────────────────────────────────────────────────────
echo ""
echo "══════════════════════════════════════════════"
echo "Results: $PASS passed, $FAIL failed"
echo "══════════════════════════════════════════════"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
