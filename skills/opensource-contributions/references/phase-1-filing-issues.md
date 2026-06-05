## Phase 1: Filing Issues

### Bug Reports

A good bug report answers: *what happened, what should have happened, and how do I make it happen?*

```markdown
<Clear, concise description of the bug>

1. <First step>
2. <Second step>
3. <See error>

<What should happen instead>

<What actually happens — include full error output>

- OS: <e.g., macOS 15.4, Ubuntu 24.04>
- Version/Build: <e.g., v2.1.3, commit abc1234>
- Relevant config: <if applicable>

- Screenshots, logs, or stack traces
- Minimal reproduction (preferred: a script or config that triggers it)
```

**Always include the minimal reproduction.** A bug report without reproduction steps is hard to act on.

### Feature Requests

Frame features around the **problem**, not your proposed solution:

```markdown
<What user need or pain point this addresses>

<Who needs this and when>

<How you think it could work — keep this section brief, the maintainers may have a better approach>

<Other ways to solve the problem — shows you've thought about it>

<Why this is worth the project's time>
```

### Agent Disclosure

When filing an issue on behalf of someone else (human delegating to an AI agent), ALWAYS disclose the agentic nature. Add a line to the issue body:

```
Filed by Jasper (AI agent on behalf of Magnus Hedemark)
```

This goes at the bottom, after the substantive content. It's not a courtesy — it's a transparency requirement. Maintainers deserve to know who they're talking to.

### Maintainer Workflow — Issue First, Code Second

When the maintainer gives you direction on a feature ("let's do it", "go"), the natural impulse is to start coding immediately. **Resist it.** Even when you're implementing something the maintainer explicitly asked for, the first step is still an issue:

1. **Write the issue** documenting the problem, proposed solution, and alternatives considered
2. **Wait for maintainer feedback** — they may have a different approach in mind
3. **Only then branch and implement**

The issue is the permanent record of the decision. Conversation threads are ephemeral; issues are durable. Future sessions can reference the issue to understand *why* a decision was made, not just *what* was implemented.

**Exception:** Trivial bugfixes (one-line typos, clear logic errors in already-merged code). File the issue and fix in one branch, referencing the issue in the commit.

#### Pitfall: Docker service code is not exempt

When the repo contains Docker-based microservices (like GroktoCrawl, or any project with a `docker-compose.yml`), **changes to the service source code require an issue first** — even when you have write access and even when the change is "just testing" a hypothesis.

The trap: you patch a file in `llm-svc/llm_svc/app.py` (or any service's source), rebuild the container with `docker compose build <service>`, restart it, and test. No issue was filed. The change feels local — it's in your own repo, you have write access, the container is running in dev. The same process rules apply:

1. File the issue documenting the problem and proposed fix
2. Branch from main
3. Implement
4. Commit, push, PR
5. Rebuild the container after merge

The container doesn't make the change any less of a code change. If the file is tracked in git and deployed via Docker, the full lifecycle applies.

**The fix if you already made the change without an issue:** revert the code and rebuild the container with the original code, file the issue, then proceed properly. Do not leave the patched container running — it creates a divergence between what's on disk (the issue's scope) and what's running.

This was corrected in a real session: patching the llm-svc fixture to test a recovery pipeline improvement, without an issue filed first, prompted "are you making code changes without an issue filed?" The container was reverted and the issue was filed before proceeding.

### Filing Coordinated Multi-Issue Feature Roadmaps

When a feature spans multiple independent work items — especially across service boundaries or involving different architectural layers — filing a single monolithic issue is wrong, but filing isolated issues without cross-references is almost as bad. The pattern: **one issue per logical change, linked by dependency metadata.**

#### When to use this pattern

