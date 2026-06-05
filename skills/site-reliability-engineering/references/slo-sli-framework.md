# SLO / SLI Framework Reference

> Site Reliability Engineering — service level objective design and error budget management.

---

## Table of Contents

1. [Definitions](#definitions)
2. [SLI Definition Patterns](#sli-definition-patterns)
3. [SLO Target Setting Methodology](#slo-target-setting-methodology)
4. [Error Budget Mechanics](#error-budget-mechanics)
5. [Burn Rate Alerting](#burn-rate-alerting)
6. [SLO Alignment to User Journeys](#slo-alignment-to-user-journeys)
7. [Service Tiering](#service-tiering)
8. [Common Pitfalls](#common-pitfalls)
9. [Example SLO Declarations](#example-slo-declarations)

---

## Definitions

| Term | Definition |
|---|---|
| **SLI (Service Level Indicator)** | A carefully defined quantitative measure of some aspect of the service level provided. |
| **SLO (Service Level Objective)** | A target value or range for an SLI over a specified window (typically 28–30 days rolling). |
| **SLA (Service Level Agreement)** | A contractual commitment to a customer about service level, usually with consequences for non-compliance. |
| **Error Budget** | The permitted amount of unreliability over an SLO window (1 - SLO target). |

---

## SLI Definition Patterns

### 1. Latency (Request-Response)

**Definition pattern:**

```
SLI_{latency} = count of "fast enough" requests / total requests
```

**Formula:**

\[
\text{SLI}_{\text{latency}} = \frac{ \sum_{t \in T} \mathbf{1}[\, \text{latency}(t) \leq \text{threshold}\, ] }{ |T| }
\]

Where:
- `threshold` is the target latency (e.g., 200ms for p99, 100ms for median)
- Only requests counted — not internal health checks or synthetic probes unless they represent real user paths.

**Measurement approaches:**

| Approach | Description | Pros / Cons |
|---|---|---|
| **Server-side** | Instrument the service at the entry point | Direct, but includes queue wait; may miss client-side latency |
| **Client-side** | Measure from the user's device | Real user experience, but harder to collect |
| **Load balancer** | Measure at reverse proxy / API gateway | Consistent, captures network; may overcount retries |
| **Synthetic** | Periodic probing from external locations | Consistent, but may not reflect real traffic patterns |

**Common thresholds:**

| Percentile | Typical range | Use case |
|---|---|---|
| p50 (median) | 50–200 ms | General "feel" of responsiveness |
| p95 | 200–500 ms | Good user experience boundary |
| p99 | 500–2000 ms | Tail latency for user-perceived slowness |
| p99.9 | 2000–10000 ms | Hard timeout / "hanging" detection |

### 2. Availability (Uptime / Success Ratio)

**Definition pattern:**

```
SLI_{availability} = successful requests / total requests
```

**Formula:**

\[
\text{Availability} = \frac{ \text{successful\_requests} }{ \text{total\_requests} } \times 100\%
\]

Where "successful" means HTTP 2xx or application-level success, and total excludes redirected requests (3xx) when those are benign.

**For request-driven services:**

\[
A = \left(1 - \frac{\text{errors}}{\text{requests}}\right) \times 100\%
\]

**For non-request-driven services (e.g., storage, queues):**

\[
A = \frac{\text{time\_serving\_normally}}{\text{total\_time}} \times 100\%
\]

**Nines reference table:**

| Availability | Downtime / 30d | Downtime / 365d |
|---|---|---|
| 90% ("one nine") | 3.0 days | 36.5 days |
| 99% ("two nines") | 7.2 hours | 3.65 days |
| 99.9% ("three nines") | 43.2 minutes | 8.76 hours |
| 99.95% | 21.6 minutes | 4.38 hours |
| 99.99% ("four nines") | 4.32 minutes | 52.56 minutes |
| 99.999% ("five nines") | 25.9 seconds | 5.26 minutes |

### 3. Error Rate

**Definition pattern:**

```
SLI_{error\_rate} = error responses / total requests
```

**Formula:**

\[
\text{Error Rate} = \frac{ \text{HTTP 5xx} + \text{application\_level\_errors} }{ \text{total\_requests} }
\]

**Types of errors to track:**

- **HTTP 5xx** — server-side failures
- **HTTP 4xx** — client errors (generally *excluded* from availability SLIs unless the API is rejecting due to overload)
- **Application-level errors** — business logic failures (e.g., checkout declined, payment failed)
- **Latency-based errors** — requests that complete but exceed a timeout threshold
- **Silent failures** — requests that appear successful but produce incorrect results (hardest to detect; requires validation)

**Recommended:** Separate "server errors" and "application errors" into distinct SLIs. A 5xx rate > 0.1% usually warrants immediate investigation regardless of SLO.

### 4. Throughput

**Definition pattern:**

```
SLI_{throughput} = requests processed / time window
```

**Formula:**

\[
\text{Throughput} = \frac{ N_{\text{requests}} }{ \Delta t }
\]

**Use case:** Capacity planning, burst detection, saturation signals. Not typically an SLO target by itself, but used as a _service level indicator_ for scaling decisions. Set a minimum throughput SLO only when the service must handle a baseline load for correctness (e.g., a payment settlement pipeline).

### 5. Durability

**Definition pattern:**

```
SLI_{durability} = intact_objects / total_objects_over_window
```

**Formula:**

\[
D = \left(1 - \frac{\text{lost\_objects}}{\text{total\_objects}}\right) \times 100\%
\]

**Used for:** Storage systems, databases, message queues, blob stores.

**Typical targets:** 99.9999999% (nine nines — one object lost per 10^11 stored per year) to 99.99999999% (eleven nines).

Durability is generally an _overall measure_, not measured per-request, and verified through:
- Checksum verification scans
- Replica consistency checks
- Data loss replication drills

### 6. Correctness

**Definition pattern:**

```
SLI_{correctness} = correct_responses / total_responses
```

**Formula:**

\[
C = \frac{ \text{responses\_matching\_expected\_output} }{ \text{total\_responses\_validated} }
\]

**Used for:** Data pipelines, search relevance, ML inference, transaction processing.

Correctness SLIs require a _validation oracle_ — either:
- A secondary verifier (shadow comparison, canary validation)
- End-to-end consistency checks (checksums on data movement)
- User-reported error signals (support tickets, chargebacks, rollbacks)

---

## SLO Target Setting Methodology

### Step 1: Identify User Journeys

Map the critical paths users take through the system:

1. **Login → Search → View results → Select item → Add to cart → Checkout → Payment → Confirmation**
2. **Login → Dashboard → Reports → Export**

Each journey gets its own SLO(s), derived from the component SLIs that compose it.

### Step 2: Set Measurable Baselines

Before setting SLO targets, collect 2–4 weeks of SLI measurements so you understand:
- Current performance
- Natural variance (daily, weekly, seasonal)
- Known bad periods

### Step 3: Apply the "Tiered Tightening" Approach

| Iteration | Method | Example |
|---|---|---|
| Start | Set SLO 1–2 "nines" below current performance | Current: 99.85% → SLO: 99.0% |
| Tighten 1 | User-journey margin: subtract margin below baseline | Baseline: 99.9% → SLO: 99.7% |
| Tighten 2 | Dissatisfaction-based: use the point where user complaints rise | Complaint threshold: 99.5% → SLO: 99.0% |
| Final | Business constraint: must meet SLA + margin | SLA: 99.9% → internal SLO: 99.95% |

### Step 4: Choose the Window

| Window | Use case |
|---|---|
| **28-day rolling** | Standard SRE practice — aligns with error budget cycles |
| **30-day calendar** | Common for SLAs |
| **7-day rolling** | Aggressive monitoring for volatile services |
| **Quarterly** | Long-burn, slow-changing services (e.g., durability) |
| **Fixed calendar month** | Needed when SLO is tied to billing/contract periods |

### Step 5: Define the Compliance Period

Specify:
- The _measurement window_ (e.g., 28 days rolling)
- The _evaluation point_ (e.g., evaluated at end of each month)
- The _reset behavior_ (rolling window resets continuously; fixed-period resets on the 1st)

---

## Error Budget Mechanics

### Accrual

The error budget is established at the start of a compliance period:

\[
\text{Error Budget} = (1 - \text{SLO}) \times \text{total\_requests}
\]

**Example:**
- SLO = 99.9% (0.999)
- Total requests in window = 10,000,000
- Error budget = (1 - 0.999) × 10,000,000 = 10,000 errors allowed

### Consumption

Error budget is consumed by each bad event:

\[
\text{Error Budget Remaining} = \text{Error Budget} - \sum_{t \in \text{window}} \text{bad\_events}_t
\]

### Depletion Rate

\[
\text{Depletion Rate} = \frac{ \text{errors\_consumed\_so\_far} }{ \text{elapsed\_time\_in\_window} }
\]

\[
\text{Time to exhaustion} = \frac{ \text{error\_budget\_remaining} }{ \text{depletion\_rate} }
\]

### Budget Status States

| Status | Condition | Action |
|---|---|---|
| **Green** | Remaining ≥ 50% | Normal operations |
| **Yellow** | 10–50% remaining | Review upcoming releases, add conservative monitoring |
| **Red** | < 10% remaining | Freeze all non-critical deployments, prioritize reliability work |
| **Exhausted** | 0% remaining | Mandatory incident response, full reliability sprint |

### Example Calculation

| Metric | Value |
|---|---|
| SLO target | 99.9% |
| Requests / 28 days | 50,000,000 |
| Error budget | 50,000 errors |
| Errors so far (day 14) | 20,000 |
| Budget remaining | 30,000 errors (60%) |
| Depletion rate | 20,000 / 14 = 1,428.6 errors/day |
| Days until exhausted | 30,000 / 1,428.6 ≈ 21.0 days (OK) |

---

## Burn Rate Alerting

### Burn Rate Definition

\[
\text{Burn Rate} = \frac{ \text{rate of bad events} }{ \text{rate of bad events allowed by SLO} }
\]

Or more simply:

\[
\text{Burn Rate} = \frac{ \text{error\_rate} }{ 1 - \text{SLO} }
\]

A burn rate of:
- **1.0** = exactly consuming the error budget
- **2.0** = consuming budget twice as fast (will exhaust in half the window)
- **0.5** = consuming half as fast (will have surplus remaining)

### Multi-Window Burn Rate Approach

Use two or more time windows to distinguish fast, dangerous burns from slow, tolerable ones:

| Alert | Burn Rate | Short Window | Long Window | Severity | Response |
|---|---|---|---|---|---|
| **Critical** | ≥ 14.4 (or ~14x) | 1 minute | 5 minutes | Pager | Immediate on-call |
| **Warning** | ≥ 6.0 | 5 minutes | 30 minutes | Pager | Investigate |
| **Watch** | ≥ 2.0 | 30 minutes | 6 hours | Ticket | Triage within 1 hour |
| **Monitor** | ≥ 1.0 | 2 hours | 1 day | Ticket | Review within 24h |

### Multi-Window Alerting Rule (Prometheus-style)

```
groups:
  - name: slo_burn_rate
    rules:
      - alert: SLIBurnRateCritical
        expr: |
          (
            (
              rate(sli_errors_total[1m])
              / on() (rate(sli_errors_total[1m]) + rate(sli_successes_total[1m]))
            )
            / on() (1 - 0.999)
          ) >= 14.4
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Burn rate critical ({{ $value }}x)"

      - alert: SLIBurnRateWarning
        expr: |
          (
            (
              rate(sli_errors_total[5m])
              / on() (rate(sli_errors_total[5m]) + rate(sli_successes_total[5m]))
            )
            / on() (1 - 0.999)
          ) >= 6.0
        for: 5m
        labels:
          severity: warning
```

### Interpreting Burn Rate Examples

| Scenario | Window | Errors | Rate | SLO | Burn Rate |
|---|---|---|---|---|---|
| 10s outage (all requests fail) | 1 min | 1,000 | 100% | 99.9% | 1,000x |
| 2 min partial (50% failures) | 5 min | 500 | 10% | 99.9% | 100x |
| Mild degradation (5% failures) | 30 min | 1,500 | 5% | 99.9% | 50x |
| Slow drift (0.2% failures) | 6h | 720 | 0.2% | 99.9% | 2x |

---

## SLO Alignment to User Journeys

### Journey Decomposition

Every user journey is a chain of service dependencies. The aggregate SLO must account for each link:

\[
\text{Journey SLO} = \prod_{i=1}^{n} \text{Component SLO}_i
\]

**Example:** A checkout journey depends on:
- Web frontend SLO = 99.9%
- Cart API SLO = 99.95%
- Payment service SLO = 99.99%
- Inventory SLO = 99.9%

\[
\text{Checkout SLO} = 0.999 \times 0.9995 \times 0.9999 \times 0.999 \approx 0.9974 \text{ (99.74\%)}
\]

### Budget Allocation — "From the User Back"

1. Define the **user-facing SLO** first (e.g., checkout journey = 99.5%)
2. Work backwards to allocate error budgets to each component
3. Tightest budgets go to the most constrained or hardest-to-fix components

### User Journey SLI Template

```yaml
journey:
  name: "Complete Checkout"
  slo: "99.5% over 28d"
  steps:
    - name: "View Cart"
      component: frontend
      sli: latency (p95 < 500ms)
      slo: 99.9%
    - name: "Submit Order"
      component: cart-api
      sli: availability
      slo: 99.95%
    - name: "Process Payment"
      component: payment-gateway
      sli: availability + correctness
      slo: 99.99%
    - name: "Confirm Inventory"
      component: inventory-service
      sli: availability
      slo: 99.9%
```

---

## Service Tiering

### Tier 1 — Critical

| Attribute | Description |
|---|---|
| **Impact** | Revenue-critical, user-facing, or compliance-mandated |
| **SLO target** | 99.95% – 99.999% |
| **Error budget** | Very tight (0.05% – 0.001%) |
| **Alerting** | Burn rate ≥ 6 → immediate page; ≥ 2 → ticket within 1h |
| **On-call** | 24/7, < 5 min response |
| **Release gating** | Error budget must be ≥ 50% to deploy |
| **Examples** | Payment processing, authentication, search, core API, user database |

### Tier 2 — Important

| Attribute | Description |
|---|---|
| **Impact** | Significant business feature, many users affected |
| **SLO target** | 99.0% – 99.9% |
| **Error budget** | Moderate (1% – 0.1%) |
| **Alerting** | Burn rate ≥ 14 → page; ≥ 6 → ticket within 2h |
| **On-call** | Business-hours + after-hours for critical degradation |
| **Release gating** | Error budget must be ≥ 25% to deploy |
| **Examples** | Recommendations, admin dashboard, reporting, notification delivery |

### Tier 3 — Best-Effort

| Attribute | Description |
|---|---|
| **Impact** | Nice-to-have, no direct user or revenue impact |
| **SLO target** | 90% – 99% (or none) |
| **Error budget** | Generous (10% – 1%) |
| **Alerting** | Burn rate ≥ 30 → ticket next business day; otherwise monitor only |
| **On-call** | Best-effort, no formal pager duty |
| **Release gating** | None required |
| **Examples** | Internal tools, experimental features, historical data exports, log processing |

---

## Common Pitfalls

### 1. Averages Lie

> "The average latency is 150ms."

Mean latency _always_ hides tail latency. A service with p50 = 100ms and p99 = 10s has a mean of ~200ms (skewed by outliers but still deceptively low).

**Rule:** Always use percentiles for latency SLIs. Never use mean/avg.

### 2. Too Many SLIs

> "We track 47 dashboards with 120 SLIs."

Every SLI has a maintenance cost: dashboards, alerts, toil in responding to false positives. Keep the count small — start with 3-5 per service.

**Rule:** If an SLI has never triggered an action in 3 months, retire it.

### 3. Heroic Targets (Aspirational SLOs)

> "Our SLO is 99.999% availability for the developer wiki."

Setting unrealistically high targets guarantees budget exhaustion, alert fatigue, and desensitization. SLOs should be _achievable_ and _represent the user's real experience_, not a wish.

**Rule:** Set SLOs from observed data + a modest margin, not from a desire to be "five nines."

### 4. Measuring the Wrong Thing

> "Our API Gateway reports 99.99% availability, but users keep complaining."

Common mismatches:
- Measuring health-check endpoints instead of real user requests
- Excluding client-side timeouts from the SLI (the user sees a failure)
- Counting retries as independent successes
- Measuring requests that are never user-facing (internal traffic)

**Rule:** The SLI must match what the user experiences. If the user sees an error, the SLI should count it.

### 5. Ignoring Traffic Patterns

> "We had no alerts during the night… but the on-call was paged at 9 AM."

If 90% of traffic arrives in a 4-hour peak window, the error budget burns 10x faster during those hours. A flat burn rate alert across the day will miss morning meltdowns.

**Rule:** Consider time-partitioned SLIs (peak / off-peak) for services with strong diurnal patterns.

### 6. Perfection as a Target

> "We need 100% availability."

Zero-defect targets eliminate the error budget — the mechanism that makes SLOs useful. Without an error budget, every incident is an escalation and you lose the ability to trade reliability for velocity.

**Rule:** If you can't tolerate any errors, you can't use SLO-based management. Add redundancy instead.

### 7. Alert Fatigue from Burn Rate

> "We get 200 burn rate alerts per day."

Burn rate alerts are _noisy by design_ for short windows. Without multi-window gating (short window condition _and_ long window condition), you'll page on every transient blip.

**Rule:** Always pair a short window with a long window in burn rate alerting. Never alert on the short window alone.

---

## Example SLO Declarations

### Example 1: Web Service (E-commerce Frontend)

```yaml
service: storefront-web
description: "Customer-facing product browsing and cart management"
tier: Tier 1 (Critical)

slis:
  - name: "Request Latency"
    type: latency
    measurement: server-side at load balancer
    metric: http_request_duration_seconds
    good_event: p99_latency <= 500ms
    window: 28 days rolling

  - name: "Request Availability"
    type: availability
    measurement: HTTP status at load balancer
    metric: http_requests_total{status=~"2xx|5xx"}
    good_event: status_code matches 2xx
    window: 28 days rolling

  - name: "Error Rate"
    type: error_rate
    measurement: HTTP 5xx responses
    metric: http_requests_total{status=~"5xx"}
    good_event: ratio of 5xx / total < 1%
    window: 28 days rolling

slo_targets:
  - sli: "Request Latency"
    target: "p99 <= 500ms at 90% of requests over the window"
    compliance: 90%

  - sli: "Request Availability"
    target: "99.95%"
    compliance: "99.95% of requests are successful"

  - sli: "Error Rate"
    target: "error ratio < 1% sustained over 5 min"
    compliance: "measured as windowed rate"

error_budget:
  availability: 0.05% of total requests
  latency: 10% of requests can exceed 500ms

alerting:
  - name: "Critical Burn (Availability)"
    burn_rate: >= 14.0
    windows: [1m, 5m]
    severity: page
    response: "Immediate incident response"

  - name: "Warning Burn (Latency)"
    burn_rate: >= 3.0
    windows: [5m, 30m]
    severity: ticket
    response: "Investigate within 30 minutes"
```

### Example 2: Public API Service

```yaml
service: payments-api
description: "External-facing REST API for payment processing"
tier: Tier 1 (Critical)

slis:
  - name: "API Availability"
    type: availability
    measurement: edge proxy (all non-3xx responses)
    metric: api_requests_total
    good_event: status_code in [200, 201, 204]
    excludes:
      - 429 (rate limited — client error, not service failure)
      - 4xx (client validation errors)
      - 503 (deliberate maintenance mode — excluded if budgeted)
    window: 28 days rolling

  - name: "API Latency (p99)"
    type: latency
    measurement: request duration at edge proxy
    metric: api_request_duration_ms
    good_event: duration <= 1000ms
    window: 28 days rolling

  - name: "API Latency (p95)"
    type: latency
    measurement: request duration at edge proxy
    metric: api_request_duration_ms
    good_event: duration <= 300ms
    window: 28 days rolling

  - name: "Correctness"
    type: correctness
    measurement: idempotency key violations & failed rollbacks
    metric: payment_processing_errors_total
    good_event: zero correctness errors
    window: 28 days rolling

slo_targets:
  - sli: "API Availability"
    target: 99.99%

  - sli: "API Latency (p99)"
    target: "p99 <= 1000ms, 95% of the time"

  - sli: "API Latency (p95)"
    target: "p95 <= 300ms, 90% of the time"

  - sli: "Correctness"
    target: "Zero correctness errors (budget: 5 errors per window)"

error_budget:
  availability: 0.01% of total API requests (~87 errors per 1M)
  latency_p99: 5% of requests may exceed 1000ms
  latency_p95: 10% of requests may exceed 300ms
  correctness: 5 errors total per 28-day window

alerting:
  - name: "Availability Critical"
    burn_rate: >= 14.0
    windows: [1m, 5m]
    severity: page

  - name: "Latency p99 Critical"
    burn_rate: >= 6.0
    windows: [5m, 30m]
    severity: page

  - name: "Correctness Violation"
    type: count-based
    threshold: >= 1 correctness error in 1 hour
    severity: page
    response: "Immediate investigation — possible data corruption"

release_gating:
  condition: "Availability error budget remaining >= 30%"
  exception: "Emergency security patches exempt"
```

---

## Quick Reference Formulas

| Concept | Formula |
|---|---|
| Availability | \( A = \frac{\text{success}}{\text{total}} \times 100\% \) |
| Error rate | \( E = \frac{\text{errors}}{\text{total}} \) |
| Error budget | \( B = (1 - \text{SLO}) \times \text{total\_events} \) |
| Error budget consumed | \( C = \frac{\text{actual\_errors}}{\text{allowed\_errors}} \times 100\% \) |
| Budget remaining | \( R = \text{allowed\_errors} - \text{actual\_errors} \) |
| Burn rate | \( \text{BR} = \frac{\text{observed\_error\_rate}}{1 - \text{SLO}} \) |
| Time to exhaustion | \( T_{\text{exhaust}} = \frac{R}{\text{depletion\_rate}} \) |
| Journey SLO | \( \text{SLO}_{\text{journey}} = \prod_{i=1}^{n} \text{SLO}_i \) |
| Errors per nines | \( \text{errors\_allowed} = (1 - \text{SLO}) \times 10^n \) |

---

## References

- Google SRE Book — *"Service Level Objectives"* (Ch. 4)
- Google SRE Workbook — *"Implementing SLOs"* (Ch. 1–4)
- Site Reliability Engineering: Measuring and Managing Reliability — Jones et al. (O'Reilly)
- CRE Life Lessons — Google Cloud Blog series
- Error budget burn rate best practices — Google SRE (https://sre.google/workbook/alerting-on-slos/)
