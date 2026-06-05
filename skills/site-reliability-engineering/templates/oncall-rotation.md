# On-Call Rotation Schedule Template

| Metadata | Value |
|---|---|
| **Team** | [Team Name / SRE] |
| **Schedule Owner** | [SRE Manager / Rotation Coordinator] |
| **Version** | 1.0 |
| **Last Updated** | [YYYY-MM-DD] |

---

## 1. Calendar Pattern

### 1.1 Rotation Structure

The on-call rotation follows a [weekly / biweekly / daily] shift pattern with **three tiers**:

| Tier | Role | Coverage | Response Time SLA |
|---|---|---|---|
| **Primary** | First responder | [24/7 / Business hours / Follow-the-sun] | [X minutes] |
| **Secondary** | Escalation / Backup | Overlapping with Primary | [Y minutes] |
| **Escalation** | Engineering management / SMEs | 24/7 as needed | [Z minutes] |

### 1.2 Rotation Schedule

```
Rotation Group A → Rotation Group B → Rotation Group C → Rotation Group A ...
```

Each rotation group consists of:
- **[1]** Primary Engineer(s)
- **[1]** Secondary Engineer(s)
- **[1]** Escalation Contact (Manager / Senior Engineer)

| Group | Primary | Secondary | Escalation | Rotation Period |
|---|---|---|---|---|
| Group A | [Name] | [Name] | [Name] | [Start Date] – [End Date] |
| Group B | [Name] | [Name] | [Name] | [Start Date] – [End Date] |
| Group C | [Name] | [Name] | [Name] | [Start Date] – [End Date] |

### 1.3 Time Zone Coverage

- **Business Hours (Local):** [e.g., 09:00 – 17:00 UTC / 09:00 – 17:00 ET]
- **After-Hours:** [e.g., 17:00 – 09:00 UTC]
- **Weekend Coverage:** [e.g., Full 48-hour shift / Rotating weekend coverage]
- **Follow-the-Sun Handoff:** [Primary shifts between US/EU/APAC regions]

### 1.4 Calendar Management

- All rotation assignments are managed in [Calendar System, e.g., Google Calendar / PagerDuty / OpsGenie].
- Calendar invites are sent [7 / 14] days before the shift begins.
- Swaps must be reflected in the calendar and the scheduling tool.

---

## 2. Shift Handoff Protocol

### 2.1 Handoff Timing

| Type | Time | Duration |
|---|---|---|
| Daily handoff (business hours) | [Time, e.g., 16:00 local] | [15 min] |
| Weekly handoff (rotation change) | [Day and Time, e.g., Monday 10:00 UTC] | [30 min] |
| Exception / Escalation handoff | As needed | [15 min] |

### 2.2 Handoff Communication Checklist

The outgoing engineer **must** communicate the following during handoff:

- [ ] **Active incidents** — List all open incidents with status, severity, and current actions.
- [ ] **Resolved incidents** — Any incidents that occurred during the shift and their resolution.
- [ ] **Ongoing investigations** — Items being actively investigated that did not result in an incident ticket.
- [ ] **Pending alerts** — Any alert conditions that are active but not yet triaged.
- [ ] **Recent changes** — Deployments, config changes, or infrastructure changes during the shift.
- [ ] **Known issues** — Non-urgent issues, tech debt, or known behavior that may cause future alerts.
- [ ] **Maintenance windows** — Any planned maintenance during the incoming shift.
- [ ] **Documentation updates** — Any new runbooks, playbooks, or wiki pages created or updated.
- [ ] **Tools / access issues** — Any problems with monitoring, alerting, or access that need attention.
- [ ] **General notes** — Anything else the incoming engineer should know.

### 2.3 Handoff Meeting Format

1. Outgoing engineer reviews the handoff log.
2. Walk through open incidents and alerts on the [Monitoring Dashboard].
3. Review any changes deployed or pending.
4. Transfer ownership of any communication threads.
5. Update the on-call status in [Status System, e.g., Slack status / PagerDuty].
6. Confirm that the [On-Call Phone / Pager] has been transferred.
7. Outgoing engineer remains available for [30 minutes] after handoff for questions.

### 2.4 Handoff Log

Maintain a handoff log at [Link to Handoff Document or Wiki Page] that captures:

```
Date: [YYYY-MM-DD]
Outgoing Engineer: [Name]
Incoming Engineer: [Name]
Active Incidents:
  - INC-######: [Description, Severity, Status]
Resolved Incidents:
  - INC-######: [Description, Resolution]
Pending Alerts: [List]
Changes Deployed: [List]
Known Issues: [List]
Action Items: [List]
Handoff Verified By: [Name]
```

---

## 3. Escalation Chain

### 3.1 Standard Escalation Path

```
  Primary On-Call (Tier 1)
      │ Response within [X] minutes
      ↓
  Secondary On-Call (Tier 2)
      │ Response within [Y] minutes
      ↓
  Engineering Manager / SRE Lead (Tier 3)
      │ Response within [Z] minutes
      ↓
  Director of Engineering / VP (Tier 4)
      │ Response within [W] minutes
      ↓
  Incident Commander / Executive Team (Tier 5)
```

