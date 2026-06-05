## Agent-Specific Checklist

When I (Jasper) make a contribution on behalf of Magnus:

- [ ] **CONTRIBUTING.md checked** at repository root (and fallback locations)
- [ ] **Existing issues searched** before filing anything new — on the current repo AND on any target repo before redirecting
- [ ] **Existing PRs checked** on the target repo too — the fix may already exist — on the current repo AND on any target repo before redirecting
- [ ] **Existing PRs checked** on the target repo too — the fix may already exist
- [ ] **For large changes:** discussed with maintainers before implementing
- [ ] **Agent disclosure** included in issue/PR body
- [ ] **PR/issue template compliance** — fetched project template (`.github/PULL_REQUEST_TEMPLATE.md` for PRs, `.github/ISSUE_TEMPLATE/` for issues), body matches required structure
- [ ] **PR compliance checker** — `check-pr-template-compliance.py` exits 0 before PR submission
- [ ] **Commits authored in the human contributor's name** (`git commit --author="Human Name <email>"` if the agent writes the code directly — but preferably the human writes/approves the commits)
- [ ] **Tests pass** before opening PR
- [ ] **No force-push** unless the project's contributing guide explicitly asks for rebased history
- [ ] **CI monitored** after PR submission, failures fixed promptly
- [ ] **Single issue per PR** — if a separate fix is discovered while a PR is open, create a NEW branch from main, new issue, and new PR. Do NOT push to the open PR's branch.
- [ ] **Review feedback addressed** — each comment gets a response or action

---