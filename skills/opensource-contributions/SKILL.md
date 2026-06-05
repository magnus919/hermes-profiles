---
name: opensource-contributions
description: >-
  Make good open source contributions — check CONTRIBUTING.md first, follow
  project norms, be a good citizen. Covers bug reports, feature requests, and
  pull requests with a defensible default posture when the project hasn't
  documented expectations.
license: MIT
compatibility: Compatible with any agent supporting the Agent Skills format (Hermes Agent, Claude Code, GitHub Copilot, OpenCode, Cursor, etc.)
metadata:
  tags: [opensource, contributing, github, etiquette, PRs, issues]
  related_skills: [github-issues, github-pr-workflow, github-code-review]
  version: "1.6.0"
  author: Hermes Agent community
source_repo: https://agentskills.io
---

# Open Source Contributions

## The Golden Rule

**Make it easy for maintainers to absorb your contribution.** Maintainers are often under-resourced volunteers or small teams. Every friction point you remove — unclear reproduction steps, missing tests, bad commit messages, force-pushed history — is time they don't have to spend figuring out what you did and why. The whole point is to *help* them, not create more work.

## When to Use This Skill

- Filing a bug report or feature request on a public repository
- Preparing a pull request for any open source project
- Working on a project without documented contributing guidelines (default posture)
- Reviewing your own PR before submission
- Setting up open source conventions for your own project

**Load the relevant phase reference for detailed instructions.**

---

## Quick Phase Overview

| Phase | What It Covers | Reference |
|-------|----------------|-----------|
| **0a — Maintainer Conventions** | README discipline, LICENSE, CONTRIBUTING.md, issue/PR templates, commit conventions, DCO, release workflow hygiene | `references/phase-0a-maintainer-conventions.md` |
| **0 — Before You Start** | Reading CONTRIBUTING.md, checking existing issues/PRs, triaging bugfix candidates, large-change discussion etiquette | `references/phase-0-before-you-start.md` |
| **1 — Filing Issues** | Bug report and feature request templates, agent disclosure, maintainer workflow ("issue first"), coordinated multi-issue roadmaps, multi-PR plan execution | `references/phase-1-filing-issues.md` |
| **2 — Pull Requests** | Branching conventions, scope assessment, studying existing implementations, cross-repo comparison, commit messages, PR templates, documentation audits, CI setup | `references/phase-2-pull-requests.md` |
| **3 — After Submitting** | CI monitoring, responding to review feedback, what to do if your PR goes stale or gets closed | `references/phase-3-after-submitting.md` |
| **3.5 — Follow-up After Scope Feedback** | Systematic call-site audits, filing comprehensive issues, complementary PRs when maintainer scope notes identify gaps | `references/phase-35-followup.md` |
| **4 — Release Process** | Version bumping, tagging, GitHub Releases vs tags, release workflow anatomy, handling failed releases | `references/phase-4-release-process.md` |

### Default Posture (No CONTRIBUTING.md)

When a project has no contributing guide, load `references/default-posture.md` for defensible defaults on issue filing, PRs, communication norms, and code of conduct.

### Agent-Specific Checklist

If you are an AI agent filing or contributing on behalf of a human, load `references/agent-checklist.md` before submitting anything.

### Pitfalls

Load `references/pitfalls.md` when you're about to submit an issue or PR, or when something goes wrong. Covers: backtick expansion, silent label failures, force-push etiquette, the "I'll just fix it quickly" trap, cross-fork PR issues, post-merge scope creep, the installed-code trap, CI debugging, and more.

---

## The Agent-Specific Rule

When filing an issue on behalf of a human, **always disclose the agentic nature.** Add this line at the bottom of the issue body:

```
Filed by {{AGENT_NAME}} (AI agent on behalf of {{HUMAN_NAME}})
```

This is a transparency requirement, not a courtesy. Maintainers deserve to know who they're talking to.

---

## Quick Reference Card

| Step | Action | Command / Check |
|------|--------|-----------------|
| 0 | Read contributing guide | `cat CONTRIBUTING.md` or `.github/CONTRIBUTING.md` |
| 0 | Check existing issues | `gh issue list --search "topic" --state all` |
| 1 | File a bug/feature | Use template if provided; include reproduction for bugs |
| 2 | Issue first before coding | File issue, wait for maintainer feedback, then branch |
| 3 | Branch | `git checkout -b fix/description` |
| 4 | Commit | `git commit -s -m "fix: description"` |
| 5 | Run tests locally | `make test` or `npm test` or `pytest` |
| 6 | Push | `git push -u origin HEAD` |
| 7 | Open PR | Fill out PR template completely. Use `--body-file` for complex bodies |
| 8 | Monitor CI | `gh pr checks --watch` |
| 9 | Address review | Respond to comments, push fixup commits. No force-push after review |
| 10 | After merge | `git checkout main && git pull && git tag vX.Y.Z && git push origin main --tags` |
| 11 | Create Release | `gh release create vX.Y.Z --title "vX.Y.Z — Title" --notes-file /tmp/notes.md` |

---

## When NOT to Use This Skill

- You're the sole maintainer of a project with no external contributors and no public collaborators
- You're making a trivial single-line fix to your own code
- The contribution is internal (same organization, same team) with established workflow norms
- You already know the project's contributing guidelines by heart and this is routine
- The issue is a security vulnerability — follow the project's security disclosure policy instead
