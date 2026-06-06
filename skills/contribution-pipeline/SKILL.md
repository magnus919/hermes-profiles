---
name: contribution-pipeline
description: Full issue-to-PR lifecycle with 5-phase gated pipeline. Produces contributions maintainers look forward to — project-aware, thoroughly tested, security-gated, well-documented. Skill bundle with sub-skills for security, test quality, documentation, clean-room verification, and vault integration.
version: 1.0.0
tags: [contribution, pipeline, opensource, PR, quality, security]
related_skills:
  - opensource-contributions
  - hermes-contrib
  - github-pr-workflow
  - github-issues
triggers:
  - "work on issue"
  - "contribute to"
  - "file a PR for"
  - "fix this issue"
  - "open a PR"
  - "contribution pipeline"
  - issue URL (github.com or git.brandyapple.com)
  - "/contribute"
---

# Contribution Pipeline

Full lifecycle from assigned issue to merged PR. Five phases with concrete, falsifiable gates — no LLM-judged rubber stamps. Every phase produces an artifact that the next phase consumes. Every gate has a criterion that can fail.

**This is a skill bundle.** The orchestrator routes to sub-skills for specialized domains:

| Sub-Skill | Domain | When Loaded |
|---|---|---|
| `contribution-security` | Static analysis, secrets scanning, disclosure policies | P3.5 Security Gate |
| `contribution-test-quality` | Test design, change-detector prevention, scorecard | P2 Test Quality Gate |
| `contribution-documentation` | Code comments, commits, CHANGELOG, README, Mermaid | P2 Documentation + P4 PR Body |
| `contribution-clean-room` | Docker/VM verification, CI fingerprinting, environment classification | P3 Clean-Room Verification |
| `contribution-vault-integration` | Project fingerprint caching, knowledge graph persistence | P0 Caching + Cross-session |

---

## Trigger Patterns

The skill accepts input through four patterns:

| Pattern | Input | Example |
|---|---|---|
| **Issue-driven** (primary) | Issue URL or `owner/repo#number` | `https://github.com/org/repo/issues/42` |
| **Discovery-driven** | Repo URL + issue description | "Found a bug in org/repo: X crashes when Y is null" |
| **Kanban-driven** | Kanban card with `issue_url` + `repo` metadata | Card body parsed from structured fields |
| **Cohort-driven** | Multiple issue URLs sharing root cause | Consolidation detected → omnibus PR pattern |

**Pre-flight checks before any phase begins:**
- Issue exists and is open (not closed, not a discussion/RFC)
- No open PR already handles this issue
- No WIP PR in flight for this project (WIP limit: 1 per project, except <10-line fixes)
- Project's AI contribution policy allows agent-assisted contributions (check AGENTS.md, AI_POLICY.md)
- **If this is a follow-up to an existing PR, verify that PR's merge status first.** A PR with `state: MERGED` means branch fresh from main — do NOT push follow-up commits to a merged branch. A PR with `state: OPEN` means push to the same branch and update the PR body. Check via `gh pr view <number> --json state,mergedAt`.

---

## Quick Reference

| Phase | What It Produces | Gate (Falsifiable) | Time Budget |
|---|---|---|---|
| **P0: Muster & Orientation** | Project fingerprint (cached) | Can you describe what maintainers ACTUALLY enforce? | 5 min |
| **P1: Comprehension** | Reproduction trace + root-cause + baseline | Does repro script produce FAIL on target branch? | 15 min |
| **P2: Design & Implementation** | Working branch (tests fail before fix, pass after) | `git stash && cleanroom test run` green + test quality scorecard ≥6/8 | 30 min |
| **P3: Clean-Room Verification** | Verification report + CI divergence surface | All checks pass in isolation | 10 min |
| **P3.5: Security Gate** | Static analysis + secrets scan report | Zero critical/high findings. Zero secrets. | Auto |
| **P4: PR Creation** | Filled template + Conventional Commit + Mermaid | PR open, CI green, SLA disclosed | 5 min |
| **Post-PR** | CI monitoring + staleness handling | PR merged (skill-level Done) | Passive |

**Skill-level Done: PR is MERGED** — not just created. Post-PR is a passive responsibility tracked across sessions.

---

## Phase Definitions

See `references/phase-definitions.md` for the complete specification of each phase: required artifacts, gate criteria, rollback rules, and fallback paths.

See `references/gate-criteria.md` for the concrete, falsifiable criteria at every phase transition.

See `references/trigger-patterns.md` for the four input patterns with parsing, validation, and branching logic.

See `references/project-fingerprint-template.md` for the 8-field conventions card produced by P0.

See `references/remote-docker-verification.md` for the sync-build-recreate-test sequence when the build target is a remote Docker host (P3 clean-room verification).

See `references/patch-recovery.md` for recovery procedures when the `patch` tool corrupts a file (P2 implementation).

---

## Cross-Cutting Rules

1. **Every gate is falsifiable.** "Do you understand?" is not a gate. "Does the reproduction script produce a FAIL on the target branch?" is a gate.

2. **Project fingerprint caching.** P0 output cached per-project with HEAD hash. Subsequent PRs to the same project skip P0. Staleness check: compare cached HEAD hash against current. TTL: 1 hour.

