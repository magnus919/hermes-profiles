## Pitfalls

### Backtick expansion in `--title`

See `github-issues` skill for the full treatment. In short: don't use backticks in double-quoted shell strings — they undergo command substitution.

```bash
# WRONG — backticks get shell-expanded
gh issue create --title "`command` crashes with error"

# RIGHT — single quotes
gh issue create --title '`command` crashes with error'

# RIGHT — no backticks in title
gh issue create --title "command crashes with error"
```

### Silent failure on non-existent labels

`gh issue create --label "nonexistent"` exits 1 and creates nothing. Verify labels first:

```bash
gh label list  # See what exists
```

Or create the issue without labels and add them after:

```bash
gh issue create --title "..." --body "..."
gh issue edit <NUMBER> --add-label "bug"
```

### The "I'll just fix it quickly" trap

The smallest-seeming changes can have the most impact. A one-line "fix" that changes behavior without understanding the architecture can break subtle edge cases. Always:
1. Understand why the code is the way it is
2. Check if tests exist for the area you're changing
3. Run the full test suite, not just your new test

### Premature PRs for discussion-mode ideas

When the user is workshopping an idea ("what if we contributed X?", "imagine a feature that Y"), do NOT interpret that as a directive to fork, branch, and create a PR. This is discussion mode. Wait for explicit directive signals like "create the PR", "file the issue", "send the patch" before executing.

### Force-push etiquette

Unless CONTRIBUTING.md explicitly asks for rebased/clean history (Linux kernel style), **do not force-push** to an open PR after a reviewer has looked at it. Force-pushing destroys the review history and makes it impossible to see what changed between review rounds. Add fixup commits instead. Maintainers can squash on merge.

### CI debugging workflow

When CI fails after a push, the systematic debugging loop is documented in `references/ci-debugging-loop.md`. It covers: reading CI logs, reproducing locally, isolating pre-existing vs new failures, common root cause categories (env var leakage, stale metadata, refactored methods, immutable types), and the fix-verify loop.

### CI as a testing crutch

Don't push broken code assuming CI will catch it. Run tests locally first. CI should confirm your work is clean, not discover basic failures. Pushing obviously broken code wastes maintainer CI resources (which the project pays for).

### Not all labels are the same

Some projects use labels like `good first issue` to indicate approachability. Others use `help wanted` for anything they'd accept help on. Still others tag issues with `needs reproduction` or `needs discussion`. Understand the project's label taxonomy before picking up issues.

### Pitfall: `gh pr create --base main` fails silently on repos with custom default branches

The most common reason for `gh pr create` to fail with an opaque "Base ref must be a branch" error is that the target repo's default branch isn't named `main`. Many older or differently-configured repos use `master`, `develop`, or `trunk`.

**The fix is a one-line discovery step before PR creation:**

```bash
BASE_BRANCH=$(gh repo view owner/repo --json defaultBranchRef --jq '.defaultBranchRef.name')
gh pr create --repo owner/repo --base "$BASE_BRANCH" ...
```

This applies to both same-repo and cross-fork PRs. The cross-fork section above now includes this as step 2 in the troubleshooting checklist.

### Pitfall: Cross-fork PR: `gh pr create` fails with opaque GraphQL error

When forking a repo into a personal account, `gh pr create --head you/repo:branch` fails with:

```
pull request create failed: GraphQL: Head sha can't be blank, Base sha can't be blank, Head user can't be blank, Head repository can't be blank, No commits between upstream:main and , Head ref must be a branch, not all refs are readable
```

**Don't waste time debugging the `--head` format.** Even the correct `username:branch` format may fail. Try the **GitHub API directly** first:

```bash
gh api repos/owner/upstream/pulls \
  -f title="fix(scope): description" \
  -f head="your-github-username:branch-name" \
  -f base="main" \
  -f body="## Summary\n\nPR description here"
```

This usually works, but **both approaches can fail** with 404 or permissions errors when:
- The **target organization has third-party access restrictions** or SAML SSO. The token must be authorized for the org via `gh auth refresh --sso`.
- The fork is very new and GitHub's systems haven't fully indexed it yet
- The token's OAuth scopes don't include `public_repo` — verify with `gh auth status`

