---
name: systematic-debugging
description: >-
  4-phase root cause debugging protocol: understand bugs before fixing.
  Use for ANY technical issue — test failures, production bugs, unexpected
  behavior, performance problems, build failures, or integration issues.
  ESPECIALLY when under time pressure, when "one quick fix" seems obvious,
  or when previous fix attempts have failed.
license: MIT
compatibility: >-
  Platform-agnostic. Some sections cover macOS-specific sandbox debugging.
  Requires access to source code, version control (git), and testing tools
  appropriate to the project.
metadata:
  tags:
    - debugging
    - troubleshooting
    - problem-solving
    - root-cause
    - investigation
  source: >-
    Adapted from obra/superpowers (Jesse Vincent, MIT).
    Expanded with real-world debugging patterns from production use.
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**
- Issue seems simple (simple bugs have root causes too)
- You're in a hurry (rushing guarantees rework)
- Someone wants it fixed NOW (systematic is faster than thrashing)

## The Four Phases

Complete each phase before proceeding to the next.

---

## Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

### 1. Read Error Messages Carefully

- Don't skip past errors or warnings — they often contain the exact solution
- Read stack traces completely. Note line numbers, file paths, error codes
- **Action:** Read the relevant source files at the error locations and search the codebase for the error string to find all related code paths.

### 2. Reproduce Consistently

- Can you trigger it reliably? What are the exact steps?
- If not reproducible → gather more data, don't guess
- **Action:** Run the failing test or trigger the bug:

```bash
pytest tests/test_module.py::test_name -v --tb=long
```

### 3. Check Recent Changes

- What changed that could cause this? Git diff, recent commits, new dependencies, config changes
- **Action:**

```bash
git log --oneline -10
git diff
git log -p --follow src/problematic_file.py | head -100
```

### 4. Gather Evidence in Multi-Component Systems

**WHEN system has multiple components (API → service → database, CI → build → deploy):**

Add diagnostic instrumentation BEFORE proposing fixes. For EACH component boundary:
- Log what data enters the component
- Log what data exits the component
- Verify environment/config propagation
- Check state at each layer

Run once to gather evidence showing WHERE it breaks. THEN analyze to identify the failing component.

### 5a. Check Schema and Environment Divergence

**WHEN a bug reproduces in production but not in tests:**

1. Compare the test fixture schema against the production schema — `PRAGMA table_info()`, `\\.schema`, or equivalent
2. Look for missing NOT NULL columns, foreign keys, unique constraints, or defaults
3. Check for differences in SQLite journal mode, connection flags, or PRAGMA settings
4. Verify the test data matches production shape — not just column names but constraints

Simplified test schemas are a common source of hidden bugs. If the production table has `model TEXT NOT NULL` but the test table only has `vector BLOB`, a bug that only fires on NOT NULL violation will pass tests cleanly.

**Action:** Run `PRAGMA table_info(table_name)` against both databases side-by-side and diff the output.

### 5b. Check Exception Type Specificity in Fallback Chains

**WHEN a try/except fallback isn't catching the error you see in logs:**

```python
try:
    # Primary path — can raise OperationalError
    conn.execute("INSERT INTO t (model_name) VALUES (?)", ...)
except sqlite3.OperationalError:
    # Fallback — can raise IntegrityError (sibling, not child)
    conn.execute("INSERT INTO t (vector) VALUES (?)", ...)
```

`OperationalError` and `IntegrityError` are **siblings** — both inherit from `DatabaseError`, which inherits from `Error`. Catching one does NOT catch the other.

The fix is either:
- Catch the parent class (`except sqlite3.DatabaseError`) if both paths can fail with different subtypes
- Catch `Exception` as last resort (broader but safer than a gap)
- Handle each expected error type explicitly

### 5c. Progressive Characterization — Tool & API Behavior

**WHEN investigating a retrieval system, API, or knowledge graph that returns empty or inconsistent results:**

Start from what works and expand until it breaks. This isolates the variable causing failure.

| Input | Expected | Actual | Diagnosis |
|-------|----------|--------|-----------|
| Single known term (e.g. `python`) | Hits | Hits | Tool works, connection OK |
| Two-word phrase from same doc (`type safety`) | Hits | Hits | Short phrase retrieval works |
| Related two-word phrase (`generic types`) | Hits | 0 hits | **Boundary found** — issue is phrase-specific |
| Longer query with same terms | 0 hits | 0 hits | Confirms: not a fluke |

**Do NOT skip characterization:** Jumping straight to "the embedding model is broken" is guessing. The grid eliminates variables one at a time.

