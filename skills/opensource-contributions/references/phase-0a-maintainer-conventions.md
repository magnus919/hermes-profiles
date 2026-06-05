
## Phase 0a: Establishing Open Source Conventions (Maintainer)

When you're setting up open source conventions for *your own project* — whether bootstrapping from scratch or formalizing after a build phase — this phase precedes all others. It's the maintainer mirror of the contributor checklist below.

### README Discipline: Describe What Exists, Not What You Plan

When writing the initial README for a repo, **describe what exists on disk right now**. Do not lay out a directory tree of folders you intend to create, a roadmap of features yet to be built, or an aspirational architecture. Ground the README in the present state.

This is not about ambition — it's about trust. A README that lists directories that don't exist yet fabricates a reality the reader will discover is false when they clone the repo. That erodes trust before the project has even started.

**Good initial README:**
- States what the repo is for (one paragraph)
- Describes what's actually in it ("Nothing yet — check back")
- Defines the concept of a skill (for context)
- Links to the license

**Bad initial README:**
```
agent-skills/
├── research/           # Web research, article capture, knowledge extraction
├── content/            # Blog writing, image generation, creative workflows
├── devops/             # Infrastructure management, deployment, CI/CD
├── software-development/  # Coding patterns, debugging, code review
├── thinking/           # Multi-agent debate (council), structured reasoning
└── templates/          # Skill templates for creating new skills
```

This directory tree described 6 folders. Zero existed. The README was a wishlist, not a description. When the user reads it and types `ls`, they find an empty folder — the discrepancy undermines confidence in everything else the agent produces.

**The principle generalizes:** Any document that describes the current state of a system (README, project overview, architecture doc, status report) must be verifiable against reality. If you can't point to a file on disk or a working feature for every item you list, don't list it. Say "planned" or "roadmap" explicitly, or leave it out until it exists.

**Future-proofing:** When you do add a folder or feature, update the README at that moment — not as a separate pass. The README should always be a snapshot of the current state, not an accumulation of past plans.

---

### What to Create

| Artifact | Purpose | Location |
|----------|---------|----------|
| **LICENSE** | The legal terms. Pick before anything else — it dictates DCO vs CLA, contribution terms, and what downstream users can do. | `LICENSE` (repo root) |
| **CONTRIBUTING.md** | The single source of truth for how to contribute. Covers dev setup, commit conventions, PR process, DCO/CLA. | `CONTRIBUTING.md` (repo root) |
| **Bug report template** | Structured form so contributors provide environment, reproduction steps, expected vs actual behavior. | `.github/ISSUE_TEMPLATE/bug_report.md` |
| **Feature request template** | Problem-focused framing so contributors explain *why*, not just *what*. | `.github/ISSUE_TEMPLATE/feature_request.md` |
| **PR template** | Summary + test plan + breaking changes + issue links. Keeps PRs reviewable. | `.github/PULL_REQUEST_TEMPLATE.md` |
| **Labels** | GitHub's defaults (bug, enhancement, documentation, good first issue, help wanted, question) cover most needs. Add domain-specific labels only when triage volume justifies them. | GitHub repo settings |

### Conventions to Choose Early

