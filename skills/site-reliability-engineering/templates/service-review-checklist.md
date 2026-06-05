# Pre-Launch Reliability Review Checklist

> **Service:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
> **Owner:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
> **Review Date:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
> **Reviewer(s):** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
> **Target Launch:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

## Instructions

Check each item as **Pass**, **Fail**, **N/A**, or **Warn** (requires documented exception). All **Fail** and **Warn** items must have an action item and owner listed in the Action Items section at the end. A service may not launch with any unchecked **Fail** items.

| Status | Meaning |
| ------ | ------- |
| [P]    | Pass — item verified and meets standards |
| [F]    | Fail — blocker; must be resolved before launch |
| [W]    | Warn — acceptable with documented exception/risk |
| [-]    | N/A — not applicable to this service |

---

## 1. Service Design

### 1.1 Architecture Review

- [ ] [\_] Architecture diagram is documented and up to date (components, data flow, network boundaries)
- [ ] [\_] Architecture has been reviewed by a senior engineer or SRE
- [ ] [\_] Single points of failure (SPOF) have been identified and documented
- [ ] [\_] Service is stateless or state is externalized (database, cache, object store)
- [ ] [\_] Stateful components have a clear durability and replication strategy
- [ ] [\_] Database schema includes indexes for query patterns; no full-table scans on critical paths
- [ ] [\_] External integration points are abstracted behind interfaces (no hard coupling)
- [ ] [\_] Protocol/API versioning strategy is defined (backward-compatible by default)

### 1.2 Failure Modes

- [ ] [\_] A failure modes analysis (FMEA / fault tree) has been performed
- [ ] [\_] Each failure mode has a documented blast radius and mitigation
- [ ] [\_] Crash-only / fail-fast behavior is verified — no silent corruption on partial failure
- [ ] [\_] Partial failure of downstream dependencies does not cascade to the whole service
- [ ] [\_] Startup/shutdown ordering is defined for multi-component services

### 1.3 Dependency Map

- [ ] [\_] All internal and external dependencies are inventoried (services, libraries, APIs, data stores)
- [ ] [\_] Each dependency is classified by criticality: critical, important, or nice-to-have
- [ ] [\_] Critical dependencies have a defined degradation mode when unavailable
- [ ] [\_] Network latency / bandwidth requirements for each dependency are known
- [ ] [\_] Dependency version pinning and update cadence is defined

---

## 2. Resilience

### 2.1 Retry & Backoff

- [ ] [\_] Transient-failure retry logic is implemented with **exponential backoff and jitter**
- [ ] [\_] Retry budgets / caps are defined (max retries, total time window)
- [ ] [\_] Retries do not amplify load on degraded downstream services (client-side shedding)
- [ ] [\_] Idempotency keys are used for mutating operations across retries
- [ ] [\_] Retries on network errors are separated from retries on application-level errors

### 2.2 Circuit Breakers

- [ ] [\_] Circuit breaker pattern is implemented for all remote / downstream calls
- [ ] [\_] Thresholds (error rate, latency, concurrency) are tuned and documented
- [ ] [\_] Half-open recovery probes are configured (test a single request before closing)
- [ ] [\_] Circuit breaker state transitions are observable (metrics, events, logs)

### 2.3 Bulkheads

- [ ] [\_] Resource pools (thread pools, connection pools, memory arenas) are partitioned by workload
- [ ] [\_] No single tenant / user / request can exhaust shared resources
- [ ] [\_] Per-customer or per-feature resource quotas are enforced
- [ ] [\_] Connection pool sizes are tuned and documented per dependency

### 2.4 Graceful Degradation

- [ ] [\_] Fallback behavior is defined for each non-critical dependency failure
- [ ] [\_] Degraded mode is observable (logged, metered, and surfaced in status endpoints)
- [ ] [\_] Static / cached responses are served when live data is unavailable (if acceptable)
- [ ] [\_] Feature flags allow disabling non-critical functionality at runtime
- [ ] [\_] Rate limiting is implemented at the appropriate layer (ingress, per-tenant, per-endpoint)

---

## 3. Observability

### 3.1 Metrics

- [ ] [\_] RED metrics (Rate, Errors, Duration) are collected for every endpoint / operation
- [ ] [\_] USE metrics (Utilization, Saturation, Errors) are collected for every resource
- [ ] [\_] Business / application-level metrics are defined (throughput, conversions, queue depth)
- [ ] [\_] Metrics are tagged with meaningful dimensions (service, version, region, tenant)
- [ ] [\_] Custom metrics are within the cardinality budget for the metrics backend
- [ ] [\_] Health check endpoints (`/healthz`, `/readyz`, `/livez`) are implemented and distinct

