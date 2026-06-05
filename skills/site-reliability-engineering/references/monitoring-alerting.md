# Monitoring & Alerting Reference

## Overview

Monitoring and alerting form the operational backbone of any production system. This reference covers the principles, patterns, and practical implementations that SREs use to observe system health, detect anomalies, and respond to incidents. It is designed as a standalone guide for site reliability engineers building or refining their observability stack.

---

## 1. The Four Golden Signals

Coined by Google's SRE team, the Four Golden Signals are the highest-level metrics every distributed system should track. They provide a minimal, universally applicable set of health indicators that cut across application domains.

### 1.1 Latency

Latency measures the time required to service a request. It must be tracked separately for *successful* and *failed* requests — a slow failure (e.g., a 500 that takes 30 seconds to return) can mask a real problem with success-path latency.

**Key considerations:**
- Use percentiles, not averages. p50, p95, p99 tell a far richer story than mean latency.
- Distinguish between *latency* (time to first byte / time to complete) and *response time* (round-trip from client perspective).
- Instrument at every layer: load balancer, application, database, downstream dependency.

**Example PromQL latency queries:**
```promql
# p99 latency of HTTP requests (successful only), last 5m
histogram_quantile(0.99,
  rate(http_request_duration_seconds_bucket{status=~"2..|3.."}[5m])
)

# p50 latency
histogram_quantile(0.50,
  rate(http_request_duration_seconds_bucket[5m])
)

# Slow request ratio: requests exceeding 1 second
rate(http_request_duration_seconds_count{status=~"2..|3.."}[5m])
/
rate(http_request_duration_seconds_bucket{le="1.0", status=~"2..|3.."}[5m])
```

### 1.2 Traffic

Traffic describes the demand placed on the system. Its units depend on the service type:

| Service Type        | Traffic Metric              | Example                            |
|---------------------|-----------------------------|------------------------------------|
| HTTP API            | Requests per second (RPS)   | `rate(http_requests_total[5m])`    |
| Database            | Queries per second (QPS)    | `rate(mysql_queries_total[5m])`    |
| Message queue       | Messages consumed per minute | `rate(kafka_messages_total[5m])`   |
| CDN / file serving  | Bytes per second            | `rate(nginx_bytes_sent_total[5m])` |
| Web application     | Active sessions / users     | `active_users`                     |

**Traffic pattern alerts** should distinguish organic growth (capacity planning) from sudden spikes (incidents):
```promql
# Sudden traffic spike: 2x over 5-minute baseline
(
  rate(http_requests_total[5m])
  /
  rate(http_requests_total[30m] offset 10m)
) > 2
```

### 1.3 Errors

Errors are requests that fail, explicitly (5xx) or implicitly (returning wrong data, meeting SLOs but returning stale results). Track both:

- **Explicit errors:** HTTP 5xx, gRPC UNAVAILABLE, TCP connection resets.
- **Implicit errors:** Success codes with semantically wrong responses (e.g., 200 OK with empty body), responses that exceed latency SLOs, degraded functionality.

**Error ratio is often more useful than raw error count**, especially during traffic changes:
```promql
# Error ratio over 5m window
sum(rate(http_requests_total{status=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))
```

**Alert on error budget burn rate** for SLO-based alerting:
```promql
# Error budget burn rate over 1h: how fast we're consuming the SLO budget
(
  1 - (
    sum(rate(http_requests_total{status=~"2.."}[1h]))
    / sum(rate(http_requests_total[1h]))
  )
) / (1 - 0.99)  // 99% SLO target
```

### 1.4 Saturation

Saturation measures how "full" the service is. The most limited resource (CPU, memory, disk I/O, network bandwidth, connection pool, database connections, file descriptors) dominates.

**Key principles:**
- Saturation often precedes performance degradation — it is a leading indicator.
- Use utilization (percentage) but also track queue depth or request-dropping behavior.
- The USE Method (Utilization, Saturation, Errors) maps directly here.

