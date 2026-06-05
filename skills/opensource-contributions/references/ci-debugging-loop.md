# CI Debugging Loop

A systematic approach to fixing CI failures on a Python project. Use this anytime CI turns red after a push.

## Step 1: Read the CI Logs

```bash
# Get the failed run ID
gh run list --limit 3 --json conclusion,displayTitle,status,databaseId

# View failed steps
gh run view <RUN_ID> --log-failed

# View full output for a specific job
gh run view <RUN_ID> --log
```

**What you're looking for:** The exact test name that failed, the assertion error, and any clues about why (env var mismatch, missing method, import error, etc.).

## Step 2: Reproduce Locally

```bash
# Reproduce just the failing test
pytest -xvs tests/test_file.py::test_name

# If it passes locally but fails in CI, check for environment differences:
# - Python version (CI may use 3.11 vs your 3.13)
# - Installed dependencies (CI installs fresh; you may have stale packages)
# - Environment variables (CI sets HF_HUB_OFFLINE=1, etc.)
# - Entry-point metadata (`pip install -e .` may cache old entry points)
```

## Step 3: Isolate Pre-existing vs New Failures

Before assuming your change broke something, check if the test was already failing:

```bash
# Stash your changes, run the failing test on clean main
git stash
pytest -xvs tests/test_file.py::test_name
git stash pop
```

| Result | Diagnosis |
|--------|-----------|
| Fails on clean main too | **Pre-existing** — your change didn't cause it. Fix separately or skip. |
| Passes on clean main, fails with your changes | **Regression** — your change caused it. Debug the interaction. |
| Different test fails on clean main | **Test ordering / flaky** — env sensitivity or timing race. Run again. |

## Step 4: Root Cause Categories

### Env Var Leakage

The user's development environment may set env vars that leak into tests. Common culprits:
- `CASHEW_*` vars from a running Hermes session override config defaults in tests
- `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc. causing unintended API calls
- Path vars that influence import resolution

**Fix pattern:** Add an autouse fixture in `conftest.py` that strips the leaking vars:

```python
@pytest.fixture(autouse=True)
def _clear_leaking_env_vars(monkeypatch: pytest.MonkeyPatch):
    for key in list(os.environ):
        if key.startswith("CASHEW_"):
            monkeypatch.delenv(key, raising=False)
```

Mirror the existing pattern already used by the project (e.g., `HF_HUB_OFFLINE=1` in conftest).

### Stale Package Metadata

`pip install -e .` installs entry point metadata that persists across source changes. If you change `pyproject.toml`'s entry point but don't reinstall, the old metadata is used:

```bash
# Check what's actually registered
python3 -c "import importlib.metadata as im; eps=list(im.entry_points(group='hermes_agent.plugins')); [print(f'{ep.name} = {ep.value}') for ep in eps]"
```

**Fix:** Update the installed entry point metadata directly, or reinstall:

```bash
# Option A: Patch the installed entry_points.txt
# Find the dist-info directory:
python3 -c "import importlib.metadata as im; d=im.distribution('your-package'); print(d._path)"
# Edit entry_points.txt in that directory

# Option B: Reinstall
pip install -e ".[dev]" --force-reinstall --no-deps
```

**Specific gotcha with entry point suffixed targets:** An entry point declared as `module.path` (without `:suffix`) resolves to a **module** via `ep.load()`. If declared as `module.path:function`, it resolves to the **function**. If you switch between these, any tests that call `ep.load()` and expect a particular type will break. On macOS, stale dist-info may retain the old format — always check with `python3 -c "import importlib.metadata as im; ..."` to see what's actually registered.

### Removed/Refactored Methods

After a major refactor, tests that reference old method names or monkeypatch old internals will fail:

```bash
# Check if the method still exists
python3 -c "from your_module import YourClass; print(hasattr(YourClass, 'old_method_name'))"
```

**Fix pattern:** Update the test to use the new API surface. If mocking internal methods, mock at the boundary instead (the public API or the dependency's interface).

### Immutable Types (Python 3.11+)

On modern Python, some C-level types (notably `sqlite3.Connection`) are immutable. `monkeypatch.setattr` appears to succeed but the teardown raises `TypeError`:

```python
# Detection: try to set a dummy attribute
try:
    sqlite3.Connection._test_mutability = lambda: None
    del sqlite3.Connection._test_mutability
except TypeError:
    # Immutable — can't use monkeypatch on this type
    pass
