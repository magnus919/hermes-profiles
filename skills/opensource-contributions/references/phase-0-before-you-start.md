## Phase 0: Before You Do Anything

### Read CONTRIBUTING.md

This is a **hard gate**. Before planning any change, before writing a single line of code, before filing anything:

```bash
# Check common locations (run from the repo root)
for f in CONTRIBUTING.md .github/CONTRIBUTING.md docs/CONTRIBUTING.md CONTRIBUTING.rst; do
  if [ -f "$f" ]; then
    echo "=== Found: $f ==="
    cat "$f"
    break
  fi
done

# Also scan README for contributing sections
if grep -qi "contributing\|how to contribute\|getting started" README.md 2>/dev/null; then
  echo "=== README.md has contributing info ==="
  grep -n -A 5 -i "contributing\|how to contribute\|getting started" README.md
fi
```

**What you're looking for:**

| Thing to Check | Why It Matters |
|---|---|
| CLA / DCO requirements | Some projects require a signed Contributor License Agreement or Developer Certificate of Origin (`Signed-off-by:` in commit messages) |
| Commit message format | Projects like Angular, Linux, and many others enforce conventional commits or specific prefixes |
| PR template | May be auto-loaded via `.github/PULL_REQUEST_TEMPLATE.md` — fill it out completely |
| Issue templates | May exist in `.github/ISSUE_TEMPLATE/` — use the right one |
| Code style / linting | May require specific formatters (prettier, black, eslint, clang-format, etc.) |
| Testing requirements | Minimum test coverage, specific test framework, how to run tests |
| Branch naming | Some projects want `fix/description` or `bugfix/description` not `feat/desc` |
| Communication channels | Whether to discuss before filing (mailing list, Discord, forum) or just file the issue |
| Code of Conduct | Be aware of the CoC — you're expected to follow it |
| Sign-off required | `git commit -s` (Signed-off-by) may be mandatory for DCO compliance |

**If CONTRIBUTING.md exists, follow it to the letter.** It overrides everything below.

#### Extracting Structure from CONTRIBUTING.md

Read the whole file, then extract these specific answers. Having them in your working context makes the rest of the contribution process smoother:

1. **What's the project's priority order for contributions?** (e.g., bug fixes > cross-platform > security > features). Aim for the highest-priority category your contribution fits.
2. **Branch naming convention** — look for explicit patterns like `fix/description` or `feat/description`
3. **Commit message format** — do they require Conventional Commits? Specific scopes? `Signed-off-by` for DCO?
4. **How to set up a dev environment** — are there specific `uv`, `pip`, `npm`, `cargo` commands? `--recurse-submodules` on clone?
5. **How to run tests** — is there a specific script (`scripts/run_tests.sh`) or framework?
6. **Code style / linting** — any formatters, linters, or style rules to apply before PR?
7. **PR description expectations** — any specific template, sections, or information they want?
8. **Architecture context** — does the document explain where different types of changes go? (tools vs skills, etc.)
9. **Cross-platform considerations** — any platform-specific rules your change needs to follow?
10. **Communication channels** — Discord, mailing list, or GitHub Discussions for pre-PR discussion?
11. **CLA / DCO / License** — do you need to sign anything? What license are you contributing under?
12. **Security reporting process** — if your contribution has security implications, where do they go?

For a worked example of extracting these from a real CONTRIBUTING.md, see the reference file `references/hermes-agent-contributing-case-study.md`.

### Check Existing Issues and Discussions

Before filing anything new:

```bash
# Check issues on the current repo
gh issue list --search "keywords related to your issue" --state all --limit 10
# Or for a broader search
gh issue list --search "your topic in:title" --state all --limit 10
```

Also check open and recently closed PRs — someone may already be working on a fix:

```bash
# Check PRs on the current repo
gh pr list --search "keywords" --state all --limit 10
```

### Finding Good Bugfix Candidates (When You Want to Fix, Not File)

When you're looking for a bug to fix rather than filing a new issue, the selection process has its own heuristics. A poor candidate wastes maintainer time and your effort.

#### Systematic Triage

```bash
gh issue list --repo owner/repo --state open --label bug --limit 50 \
  --json number,title,labels,updatedAt
```

#### Filter Out Blocked Issues

| Red flag | What it means |
|----------|---------------|
| `NeedsUserFeedback` / `needs info` | Blocked on reporter — can't reproduce |
| `NeedsTriage` / `untriaged` | Not yet evaluated — may be invalid |
| `DifficultToImplement` / `complex` | Maintainer flagged high difficulty |
| `Upstream` / `external` | Bug is in a dependency, not fixable here |
| `Won't fix` / `out of scope` | Project has decided not to address |

Cleanest candidates have only `bug` (plus maybe a feature-area tag).

#### Check for Existing PRs

```bash
gh pr list --repo owner/repo --state all --search "ISSUE_NUMBER in:body" \
  --json number,title,state
```

#### Read Every Comment

Comments are the richest signal:
- **Positive:** maintainer isolated root cause, created reproduction, said "should be fixed"
- **Negative:** "not obvious," "won't fix," scope ballooned during discussion
- **Free issue:** someone volunteered but never followed up

#### Find Related Issues

After settling on a candidate, search for duplicates. A closed issue with "can't fix this" is a strong risk signal:

```bash
gh issue list --repo owner/repo --state all \
  --search '"keyword1" OR "keyword2" in:title,body' \
  --json number,title,state
```

#### Reproduce in a Clean Environment

