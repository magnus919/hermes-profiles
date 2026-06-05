# Error Budget Policy

| Metadata | Value |
|---|---|
| **Document Owner** | [SRE Team Lead] |
| **Version** | 1.0 |
| **Last Reviewed** | [YYYY-MM-DD] |
| **Review Cadence** | [Quarterly / Semi-Annual] |
| **Approved By** | [Engineering Director / VP of Infrastructure] |

---

## 1. Purpose

This document defines the error budget policy for all services covered under the Site Reliability Engineering (SRE) framework. The error budget is the primary mechanism for balancing feature velocity against service reliability. It quantifies how much "unreliability" is acceptable over a given window and governs when releases must be halted to protect the user experience.

---

## 2. Scope

This policy applies to the following services:

| Service | SLO Target | Measurement Method | Owner Team |
|---|---|---|---|
| [Service Name] | [e.g. 99.9%] | [e.g. Request success rate] | [Team] |
| [Service Name] | [e.g. 99.99%] | [e.g. Latency P99 < 200ms] | [Team] |
| [Service Name] | [e.g. 99.95%] | [e.g. Request success rate] | [Team] |

All services with an SLO defined in [link to SLO documentation] are subject to this policy. Services without an explicit SLO are considered best-effort and are not governed by error budget rules.

---

## 3. Error Budget Mechanics

### 3.1 Accrual

Error budgets are calculated over a **rolling [30]-day window**. The total budget available at the start of any window is:

```
total_error_budget = (1 - slo_target) * total_requests
```

For a service with an SLO of 99.9% and 10,000,000 requests over 30 days:

```
total_error_budget = (1 - 0.999) * 10,000,000 = 10,000 errors
```

### 3.2 Consumption

Each request that does **not** meet the SLO criteria (e.g., 5xx status code, latency exceeding P99 threshold) consumes one unit of error budget. Consumption is calculated as:

```
consumed_budget = bad_events_count
budget_remaining = total_error_budget - consumed_budget
```

### 3.3 Burn Rate

The **burn rate** measures how fast the error budget is being consumed relative to the target:

```
burn_rate = (1 - measured_availability) / (1 - slo_target)
```

A burn rate of:
- **1.0** means errors are occurring exactly at the SLO boundary.
- **> 1.0** means errors are exceeding the allowed rate (budget is being consumed faster than it accrues).
- **< 1.0** means the service is outperforming its SLO (budget is accumulating).

---

## 4. Consumption Thresholds & Actions

The error budget is divided into four color-coded zones. Each zone triggers specific operational and release-gating actions.

| Zone | Budget Remaining | Burn Rate (over 1h) | Burn Rate (over 6h) | Actions |
|---|---|---|---|---|
| **Green** | > 70% | < 1 | < 1 | Normal operations. Releases permitted. No action required. |
| **Yellow** | 30% – 70% | 1 – 3 | 1 – 2 | Tag incident. Create postmortem for any SLO-violating event. Notify team lead. Releases proceed with caution. |
| **Red** | 5% – 30% | 3 – 10 | 2 – 5 | **Releases halted.** On-call escalation. Engineering leadership notified. Daily standup review. Blameless postmortem required. |
| **Exhausted** | < 5% | > 10 | > 5 | **All non-critical releases frozen.** Emergency incident response activated. Executive briefing required. Auto-scaling and resilience measures enforced. RCAs due within 48 hours. |

### Detailed Actions by Threshold

#### Green (Normal)
- All release types permitted.
- Standard monitoring and alerting.
- Regular on-call shift rotation.

#### Yellow (Elevated Consumption)
1. Tag all recent deployments and changes in the [Deployment Tracker].
2. Open a [Low-Severity Incident] in the incident management system.
3. Review recent changes with the on-call engineer.
4. Notify the service team lead.
5. **Release Gate**: Critical/hotfix releases only with team lead approval.

#### Red (Critical Consumption)
1. **Immediately halt all non-critical releases.**
2. Escalate to the [Secondary On-Call Engineer].
3. Notify [Engineering Manager] and [SRE Manager].
4. Initiate a [War Room] if burn rate exceeds [8].
5. Create a blameless postmortem draft.
6. Review dashboards, logs, and metrics to identify root cause.
7. **Release Gate**: Only emergency security patches and P0 incident fixes permitted.

#### Exhausted (Budget Depleted)
1. **Freeze all releases** except patches for CVSS >= [7.0] vulnerabilities.
2. Activate [Major Incident Response Protocol].
3. Brief [VP of Engineering / CTO] within [1 hour].
4. Compile draft Root Cause Analysis (RCA) within [24 hours], final within [48 hours].
5. Implement mandatory resilience improvements (rate limiting, circuit breakers, auto-scaling).
6. **Release Gate**: Only incident remediation code allowed. Requires SRE Director approval.
7. Conduct a reliability postmortem with all stakeholders.

