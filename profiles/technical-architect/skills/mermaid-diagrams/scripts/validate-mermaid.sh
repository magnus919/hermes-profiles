#!/usr/bin/env bash
# validate-mermaid.sh — Validate a .mmd Mermaid file for syntax errors
# Uses Node.js mermaid.parse() for validation
#
# Usage: ./validate-mermaid.sh diagram.mmd
# Returns 0 if valid, 1 if invalid

set -euo pipefail

FILE="${1:-}"
if [ -z "$FILE" ]; then
  echo "Usage: $0 <file.mmd>"
  exit 1
fi

if [ ! -f "$FILE" ]; then
  echo "Error: $FILE not found"
  exit 1
fi

# Validate with Node.js mermaid.parse()
node -e "
const fs = require('fs');
const { parse } = require('mermaid');
const content = fs.readFileSync('$FILE', 'utf-8');
try {
  parse(content);
  console.log('✓ Valid Mermaid syntax');
  process.exit(0);
} catch(e) {
  console.error('✗ Invalid:', e.message);
  process.exit(1);
}
" 2>&1 || {
  # Fallback: check for common syntax issues
  echo "--- Common issue check ---"
  grep -n '^end$' "$FILE" | head -3 && echo "⚠  Lowercase 'end' found (should be case-context sensitive)"
  grep -n '-->o\|--o>' "$FILE" | head -3 && echo "⚠  Arrow with o/x found (may need spaces)"
  echo "Install mermaid: npm install mermaid"
  exit 1
}
