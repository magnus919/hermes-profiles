---
name: backend-engineering
description: "Backend engineering methodology — API implementation patterns (REST, gRPC, GraphQL), service architecture (clean/hexagonal/layered), database access patterns, integration and middleware design, error handling, and service-level testing. Language and framework agnostic."
version: 1.0.0
author: Hermes Agent community
license: MIT
metadata:
  hermes:
    tags: [backend, api, services, server, database, integration, middleware]
    related_skills: [technical-architect, data-engineering, platform-engineering, qa-methodology]
---

# Backend Engineering Methodology

Backend engineering is the craft of building the server-side systems that power applications — APIs, services, data access, integrations, and the runtime behavior that makes the architecture real. This methodology covers the implementation patterns between architecture design (technical-architect) and quality validation (reviewer).

## The Backend Engineer's Domain

| You own | You don't own |
|---------|--------------|
| API implementation — REST/gRPC/GraphQL endpoints, request validation, response formatting, error handling, middleware chains | API contract and service boundary design — that's the technical-architect |
| Service logic — business rules, workflow orchestration, state management, background job processing | Deployment pipeline and infrastructure — that's the platform-engineer |
| Database access patterns — query design, connection management, transaction boundaries, N+1 detection, pagination | Schema design and migrations — that's the data-architect / data-engineer |
| Integration code — third-party API clients, webhook handlers, message queue consumers/producers | Code review and quality gates — that's the reviewer |
| Observability instrumentation at the service level — structured logging, metrics, tracing hooks | Observability infrastructure — that's the SRE / platform-engineer |
| Service-level tests — unit tests for business logic, integration tests for API contracts | Test strategy and automation — that's the QA-engineer |

## Reference Files

| Reference | When to load |
|-----------|-------------|
| `references/api-patterns.md` | Designing or implementing API endpoints — resource modeling, versioning, pagination, error response formats, request validation |
| `references/service-patterns.md` | Structuring service logic — clean/hexagonal/layered architecture, dependency injection, middleware composition, request lifecycle, background jobs |
| `references/database-patterns.md` | Writing database access code — connection pooling, query optimization, N+1 detection, pagination strategies, transaction boundaries |
| `references/integration-patterns.md` | Integrating with external systems — retry with backoff, circuit breakers, idempotency keys, webhook verification, message queue consumers |
| `references/error-handling.md` | Handling errors systematically — classification (client vs server), structured responses, exception handling patterns, observability correlation |
| `references/testing.md` | Testing backend services — unit tests for business logic, integration tests for API contracts, contract tests for service boundaries |

## Core Principles

**The interface is the contract** — API boundaries are service-level contracts. Every endpoint signature, request schema, response format, and error code is a promise to consumers. Breaking changes are coordination problems, not version bumps.

**Business logic is the center of gravity** — Keep business rules isolated from framework concerns, transport protocols, and infrastructure details. A well-structured service can survive changes to its HTTP library, database driver, and deployment platform.

**Handle errors where they make sense** — Catch errors at the boundary where you have enough context to handle them meaningfully. Catch too early and you lose context. Catch too late and you can't recover.

**Design for failure, not just success** — Every external call can fail. Every database connection can drop. Every message can be duplicated. Idempotency, retry, and graceful degradation are not optimizations — they're requirements.

**Test at the right level** — Business logic gets unit tests. API contracts get integration tests. Service boundaries get contract tests. Each level catches a different class of failure.
