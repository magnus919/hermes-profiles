## Phase 4: The Release Process (After Merge)

Once a PR is merged to the main branch, getting it to users requires a release.
This phase is often overlooked by contributors but essential for maintainers.

### Sequence After Merge

```bash
# 1. Pull the merged main
git checkout main && git pull

# 2. Update version and changelog
#    Edit pyproject.toml (version field) and CHANGELOG.md (new section)
git commit -s -m "chore: bump to vX.Y.Z"

# 3. VERIFY version matches before tagging
#    Run this check — if it fails, fix pyproject.toml before proceeding
PACKAGE_VERSION="$(grep -Po '^version = \"\K[^\"]+' pyproject.toml)"
echo "Package version: $PACKAGE_VERSION  Tag: v$PACKAGE_VERSION"

# 4. Tag and push (triggers release workflow on many projects)
git tag v$PACKAGE_VERSION && git push origin main --tags

# 4. Create a GitHub Release with notes
gh release create vX.Y.Z --title "vX.Y.Z — Title" --notes "..."
```

**Version numbering conventions:**
- `v1.0.0` — MAJOR: breaking changes
- `v0.4.0` — MINOR: new features (pre-1.0: significant additions)
- `v0.4.1` — PATCH: bug fixes (pre-1.0: small fixes)

### Release workflow anatomy

Many projects use a separate release workflow (`.github/workflows/release.yml`) that:
- Triggers on `v*` tag pushes (not on branch pushes)
- May gate on tests passing before publishing
- Publishes to a package registry (PyPI, npm, etc.) via trusted publishing OIDC
- Creates a deployment record visible on the repository's Deployments page

**Key gotcha:** Merging to main does NOT trigger the release workflow. You must
push the tag separately. If you forget, the release won't happen — no error,
no notification, just silence. The PyPI publish won't fire until the tag exists.

### GitHub Releases vs Tags

A tag is just a pointer to a commit. A GitHub Release is a tag + release notes
+ optional assets. They are separate concepts:

```bash
# Tag only (no release page, no announcement)
git tag v1.0.0 && git push origin v1.0.0

# Tag + GitHub Release
gh release create v1.0.0 --title "v1.0.0 — Title" --notes "..."
```

Always create a GitHub Release after tagging. The release notes are what users
see on the repository's Releases page, and what gets announced via GitHub's
notification system. Without a Release, the tag exists but is invisible to most
users.

### Handling release metadata

**`--body-file` for gh commands:** When your release notes or PR body contains
special characters (backticks, `&`, quotes, braces), use a file instead of an
inline string:

```bash
# WRONG — shell interprets special chars
gh release create v1.0.0 --notes '{"query": "test", "exclude_tags": ["private"]}'

# RIGHT — use a file
cat > /tmp/release.md << 'EOF'

Adds `exclude_tags` filtering.
EOF
gh release create v1.0.0 --title "v1.0.0" --notes-file /tmp/release.md
```

This avoids shell interpretation of backticks, `$` signs, curly braces, and
ampersands in structured text like JSON examples or code blocks.

### What to do when a commit accidentally lands on main

If you accidentally push a feature commit directly to `main` (bypassing the PR
process), the correct fix is:

```bash
# 1. Create a branch from the accidental commit
git branch feat/description HEAD

# 2. Revert the commit on main
git revert --no-edit HEAD
git push origin main

# 3. Push the branch and open a proper PR
git push -u origin feat/description
gh pr create --base main --head feat/description
```

Do NOT force-push to main to "undo" the commit — rewriting published history
causes problems for anyone who has already pulled. A revert is clean, auditable,
and doesn't require force push.

If the branch already exists (from `git checkout -b` that was never used),
delete it first:

```bash
git branch -D feat/description
git push origin --delete feat/description
# Then proceed with the steps above
```

**Cherry-pick note:** After reverting main, create the feature branch from the
current main (`git checkout -b feat/description main`) and cherry-pick the
original commit (`git cherry-pick <sha>`). This ensures the branch is based
on the current tip of main, not on a now-reverted ancestor.