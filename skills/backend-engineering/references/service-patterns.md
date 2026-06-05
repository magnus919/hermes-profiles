# Service Patterns

## Architecture Styles

| Style | Separation axis | Best for | Tradeoff |
|-------|----------------|----------|----------|
| Layered | Technical layer (controller → service → repository) | Simple CRUD services, convention-based frameworks | Business logic leaks across layers |
| Clean Architecture | Dependency direction (outer → inner) | Complex business logic, long-lived projects | Boilerplate for interfaces |
| Hexagonal (Ports & Adapters) | External vs internal (ports as boundaries) | Services with multiple I/O sources | More interfaces upfront |
| Pipeline | Request flow through stages | Data processing, middleware-heavy services | Composable but hard to trace |

## Request Lifecycle

```
Request → Middleware 1 → Middleware N → Router → Controller → Service → Repository → Database
                                             ↓
                                        Response ← Middleware N ← Middleware 1 ←
```

Each layer has a distinct responsibility:

| Layer | Responsibility | Doesn't do |
|-------|---------------|------------|
| Middleware | Auth, logging, rate limiting, CORS, tracing | Business logic, data access |
| Controller | Request parsing, validation, response formatting | Business decisions, database queries |
| Service | Business rules, workflow orchestration, state mgmt | HTTP concerns, direct database access |
| Repository | Data access, query construction, result mapping | Business rules, request parsing |

## Background Job Processing

| Pattern | When to use | Concerns |
|---------|-------------|----------|
| In-process worker | Lightweight, no external deps | Memory, process lifecycle, scaling |
| Message queue | Reliable async processing | Queue management, retry, DLQ |
| Scheduled cron | Periodic batch work | Timing guarantees, overlap |
| Event-driven streaming | Real-time event processing | State management, ordering |

Every background job should be: idempotent, retryable, and have a defined failure path (dead letter or alert).
