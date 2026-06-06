# Gate Criteria — Contribution Pipeline

Every gate must be falsifiable — there must exist a concrete condition that causes the gate to FAIL. An LLM self-assessing "I understand" is not a gate. A reproduction script that doesn't produce the bug is a gate.

---

## P0 → P1: Orientation Gate

**Criterion:** Can you describe what maintainers ACTUALLY enforce, with evidence?

**Passes when:**
- 8-field project fingerprint is complete (not missing fields)
- Each convention claim is backed by at least one merged PR example
- Discrepancies between CONTRIBUTING.md promises and merged-PR reality are explicitly noted
- AI contribution policy is identified (welcome / disclose-required / banned / unknown)
- SECURITY.md disclosure contact is identified (if present)

**Fails when:**
- Fingerprint is missing fields (e.g., "test framework: unknown" with no investigation)
- Claim conflicts with a merged PR without explanation
- AI policy says "banned" or "human-only" → HARD STOP
- Issue is closed, a discussion, or already has an open PR → HARD STOP

**Falsification test:** Pick a random merged PR from the last 30 days. Does the fingerprint correctly predict the conventions that PR followed? If not, the fingerprint is incomplete.

---

## P1 → P2: Comprehension Gate

**Criterion:** Does the reproduction script produce a FAIL on the target branch?

**Passes when:**
- Reproduction script runs to completion on a clean checkout of the target branch
- Script produces a FAIL (exit code non-zero, or assertion failure matching the issue description)
- Root-cause statement is specific: names the file, line number, and condition
- Code path trace is complete: entry point → intermediate calls → bug site
- Baseline test pass/fail counts are recorded (for comparison at P3)
- Bug classification is correct (Bug / Feature / Design / Config / Support)

**Fails when:**
- Reproduction script passes on clean checkout → bug not understood, or not reproducible
- Root-cause statement is vague ("something is wrong with the caching layer")
- Code path trace has gaps ("... then some middleware runs ...")
- Bug is non-deterministic and failure rate <10% after 100 attempts → document, escalate
- Issue is actually a design discussion → classify and stop
- Cannot reproduce after 2 honest attempts → stop, file "could not reproduce" comment

**Falsification test:** Hand the reproduction script to someone who hasn't read the issue. Can they run it and see the bug? If the script requires implicit knowledge, the gate fails.

---

## P2 → P3: Implementation Gate

**Criterion:** `git stash && cleanroom test run` produces green suite + test quality scorecard ≥6/8.

**Passes when:**
- All pre-existing tests pass (no regressions)
- New tests pass and are verified NOT change-detectors:
  - Test fails on unmodified branch (proven mechanically)
  - Assertion Relevance Scan passes (zero private access, zero internal mocks, zero mock call-counts)
  - Intent-annotated coverage is present
  - Scorecard ≥6/8
- Linter produces zero NEW violations (project's existing lint baseline is excluded)
- Code follows conventions documented in the project fingerprint

**Fails when:**
- Any pre-existing test fails → regression introduced
- Test passes on unmodified branch → tautological test, not testing the fix
- Scorecard <6/8 → test quality insufficient
- New linter violations introduced
- Code violates a convention from the project fingerprint

**Scorecard (8 points, binary PASS/FAIL each, ≥6 required):**

| # | Criterion | How Verified |
|---|---|---|
| 1 | No private attribute access in test assertions | AST scan for `._`, `.__` in test files |
| 2 | No internal mock assertions (mock.call_count, mock.assert_called_with on internals) | AST scan for mock assertion patterns |
| 3 | One assertion per logical concept (not 15 asserts testing the same thing) | Heuristic: >5 assertions on same object flags |
| 4 | Realistic inputs (not "test", "", 0, None for everything) | Input diversity check: unique values / total inputs >0.5 |
| 5 | Round-trip or invariant assertion present (not just "returns expected value") | Pattern match: assert x == constant is NOT round-trip |
| 6 | No conditional assertions (`if` inside test) | AST scan |
| 7 | Error cases have named tests (test_raises_*, test_fails_on_*) | Filename/test-name pattern match |
| 8 | No mock of module under test | AST scan for `@mock.patch('module_under_test.')` |

**Falsification test:** Delete the fix (revert to target branch). Do all new tests fail? If any new test passes without the fix, it's a change-detector.

---

## P3 → P3.5: Verification Gate

**Criterion:** All checks pass cleanly in isolation. No pre-existing failures attributed.

**Passes when:**
- Full test suite passes in isolated environment (Docker/VM/Nix/CI-runner)
- Linter passes with zero new violations
- Build succeeds
- P3 results compared against P1 baseline: no new failures introduced
- CI divergence report is generated (MATCH/PARTIAL/MISMATCH/UNKNOWN)

**Fails when:**
- Any test failure in isolated environment → roll back to P1
- Build failure in isolated environment → roll back to P1
- New linter violations → fix and re-run
- Environment setup takes >10 minutes → report what was verified, flag what wasn't

**Falsification test:** Run the same tests on a different OS or architecture. Do the results diverge? If so, the verification environment was incomplete — surface this in the CI divergence report.

---

## P3.5 → P4: Security Gate

**Criterion:** Zero critical/high static analysis findings. Zero secrets detected.

**Passes when:**
- semgrep scan: zero ERROR severity findings
- Secrets scan: zero findings
- Dependency check: no typo-squatted or brand-new packages
- All MEDIUM/LOW findings are logged and attached to PR

**Fails when:**
- Any ERROR finding → block PR, classify (CRITICAL → private disclosure; HIGH → fix before PR)
- Any secret detected → HARD STOP, do not create public PR
- New dependency is typo-squatted (<30 days old, name differs from popular package by 1-2 chars) → block

**Falsification test:** Insert a known secret pattern (`AWS_KEY=AKIA...`) into the diff. Does the scan catch it? If not, the scan is misconfigured.

---

## P4: PR Creation Gate

**Criterion:** PR is open, template is filled, CI passes, SLA is disclosed.

**Passes when:**
- PR is created (not draft — unless flagged for security review)
- Project's PR template is used (exact headers, exact checkboxes — verified against template)
- Conventional Commit message(s) follow project convention
- CI is green on the PR branch
- SLA disclosure is in the PR body
- Mermaid diagram is included (if change crosses complexity threshold)
- Agent disclosure is at the bottom of the PR body

**Fails when:**
- Template headers don't match project template (caught by compliance checker)
- CI is red → fix before marking ready
- Commit format doesn't match project convention
- SLA disclosure is missing or aspirational ("24h response" when agent doesn't run continuously)

**Falsification test:** Can a maintainer understand the change, the rationale, the testing methodology, and the expected response cadence from the PR body alone — without reading the diff?