```promql
# CPU saturation: load average relative to core count
node_load1 / count(node_cpu_seconds_total{mode="idle"}) > 0.8

# Memory saturation: available to total ratio
node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes < 0.1

# Connection pool saturation: active connections vs max
pg_stat_activity_count / pg_settings_max_connections > 0.8

# Disk I/O saturation: queue depth
rate(node_disk_io_time_weighted_seconds_total[5m]) > 1000
```

---

## 2. Black-Box vs White-Box Monitoring

### 2.1 Black-Box Monitoring

Black-box monitoring observes the system from the outside as a user would. It tests behaviour, not implementation.

**Characteristics:**
- Synthetic probes, health checks, external uptime monitors.
- Validates *what* the system does, not *how*.
- Catches issues invisible to internal metrics: DNS resolution failures, TLS certificate expiry, CDN misconfiguration, routing problems.
- Example: "HTTP GET /health returns 200 within 5 seconds."

**Tools:** Prometheus blackbox exporter, synthetic monitoring (Checkly, Grafana Synthetics), external uptime services.

**Alert rules:**
```promql
# Probe failure over 5 minutes
avg_over_time(probe_success[5m]) < 0.5

# Latency from probe perspective
probe_duration_seconds > 3
```

### 2.2 White-Box Monitoring

White-box monitoring observes the system from the inside, exposing internal state, metrics, and performance characteristics.

**Characteristics:**
- Application metrics (request durations, error rates, goroutine counts).
- Database query performance, connection pool depth, cache hit ratios.
- Runtime behaviour (GC pauses, thread contention, memory allocation).
- Enables root-cause analysis and capacity planning.
- Example: "JVM heap usage is at 85% and growing at 100 MB/min."

**Tools:** Application metrics instrumentation (Prometheus client libraries, OpenTelemetry), runtime debugging endpoints, structured logging.

The two approaches are complementary. A mature observability stack uses both: black-box for customer-facing SLIs, white-box for debugging and proactive capacity management.

---

## 3. Symptom-Based vs Cause-Based Alerting

### 3.1 Symptom-Based Alerting (Preferred)

Alert on *symptoms* — observable problems that affect users right now or will imminently.

| Symptom                         | Example Alert                                      |
|---------------------------------|----------------------------------------------------|
| High latency                    | p99 latency > 2 seconds for 5 minutes              |
| Elevated error rate             | Error ratio > 5% for 10 minutes                    |
| Error budget exhaustion         | 2% of monthly error budget consumed in 1 hour      |
| Degraded user experience        | Page load time > 3 seconds for logged-in users     |

**Rule of thumb:** If the alert fires and no user-facing impact can be articulated, the alert is cause-based and should be re-evaluated or demoted to a diagnostic signal.

### 3.2 Cause-Based Alerting

Alert on *causes* — internal conditions that *might* lead to symptoms. These should generally be:
- **Log-only** or **warning-level** notifications (dashboards, not pages).
- Tied to a specific known failure mode with clear remediation.
- Rate-limited to avoid noise storms.

| Cause                            | Better Approach                                   |
|----------------------------------|---------------------------------------------------|
| CPU > 90%                        | Dashboard panel + capacity planning ticket        |
| Disk > 80% full                  | Automated cleanup or low-severity notification    |
| Specific error log line appears  | Log-based metric + dashboard, not page            |
| Single pod OOMKilled             | Auto-restart (Kubernetes handles this)            |

---

## 4. Alert Design Principles

Every alert should pass three tests: **actionable**, **urgent**, and **novel**.

### 4.1 Actionable

The recipient must be able to do something about it.

- **Good:** "API error ratio exceeds 5% — investigate upstream database connectivity."
- **Bad:** "CPU is at 88% — no further context, no clear action."
- **Test:** If the alert fires and the on-call engineer asks "so what?" it is not actionable.

### 4.2 Urgent

The alert must require immediate attention.

