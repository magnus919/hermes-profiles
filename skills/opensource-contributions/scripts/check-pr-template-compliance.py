#!/usr/bin/env python3
"""
PR Template Compliance Checker

Validates that a PR body matches the structure of the project's PR template.
Exits 0 (compliant) or 1 (non-compliant) with a reason.

Usage:
    python3 check-pr-template-compliance.py /tmp/pr-body.md /tmp/pr-template.md

The checker verifies:
- Every section header from the template appears in the body
- Required sections are not empty
- Checkboxes are present when the template includes them
"""

import re
import sys


def extract_section_headers(text: str) -> list[str]:
    """Extract markdown section headers (## or ###) from text."""
    headers = re.findall(r'^(#{2,3})\s+(.+)$', text, re.MULTILINE)
    return [h[1].strip() for h in headers]


def extract_checkboxes(text: str) -> list[str]:
    """Extract checkbox items from text."""
    return re.findall(r'-\s*\[\s*[ x]?\s*\]\s*(.+)', text)


def has_content(text: str, header: str) -> bool:
    """Check if a section has substantive content (not just N/A or empty)."""
    pattern = re.compile(rf'^#{{2,3}}\s+{re.escape(header)}\s*$', re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return False
    # Get content after this header until the next header or end
    start = match.end()
    remainder = text[start:].lstrip('\n')
    # Find next header
    next_header = re.search(r'^#{2,3}\s+', remainder, re.MULTILINE)
    section_text = remainder[:next_header.start()] if next_header else remainder
    section_text = section_text.strip()
    # Empty or only N/A/not applicable
    if not section_text:
        return False
    if section_text.lower() in ('n/a', 'na', 'not applicable', 'none'):
        return False
    return True


def main():
    if len(sys.argv) < 3:
        print("Usage: check-pr-template-compliance.py <pr-body.md> <pr-template.md>")
        sys.exit(1)

    body_path = sys.argv[1]
    template_path = sys.argv[2]

    try:
        with open(body_path) as f:
            body = f.read()
    except FileNotFoundError:
        print(f"FAIL: PR body file not found: {body_path}")
        sys.exit(1)

    try:
        with open(template_path) as f:
            template = f.read()
    except FileNotFoundError:
        print(f"SKIP: No template found at {template_path} — skipping compliance check")
        sys.exit(0)

    template_headers = extract_section_headers(template)
    body_headers = extract_section_headers(body)

    missing = [h for h in template_headers if h not in body_headers]
    empty_sections = [h for h in template_headers if h in body_headers and not has_content(body, h)]

    if missing:
        print(f"FAIL: Missing required template sections: {', '.join(missing)}")
        sys.exit(1)

    if empty_sections:
        print(f"WARN: Empty or N/A sections: {', '.join(empty_sections)}")

    # Check checkboxes
    template_checkboxes = extract_checkboxes(template)
    body_checkboxes = extract_checkboxes(body)
    missing_boxes = [c for c in template_checkboxes if c not in body_checkboxes]
    if missing_boxes:
        print(f"WARN: Missing checkboxes: {', '.join(missing_boxes)}")

    print("PASS: PR body complies with template")
    sys.exit(0)


if __name__ == '__main__':
    main()