```

**Fix:** Detect immutability and adapt the test — either skip the mock and test the fallback path directly, or mock at a different level.

### Direct Dependency in PyPI Package

If `pyproject.toml` has a git+SHA pinned dependency (e.g., `package @ git+https://github.com/user/repo.git@abc123`), the PyPI publish step will reject the package with `400 Can't have direct dependency`. The build and wheel-smoke steps pass — only the upload fails.

**Fix:** Check if the dependency is available on PyPI. If yes, switch to a version specifier:
```
# Before (blocks PyPI):
"package @ git+https://github.com/user/repo.git@abc123"

# After:
"package>=1.0.0,<2.0.0"
```

## Step 5: Fix and Verify

1. Make the minimal fix
2. Run the failing test locally: `pytest -xvs tests/test_file.py::test_name`
3. Run the full test suite: `pytest`
4. Commit with conventional commit + DCO sign-off: `git commit -s -m "fix: description"`
5. Push: `git push`

## Step 6: Verify CI Passes

After pushing, **check CI status proactively** — don't wait for the user to tell you it's red:

```bash
# Wait for CI to start and complete
gh run watch <RUN_ID> --exit-status

# Or check status periodically
gh run list --limit 1 --json conclusion,status
```

If still red, go back to Step 1. Repeat until green.

## Step 7: Multiple Fixes, Multiple Commits

When fixing a series of related CI issues, use **one commit per root cause** — not one commit per test file, and definitely not one mega-commit. This keeps the history reviewable and makes it easy to revert individual fixes if needed.

Example from a real session:
```
fix: switch dependency from git+SHA to PyPI specifier         # unblocks release
fix: handle repr-style list env vars in config                # fixes config parsing
fix: align entry-point test with module-load contract          # fixes test gap
fix: update macos-fallback test for refactored retrieval       # fixes stale mock
```

Each commit is a single logical change, has its own DCO sign-off, and could stand alone.

## Step 8: Structural Release-Workflow Fixes

After fixing the immediate CI failure, consider whether the *workflow itself* has a structural gap that allowed the bad state to reach production (or PyPI).

### Gate Release Workflow Behind Tests

The most common gap: the release workflow runs on tag push but has **no dependency on the test workflow**. A broken tag can publish to PyPI.

**Fix pattern:** Add a `test` job as a prerequisite to `build` (and thus `publish-pypi`):

```yaml
jobs:
  test:
    name: Run tests
    runs-on: ubuntu-latest
    env:
      HF_HUB_OFFLINE: "1"
      # … any env vars your tests need
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install -e ".[dev]"
      - run: pytest -xvs

  build:
    name: Build distribution
    needs: test          # ← never build if tests fail
    # … rest of build steps

  publish-pypi:
    name: Publish to PyPI
    needs: build         # ← never publish if build fails
    if: contains(github.ref_name, '-') == false  # skip RC tags
    # … publish steps
```

### Add workflow_dispatch for Retries

Without `workflow_dispatch`, the only way to retry a failed release is to delete and recreate the tag — which rewrites history. Add a manual trigger:

```yaml
on:
  push:
    tags:
      - "v*"
  workflow_dispatch:     # ← manual retry button in the Actions tab
```

This lets you retry a failed publish without touching the tag. If the release process has a "publish to PyPI" step that depends on an environment with protection rules, `workflow_dispatch` will respect those rules on manual runs too.

### Tag-Delete-and-Recreate Cycle

If a release does fail and `workflow_dispatch` wasn't yet added (or the tag itself was pushed before the fix was in):

```bash
# Delete the broken tag
git tag -d vX.Y.Z
git push --delete origin vX.Y.Z

# Fix the issue, push the fix
git add …
git commit -s -m "fix: root cause"
git push

# Recreate the tag on the new HEAD
git tag vX.Y.Z
git push origin vX.Y.Z
```

This re-triggers the release workflow. Only do this for failed releases — never for successful ones (would unpublish the package if downstream consumers already depend on it).

## Quick Reference

| Step | Command |
|------|---------|
| Read CI logs | `gh run view <ID> --log-failed` |
| Run single test | `pytest -xvs tests/file.py::test_name` |
| Check pre-existing | `git stash && pytest ... && git stash pop` |
| Check installed entry point | `python3 -c "import importlib.metadata as im; ..."` |
| Full test suite | `pytest` |
| Commit + push | `git commit -s -m "fix: ..." && git push` |
| Watch CI | `gh run watch <ID> --exit-status` |
