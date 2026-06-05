# Code Review Standards

Based on Google's engineering practices, adapted for the Hermes codebase and Magnus's Python/JS/Go projects.

## The Nine Dimensions

Every code review evaluates across these dimensions, in this priority order.

### 1. Design — The most critical aspect

**What to check:**
- Does the overall design make sense for this problem?
- Do interactions between components work well together?
- Should this change live in the current codebase or as a separate library?
- Does it integrate well with existing systems?
- Is now the right time to add this functionality?

**Red flags:**
- Design solves a problem that doesn't exist yet (future-proofing that adds complexity)
- Design duplicates existing functionality
- Design introduces a new pattern where existing conventions would work
- Design couples components that should be independent

### 2. Functionality — Does it actually work?

**What to check:**
- Does the change achieve its stated intent? (Read the issue/description first)
- Is the intent good for the users? (Both end-users AND future developers)
- **Edge cases** — What happens on empty input, null values, network failures, concurrent access?
- **Error handling** — Are errors caught at the right level? Are they recoverable or fatal?
- **Concurrency** — Deadlocks, race conditions, thread safety

**Red flags:**
- Error messages are swallowed with `except: pass`
- No handling for obvious edge cases (empty list, missing key, type mismatch)
- Concurrency model that makes race conditions likely (shared mutable state without locks)

### 3. Complexity — Is it harder than it needs to be?

**What to check at every level** — lines, functions, classes, modules:
- Can this code be understood quickly by someone who hasn't seen it before?
- Would a future developer be likely to introduce bugs when calling or modifying it?
- Is the solution the simplest that works, or does it over-engineer?

**Over-engineering signals:**
- Abstract interfaces with one implementation (YAGNI violation)
- Configurability for cases that don't exist yet
- Generic patterns applied where a simple solution works
- Inheritance hierarchies where a single function would do

**The rule:** Solve the problem you know needs to be solved now, not the problem you speculate might need to be solved in the future.

### 4. Tests — Is the change verifiable?

**What to check:**
- Unit, integration, or E2E tests as appropriate for the change
- Tests in the same CL as production code (except emergencies)
- **Will tests actually fail when the code is broken?** (Positive test for known failure modes)
- **Will tests produce false positives?** (Fragile tests that break on unrelated changes)
- Are assertions simple and meaningful?
- Are tests well-separated across different test methods?

**Red flags:**
- Tests that never run (no CI integration, skipped tests)
- Tests that assert the wrong thing (testing implementation, not behavior)
- Tests that are more complex than the code they test
- No tests for bug fixes (regression coverage missing)

### 5. Naming — Is intent clear from names alone?

**What to check:**
- Do names communicate *why* something exists, not just *what* it is?
- Are names reasonably concise without being cryptic?
- Do function names describe what they do (verb + object pattern)?
- Do variable names describe their content, not their type?

**Red flags:**
- Single-letter variables outside loops
- Names that lie about what the code does
- Abbreviations that aren't standard in the project
- Hungarian notation in Python/JS

### 6. Comments — Why, not what

**What to check:**
- Comments explain *why* code exists, not *what* it does (code should be self-documenting)
- Exceptions: complex regex, algorithms with non-obvious logic
- Comments contain information the code cannot convey itself (design rationale, tradeoffs)
- TODO comments have associated issues or clear owners
- No commented-out code

**Red flags:**
- `# This line adds 1 to x` style comments (state the obvious)
- No comment on a non-obvious decision that reviewers will question
- Old comments that no longer match what the code does (stale documentation)

### 7. Style — Conventions matter

**What to check:**
- Follow the project's style guide (if one exists). For Python: PEP 8. For Hermes: ruff config.
- Prefer the project's existing patterns over personal preferences
- Use "Nit:" prefix for non-blocking style suggestions
- Keep style-only changes in separate CLs from functional changes

**Red flags:**
- Reformatted entire files in the same PR as logic changes
- Inconsistent style within the same file or module

### 8. Consistency — The codebase should feel like one person wrote it

**What to check:**
- Does this change follow the patterns established in nearby code?
- If the established pattern violates the style guide, favor the style guide
- If there's no style guide rule and no established pattern, follow standard language idioms

**Red flags:**
- New code using a different approach than existing code doing the same thing
- Import style different from rest of project
- Error handling pattern different from rest of codebase

### 9. Documentation — Does the change update docs?

**What to check:**
- If the CL changes build, test, deploy, or release processes → docs updated
- If the CL changes API behavior → docs updated
- If the CL adds or changes CLI flags → help text and examples updated
- If code is deleted → related documentation removed

## The Severity Scale

| Severity | Label | Meaning | Action |
|----------|-------|---------|--------|
| 🔴 Critical | `blocking` | Bug, security issue, or correctness problem | Must fix before merge |
| 🟡 Warning | `should-fix` | Design issue, test gap, complexity concern | Should fix but can discuss |
| 💡 Suggestion | `nit` | Style preference, minor improvement | Can be ignored but consider |
| ❓ Question | `question` | I don't understand this code path | Author should clarify |

## Magnus-Specific Conventions

These stack on top of the general standards above:

- **Em-dashes in prose strings**: Zero allowed. Flag as blocking for user-facing text.
- **`except Exception` with no logging**: Flag as should-fix. Silent failures are debugging nightmares.
- **Bare `except:` without exception type**: Flag as critical. Catches `KeyboardInterrupt` and `SystemExit`.
- **Hardcoded paths** (`/Users/magnus/`, `/home/`, absolute paths): Flag as blocking — won't work on other machines.
- **API keys or tokens in code**: Flag as critical — credential leak.
- **Inline `color`/`background-color` styles in HTML templates**: Flag as should-fix — dark-mode artifacts.
- **Tests that don't assert anything**: Flag as should-fix — dead tests.
- **Type hints missing on new public functions**: Flag as suggestion — Magnus prefers typed Python.
