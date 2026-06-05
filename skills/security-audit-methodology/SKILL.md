---
name: security-audit-methodology
description: "Security audit and vulnerability assessment methodology — threat modeling, vulnerability classification, defense-in-depth review, dependency analysis, and security architecture evaluation. Grounded in OWASP, CWE, and STRIDE/LINDDUN frameworks."
version: 1.0.0
author: Hermes Agent community
license: MIT
metadata:
  hermes:
    tags: [security, audit, vulnerability, threat-modeling, OWASP, penetration-testing]
    related_skills: [review-methodology, systematic-debugging, codebase-security-audit]
---

# Security Audit Methodology

Security is not a checklist — it's a posture. This methodology covers systematic evaluation of code, architecture, dependencies, and operational practices for security weaknesses.

## The Security Engineer's Domain

| You own | You don't own |
|---------|--------------|
| Threat modeling — STRIDE, attack trees, trust boundaries | General code review — that's the reviewer |
| Vulnerability assessment — classification, severity, reproduction | Performance analysis — that's the debugger |
| Security architecture review — authn/authz, data flow, secrets management | Operational reliability — that's SRE |
| Dependency analysis — supply chain, known vulnerabilities, license risk | Compliance certification — that's legal |
| Security testing guidance — fuzzing, SAST/DAST integration | Incident response execution — that's SRE/on-call |

## Reference Files

| Reference | When to load |
|-----------|-------------|
| `references/threat-modeling.md` | Evaluating a system's attack surface — STRIDE per component, trust boundaries, data flow analysis |
| `references/vulnerability-classification.md` | Assessing a finding — CVSS scoring, CWE mapping, severity triage, exploitability assessment |
| `references/security-architecture.md` | Reviewing authn/authz, secrets management, encryption, network segmentation, and secure defaults |
| `references/dependency-audit.md` | Checking supply chain risk — known CVEs, license compatibility, maintenance health, transitive dependency risk |
| `references/testing-and-tooling.md` | Recommending SAST/DAST tools, fuzzing strategies, and security test patterns |

## Core Principles

**Trust nothing, verify everything** — Every input, every boundary, every assumption is a potential attack surface. Default deny, explicit allow.

**Defense in depth** — No single control is sufficient. Authentication without rate limiting, encryption without key management, input validation without output encoding — each is a vulnerability waiting to chain.

**Least privilege** — Every component, every user, every process should have exactly the permissions it needs and no more. Over-privilege is the most common security debt.

**Understand the attacker's perspective** — The question isn't "can this be exploited?" It's "how would an attacker think about this system?" Model their incentives, constraints, and capabilities.

**Fix the class, not the instance** — One SQL injection means you need parameterized queries everywhere, not just at that one endpoint. A single XSS means review the entire rendering pipeline.
