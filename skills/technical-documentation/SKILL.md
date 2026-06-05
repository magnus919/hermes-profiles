---
name: technical-documentation
description: "Technical documentation methodology — API reference documentation, README authorship, CLI help text design, agent-facing documentation (AGENTS.md), developer guides, and documentation site information architecture."
version: 1.0.0
author: Hermes Agent community
license: MIT
metadata:
  hermes:
    tags: [documentation, technical-writing, API-docs, README, developer-guides, information-architecture]
    related_skills: [editorial-methodology, copy-editor-methodology, artifact-pyramids]
---

# Technical Documentation Methodology

Technical documentation is the interface between a tool and its user. This methodology covers writing documentation that answers the reader's question, doesn't get in their way, and stays maintainable as the project evolves.

## The Technical Writer's Domain

| You own | You don't own |
|---------|--------------|
| API documentation — endpoint references, parameters, examples | Editorial and long-form narrative content — that's the writer |
| README authorship — project overview, quickstart, configuration | Brand messaging and marketing copy — that's the brand designer |
| CLI documentation — help text, usage patterns, exit codes | Code architecture decisions — those belong to the technical architect |
| Agent-facing docs — AGENTS.md, skill documentation | Project roadmap and product vision — that's the product manager |
| Reference documentation — config files, troubleshooting, architecture | Performance optimization guidance — that's the debugger/SRE |
| Documentation site structure — IA, cross-referencing, search | Code quality and standards — that's the reviewer/QA engineer |

## Reference Files

| Reference | When to load |
|-----------|-------------|
| `references/readme-patterns.md` | Writing or restructuring a README — sections every README needs, quickstart patterns, installation variants, configuration documentation |
| `references/api-documentation.md` | Documenting an API — endpoint structure, parameter tables, request/response examples, authentication, error handling |
| `references/agent-facing-docs.md` | Writing AGENTS.md and skill documentation — trigger patterns, loading order, output contracts, cross-references |
| `references/cli-help.md` | Designing CLI help text — usage line, flag documentation, exit codes, environment variables, examples section |
| `references/information-architecture.md` | Structuring a documentation site — progressive disclosure, cross-referencing, search optimization, maintenance strategy |

## Core Principles

**Document the interface, not the implementation** — Users need to know what a function does, what it expects, and what it returns. How it works internally is for the source code.

**Good docs answer the question the reader has** — Different readers come with different questions. Getting started? Reference? Troubleshooting? Structure docs to route each reader to their answer fast.

**Exhaustive completeness over narrative arc** — Technical docs are not articles. Readers skip to the part they need. Cover every parameter, every edge case, every error code. Don't skip the boring bits — those are the ones people need.

**Every doc is a liability** — Every page you write must be maintained. Prefer documenting less with more completeness over documenting everything with lower quality. Maintenance cost is proportional to surface area.

**Show, don't just tell** — Every concept needs a worked example. Every API endpoint needs a request and response. Every configuration option needs a complete example, not just a description.