### 5d. Check Dependency Source Before Fixing Library Code

**WHEN you trace a bug into a third-party dependency:**

Before patching the library code, verify WHERE it's installed from:

```bash
pip show <package-name>
```

Key fields:
- **Editable project location** — If present, this is a `pip install -e` dev copy. Was this intentional?
- **Location** — Is it in site-packages (production) or a temp/dev directory?
- **Version** — Compare against latest on PyPI: `pip index versions <package-name>`

**The rule:** If the package is installed as an editable dev copy and you didn't put it there intentionally, STOP and ask. The symptom may be caused by code diverging from upstream — and the right fix is to switch to the production package, not to patch the fork.

**Example:** A background worker crashed with `table X has no column named Y`. Investigation traced it to an editable install from `/private/tmp/some-fork/`. A dev fork had added the column name to INSERT statements but never added the schema migration. The correct fix wasn't to add the migration to the fork — it was to switch to the production PyPI package and delete the dev copy.

### 6a. Research Before Guessing — Systematic Web Search

**WHEN you've gathered all local evidence but still don't understand the root cause:**

Do NOT guess solutions. Use structured web research:

1. **Search with the exact error message** — Quote the error, include error codes and function names
2. **Search with symptom + platform context** — Combine what broke + what OS/tool version
3. **Search with the component/service name** — XPC services, daemons, subsystems often have documented bugs
4. **Prioritize recent threads** — Filter for current versions. Old solutions may not apply
5. **Read the full thread** before proposing solutions — partial reading causes partial fixes
6. **Check for a confirmed workaround** at the thread's end, not just the initial diagnosis

### 6b. macOS App Troubleshooting — Sandboxed Applications

**WHEN debugging a macOS app (especially sandboxed ones like Books, Music, or App Store apps):**

The app is confined to a sandbox container under `~/Library/Containers/<bundle-id>/`.

#### Locate the Container

```bash
ls ~/Library/Containers/<bundle-id>/
# Data/Library/ — preferences, caches, databases
# Data/Documents/ — user-visible content, import queues
```

#### Check for an XPC Service Companion

Many Apple apps use a background XPC service for file operations:

```bash
# XPC services live in the framework bundle or app bundle:
/System/Library/PrivateFrameworks/<Framework>.framework/XPCServices/
/System/Applications/<App>.app/Contents/XPCServices/
ps aux | grep -i "<service-name>"
```

#### Read the Database Directly

Sandboxed apps often use SQLite/CoreData:

```bash
sqlite3 ~/Library/Containers/<bundle-id>/Data/Documents/<path>.sqlite ".tables"
sqlite3 ~/Library/Containers/<bundle-id>/Data/Documents/<path>.sqlite "SELECT * FROM ZTABLE LIMIT 10;"
```

#### Check System Logs

```bash
log show --predicate 'process == "AppName"' --last 10m --style compact
log stream --predicate 'process == "AppName"' --style compact
```

#### Reset TCC Permissions

If the app can't access files outside its sandbox (silent import failures):

```bash
tccutil reset All com.apple.bundle-id
```

#### Know the I/O Boundary

- **Security-scoped bookmarks** (from drag-drop or `open` command) are one-time-use. If the import fails, the bookmark is consumed and subsequent attempts fail silently.
- **NSOpenPanel** (File > Import dialog) creates fresh bookmarks — more reliable for testing.
- If `open -b bundle-id file.ext` works from Downloads but not Desktop, it's likely a TCC/tiered-access issue (macOS gives Downloads more permissive access).

#### Differentiate Local vs Cloud Sync Corruption

Container resets fix local state but NOT iCloud sync corruption. Signs of cloud issues:
- Problem persists after full container deletion and reinstall
- Import works once after restart then degrades
- Same issue across multiple devices

**Action:** If local reset doesn't fix it, the iCloud sync state may be corrupted. System Settings → Apple ID → iCloud → Manage Storage → [App] → Delete All Data is the nuclear option.

#### Recovery Options (in order of escalation)

1. Kill and restart the XPC service (`kill -9 <PID>`) — temporary, XPC respawns
2. Reset the app container (`rm -rf ~/Library/Containers/<bundle-id>/`)
3. Reset TCC permissions (`tccutil reset All <bundle-id>`)
4. Reboot the Mac
5. Delete iCloud data for the app
6. Create a test macOS user — if the app works there, it's your user library, not the system

### 6c. Trace Data Flow

**WHEN error is deep in the call stack:**

- Where does the bad value originate?
- What called this function with the bad value?
- Keep tracing upstream until you find the source
- Fix at the source, not at the symptom