---

## 5. Release Gating Rules

| Release Type | Green | Yellow | Red | Exhausted |
|---|---|---|---|---|
| Standard feature releases | Allowed | Halted | Halted | Halted |
| Bug fixes (non-critical) | Allowed | Allowed | Halted | Halted |
| Critical bug fixes / hotfixes | Allowed | Team lead approval | SRE lead approval | SRE Director approval |
| Security patches (CVSS < 7) | Allowed | Allowed | SRE lead approval | SRE Director approval |
| Security patches (CVSS >= 7) | Allowed | Allowed | Allowed | Allowed |
| Infrastructure changes | Allowed | Caution required | Halted | Halted |
| Config changes | Allowed | Peer review required | SRE lead approval | Halted |

Releases may resume when the error budget returns to **Yellow** or above and the [Release Review Board] approves.

---

## 6. Exceptions & Overrides

| Exception | Process | Approver |
|---|---|---|
| Emergency release during freeze | File [Exception Request] with justification | [VP of Engineering] |
| SLO adjustment | Submit [SLO Change Proposal] with data | [SRE Steering Committee] |
| Budget over-allocation (new feature launch) | Request via [Governance Board] | [CTO / VP Eng] |
| One-time budget extension | Submit [Budget Waiver Request] | [SRE Director] |
| Experimental / Beta services | Opt-out of error budget policy | [Product Manager + SRE Lead] |

---

## 7. Escalation Paths

### When Budget is Exhausted

```
Level 0: On-Call Engineer (Primary)
    ↓ (if unresolved in 15 min)
Level 1: On-Call Engineer (Secondary) + Service Team Lead
    ↓ (if unresolved in 30 min)
Level 2: SRE Manager + Engineering Manager
    ↓ (if unresolved in 60 min)
Level 3: Director of Engineering / VP of Infrastructure
    ↓ (if unresolved in 120 min)
Level 4: Incident Commander + Executive Team
```

### Communication Chain

1. **Internal**: [#oncall-alerts Slack channel] — automated alerts from monitoring.
2. **Engineering**: [#sre-eng channel] — incident coordination.
3. **Leadership**: Email to [sre-leadership@example.com] for Red zone or above.
4. **Executive**: Email + Slack DM to [VP Engineering] for Exhausted zone.

---

## 8. Review Cadence

| Review Type | Frequency | Participants |
|---|---|---|
| Error budget report review | Weekly | Service team + SRE |
| Policy effectiveness review | Monthly | SRE team |
| SLO and budget adjustment | Quarterly | SRE + Product + Engineering leadership |
| Full policy audit | Annually | SRE team + Legal + Compliance |

### Required Artifacts

- Weekly error budget report (auto-generated by [Monitoring System] dashboard).
- Monthly consumption trends analysis.
- Quarterly SLO attainment review with [Stakeholder Group].
- Annual policy effectiveness report.

---

## 9. Appendices

### A. Example Budget Calculation

| Service | SLO | Total Requests | Error Budget | Consumed | Remaining | % Remaining | Status |
|---|---|---|---|---|---|---|---|
| api-gateway | 99.9% | 50,000,000 | 50,000 | 5,000 | 45,000 | 90% | Green |
| user-service | 99.95% | 10,000,000 | 5,000 | 3,500 | 1,500 | 30% | Yellow |
| search-service | 99.99% | 100,000,000 | 10,000 | 9,200 | 800 | 8% | Red |
| payment-service | 99.99% | 5,000,000 | 500 | 490 | 10 | 2% | Exhausted |

### B. Related Documents

- [Service Level Objectives (SLO) Definition]
- [Incident Response Playbook]
- [Release Management Policy]
- [Postmortem Template]
- [On-Call Rotation Schedule]
- [SLO Burn Rate Script / Tooling]

### C. Glossary

| Term | Definition |
|---|---|
| **Error Budget** | The maximum number of failures allowed in a service over a given time window before violating the SLO. |
| **Burn Rate** | The rate at which the error budget is being consumed relative to the target. |
| **SLO** | Service Level Objective — the target level of reliability for a service. |
| **SLI** | Service Level Indicator — the actual measured value of reliability. |
| **SLA** | Service Level Agreement — a contractual commitment to reliability. |
| **Exhausted** | State where the error budget is depleted (less than 5% remaining). |