- **Good:** "Error budget depletion rate will exhaust budget in 2 hours at current burn rate."
- **Bad:** "Certificate expires in 30 days" (should be a scheduled task, not a page).
- **Test:** Would it be acceptable to ignore this alert for 30 minutes? If yes, it is not urgent.

### 4.3 Novel

The alert should represent new information not already visible in dashboards or automated remediation.

- **Good:** "This is the first occurrence of a database connection pool exhaustion event today."
- **Bad:** "Pod restarted" — if Kubernetes auto-recovered and there's no systemic pattern.
- **Test:** Is this the same incident-meets-recovery cycle firing repeatedly? Suppress or tune.

### 4.4 Additional Design Heuristics

- **One alert = one problem.** Do not bundle multiple conditions into a single rule.
- **Include runbook links** in alert annotations.
- **Use consistent naming conventions:** `Service/Component/Severity/Description`.
- **Set appropriate `for` durations** (e.g., 5 minutes) to avoid flapping on transient issues.
- **Define expected response times** in the alert metadata (e.g., "Respond within 15 minutes").
- **Every page-level alert needs a documented escalation path.**

---

## 5. Time-Series Monitoring Architecture (Prometheus-Inspired)

### 5.1 Core Architecture Pattern

```
[Instrumented Services] --scrape--> [Prometheus Server] --read--> [Alertmanager]
                                     |                        +--> [Dashboards (Grafana)]
                                     |                        +--> [Long-term storage (Thanos/Cortex)]
                                     v
                                  [Recording Rules] --> [Aggregated metrics]
```

### 5.2 Metric Types

| Type        | Description                                          | Example                                      |
|-------------|------------------------------------------------------|----------------------------------------------|
| Counter     | Monotonically increasing value (resets on restart)   | `http_requests_total`, `errors_total`        |
| Gauge       | Point-in-time value that can go up and down          | `memory_usage_bytes`, `queue_depth`          |
| Histogram   | Configurable buckets for observing distributions     | `request_duration_seconds_bucket{le="0.5"}`  |
| Summary     | Pre-computed quantiles (cannot aggregate)            | `request_duration_seconds{quantile="0.99"}`  |

### 5.3 Recording Rules

Pre-compute expensive or frequently queried expressions to reduce query load:

```promql
# Group: "service:request_error_ratio:5m"
record: namespace:http_errors:ratio_rate5m
expr: |
  sum(rate(http_requests_total{status=~"5.."}[5m])) by (namespace)
  /
  sum(rate(http_requests_total[5m])) by (namespace)

# Group: "instance:cpu_utilization:rate5m"
record: instance:node_cpu_utilization:rate5m
expr: |
  1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance)
```

### 5.4 Alerting Rules Architecture

Separate evaluation tiers:

```promql
# Tier 1 — Direct metric threshold (immediate symptom)
alert: APIHighErrorRate
expr: |
  (sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
   /
   sum(rate(http_requests_total[5m])) by (service)) > 0.05
for: 5m
labels:
  severity: critical
annotations:
  summary: "{{ $labels.service }} error rate above 5%"
  runbook: "https://runbooks.example.com/high-error-rate"

# Tier 2 — Error-budget-based (burn rate)
alert: ErrorBudgetBurnedFast
expr: |
  (
    (1 - (sum(rate(http_requests_total{status=~"2.."}[1h])) by (service)
         / sum(rate(http_requests_total[1h])) by (service)))
    / (1 - 0.99)
  ) > 0.05
for: 2m
labels:
  severity: critical
annotations:
  summary: "Error budget burning at 5x safe rate"

# Tier 3 — Absent metric (service down)
alert: ServiceDown
expr: |
  absent(up{job="api-server"}) == 1
for: 30s
labels:
  severity: critical
```

---

## 6. Alert Routing and Severity

### 6.1 Severity Levels