### Cross-fork PR: When Both `gh pr create` and the API Fail (Org Restrictions)

If both `gh pr create` and the REST API return 404 despite the compare endpoint confirming the branches are connected, the fallback is the **GitHub compare URL**:

```bash
# Print the URL — open in browser to create the PR manually
echo "https://github.com/upstream-org/upstream-repo/compare/develop...your-github-username:branch-name"

# On macOS, open it directly:
open "https://github.com/upstream-org/upstream-repo/compare/develop...your-github-username:branch-name"
```

The compare URL pre-fills the diff and lets you write/edit the body. Requires human click-through — it's a hand-off point rather than fully automated, but it works when the API doesn't.

**Prerequisites:**
- Fork must exist (created via `gh repo fork` or the web UI)
- Fork's default branch must be synced with upstream:
  ```bash
  git fetch upstream main
  git push origin upstream/main:main
  ```
- Branch must have been pushed to the fork

**Head format:** The `head` field takes `owner:branch` — the GitHub username (or org name), not the repo name. For a fork at `you/hermes-agent-1` with branch `fix/foo`, use `head="you:fix/foo"`.

#### Troubleshooting checklist when both approaches fail:
1. Verify the fork exists and branch is pushed: `gh api repos/you/fork/branches/your-branch --jq '.name'`
2. **Verify the target repo's default branch name** — it may not be `main`: `gh repo view owner/upstream --json defaultBranchRef --jq '.defaultBranchRef.name'`
3. Verify the compare API works: `gh api repos/owner/upstream/compare/develop...you:branch --jq '.status'` — should return `ahead`, `behind`, or `identical`
4. Check token authorization for the org: `gh auth refresh --sso` (if the org requires SAML)
5. Check token has `public_repo` scope: `gh auth status`
6. A **404 on PR creation with a valid compare check** usually means an **org-level access restriction** — use the compare URL as the fallback

See `references/cross-fork-pr-workaround.md` for the full debugging session transcript and the org-restriction case study added in v1.4.0.

---

### Post-merge scope creep — extra commits on a merged branch

A variant that catches agents off guard: **the PR was merged, but the branch still exists locally with additional commits that were never on main.** Those commits are not in the repo's history — they only exist on your local branch.

When the PR is already merged, do NOT push the remaining commits to the old branch or try to re-open the PR. The correct workflow:

```bash
# 1. Switch to main, pull the latest (which includes the merged PR)
git checkout main && git pull origin main

# 2. Create a fresh branch from the current main
git checkout -b fix/separate-issue

# 3. Apply the change (cherry-pick from the old branch, or re-apply manually)
git cherry-pick <commit-sha-from-old-branch>

# 4. File a NEW issue, commit, push, open a NEW PR
gh issue create --title "Separate issue" --body "..."
git commit -s -m "fix: description of separate issue"
git push -u origin HEAD
gh pr create --title "fix: description" --body "Closes #ISSUE"
```

**Why the old branch is dangerous:** If you push more commits to a branch whose PR was already merged, those commits orphan — they're on the branch but not on main. No CI will run against them, no review will happen, and the only way they reach main is through a new PR from a main-based branch.

### Scope creep on an open PR — pushing a separate issue to the same branch

A distinct variant that applies *before* merge: **a PR is already open, you discover a separate issue that needs fixing, and you push it to the same branch.**

This is wrong for three reasons:

1. **The PR was opened for a specific issue.** If the original PR merges and the branch is closed, the second fix disappears with it — it was never on main.
2. **If the PR hasn't merged yet**, the reviewer sees unrelated changes mixed into the same diff. They can't approve one and reject the other.
3. **You lose the audit trail.** The second fix has no issue of its own, no separate review, and no independent merge record.

**The correct response when you discover a separate issue while a PR is open:**

```bash
# 1. Leave the open PR alone. Do NOT push to that branch.
# 2. Create a fresh branch from the current main:
git checkout main && git pull
git checkout -b fix/second-issue-description
# 3. Apply the fix (cherry-pick if you already committed on the wrong branch,
#    or re-apply manually)
# 4. File a NEW issue, commit, push, open a NEW PR
gh issue create --title "Second issue" --body "..."
git commit -s -m "fix: description of second issue"
git push -u origin HEAD
gh pr create --title "fix: description" --body "Closes #NEW_ISSUE"
```

