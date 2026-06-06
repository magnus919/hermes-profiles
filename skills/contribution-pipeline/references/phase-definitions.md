# Phase Definitions — Contribution Pipeline

Each phase produces concrete, verifiable artifacts. Each gate has a falsifiable criterion.
Failure at any gate: report what's known, do not proceed with incomplete understanding.

---

## P0: Muster & Orientation

**Purpose:** Determine whether this issue is actionable and what the project's actual conventions are.

**Artifacts produced:**
1. Issue validity assessment (open? bug? has reproduction? not a discussion?)
2. AI policy check (AGENTS.md, AI_POLICY.md, CONTRIBUTING.md AI clause)
3. SECURITY.md check (disclosure contact, policy)
4. Project fingerprint (8-field conventions card — see `references/project-fingerprint-template.md`)
5. 3-5 recently merged PRs studied (different contributors, different types)

**Gate:** Can you describe what maintainers ACTUALLY enforce, with evidence from merged PRs?
- Falsified by: failing to catch a convention that merged PRs demonstrate (e.g., claiming "no commit format convention" when 100% of merged PRs use Conventional Commits)

**Cache behavior:**
- Fingerprint cached per-project with HEAD commit hash
- On next contribution to same project: check cached HEAD against current HEAD
- Match → skip P0. Mismatch → full P0 regeneration.
- TTL: 1 hour minimum refresh

**Fallback paths:**
- Issue is a discussion, not a bug → classify, stop, report
- Project bans AI contributions → stop, report
- Project has no CONTRIBUTING.md → default posture (see opensource-contributions skill)
- Project is a monorepo (fingerprint >30K tokens) → layered strategy, on-demand deep-dives

**Time budget:** 5 minutes. If stuck, report what's known and escalate.

---

## P1: Comprehension & Reproduction

**Purpose:** Understand the issue deeply enough to state definitively what must change and why.

