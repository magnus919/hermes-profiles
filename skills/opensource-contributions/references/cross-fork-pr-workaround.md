# Cross-Fork PR Workaround — Session Detail

## Background

On Contributing to `NousResearch/hermes-agent` from fork `user/repo` (note: fork name differs from upstream). `gh pr create` repeatedly failed with an opaque GraphQL error despite correct parameters.

## Error

```
pull request create failed: GraphQL: Head sha can't be blank, Base sha can't be blank, 
Head user can't be blank, Head repository can't be blank, No commits between 
NousResearch:main and , Head ref must be a branch, not all refs are readable
```

## Attempted Fixes That Did NOT Work

1. **Correcting `--head` format from `user/repo:branch` to `user:branch`**
   - `--head user/repo:fix/foo` → `--head user:fix/foo`
   - Result: same error

2. **Syncing fork's `main` with upstream**
   ```bash
   git fetch upstream main
   git push origin upstream/main:main
   ```
   - Result: `origin/main` now matched upstream, but `gh pr create` still failed

3. **Using `gh pr create` from within the fork checkout**
   - Without `--repo` flag (let gh infer from cwd)
   - With `--repo NousResearch/hermes-agent` (explicit)
   - Result: same error both ways

## Fix That Worked

Use the **GitHub REST API directly**, bypassing `gh`'s fork-resolution heuristics entirely:

```bash
gh api repos/NousResearch/hermes-agent/pulls \
  -f title='fix(agent): description' \
  -f head='user:fix/tool-call-regex-nested-json' \
  -f base='main' \
  -f body='## Summary\n\nPR body here'
```

Key points:
- `-f head='username:branch'` — username only, not the repo name
- No `-f head='username/repo:branch'` — that causes 422 "head is invalid"
- The API always returns 201 Created for valid cross-fork PRs
- Response includes full PR object with `html_url`, `number`, etc.

## Root Cause Hypothesis

`gh pr create` uses a GraphQL mutation that resolves the head ref through the fork's repository connection. When the fork name differs from the upstream (e.g. `hermes-agent-1` vs `hermes-agent`), `gh`'s fork-resolution heuristics fail silently. The REST API endpoint (`POST /repos/:owner/:repo/pulls`) accepts a simpler `head` string that doesn't require the same repo-name resolution.

## Update: This Is Not the Only Failure Mode

On 2026-05-18, contributing to `shlinkio/shlink`, the REST API also failed with 404 despite the compare endpoint confirming `status: ahead` — see `cross-fork-org-restriction.md` for this separate failure mode caused by org-level access restrictions. In that case, the GitHub compare URL is the only reliable fallback.