**The "but it's just a small fix" trap:** This is the same rationalization that produces one-line direct-to-main pushes. A fix's size doesn't determine whether it needs its own issue and PR — its *logical independence* from the open PR does. If it addresses a different problem, it gets its own lifecycle.

**Exception:** Fixup commits for *review feedback* on the open PR are fine — those are part of the same logical change. The boundary is: "does this change make sense to a reviewer without knowing about the open PR's issue?" If yes, it's a separate change and needs its own PR.

### The "I have write access" trap — accidental main commit recovery

You branched, you worked, you committed — but you were on `main`, not the feature branch. The commit is now on main and pushed. This is not a crisis, but the fix requires care:

```bash
# 1. Create a branch at the commit so the work isn't lost
git branch feat/my-feature HEAD

# 2. Revert the commit on main (creates a new commit, does NOT rewrite history)
git revert --no-edit HEAD
git push origin main

# 3. Cherry-pick onto a fresh branch from current main
git checkout -b feat/my-feature main
git cherry-pick <original-commit-sha>
git push -u origin HEAD

# 4. Open PR from the branch
gh pr create --title "..." --body "..."
```

**Why not just force-push to reset main?** Because main is shared history. If anyone else has pulled (CI, another agent session, a collaborator), force-pushing creates divergence. Revert is safe — it creates a new commit that undoes the change, which merges cleanly with anyone else's history.

**Why not just leave the commit on main and open the PR from a branch?** Because the commit already on main means "no commits between `main` and `branch`" error. The PR system sees the feature branch as behind main, not ahead. The cherry-pick onto a main-based branch creates a clean diff.

**One gotcha:** After reverting and cherry-picking, the git history looks like:

```
A — B (feature commit) — C (revert)    ← main
      \
       D (cherry-pick of B)             ← feat/my-feature
```

The `gh pr create` may fail with "no commits between main and feat/my-feature" if the cherry-pick SHA matches the original commit SHA. In practice, cherry-pick creates a new SHA, so this usually works. If it doesn't, `git commit --amend --no-edit` on the branch creates a new SHA and unblocks the PR.

### The "I have write access" trap — release edition

The same trap applies at release time. After a feature PR merges, the natural next steps are:

```bash
git checkout main && git pull
git tag vX.Y.Z && git push origin vX.Y.Z
```

But that's not the complete release cycle. Two things are easy to forget:

1. **GitHub Releases are not automatic.** The tag triggers PyPI publish via the release workflow, but GitHub Releases are separate — they need `gh release create`. Without this, the Releases page shows tags without release notes, and users browsing GitHub don't see the changelog.
2. **Release backlog.** If a previous release was shipped without a proper GitHub Release (common during agent-assisted build phases), backfill it. The Releases page should show every release that exists on PyPI. Use `gh release create vX.Y.Z --title "..." --notes "..."` to fill in gaps.

**Full release checklist for maintainers:**

```bash
# 1. After PR merges, update local main
git checkout main && git pull

# 2. Create the release commit (version bump + CHANGELOG)
# This should have been done in the PR — verify before tagging

# 3. Verify version matches what you intend to release
PACKAGE_VERSION="$(grep -Po '^version = \"\K[^\"]+' pyproject.toml)"
echo "Releasing: v$PACKAGE_VERSION"

# 4. Tag and push
git tag v$PACKAGE_VERSION && git push origin v$PACKAGE_VERSION
# Release workflow runs tests, builds, publishes to PyPI

# 5. Verify PyPI publish succeeded
# Check: https://pypi.org/project/<project>/

# 6. Create GitHub Release with release notes
gh release create v$PACKAGE_VERSION --title "v$PACKAGE_VERSION — Title" --notes "Changelog summary..."

# 7. Update project metadata files (AGENTS.md, any version references in docs)
# that were touched by the release changes
```

**If the release workflow fails after tagging:**