### 3.2 Logging

- [ ] [\_] Structured logging (JSON) is used — machine-parseable with consistent schema
- [ ] [\_] Log levels (debug, info, warn, error) are used consistently and without noise
- [ ] [\_] Request IDs / trace IDs are propagated through all components and logs
- [ ] [\_] Sensitive data (PII, credentials, tokens) is never logged
- [ ] [\_] Error logs include stack traces and contextual metadata
- [ ] [\_] Log retention and archival policy is defined

### 3.3 Distributed Tracing

- [ ] [\_] Traces are emitted for all service-to-service calls
- [ ] [\_] Trace sampling strategy is defined (head-based, tail-based, or rate-based)
- [ ] [\_] Critical user journeys are identifiable by trace attributes
- [ ] [\_] gRPC / HTTP middleware for trace propagation is instrumented

### 3.4 Dashboards

- [ ] [\_] **Service overview dashboard** exists (RED metrics, saturation, error budget)
- [ ] [\_] **Dependency health dashboard** exists (upstream/downstream latency and errors)
- [ ] [\_] **Resource dashboard** exists (CPU, memory, disk, network, connections)
- [ ] [\_] Dashboards have meaningful time ranges, annotations, and thresholds
- [ ] [\_] Dashboards are shared with the owning team and documented in the runbook

### 3.5 Alert Rules

- [ ] [\_] Alerts exist for: error budget burn rate, high latency, high error rate, saturation
- [ ] [\_] Alerts use multi-window / multi-condition evaluation to reduce flapping
- [ ] [\_] Page-worthy alerts are well-separated from low-severity warnings
- [ ] [\_] Alert thresholds are calibrated to generate actionable notifications (not noise)
- [ ] [\_] Each alert has a documented runbook link and a clear remediation step

---

## 4. Capacity

- [ ] [\_] Traffic estimates are documented (peak QPS, data volume, concurrent connections)
- [ ] [\_] Scaling plan is defined: horizontal (stateless tier) and vertical (stateful tier)
- [ ] [\_] Auto-scaling policies are configured with min/max bounds and cooldown periods
- [ ] [\_] Resource limits (CPU, memory, disk, connections) are set per container / process
- [ ] [\_] Load testing results demonstrate capacity for 2×-3× peak estimated traffic
- [ ] [\_] Database connection pooling and max connections are configured
- [ ] [\_] Downstream dependency rate limits are known and not exceeded at peak
- [ ] [\_] Storage growth rate is projected; capacity alerts exist for 80% / 90% thresholds
- [ ] [\_] Cold-start / warm-up time is measured; prewarming strategy is defined if needed

---

## 5. Release

### 5.1 CI/CD Pipeline

- [ ] [\_] CI pipeline runs linting, unit tests, integration tests, and security scans
- [ ] [\_] CD pipeline is fully automated (no manual steps for standard releases)
- [ ] [\_] Artifacts are immutable (versioned, checksummed, stored in artifact registry)
- [ ] [\_] Infrastructure changes are codified (IaC — Terraform, Pulumi, CloudFormation, etc.)
- [ ] [\_] Database migrations are automated, reversible, and tested in CI

### 5.2 Rollback Plan

- [ ] [\_] Rollback procedure is documented and tested
- [ ] [\_] Rollback target is a known-good previous version (not a rebuild from scratch)
- [ ] [\_] Database schema changes are backward-compatible for at least one release cycle
- [ ] [\_] Rollback success criteria are defined (e.g., error rate returns to baseline)
- [ ] [\_] Rollback time target is documented (e.g., < 15 minutes from decision)

### 5.3 Canary Strategy

- [ ] [\_] Canary / progressive delivery process is defined
- [ ] [\_] Canary metrics and success criteria are defined (error rate, latency, error budget)
- [ ] [\_] Automatic rollback on canary failure is configured
- [ ] [\_] Traffic shifting is gradual (e.g., 1% → 5% → 25% → 100%)
- [ ] [\_] Feature flags allow toggling new functionality without redeployment

---

## 6. Security

- [ ] [\_] Authentication boundaries are defined (service-to-service, user-to-service)
- [ ] [\_] Service-to-service communication uses mutual TLS (mTLS) or equivalent
- [ ] [\_] Secrets (API keys, database passwords, certificates) are managed via a vault solution
- [ ] [\_] No secrets are hardcoded in code, configuration files, or environment variables
- [ ] [\_] Secrets are rotated on a defined schedule and after any compromise event
- [ ] [\_] Data classification labels are applied (public, internal, confidential, restricted)
- [ ] [\_] Encryption in transit (TLS ≥ 1.2) is enforced for all network communication
- [ ] [\_] Encryption at rest is enabled for all data stores
- [ ] [\_] Input validation and output encoding are applied (no injection vulnerabilities)
- [ ] [\_] Least-privilege principle is applied to service accounts / IAM roles
- [ ] [\_] Dependency vulnerabilities are scanned in CI (SCA / SAST)
- [ ] [\_] A penetration test or security review has been completed (or is scheduled)