Before writing fix code, confirm the bug in an isolated environment:

```bash
docker run --rm -v "$(pwd)/test-site:/site" -w /site \
  PROJECT_IMAGE:latest --gc --cleanDestinationDir
```

#### Decision Matrix

| Criterion | Good | Bad |
|-----------|------|-----|
| Label | Bug only | NeedsUserFeedback, Upstream, DifficultToImplement |
| PRs | None open | Open PR exists |
| Reproduction | Has steps or test repo | Vague or missing |
| Maintainer signal | "Should be fixed" | "Not obvious" |
| Code scope | Single package, isolated | Cross-cutting, architectural |

For a worked example with real command output (50+ issues triaged on gohugoio/hugo), see the `hugo-contrib` skill's `references/finding-bugfix-candidates.md`.

### Filtering Idea Lists Against Repo Reality: Ideation-to-Issue Gap Assessment

When a brainstorm or ideation session produces a list of improvement ideas (especially from `/ideation` or `/council`), the natural next step is to file issues. But generic ideas often don't fit a specific repo. Filing unfit issues wastes maintainer attention and clutters the tracker.

**The pre-filing filter:** Before any issue is filed, cross-reference each idea against the repo's actual state. See `references/contribution-idea-filtering.md` for the full methodology — a decision matrix mapping repo attributes (Docker presence, Renovate config, existing PR volume, stale branches, CI setup, etc.) to which idea categories are actionable vs. premature.

Quick decision table (full version in the reference):

| Repo has | Relevant ideas | Premature |
|----------|---------------|-----------|
| No CI/CD, no Docker, no Renovate | SKILL.md compliance, issue/PR templates, dependency drift | PR size gate, Docker health, Renovate auditor |
| CI but no PRs yet | SKILL.md compliance, templates, PR size gate | PR gardener (nothing to garden yet) |
| Active PRs but no stale-branch policy | All of the above + branch archiver | — |

This step sits between "ideation output exists" and "Phase 1: Filing Issues."

### Verify Before Redirecting

When you identify that an issue belongs in a **different project** (e.g., a core bug that's really a documentation concern, a backend issue that's actually a frontend problem, a feature request that should be an integration library), the natural instinct is to redirect: "you should file this over there." **Resist the redirect impulse until you verify the target repo.**

Always check the target repo's issue tracker **and** open/closed PRs first:

```bash
# Check target repo for existing issues on the topic
gh issue list --repo owner/target-repo --state all --search "topic keywords" --limit 10

# Check target repo for existing PRs that may already fix it
gh pr list --repo owner/target-repo --state all --search "topic keywords" --limit 10
```

If the fix already exists as an open PR on the target repo, the best contribution is to update the original issue with a link to that PR — not to file another one. This applies equally to documentation, code, and configuration repos.

**Real example:** The Home Assistant fritz integration had 19+ comments from users hitting an auth failure after repeater firmware updates. The core repo couldn't fix it — it was a docs gap. The natural response would be "file this on home-assistant.io." But someone had already opened PR #45402 on the docs repo with the exact troubleshooting note. The right action was linking the core issue to the existing docs PR, not asking for another issue to be filed.

**Exception:** If a thorough search turns up nothing on the target repo *and* the maintainer has explicitly asked someone to address it (e.g., "do you mind editing the docs?"), then filing a new issue or PR on the target repo is the correct next step.

### Verify Before Redirecting

When you identify that an issue belongs in a **different project** (e.g., a core bug that's really a documentation concern, a backend issue that's actually a frontend problem, a feature request that should be an integration library), the natural instinct is to redirect: "you should file this over there." **Resist the redirect impulse until you verify the target repo.**

Always check the target repo's issue tracker **and** open/closed PRs first:

```bash
# Check target repo for existing issues on the topic
gh issue list --repo owner/target-repo --state all --search "topic keywords" --limit 10

# Check target repo for existing PRs that may already fix it
gh pr list --repo owner/target-repo --state all --search "topic keywords" --limit 10
```

If the fix already exists as an open PR on the target repo, the best contribution is to update the original issue with a link to that PR — not to file another one. This applies equally to documentation, code, and configuration repos.

**Real example:** The Home Assistant fritz integration had 19+ comments from users hitting an auth failure after repeater firmware updates. The core repo couldn't fix it — it was a docs gap. The natural response would be "file this on home-assistant.io." But someone had already opened PR #45402 on the docs repo with the exact troubleshooting note. The right action was linking the core issue to the existing docs PR, not asking for another issue to be filed.

**Exception:** If a thorough search turns up nothing on the target repo *and* the maintainer has explicitly asked someone to address it (e.g., "do you mind editing the docs?"), then filing a new issue or PR on the target repo is the correct next step.

### For Large Changes: Discuss First

If your change is more than a few hundred lines, touches architecture, or adds significant new features:

1. Open a **discussion** or **issue** first, describing what you want to do and why
2. Wait for maintainer feedback before implementing
3. This prevents wasted work if the maintainers have a different vision

**Read the room on feature requests.** If maintainers have already discussed a feature and deferred it with explicit reasoning (e.g., "we need to see adoption before embedding a template"), a PR implementing it directly is unlikely to be accepted even if the implementation is clean. In that situation, the more effective contribution is the one the maintainers asked for: a documented working example the community can use and build adoption around. The embedded PR can come later once adoption is compelling.

The exception: trivial bugfixes (one-liner typos, obvious logic errors). Just fix and PR.

---