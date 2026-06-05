---
name: review-methodology
description: "Professional review methodology — code review, security audit, architectural review, and kanban swarm verification. References codify Google's code review standards, OWASP audit patterns, and architectural assessment frameworks."
version: 1.0.0
author: Hermes Agent community
license: MIT
metadata:
  hermes:
    tags: [review, code-review, security-audit, architecture-review, verification, quality]
    related_skills: [github-code-review, codebase-security-audit, systematic-debugging, requesting-code-review]
---

# Review Methodology

Professional review standards for code, security, architecture, and swarm output verification.

## Review Types

| Type | Reference | When to load |
|------|-----------|-------------|
| **Code review** | `references/code-review-standards.md` | Reviewing a PR or diff — 9 dimensions from Google's engineering practices plus project-specific conventions |
| **Security review** | `references/security-review.md` | Auditing for vulnerabilities — threat modeling, vulnerability classes, dependency analysis, supply chain |
| **Architectural review** | `references/architectural-review.md` | Evaluating design decisions — coupling/cohesion, scalability, data flow, abstraction boundaries |
| **Swarm gate** | `references/swarm-verification.md` | Evaluating swarm worker outputs — passing or blocking the kanban verifier gate |

## Templates

| Template | When to use |
|----------|-------------|
| `templates/code-review-response.md` | Writing a PR review with findings organized by severity |
| `templates/security-finding.md` | Documenting a security vulnerability with reproduction steps |
| `templates/swarm-verdict.md` | Passing or blocking the kanban verifier gate with evidence |

## The Review Mindset

Every review follows the same arc, regardless of type:

1. **Understand intent** — What is the change trying to achieve? Read the description, issue, or brief first.
2. **Assess correctness** — Does it achieve its stated goal? Start here before considering style or elegance.
3. **Assess quality** — Is it well-constructed for its purpose? Complexity, maintainability, test coverage.
4. **Assess risk** — What could go wrong? Edge cases, security, regressions, operational impact.
5. **Communicate** — Clear findings, severity levels, actionable next steps. Not personal, not dismissive.

Never skip to quality or style before understanding intent and correctness. A well-styled solution to the wrong problem is still wrong.
