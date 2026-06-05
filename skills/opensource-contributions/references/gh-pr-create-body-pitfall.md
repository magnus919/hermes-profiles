# gh pr create — body content shell expansion pitfall

## Problem

When the PR body contains characters that the shell interprets (backticks, curly braces, JSON, `$` variables), `gh pr create --body "..."` fails because the shell expands the content before passing it to gh.

**Example:** A body containing JSON-like text or backtick-wrapped inline code:

```bash
gh pr create --title "feat: add widget" --body '{"query": "test", "exclude_tags": ["vault:private"]}'
```

The shell interprets `{}`, `[]`, and other special characters, causing `gh` to error with `unknown argument` or similar.

## Fix: use --body-file

Write the body to a temporary file and pass it via `--body-file`:

```bash
cat > /tmp/pr-body.md << 'HEREDOC'
## Summary

## Changes

- 

## Related Issues

Closes #N

## Test Plan

- [ ]
HEREDOC

gh pr create --title "feat: ..." --body-file /tmp/pr-body.md --base main --head my-branch
```

The `'HEREDOC'` (quoted) prevents shell expansion of the content. This works for any body content including JSON, backticks, and special characters.

## When to use

Any PR body that contains:
- JSON or code blocks with `{}`
- Backtick-wrapped inline code
- Curly braces or square brackets
- Markdown with special characters

For plain-text bodies with no special characters, `--body "..."` is fine.