1. Fix the issue in a PR (not directly on main)
2. Merge the fix PR  
3. **Do not re-push the same tag** — GitHub won't re-trigger the workflow. Instead:
   - Delete the tag: `git tag -d vX.Y.Z && git push --delete origin vX.Y.Z`
   - Recreate it on the new merge commit: `git tag vX.Y.Z && git push origin vX.Y.Z`
   - Or bump the version and create a new tag (`vX.Y.Z+1`)

### Issue Debt — File First, Even When Direction is Clear

When a conversation with the maintainer converges on a feature direction, the natural next step is to file an issue before implementing. This applies even when:

- The maintainer said "go" or "let's do it"
- The scope seems clear and well-understood
- The change is small (under 50 lines)

The issue is the durable record. Conversation context is lost across sessions, but an issue persists. Filing one ensures:

- A future session can find the decision rationale
- The maintainer can review and correct the approach before code is written
- The conversation-to-code handoff is explicit rather than implicit

The pattern: **discuss → issue → implement → PR**. Never skip from "discuss" to "implement" without the issue in between.

### The "installed code" trap — debug → issue → PR, not patch

When debugging installed code you have write access to (your own project or a repo you maintain), there's a strong temptation to skip from "found the root cause" directly to "patching the file." This is a distinct variant of the Issue Debt trap — the fix isn't speculative, you fully understand it — but the process still applies:

**Even when you know the exact fix, even when it's five lines, even when you traced root cause yourself — file the issue first, then PR the fix.**

This has been corrected multiple times across different projects (direct patching of installed plugin code, modifying upstream library files in site-packages, applying fixes without PR review). The pattern is always the same:

1. Debug the issue, find root cause ✅
2. Understand the exact fix needed ✅
3. ~~Apply the patch directly to installed code~~ ❌
4. File an issue documenting root cause and proposed fix ✅
5. Branch, implement, submit PR ✅

Step 3 is the trap. It feels efficient because you already know the answer. But it bypasses:
- **The durable record** — conversation context about the bug is lost across sessions; the issue persists
- **Review** — even obvious fixes can have edge cases or alternative approaches
- **CI validation** — the fix lands without tests running
- **Process integrity** — every skipped step erodes the convention for future contributions

The fix for the installed patch: revert it (git checkout or restore the original), file the issue, then proceed with a proper branch + PR.

**Exception:** CI hotfixes where the pipeline is actively broken (same as the "Don't Skip the PR" table). Even then, file a follow-up issue documenting the root cause.

### Pitfall: The "debugging discovery" shortcut

When you're deep in an active debugging or dogfooding session and you discover a root cause that needs a fix, there is a strong gravitational pull to apply the fix immediately — patch the file, rebuild the container, re-test, all within the same session without filing an issue. **This is the same trap as the installed-code trap, with a different rationalization.**

The rationalization sounds like: "I'm already debugging. I found the problem. Applying the fix now is part of the same flow. Filing an issue would break momentum."

This is wrong for three reasons:

1. **The fix is a separate action from the diagnosis.** Finding the root cause is debugging. Applying the fix is a code change. These are different activities governed by different processes. The debugging flow should produce an issue documenting the root cause, not a commit.

2. **The container doesn't make it any less of a code change.** If you patched the file in a Docker service source, rebuilt the image, and restarted the container — you made a production code change without an issue. The fact that it was "just testing" or "part of debugging" doesn't exempt the file from the issue requirement.

3. **The session ends and the context is lost.** The issue is the permanent record. The conversation thread about "I fixed X while debugging Y" vanishes when the session wraps. Without an issue, the next session finds the fix in the code with zero context about why it was done or what alternatives were considered.

**The fix if you already did this:** Revert the code, rebuild the container to restore original behavior, file the issue, then proceed with a branch + PR. The momentary cost of reverting is less than the long-term cost of a process exception that erodes conventions.

**This was corrected in a real session:** During a GroktoCrawl debugging session, a fix to the `llm-svc` fixture was applied and the container rebuilt — all without an issue. The user asked "are you making code changes without an issue filed?" The container was reverted, the issue was filed, and the fix proceeded through the proper lifecycle.