## Phase 3.5: Follow-up After Maintainer Scope Feedback

Sometimes a PR gets merged with a maintainer note that the fix is correct but **incomplete in scope** — it fixes the highest-leverage call site but misses others that need the same treatment. This is not a rejection; it's a direction to expand the fix systematically.

The correct response is a systematic follow-up: issue → PR, with a full call-site audit as the bridge between them.

> **Pre-flight checklist:** Before beginning a Phase 3.5 investigation, run
> the three-state check in `references/tracking-upstream-fix-status.md` to
> verify the fix isn't already in your local install, a released tag, or an
> existing open PR. This avoids duplicating work.

## Step 1: Understand the Scope Note

The maintainer's comment tells you exactly what they noticed was missing. Before doing anything, parse their note:

- **What specific call sites or patterns did they name?** (e.g., "`metrics.py` has seven more" or "`db.py::connect()` is the canonical factory")
- **What's the principle behind the gap?** (e.g., "every `sqlite3.connect()` call site needs this, not just the session module")
- **Is there an existing open PR from the maintainer** that already addresses part of the gap? Check their repo for related PRs.

### Step 2: Do a Full Call-Site Audit

Grep the entire codebase for the pattern that needs fixing, excluding tests initially (the maintainer's concern is production code):

```bash
# Find ALL direct call sites, excluding tests
grep -rn 'sqlite3\.connect' --include='*.py' core/ scripts/ other_dirs/ \
  | grep -v __pycache__ | grep -v test | grep -v 'busy_timeout'
```

Then build a **completion table** with four columns:

| Module | Call sites | Fixed by (PR) | Status |
|--------|-----------|---------------|--------|
| `core/session.py` | 1 | Your PR #56 | ✅ Fixed |
| `core/metrics.py` | 7 | — | ❌ Open |
| ... | ... | ... | ... |

**Key technique: cross-reference against existing PRs.** If there's an open PR (e.g., PR #59) that already covers most of the remaining sites, don't duplicate that work. Instead, identify what that PR *still misses*:

```bash
# Check which files an existing PR touches
git fetch origin pull/59/head:pr59
git diff main..pr59 --name-only

# Then check if any grep-identified sites fall outside those files
# Those are the remaining gaps
```

This gives you the precise delta: sites covered by your merged PR + sites covered by the existing follow-up PR = coverage. Anything left is your gap.

### Step 3: File a Comprehensive Issue

Open an issue that documents the full audit. Don't just say "we need to fix the metrics module too" — show the complete picture:

```markdown

**Context:** PR #56 added `X` to `core/session.py` as the highest-leverage call site.
The maintainer noted ([link to comment]) that `core/db.py::connect()` and
`core/metrics.py` also needed the same treatment.

**Completion table:**

| Module | Direct call sites | Status |
|--------|------------------|--------|
| `core/session.py` | 1 | Fixed by #56 |
| `core/db.py::connect()` | delegates to session | ✅ transitive |
| `core/metrics.py` | 7 | Covered by #59 |
| ... | ... | ... |
| `scripts/migrate_embeddings.py` | 3 | ❌ Still open |
| `extractors/obsidian.py` | 1 | ❌ Still open |

**Remaining gaps:**
- `extractors/obsidian.py` (1 site at line 191)
- `scripts/migrate_embeddings.py` (3 sites at lines 57, 128, 144)

**Suggested fix:** Apply the same `busy_timeout=5000` PRAGMA pattern used in #56.
```

The table format is critical. It shows the maintainer you did the full audit, found the gaps, and aren't duplicating existing open work. A table is scannable and leaves no ambiguity about what's been checked.

### Step 4: Create the Follow-up PR

The PR should:

1. **Only address remaining gaps** — don't redo files already covered by your merged PR or existing open PRs. Duplicating work creates merge conflicts and makes the maintainer's review harder.
2. **Follow the same fix pattern** as your original PR for consistency
3. **Update the issue reference** — close the scope-gap issue once merged

```bash
# Branch from the latest upstream main
git fetch upstream main
git checkout -b fix/remaining-busy-timeout-sites upstream/main

# Apply the same pattern to gap sites, commit, push
gh pr create --title "fix: apply busy_timeout=5000 to remaining sqlite3.connect sites" \
  --body "## Summary\n\nCompletes the scope outlined in #ISSUE_NUMBER.\n\n### Remaining sites\n- `extractors/obsidian.py` (line 191)\n- `scripts/migrate_embeddings.py` (lines 57, 128, 144)\n\n### Test plan\n- [ ] Syntax check on changed files\n- [ ] Existing test suite passes\n\nCloses #ISSUE_NUMBER"
```

### When There's Already an Open PR from the Maintainer

If the maintainer opened their own PR (#59) to address part of the scope:

1. **Don't open a competing comprehensive PR.** Instead, create a complementary PR that covers only the gaps the maintainer's PR missed.
2. **Reference both** the original issue/PR context and the maintainer's open PR in your issue and PR body.
3. **The maintainer's PR covers the bulk; your complementary PR handles the stragglers.** This is cleaner than one superseding PR — it respects the maintainer's work while filling the gap they overlooked.

### Pitfall: The Installed-Code Ambush

When tracking the status of an upstream fix you developed on your local machine, **check the installed code before reporting it as broken.** The local installed copy may already have the fix applied from your development work, even though the upstream release doesn't.

```bash
# Before assuming installed code is broken:
python -c "import inspect, core.embedding_service; print(inspect.getsource(core.embedding_service.get_default_service))"
```

If the fix is in the installed code, your local machine is fine — the gap is only for fresh installs of the unreleased version. This matters when you're deciding whether to prioritize a workaround vs. waiting for the upstream release.

The dual trap:
- **Direction 1:** Patching installed code without filing an issue or PR → erodes process (covered above as "The installed code trap")
- **Direction 2:** Assuming installed code is still broken when the fix was already applied locally → wasted investigation

Both directions have the same root cause: *asserting state without verification.* Fix: check first, speak second.

---