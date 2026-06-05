# Worked Example: Establishing CONTRIBUTING.md Post-Build Phase

## Context

A project transitioning from an agent-assisted build phase to a formal open source project needed contributing conventions established. The project had shipped 3 milestones via rapid iteration before any open source conventions existed.

- **License**: Apache 2.0
- **Language**: Python
- **Build system**: Hatchling
- **Test framework**: pytest

## Key Architectural Detail

The project used PEP 420 namespace packages (no `__init__.py` at intermediate levels), with a dual-path loading strategy for pip-installed vs. flat-entry loaders. The dev install required a non-obvious symlink — without documenting this, the first external contributor would hit a `ModuleNotFoundError` with no obvious fix.

## What Was Created

| Artifact | Key Decisions |
|----------|--------------|
| `CONTRIBUTING.md` | DCO sign-off required; Conventional Commits; one PR per change; no force-push after review; tests must run locally first |
| `.github/ISSUE_TEMPLATE/bug_report.md` | Project-specific env fields (library version, storage backend status) |
| `.github/ISSUE_TEMPLATE/feature_request.md` | Problem-first framing with scope estimation |
| `.github/PULL_REQUEST_TEMPLATE.md` | Summary + test plan + breaking changes section |

## Convention Choices

### Commit Format: Conventional Commits

The existing git history already used `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `ci:`, `chore:` prefixes from the build phase. Formalizing them codified existing practice.

### Legal: DCO (Developer Certificate of Origin)

Apache 2.0 license + DCO is the standard lightweight combination. `git commit -s` on every commit.

### Branch Naming: Match Commit Types

```
fix/description       → fix/vector-search-rowid-mismatch
feat/description      → feat/add-ollama-embedding-support
refactor/description  → refactor/extract-db-migration-module
docs/description      → docs/api-reference-typo
ci/description        → ci/publish-automation
```

### Merge Strategy: Squash

Keeps main history clean. Allows fixup commits during review without force-push.

## What Was Tricky

### The virtual environment + symlink dev install

The most non-obvious setup detail: the project's loader inserts itself at the front of `sys.path`, making its bundled `__init__.py` a regular package that blocks PEP 420 namespace resolution. A dev install (`pip install -e .`) must be done in the project's virtual environment AND requires a symlink into the loader's plugin directory.

### Offline requirement in tests

The embedding model was ~500 MB. Tests must never trigger a download. Documented as: offline environment variable in `conftest`, enforced by CI log-scan.

### Knowledge graph for orientation

The project included a generated knowledge graph directory, documented as an orientation tool for new contributors — cheaper than reading every source file.

## What Got Deferred

- **Automated linter** — no CI enforcement (yet). Noted as aspirational.
- **Issue labels** — used GitHub's defaults. No domain-specific labels yet.

## Phase 2: Issue Reconciliation

After the conventions were established, 9 open issues were reconciled against the new architecture pivot. The conventions tell contributors *how* to contribute; issue reconciliation tells them *what* still needs doing.

### Process

1. Read each open issue through the lens of the new architecture
2. For issues describing functionality now handled upstream: close with explanation
3. For issues needing re-scoping: update the body, change the milestone
4. For still-valid issues: leave open, verify they're actionable

### Outcome

| Result | Count | Examples |
|--------|-------|---------|
| Closed (addressed by refactor) | 2 | Schema fork, novelty gate |
| Closed (out of scope for thin adapter) | 4 | Warm daemon, dashboard, domain separation, custom extractors |
| Re-scoped | 2 | Think cycles → resolved-by LLM integration; Privacy filter |
| Kept | 1 | LLM integration (the core remaining gap) |

### Milestones Cleaned Up

Three milestones were closed as all their issues were resolved or determined out of scope. One milestone remained open for the one re-scoped privacy issue.
