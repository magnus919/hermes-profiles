# Project Fingerprint Template — P0 Artifact

P0 produces a single conventions card — not a dossier. The agent must be able to fill this in under 5 minutes. If a field requires more time than that, the project has unusual complexity and the agent should flag it.

---

## Fingerprint Fields

```yaml
# REQUIRED — must be filled
project: owner/name
fingerprinted_at: ISO timestamp
head_commit: full SHA
default_branch: main or master

# CONVENTIONS — each must cite at least one merged PR as evidence
test_framework: pytest / nose / jest / ava / go test / cargo test / unknown
test_runner_command: the exact command (e.g., "python -m pytest tests/ -q")
linter: ruff / flake8 / eslint / prettier / gofmt / none
linter_command: the exact command (e.g., "ruff check .")
commit_convention: Conventional Commits / freeform / signed-off / other
commit_convention_evidence: PR #123 used "fix(scope): description" format
pr_size_preference: small (<200 lines) / medium (200-500) / large (500+) / unstated
pr_size_evidence: merged PRs studied had median 147 lines changed
review_style: line-by-line / holistic / approval-only / unknown
review_style_evidence: PR #456 had 12 inline comments before approval
ai_policy: welcome / disclose-required / banned / unknown
ai_policy_source: AGENTS.md line 14 says "AI contributions welcome with disclosure"
security_contact: email or URL from SECURITY.md, or "none found"
branch_naming: fix/ feat/ docs/ or no convention
branch_naming_evidence: PR #789 used "fix/null-check-in-parser"
ci_provider: GitHub Actions / GitLab CI / Jenkins / CircleCI / none
ci_config_path: .github/workflows/ci.yml

# REFERENCE PRs — URLs to the merged PRs studied
reference_prs:
  - url: https://github.com/owner/repo/pull/123
    type: bugfix
    contributor: different from Magnus
    lines_changed: 47
  - url: https://github.com/owner/repo/pull/456
    type: feature
    contributor: different from Magnus
    lines_changed: 312
  - url: https://github.com/owner/repo/pull/789
    type: refactor
    contributor: different from Magnus
    lines_changed: 89

# DISCREPANCIES — where templates and reality differ
discrepancies:
  - "CONTRIBUTING.md says 'use pytest' but 3/5 merged PRs use unittest"
  - "PR template asks for 15 checkboxes but all merged PRs leave 8-10 unchecked"

# DANGER SIGNALS — things that could cause problems
danger_signals:
  - "Repo uses git-lfs for large binary files — sparse checkout recommended"
  - "Build requires PostgreSQL running — Docker with service container needed"
  - ".env.example exists — careful not to commit secrets"
```

## Size Limit

If the fingerprint exceeds ~2000 words, the project is too complex for a single conventions card. Switch to layered strategy:
1. Top-level: the 8 required fields above
2. Deep-dive files: per-directory conventions loaded on demand during P1/P2

## Cache Invalidation

On every load:
1. Compare cached `head_commit` against current `git rev-parse HEAD`
2. If mismatch → full regeneration (not cache + patch)
3. TTL: if fingerprint is >1 hour old, refresh regardless of HEAD match
4. If any `danger_signals` field references a file that no longer exists → regenerate