| Level       | Label      | Response SLA     | Channel       | Purpose                               |
|-------------|------------|------------------|---------------|---------------------------------------|
| Critical    | P0         | < 15 minutes     | Page (phone)  | User-facing outage, data loss, breach  |
| High        | P1         | < 30 minutes     | Page (push)   | Severe degradation, error budget risk  |
| Medium      | P2         | < 4 hours        | Chat (thread) | Degradation without immediate impact   |
| Low         | P3         | Next business day| Ticket        | Capacity warnings, cleanup reminders   |
| Informational | P4       | None             | Log only      | Dashboard annotations, debugs          |

### 6.2 Routing Matrix

Route based on service, severity, time of day, and team ownership:

```
[Alertmanager Configuration]
route:
  receiver: 'default'
  routes:
    - match:
        severity: critical
      receiver: 'page-oncall'
      repeat_interval: 1h
    - match:
        service: billing
      receiver: 'billing-team'
    - match_re:
        component: "^database"
      receiver: 'data-platform'
    - match:
        severity: warning
      receiver: 'chat-channel'
      group_wait: 30s
      group_interval: 5m
```

### 6.3 Grouping and Deduplication

Prevent alert storms by grouping related alerts:

```yaml
group_by: ['alertname', 'service', 'cluster']
group_wait: 30s       # collect alerts for 30s before sending
group_interval: 5m    # wait 5m between repeat notifications
repeat_interval: 4h   # don't re-notify for 4h unless severity changes
```

---

## 7. Dashboard Design Principles

### 7.1 The Golden Rules

1. **One dashboard per story.** A dashboard should answer a single question or serve a single persona (e.g., "Is the API healthy?", "Database capacity planning").
2. **Three-tier layout:**
   - **Top row:** Summary / health — the single number or status that tells you if everything is OK.
   - **Middle rows:** Key time-series — latency, errors, traffic, saturation per component.
   - **Bottom rows:** Drill-down details — per-shard, per-host, per-endpoint.
3. **Consistent time ranges** across panels on the same dashboard.
4. **Use left Y-axis** for the primary metric; avoid dual-axes unless essential.
5. **Label clearly** with units (ms, req/s, %). Include SLO targets as threshold lines.

### 7.2 Dashboard Types

| Type            | Audience       | Refresh  | Content Summary                          |
|-----------------|----------------|----------|------------------------------------------|
| Executive       | Management     | 1 day    | SLIs, error budget, cost, capacity trends |
| Service Health  | On-call        | 30s      | Golden signals per service               |
| Capacity        | Infrastructure | 1 hour   | Resource utilization, growth projections  |
| Debug / Triage  | Engineering    | Real-time| Detailed traces, log rates, anomaly plots |
| SLO Burn Rate   | SRE            | 1 min    | Burn rate vectors, remaining budget      |

### 7.3 Anti-Patterns

- **Spaghetti dashboards:** More than 20 panels on one dashboard. Split by concern.
- **Red/green everywhere:** Red color should be reserved for *failing* the SLO.
- **No time context:** Single-number stat panels without a sparkline or change indicator.
- **Orphan dashboards:** No owner, no last-modified date, no description.

---

## 8. On-Call Alert Fatigue Prevention

Alert fatigue is the leading cause of pager burnout and missed real incidents.

### 8.1 Causes

| Cause                          | Remedy                                            |
|--------------------------------|---------------------------------------------------|
| Too many low-severity alerts   | Demote to P3/P4; page only on critical.           |
| Flaky alerts (transient)       | Increase `for` duration; use multi-window logic.  |
| Duplicate alerts               | Use alertmanager grouping; deduplicate rules.     |
| Noisy auto-remediation cycles  | Silence alerts for N minutes after auto-fix.      |
| Undefined ownership            | Every alert must route to exactly one team.       |
| Missing runbooks               | Add runbook links; if unclear, the alert is bad.  |

### 8.2 Fatigue Prevention Techniques

