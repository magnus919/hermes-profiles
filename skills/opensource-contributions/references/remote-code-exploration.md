# Remote Code Exploration with `gh api`

When contributing to an unfamiliar open source project, you need to understand
the codebase before writing code. The fastest way is often **not** to clone the
repo — instead, use the GitHub API remotely to explore specific directories and
files.

## Why Remote First

| Approach | Cost | Best For |
|----------|------|----------|
| `gh repo clone` | Full clone (can be slow for large repos) | When you need to run the project or make many edits |
| `gh api repos/.../contents/` | One API call per directory | When you only need to study one area of the codebase |
| `gh api repos/.../git/trees` | One API call for the full tree | When you need the complete file listing |
| Web browser | Interactive but slow | When you need to read docs formatted for web |

For **studying a plugin/extension interface** before implementing, remote
exploration is usually faster because you only fetch the relevant files.

## Basic Commands

### List a directory

```bash
gh api repos/owner/repo/contents/path/to/dir --jq '.[].name'
```

This returns file/directory names in the target path. No clone needed.

### Read a file

```bash
gh api repos/owner/repo/contents/path/to/file.py --jq '.content' | base64 -d
```

The API returns file content base64-encoded. Decode inline.

### Read multiple files quickly

```bash
for f in __init__.py example_extractor.py; do
  echo "=== $f ==="
  gh api repos/owner/repo/contents/extractors/$f --jq '.content' | base64 -d
  echo
done
```

### Get the full source tree

```bash
gh api repos/owner/repo/git/trees/main?recursive=1 --jq '.tree[].path'
```

## When to Use This Pattern

- **Studying an interface before implementing against it** — read the base class
  (e.g., `BaseExtractor`), an existing implementation (e.g., `sessions.py`), and
  the wiring (e.g., CLI parser choices) in one shot
- **Checking if a certain type of file exists** — discover project structure
  without cloning
- **Quick validation** — verify that a pattern exists before writing code that
  depends on it

## When to Clone Instead

- You need to run the project (build, test)
- You're making changes that need local validation (test suite, linting)
- You're reading many files across many directories (API rate limits apply)
- The repo is small (clone is faster than N API calls)

## Pitfall: Base64 Decoding

The GitHub API returns file contents base64-encoded. Always pipe through
`base64 -d`. For large files, the API response may be truncated — in that
case, use `?ref=branchname` and check for `"truncated": true` in the response.
For truncated files, clone the repo instead.

## Pitfall: Binary Files

The `contents/` API endpoint does not work for binary files — it returns a
`"download_url"` instead of `"content"`. Use the download URL with `curl` for
binary assets.

## Pitfall: API Rate Limits

Unauthenticated requests are limited to 60/hour. Authenticated (`gh api`) uses
the OAuth token and gets 5000/hour. Always use `gh api` over bare `curl`.