**Action:** Search the codebase for function references and variable assignments to trace the data path.

### Phase 1 Completion Checklist

- [ ] Error messages fully read and understood
- [ ] Issue reproduced consistently
- [ ] Recent changes identified and reviewed
- [ ] Evidence gathered (logs, state, data flow)
- [ ] Problem isolated to specific component/code
- [ ] Root cause hypothesis formed

**STOP:** Do not proceed to Phase 2 until you understand WHY it's happening.

---

## Phase 2: Pattern Analysis

**Find the pattern before fixing:**

### 1. Find Working Examples

- Locate similar working code in the same codebase
- What works that's similar to what's broken?

### 2. Compare Against References

- If implementing a pattern, read the reference implementation COMPLETELY — don't skim
- Understand the pattern fully before applying

### 3. Identify Differences

- What's different between working and broken?
- List every difference, however small
- Don't assume "that can't matter"
- **Action:** Search the codebase for similar patterns to compare.

### 4. Understand Dependencies

- What other components does this need?
- What settings, config, environment?
- What assumptions does it make?

---

## Phase 3: Hypothesis and Testing

**Scientific method:**

### 1. Form a Single Hypothesis

- State clearly: "I think X is the root cause because Y"
- Write it down. Be specific, not vague.

### 2. Test Minimally

- Make the SMALLEST possible change to test the hypothesis
- One variable at a time
- Don't fix multiple things at once

### 3. Verify Before Continuing

- Did it work? → Phase 4
- Didn't work? → Form NEW hypothesis
- DON'T add more fixes on top

### 4. When You Don't Know

- Say "I don't understand X" — don't pretend to know
- Ask for help. Research more.

---

## Phase 4: Implementation

**Fix the root cause, not the symptom:**

### 1. Create Failing Test Case

- Simplest possible reproduction. Automated test if possible.
- MUST have before fixing.
- Test environment must mirror production — audit test fixtures against real schema.

### 2. Implement Single Fix

- Address the root cause identified. ONE change at a time.
- No "while I'm here" improvements. No bundled refactoring.

### 3. Verify Fix

```bash
# Run the specific regression test
pytest tests/test_module.py::test_name -v

# Run full suite — no regressions
pytest tests/ -q
```

### 4. If Fix Doesn't Work — The Rule of Three

- **STOP.**
- Count: How many fixes have you tried?
- If < 3: Return to Phase 1, re-analyze with new information
- **If ≥ 3: STOP and question the architecture (step 5 below)**
- DON'T attempt Fix #4 without architectural discussion

### 5. If 3+ Fixes Failed: Question Architecture

**Pattern indicating an architectural problem:**
- Each fix reveals new shared state/coupling in a different place
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere

**STOP and question fundamentals:**
- Is this pattern fundamentally sound?
- Are you "sticking with it through sheer inertia"?
- Should you refactor the architecture vs. continue fixing symptoms?

**Discuss before attempting more fixes.** This is NOT a failed hypothesis — this is a wrong architecture.

---

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals a new problem in a different place**

**ALL of these mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the architecture (Phase 4, step 5).

## Investigation Flow — Keep Forward Momentum

When the investigation is active and the user says things like "we made progress but we're not done":

Do NOT break flow by asking clarifying questions. Keep pushing — gather more evidence, try the next diagnostic step, check another angle. A paused investigation that asks "what happened when you tried X?" wastes the user's attention.

**Signals to keep pushing:**
- "we made progress but we're not done" — continue investigating
- User ignores a clarify question — they want action, not questions
- "ok" or "still broken" — try next step, don't ask for permission

**What to do instead:** Derive information from logs, databases, or file state — don't ask the user to be your instrumentation layer. Only ask questions when you genuinely cannot proceed without input AND you've exhausted all self-service options.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question the pattern. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence, trace data flow | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare, identify differences | Know what's different |
| **3. Hypothesis** | Form theory, test minimally, one variable at a time | Confirmed or new hypothesis |
| **4. Implementation** | Create regression test, fix root cause, verify | Bug resolved, all tests pass |

## References

- [references/dependency-source-example.md](references/dependency-source-example.md) — Worked example of detecting an editable dev fork that caused schema drift in a library dependency. Read when Phase 1 step 5d leads you to a third-party package as the suspected source of a bug.
- [references/macos-sandbox-debug-example.md](references/macos-sandbox-debug-example.md) — Complete walkthrough of debugging Apple Books.app import failures, demonstrating the macOS sandbox techniques from Phase 1 step 6b. Read when debugging a macOS sandboxed application.