- **Weekly alert reviews:** Every critical alert is reviewed for signal-to-noise ratio. If it fired "unnecessarily" more than once in the past week, tune or delete it.
- **Gradual escalation:** Start with a 5-minute `for` duration, alert warning first, then escalate to critical if condition persists.
- **Suppression during maintenance:** Tag maintenance windows; suppress alerts during known change windows.
- **Machine learning / dynamic thresholds:** For seasonal systems, use anomaly detection instead of static thresholds.
- **Error budget alerts over raw threshold alerts:** Raw threshold alerts (e.g., "p99 > 500ms") are rigid. Error-budget-based alerts account for the SLO's remaining headroom.
- **Self-healing integration:** If a runbook step can be automated (restart, scale-up, traffic shed), add it. Only page if the automated action fails.
- **Psychologically safe culture:** No blame for acknowledging an alert and determining it was not actionable — that becomes tuning feedback.

### 8.3 Alert Fatigue Metrics to Track

- **Alert-to-incident ratio:** Number of pages that resulted in a documented incident vs. total pages. Target: > 50%.
- **Mean time to acknowledge (MTTA):** Should be under the defined SLA. Spikes suggest routing issues or fatigue.
- **Mean time to resolve (MTTR):** Tracks operational effectiveness.
- **False positive rate per rule:** Identify the worst offenders in the weekly review.

---

## 9. The USE Method and RED Method for Metrics

### 9.1 USE Method (Utilization, Saturation, Errors)

