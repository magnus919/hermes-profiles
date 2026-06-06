# Trigger Patterns — Contribution Pipeline

The skill accepts input through four patterns. Each maps to the same 5-phase pipeline but has different pre-processing.

---

## Pattern A: Issue-Driven (Primary)

**Input:** GitHub or ForgeJo issue URL or `owner/repo#number` shorthand.

**Example inputs:**
```
https://github.com/NousResearch/hermes-agent/issues/372
git.brandyapple.com/magnus/agent-skills#15
org/repo#42
```

**Pre-processing:**
1. Parse URL → extract owner, repo, issue number
2. Fetch issue via `gh issue view` or `forgejo-cli issue view`
3. Validate: issue is open, not a discussion, not assigned to someone else, no open PR already handles it
4. Check project's AI contribution policy (AGENTS.md, AI_POLICY.md, or CONTRIBUTING.md AI clause)
5. Enter P0

**If issue has no reproduction steps:** file a comment asking the reporter for details. Do not proceed.

**If issue IS a discussion/RFC:** classify as "design discussion." Do not proceed with implementation.

---

## Pattern B: Discovery-Driven

**Input:** Repo URL + issue description in natural language. No pre-existing issue.

**Example inputs:**
```
Found a bug in org/repo: X crashes when Y is null. Steps to reproduce: ...
org/repo needs a feature: rate limiting on the /api/v2 endpoint
```

**Pre-processing:**
1. Verify the repo exists and is accessible
2. Check if the project requires an issue before a PR (most do)
3. If required → file a well-formed issue first (use project's issue template), wait for triage
4. If not required → treat the natural-language input as the issue, proceed to P0
5. If uncertain → file an issue. Better to have a paper trail.

---

## Pattern C: Kanban-Driven

**Input:** Kanban card with structured metadata. Triggered by dispatcher or cron.

**Card metadata fields:**
- `issue_url` (required)
- `repo` (required) — `owner/name`
- `branch_prefix` (optional) — override branch naming convention
- `skip_orientation` (optional) — use cached fingerprint if fresh
- `work_strict` (optional) — enforce test-first fork even for negative invariants

**Pre-processing:**
1. Validate all required fields are present and parseable
2. Issue URL must be resolvable
3. WIP limit check per project
4. Enter P0 (or skip to P1 if `skip_orientation` is set AND cache is fresh)

---

## Pattern D: Cohort-Driven (Batch)

**Input:** Multiple issue URLs sharing a root cause.

**Example:**
```
These three issues are all caused by the same race condition:
- org/repo#101
- org/repo#142
- org/repo#198
```

**Pre-processing:**
1. Validate all issues, classify root cause overlap
2. Check if an omnibus PR is appropriate (see hermes-contrib skill, "Consolidation Strategy")
3. File a coordination issue on the project: "These N issues share root cause X. I propose a single PR that addresses the architectural gap. Is this useful?"
4. Wait for maintainer response before implementing
5. If approved → single P0-P4 pipeline addressing all issues in one PR

---

## Pre-Flight Validation (All Patterns)

Before ANY phase begins, validate:

1. **Issue exists and is open** — not closed, not locked, not a pull request
2. **No open PR already handles this issue** — check open AND merged PRs
3. **WIP limit not exceeded** — one PR per project in flight. Exception: changes under 10 lines
4. **AI policy allows contributions** — check AGENTS.md, AI_POLICY.md, CONTRIBUTING.md
5. **Repo is accessible** — can clone, has a default branch, has a build system we can use
6. **Issue is scoped** — if the issue is a saga (touches 5+ modules), flag for decomposition
7. **PR merge status (follow-up work only)** — if this is a follow-up to a PR from the same session, verify that PR's merge status via `gh pr view <number> --json state,mergedAt`. If MERGED, branch fresh from main. If OPEN, push to the same branch and update the PR body. If CLOSED without merge, escalate to the user.
