#!/usr/bin/env bash
# brand-book test suite
# Run: bash scripts/brand-book_test.sh

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BRAND_BOOK="$SCRIPT_DIR/brand-book"
TEMPLATES_DIR="$SCRIPT_DIR/../templates"
TEST_DIR="/tmp/brand-test-$$"
PASS=0
FAIL=0

cleanup() { rm -rf "$TEST_DIR"; }
trap cleanup EXIT

green() { printf "  \033[32m✓\033[0m %s\n" "$1"; ((PASS++)); }
red() { printf "  \033[31m✗\033[0m %s\n" "$1"; ((FAIL++)); }

echo "=== brand-book Test Suite ==="
echo ""

# 1. Smoke: CLI runs
if "$BRAND_BOOK" --help > /dev/null 2>&1; then
    green "CLI runs with --help"
else
    red "CLI --help failed"
fi

# 2. Init: scaffold a brand
mkdir -p "$TEST_DIR"
if "$BRAND_BOOK" init "$TEST_DIR/mybrand" --name "Acme Corp" > /dev/null 2>&1; then
    green "init scaffolds brand directory"
else
    red "init failed"
fi

# 3. Init creates 7 template files
COUNT=$(ls "$TEST_DIR/mybrand/"*.md 2>/dev/null | wc -l | tr -d ' ')
if [ "$COUNT" -eq 7 ]; then
    green "init creates 7 template files (got: $COUNT)"
else
    red "init created $COUNT files, expected 7"
fi

# 4. Validate a template
if "$BRAND_BOOK" validate "$TEST_DIR/mybrand/strategy.md" > /dev/null 2>&1; then
    green "validate runs on strategy template"
else
    red "validate failed on strategy template"
fi

# 5. Validate with --strict
if "$BRAND_BOOK" validate --strict "$TEST_DIR/mybrand/brand-card.md" > /dev/null 2>&1; then
    green "validate --strict runs on brand-card"
else
    red "validate --strict failed"
fi

# 6. Compile brand card
OUTPUT=$("$BRAND_BOOK" compile "$TEST_DIR/mybrand" --artifact brand-card 2>/dev/null)
if [ -n "$OUTPUT" ]; then
    green "compile --artifact brand-card produces output (${#OUTPUT} chars)"
else
    red "compile brand-card produced empty output"
fi

# 7. Compile full brand book
OUTPUT=$("$BRAND_BOOK" compile "$TEST_DIR/mybrand" --artifact full 2>/dev/null)
if [ -n "$OUTPUT" ]; then
    green "compile --artifact full produces output (${#OUTPUT} chars)"
else
    red "compile full produced empty output"
fi

# 8. Compile with --output
OUTFILE="$TEST_DIR/compiled.md"
"$BRAND_BOOK" compile "$TEST_DIR/mybrand" --artifact full --output "$OUTFILE" > /dev/null 2>&1
if [ -f "$OUTFILE" ]; then
    green "compile --output writes to file"
else
    red "compile --output did not create file"
fi

# 9. Preview
OUTPUT=$("$BRAND_BOOK" preview "$TEST_DIR/mybrand/strategy.md" 2>/dev/null)
if [ -n "$OUTPUT" ]; then
    green "preview produces output"
else
    red "preview produced empty output"
fi

# 10. Preview with --json
OUTPUT=$("$BRAND_BOOK" preview --json "$TEST_DIR/mybrand/strategy.md" 2>/dev/null)
if echo "$OUTPUT" | python3 -m json.tool > /dev/null 2>&1; then
    green "preview --json produces valid JSON"
else
    red "preview --json is not valid JSON"
fi

# 11. Validate with --json
OUTPUT=$("$BRAND_BOOK" validate --json "$TEST_DIR/mybrand/visual-id.md" 2>/dev/null)
if echo "$OUTPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); assert 'issues' in d; assert 'count' in d" > /dev/null 2>&1; then
    green "validate --json produces valid JSON with issues and count"
else
    red "validate --json format incorrect"
fi

# 12. Re-init on existing dir fails
mkdir -p "$TEST_DIR/nonempty"
touch "$TEST_DIR/nonempty/existing.txt"
if "$BRAND_BOOK" init "$TEST_DIR/nonempty" --name "Test" > /dev/null 2>&1; then
    red "init on non-empty directory should have failed"
else
    green "init rejects non-empty directory"
fi

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[ "$FAIL" -eq 0 ] || exit 1