---

## 7. Incident Response

- [ ] [\_] Runbook exists and covers: common failure scenarios, diagnostic steps, and remediation
- [ ] [\_] Runbook includes: service owner, escalation contacts, dashboard links, and alert links
- [ ] [\_] Runbook is stored alongside the service code or in a known wiki location
- [ ] [\_] On-call rotation is established and the team is trained on the service
- [ ] [\_] On-call engineers have production access and can deploy fixes
- [ ] [\_] Escalation path is documented (primary → secondary → engineering manager → director)
- [ ] [\_] Incident severity levels are defined (SEV1–SEV4) with corresponding response SLAs
- [ ] [\_] Postmortem process is defined (blameless, within 5 business days)
- [ ] [\_] A communication template exists for incident status updates
- [ ] [\_] Service is registered with the incident management platform (PagerDuty, Opsgenie, etc.)

---

## 8. Service Level Objectives (SLOs)

- [ ] [\_] Service Level Indicators (SLIs) are defined for availability, latency, and durability
- [ ] [\_] SLO targets are defined for each SLI (e.g., 99.9% availability, p99 < 200ms)
- [ ] [\_] SLIs are measured and instrumented (not just theoretical)
- [ ] [\_] Error budget is calculated (1 − SLO) and tracked over a defined window (e.g., 30 days)
- [ ] [\_] Error budget burn rate alerts are configured (fast, medium, slow burn)
- [ ] [\_] SLO attainment is visible on a dashboard shared with the team
- [ ] [\_] Consequences for exhausting the error budget are defined (freeze features, rollback)
- [ ] [\_] SLOs are documented and agreed upon with product / business stakeholders

---

## 9. Compliance

- [ ] [\_] Applicable regulatory frameworks are identified (SOC 2, HIPAA, PCI-DSS, GDPR, FedRAMP, etc.)
- [ ] [\_] Data residency requirements are documented and enforced (which regions data may reside in)
- [ ] [\_] Data retention and deletion policies are implemented
- [ ] [\_] Audit logs are captured for all administrative and data-access actions
- [ ] [\_] Audit log retention period meets regulatory requirements
- [ ] [\_] Access controls satisfy compliance requirements (RBAC, least privilege, separation of duties)
- [ ] [\_] Privacy impact assessment (PIA) or data protection review has been completed (if applicable)
- [ ] [\_] Licensing compliance for all dependencies is verified
- [ ] [\_] Third-party vendor security assessments are on file for external dependencies

---

## Action Items (Fails & Warns)

| # | Category | Item | Status | Owner | Due Date | Notes |
| - | -------- | ---- | ------ | ----- | -------- | ----- |
|   |          |      |        |       |          |       |
|   |          |      |        |       |          |       |
|   |          |      |        |       |          |       |
|   |          |      |        |       |          |       |
|   |          |      |        |       |          |       |

---

## Scoring Rubric

### Overall Review Result

| Score | Range | Meaning | Launch Decision |
| ----- | ----- | ------- | --------------- |
| **PASS** | 0 Fails, < 5 Warns | All critical items pass; minor or no exceptions | Authorized to launch |
| **CONDITIONAL PASS** | 0 Fails, ≥ 5 Warns | No blockers, but significant risks documented | Launch authorized with conditions; all Warn items must have remediation plans |
| **FAIL** | ≥ 1 Fail | At least one blocker remains | Launch blocked; must resolve all Fails before re-review |

### Category Health Score

Count how many categories have **zero Fails** versus **one or more Fails**:

- **9/9** categories clear — Excellent
- **7–8/9** categories clear — Good; address outstanding Fails
- **5–6/9** categories clear — Needs improvement; significant work required
- **< 5/9** categories clear — Unacceptable; launch should not proceed

### Sign-off

| Role | Name | Signature | Date |
| ---- | ---- | --------- | ---- |
| Service Owner | \_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_\_\_\_\_\_\_\_ |
| SRE Reviewer | \_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_\_\_\_\_\_\_\_ |
| Engineering Manager | \_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_\_\_\_\_\_\_\_ |
| Security Reviewer (if applicable) | \_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_\_\_\_\_\_\_\_ |
| Compliance Reviewer (if applicable) | \_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_\_\_\_\_\_\_\_ |