Used for **infrastructure resources** (CPU, memory, disk, network). Ask: For every resource, what is:
- **Utilization:** The average percent of time the resource is busy.
- **Saturation:** The degree to which the resource has extra work queued (can't service more).
- **Errors:** The count of error events.

**USE Method Counterpart per Resource:**

| Resource       | Utilization                    | Saturation                      | Errors                             |
|----------------|--------------------------------|---------------------------------|------------------------------------|
| CPU            | `avg by(instance) (rate(cpu_seconds_total{mode!="idle"}[5m]))` | `load1 / cpu_count` | `process_errors_total` (per process) |
| Memory         | `used / total`                 | `swap_usage` / OOM events       | `vmstat -s` page failures           |
| Disk I/O       | `avg by(device) (rate(disk_io_time_seconds_total[5m]))` | `rate(disk_io_time_weighted_seconds_total[5m])` | `disk_read_errors_total` / `disk_write_errors_total` |
| Network        | `rate(bytes_total[5m]) / bandwidth` | `drop_count / segment_retransmits` | `interface_errors_total`         |
| File handles   | `filefd_allocated / filefd_max` | —                               | `failed_file_opens_total`          |

**Example alert using USE:**
```promql
# Saturation: CPU run queue > 4x core count
(
  node_load15
  /
  count(node_cpu_seconds_total{mode="idle"})
) > 4
```

### 9.2 RED Method (Rate, Errors, Duration)

Used for **services and applications**. Ask for every service:
- **Rate:** Requests per second (throughput).
- **Errors:** Number of requests that fail.
- **Duration:** Time taken to process a request (latency distribution).

The RED Method is essentially the Four Golden Signals minus saturation — it focuses purely on user-facing service health rather than resource health.

**Instrumentation pattern (per endpoint or per operation):**
```promql
# Rate
rate(http_requests_total{job="api"}[5m])

# Errors (ratio)
sum(rate(http_requests_total{job="api", status=~"5.."}[5m]))
/
sum(rate(http_requests_total{job="api"}[5m]))

# Duration (p99)
histogram_quantile(0.99,
  rate(http_request_duration_seconds_bucket{job="api"}[5m])
)
```

### 9.3 When to Use Which

| Layer                 | Best Fit     | Rationale                                    |
|-----------------------|--------------|----------------------------------------------|
| Infrastructure (VM, container, disk, NIC) | USE | Resources have bounded capacity; saturation is meaningful. |
| Application (API, database, queue) | RED (or Golden Signals) | Behaviours (requests, errors, latency) are the concern. |
| Middleware / Proxy    | Both         | Resource concerns (connections, memory) AND service behaviours matter. |
| Network / Load balancer | RED + USE  | Throughput and errors (RED) plus interface saturation (USE). |

---

## 10. SLI-Based Alerting vs Threshold-Based Alerting

### 10.1 Threshold-Based Alerting (Classic)

**How it works:** Static thresholds on raw metrics (e.g., p95 latency > 500ms, CPU > 90%).

**Pros:**
- Simple to understand and implement.
- Works well for resource saturation alerts (disk full, OOM).
- No SLO definition required.

**Cons:**
- Requires manual tuning for each service.
- Does not account for *time remaining* — a p99 of 600ms at 8am on a Monday might be fine, but at 3am it indicates something wrong.
- Brittle: thresholds that are too tight generate noise, those too loose miss incidents.

### 10.2 SLI-Based Alerting

**How it works:** Define Service Level Indicators (SLIs) and Service Level Objectives (SLOs). Alert based on *error budget burn rate* — how fast the remaining allowable error budget is being consumed.

**SLI definition pattern:**
```yaml
sli_name: "api_request_latency_sli"
description: "Fraction of requests served in under 500ms"
good_event: "http_request_duration_seconds <= 0.5"
valid_events: "http_requests_total"
measurement_window: "28d"
```

**Burn rate alerting approach (Google SRE Workbook):**

| Burn Rate (x of target) | Duration     | Severity | Meaning                                               |
|-------------------------|--------------|----------|-------------------------------------------------------|
| >= 10x                  | 5 minutes    | Critical | Very severe, multi-9s breach imminent in minutes      |
| >= 5x                   | 30 minutes   | Critical | Severe, will exhaust budget in hours                  |
| >= 2x                   | 6 hours      | High     | Moderate burn, needs investigation                    |
| >= 1x                   | 3 days       | Low      | Slow bleed, ticket for next business day              |

**PromQL burn rate alert:**
```promql
# 10x burn rate over 5 minutes
alert: HighBurnRate_10x_5m
expr: |
  (
    (
      1 - (
        sum(rate(http_requests_total{status=~"2..", job="api"}[5m]))
        / sum(rate(http_requests_total{job="api"}[5m]))
      )
    ) / (1 - 0.99)
  ) > 10
for: 2m
labels:
  severity: critical
```

### 10.3 Comparison

| Aspect                | Threshold-Based                  | SLI-Based (Burn Rate)                  |
|-----------------------|----------------------------------|----------------------------------------|
| Tuning effort         | Per-service, per-metric           | Shared SLO framework                   |
| Sensitivity to traffic | Fixed threshold may be too tight at low traffic or too loose at high traffic | Proportional — error ratio, not absolute count |
| Leading vs lagging    | Leading (catches impending resource saturation) | Lagging for resource issues, leading for SLO breaches |
| Business alignment    | Weak                              | Direct: maps to customer-facing objectives |
| Complexity            | Low                               | Moderate (requires SLO definitions)    |

**Recommendation:** Use SLI/burn rate alerting for user-facing symptoms. Use threshold-based alerting for resource saturation and capacity warnings. The two approaches are complementary.

---

## 11. Multi-Window Alerting Approaches

Multi-window, multi-burn-rate alerting is the gold standard for balancing sensitivity with noise reduction. It evaluates the same condition across *multiple time windows* before firing.

### 11.1 Why Multi-Window?

A single-window alert (e.g., `error_ratio > 5% over 5m`) can:
- Fire on transient spikes that resolve before anyone acts (false positive).
- Miss slow-burn degradation that accumulates over hours but never crosses a short-window threshold (false negative).

### 11.2 Multi-Window, Multi-Burn-Rate Design

Evaluate the metric across two windows — a *short window* (high sensitivity) and a *long window* (confirms sustained condition):

```promql
# Conditional: short-window burn rate is > 10x target
# AND long-window burn rate is > 10x target
# Both must be true — catches sustained high burn, rejects transient spikes

alert: MultiWindowErrorBudgetBurn
expr: |
  (
    # Short window: 5m burn rate > 10x
    (
      (1 - (sum(rate(http_requests_total{status=~"2.."}[5m]))
           / sum(rate(http_requests_total[5m]))))
      / (1 - 0.99)
    ) > 10
  )
  and
  (
    # Long window: 1h burn rate > 10x (confirms sustained)
    (
      (1 - (sum(rate(http_requests_total{status=~"2.."}[1h]))
           / sum(rate(http_requests_total[1h]))))
      / (1 - 0.99)
    ) > 10
  )
for: 2m
labels:
  severity: critical
```

### 11.3 The Google SRE Multi-Window Alerting Matrix

| Condition                                 | Fires When                               | Character              |
|-------------------------------------------|------------------------------------------|------------------------|
| Short (5m) high burn AND Long (1h) high burn | Instant + sustained severe event     | "House on fire"       |
| Short (5m) low burn AND Long (1h) high burn | Slow bleed below burst sensitivity    | "Radiator leak"       |
| Short (5m) high burn AND Long (1h) low burn | Transient spike, already recovered    | No alert (correct!)   |
| Short (5m) low burn AND Long (1h) low burn | Everything nominal                      | No alert              |

### 11.4 Implementation Pattern with Recording Rules

```promql
# Recording rule: 5m burn rate ratio
record: slo:api_error_burn_rate_5m
expr: |
  (
    (1 - (sum(rate(http_requests_total{job="api", status=~"2.."}[5m]))
         / sum(rate(http_requests_total{job="api"}[5m]))))
    / (1 - 0.99)
  )

# Recording rule: 1h burn rate ratio
record: slo:api_error_burn_rate_1h
expr: |
  (
    (1 - (sum(rate(http_requests_total{job="api", status=~"2.."}[1h]))
         / sum(rate(http_requests_total{job="api"}[1h]))))
    / (1 - 0.99)
  )

# Alert: both windows agree on high burn
alert: APIErrorBudgetCriticalBurn
expr: |
  slo:api_error_burn_rate_5m > 10 and slo:api_error_burn_rate_1h > 10
for: 2m
labels:
  severity: critical
annotations:
  summary: "API error budget burning at critical rate"

# Alert: long window burn without short window (slow drain)
alert: APIErrorBudgetSlowBurn
expr: |
  slo:api_error_burn_rate_1h > 2 and slo:api_error_burn_rate_5m <= 10
for: 10m
labels:
  severity: warning
annotations:
  summary: "API error budget slowly draining"
```

### 11.5 Alternative: Sliding-Window with `min_over_time`

For environments where PromQL `and` semantics are unavailable, simulate multi-window with `min_over_time`:

```promql
alert: SlidingWindowHighErrorRate
expr: |
  min_over_time(
    (
      sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
      /
      sum(rate(http_requests_total[5m])) by (service)
    )[15m:]
  ) > 0.05
for: 2m
```

This requires the high error rate to be sustained across three consecutive 5-minute windows (15 minutes).

---

## 12. Practical PromQL Alert Rule Templates

### 12.1 Service Availability

```promql
# Service down — no metrics received
alert: ServiceDown
expr: absent(up{job="api-server"}) == 1
for: 1m
labels:
  severity: critical
annotations:
  summary: "{{ $labels.job }} is not sending metrics"
```

### 12.2 High Error Rate

```promql
# Per-path error rate
alert: PathHighErrorRate
expr: |
  (
    sum(rate(http_requests_total{status=~"5.."}[5m])) by (service, path)
    /
    sum(rate(http_requests_total[5m])) by (service, path)
  ) > 0.05
for: 5m
labels:
  severity: critical
annotations:
  summary: "5xx rate > 5% on {{ $labels.path }}"
```

### 12.3 High Latency

```promql
# Per-service p99 latency
alert: HighLatency
expr: |
  histogram_quantile(0.99,
    sum(rate(http_request_duration_seconds_bucket{status=~"2.."}[5m])) by (le, service)
  ) > 2.0
for: 5m
labels:
  severity: critical
annotations:
  summary: "p99 latency > 2s on {{ $labels.service }}"
```

### 12.4 Certificate Expiry

```promql
alert: TLSCertExpiringSoon
expr: |
  probe_ssl_earliest_cert_expiry - time() < 604800  # 7 days in seconds
for: 1h
labels:
  severity: warning
annotations:
  summary: "TLS certificate for {{ $labels.instance }} expires in less than 7 days"
```

### 12.5 Disk Space

```promql
alert: DiskSpaceCritical
expr: |
  (
    1 - (node_filesystem_avail_bytes{mountpoint="/", fstype!~"tmpfs|overlay"}
         / node_filesystem_size_bytes{mountpoint="/", fstype!~"tmpfs|overlay"})
  ) > 0.95
for: 5m
labels:
  severity: critical
annotations:
  summary: "Disk usage > 95% on {{ $labels.instance }}"
```

### 12.6 Connection Pool Saturation

```promql
alert: PgConnectionPoolExhausted
expr: |
  (
    sum by (instance) (pg_stat_activity_count{datname!~"template.*|postgres"})
    /
    avg by (instance) (pg_settings_max_connections)
  ) > 0.9
for: 5m
labels:
  severity: critical
annotations:
  summary: "PostgreSQL connection pool > 90% on {{ $labels.instance }}"
```

### 12.7 OOM Kill Detection

```promql
alert: OOMKilled
expr: |
  increase(kube_pod_container_status_restarts_total{reason="OOMKilled"}[15m]) > 0
for: 0m
labels:
  severity: critical
annotations:
  summary: "Pod {{ $labels.pod }} was OOMKilled"
```

### 12.8 Traffic Anomaly

```promql
alert: TrafficDrop
expr: |
  (
    rate(http_requests_total[5m])
    /
    rate(http_requests_total[5m] offset 1w at same day of week)
  ) < 0.5
for: 15m
labels:
  severity: warning
annotations:
  summary: "Traffic dropped > 50% compared to same time last week"
```

---

## 13. Closing Principles

1. **Page on symptoms, investigate causes.** Symptoms affect users; causes affect operators. One is urgent, the other is not.
2. **Every alert needs an owner and a runbook.** If the on-call cannot find both within 30 seconds, the alert is not production-ready.
3. **Test your alerts.** Use alert simulation tools (e.g., `amtool`, Prometheus alert unit tests with `promtool`) to validate logic before deploying.
4. **Review alerts weekly.** Each alert that fired is either a real incident (document it) or a false positive (tune it). No alert fires without producing an improvement action.
5. **Prefer dashboards for diagnostic data, alerts for escalations.** If a metric only says "look at the dashboard" it should be a panel, not a page.
6. **Multi-window beats single-window.** Short windows are noisy; long windows are slow. Use both for reliable detection.
7. **Error budget burn rate alerts are the gold standard** for user-facing services. They automatically account for the service's SLO, remaining budget, and traffic levels.
8. **Instrumentation is an investment.** Every metric you add has a storage and maintenance cost. Start with the Four Golden Signals, expand only when you have a concrete question that existing data cannot answer.

---

## References

- Google SRE Book — Chapter 6: Monitoring Distributed Systems
- Google SRE Workbook — Chapter 5: Alerting on SLOs
- The USE Method (Brendan Gregg) — https://www.brendangregg.com/usemethod.html
- The RED Method (Tom Wilkie) — https://grafana.com/blog/2018/08/02/the-red-method-how-to-instrument-your-services/
- Prometheus Documentation — Alerting Rules: https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/
- Alertmanager Documentation: https://prometheus.io/docs/alerting/latest/alertmanager/
- Grafana Dashboard Design Best Practices: https://grafana.com/docs/grafana/latest/dashboards/
