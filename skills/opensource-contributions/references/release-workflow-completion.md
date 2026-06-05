# Release Workflow Completion

Release lifecycle steps that are easy to miss — from a messy agent-assisted release cycle.

## The Full Release Cycle

After a feature PR merges, the complete sequence is:

1. **Update local main**
   ```bash
   git checkout main && git pull
   ```

2. **Create the release commit** (version bump in pyproject.toml + CHANGELOG entry)
   ```bash
   git commit -s -m "chore: bump to vX.Y.Z"
   git tag vX.Y.Z && git push origin main --tags
   ```

3. **Verify PyPI publish succeeded**
   ```bash
   curl -s https://pypi.org/pypi/<project>/json | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['info']['version'])"
   ```

4. **Create GitHub Release** (separate from tag — easy to forget)
   ```bash
   gh release create vX.Y.Z --title "vX.Y.Z — Title" --notes "..."
   ```

5. **Check the Releases page** — verify it shows at [github.com/owner/repo/releases](https://github.com/owner/repo/releases)

## Missed Release — Backfill

If a previous release tag exists but has no GitHub Release (common during build phases), backfill:

```bash
# Check what releases exist
gh release list --json tagName,name,createdAt

# Backfill a missing one
gh release create v0.3.0 --title "v0.3.0 — Title" --notes "Release notes..."
```

This is important for anyone browsing the project's release history — gaps make the project look abandoned.

## Release Workflow Failure Recovery

**Scenario:** Tag was pushed, release workflow ran, PyPI publish failed.

**Do NOT** push the same tag again — GitHub won't re-trigger the workflow. Instead:

**Option A — Keep the version, re-push the tag (risky):**
```bash
git tag -d vX.Y.Z              # delete locally
git push --delete origin vX.Y.Z  # delete remotely
# Then fix, commit, and re-tag on the fix commit
git tag vX.Y.Z && git push origin vX.Y.Z
```

**Option B — Bump the version (safer):**
```bash
# Increment patch version, update CHANGELOG
git commit -s -m "chore: bump to vX.Y.Z+1"
git tag vX.Y.Z+1 && git push origin main --tags
```

### Pitfall: Recreating a tag orphans its GitHub Release

If you delete and recreate a tag (Option A), the associated GitHub Release becomes a **draft**. The release page shows the tag but the release is in an unpublished state — users see nothing. This happens because the release is bound to the tag's original commit SHA, and the new tag points to a different commit.

After recreating the tag, check the release state:
```bash
gh release view vX.Y.Z --json isDraft,isPrerelease
```

If `isDraft` is true, publish:
```bash
gh release edit vX.Y.Z --draft=false
```

This also resets the "latest" flag — run `gh release edit vX.Y.Z --latest` if needed.

**Better to avoid the whole problem:** Prefer Option B (bump version) over Option A (recreate tag). The extra version number is cheap insurance against release metadata corruption.

### Pitfall: Version mismatch between pyproject.toml and tag

The tag name and the version in `pyproject.toml` MUST agree. If you tag `v0.5.0` but `pyproject.toml` still says `version = "0.4.0"`, the build produces `hermes_cashew-0.4.0-*` files and PyPI rejects them with `400 File already exists` (since 0.4.0 was already published).

**Check before tagging:**
```bash
grep '^version = ' pyproject.toml
# Must match the tag you're about to create
```

If you already tagged and pushed with the wrong version:
1. Delete the tag: `git tag -d vX.Y.Z && git push --delete origin vX.Y.Z`
2. Fix the version in `pyproject.toml` (via a PR)
3. Wait for PR to merge
4. Tag on the merge commit

**Don't fix the version AND tag on the same direct-to-main commit** — that's trading one process violation for another.

## Channeling Release Notes Without Shell Escaping

When your release notes or PR body contain special characters (backticks, `&`, quotes, braces, JSON), use a file instead of an inline string:

```bash
# Write notes to a file to avoid shell interpretation
cat > /tmp/release.md << 'EOF'
## Summary

Adds `exclude_tags` filtering.

### Usage
```json
{"query": "test", "exclude_tags": ["vault:private"]}
```
EOF

# Then reference the file
gh release create vX.Y.Z --title "Title" --notes-file /tmp/release.md
```

The `<< 'EOF'` (quoted delimiter) prevents the shell from expanding variables or interpreting backticks inside the heredoc.

## Post-Release Project Housekeeping

After any release, check these project metadata files for staleness:

| File | What to check |
|------|---------------|
| `AGENTS.md` | Version references, dependency specs, config key counts, architecture description, open issue count. **Must be updated** — the next AI agent session reads this to orient itself. Stale AGENTS.md causes agents to operate on wrong assumptions. |
| `README.md` | Version badge, feature descriptions, setup instructions, config reference |
| Issue tracker | Milestones that should be closed, issues that were resolved |

The AGENTS.md is especially important — it's what the next AI agent session reads to orient itself. Stale AGENTS.md causes agents to operate on wrong assumptions (wrong dependency type, wrong config shape, references to removed code).
