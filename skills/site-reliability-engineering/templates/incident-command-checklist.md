# Incident Command Checklist

**Role:** Incident Commander (IC)
**Purpose:** Structured runbook for managing an active incident from page to postmortem.
**Usage:** Check off items as completed. Print or keep open in a dedicated window.

---

## Severity Reference Table

| Sev | Title | Description | SLO Impact | Example | Response Time |
|:---:|-------|-------------|:----------:|---------|:-------------:|
| **SEV1** | Critical Outage | Complete or near-complete service unavailability affecting all users | Critical drop | Site down, core API unreachable | < 5 min |
| **SEV2** | Major Degradation | Significant feature impairment or partial outage affecting a subset of users | Major drop | Payment failures, high latency on major endpoint | < 15 min |
| **SEV3** | Minor Issue | Isolated feature bug or minor degradation with workaround available | Minor drop | UI glitch on non-critical page, slow but functional | < 60 min |
| **SEV4** | Informational | Non-urgent observation; no user-facing impact | No SLO impact | Cosmetic bug, log noise, low-severity alert | Next business day |

> **Escalation rule:** If uncertainty exists between two severity levels, declare at the **higher** severity and re-evaluate during triage.

---

## Phase 1: Incident Recognition ⚠️

Goal: Acknowledge the alert and formally declare an incident.

- [ ] **Acknowledge the page/alert**
  - Respond to the monitoring alert, ticket, or manual report within the SLO response time for the suspected severity.
  - _Note the timestamp — this is `t_incident_ack` for your timeline._

- [ ] **Confirm severity level**
  - Use the Severity Reference Table above. Check user-facing impact, SLO burn rate, and affected services.
  - _Unsure? Declare SEV1 and triage down._

- [ ] **Open the incident in the tracking system**
  - Create incident record in PagerDuty/OpsGenie/incident management tool.
  - _Record the incident ID / internal ticket number._

- [ ] **Declare the incident**
  - Broadcast a clear declaration to the #incidents channel or equivalent: "I am declaring a SEV[X] incident for [service] — [brief symptom]."
  - Formats: `!ic declare --severity SEV1 --service api-gateway --summary "503s on all routes"`
  - _This is `t_incident_declared`._

- [ ] **Set a 5-minute timer for initial triage**
  - Start a timer. Initial triage must begin before it expires.

---

## Phase 2: Initial Triage 🔍

Goal: Understand what's broken, who needs to be involved, and start organizing.

- [ ] **Assess blast radius and user impact**
  - Check dashboards (latency, error rate, throughput, saturation).
  - Identify affected services, user segments (e.g. free-tier vs. paid), and geographic regions.
  - Verify vs. the last known good state (LKGS) — when was the last deploy/change?

- [ ] **Select the response team**
  - Identify the right subject-matter experts (SMEs) by service ownership.
  - Call in on-call engineers from affected teams.
  - _Do not over-invite — too many cooks slows response._

- [ ] **Assign core roles**
  - **Incident Commander (IC):** YOU — owns coordination, decision-making, and timeline.
  - **Scribe:** Responsible for real-time timeline/tick-tock documentation. _Assign this immediately — it is the most commonly forgotten role._
  - **Communications Lead (Comms):** Owns external/internal status updates.
  - **Subject Matter Experts (SMEs):** Engineers actively debugging/mitigating.
  - **Sub-ICs (if needed):** Delegate management of isolated subsystems (e.g. database team, frontend team).

- [ ] **Escalate if needed**
  - If the severity is beyond current team scope or requires exec awareness, escalate through the on-call chain.
  - Notify management / NOC / designated stakeholders per your org escalation policy.

- [ ] **Update incident status**
  - Set status to **TRIAGING** in the incident tracking system.
  - Confirm the severity one more time with the assembled team.

---

## Phase 3: Response / Mitigation 🛠️

Goal: Drive toward mitigation while maintaining clear communication and documentation.

### Communications

- [ ] **Establish the primary communications channel**
  - Dedicated Slack/Discord channel (e.g. `#incident-servicedown-YYYYMMDD`).
  - Pin the incident ID, current severity, and list of IC/Comms/Scribe/SMEs.
  - _All incident-related discussion happens here — no DMs about the incident._

- [ ] **Set up the incident timeline document**
  - Google Doc / Notion / HackMD shared with the entire response team.
  - Template includes: timestamp, event, action, owner.
  - Scribe begins recording every event immediately.

- [ ] **Draft first external communication (if applicable)**
  - Status page update (e.g. Statuspage.io).
  - Comms Lead owns this; IC approves before publishing.
  - Format: "We are investigating reports of [symptom] affecting [scope]. Next update in [X] minutes."

### Mitigation

- [ ] **Assemble hypotheses**
  - SMEs brainstorm root cause candidates.
  - List on the timeline doc with owners for each.
  - _Log everything, even dead ends — they prevent re-tracing._

- [ ] **Drive parallel investigation**
  - SMEs work independently on different hypotheses.
  - IC removes blockers: access, permissions, credentials, config changes.

- [ ] **Evaluate mitigation options**
  - Possible mitigations: rollback, feature flag disable, traffic shift, scale-up, config revert.
  - Risk/reward each option. _Speed is important; correctness is more important for SEV1._
  - IC makes the final call on which mitigation to pursue.

