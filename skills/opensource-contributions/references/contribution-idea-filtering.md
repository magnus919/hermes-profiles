# Contribution Idea Filtering: Ideation-to-Issue Gap Assessment

## Problem

A brainstorm or `/ideation` session produces a list of improvement ideas. Filing all of them as issues on a repo is wrong — some won't fit, some are premature, and cluttering the tracker wastes maintainer attention. The missing step: **filtering generic ideas against a specific repo's actual state** before any issue is filed.

## The Methodology

This session's worked example: 9 ideas from `/ideation` → 3 applicable to chazcheadle/rtlamr-meter-reader.

### Step 1: Run repo reconnaissance (read-only)

Before assessing any idea, know what the repo actually has:

```bash
# What infrastructure exists?
ls Dockerfile docker-compose.yml .github/workflows/ 2>/dev/null
ls renovate.json .renovaterc 2>/dev/null
ls CONTRIBUTING.md 2>/dev/null

# What's the contributor pipeline like?
gh pr list --repo owner/repo --state all --json number --limit 1 | jq length
gh issue list --repo owner/repo --state all --json number --limit 1 | jq length

# What labels are available?
gh label list --repo owner/repo --limit 100

# What templates exist?
gh api repos/owner/repo/contents/.github/PULL_REQUEST_TEMPLATE.md --jq '.name' 2>/dev/null || echo "none"
gh api repos/owner/repo/contents/.github/ISSUE_TEMPLATE --jq '.[].name' 2>/dev/null || echo "none"
```

### Step 2: Build a repo-attribute matrix

Map the repo's characteristics to columns:

| Attribute | Value | Signal |
|-----------|-------|--------|
| Has Docker Compose? | Yes/No | Docker health ideas applicable? |
| Uses Renovate? | Yes/No | Renovate auditor applicable? |
| Has CI workflow? | Yes/No | CI-based gates applicable? |
| Has existing PRs? | Count | PR gardener premature? |
| Has stale branches? | Count (besides main) | Branch archiver premature? |
| Has issue/PR templates? | Yes/No | Template unifier needed? |
| Has a SKILL.md? | Yes/No | SKILL.md compliance check applicable? |
| Published on package registry? | Yes/No | Release workflow hygiene relevant? |
| Has CONTRIBUTING.md? | Yes/No | Phase 0 content needed? |

### Step 3: Score each idea against the matrix

Ask for each idea:

1. **Does the repo have the thing this idea targets?** (e.g., "Docker health layering" needs a Docker Compose file — no Docker = not applicable)
2. **Is there enough volume for this idea to matter?** (e.g., "PR gardener" needs existing PRs — 0 PRs = premature)
3. **Is the idea a net negative at this stage?** (e.g., adding a PR size gate to a repo with 0 contributors adds noise, not health)
4. **Does the user already have the thing this idea would add?** (e.g., "Renovate config auditor" — no Renovate means the idea is "add Renovate first," not "audit the config")

### Step 4: Categorize

| Category | Action | Example |
|----------|--------|---------|
| ✅ **High fit** | File issue now | SKILL.md size enforcer on a repo with oversized SKILL.md |
| ⚠️ **Secondary** | File after blocking ideas land | PR size gate after PRs start flowing |
| ❌ **Not applicable** | Skip (repo lacks prerequisites) | Docker health on a repo without Docker |
| 🌳 **Separate project** | File on a different repo or create new project | `gh health-check` is a standalone CLI tool, not a PR |

### Step 5: Present the filtered list

Don't just file the accepted ones — show the user what was excluded and why. This builds trust that the filtering was deliberate:

```
3 of 9 ideas apply to this repo:

✅ FILE:
  - SKILL.md size enforcer (directly addresses 5x budget violation)
  - Issue/PR templates (zero exist — foundational)
  - Dependency drift detector (rtlamr v0.9.5 pinned, no version checks)

❌ SKIP (not applicable / premature):
  - PR size gate (0 PRs exist)
  - Docker health (no Docker)
  - Renovate auditor (no Renovate)
  - PR gardener (0 PRs)
  - Branch archiver (0 stale branches)
  - gh health-check CLI (separate project, not a PR)
```

## Decision Table

| Repo characteristic | Ideas that fit | Ideas that don't |
|--------------------|----------------|-------------------|
| Has SKILL.md | SKILL.md size enforcer, progressive disclosure audit | — |
| No issue/PR templates | Template unifier | — |
| Has Docker Compose | Docker health layering | — |
| Has Renovate config | Renovate auditor | — |
| Has active PRs (3+) | PR size gate, PR gardener | — |
| Has stale branches (3+, 90d+ untouched) | Branch archiver (`git archive-branch`) | — |
| Has CI workflow | CI-related gates (size, compliance) | PR size gate (if repo has no PRs) |
| Has package registry (PyPI, npm) | Release workflow hygiene | — |
| No CI/CD at all | Start with CI foundation | Any CI-dependent gate is premature |
| Brand new (0 issues, 0 PRs, 0 contributors) | Templates, CONTRIBUTING.md, dependency drift | Everything else is premature |

## Why This Matters

Without this filter, an ideation session that produces 9 reasonable ideas leads to **9 issues filed on a repo where 6 are noise.** The user has to sort through which ones apply, the maintainer scrolls past irrelevant issues, and the tracker accumulates dead entries. The 30 seconds of reconnaissance before filing saves everyone time.