**Artifacts produced:**
1. Bug classification (Bug / Feature / Design Question / Configuration / Support)
2. Reproduction script (Dockerfile or shell script that demonstrates the bug on a clean checkout)
3. Root-cause statement ("error at line 147 because X is null when Y is non-null")
4. Code path trace (entry point → intermediate calls → bug site)
5. Baseline test pass/fail counts (existing test suite run before any modification)
6. Platform awareness check (does the issue specify OS/arch/locale the agent doesn't have?)

**Gate:** Does the reproduction script produce a FAIL on the target branch (unmodified)?
- Falsified by: reproduction script passes on clean checkout, or doesn't run at all

**Non-deterministic bug handling:**
- If bug is timing/race/async → loop reproduction 50-100 times, document failure rate
- If bug cannot be reproduced after 2 honest attempts → stop, file "could not reproduce" comment

**Time budget:** 15 minutes. If Docker build keeps failing, report with partial findings.

---

## P2: Design & Implementation

**Purpose:** Design the fix (scaled to complexity), implement it, and verify it works.

**Artifacts produced:**
1. Spec (scaled — see `references/gate-criteria.md` for tiers)
2. Working branch with fix applied
3. Tests (fail before fix, pass after — verified mechanically)
4. Code comments (Why, not What)
5. Commit messages (Conventional Commit format, body explains Why)
6. CHANGELOG entry (if user-facing change)
7. README update (if new dependency, CLI flag, env var, API, or platform support)

**Spec Tiers:**
| Tier | Trigger | Format | Gate Review? |
|---|---|---|---|
| Light | Typo, trivial, comment-only, refactor | One-paragraph spec in issue body | No — test-first IS verification |
| Medium | New function, API addition, config change | SPEC.md (scope + acceptance criteria + edge cases) | Self-review |
| Full | Deadlock, race, auth, crypto, public API | Full SDD spec + Gherkin for stateful | Independent agent review |

**Test quality checks (see contribution-test-quality sub-skill):**
- "Fails on main": test runs on unmodified branch first. Must fail.
- Assertion Relevance Scan: no private access, no internal mocks, no mock call-counts
- Intent-annotated coverage: each test file declares what IS and IS NOT covered
- 8-point test quality scorecard: minimum 6/8 to pass

**Gate:** `git stash && cleanroom test run` produces green suite + test quality scorecard ≥6/8
- Falsified by: tests passing on unmodified code (tautology), scorecard <6, linter violations

**Time budget:** 30 minutes. At 15 minutes, if core logic isn't working: ship a design-doc version and escalate.

---

## P3: Clean-Room Verification

**Purpose:** Prove the fix works in an environment that mirrors the project's CI, not just the agent's local state.

**See:** `contribution-clean-room` sub-skill for the full decision tree, environment classifier, and CI fingerprinting.

**Artifacts produced:**
1. Environment classification (Docker / VM / Nix / CI-runner)
2. Verification report (test suite pass/fail, linter clean, build success)
3. CI divergence surface (MATCH / PARTIAL / MISMATCH / UNKNOWN per dimension)
4. Baseline comparison (P3 results vs P1 baseline — no new failures introduced)

**Gate:** All checks pass cleanly in isolation. No pre-existing failures attributed to the fix.
- Falsified by: any test failure, linter error, or build failure in the isolated environment

**Failure → roll back to P1, not P2.** If the fix doesn't work in isolation, the agent didn't understand the problem. Re-implementing the same understanding is wasted work.

**Time budget:** 10 minutes. If environment setup takes longer, report what was verified and what wasn't.

---

## P3.5: Security Gate

**Purpose:** Catch vulnerabilities, secrets, and dangerous patterns before they reach a public PR.

**See:** `contribution-security` sub-skill for the full checklist, semgrep config, and disclosure routing.

**Artifacts produced:**
1. semgrep static analysis report
2. Secrets scan report (trufflehog/gitleaks)
3. Dependency check (new deps only — typosquatting, age, source)
4. Classification of findings

**Gate:** Zero critical/high findings. Zero secrets detected.
- CRITICAL/HIGH → block PR creation, route to SECURITY.md disclosure
- MEDIUM/LOW → log, create PR with security-review label
- SECRETS → block, do not create public PR under any circumstances

---

## P4: PR Creation

**Purpose:** Package the contribution for maintainer review — make their job easy.

**Artifacts produced:**
1. Filled PR template (exact headers, exact checkboxes — matched to project's template)
2. Conventional Commit message(s) with body explaining Why
3. Mermaid diagram (if complexity warrants — see contribution-documentation sub-skill)
4. Honest SLA disclosure ("I don't run continuously — responses within 24-48h")
5. CI monitoring plan (check status, respond to failures)

**Gate:** PR is open, template is filled, CI passes on the branch, SLA is disclosed.
- Do NOT mark as "ready for review" with red CI.

**Time budget:** 5 minutes.

---

## Post-PR: Passive Responsibility

**Purpose:** Shepherd the PR to merge without requiring the user to remember to check.

**Ongoing:**
- Monitor CI status after creation
- Respond to review comments within next available session window
- 14-day staleness → polite nudge comment (from the agent, disclosed)
- 30-day staleness → notify user to reassess the PR
- Rebase when merge conflicts arise (with care — don't force-push after review)

**Skill-level Done: PR is MERGED** (or definitively closed with maintainer explanation).

---

## Phase Dependencies

```
P0 ──→ P1 ──→ P2 ──→ P3 ──→ P3.5 ──→ P4
       ↑                ↑
       └── P3 failure rolls back to P1 (not P2)
```

Each phase consumes the artifacts of the previous phase. If a phase fails:
1. Report what's known
2. Identify the specific gate criterion that failed
3. Determine whether to retry the phase, roll back to a previous phase, or stop

---

## Trivial Fix Fast Path

Changes under 10 lines that are unambiguously correct (typo fix, comment correction, obvious off-by-one with existing test coverage):
1. Skip P3 (clean-room verification) — local test run suffices
2. Skip Mermaid diagram
3. Short-form PR body (3 lines max)
4. Still run P3.5 security gate (secrets scan at minimum)
5. Bypass WIP limit (doesn't count toward per-project cap)
