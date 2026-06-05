# On-Call Best Practices Reference

> **Audience:** Site Reliability Engineers, Infrastructure Engineers, DevOps practitioners
> **Purpose:** Comprehensive reference for designing, operating, and improving on-call rotations
> **Last Updated:** 2026-06-05

---

## Table of Contents

1. [Rotation Design](#1-rotation-design)
2. [Response SLAs](#2-response-slas)
3. [Workload Caps](#3-workload-caps)
4. [Balance and Fairness](#4-balance-and-fairness)
5. [Cognitive Load Management](#5-cognitive-load-management)
6. [Escalation Paths and Policies](#6-escalation-paths-and-policies)
7. [Tools and Infrastructure](#7-tools-and-infrastructure)
8. [Handoff Best Practices](#8-handoff-best-practices)
9. [Training and Onboarding](#9-training-and-onboarding)
10. [Underload Prevention](#10-underload-prevention)
11. [When On-Call Isn't Working](#11-when-on-call-isnt-working)

---

## 1. Rotation Design

### Primary / Secondary Model

Every rotation should have at least two tiers to provide redundancy and support:

- **Primary on-call:** First responder. Paged first, responsible for acknowledging and triaging all alerts within the defined SLA. Handles day-to-day operational incidents and escalations.
- **Secondary / Shadow:** Backup to the primary. Pages if the primary does not acknowledge within the SLA window (typically 2-3 minutes for critical alerts). The secondary is also a designated support channel — the primary can escalate to them for complex incidents requiring additional investigation or a second set of eyes.
- **Tertiary / Escalation:** Senior engineer or team lead. Paged only after both primary and secondary have missed acknowledgements. Also serves as the management escalation for high-severity incidents (SEV-0 / SEV-1).

For teams smaller than 5 people, a single primary with a floating secondary that rotates weekly is often the most practical arrangement. For teams of 6 or more, maintain a dedicated primary and dedicated secondary on separate rotations.

### Team Sizing Math

The size of an on-call rotation is governed by the relationship between shift length, team size, and time spent on-call. Use the following formulas to determine minimum safe team sizes.

**On-Call Frequency Formula:**

```
OnCallPercentage = (ShiftLengthDays / RotationLengthDays) x 100

Where:
  ShiftLengthDays = Number of consecutive days a single engineer is primary
  RotationLengthDays = ShiftLengthDays x TeamSize
  TeamSize = Number of engineers in the rotation pool
```

**Example calculations:**

- 4 engineers, 7-day shifts: each engineer is on-call 25% of the time (7/28 = 25%)
- 6 engineers, 7-day shifts: each engineer is on-call ~16.7% of the time (7/42 ≈ 16.7%)
- 3 engineers, 7-day shifts: each engineer is on-call ~33% of the time (7/21 ≈ 33%) — *high risk of burnout*
- 8 engineers, 24-hour shifts: each engineer is on-call ~12.5% of the time but with daily context-switching overhead

**Minimum Viable Team Size Formula:**

```
MinTeamSize = ceil(ShiftLengthDays / (MaxOnCallDaysPerYear / 365))

Where MaxOnCallDaysPerYear is a policy choice (recommended max: 91 days, or 25%)
```

With a 25% annual cap and 7-day shifts:

```
MinTeamSize = ceil(7 / (91 / 365)) = ceil(7 / 0.249) = ceil(28.1) = 29 ... (WRONG formula approach)
```

Correct pragmatic approach — given a shift length S and a target maximum on-call percentage P (as a decimal), the minimum team size N is:

```
N = ceil(1 / P)
```

For P = 0.25 (25% cap): N = ceil(1 / 0.25) = **4 engineers minimum**
For P = 0.20 (20% target): N = ceil(1 / 0.20) = **5 engineers minimum**
For P = 0.125 (12.5% ideal): N = ceil(1 / 0.125) = **8 engineers minimum**

**Recommended minimum team sizes:**

| Shift Length | Min Team Size (25% cap) | Ideal Team Size (12.5%) |
|--------------|------------------------|-------------------------|
| 24 hours     | 4                      | 8                       |
| 7 days       | 4                      | 8                       |
| 14 days      | 4                      | 8                       |

**Important caveat:** These formulas assume equal distribution. They do not account for holidays, sick leave, PTO, or training time. Add a buffer of at least 1-2 extra engineers to account for real-world availability gaps.

### Follow-the-Sun Model

For global teams operating across time zones, the follow-the-sun (FTS) model provides 24/7 coverage without requiring any single engineer to carry overnight shifts:

- **Region A (APAC):** Covers 00:00-08:00 UTC — primary for that time window
- **Region B (EMEA):** Covers 08:00-16:00 UTC — primary for that time window
- **Region C (AMER):** Covers 16:00-00:00 UTC — primary for that time window

Each region has its own rotation (typically 3-5 engineers per region). Handoffs occur at the region boundaries with structured shift-change processes. FTS works best when each region has sufficient engineering presence to maintain independent operations and shared ownership of the global infrastructure.

**Key requirements for FTS success:**

- At least 3 geographic hubs with 3+ engineers each
- Synchronized runbooks and dashboards across all regions
- Shared incident documentation standards
- Regular cross-region sync meetings (at least bi-weekly)
- Explicit handoff protocols at shift boundaries

### Optimal Shift Length

The optimal shift length balances coverage continuity against engineer fatigue:

- **24-hour shifts (follow-the-sun):** Best for global teams where "night" is never the same person's problem. High context but disruptive to personal rhythm.
- **7-day shifts (weekly):** The industry standard at most SRE organizations (Google, Meta, etc.). Good balance of context continuity and recovery time. Recommended as the default for most teams.
- **12-hour shifts (day/night split):** Useful when overnight coverage is needed but follow-the-sun isn't feasible. Typically 3-4 consecutive 12-hour days before rotation.
- **14-day shifts (bi-weekly):** May be acceptable for low-alert-volume services with small teams, but carries significantly higher fatigue risk. Not recommended for high-traffic or critical systems.

**General guidance:** Weekly (7-day) shifts are the strongest default. If your team exceeds 25% time on-call with weekly shifts, hire more engineers rather than extending shift length.

---

## 2. Response SLAs

Response SLAs define how quickly on-call engineers must acknowledge and respond to alerts. These are not resolution SLAs — they measure *response* time, not *fix* time.

### SLA Tiers

| Severity | Label          | Acknowledgement SLA | Response SLA       | Typical Scenarios                                   |
|----------|----------------|---------------------|--------------------|-----------------------------------------------------|
| SEV-0    | Critical       | 2 minutes           | 5 minutes          | Complete service outage, data loss, security breach |
| SEV-1    | High           | 5 minutes           | 15 minutes         | Major feature degradation, partial outage           |
| SEV-2    | Medium         | 10 minutes          | 30 minutes         | Minor degradation, non-critical feature broken      |
| SEV-3    | Low            | 30 minutes          | 2 hours            | Non-urgent issues, cosmetic problems, noise alerts  |
| SEV-4    | Informational  | Best effort         | Next business day  | Log entries, low-priority notifications             |

**Critical (SEV-0) — 5 minutes:** The engineer must acknowledge the page and begin investigation within 5 minutes. Services at this severity should have redundant alerting paths (email + SMS + phone call) and automated escalation if not acknowledged within 2 minutes.

**Standard (SEV-2) — 30 minutes:** The standard tier for most production alerts. Engineers have enough time to finish a context switch but are still expected to respond promptly.

### SLA Enforcement

- Track acknowledgement and response times against SLAs for every alert
- Use automated reporting (weekly/monthly) to identify:
  - Engineers routinely missing SLAs (training or burnout risk)
  - Alerting systems with delayed delivery (infrastructure issue)
  - Overly aggressive SLAs on non-critical alerts (tuning opportunity)
- SLA misses should trigger a post-incident review, not punitive action

### SLA Math: Coverage Requirements

To meet a 5-minute critical response SLA with 99.9% reliability:

```
P(miss) = 0.001
Required number of responders k such that P(all miss) <= 0.001

If each engineer has a 95% chance of acknowledging within 5 minutes:
  P(engineer_i misses) = 0.05
  P(primary misses) = 0.05
  P(secondary misses) = 0.05
  P(both miss) = 0.05 x 0.05 = 0.0025 = 0.25%

  This gives 99.75% reliability — above 99.9% requires a third tier:
  P(all three miss) = 0.05^3 = 0.000125 = 0.0125%
  This gives 99.9875% reliability
```

**Practical takeaway:** Two-tier escalation (primary + secondary) is sufficient for almost all teams. Add a third tier only for the most critical services where a missed page has regulatory or safety implications.

---

## 3. Workload Caps

Unlimited on-call workload leads directly to burnout, turnover, and incident mishandling. Enforce hard caps on both incident volume and time commitment.

### Incident Volume Caps

- **Maximum 2 active incidents per shift:** If a third incident occurs while two are already being handled, the secondary must take the new incident, or the shift must be split (page a third engineer from the rotation pool). This prevents "incident stacking" where an engineer is overwhelmed by simultaneous events.
- **Maximum 4 incidents per 24-hour period:** Beyond four incidents, the engineer should be relieved from on-call duty regardless of shift length. The rotation pool or secondary should cover the remainder.
- **Post-incident recovery time:** After any SEV-0 or SEV-1 incident resolution, the engineer should be given at least 30 minutes of quiet time for write-ups and cognitive recovery before being expected to handle another incident.

### Time Commitment Caps

- **Maximum 25% of working time on-call:** No engineer should be primary for more than 25% of their total working hours averaged over a quarter. This is the Google SRE standard and is widely adopted across the industry.
- **Maximum 12 hours of incident response in a single shift:** If incidents consume more than 12 hours of a 24-hour on-call shift, the engineer must be relieved.
- **No back-to-back on-call shifts:** Ensure at least one full shift length (e.g., one week) of non-on-call time between rotations.
- **Maximum 3 consecutive on-call weeks per quarter:** Even if the 25% average is met, no engineer should serve more than 3 weeks of primary on-call in any 13-week quarter.

### Escalation When Caps Are Hit

When any cap is reached, the escalation path must trigger automatically:

1. Primary hits cap -> Secondary takes over all new pages
2. Secondary hits cap -> Tertiary or rotation pool manager pages a volunteer
3. Rotation pool exhausted -> Engineering manager is paged to find coverage
4. Manager cannot find coverage -> Director-level escalation for staffing rebalance

---

## 4. Balance and Fairness

An on-call rotation is only sustainable if it is perceived as fair by every member of the team. Inequity — whether real or perceived — destroys morale and drives attrition.

### Distribution Tracking

Track and publish the following metrics for every engineer each quarter:

| Metric                          | Description                                           |
|---------------------------------|-------------------------------------------------------|
| Total on-call hours             | Cumulative hours as primary and secondary             |
| Number of pages received        | Raw count of alert notifications                      |
| Number of incidents handled     | Distinct incidents (ignoring repeat alerts)           |
| Incident hours                  | Total time spent investigating/resolving              |
| After-hours incidents           | Pages received outside core business hours            |
| Holiday/weekend coverage count  | Number of holidays or weekend days covered            |

These metrics should be visible to the entire team via a shared dashboard. Transparency is the foundation of trust in the rotation.

### Fairness Principles

1. **Equal rotation frequency:** Every engineer in the pool should rotate through on-call at the same frequency, absent exceptional circumstances (medical leave, bereavement, etc.).
2. **Equal holiday distribution:** Holiday on-call should be rotated equitably year-over-year. Maintain a running tally of holiday coverage and give preference to engineers with lower counts.
3. **Equal weekend distribution:** Weekend shifts should be evenly distributed. No engineer should carry more than 2 weekend shifts per quarter.
4. **Credit for secondary duty:** Time spent as secondary should count toward on-call metrics at some weighted value (e.g., 0.5x primary time) to acknowledge the cognitive load of backup responsibility.

### Fatigue Prevention

Fatigue is the single largest risk to on-call effectiveness. Implement these safeguards:

- **Minimum rest period:** No on-call duty within 8 hours of a prior incident that lasted more than 2 hours. Enforce this programmatically if possible.
- **Swap approval:** All rotation swaps must be approved by the rotation manager to prevent a single engineer from accumulating excessive swaps (which can indicate avoidance or burnout).
- **Mandatory timeout:** After handling 3 SEV-0 or SEV-1 incidents in a single week, the engineer is automatically cycled out of the rotation for at least one week.
- **Post-on-call recovery day:** The day after an on-call shift ends, the engineer should have no meetings before noon (for weekly shifts) or should take a "no meetings" day (for longer shifts).

---

## 5. Cognitive Load Management During Incidents

Incident response is cognitively demanding. High stress, incomplete information, time pressure, and multitasking degrade decision-making quality. Managing cognitive load is an operational imperative.

### The Incident Commander Model

Adopt a clear role structure during incidents to distribute cognitive load across multiple people:

- **Incident Commander (IC):** The single person responsible for coordinating response. Does NOT touch any systems. Focuses entirely on communication, timeline, resource allocation, and decision-making.
- **Operations Lead:** The technical lead doing the actual investigation and remediation. Reports status to the IC. Should not be distracted by communication or coordination tasks.
- **Scribe:** Maintains the incident timeline, records all actions taken, and documents decisions. Critical for post-incident reviews.
- **Subject Matter Experts (SMEs):** Called in as needed for specific subsystems. Should be briefed by the Operations Lead and then given focused tasks.
- **Communications / Liaison:** If the incident is customer-facing, a designated person handles status updates to stakeholders so the IC and Operations Lead can focus.

Even in smaller teams where one person wears multiple hats, explicitly state hats at the beginning of an incident: "I am the IC for this incident. Alice, you are Operations. Bob, please scribe."

### Decision Fatigue Countermeasures

- **Runbooks first:** Always check the runbook before making novel decisions. Runbooks reduce cognitive load by providing pre-vetted paths.
- **Time-box investigation:** After 30 minutes without progress, escalate or change approach. Stale investigation loops waste cognitive energy.
- **Defer non-critical decisions:** If a decision is not time-sensitive, write it down and make it after the incident is resolved.
- **Use decision trees:** Build incident decision trees that branch based on symptoms, guiding the engineer step by step without requiring recall of rare procedures.

### Post-Incident Cognitive Recovery

An incident isn't over when the service is restored. Cognitive recovery requires structured decompression:

- Mandatory 15-minute break after incident resolution before starting the postmortem
- Post-incident reviews as blameless learning exercises, not fault-finding
- Encourage exercise, hydration, and walking away from the keyboard after a severe incident
- Manager check-in within 24 hours of a SEV-0 or SEV-1 incident to assess engineer well-being

---

## 6. Escalation Paths and Policies

Every service must have a documented, tested, and well-understood escalation path.

### Escalation Chain

```
Level 0: Primary On-Call Engineer
  -> Acknowledges within SLA, attempts resolution using runbooks
  -> If stuck > 15 min: calls in Secondary

Level 1: Secondary On-Call Engineer  
  -> Collaborates with Primary on investigation
  -> Can triage to appropriate SME if needed
  -> Pages Tertiary if incident scope exceeds team capacity

Level 2: Tertiary / Domain Expert / Team Lead
  -> Provides technical guidance or access to specialized systems
  -> Can authorize emergency changes that bypass normal review

Level 3: Engineering Manager
  -> Decision-making authority for resource allocation
  -> Handles cross-team coordination
  -> Decides on extended outage communications

Level 4: Director / VP
  -> Only for SEV-0 or extended SEV-1 (>4 hours)
  -> Business continuity decisions
  -> External stakeholder communication
```

### Escalation Timing Rules

| Situation                                         | Escalate After   |
|---------------------------------------------------|------------------|
| Primary doesn't acknowledge page                  | 2-3 minutes      |
| Primary acknowledges but makes no progress        | 15 minutes       |
| Incident requires expertise outside team          | Immediately      |
| Primary suspects security incident                | Immediately      |
| Incident duration exceeds 1 hour                  | Page Manager     |
| Incident duration exceeds 4 hours                 | Page Director    |
| Customer-affecting incident during business hours | Page Comms team  |

### Policies

- **No blame for escalation:** Engineers must never be penalized for escalating. The cost of a false escalation is negligible compared to the cost of a delayed response.
- **When in doubt, escalate:** If an engineer is unsure whether escalation is warranted, they should escalate. The receiving engineer can always downgrade.
- **Automated escalation:** Configure paging software to automatically escalate after acknowledgement timeout, regardless of engineer action.
- **Document every escalation:** Each escalation event must be recorded in the incident log with timestamp, reason, and outcome. This data informs rotation and training improvements.

---

## 7. Tools and Infrastructure

### Pager Setup and Configuration

- **Primary channel:** Mobile push notification via a dedicated on-call app (PagerDuty, Opsgenie, Grafana OnCall, or similar)
- **Fallback channel:** SMS for all SEV-0 and SEV-1 alerts
- **Final fallback:** Phone call for SEV-0 only (or if SMS not acknowledged within 2 minutes)
- **Escalation timing:** 2-minute delay between primary and escalation tiers
- **Override scheduling:** All PTO, holidays, and planned absences must be entered into the scheduling system at least 2 weeks in advance
- **Calendar integration:** Sync on-call schedule to team calendar so everyone knows who is currently on duty

### Runbooks

Every alert that pages a human must have a corresponding runbook. A runbook is not optional — it is the minimum bar for a well-operated service.

**Required runbook content:**

- Alert name and description
- Severity classification
- Step-by-step investigation procedure (with specific dashboards, queries, and commands)
- Common causes and their telltale symptoms
- Remediation steps for each known cause
- Escalation criteria and contacts
- Service dependencies and responsible teams
- Links to relevant dashboards, logs, and monitoring
- Time estimates for each remediation step

**Runbook maintenance:**

- Review and update every runbook at least quarterly
- Automated testing where possible (e.g., validate that linked dashboards and queries still return data)
- After any incident that reveals a gap in a runbook, update the runbook within 48 hours
- Runbooks should be version-controlled alongside service code

### War Rooms

For major incidents, a war room (virtual or physical) concentrates the response team in a single communication channel.

**Virtual war room setup:**

- Dedicated Slack/Discord channel auto-created on SEV-0 declaration
- Bot auto-posts: current time, affected service, severity, primary/seconary names
- Pin the timeline, investigation notes, and current action items
- Only the IC posts status updates to prevent noise
- All non-essential communication happens in a thread

**Physical / Zoom war room:**

- Join a dedicated video call with screensharing
- Mute all non-speaking participants
- Use a shared document for structured note-taking (Decision Log format)
- Designate a timekeeper to announce every 15-minute interval

---

## 8. Handoff Best Practices

The handoff between on-call engineers is a high-risk moment. Information that lives in one person's head but not in the runbooks or dashboards is lost if not explicitly transferred.

### Structured Handoff Process

**15 minutes before shift change:**

1. **Review active incidents:** Go through every open incident with the outgoing engineer. Understand the current state, what has been tried, and what the next steps are.
2. **Pass known issues:** Is there anything brewing? A deployment in progress? A cron job about to run? Known flaky tests or odd monitoring behavior?
3. **Review dashboards:** Quickly scan the key service health dashboards together.
4. **Share context:** Recent changes (deployments, config changes, infrastructure modifications) that might affect on-call.
5. **Check the schedule:** Who is the secondary? Are there any known absences in the next few days?
6. **Acknowledge transfer:** Both engineers acknowledge the handoff in the scheduling system.

**Handoff documentation template:**

```
HANDOFF: [Date] [Time] [Time Zone]
FROM: [Outgoing Engineer]
TO: [Incoming Engineer]

ACTIVE INCIDENTS:
  - [#12345] Brief description, current status, next step

PENDING ITEMS:
  - Deployment of v2.3.1 expected at 14:00, watch for increased error rates
  - Database migration scheduled for 02:00 UTC

RECENT CHANGES:
  - Config change on api-gateway at 11:30 (rolled back, monitoring still active)

KNOWN ISSUES:
  - Flaky test in CI pipeline, may generate false-positive alerts
  - Elevated latency on us-east-1 during peak hours (under investigation)

SECONDARY ON-CALL: [Name]
```

### Overlap Requirements

- Minimum 15-minute overlap between primary shifts
- Minimum 30-minute overlap for cross-region handoffs (time zone differences)
- No handoff-by-email — must be synchronous (voice or video call + shared screen)

### Post-Handoff

The outgoing engineer remains "on-call" for their shift's open incidents for an additional 30 minutes (the "tail period") to ensure continuity. After 30 minutes, all responsibility formally transfers.

---

## 9. Training and Onboarding

New engineers should not be placed on the primary on-call rotation until they demonstrate operational competence. Rushing this process endangers both the service and the engineer's well-being.

### Shadowing Program

**Phase 1 — Observation (2-4 weeks):**
- Shadow the current primary on-call during all alerts
- Read every page notification, observe the response, read the runbook
- No responsibility — purely observational
- Goal: Understand alert patterns, service architecture, and team processes

**Phase 2 — Supervised (4-6 weeks):**
- Shadow engineer takes the first action on every page under direct supervision of the primary
- Primary reviews and approves/escalates every decision
- Shadow keeps their own incident log for feedback discussion
- Goal: Build procedural memory through guided practice

**Phase 3 — Secondary rotation (4 weeks):**
- New engineer rotates as secondary (backup) for one full rotation cycle
- Can be promoted to primary if no critical misses occur during this period
- Goal: Validate independence in a low-risk role

### Ramp-Up Schedule

| Phase                | Duration     | Role            | Success Criteria                          |
|----------------------|--------------|-----------------|-------------------------------------------|
| Shadowing            | 2-4 weeks    | Observer        | Can explain each alert and response       |
| Supervised practice  | 4-6 weeks    | Supervised      | Handles 80%+ of pages without help        |
| Secondary rotation   | 4 weeks      | Backup          | No SLA misses, demonstrates good judgment |
| Primary (initial)    | 2 weeks      | Primary (light) | Reduced rotation frequency at first       |
| Full rotation        | Ongoing      | Primary         | Full rotation inclusion                   |

### Wheel of Misfortune

The Wheel of Misfortune is a rotational training exercise where engineers practice incident response in a simulated environment:

- **Format:** Weekly or bi-weekly, 45-60 minutes
- **Setup:** Simulated incident scenario using a staging environment or tabletop exercise
- **Execution:** A random engineer is spun as the "on-call" and must respond to the scenario in real-time
- **Evaluation:** Peers observe and provide feedback on the response process, communication, and runbook usage
- **Rotation:** Different engineer each session; each engineer participates at least once per quarter

**Scenario library:** Maintain a library of 20+ scenarios based on real past incidents. Pull from this library randomly so the scenarios are not anticipated.

---

## 10. Underload Prevention

The flip side of on-call burnout is **underload** — long stretches with no pages that lead to skill degradation, complacency, and rust. Both extremes are dangerous.

### Keeping Skills Fresh

- **The 10% Rule:** If an engineer receives fewer than 2 pages per shift on average, they should proactively spend 10% of their on-call time on readiness activities (see below).
- **Scheduled system exploration:** During quiet periods, engineers should explore the monitoring dashboards, review recent changes, and trace through the systems they're responsible for.
- **Runbook refreshers:** Re-read the top 5 runbooks for the service. Once you know them cold, review the less common ones.
- **Regular practice:** The Wheel of Misfortune becomes even more important for teams with low alert volumes.

### Active Readiness Activities

Engineers with no active incidents should rotate through these tasks during their on-call shift:

1. **Dashboard review:** Spend 15 minutes reviewing each major service dashboard. Notice any trends, anomalies, or degraded metrics that haven't yet triggered alerts.
2. **Runbook verification:** Pick one runbook and verify every link, command, and query still works. File bugs for broken items.
3. **Alert audit:** Review the last 7 days of alerts. Any that were false alarms? Any that were legitimate but had no runbook?
4. **Monitoring gap analysis:** Are there failure modes that should have alerts but don't? Create tickets for missing coverage.
5. **Capacity review:** Check resource utilization trends — are any services approaching capacity limits?
6. **Documentation updates:** Fix stale documentation discovered during shift.

### DiRT Drills (Disaster Recovery Testing)

DiRT drills are planned exercises that simulate catastrophic failure scenarios to test team readiness:

- **Frequency:** At least quarterly per critical service
- **Scope:** Ranges from single-service failure to full-region outage
- **Execution:** Varies from tabletop walkthroughs to actual chaos engineering experiments (e.g., Chaos Monkey)
- **Outcome:** Each drill produces an action-item list of gaps found in runbooks, monitoring, or system design
- **Post-drill:** Fix identified gaps within the next sprint cycle

**Sample DiRT scenarios:**
- Primary database region becomes unavailable
- TLS certificate expires across all services
- Kubernetes control plane is unreachable for 30 minutes
- A bad deployment rolls out affecting 50% of traffic
- Secrets management system is compromised

---

## 11. When On-Call Isn't Working

Even the best-designed on-call system will show signs of strain over time. Recognize the symptoms early and intervene before they become chronic.

### Give Back the Pager

It is every engineer's right — and responsibility — to escalate concerns about the on-call system. This should be a supported, blameless process:

**When an engineer should signal distress:**
- Consistently missing SLA targets despite good-faith effort
- Dreading on-call shifts (anxiety, sleep disruption, avoidance behavior)
- Incident volume is interfering with day-job responsibilities
- Feeling inadequately prepared for the services on-call
- Multiple consecutive rotations with high incident count

**The "Give Back the Pager" protocol:**

1. Engineer notifies their manager that on-call is not working
2. Manager immediately finds coverage for the next rotation (no questions asked)
3. A structured conversation follows to identify root causes:
   - Is the engineer undertrained?
   - Are alerts excessive or poorly tuned?
   - Is the rotation schedule unfair?
   - Are there personal circumstances affecting availability?
4. An action plan is created with specific timelines
5. Engineer returns to on-call only after the action plan is executed and the engineer agrees they are ready

This process should be documented in team charter and reinforced by management as a positive signal (self-awareness and responsibility), not a negative one.

### Alert Tuning

If on-call engineers are complaining about alert volume or noise, the solution is almost never "the engineer needs to deal with it" — it is to tune the alerting.

**Common alerting problems and solutions:**

| Symptom                                  | Likely Cause                       | Fix                                                |
|------------------------------------------|------------------------------------|----------------------------------------------------|
| Too many pages per shift                 | Thresholds too sensitive           | Raise thresholds, add debouncing, use rate-of-change |
| Same page fires repeatedly               | No auto-acknowledge or dedup       | Implement alert deduplication and flapping detection |
| Pages during clearly understood patterns | Known issue, but no suppression    | Add maintenance windows or known-issue suppression |
| Alert fires but no actionable response   | Missing runbook or too vague       | Either add a runbook or remove the alert entirely  |
| Pager goes off during business hours for the same alerts every day | Alerts should be tickets, not pages | Downgrade to SEV-3/SEV-4 or convert to daily digest |
| "False alarm" rate > 50%                 | Alert logic is poor                | Investigate and fix each false-positive pattern    |

**The golden rule of alert tuning:** Every page should represent a real, actionable condition that requires a human within the defined SLA. If an alert does not meet this criteria, it should be removed, not tolerated.

### Collaboration with Dev Teams

Chronic on-call pain is often a symptom of systemic issues in how operational responsibility is shared between development and operations teams:

**Principles for healthy dev/SRE collaboration on on-call:**

1. **You build it, you run it (or close to it):** Development teams should participate in on-call for their own services. This creates a feedback loop — if your code pages you at 3 AM, you will write more resilient code.
2. **Error budgets:** Dev teams get a budget for acceptable error rates. If error budget is exhausted, no new features — only reliability work. This ties operational health directly to development decisions.
3. **Shared on-call:** In some organizations, dev and SRE engineers share the rotation for a service. This ensures both sides understand the operational reality.
4. **Pre-release operational readiness review:** Before a new service or major feature goes live, the team must pass an operational readiness checklist:
   - Runbooks exist and are tested
   - Monitoring and alerting covers known failure modes
   - Capacity planning is completed
   - Performance benchmarks are established
   - Escalation contacts are identified
5. **Blameless postmortems with dev ownership:** When an incident is caused by a code change, the postmortem action items should be owned by the dev team, not the SRE team. SREs support reliability improvements but should not be the sole implementors.

### When to Redesign the Rotation

Some problems cannot be fixed by incremental tuning. Signs that a rotation redesign is needed:

- Attrition due to on-call stress exceeds 15% per year
- More than 30% of on-call shifts require manager intervention to fill
- Average time to acknowledge pages exceeds SLA targets by 2x or more
- Engineers consistently cite on-call as their top source of dissatisfaction in surveys
- The team has grown or shrunk significantly but the rotation hasn't changed

**Rotation redesign triggers a structured process:**

1. Collect 6 months of on-call metrics (page volume, incident types, SLA performance, distribution)
2. Survey all engineers in the rotation about their experience, pain points, and suggestions
3. Design 2-3 alternative rotation models
4. Socialize the alternatives with the team and gather feedback
5. Pick the best model and pilot it for 1 full rotation cycle
6. Evaluate the pilot with metrics and surveys before committing

---

## Appendix: Quick Reference Checklist

### Weekly On-Call Checklist

- [ ] Verify the rotation schedule — confirm I am primary/secondary
- [ ] Check the alerting system — confirm contact methods are configured
- [ ] Check for active incidents from the prior shift
- [ ] Read the handoff doc from the outgoing engineer
- [ ] Review any upcoming deployments or maintenance windows
- [ ] Confirm secondary's contact info and availability
- [ ] Review the top 5 runbooks for my primary service

### Daily On-Call Checklist

- [ ] Review new alerts from the past 24 hours (even if acknowledged by auto-resolution)
- [ ] Scan key dashboards for anomalies
- [ ] Check for any scheduled changes or maintenance
- [ ] Review incident queue for any stale/in-progress items
- [ ] Update handoff doc at end of shift

### Quarterly On-Call Health Check

- [ ] Review on-call distribution metrics for the quarter
- [ ] Survey the team on on-call satisfaction (anonymous)
- [ ] Update and test all critical runbooks
- [ ] Conduct at least one DiRT drill
- [ ] Review and tune alert thresholds
- [ ] Audit escalation paths and contacts — are they still correct?
- [ ] Evaluate rotation schedule against team size changes
- [ ] Plan holiday coverage for the next quarter

---

## References and Further Reading

- Google SRE Books: *Site Reliability Engineering* and *The Site Reliability Workbook* (especially chapters on On-Call, Incident Response, Postmortem)
- *Seeking SRE* by David N. Blank-Edelman (Conference proceedings on SRE culture)
- *Incident Management for Operations* by Rob Schnepp, Ron Vidal, and Chris Hawley
- *The Checklist Manifesto* by Atul Gawande (for runbook design principles)
- PagerDuty Best Practices Guide for On-Call Scheduling
- Grafana On-Call Documentation: Incident Management Playbooks

---

> **Maintainer Note:** This document is a living reference. Review and update it at least quarterly as team practices, tools, and service architecture evolve. The most dangerous runbook is the one that contains stale, incorrect, or outdated guidance.
