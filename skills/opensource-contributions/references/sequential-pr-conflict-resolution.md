# Resolving Conflicts Between Sequential PRs

## Context

When implementing a chain of dependent PRs that modify the same files, merge conflicts are inevitable when upstream PRs merge before yours. This is a common pattern in multi-PR feature rollouts and has a systematic resolution strategy.

## The Pattern

Three times in one session this pattern appeared: both PRs added independent code to the same file. The conflicts were merge artifacts, not competing design decisions. In every case, the correct resolution was to **keep both sets of changes**.

## Resolution Workflow

### Step 1: Check PR status

```bash
gh pr view N --json mergeStateStatus,mergeable
# MERGEABLE = clean, CONFLICTING = needs attention
```

### Step 2: Fetch and merge

```bash
git fetch upstream main
git merge upstream/main
```

**Always use `merge` (not `rebase`)** on shared PR branches. Rebase rewrites history — force-pushing after review hurts the audit trail.

### Step 3: Identify conflict regions

```bash
grep -n "<<<<<<<\|=======\|>>>>>>>" path/to/file.py
```

### Step 4: Resolve each conflict

For each conflict region, determine if the changes are:

1. **Independent additions** — both heads add new code that doesn't overlap logically.
   → Keep both. Remove conflict markers.
2. **Competing changes** — both modify the same logical block.
   → Evaluate which is correct; upstream usually wins since it's been reviewed.
3. **Dependency chain** — one adds a function the other side calls.
   → Keep both.

**Safe default:** when in doubt about two independent additions, keep both. If they conflict, syntax check catches it:

```bash
python3 -c "import ast; ast.parse(open('path/to/file.py').read())"
```

### Step 5: Stage, commit, push

```bash
git add path/to/resolved/file.py
git commit -s -m "Merge upstream/main into feat/my-feature

Resolved conflict(s) in path/to/file.py:
- kept both X and Y changes"
git push upstream HEAD
```

### Step 6: Notify the reviewer

Add a PR comment noting which files conflicted and how they were resolved.

## Proactive Avoidance

- **Implement foundation PRs first** — get model changes merged before building on them
- **No branch stacking** — always branch from main, not from unmerged feature branches
- **Merge upstream/main before pushing** on branches older than a day

## When NOT to merge (rebase instead)

Before any reviews: rebase for clean linear history.

```bash
git fetch upstream main
git rebase upstream/main
git push --force-with-lease upstream HEAD
```

After first review: **use merge** — force-push destroys the review audit trail.

## Worked Example

PR #36 (cookie persistence) conflicted with PR #32 (stealth config) in `browser-svc/app.py`:

**Conflict 1 — Constants:** Both PRs added constant definitions to the same area. Resolution: keep both sections.
**Conflict 2 — Navigate action:** PR #36 added cookie injection, PR #32 added Cloudflare-aware navigation. Resolution: merged — inject cookies → cloudflare-aware navigate → store cookies.

```
git add browser-svc/browser_svc/app.py
git commit -s -m "Merge upstream/main into feat/cookie-persistence

Resolved conflicts in browser-svc/browser_svc/app.py:
- Kept both cookie persistence constants and stealth config constants
- Merged navigate action: cookie injection + Cloudflare-aware nav + cookie storage"
```