### 3.2 Escalation Contacts

| Tier | Role | Contact Name | Phone | Email / Slack |
|---|---|---|---|---|
| Tier 1 | Primary On-Call | [Name / Role] | [+1-555-...] | [@slack-handle] |
| Tier 2 | Secondary On-Call | [Name / Role] | [+1-555-...] | [@slack-handle] |
| Tier 3 | SRE Manager | [Name] | [+1-555-...] | [email / @slack] |
| Tier 4 | Engineering Director | [Name] | [+1-555-...] | [email / @slack] |
| Tier 5 | VP of Engineering | [Name] | [+1-555-...] | [email / @slack] |

### 3.3 Non-Response Escalation

If the Primary On-Call does not acknowledge an alert within [X] minutes:
1. Alert re-fires to Secondary On-Call.
2. If Secondary does not acknowledge within [Y] minutes, alert goes to Tier 3.
3. Each subsequent tier follows the same escalation timer.
4. If all tiers are unresponsive for [Z] total minutes, the [Major Incident Protocol] is triggered.

---

## 4. On-Call Responsibilities

### 4.1 During the Shift

- [ ] Respond to all alerts within the defined SLA.
- [ ] Triage and classify incidents (severity, impact, urgency).
- [ ] Mitigate or resolve incidents per established runbooks.
- [ ] Log all actions in the incident management system.
- [ ] Maintain the handoff log.
- [ ] Update on-call status (Slack status, PagerDuty, etc.).
- [ ] Perform proactive monitoring checks at least every [N] hours.
- [ ] Attend daily standup / handoff meetings.
- [ ] Escalate when appropriate — do not hesitate.

### 4.2 Not During the Shift

- [ ] No deployment or change duties (unless explicitly coordinating).
- [ ] No major project work — focus on incident readiness.
- [ ] Respond to critical pages within [X] minutes, even during off-hours.
- [ ] Maintain situational awareness of ongoing incidents and changes.

### 4.3 Post-Shift Responsibilities

- [ ] Complete the handoff for the incoming engineer.
- [ ] Follow up on any incomplete investigations or incident tasks.
- [ ] Ensure incident tickets are properly documented and closed.
- [ ] Submit any runbook or documentation updates discovered during the shift.
- [ ] Participate in postmortem reviews for incidents that occurred during the shift.

---

## 5. Incident Response SLAs

| Severity | Description | Acknowledge Time | Response Time | Update Frequency | Resolution Target |
|---|---|---|---|---|---|
| **P0 — Critical** | Service down, data loss, security breach | [2 min] | [5 min] | Every [15 min] | [2 hours] |
| **P1 — Major** | Feature impairment, degraded performance | [5 min] | [15 min] | Every [30 min] | [4 hours] |
| **P2 — Minor** | Partial impairment, cosmetic issues | [15 min] | [1 hour] | Every [2 hours] | [24 hours] |
| **P3 — Low** | Non-critical, informational | [30 min] | [4 hours] | Daily | [72 hours] |
| **P4 — Trivial** | Questions, feature requests | [1 hour] | [8 hours] | Per shift | [Next sprint] |

### SLA Definitions

- **Acknowledge Time**: Time from alert firing to engineer acknowledging the page.
- **Response Time**: Time from acknowledgment to engineer beginning work on the issue.
- **Update Frequency**: How often status updates must be posted to the incident ticket.
- **Resolution Target**: Target time to mitigate or resolve (may not include root-cause fix).

---

## 6. Communication During Rotation

### 6.1 Channels