- The feature requires changes in multiple services (e.g., API model + fetch pipeline + CLI)
- The work has a clear dependency chain (issue B can't start until issue A merges)
- Different aspects could be worked on in parallel (separate tracks, same feature)
- The total scope is large enough that a single issue would be unwieldy

#### Issue body dependency references

Each issue's body should include a `## Dependencies` section that explicitly names what it needs:

```markdown

- **Requires:** #23 (response model changes) — this issue adds content-type
  detection that feeds into the new `download` fields created in #23.
- **Independent of:** #25 (CLI download command) — separate scope, different code paths.
```

GitHub auto-links `#N` references, so clicking the number jumps to the dependency. This creates a navigable graph from any issue.

#### Filing order strategy

| Dependency type | How to file | Example |
|----------------|-------------|---------|
| **Foundation** (no deps) | File first, all at once | `#23` response model, `#24` stealth browser, `#25` CLI download |
| **Depends on foundation** | File immediately after, reference dependency | `#26` content-type detection → `Depends on #23` |
| **Depends on dependent** | File in same batch but note chain | `#28` LLM recovery → `Depends on #26` |
| **Escalation tier** | File alongside what it escalates from | `#29` FlareSolverr → `Depends on #24, #27` |

File foundation issues and their dependents in the same batch — the dependency metadata makes the ordering clear to whoever picks them up. The goal is to get the full roadmap onto the tracker, not to serialize filing to match implementation order.

#### Use cases for `Depends on` vs. `Blocked by` vs. `Related to`

| Term | Meaning | When to use |
|------|---------|-------------|
| **Requires / Depends on** | Cannot implement without this | The other issue's code changes are a hard prerequisite |
| **Blocked by** | External dependency outside the repo | Waiting on upstream release, API key, or maintainer decision |
| **Related to** | Shares context but no hard dependency | Alternative approach, adjacent feature, overlapping code area |
| **Independent of** | Explicitly not a dependency | Clarifies that these issues can proceed in any order |

#### What a coordinated roadmap looks like on the tracker

```
#23 Response model changes        ──founded──▶ #26 Content-type detection ──▶ #28 LLM recovery
                                                                    └──▶ #30 LLM Cloudflare classification
#24 Stealth browser config        ──founded──▶ #27 Cookie persistence  ──▶ #29 FlareSolverr
#25 CLI download subcommand       (independent, enhanced by #23)
```

Each issue body tells the same story in prose. The tracker renders `#N` as clickable links, so the full dependency graph is navigable from any single issue. A future contributor landing on #30 can follow the chain back to the foundations.

#### Pitfall: Don't file all issues as one "epic"

A single issue that describes seven work items is unfindable — someone searching for "CLI download" won't land on a feature-request titled "Response model changes." Keep each issue focused on one logical deliverable, and use the dependency metadata to connect them.

### Executing a Comprehensive Multi-PR Plan

After filing coordinated issues, the PR phase follows the same dependency chain. The pattern is linear: branch from main, implement, commit, push, PR for each issue in order, respecting cross-issue dependencies.

#### Dependency tiers at PR time

| Tier | What goes here | Strategy |
|------|----------------|----------|
| **Foundation** (no deps) | Model changes, config-only changes, new independent subcommands | Branch and submit all at once. These PRs have no blockers. |
| **Depends on foundation** | Logic that uses the new model fields, services that call the new endpoints | Branch from main *after* foundation PRs exist (commits are independent). Reference the dependency in the PR body. |
| **Escalation/meta** | Higher-level features that build on multiple lower tiers | These PRs can be written in parallel with dependents, but should be submitted last. |

#### Branch naming for coordinated work

Keep branch names consistent so the relationship is obvious:

| Dependency | Branch name | PR references |
|-----------|-------------|--------------|
| Foundation | `feat/binary-content-response-model` | `Closes #23` |
| Depends on #23 | `feat/content-type-detection` | `Closes #26 — Depends on #23` |
| Depends on #23, #26 | `feat/llm-recovery` | `Closes #28 — Depends on #23, #26` |

No need to encode dependency order in the branch name — just keep them single-purpose.

#### Tracking dependencies in PR bodies

In the PR body, use the same dependency metadata that appears in the issue:

```markdown

- **Depends on:** #23 (response model changes) — adds the `download` field this PR populates
- **Related:** #25 (CLI download) — separate code path, no conflict
```

GitHub doesn't auto-close or block PRs based on issue dependencies, but showing the chain in the PR body tells the reviewer the order they should merge in.

#### What to do when foundation PRs haven't merged yet

You branch from main, which doesn't have the foundation changes yet. Your code references new fields that don't exist on main. This is fine — the PRs are in the system, the diff shows what's being added, and the reviewer sees the full chain. Two strategies:

1. **Write independent code** — if your changes only touch files the foundation doesn't touch, there's no merge conflict when you rebase after the foundation merges.
2. **Assume the merge** — if your code directly uses the new fields, write it as if they already exist. The PR diff is clean and the merge order is clear.

Do NOT branch from a feature branch (branch stacking). Each PR should branch from main so they're reviewable independently.

#### Pitfall: Don't stop at issues — execute the full plan

When you've planned a comprehensive change involving multiple issues and PRs, it's tempting to stop after filing the issues. The issues are on the tracker, the plan is documented — feels like progress. **The plan isn't done until the PRs are open.**

This was corrected in a real session: after filing 8 issues across two gap areas, the user said "the plan didn't stop at issues" — the next step was implementing the PRs in dependency order, not declaring victory at the issue tracker.

The pattern: **issues → PRs → done**. Issues capture the decision; PRs deliver the implementation. Filing issues is the midpoint, not the finish line.

For a worked example of this full lifecycle (ideation → gaps → issues → 6 PRs), see `references/groktocrawl-gaps-worked-example.md`.
For the companion pattern — resolving merge conflicts when sequential PRs modify the same files — see `references/sequential-pr-conflict-resolution.md`.

### Maintainer Workflow — Don't Skip the PR

When you have **write access** to a repo (you're working on your own project or one where you're a maintainer), there's a strong temptation to skip the branch-PR-merge cycle and push directly to main. **Don't.** The same rules apply to maintainers as to contributors:

| Scenario | Branch + PR? | Exception |
|----------|-------------|-----------|
| New feature (any size) | **Yes** — always | None. Features need review and a clean history entry. |
| Bugfix (non-trivial logic change) | **Yes** — always | None. Even one-line fixes can have subtle effects. |
| Documentation (README, CHANGELOG, CONTRIBUTING) | **Yes** — preferred | Tiny fixes (typo in a comment, single-line docs correction) may push directly if and only if the user explicitly says "ship it" or "just push it." |
| CI hotfix (unblocking a release pipeline) | **Conditional** — branch + PR if time permits; direct push if the pipeline is actively broken and a 2-minute delay compounds the damage | After the hotfix, create a follow-up PR to capture the decision rationale. |
| Release prep (version bump, CHANGELOG entry) | **Yes** — always | The release commit itself is the merge commit from the PR. |

**The rule of thumb:** If you'd want a code review on it, make it a PR. When in doubt, branch.

### The "merged PR branch is dead" rule

When a PR is merged, **the branch is dead.** Any remaining unmerged commits on that branch — even single-commit follow-ups — belong to a new issue, a new branch from `main`, and a new PR.

**Common scenario that triggers this correction:** You filed PR #1 for feature A. It merged. While it was under review, you also pushed a commit for fix B to the same branch. Now PR #1 is merged but fix B was not included. Do NOT push fix B's branch to update the merged PR. Fix B needs its own issue, its own branch from current `main`, and its own PR.

The trap is feeling efficient — "it's just one more commit on the same branch." But the merged PR's branch no longer exists in a meaningful sense: `main` has moved past the merge point, and any additional commits are orphan history. A fresh branch from `main` is the only clean way to propose new work.

**Exception:** Trivial one-line documentation changes that were explicitly part of the same PR scope and were simply forgotten (e.g., a CHANGELOG entry for the merged feature that the reviewer asked you to add). Even then, prefer a fast-follow PR — it keeps the audit trail clean.

**The "I have write access" trap:** Write access doesn't mean you're exempt from the process — it means you're *responsible* for upholding the process on behalf of contributors who don't have write access. Every direct push to main is a signal that the PR process is optional, which erodes the convention for everyone.

**This is especially important in the transition from agent-assisted build phase to open source.** During the build phase, pushing directly to main was efficient — fast iterations, no external contributors, no review needed. But once CONTRIBUTING.md exists and external contributors could arrive, the process has to shift. The first direct push after establishing conventions does more damage than the hundredth one during the build phase.

---