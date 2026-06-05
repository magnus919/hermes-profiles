# Worked Example: Multi-PR Plan Execution Across Dependent Changes

## Context

A project needed two parallel feature tracks — backend model changes and browser automation — with a dependency chain of 8 issues spanning multiple microservices.

**Gaps discovered during testing:**
1. **No binary content support** — the scraper only produces markdown
2. **No Cloudflare bypass** — the browser service was trivially detectable as a bot

## Phase 0a: Contribution Infrastructure

Before filing any issues, set up `.github` templates and update CONTRIBUTING.md:

```
.github/
├── ISSUE_TEMPLATE/
│   ├── bug_report.md
│   └── feature_request.md
└── PULL_REQUEST_TEMPLATE.md
```

CONTRIBUTING.md updated with Conventional Commits + DCO sign-off + PR template reference.

## Phase 1: Ideation → Issues

Gaps were ideated into a dependency graph of 8 issues:

| # | Title | Track | Depends on |
|---|-------|-------|------------|
| #1 | Binary content response model | Gap 1 | — (foundation) |
| #2 | Stealth browser config | Gap 2 | — (foundation) |
| #3 | CLI download subcommand | Gap 1 | — (independent) |
| #4 | Content-type detection | Gap 1 | #1 |
| #5 | Cookie persistence | Gap 2 | #2 |
| #6 | Auto-recovery pipeline | Gap 1 | #4 |
| #7 | CAPTCHA-solving sidecar | Gap 2 | #2, #5 |
| #8 | Classification-based routing | Both | #6 |

Each issue body included a `## Dependencies` section:
- `**Requires:** #1 — cannot implement without this`
- `**Independent of:** #3 — separate scope`

### Key lesson: filing issues is the midpoint, not the finish line

After filing all issues, the next step is implementing the PRs. Filing issues documents the roadmap; implementing them delivers it.

## Phase 2: Multi-PR Execution

6 PRs were implemented following the dependency chain:

| PR # | Issue | Scope | Depends on |
|------|-------|-------|------------|
| A | #1 — Response model | API layer | — |
| B | #2 — Stealth browser | Browser service | — |
| C | Phase 0a — Templates | 4 config files | — |
| D | #3 — CLI download | CLI tool | — |
| E | #4 — Content detection | Scraper pipeline | A |
| F | #5 — Cookie persistence | Browser service | B |

### Execution pattern

Each PR followed the same workflow:
1. `git checkout main && git checkout -b feat/<descriptive-name>`
2. Implement changes
3. Verify syntax: `python3 -c "import ast; ast.parse(open('file').read())"`
4. `git add` + `git commit -s -m "type: description"`
5. `git push upstream HEAD`
6. `gh pr create --body-file /tmp/pr-body.md`

### Dependency handling

For dependent PRs (e.g., PR E depended on PR A's model changes):
- Branch was from main (not from the foundation branch)
- Code referenced new fields not yet on main
- PR body documented the dependency explicitly
- Foundation PRs submitted first — reviewer merges in order
- No branch stacking — each PR reviewable independently

## What Worked Well

- **Issue dependency metadata** made the roadmap navigable from any single issue
- **Foundation-first implementation** avoided merge conflicts
- **Consistent branch naming** (`feat/<feature>`) made relationships obvious
- **Syntax verification before commit** caught errors early
- **`--body-file` for PR creation** avoided shell escaping issues with special characters

## Common Pitfalls Encountered

- **File truncation during agent tool use**: Reading a file with a line-number-prefixed tool and writing it back can truncate content. Use direct Python file I/O (`open()`/`read()`/`write()`) for round-trips on large files.
- **Non-unique search patterns**: The patch tool failed on non-unique patterns in large files. Use precise surrounding context for reliable string matching.

## Key Metrics

- 12 distinct work items (4 infrastructure + 8 issues)
- 6 PRs submitted
- ~490 lines of code changed across 5 microservices
- Zero merge conflicts between dependent PRs