- [ ] **Apply mitigation**
  - Execute the chosen action. _Scribe logs who did what and when._
  - _This is the target we want to reach: `t_mitigation_applied`._

- [ ] **Issue progress updates**
  - Comms Lead sends regular status updates (every 15 min for SEV1, every 30 min for SEV2).
  - IC reviews and approves each update.
  - Even "no new information" is a valid update.

---

## Phase 4: Resolution ✅

Goal: Confirm the incident is truly over and stabilize the system.

- [ ] **Verify the fix in production**
  - SMEs confirm the mitigation resolved the symptoms:
    - Error rate returned to baseline.
    - Latency normalized.
    - All affected endpoints returning correct responses.
  - _Scribe logs `t_verification_complete`._

- [ ] **Monitor stability window**
  - Observe the system for at least one full monitoring cycle (recommended: 15 min for SEV1, 5 min for SEV2) with stable metrics.
  - Watch for secondary effects (cascading failures, degraded dependent services).

- [ ] **Run a smoke test of critical user journeys**
  - Execute the team's standard post-incident smoke test suite (or manually verify: login, search, checkout, key API calls).
  - _If smoke tests fail, return to Phase 3._

- [ ] **Confirm impact bounds**
  - Data loss? Corrupted state? Need for manual recovery (e.g. replay queue, re-sync replicas)?
  - Document known edge cases that might still be affected.

- [ ] **Declare the incident resolved**
  - Clear statement: "This incident is now RESOLVED. The mitigation was [summary]. Monitoring continues."
  - Update incident tracking system status to **RESOLVED**.
  - _This is `t_resolved`._

- [ ] **Update external status page**
  - Set status to "Resolved — no further issues expected."
  - Include a brief summary and, if available, an ETA for the postmortem.

---

## Phase 5: Recovery 🔄

Goal: Return to normal operations, capture follow-up work, and schedule the learning event.

### Immediate Follow-Up

- [ ] **Restore normal operations**
  - Close the incident channel — leave it archived for reference, not active.
  - Remove on-call overrides, restore normal rotation if it was modified.
  - Comms Lead sends a final summary to wider team/stakeholders.

- [ ] **Evaluate data / state recovery needs**
  - Any manual repair needed? Queue replays? Database repairs?
  - Create tracking tickets for each remediation task.

- [ ] **Triage and document follow-up action items**
  - Capture every "we should fix this" that came up during the incident.
  - Categorize as:
    - **P0 / Must fix:** Directly contributed to the incident or would have reduced severity.
    - **P1 / Should fix:** Would improve detection or response time.
    - **P2 / Nice to have:** Would improve general robustness.
  - File tickets in your issue tracker with labels like `post-incident`, `incident-YYYYMMDD`.

### Postmortem

- [ ] **Schedule the postmortem meeting**
  - Within 48 hours for SEV1, within 5 business days for SEV2.
  - Required attendees: IC, Scribe, Comms Lead, SMEs. Optional: stakeholders.
  - Duration: 60 min for SEV1, 30 min for SEV2.

- [ ] **Assign the postmortem owner**
  - Usually the IC or a designated engineering manager.
  - Owner is responsible for drafting the doc and tracking action items to closure.

- [ ] **Create the postmortem document**
  - Use the organization's standard postmortem template (or create one with sections for):
    1.  **Summary** — What happened, in 2-3 sentences.
    2.  **Timeline** — Curated from the scribe's tick-tock log.
    3.  **Impact** — Users affected, duration, data loss (if any).
    4.  **Root Cause** — What actually caused it.
    5.  **Trigger** — What started it (deploy, config change, external dependency).
    6.  **Detection** — How we learned about it. How quickly?
    7.  **Response** — What went well, what didn't.
    8.  **Action Items** — The P0/P1/P2 items with owners and due dates.
  - _Blameless postmortem culture applies — focus on systems, not people._

- [ ] **Send postmortem for review**
  - Share with the response team before publishing widely.
  - Address factual corrections before finalizing.

---

## Quick Reference: IC Do's and Don'ts

| Do | Don't |
|----|-------|
| Delegate debugging to SMEs | Jump into debugging yourself |
| Keep the timeline updated | Trust memory — log everything, even small things |
| Make decisions and own them | Wait for consensus on time-sensitive calls |
| Clear blockers for the team | Micromanage engineers |
| Keep comms structured and regular | Go silent for extended periods |
| Escalate when out of depth | Hero-mode through a crisis alone |
| Hand off cleanly if rotating out | Drop the IC role without a full handoff |

---

## Key Timestamps to Record

| Event | Variable | Description |
|-------|----------|-------------|
| Page received | `t_ack` | When the IC first acknowledged the alert |
| Incident declared | `t_declared` | Formal declaration timestamp |
| Team assembled | `t_assembled` | Full response team in the channel |
| Mitigation applied | `t_mitigated` | When the fix was deployed |
| Verification complete | `t_verified` | Symptoms confirmed gone |
| Incident resolved | `t_resolved` | Formal resolution declaration |
| Time to Mitigation (TTM) | `t_mitigated - t_declared` | Key metric |
| Time to Resolve (TTR) | `t_resolved - t_declared` | Key metric |

---

*Template version: 1.0 — Last updated: 2025-06-05*
*Maintainer: Site Reliability Engineering*
