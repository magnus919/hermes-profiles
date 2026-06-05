# Incident Command System (ICS) for Technology Incidents

> **Purpose:** Adapt the National Incident Management System (NIMS) / Incident Command System (ICS) — proven in emergency management — to technology and SRE incidents. This reference provides a complete framework for structured, role-based incident response in production environments.
>
> **Audience:** SREs, on-call engineers, incident commanders, engineering managers, and post-incident reviewers.

---

## Table of Contents

1. [NIMS/ICS Adapted for Tech Incidents](#1-nimsics-adapted-for-tech-incidents)
2. [Incident Command Roles](#2-incident-command-roles)
3. [Command Hierarchy and Reporting Structure](#3-command-hierarchy-and-reporting-structure)
4. [Role Handoff Protocols](#4-role-handoff-protocols)
5. [Incident Severity Classification](#5-incident-severity-classification)
6. [Communication Channels and War Room Logistics](#6-communication-channels-and-war-room-logistics)
7. [Timeline Reconstruction Methods](#7-timeline-reconstruction-methods)
8. [Decision Authority Boundaries](#8-decision-authority-boundaries)
9. [Post-Incident Actions](#9-post-incident-actions)
10. [Appendix: Role Cards](#10-appendix-role-cards)

---

## 1. NIMS/ICS Adapted for Tech Incidents

### 1.1 What is ICS?

The Incident Command System is a standardized, on-scene, all-hazards incident management approach originally developed for wildfire response in the 1970s. It was later adopted by FEMA as part of the National Incident Management System (NIMS). ICS is:

- **Scalable** — works for a 2-person database issue or a 40-person multi-service outage.
- **Modular** — only activate the roles you need.
- **Common terminology** — everyone on the call knows what "IC" means.
- **Unified command** — a single incident commander makes decisions.

### 1.2 Why ICS for Tech Incidents?

Technology incidents share critical characteristics with emergency response:

| Emergency Management | Technology Incident |
|---|---|
| Wildfire spreading | Cascading service failures |
| Multiple responding agencies | Multiple engineering teams (DB, networking, app) |
| Command post coordination | War room / bridge call |
| Situation reports (SITREPs) | Status updates to stakeholders |
| Incident Action Plans | Mitigation strategy and runbooks |
| Demobilization | Return to normal operations |
| After-action review | Post-incident review (PIR) |

### 1.3 Key ICS Principles

1. **Unity of Command** — Every person reports to exactly one supervisor.
2. **Span of Control** — Manageable ratio: 3–7 direct reports per supervisor (ideal 5).
3. **Modular Organization** — Activate only the needed functions.
4. **Incident Action Planning** — Each operational period has clear objectives.
5. **Integrated Communications** — One primary communication channel, one scribe channel.
6. **Comprehensive Resource Management** — Track who is doing what.
7. **Transfer of Command** — Formal handoff procedures for every role change.

### 1.4 ICS Organizational Chart for Tech Incidents

```
                     ┌─────────────────────┐
                     │  Incident Commander  │
                     │        (IC)         │
                     └──────────┬──────────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
     ┌────────┴────────┐ ┌─────┴──────┐ ┌───────┴────────┐
     │  Deputy / Ops   │ │ Scribe /   │ │  Comms /       │
     │     Lead        │ │ Logistics  │ │  Liaison       │
     └────────┬────────┘ └────────────┘ └────────────────┘
              │
    ┌─────────┼─────────┬──────────┬──────────┬──────────┐
    │         │         │          │          │          │
  SMEs    SMEs     SMEs     SMEs     External   Legal/
  (DB)    (Net)   (App)    (Sec)     Vendors    Compliance
```

---

## 2. Incident Command Roles

### 2.1 Incident Commander (IC)

**Tagline:** "I am the IC. I own the timeline and decisions."

The IC is the single person ultimately responsible for the incident response. They do **not** debug. They manage.

**Responsibilities:**

| Area | Details |
|---|---|
| Establish Command | Declare the incident, assign initial roles, open the war room channel. |
| Situation Assessment | Understand the scope, severity, and impact. Make the initial severity classification. |
| Strategy | Set response objectives (Isolate? Mitigate? Rollback? Fix-forward?). |
| Resource Management | Call in additional engineers, escalate to management, engage vendors. |
| Decision Authority | Approve breaking-glass actions, feature flag changes, rollbacks, traffic reroutes. |
| Communication | Provide structured updates to the scribe and liaison. Sign off on external communications. |
| Transitions | Manage role handoffs. Transfer command when shift ends or situation escalates. |
| Termination | Declare incident resolved. Approve the move from response to recovery. |

**What the IC should be saying:**
- "I am now the Incident Commander."
- "What is the current impact? How many users/customers?"
- "What have we tried? What's the next best action?"
- "Scribe, note this decision: we are rolling back v2.14.1 to v2.13.9."
- "I am handing off IC to Sarah. Sarah, you have command."

**What the IC should NOT be doing:**
- SSHing into servers
- Writing code
- Looking at dashboards for more than 30 seconds
- Getting into technical rabbit holes

### 2.2 Deputy / Operations Lead

**Tagline:** "I run the technical response so the IC can command."

The Operations Lead (or Deputy IC) manages the technical execution of the response plan. This is the senior technical person who coordinates the SMEs.

**Responsibilities:**

| Area | Details |
|---|---|
| Technical Coordination | Triage incoming issues, assign tasks to SMEs, track what's been tried. |
| Runbook Execution | Ensure standard runbooks are followed; adapt if they don't fit. |
| Parallel Work | Split the team: "Alice, check the database. Bob, look at the CDN. Carol, examine the app logs." |
| Situation Updates | Feed concise technical status to the IC every few minutes or on significant changes. |
| Handoffs | Brief incoming operations lead so technical context isn't lost. |

**What Ops should be saying:**
- "IC, here's my assessment: it's a database connection pool exhaustion."
- "Alice, you're on DB replication lag. Bob, you're on app error rates."
- "We tried restarting the primary. No change. Next step: failover to replica."

### 2.3 Scribe / Logistics

**Tagline:** "I write down everything so nobody has to remember."

The Scribe is the historian and logistics coordinator. This is arguably the second most important role after IC. In many incidents, the IC also scribes for the first few minutes until a scribe is found.

**Responsibilities:**

| Area | Details |
|---|---|
| Timeline Logging | Record every action, decision, observation with timestamps. |
| Decision Documentation | Capture key decisions and the rationale behind them. |
| Action Tracking | Maintain a running list of open actions, who owns them, and status. |
| Resource Logistics | Coordinate conference bridges, war room access, tool credentials, food. |
| Shift Management | Track who is on-call and when shift changes should happen. |
| Session Recording | Record the bridge call / war room chat for post-incident review. |

The scribe produces the **incident log** — the raw timestamped record that becomes the backbone of the post-incident review.

**What the Scribe should be saying:**
- "Can you repeat that decision? I want to capture the rationale."
- "Current action items: 1) Alice — test failover. 2) Bob — check DNS propagation."
- "IC, we've been in incident for 47 minutes. Do you want to escalate to the VP?"

**Log entry format:**
```
[T+00:05] IC declares SEV-2 incident — API latency above 5s p99
[T+00:07] Alice assigned to check database connection pool
[T+00:09] Decision: roll back frontend from v42 to v41 (IC approved)
[T+00:12] Bob reports: DB pool at 100%, connections not releasing
```

### 2.4 Comms / Liaison

**Tagline:** "I keep everyone who isn't on this call informed."

The Communications / Liaison role manages the external communication channels. This is the buffer between the incident response team and the rest of the organization (and possibly customers).

**Responsibilities:**

| Area | Details |
|---|---|
| Internal Status Updates | Send regular updates to the #incident-status channel, email distribution lists, or Slack. |
| Stakeholder Management | Brief executives, product managers, and customer success. |
| External Communication | Draft and coordinate customer-facing status page messages (e.g., Statuspage). |
| Escalation Notification | Alert on-call managers, VPs, and the CTO as per severity escalation policy. |
| FAQ Management | Collect common questions from stakeholders and provide consistent answers. |

**Communication cadence:**

| Severity | Internal Updates | External Status Page |
|---|---|---|
| SEV-1 | Every 15 minutes | Every 30 minutes |
| SEV-2 | Every 30 minutes | Only if customer-visible |
| SEV-3 | At key milestones | Not required |
| SEV-4 | Once at resolution | Not required |
| SEV-5 | Not required | Not required |

**What Comms should be saying:**
- "IC, the VP of Engineering is asking for a status update. What can I share?"
- "Status page updated: 'We are investigating increased latency on the API.'"
- "Next internal update due in 5 minutes. IC, do you have anything new?"

### 2.5 Subject Matter Experts (SMEs)

**Tagline:** "I fix things. Tell me what to look at."

SMEs are the engineers doing the hands-on technical work. They report to the Operations Lead.

**Responsibilities:**

| Area | Details |
|---|---|
| Investigation | Diagnose the issue in their domain (database, networking, application, security). |
| Mitigation | Execute mitigation actions — restarts, rollbacks, config changes, traffic re-routing. |
| Reporting | Report findings clearly to Ops Lead: "What I found, what I tried, what I recommend." |
| Runbook Execution | Follow standard operating procedures; escalate when they don't apply. |

**SME types commonly needed:**

| SME | Domain |
|---|---|
| Database SME | Replication, connection pooling, query performance, failover |
| Networking SME | DNS, BGP, CDN, load balancers, firewall rules |
| Application SME | Service code, deployment pipeline, feature flags, configuration |
| Security SME | Intrusion detection, DDoS, access control anomalies |
| Infrastructure SME | Kubernetes, cloud provider, CI/CD pipelines, observability stack |
| Vendor SME | Third-party SaaS dependencies (Datadog, PagerDuty, cloud provider support) |

---

## 3. Command Hierarchy and Reporting Structure

### 3.1 Who Reports to Whom

```
                                    Incident Commander (IC)
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    │                      │                      │
              Ops Lead              Scribe/Logistics         Comms/Liaison
                    │
     ┌──────────────┼──────────────┬──────────────┐
     │              │              │              │
  DB SME      App SME        Net SME       Sec SME
```

### 3.2 Reporting Rules

1. **SMEs report to Ops Lead, not to IC.** If an SME has an update, they tell Ops. Ops filters and escalates to IC.
2. **The IC does not assign tasks directly to SMEs.** The IC tasks Ops; Ops tasks SMEs.
3. **Anyone can speak up if they have critical safety/security information.** The chain bypasses only for imminent danger.
4. **Comms does not report technical details directly to the IC's command chain.** Comms gets their content from the scribe log and IC briefings.

### 3.3 Span of Control

- IC to direct reports: 3–5 (Ops Lead, Scribe, Comms, plus any direct stakeholders like Legal if needed).
- Ops Lead to SMEs: 3–7, ideally 5.
- If the incident requires more than 7 SMEs, split into functional teams (e.g., "DB team," "Networking team") each with their own lead reporting to Ops.

### 3.4 Unified Command (Multi-Organization Incidents)

When the incident spans multiple organizations (e.g., a cloud provider outage affecting your service, or a joint incident with a partner company), a **Unified Command** structure may be used:

- Each organization designates an IC.
- The ICs form a unified command team that makes joint decisions.
- Each IC is responsible for their organization's resources.
- A single spokesperson is designated for external communications.

---

## 4. Role Handoff Protocols

Role handoffs are a critical failure point in incident management. A poorly performed handoff can lose context, decisions, and momentum. Every handoff must be explicit and documented.

### 4.1 General Handoff Principles

1. **Verbal declaration**: The outgoing person explicitly says "I am handing off [ROLE] to [NAME]."
2. **Confirmation**: The incoming person explicitly says "I have accepted [ROLE]."
3. **Scribe records it**: The exact handoff time is logged.
4. **Overlap**: A 3–5 minute overlap period (longer for IC) where the outgoing person is available for questions.
5. **State transfer**: All relevant context is transferred (see checklists below).

### 4.2 IC Handoff Protocol

**When to hand off IC:**
- End of shift (e.g., after 4–6 hours in a prolonged incident)
- Escalation to a more senior engineer or manager
- Fatigue or cognitive overload
- Original IC was the first responder and needs to step back

**IC Handoff Checklist:**

| Step | Action |
|---|---|
| 1 | Outgoing IC announces: "I am handing off IC to [NAME]." |
| 2 | Outgoing IC briefs incoming IC on: current situation, actions taken, decisions made, open tasks, pending escalations, stakeholder status. |
| 3 | Outgoing IC reviews the timeline log with the incoming IC. |
| 4 | Scribe timestamps: "IC transferred from [OUT] to [IN] at [TIME]." |
| 5 | Incoming IC announces to the channel/call: "I am now the Incident Commander." |
| 6 | Outgoing IC remains available for 5 minutes as a resource, then stands down. |
| 7 | Comms updates any stakeholder channels that the IC has changed. |

**IC Handoff briefing template:**
```
--- IC HANDOFF BRIEFING ---
Current severity: [SEV-1]
Situation: [one paragraph summary]
What we know: [bullet points]
What we don't know: [bullet points]
Actions taken: [bullet points]
Open actions: [who is doing what]
Key decisions made: [bullet points]
Pending decisions: [bullet points]
Stakeholders notified: [list]
Escalations needed: [yes/no - to whom]
Risks: [any new risks identified]
```

### 4.3 Ops Lead Handoff Protocol

**Ops Lead Handoff Checklist:**

| Step | Action |
|---|---|
| 1 | Announce: "I am handing off Ops Lead to [NAME]." |
| 2 | Transfer: current technical assessment, what's been tried, what's pending, SME assignments. |
| 3 | Introduce incoming Ops Lead to each SME. |
| 4 | Scribe timestamps the handoff. |
| 5 | Incoming Ops Lead confirms acceptance. |

### 4.4 Scribe Handoff

**Scribe Handoff Checklist:**

| Step | Action |
|---|---|
| 1 | Current scribe shares the running log document with the incoming scribe. |
| 2 | Brief on: format conventions, any shorthand used, pending log entries, tools (the document, recording, etc.). |
| 3 | Tandem log for 2–3 minutes to ensure format continuity. |
| 4 | Scribe timestamps the handoff in the log. |

### 4.5 Comms Handoff

**Comms Handoff Checklist:**

| Step | Action |
|---|---|
| 1 | Transfer: current status message drafts, stakeholder contact list, communication schedule, pending external updates. |
| 2 | Share any feedback received from stakeholders. |
| 3 | Share the scribe log link and the latest approved status message. |
| 4 | Announce the handoff to stakeholders if appropriate. |

### 4.6 Shift Schedules for Extended Incidents

| Duration | Shift Pattern |
|---|---|
| 1–2 hours | Single team |
| 2–4 hours | Single team, consider backup |
| 4–8 hours | Two-team rotation: IC + Ops switch at 4h mark |
| 8–24 hours | Three-team rotation: 8h shifts for IC/Ops/Comms |
| 24+ hours | Full team rotation: complete handoff every 8-12h, rest period for outgoing team |

---

## 5. Incident Severity Classification

### 5.1 SEV Definitions

| Level | Label | Definition | Examples |
|---|---|---|---|
| **SEV-1** | Critical | Complete service outage or severe degradation affecting a significant portion of users. Data loss or security breach. | • Entire site/app down<br>• Customer data accessible to unauthorized users<br>• Payment processing completely broken<br>• Core API returning 500s for all requests |
| **SEV-2** | Major | Significant impairment of core functionality affecting many users but not a total outage. | • Major feature non-functional<br>• Severe latency (>5x normal, >5% of users)<br>• Partial regional outage<br>• Degraded but still operational with workarounds |
| **SEV-3** | Minor | Isolated issue affecting a subset of users or non-critical functionality with acceptable workaround. | • Minor feature broken<br>• Slight latency increase<br>• Cosmetic issues<br>• Single-user or single-tenant issue |
| **SEV-4** | Informational | No user impact. Operational issue that should be investigated during business hours. | • Non-critical alert firing<br>• Slightly elevated error budget consumption<br>• Internal tool issue<br>• Bug with no user-facing impact |
| **SEV-5** | Scheduled / Maintenance | Planned work that has been communicated and approved. No user-facing impact expected. | • Scheduled maintenance<br>• Database migration<br>• Deployment of new feature<br>• Planned failover testing |

### 5.2 Response Time Targets

| Severity | Initial Response | Update Cadence | MITR Target | Escalation |
|---|---|---|---|---|
| SEV-1 | Immediate (<2 min) | Every 15 min internal, 30 min external | <1 hour | VP/Director within 15 min, CTO within 30 min |
| SEV-2 | Within 5 min | Every 30 min internal | <4 hours | Manager within 30 min, Director within 1 hour |
| SEV-3 | Within 30 min | At key milestones, or daily | <24 hours | Team lead within 1 business day |
| SEV-4 | Next business day | Upon resolution | <1 week | None required |
| SEV-5 | At scheduled time | Per change plan | N/A | Per change management process |

### 5.3 Severity Change Protocol

Severity can change during an incident. The process:

1. IC assesses that severity has changed (upgraded or downgraded).
2. IC announces: "We are upgrading from SEV-2 to SEV-1."
3. Scribe records the change.
4. Comms notifies the appropriate escalation contacts for the new severity.
5. All response cadences adjust to the new severity level.

### 5.4 Escalation Chain Example

```
SEV-3 ──> Team Lead ──> Engineering Manager
SEV-2 ──> Engineering Manager ──> Director of Engineering  
SEV-1 ──> Director of Engineering ──> VP of Engineering ──> CTO / CEO
```

| Role | Contact Method | Response SLO |
|---|---|---|
| Primary On-Call | PagerDuty push + SMS + phone | Acknowledge: 2 min |
| Engineering Manager | Phone call, Slack ping | Acknowledge: 5 min |
| Director of Engineering | Phone call | Acknowledge: 15 min |
| VP of Engineering | Phone call | Acknowledge: 30 min |
| CTO | Phone call | Per VP discretion |

---

## 6. Communication Channels and War Room Logistics

### 6.1 Channel Architecture

| Channel | Purpose | Who Has Access |
|---|---|---|
| **Primary Incident Channel** (e.g., Slack #inc-1234) | Real-time coordination, decisions, updates | All incident responders |
| **Scribe Log** (e.g., Google Doc, HackMD, GitHub issue) | Timestamped record of every action/decision | All incident responders |
| **Status Updates** (e.g., Slack #incident-status) | Read-only broadcasts to the wider org | Organization-wide |
| **External Status Page** (e.g., Statuspage) | Customer-facing status | Public |
| **Bridge / Zoom** | Voice coordination | Incident responders + stakeholders by invitation |
| **Backchannel** (e.g., DM, separate Slack channel) | Comms to specific vendors or sensitive discussions | IC + relevant parties |

### 6.2 Channel Naming Convention

```
#inc-<YYYYMMDD>-<brief-description>
Examples:
#inc-20250605-api-latency-spike
#inc-20250605-db-primary-failover
#inc-20250605-security-breach-alert
```

### 6.3 War Room Logistics Checklist

**Immediate (first 5 minutes):**
- [ ] Establish primary incident Slack channel
- [ ] Set up voice bridge / Zoom room
- [ ] Assign initial roles (even if someone wears multiple hats)
- [ ] Create scribe document and share link in channel
- [ ] Pin the scribe doc and bridge link to the channel
- [ ] Announce the incident severity

**First 15 minutes:**
- [ ] Confirm all needed SMEs are on the call
- [ ] Add escalation contacts (if needed for severity)
- [ ] Set up status page (if customer-facing)
- [ ] Begin timeline log in scribe document

**Ongoing:**
- [ ] Rotate scribe every 30–45 minutes (scribe fatigue is real)
- [ ] Keep the incident channel focused — move side conversations to threads or DMs
- [ ] Post a mandatory "no non-incident chatter" message
- [ ] IC reviews the timeline log every 30 minutes for accuracy
- [ ] Comms posts regular updates to stakeholders

### 6.4 Communication Templates

**Initial notification (Slack / PagerDuty):**
```
:rotating_light: INCIDENT DECLARED :rotating_light:
Title: [Brief description]
Severity: SEV-[1-5]
IC: [Name]
Channel: #inc-[date]-[description]
Scribe doc: [link]
Bridge: [link]
Impact: [brief description of user/customer impact]
```

**Status update template (internal):**
```
=== STATUS UPDATE #[N] ===
Time: [UTC timestamp]
Duration so far: [X hours, Y minutes]
Severity: SEV-[X] (unchanged/changed from SEV-[Y])
Current status: [Investigating / Mitigating / Monitoring / Resolved]
Summary: [brief paragraph]
Next update: [time or milestone]
```

**Resolution announcement:**
```
✅ INCIDENT RESOLVED
Title: [title]
Duration: [X hours, Y minutes]
Severity: SEV-[X]
Root cause: [brief description]
Action taken: [brief description]
Monitoring: [what we're watching]
Post-incident review: [link when available]
```

---

## 7. Timeline Reconstruction Methods

### 7.1 Real-Time Scribing (Gold Standard)

The simplest and most reliable method is having a dedicated scribe logging in real time.

**What to log:**
- Each timestamped observation
- Each action taken (and by whom)
- Each decision made (and the IC who made it)
- Each change in severity
- Each role change or handoff
- Each escalation
- Each external communication sent

**Tool options:**

| Tool | Pros | Cons |
|---|---|---|
| Google Docs | Real-time collaborative, familiar | Can lag with many editors, merge conflicts |
| HackMD / HedgeDoc | Real-time markdown, lightweight | Less familiar to non-technical users |
| Dedicated incident platform (FireHydrant, PagerDuty, Blameless) | Structured, integrates with alerting | Requires setup, not always available |
| Git + Markdown | Permanent, reviewable, CI-friendly | Higher friction, no real-time collaboration |
| Slack thread | Fast, zero setup | Hard to reconstruct later, easy to lose context |
| Voice recording (transcribed) | Captures everything | Requires transcription, harder to search |

### 7.2 Post-Incident Reconstruction

If real-time scribing was incomplete, reconstruct the timeline from these sources:

| Source | What It Provides |
|---|---|
| Monitoring / Dashboards | Metric graphs with timestamps (latency, error rates, throughput) |
| Alerting System (PagerDuty, Opsgenie) | First alert timestamp, escalation history |
| Log Aggregator (Splunk, Datadog Logs, ELK) | Error logs, access logs, application logs |
| Deployment System (Spinnaker, ArgoCD, GitHub Actions) | Deployment timestamps, version changes |
| Feature Flag System (LaunchDarkly) | Flag toggle timestamps |
| Change Management System | Change request timestamps and approvals |
| Chat History (Slack, Teams) | All incident channel messages with timestamps |
| Voice Recording / Transcript | Everything said on the bridge call |
| Git History | Code changes, reverts, commit messages |
| Incident Comm System | Scribe log (if any), status updates |

### 7.3 Timeline Reconstruction Process

1. **Collect all sources** — Gather monitoring screenshots, chat logs, deployment logs.
2. **Create a shared timeline document** with a spreadsheet-like format.
3. **Merge data chronologically** — Each source contributes events with timestamps.
4. **Identify gaps** — Periods where no data exists. These are areas to investigate in the PIR.
5. **Validate with participants** — Ask the people on the call to fill in gaps.
6. **Flag uncertain timestamps** — Use `[~HH:MM]` notation for approximate times.
7. **Produce final timeline** — Clean, sorted, with clear event categories.

**Timeline format:**
```
| Timestamp (UTC) | Event | Source | Category |
|---|---|---|---|
| 14:02:00 | PagerDuty alert: API p99 latency >5s | PagerDuty | Alert |
| 14:02:30 | On-call engineer acknowledges | PagerDuty | Response |
| 14:03:15 | Incident declared SEV-2 | Engineer | Decision |
| 14:04:00 | #inc-20250605-api-latency created | Slack | Logistics |
| ... | ... | ... | ... |
```

### 7.4 Timeline Categories

Use consistent event categories to make analysis easier:

| Category | Color / Tag | Examples |
|---|---|---|
| Alert | 🔴 | PagerDuty alert fired, threshold exceeded |
| Detection | 🟡 | Someone noticed, user report, monitoring dashboard |
| Decision | 🔵 | IC made a decision, severity change, strategy shift |
| Action | 🟢 | Rollback executed, server restarted, config changed |
| Communication | 🟣 | Status page updated, exec notified, customer emailed |
| Escalation | 🟠 | Manager called in, vendor contacted, legal notified |
| Resolution | ✅ | Incident declared resolved, monitoring confirmed stable |

---

## 8. Decision Authority Boundaries

### 8.1 Decision Authority Matrix

| Decision | Authority | Consultation Needed |
|---|---|---|
| Declare incident | First responder / IC | None |
| Assign severity | IC | None (but can be challenged) |
| Change severity | IC | None |
| Roll back a deployment | IC | Ops Lead, code owner |
| Feature flag change | IC / Ops Lead | Feature owner if available |
| Restart a database primary | IC | Ops Lead, DB SME |
| Failover to replica/region | IC | Ops Lead, DB SME |
| Scale up infrastructure | IC / Ops Lead | Cloud cost owner (if time permits) |
| Change DNS / routing | IC | Net SME |
| Disable a service | IC | Ops Lead, service owner |
| Contact a vendor for support | IC / Ops Lead | Vendors team |
| Communicate externally | Comms (with IC approval) | Legal (for SEV-1), PR (if customer-facing) |
| Contact legal / compliance | IC | None |
| Contact law enforcement (security breach) | IC + Legal | Executive team |
| Declare incident resolved | IC | Ops Lead confirms mitigation stable |
| Authorize post-incident review | IC | None |
| Deploy a hotfix | IC | Ops Lead, code owner, QA (if time permits) |
| Cache invalidation / purge | Ops Lead | Net SME |
| Database query kill / terminate | Ops Lead / DB SME | IC (if impact is broad) |

### 8.2 "Break Glass" Decisions

Certain actions carry high risk but may be necessary. These require explicit IC approval and scribe documentation:

**Break glass actions:**
- Force-restarting a database primary
- Dropping database connections / killing queries
- Disabling authentication or security controls
- Bypassing change management for a deployment
- Manual edits to production data
- Rolling back a database migration
- Hard reboot of infrastructure hosts

**Break glass protocol:**
1. SME says: "I recommend we do [action]. This is a break-glass action with risk [description]."
2. IC asks: "What happens if this fails? What's our rollback?"
3. IC decides. If approved: "Approved. Scribe, log this. Let's proceed."
4. If declined: "Not approved. What's our alternative? Ops Lead, any other options?"
5. Scribe records the decision and rationale regardless of outcome.

### 8.3 Authority Outside Business Hours

During off-hours/weekends, the on-call IC has broader authority:

- Can approve emergency change requests without standard change management
- Can escalate to any level of management (including VP/CTO) without waiting
- Can authorize spending for emergency infrastructure scaling
- Can call in additional engineers from any team

After-hours authority is checked by:
- Mandatory scribe documentation of all decisions
- Post-incident review within 1 business day
- Right-to-challenge by the on-call manager

### 8.4 What the IC Cannot Do Alone

Even the IC has limits:

- Cannot unilaterally terminate employees or contractors
- Cannot make binding legal commitments or admissions of liability
- Cannot disclose customer data outside the incident response team
- Cannot authorize payment to vendors without the finance team (unless pre-approved)
- Cannot override a security hold without security lead concurrence
- Cannot authorize data deletion without documented legal/compliance consultation

---

## 9. Post-Incident Actions

### 9.1 Immediate Actions (Within 1 Hour of Resolution)

| Action | Owner | Details |
|---|---|---|
| Verify mitigation | Ops Lead | Confirm the fix is holding and monitoring is green |
| Declare resolved | IC | Announce in incident channel: "Incident is resolved. Moving to recovery." |
| Change severity to SEV-5 | IC | The incident is now a monitoring/recovery phase |
| Update status page | Comms | Set status page to "Resolved" |
| Stop the recording / close bridge | IC | End the voice bridge |
| Send final status update | Comms | Send the resolution announcement |
| Save all materials | Scribe / IC | Archive the scribe doc, channel history, monitoring screenshots |
| Pause non-critical alerts | IC | Prevent alert fatigue from residual effects |
| Determine monitoring period | IC | How long before we're confident the fix is stable? |

### 9.2 Short-Term Follow-Up (Within 1 Business Day)

| Action | Owner | Details |
|---|---|---|
| Schedule post-incident review | IC or designate | Book 60–90 min within 3–5 business days |
| Complete timeline | Scribe / IC | Fill in any gaps in the timeline from logs and monitoring |
| Triage action items | IC | Create a tracker of all follow-up actions from the incident |
| Assign owners | IC | Every action item needs an owner and due date |
| Create incident ticket | IC | File in the incident tracking system with severity, duration, summary |
| Preserve evidence | Scribe | Collect dashboards, logs, outputs before they expire |
| Notify affected customers | Comms + Legal | Send customer communication if applicable |
| File any required reports | IC / Legal | Regulatory or compliance reporting if applicable |

### 9.3 Post-Incident Review (PIR)

**PIR Schedule:**

| Severity | PIR Required | Timeline | Participants |
|---|---|---|---|
| SEV-1 | Yes | Within 5 business days | All responders, engineering manager, director |
| SEV-2 | Yes | Within 10 business days | All responders, engineering manager |
| SEV-3 | As needed | Within 2 weeks | Team lead and relevant engineers |
| SEV-4 | Optional | N/A | Team lead |
| SEV-5 | No | N/A | N/A |

**PIR Agenda (60–90 minutes):**

| Section | Time | Facilitator |
|---|---|---|
| 1. Set the stage | 5 min | Facilitator (not the IC!) |
| 2. Timeline walkthrough | 20 min | Scribe / IC |
| 3. What went well | 10 min | All participants |
| 4. What went wrong | 15 min | All participants |
| 5. What was confusing | 10 min | All participants |
| 6. Action item generation | 10 min | All participants |
| 7. Summary and next steps | 5 min | Facilitator |

**PIR Principles (Blameless Postmortem):**
- Assume good intent from everyone
- Focus on systems, not individuals
- The goal is learning, not accountability for the incident
- Every action item should be a system change (runbooks, automation, monitoring, architecture)
- Track action items to completion with owners and due dates

**PIR Output Document:**

```markdown
# Post-Incident Review: [Title]

**Incident ID:** INC-YYYY-MM-DD-XXX
**Date:** YYYY-MM-DD
**Duration:** Xh Ym
**Severity:** SEV-X
**Services affected:** [list]

## Timeline
[UTC timestamps of key events]

## Impact
- Users affected: [count or percentage]
- Revenue impact: [if measurable]
- Duration: [total outage or degradation time]

## Root Cause
[Clear description of the root cause]

## Trigger
[What set off the incident]

## Detection
[How was it first detected? How long from occurrence to detection?]

## Response
[What worked well in the response? What didn't?]

## What Went Well
- [item]
- [item]

## What Went Wrong
- [item]
- [item]

## What Was Confusing
- [item]
- [item]

## Action Items
| # | Action | Owner | Due Date | Status |
|---|---|---|---|---|
| 1 | ... | ... | ... | Open |
| 2 | ... | ... | ... | Open |
```

### 9.4 Action Item Tracking

Action items from the PIR must be tracked to completion:

| Severity of Incident | Action Item Due |
|---|---|
| SEV-1 | Critical: within 30 days |
| SEV-2 | Major: within 60 days |
| SEV-3 | Minor: within 90 days |
| SEV-4/5 | Optional: next planning cycle |

**Action item tracker columns:**
- ID
- Description
- Owner
- Due date
- Status (Open / In Progress / Done / Won't Do)
- Linked incident
- Priority

### 9.5 Incident Data Retention

| Artifact | Retention Period |
|---|---|
| Scribe log | 1 year |
| Chat history | 1 year |
| Monitoring screenshots | 90 days |
| Voice recording | 30 days (or as required by compliance) |
| Post-incident review | 2 years |
| Action item tracker | Until all items closed + 1 quarter |

---

## 10. Appendix: Role Cards

### Role Card: Incident Commander (IC)

The Incident Commander is the single decision-maker responsible for the entire incident response. They do not debug, do not SSH into servers, and do not chase metrics. Instead, they maintain the big picture: understanding the scope and severity of the incident, setting response strategy, managing resources and escalations, and making all key decisions. The IC approves break-glass actions, communicates the response strategy to the scribe and liaison, and ultimately decides when the incident is resolved. They are accountable for the safety of the response and for ensuring that the right people are working on the right problems. In extended incidents, the IC manages shift rotations and role handoffs to prevent responder fatigue.

### Role Card: Deputy / Operations Lead

The Operations Lead (also called Deputy IC or Ops Lead) runs the technical side of the response so the IC can focus on command. They receive technical updates from Subject Matter Experts, triage incoming information, and assign investigation and mitigation tasks. The Ops Lead maintains the technical picture — what has been tried, what is currently being investigated, and what the next-best technical action should be. They filter and summarize technical status for the IC in concise, actionable updates. In a large incident, the Ops Lead may delegate sub-teams (e.g., a database team, a networking team), each with their own lead. The Ops Lead role requires deep technical experience and the ability to think clearly under pressure.

### Role Card: Scribe / Logistics

The Scribe is the historian of the incident, responsible for maintaining a real-time, timestamped log of every observation, action, decision, role change, escalation, and communication. They produce the raw timeline that becomes the backbone of the post-incident review. The Scribe also handles logistics — setting up and maintaining the war room (bridge lines, Slack channels, shared documents), tracking open action items, managing shift schedules, and ensuring the incident runs smoothly. Because scribe fatigue builds quickly, this role should rotate every 30–45 minutes in prolonged incidents. A good scribe captures decisions and the rationale behind them, asking "Can you repeat that for the log?" when things move fast.

### Role Card: Comms / Liaison

The Communications and Liaison role is the buffer between the incident response team and the outside world. They send regular status updates to internal stakeholders (Slack channels, email lists) and draft customer-facing messages for the status page. They field incoming questions from executives, product managers, customer success, and support teams, providing consistent, approved information without distracting the incident responders. The Comms role tracks the communication cadence required by the incident severity and ensures that every stakeholder who needs to know is informed. No external communication goes out without IC approval, and the Comms person never speculates — they only share confirmed facts.

### Role Card: Database SME

The Database Subject Matter Expert is responsible for diagnosing and resolving database-related issues during an incident. This includes investigating connection pool exhaustion, replication lag, slow queries, locked tables, disk space issues, and failover scenarios. The DB SME reports findings to the Operations Lead in a structured format: what they found, what they tried, and what they recommend. They execute database restarts, failovers, query terminations, index rebuilds, and scaling operations under the direction of the Ops Lead and with IC approval for break-glass actions. In major incidents, the DB SME also assesses whether the database issue is the root cause or a symptom of a broader problem.

### Role Card: Networking SME

The Networking SME handles all network-layer issues during an incident. This includes DNS resolution failures, BGP routing problems, CDN configuration errors, load balancer misconfigurations, firewall rule blocks, DDoS attacks, and VPN or connectivity issues. They use tools like traceroute, dig, curl, cloud provider network consoles, and observability platforms to pinpoint network faults. They report to the Operations Lead and recommend actions such as DNS record changes, traffic rerouting, CDN purges, or WAF rule adjustments. The Networking SME also coordinates with external providers (cloud providers, CDNs, ISPs) when the incident involves their infrastructure.

### Role Card: Application SME

The Application SME investigates and resolves issues in the application code and runtime. This includes debugging error spikes, analyzing application logs, reviewing recent deployments, toggling feature flags, checking configuration files, and assessing whether a rollback or hotfix is needed. They work closely with the deployment and CI/CD pipelines and may coordinate with the code owners for specific services. The Application SME reports to the Operations Lead with clear findings ("Service X is throwing 500s because config parameter Y is invalid") and recommended actions ("Roll back service X to version 1.2.3"). They may also implement temporary mitigations like circuit breakers or rate limiting.

### Role Card: Security SME

The Security SME handles any incident with a security component: suspected breaches, unauthorized access, DDoS attacks, data exfiltration indicators, compromised credentials, or vulnerability exploitation. They prioritize containment over investigation — the first question is always "How do we stop the bleeding?" The Security SME coordinates with the IC on breach notification requirements, interfaces with legal and compliance as needed, and preserves forensic evidence (logs, system snapshots, network captures) for later analysis. They may advise on bringing in additional security tooling, rotating credentials, or isolating compromised systems. The Security SME has the authority to raise a security concern even if it changes the incident classification.

### Role Card: Infrastructure / Cloud SME

The Infrastructure SME manages issues at the cloud provider or data center level: instance failures, auto-scaling group problems, Kubernetes cluster issues, storage volume problems, and cloud API throttling. They handle infrastructure-level escalations to cloud provider support (AWS, GCP, Azure) and manage infrastructure-as-code tooling (Terraform, Pulumi, CloudFormation). The Infrastructure SME assesses whether the issue is localized to specific availability zones or regions and recommends infrastructure-level mitigations such as scaling up instance counts, moving workloads to healthy zones, or initiating disaster recovery procedures.

### Role Card: Vendor SME

The Vendor SME handles incidents involving third-party SaaS dependencies — either as the root cause (e.g., Datadog is down, PagerDuty is not delivering alerts, a cloud provider has an Availability Zone failure) or as part of the mitigation (e.g., contacting Fastly support for cache issues, rotating API keys for an external service). They maintain contacts and support plans for all critical vendors, know the escalation paths for each vendor, and track vendor SLAs during the incident. The Vendor SME coordinates with the Ops Lead to determine whether the organization should implement a workaround or wait for the vendor to resolve the issue on their end.

---

## Quick Reference Card

### First 60 Seconds

```
1. TAKE A DEEP BREATH
2. "I am now the Incident Commander."
3. "What is the impact? How many users?"
4. Assign Scribe (even if it's you initially).
5. Declare severity: SEV-1/2/3/4/5.
6. Open channel + bridge + scribe doc.
7. "Scribe, start the timeline."
```

### During the Incident

```
IC should ask every 5-10 minutes:
  - "What's the current impact?"
  - "What have we tried?"
  - "What's the next action?"
  - "Do we need more people?"
  - "Scribe, did you get that last decision?"
```

### At Resolution

```
1. Verify monitoring is green. (Ops Lead)
2. "Incident is resolved." (IC)
3. Update status page to "Resolved." (Comms)
4. Final status update to stakeholders. (Comms)
5. Save all materials. (Scribe)
6. Schedule post-incident review. (IC)
7. Log the incident in the tracking system. (IC)
```

---

*This document is a reference for SRE teams adopting structured incident command. Adapt severity definitions, escalation chains, and response times to your organization's specific service levels, team structure, and regulatory requirements.*
