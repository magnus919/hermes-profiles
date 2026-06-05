---
title: "SLO Declaration: [Service Name]"
doc_id: SLO-[SERVICE-CODE]-[VERSION]
status: draft | reviewed | approved | superseded
created: [YYYY-MM-DD]
last_modified: [YYYY-MM-DD]
owner: "[Owner Name / Team]"
approver: "[Approver Name]"
classification: internal | customer-facing | critical-infrastructure
---

# SLO Declaration — [Service Name]

## 1. Service Overview

| Field | Value |
|---|---|
| **Service Name** | [Service Name] |
| **Service ID** | [SVC-XXXXX] |
| **Description** | [Brief description of service purpose and functionality] |
| **Owner** | [Team Name / Individual] |
| **Escalation Path** | [#slack-channel](https://...), [@oncall-handoff] |
| **Tier Classification** | **Tier [1/2/3/4]** — [Critical / High / Medium / Low] |
| **Service Dependencies** | [List of upstream/downstream services] |
| **Documentation Links** | [Runbook], [Architecture Doc], [Dashboards] |

### Tier Definitions

| Tier | Definition | Acceptable Uptime |
|---|---|---|
| 1 | Customer-facing critical path; revenue-impacting | ≥ 99.99% |
| 2 | Important internal service; customer-facing non-critical | ≥ 99.9% |
| 3 | Internal tooling; best-effort availability | ≥ 99.5% |
| 4 | Experimental / dev-only; no formal commitment | No commitment |

---

## 2. SLO Window

| Parameter | Value |
|---|---|
| **Measurement Window** | [e.g., 28-day rolling / 30-day calendar / quarterly] |
| **Window Start** | [YYYY-MM-DD] |
| **Window End** | [YYYY-MM-DD or "rolling"] |
| **Evaluation Cadence** | [e.g., daily / weekly / upon window close] |
| **Reporting Channels** | [e.g., Grafana dashboard, PagerDuty, weekly SRE review] |

---

## 3. SLI Specifications

Each SLI is defined with an explicit metric name, data source, and measurement method.

### 3.1. SLI Definition Table

| SLI ID | Indicator Name | Metric Name | Data Source | Measurement Method | Good Criteria | Aggregation |
|---|---|---|---|---|---|---|
| SLI-001 | Request Latency (p99) | `[service]_http_request_duration_ms` | [Prometheus / Datadog / CloudWatch / custom] | Histogram quantile over 1m buckets; sampled every [15s] | ≤ [200]ms at p99 | Rolling window average |
| SLI-002 | Error Rate | `[service]_http_requests_total{status=~"5.."}` | [Prometheus / Datadog / CloudWatch / custom] | Count of 5xx / total requests; measured in [1m] bins | Ratio < [0.001] (0.1%) | Rolling window sum |
| SLI-003 | Availability | `[service]_probe_success` | [Synthetic probes / Blackbox exporter / Health endpoint] | Synthetic check every [60s] from [3] regions | Probe returns HTTP 200 in ≥ [2]/[3] regions | Rolling window % |
| SLI-004 | Throughput | `[service]_requests_per_second` | [Prometheus / Data source] | Rate() over [5m] intervals | Within [baseline ± 20%] of expected throughput | Rolling window avg |
| SLI-005 | [Custom SLI Name] | `[metric_name]` | [Data source] | [Measurement method] | [Good criteria] | [Aggregation] |

### 3.2. SLI Details (Optional — for complex SLIs)

**SLI-001: Request Latency (p99)**
- **Metric**: `[service]_http_request_duration_ms`
- **Source**: Prometheus (datasource: `[prometheus-datasource-name]`)
- **Query**: `histogram_quantile(0.99, sum(rate([service]_http_request_duration_seconds_bucket[1m])) by (le))`
- **Exclusions**: Requests to `/healthz`, `/metrics`; requests from synthetic probes
- **Measurement Notes**: [e.g., Measured at load balancer edge, excludes client-side latency]

**SLI-002: Error Rate**
- **Metric**: `[service]_http_requests_total`
- **Source**: [Data source]
- **Query**: `sum(rate([service]_http_requests_total{status=~"5.."}[1m])) / sum(rate([service]_http_requests_total[1m]))`
- **Exclusions**: Expected errors (rate-limited requests, known bad actors); 503s from deliberate traffic-shedding
- **Measurement Notes**: [e.g., Only counts requests that reached application servers]

---

## 4. SLO Targets & Error Budgets

| SLI ID | SLO Target | Measurement Window | Error Budget | Budget per Window | Consumed So Far |
|---|---|---|---|---|---|
| SLI-001 | p99 latency ≤ 200ms for ≥ 99.9% of requests | 28-day rolling | 0.1% of requests (43.2 minutes of bad requests per 30d) | [43.2] min | [X.X]% |
| SLI-002 | Error rate < 0.1% for ≥ 99.95% of time | 28-day rolling | 0.05% of time (≈ 21.6 minutes of excessive errors per 30d) | [21.6] min | [X.X]% |
| SLI-003 | Availability ≥ 99.99% | 28-day rolling | 0.01% (≈ 4.3 minutes of downtime per 30d) | [4.3] min | [X.X]% |
| SLI-004 | Throughput within baseline ±20% for ≥ 99.5% of time | 28-day rolling | 0.5% of time (≈ 3.6 hours per 30d) | [3.6] hr | [X.X]% |
| SLI-005 | [Custom target] | [Window] | [Error budget calculation] | [Amount] | [X.X]% |

### Error Budget Policy

- **Consumption ≤ 50%**: Normal operations; feature releases permitted.
- **Consumption 50–75%**: Increased monitoring, reduce deployment velocity, review changes.
- **Consumption 75–100%**: **Error budget at risk.** Feature freezes in effect; only P0/P1 fixes and rollbacks permitted. SRE review required.
- **Consumption > 100%**: **Budget exhausted.** Service classified as "out of SLO." Immediate incident response triggered. Exhaustion requires a postmortem with root cause analysis.

---

## 5. Burn Rate Alert Thresholds

| Severity | Burn Rate | SLO Consumption | Example (30d window) | Alert Action |
|---|---|---|---|---|
| **Page (P0)** | ≥ 1440× (1h budget in 1h) | Consumes entire budget in ≤ 1 hour | 0.1% of 30d ≈ 43m → burning budget in 1h | Immediate page; incident response; auto-rollback |
| **Page (P1)** | ≥ 144× (10h budget in 1h) | Consumes 10% of budget in 1 hour | Consumes 4.3m of budget per hour | Page on-call; escalation if sustained > 2h |
| **Warning** | ≥ 14.4× (10h budget in 10h) | Consumes 10% of budget in 10 hours | Consumes 4.3m over 10h window | Slack notification; dashboard alert |
| **Watch** | ≥ 1.44× (10h budget in 100h) | Consumes 10% of budget in 100 hours | Slow drift detection | Informational; included in weekly report |

### Multi-Window, Multi-Burn-Rate (MWMBR) Configuration

| Alert | Short Window | Long Window | Short Budget Consumption | Long Budget Consumption |
|---|---|---|---|---|
| Critical Page | 1m | 1h | ≥ [X]% | ≥ [Y]% |
| Warning | 5m | 6h | ≥ [X]% | ≥ [Y]% |

---

## 6. Release Gating Rules

| Condition | Gate Action | Override Authority |
|---|---|---|
| Error budget consumption > 75% | Block new production deployments | VP of Engineering + SRE Lead |
| Error budget consumption > 100% | Block all deployments (including roll-forward) | CTO / VP Eng; rollback still permitted |
| Any SLI breaching SLO for > 2 consecutive evaluation windows | Block canary → full rollout | SRE Lead; requires approved mitigation plan |
| Critical burn-rate alert active (P0/P1) | Block any deployment until alert clears | N/A (auto-gate) |
| Release window blackout ([specify dates]) | Block production releases | Release Engineering |
| [Custom rule] | [Gate action] | [Override authority] |

### Release Exception Process

1. Engineer submits exception request via [link to form/tool].
2. SRE Lead reviews impact analysis and mitigation plan.
3. If approved by both SRE Lead and Service Owner, deploy proceeds with monitoring overlay.
4. Exception automatically expires after [X] hours.

---

## 7. Exception Handling

### 7.1. Planned Exceptions

| Exception ID | Description | SLI(s) Affected | Start Date | End Date | Approved By | Notes |
|---|---|---|---|---|---|---|
| EXC-001 | [e.g., Database migration] | SLI-001, SLI-002 | [YYYY-MM-DD] | [YYYY-MM-DD] | [Name] | Expected latency increase of ~50ms during window |
| EXC-002 | [Description] | [SLI IDs] | [Start] | [End] | [Name] | [Notes] |

### 7.2. Exclusion Rules

The following events are **excluded** from SLO measurement:

- **Scheduled maintenance** with [X] days' advance notice and approved change window.
- **Known client throttling** where the service intentionally returns 429/503 for traffic management.
- **External dependency failures** that the service cannot mitigate (requires dependency downtime documentation).
- **Pre-release environments** (staging, dev, canary deployments).
- **Graceful degradation modes** explicitly documented and approved by SRE.

### 7.3. Exceptional Events

Events not covered by the above exclusions that require SLO relief must follow the exception process in Section 6.1.

---

## 8. Version History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | [YYYY-MM-DD] | [Author Name] | Initial SLO declaration |
| 1.1 | [YYYY-MM-DD] | [Author Name] | [Summary of changes] |
| 1.2 | [YYYY-MM-DD] | [Author Name] | [Summary of changes] |

---

## 9. Review Schedule & Sign-off

| Item | Detail |
|---|---|
| **Review Cadence** | Quarterly (or triggered by architectural / capacity changes) |
| **Next Review Date** | [YYYY-MM-DD] |
| **Last Reviewed** | [YYYY-MM-DD] |

### Sign-off

| Role | Name | Date | Signature |
|---|---|---|---|
| **Service Owner** | [Name] | [YYYY-MM-DD] | |
| **SRE Lead** | [Name] | [YYYY-MM-DD] | |
| **VP of Engineering** | [Name] | [YYYY-MM-DD] | *(Tier 1 only)* |

---

*This SLO declaration should be reviewed and updated whenever the service architecture, capacity, or business requirements change materially. Keep this document in version control alongside service configuration.*
