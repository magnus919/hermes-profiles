## Phase 2: Pull Requests

### Before Writing Code

1. **Fork and clone** the repo (if you don't have write access)
2. **Create a feature branch** from the main development branch
3. **Check the branch naming convention** in CONTRIBUTING.md — common patterns:

| Pattern | Example |
|---|---|
| `fix/description` | `fix/login-redirect-null-pointer` |
| `feat/description` | `feat/add-jwt-auth` |
| `bugfix/description` | `bugfix/issue-42` |
| `username/description` | `user/fix-stream-timeout` |
| `issue-N-description` | `issue-142-fix-typo` |

4. **Make small, focused commits** — one logical change per commit

### Scope Assessment: Trace Before You Build

Before writing code, **trace every code path that could be affected by your change.** A feature request or bug fix that seems local may touch multiple independent paths. Missing one produces a partial fix and a second round of review.

**The methodology (demonstrated on rreading-glasses issue #96):**

1. **Map the entry points.** List every handler, endpoint, or CLI command that could serve the data you're changing:
   ```bash
   grep -n 'func.*Handler.*get\|func.*Handler.*search\|func.*Controller\.' *.go
   ```

2. **Follow each path to the data.** For each entry point, trace: handler → controller method → cache/getter call → data transformation. Does it manipulate the field you're changing? At what line?

3. **Build a flow table.** Every path gets a row:

   | Code Path | Subtitle Handling | Title Set Where |
   |-----------|------------------|-----------------|
   | `handler:getAuthorID` → controller | Smart dedup logic | `controller.go:1049-1071` |
   | `handler:bulkBook` | Always FullTitle (independent) | `handler.go:242-247` |
   | `handler:getWorkID` | Passthrough (no manipulation) | None |

4. **Identify the true change surface.** Most paths may be irrelevant (passthrough), some may be intentionally different (search shows full titles). The actual change is usually 1-2 condition checks. The table tells you *which* ones.

5. **Check for pre-existing independence.** If one path already hardcodes a different behavior (e.g., search always shows subtitles), it was a deliberate decision. Don't unify it unless you understand why it diverged.

**Why this matters:** Without the trace, you might change the right condition in the right file but miss that a separate handler independently overrides the field. Or you might spend time refactoring four paths when only one matters.

The output of this step goes in the PR's "Scope Assessment" section to show the maintainer you checked all paths.

### Study Existing Implementations First

Before writing code that extends an interface or adds a new plugin/extractor/tool,
**read the existing implementations of the same interface.** This is faster and
more accurate than guessing the pattern from the base class alone.

**What to read:**
1. **The base class / abstract interface** — understand the contract (`extract()`,
   `get_state()`, etc.)
2. **One or two concrete implementations** — how they handle incremental processing,
   error handling, model_fn, state persistence
3. **The wiring / registration point** — how the CLI or registry discovers and
   invokes it
4. **The tests for existing implementations** — understand the test patterns,
   fixtures, and what edge cases are covered

**Technique:** Use `gh api repos/owner/repo/contents/` to read these files
remotely without cloning (see `references/remote-code-exploration.md`). By the
time you clone or branch, you should already know exactly where your new file
goes, what imports it needs, and how it registers.

**The signal that you've studied enough:** you can answer "what's the minimal
set of methods my class needs to implement, and what pattern does each one
follow?" without looking at the base class again.

### Cross-Repo Comparison for Feature Extraction

When contributing improvements inspired by a **different project** (a fork,
plugin, or parallel implementation that solved the same problem differently),
use cross-repo comparison to extract what the other project did better:

1. **Clone both repositories** side by side:
   ```bash
   git clone https://github.com/owner/upstream.git upstream
   git clone https://github.com/owner/fork.git fork
   ```

2. **Read the equivalent module in both** — don't guess the differences. Read
   both implementations end-to-end.

3. **Build a comparison table** with concrete columns:

   | Dimension | Upstream (old) | Fork (new) | Improvement |
   |-----------|---------------|------------|-------------|
   | Scaling strategy | Full-graph O(N²) | Work-capped incremental | Bound compute to subset |
   | DB writes | Per-pair commit | Batched executemany | ~1000× fewer round-trips |
   | Architecture | Stateful class | Pure functions | Testable, composable |
   | Error handling | try/except | Input filtering pre-check | Explicit precondition |

4. **For each improvement, ask**: "Is this a fundamental algorithmic improvement,
   a performance optimization, a safety feature, or a structural preference?"
   This determines which belong in the issue and which are style differences.

5. **Draft the issue** before implementing — document the comparison findings,
   proposed improvements, and a sketch of the new design. Reference the source
   project where the pattern was proven. This gives the maintainer a chance to
   correct direction before you invest in implementation.

6. **Implement with a backward-compatible shell** — the maintainer's existing
   callers (tests, scripts, integrations) should not break. See the section
   below on backward compatibility.

7. **Preserve existing tests** — every existing test that still tests valid
   behavior must pass unchanged. Add new tests for the new code paths. If the
   existing tests exercised the system via a different interface (class methods
   vs free functions), keep that interface working.

8. **Run both test suites** — the old tests AND the new tests. If the old tests
   are testing through a deprecated interface, that's fine — those callers still
   exist and the maintainer needs to know they still work.

9. **Update ALL project docs that reference the changed area** — README tables,
   CLAUDE.md architecture docs, DESIGN.md specification, and any inline code
   comments. A PR that changes how a core module works but doesn't update the
   developer guide leaves the project in a worse state than it started.

### Backward-Compatibility Pattern for Refactoring

When rewriting a module that has existing callers (tests, scripts, integrations),
use a **shell-and-pipeline** architecture to avoid breaking them:

```
Old interface (class) ──▶ checks dependencies ──▶ New pipeline (free functions)
                      │                         │
                      └── if absent ──▶ Legacy fallback (old code path)
```

**Implementation steps:**

1. **Extract the new algorithm into free functions.** Each phase of the
   pipeline is a standalone function with explicit `conn` parameter. No class
   state, no implicit connection fetching.

2. **Keep the old class interface.** Every public method stays — same name,
   same signature, same return type. Add a deprecation notice in the docstring
   if desired, but don't remove it.

3. **Make the main orchestration method a dispatcher.** The class's
   `run()` / `execute()` method checks whether the new infrastructure exists
   (e.g., required table in the database, required library). If yes, delegate
   to the new pipeline. If no, fall back to the old per-method approach.

4. **The legacy fallback preserves old behavior unchanged.** It calls the
   same class methods in the same order as the original implementation. This
   ensures test databases without the new infrastructure (e.g., no embeddings
   table) continue to work.

5. **Keep both code paths until the maintainer explicitly removes the old one.**
   Don't delete the legacy path — that's the maintainer's call once they've
   verified the new path covers all cases.

**When to use this pattern:** Any refactoring where:
- The module has existing tests you must not break
- The new implementation requires infrastructure the old one didn't (a DB table, a library, a configuration key)
- The change is structural enough that callers might rely on specific intermediate behaviors

For a worked example of this pattern applied to a real upstream PR (Cashew
sleep cycle refactor, 61 tests preserved), see
`references/sleep-cycle-refactor-worked-example.md`.

**When NOT to use this pattern:** Adding a new module or feature that has no
existing callers — there's nothing to be backward compatible with.

### Commit Messages

Default format (Conventional Commits, widely used):

```
type(scope): short description

Longer body explaining why the change was made, wrapped at 72 characters.
Reference related issues (Fixes #42) in the body.

Signed-off-by: Your Name <email>
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `ci`, `chore`, `perf`, `style`

**Sign-off:** If the project uses DCO (Developer Certificate of Origin), every commit MUST have:

```bash
git commit -s  # Adds Signed-off-by trailer automatically
```

The DCO certifies you have the right to contribute the code under the project's license. It's legally simpler than a CLA and many projects prefer it.

**Never force-push to shared branches** unless the project's contributing guide explicitly asks for it (some projects want rebased, clean history). When in doubt, add commits on top.

### 🔴 Mandatory: Use Project Issue & PR Templates

**For both issues AND PRs, check for and use the project's templates first.**

#### Issue Templates

Before filing an issue, check if the project has structured templates:

```bash
# List available issue templates
gh api repos/$OWNER/$REPO/contents/.github/ISSUE_TEMPLATE --jq '.[].name' 2>/dev/null

# If templates exist, pick the right one and fetch it
gh api repos/$OWNER/$REPO/contents/.github/ISSUE_TEMPLATE/bug_report.yml --jq '.content' 2>/dev/null | \
  python3 -c "import sys,base64; sys.stdout.buffer.write(base64.b64decode(sys.stdin.read()))" \
  > /tmp/issue-template.md 2>/dev/null
```

**If issue templates exist:**
- Use the correct template type (bug_report vs feature_request vs task)
- Fill in ALL required fields — do not skip sections
- Keep the YAML form structure intact — don't remove fields
- Include agent disclosure at the end of the body

**If no issue template exists**, use the standard structure from the Filing Issues section above.

#### PR Templates

Before writing any PR body, fetch the project's template:

```bash
gh api repos/$OWNER/$REPO/contents/.github/PULL_REQUEST_TEMPLATE.md --jq '.content' | \
  python3 -c "import sys,base64; sys.stdout.buffer.write(base64.b64decode(sys.stdin.read()))" \
  > /tmp/pr-template.md 2>/dev/null
```

**If a template exists, you MUST:**
- Use every section header exactly as written — do not rename, reorder, or remove any
- Keep every checkbox — leave unchecked boxes in place so reviewers can see what wasn't done
- Fill sections that don't apply with "N/A" or "Not applicable" — do not delete them
- Include all HTML comments and link reference definitions from the template
- Use `--body-file` (not `--body`) for the PR body to avoid shell escaping issues

**If no template exists**, use this default structure:

```markdown
<What this PR does, in 1-2 sentences>

- <Specific change 1>
- <Specific change 2>

- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing done (describe)

Closes #42
Fixes #123
```

#### 🔴 Mandatory Compliance Gate

Before submitting ANY PR (create or edit), run the compliance checker:

```bash
python3 scripts/check-pr-template-compliance.py \
  /tmp/pr-body.md /tmp/pr-template.md
```

**If this exits non-zero — DO NOT SUBMIT.** Fix the body and re-run. This gate is not optional. Multiple PRs were rejected on May 19 2026 for template violations across different projects.

**One PR per logical change.** Don't mix a bugfix with a refactoring with a feature. Maintainers may want to accept one and reject another, and they can't if they're in the same PR.

**Include tests** for new code. If the project doesn't have tests, at minimum document how you verified the change works.

**Documentation is not optional.** A feature PR that doesn't update the README, CHANGELOG, or relevant docs is incomplete. This applies even (especially) when you're the maintainer shipping your own project — the README is the user's first impression, and if it doesn't describe the new feature, the feature doesn't exist to the user. The rule: **before opening the PR, verify every user-facing change has a corresponding doc update.** If you can't point to the line in the README that describes what you just added, the PR isn't ready.

### 📋 Mandatory Pre-PR Step: Test Locally First

**Do NOT open a PR until you have verified the implementation works in the actual environment.** The user explicitly requires this — "I want to test it locally before opening the PR." A branch with unverified code is not ready for review.

The local test must verify more than just "tests pass." It must confirm the feature actually produces correct output in the real runtime:

```bash
# For a code change: run the actual feature end-to-end
python3 scripts/orchestrate.py full --mode new-feature --question "test question" --agents 3

# Verify the output matches expectations
ls -la /tmp/output-dir/
cat /tmp/output-dir/results.json | python3 -m json.tool

# For a bugfix: reproduce the original issue first, confirm fix resolves it
# For a new command: run --help and verify the new option appears
```

**The distinction matters:** Local tests confirm your code doesn't crash. Local *verification* confirms it produces correct results. You need both before the PR exists. If the user says "test it locally first," they mean verification, not just test-passing.

**Checklist before opening:**
- [ ] README updated if user-facing behavior changed (new feature, new config key, changed behavior)
- [ ] CHANGELOG updated (new entry for unreleased changes)
- [ ] Docstrings/type hints on new public APIs
- [ ] Existing docs scanned for references to the changed area (outdated examples, stale config snippets)

### Before Opening the PR

1. **Verify everything is committed** — `git status` must show a clean working tree. The most common new-contributor mistake is pushing without committing, which produces "No commits between upstream:main and your:branch" on PR creation.
2. **Rebase on latest upstream** (don't merge unless the project prefers merge commits). If conflicts arise, see `references/rebase-conflict-resolution.md` for the step-by-step resolution workflow.
3. **Run the test suite** locally — don't rely on CI to catch basic failures
4. **Check for merge conflicts** — if there are conflicts, resolve them using `references/rebase-conflict-resolution.md`
5. **Lint your code** per the project's style (run the formatter/linter they use)

```bash
# FIRST: verify commits exist
git status                  # Must show: nothing to commit, working tree clean
git log --oneline origin/main..HEAD  # Must show your commit(s)

git fetch origin
git rebase origin/main
# If conflicts: see references/rebase-conflict-resolution.md
# After resolving:
git push --force-with-lease  # --force-with-lease, not --force
```

### Documentation Audit Before Opening

**Documentation is not optional.** A feature PR that doesn't update the README, CHANGELOG, or relevant docs is incomplete. This applies even (especially) when you're the maintainer shipping your own project — the README is the user's first impression, and if it doesn't describe the new feature, the feature doesn't exist to the user.

**Three-document scan for CLI/command changes:** When your PR adds or modifies a CLI command, subcommand, or flag, scan these three locations before opening:

1. **CLI help text** — Run `command --help` and verify the new command appears in the choices list, usage examples, and epilog. If the project has a help string that lists available subcommands (e.g., `choices=['obsidian', 'sessions', ...]`), update it.
2. **README CLI reference tables** — Most projects with CLIs have a table of commands in the README. Add a new row for the command, or update any existing row that your change affects.
3. **Project-internal dev docs** — Some projects maintain a `CLAUDE.md`, `AGENTS.md`, or `DEVELOPMENT.md` with architecture documentation, including tables of modules or interfaces. If your change adds a new module (e.g., a new extractor, new plugin, new tool), that table needs a new row.

The test: **before opening the PR, can you point to the exact line in the README that tells a user how to use what you just added?** If not, the PR isn't ready.

**CLI-specific checklist:**
- [ ] `command --help` output includes the new subcommand
- [ ] README CLI reference table has a row for the new command
- [ ] Developer docs (CLAUDE.md, AGENTS.md) updated for new modules/interfaces
- [ ] Existing examples or usage snippets that reference the changed area are updated

---