| Purpose | Channel | Participants |
|---|---|---|
| Alert notifications | [#oncall-alerts] | On-call engineers + all SRE |
| Incident coordination | [#oncall-incidents] | On-call engineers + involved teams |
| Status updates | [#sre-standup] | SRE team |
| Escalation paging | [PagerDuty / OpsGenie] | On-call chain |
| Emergency communication | Phone / SMS | On-call chain |

### 6.2 Status Reporting

- **Shift Start**: Post in [#oncall-status]: "Primary: [Name], Secondary: [Name], Start: [time]"
- **Active Incidents**: Post severity, impact, and current status in [#oncall-incidents].
- **Shift End**: Post summary of incidents handled and handoff status.
- **Escalation Events**: Notify manager immediately when escalation path is triggered.

### 6.3 Silence Periods

- [ ] Do not page the on-call engineer for non-urgent communications (e.g., bug reports, feature questions, meeting invites) — use [async channel, e.g., #sre-questions].
- [ ] Do not expect responses during documented out-of-office hours unless a critical page is sent.
- [ ] Schedule non-urgent maintenance windows during [designated low-traffic period].

---

## 7. Tools and Access Needed

### 7.1 Required Tools

| Tool | Purpose | Access URL | Account Type |
|---|---|---|---|
| [Monitoring System, e.g., Datadog / Grafana] | Observability and alerting | [URL] | [Role-based] |
| [Incident Management, e.g., PagerDuty / OpsGenie] | Alert routing and paging | [URL] | [Engineer account] |
| [Logging System, e.g., Splunk / ELK] | Log analysis | [URL] | [Read-write] |
| [Ticketing System, e.g., Jira / ServiceNow] | Incident tracking | [URL] | [Agent access] |
| [Runbook / Documentation] | Runbooks and playbooks | [URL] | [Read-write] |
| [Chat / Comms, e.g., Slack] | Communication | [URL] | [Standard account] |
| [Infrastructure Dashboard] | System health overview | [URL] | [Read-only] |
| [Deployment System, e.g., Spinnaker / ArgoCD] | Deployment visibility | [URL] | [Read-only] |
| [Cloud Console, e.g., AWS / GCP / Azure] | Infrastructure management | [URL] | [Read-only / Limited write] |

### 7.2 Required Access

- [ ] [Monitoring System] — Alert configuration and dashboard access.
- [ ] [Incident Management] — Ability to acknowledge, resolve, and re-route incidents.
- [ ] [Logging System] — Full log search and export capabilities.
- [ ] [Ticketing System] — Create, update, and close incident tickets.
- [ ] [Chat / Comms] — All relevant Slack channels.
- [ ] [SSH / Bastion] — Access to production instances (read-only or limited write as defined).
- [ ] [Kubernetes / Orchestration] — `kubectl` access with read-only / troubleshooting permissions.
- [ ] [Database Query Tool] — Read-only query access for investigation.
- [ ] [Runbook / Documentation Wiki] — Edit access to update runbooks.

### 7.3 Hardware Requirements

- [ ] Company laptop with VPN access.
- [ ] Stable internet connection (backup recommended).
- [ ] [On-Call Phone / Device] — if applicable.
- [ ] Access to [Corporate SSO / 2FA].

---

## 8. Pre-Flight Checklist for Joining Rotation

> Complete this checklist at least [2 days] before your on-call shift begins.

### 8.1 Communication Setup

- [ ] Added to all on-call Slack channels: [#channel1], [#channel2].
- [ ] Slack status configured to show "On-Call" during the shift.
- [ ] Phone number verified in [PagerDuty / OpsGenie].
- [ ] Notification preferences configured (push, SMS, phone call).
- [ ] Scheduled handoff call with outgoing engineer.
- [ ] Out-of-office / reduced availability communicated to team.

### 8.2 Tooling & Access Verification

- [ ] Log in to [Monitoring System] and verify access to all relevant dashboards.
- [ ] Log in to [Incident Management] and verify ability to acknowledge alerts.
- [ ] Log in to [Logging System] and verify search capabilities.
- [ ] Log in to [Cloud Console] and verify access.
- [ ] Test [VPN / Bastion] access to production environment.
- [ ] Verify [Kubernetes / kubectl] access with a test command.
- [ ] Verify [SSH key] is loaded and working.
- [ ] Verify [Database query tool] access with a read-only test query.
- [ ] Test [Chat / Comms] channels are unmuted and notifications enabled.
- [ ] Confirm [Phone / SMS] delivery works for the on-call number.

### 8.3 Documentation Review

- [ ] Read the following runbooks:
  - [Incident Response Runbook]
  - [Service Restart / Recovery Runbook]
  - [Database Failover Runbook]
  - [Deployment Rollback Runbook]
- [ ] Review recent incident postmortems (last [30] days).
- [ ] Review current known issues and active incident tickets.
- [ ] Familiarize yourself with service architecture diagram at [Link].
- [ ] Review the Error Budget Policy at [Link].
- [ ] Confirm location of escalation contacts list.

### 8.4 Knowledge Transfer

- [ ] Attend handoff meeting with outgoing engineer.
- [ ] Review handoff log from prior shifts (last [7] days).
- [ ] Get walkthrough of any active incidents or pending investigations.
- [ ] Understand current release / deployment status.
- [ ] Identify any known upcoming maintenance windows.
- [ ] Review recently deployed changes (past [72] hours).

### 8.5 Practical Drills (Optional but Recommended)

- [ ] Walk through a simulated P0 incident using [Game Day / Chaos Engineering] platform.
- [ ] Practice using the [War Room] process.
- [ ] Verify ability to escalate to all tiers in the escalation chain.
- [ ] Time yourself on acknowledging a test alert.

### 8.6 Final Confirmation

> **I confirm that I have completed the pre-flight checklist and am ready to assume on-call responsibilities.**

Signature: _________________________________
Date: _______________________________________

---

## 9. Appendix

### A. Rotation Calendar Template

```
Week [N] ([Start Date] – [End Date]):
  Primary:   [Name] ([Time Zone])
  Secondary: [Name] ([Time Zone])
  Escalation: [Name]

Week [N+1] ([Start Date] – [End Date]):
  Primary:   [Name] ([Time Zone])
  Secondary: [Name] ([Time Zone])
  Escalation: [Name]
```

### B. Related Documents

- [Incident Response Playbook]
- [Error Budget Policy]
- [Postmortem Template]
- [Runbook Index]
- [Service Architecture Diagram]
- [Escalation Contacts List]