| Decision | Options | Recommendation |
|----------|---------|---------------|
| **Commit format** | Conventional Commits, Freeform, Angular | **Conventional Commits** — `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `ci:`, `chore:`, `perf:`. Widely understood, machine-parseable, generates changelogs. |
| **Legal sign-off** | DCO (`Signed-off-by`), CLA, None | **DCO** for most projects — lighter weight than a CLA, legally sufficient for Apache 2.0 / MIT. Require `git commit -s` on every commit. |
| **Scope style** | Module names, issue numbers, none | Module/area names when the project has distinct subsystems (e.g., `fix(vec-search):`). Omit for small projects. |
| **Branch naming** | `fix/`, `feat/`, `refactor/`, `docs/`, `ci/` prefixes | Match commit types for consistency. One branch per logical change. |
| **Merge strategy** | Squash, Rebase, Merge commit | **Squash merge** for feature branches — keeps main history clean, allows fixup commits during review without force-push. |

### CONTRIBUTING.md — What to Cover

A good CONTRIBUTING.md answers these questions for a first-time contributor:

1. **How do I set up a dev environment?** Exact commands, venv caveats, system requirements. Include troubleshooting for known issues (namespace collisions, symlink requirements, etc.).
2. **How do I run tests?** Single command, any test framework quirks, offline requirements.
3. **What commit format do you use?** Show examples of good and bad commit messages.
4. **Do I need to sign commits?** If DCO, say `git commit -s` and link to developercertificate.org.
5. **What's the PR workflow?** Branch from main, one change per PR, no force-push after review, CI must pass.
6. **What's the project architecture?** A 3-5 sentence overview so they know where their change lives.
7. **Where do I report security issues?** Separate channel from public issues.

### When to Establish Conventions

- **Bootstrapping**: Best time — set conventions before the first external contributor arrives.
- **After a build phase**: Common for projects that started as internal tools or agent-assisted builds. The conventions formalize what was implicit during the build phase. **Crucial**: align the commit history with the new conventions retroactively via the CHANGELOG, not by rewriting history. The existing history is what it is — the convention applies going forward.
- **Never**: Rewriting history to retroactively enforce new commit conventions. Don't force-push over published history.

### Phase 0b: Reconcile Issues After Architecture Change

When a significant refactor changes the project's architecture (e.g., "stop implementing everything yourself, become a thin adapter around upstream"), existing open issues need reconciliation. Feature requests written for the old approach may no longer make sense.

**The workflow:**

1. **List all open issues** and group them by type:
   - Directly addressed by the refactor → close as completed
   - Now handled by upstream/dependencies → close as out of scope (comment explaining why)
   - Still valid but need re-scoping → update title and body, link to related issues
   - Truly still open → leave, but verify they're still actionable

2. **Check milestones** — if the refactor shipped as a release but didn't close its milestone issues, the milestone is in a broken state:
   - Move re-scoped issues out of the milestone (so closing it doesn't orphan them)
   - Close issues that are fixed or out of scope
   - Close the milestone with a description explaining what actually shipped vs what was deferred

3. **Update issue bodies** for re-scoped items — old feature descriptions are misleading. Replace them with:
   - What changed (the refactor that made the old approach obsolete)
   - What the new approach should look like (specific acceptance criteria)
   - Links to related issues (e.g., "Resolved by #N")

4. **Document the reconciliation in the CHANGELOG** — future contributors shouldn't find closed issues in old milestones without knowing why.

**Example session output (9 issues → 3):**

| Outcome | Count | Examples |
|---------|-------|---------|
| Closed (fixed by refactor) | 2 | Schema fork → now uses upstream `ensure_schema()` |
| Closed (out of scope) | 4 | Dashboard, extractor plugins, warm daemon, novelty gate |
| Re-scoped | 2 | Privacy → `exclude_tags` passthrough; Think cycles → resolved-by LLM integration |
| Kept | 1 | LLM integration (the remaining core gap) |

**CLI commands for bulk reconciliation:**

```bash
# Close an issue with a reason
gh issue close N --comment "Reason for closing…" --reason "completed"  # or "not planned"

# Edit issue body (re-scope)
gh issue edit N --body "New body text…"

# Remove milestone
gh issue edit N --remove-milestone

# Close milestone
gh api repos/owner/repo/milestones/M -X PATCH -f state=closed

# Bulk: list all open issues in a milestone
gh issue list --state open --json number,title --jq '.[] | .number'
```

### Release Workflow Hygiene

After setting up contribution conventions, check that the release workflow won't publish broken code. Two structural gaps to close:

1. **Gate behind tests**: The release workflow's build job should `needs: test` — never build or publish if tests are red. See `references/ci-debugging-loop.md` Step 8 for the YAML pattern.
2. **Add `workflow_dispatch`**: Manual trigger so a failed release can be retried without deleting and recreating the tag.

These are part of the initial setup, not deferred concerns. A PyPI release that bypasses CI is worse than no release at all — downstream users install the broken package.

### Pitfall: PyPI rejects git+SHA dependency pins

If your project uses a git+SHA pinned dependency during development (e.g., `package @ git+https://github.com/user/repo.git@abc123`), the PyPI publishing workflow will reject the package with `400 Can't have direct dependency`. PyPI only accepts version specifiers (`package>=1.0.0,<2.0.0`).

**When this happens:** Before your first PyPI release, check if your dependency is published on PyPI. If it is, switch the specifier before tagging. If it isn't, you need an alternative distribution strategy (point users to pip install from source, or publish the dependency first).

**The gotcha:** Agent-built projects often use git+SHA pins during development because the agent pins the exact version it tested against. This works fine for dev installs but blocks publishing. The fix is trivial (swap the specifier) but it blocks the release workflow silently — the build passes, the wheel passes, only the upload step fails.

### Template: CONTRIBUTING.md Structure

A minimal but complete CONTRIBUTING.md needs these sections in order:

```
# Contributing to [Project Name]

Table of Contents


  - Development Install
  - Running Tests
  - Understanding the Architecture

  - Reporting Bugs
  - Suggesting Features
  - Pull Requests

  - Conventional Commits
  - Signing Your Commits (DCO)




```

Each section should be concrete — exact commands, exact file paths, real examples. Avoid "please follow best practices" — show them what best practices look like in *this project*.

For a worked example of a CONTRIBUTING.md created during an agent-assisted post-build transition, see `references/hermes-cashew-contributing-worked-example.md`.

---