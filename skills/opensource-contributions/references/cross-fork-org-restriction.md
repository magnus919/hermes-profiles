# Cross-Fork PR Failure Due to Org Restriction — Case Study

## Context

2026-05-18: Contributing to `shlinkio/shlink` (PHP URL shortener) from fork `user/shlink`.

All the usual approaches failed:

| Approach | Error |
|----------|-------|
| `gh pr create --head user:feature-branch` | `GraphQL: user does not have the correct permissions to execute CreatePullRequest` |
| `gh api repos/shlinkio/shlink/pulls -f head="user:feature-branch"` | `404 Not Found` |
| `curl -X POST ...` (raw HTTP) | `404 Not Found` |

## What DID Work

The **GitHub compare URL** always works and pre-fills the diff:

```
https://github.com/shlinkio/shlink/compare/develop...user:feature-branch
```

This requires a human to click "Create Pull Request" — not fully automatable, but the only reliable fallback.

## Diagnostic Steps

These confirmed the setup was correct — the problem was on GitHub's side, not ours:

```bash
# 1. Confirm fork exists and is recognized
gh api repos/user/shlink --jq '{.parent.full_name, .fork}'  → shlinkio/shlink, true

# 2. Confirm branch exists on fork
gh api repos/user/shlink/branches/feat/agents-md --jq '.name'  → feat/agents-md

# 3. Confirm upstream can see the branch via compare API (the key check)
gh api repos/shlinkio/shlink/compare/develop...user:feature-branch --jq '.status'  → ahead

# 4. Confirm PR creation within the same fork works (isolates the issue to cross-fork)
gh api repos/user/shlink/pulls -f title="Test" -f head="feat/agents-md" -f base="develop"  → 201 Created

# 5. Check token scopes
gh auth status  → ✓ Logged in, repo scope present

# 6. List PRs on upstream repo (read access confirmed)
gh api repos/shlinkio/shlink/pulls --jq '.[].number'  → returns PR numbers
```

Steps 3-5 all passed, which means the issue was an **org-level restriction on the shlinkio organization** — likely third-party access restrictions preventing the OAuth token from creating PRs via the API, even though the compare endpoint could see the branch.

## Root Cause Hypothesis

The `shlinkio` organization likely has one of:
- **Third-party application access restrictions** (the OAuth token's app is not authorized for the org)
- **SAML SSO enforcement** that requires `gh auth refresh --sso`
- **"Allow outside collaborators to submit pull requests" disabled** at the org level

Since the compare endpoint works (`status: ahead`) but PR creation returns 404, the token has read access but not the write access needed to create cross-fork PRs to repos in restricted orgs.

## Takeaways

For future cross-fork PR contributions to org repos:

1. Try `gh pr create` and `gh api` first — they'll work for most orgs
2. If both fail with 404 despite `gh api repos/org/repo/compare/develop...you:branch` returning `ahead`:
   - Try `gh auth refresh --sso` to authorize the token for the org
   - If that doesn't help, hand off via the compare URL
3. The compare URL is the **universal fallback** that works regardless of org restrictions
