# Tracking Upstream Fix Status — Three-State Checklist

When tracking a fix or feature you developed, that was merged upstream, but you're
unsure whether it has landed in your local installation or a released version yet.
Check the three states **in this order** to avoid wasted investigation.

## State 1: Local Installed Code

**Check the actual disk copy**, not just `pip show`.

```bash
# Quick — is the version number newer than when you submitted the fix?
pip show package-name

# More precise — inspect the specific function for your fix
python3 -c "
import inspect
from core.embedding_service import get_default_service
print(inspect.getsource(get_default_service))
"
```

The version number can be misleading if:
- The fix was applied locally during development but not released yet
- The package was installed from a git branch or source checkout
- You patched the site-packages copy during debugging

**Always inspect the code before assuming it's broken.** The fix may already be
on your machine even though upstream hasn't tagged a release.

## State 2: Upstream Release Tags

The upstream repo's tags tell you which fixes are in which release:

```bash
# Clone fresh (or fetch existing)
git clone git@github.com:owner/repo.git /tmp/check-repo
cd /tmp/check-repo

# Find the fix commit
git log --oneline --all | grep -i "keyword"

# Check if it's in any release tag
git tag --contains <commit-sha>
```

If no tag contains the commit, the fix hasn't been released. You need either:
- A new upstream release
- Pinning to `main` in your dependencies
- Applying the patch locally (not recommended for production)

## State 3: Open PRs on Upstream

Before doing any original work, check whether someone else (including the
maintainer) already opened a PR addressing the same gap:

```bash
# Search open PRs by topic
gh pr list --repo owner/repo --state open --limit 20

# Search for related terms
gh pr list --repo owner/repo --state open --search "busy_timeout" --json title,number,author

# If your fix had a scope-gap follow-up (Phase 3.5), the maintainer may
# have opened their own PR addressing the remaining sites
```

If an open PR already covers the scope, don't duplicate — instead:
- Do a full call-site audit to find what it misses
- Comment on the existing PR with findings
- Create a complementary PR for the gaps

## Combined Flow

```
                    ┌──────────────────────┐
                    │ Start tracking a fix  │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │ Check installed code  │──── The fix is here? → ✅ Done
                    │ (inspect source)      │
                    └──────────┬───────────┘
                               │ Not present
                    ┌──────────▼───────────┐
                    │ Check upstream tags   │──── Tagged? → Upgrade pip / npm / etc.
                    │ (git tag --contains)  │
                    └──────────┬───────────┘
                               │ Not tagged
                    ┌──────────▼───────────┐
                    │ Check open PRs        │──── PR exists? → Audit + complement
                    │ (gh pr list --search) │
                    └──────────┬───────────┘
                               │ No PR
                    ┌──────────▼───────────┐
                    │ File issue +          │
                    │ create PR ourselves   │
                    └──────────────────────┘
```

## Why This Order Matters

- **Local first** — the fastest resolution is "it's already here." Checking the
  disk avoids an upstream investigation that may be irrelevant.
- **Tags before PRs** — if the fix is already released, you don't need to open
  or search for PRs at all.
- **PRs before issue-filing** — if someone else already did the work,
  contributing to their PR is better than creating a competing one.
