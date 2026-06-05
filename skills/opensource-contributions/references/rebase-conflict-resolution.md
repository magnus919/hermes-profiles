# Rebase Conflict Resolution

When a PR branch has diverged from `main` (because other PRs merged while yours was open), you need to rebase. If that rebase produces conflicts, here's how to resolve them systematically.

## The Workflow

```bash
# 1. Update main
git checkout main && git pull origin main

# 2. Rebase your branch onto main
git checkout feat/your-branch
git rebase main
```

**Expected outcomes:**
- `Successfully rebased` → no conflicts. Push with `--force-with-lease`.
- `CONFLICT (content): Merge conflict in <file>` → conflicts to resolve.

## Resolving Conflicts

### 1. Identify the conflict markers

```bash
grep -rn "<<<<<<<\|=======\|>>>>>>>" --include='*' . | grep -v node_modules | grep -v '.git/'
```

Each conflict looks like:

```
<<<<<<< HEAD (current branch's version — what's on main)
content from main
=======
content from your branch's commit
>>>>>>> commit-hash (your commit message)
```

### 2. Understand what each side represents

| Section | Meaning |
|---------|---------|
| `<<<<<<< HEAD` to `=======` | What's currently on `main` (the base you're rebasing onto) |
| `=======` to `>>>>>>> <sha>` | What your commit introduced |

During a rebase, you're applying your commits *on top of* main. `HEAD` = what's already on main; the bottom section = what your change tried to do.

### 3. Resolve the conflict

- **If both sides' content is needed** — keep both, in the right order.
- **If one side supersedes the other** — keep the version from main that already incorporates similar logic.
- **If both sides added independent content near the same line** — keep both, stacked.

Edit the file to produce the correct result, **removing all conflict markers**.

### 4. Verify no markers remain

```bash
grep -c "<<<<<<<\|>>>>>>>" <resolved-file>
# Must return 0
```

### 5. Stage and continue

```bash
git add <resolved-file(s)>
git rebase --continue
```

### 6. Handle editor hangs in non-interactive environments

If `git rebase --continue` opens an editor in a non-interactive terminal (agent session, CI), it will time out:

```bash
# Option A: Skip the editor entirely
GIT_EDITOR=true git rebase --continue

# Option B: Set EDITOR to a no-op
EDITOR=true git rebase --continue
```

This preserves the original commit message without requiring interactive editing.

### 7. Push the rebased branch

```bash
git push --force-with-lease origin feat/your-branch
```

**Use `--force-with-lease`, NOT `--force`.** `--force-with-lease` checks that no one else has pushed to the branch since you last fetched. It's safer.

### 8. Check the PR for resolved status

```bash
gh pr view <number> --json mergeable
# Should show "MERGEABLE" or clean
```

## Common Patterns

### Pattern A: Both sides added content to the same area (most common)

Both main and your branch added new sections near each other. Keep both, ordered logically.

```
<<<<<<< HEAD
- /council hybrid "question"    ← from main
=======
- /council premortem "question" ← from your branch
>>>>>>> feat/premortem-mode
```

Resolution:

```
- /council hybrid "question"
- /council premortem "question"
```

### Pattern B: One side refactored what the other changed

Main has a refactored version of the same code your branch touched. Read the version on main to understand the new structure, then re-apply your intent.

### Pattern C: Semantic conflicts (no merge markers but wrong behavior)

A rebase can succeed with zero conflict markers but produce incorrect behavior if the code on main changed the assumptions your code depends on. Always smoke-test after rebasing.

## Key Principles

1. **The rebase applies your commits one at a time.** If you have multiple commits, you'll resolve conflicts multiple times — once per commit. This is normal.

2. **Resolve each conflict in the context of the specific commit being applied.** Don't try to produce the final merged result in one shot — make each commit's change consistent with what's already on main at that point.

3. **Never force-push to main.** Force-push is for feature branches after rebase, where you're the sole contributor to that branch.

4. **Force-push requires user approval.** Always flag that a force-push is needed and wait for approval before executing.