3. **WIP limit: one PR per project.** Maintainer attention is the bottleneck, not code generation throughput. Exception: changes under 10 lines bypass the limit.

4. **Clean-room failure → comprehension, not implementation.** If P3 fails, the agent didn't understand the problem. Roll back to P1, not P2.

5. **"No defect the agent could reasonably catch."** Not "zero defects." Design preferences and edge case interpretations legitimately require human review.

6. **Honest SLA disclosure.** At PR creation: "I don't run continuously — responses within 24-48h." No aspirational promises that can't be kept.

7. **PR verbosity scales to change size.** ~50 + (lines_changed × 0.5) words max, capped at 500. A one-liner gets a 3-line PR body.

8. **Documentation written alongside code.** Commit messages, code comments, and inline docs happen during P2 implementation — not in a separate post-hoc phase.

9. **Safe-to-fail exits at every phase.** If the agent hits a blocker, report what's known and escalate. Don't generate increasingly wrong work.

10. **Templates lie. Merged PRs tell truth.** P0 must study 3-5 recently merged PRs from different contributors — not just read CONTRIBUTING.md.

11. **Triage test infrastructure before P3.** Before attempting clean-room verification, check what's available: `docker compose ps` for running fixtures, `which pytest` for test runner, `pip list 2>/dev/null | grep pytest` for package availability. If the full integration suite can't run, run the subset that can and document the gap in the PR body. A documented partial verification is better than a skipped gate or a fabricated pass.

---

## Sub-Skill Loading

At the appropriate phase, load the sub-skill for specialized domain guidance.
**If the sub-skill is not installed, use the fallback — do not skip the gate.**

| Phase | Sub-Skill | What It Provides | Fallback When Missing |
|---|---|---|---|
| P2 test quality | `contribution-test-quality` | Test design, change-detector prevention, 8-point scorecard | Manual scorecard: check each of the 8 criteria from gate-criteria.md via AST scan and heuristics |
| P2 documentation | `contribution-documentation` | Code comments, commits, CHANGELOG, README conventions | Follow project's merged PRs for documentation patterns. Conventional Commits with DCO sign-off. |
| P3 clean-room | `contribution-clean-room` | Docker/VM verification, CI fingerprinting, environment classification | See `references/remote-docker-verification.md`. Sync code, build, recreate, run test suite. Report what was verified and what wasn't. |
| P3.5 security | `contribution-security` | semgrep config, secrets scan, dependency check | Run `git diff main -- <changed-files>` and grep for: secrets patterns (`password`, `secret`, `key`, `token`, `AKIA`, `-----BEGIN`), debug artifacts (`print`, `pdb`, `breakpoint`), local paths (`/Users`, `/home/`, hostnames). If no new deps, skip dep check. |
| P0/P4 persistence | `contribution-vault-integration` | Project fingerprint caching, knowledge graph persistence | Skip — fingerprint freshness is checked by P0 staleness check. No vault write required. |

---

## Pitfalls

- **Don't skip P0 even on familiar projects.** The cached fingerprint may be stale. Run the staleness check before proceeding.
- **Don't create a PR until CI-equivalent verification passes.** "Ready for review" with red CI is the fastest way to lose maintainer trust.
- **Don't let the reproduction script pass before the fix.** If the test passes on the unmodified branch, the test is tautological — go back to P1.
- **Don't fill PR templates with N/A sections just to satisfy the gate.** If the change is trivial, use short-form and apologize in a comment.
- **Don't proceed past P1 if you can't reproduce.** File a "could not reproduce, here's what I tried" comment and stop.
- **Don't add Mermaid diagrams to one-line fixes.** The complexity threshold is 4+ sequential steps with branching.
- **Don't run builds outside disposable containers.** See contribution-security sub-skill for isolation requirements.
- **Enrich pipeline results before caching, not after.** If P2 adds metadata to pre-existing pipeline outputs (quality scores, classification results, verification flags), call the enrichment function BEFORE `_set_cache()` or equivalent. Caching a result before enriching it means all subsequent cache hits return stale data without the new field. Pattern: `result = _enrich(result); _set_cache(url, result); return result` — not `_set_cache(url, result); return _enrich(result)`.
- **Triage test infrastructure before assuming tests will run.** At P3, check: is Docker running? Are fixture containers deployed? Is pytest installed in the target environment? If integration tests require containers that aren't available, fall back to unit tests, or run the subset of tests that work in the current environment and clearly report what was verified vs. skipped.
- **Recover from patch corruption by rewinding, not patching more.** If the `patch` tool corrupts a file (lint fails after patch, or the file structure is broken), do NOT try to patch the corrupted state — the match context is now unreliable. Instead: (1) restore the file from git (`git checkout <path>`), (2) re-read the current file content to get fresh line numbers and context, (3) re-apply the edit with more surrounding context. For files under 200 lines, it's faster to rewrite entirely. If the file is >500 lines and heavily modified, escalate.

---

## Cross-Reference

- **`opensource-contributions`** — OSS etiquette, phase references (0-4), default posture
- **`hermes-contrib`** — Hermes-Agent-specific conventions, PR templates, privacy rules
- **`github-pr-workflow`** — PR lifecycle, branch naming, conventional commits
- **`github-issues`** — Issue filing, labeling, agent disclosure
- **`github-code-review`** — Code review response patterns
