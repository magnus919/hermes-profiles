# The Seven Kanban Cadences

Unlike Scrum's four ceremonies, Kanban defines seven cadences spanning from daily coordination to quarterly strategy. These cadences replace the ad-hoc management conversations, escalation chains, and priority negotiations that emerge in the absence of structure.

## 1. Daily Kanban Standup

**Frequency:** Daily. **Duration:** 15 minutes hard stop. **Participants:** Whole team.

**Purpose:** Optimize today's flow. Identify and address blockers. Determine what to pull next.

**Format:** Stand at the board. Walk **right-to-left** — start at the column closest to Done, move leftward. Focus on blocked and aging items. Do not have individuals report what they did yesterday — the board shows that.

**Agenda:**
1. Review Done column (2 min) — what shipped? Celebrate briefly.
2. Review In Review (3 min) — any items blocked waiting for feedback, deployment? Who can unblock?
3. Review In Progress (5 min) — stuck, blocked, or aging items? Are we at WIP limit?
4. Determine what to pull from Ready (3 min) — given WIP and allocations, what's next?
5. Parking lot (2 min) — blockers needing offline follow-up. Don't solve in standup.

**Anti-patterns:** Going around the room for individual status updates. Solving problems in standup. Treating it as reporting to the EM rather than team coordination.

## 2. Replenishment (Intake)

**Frequency:** 1–2× per week. **Duration:** 30–60 minutes. **Participants:** EM/TL + PMs.

**Purpose:** Decide what enters the Ready queue, respecting WIP capacity and capacity allocations. Close the intake to all other entry paths.

**Agenda:**
1. System state review — current WIP, throughput, capacity allocations
2. Fixed Date and Bug items first (objective urgency)
3. PMs present candidates
4. Selection respects allocation percentages and WIP capacity
5. Return items that don't meet Definition of Ready

**Key rule:** All new work enters through Replenishment. No side-channel asks to engineers. The EM/TL enforces this boundary consistently.

## 3. Delivery Planning

**Frequency:** Weekly or bi-weekly (often combined with Replenishment). **Duration:** 30–45 minutes.

**Purpose:** Coordinate near-term delivery expectations against actual WIP and throughput data. Surface Fixed Date items at risk. Resolve timing conflicts between portfolios.

**Agenda:**
1. WIP aging review (10 min) — walk in-progress items sorted by age, oldest first
2. Fixed Date calendar review (10 min) — upcoming deadlines, flag at-risk items
3. Throughput-to-commitment check (10 min) — for each portfolio, does pipeline clear rate match roadmap expectations?
4. Dependency and constraint review (10 min) — cross-team, infrastructure, skills
5. Adjustments and escalations (5 min)

## 4. Service Delivery Review (SDR)

**Frequency:** Bi-weekly or monthly. **Duration:** 60–90 minutes. **Participants:** EM/TL + all PMs + leadership (optional).

**Purpose:** The primary governance loop for shared teams. Inspect actual throughput against allocation targets, review SLE adherence, analyze systemic blockers, and make allocation adjustment decisions with data.

**Pre-work (distributed 24h in advance):** Data packet with throughput by portfolio, lead time distribution, blocker log, SLE hit rate.

**Agenda:**
1. Service definition reminder (3 min) — current allocation splits
2. Throughput by portfolio (12 min) — actual vs. target
3. Lead time and SLE review (12 min) — 85th percentile by class of service
4. Blocker analysis (10 min) — categorize by root cause; identify top patterns
5. PM portfolio health checks (10 min) — each PM asserts under/over-served
6. Improvement experiments (15 min) — 1–2 changes to test next period
7. Allocation decision (10 min, if needed) — temporary shifts, documented
8. Close-out (3 min)

**See also:** `references/multi-portfolio.md` for deeper governance context.

## 5. Team Retrospective

**Frequency:** Every 2–4 weeks. **Duration:** 60–90 minutes. **Participants:** Engineering team only.

**Purpose:** Inward-focused improvement. How are we working together? What can we improve about our practices? Separated cleanly from the SDR's outward-facing service review.

**Suggested format (75 min):**
1. Safety check (5 min) — anonymous psychological safety rating
2. What went well? (15 min) — practices, behaviors, decisions worth repeating
3. What was hard or frustrating? (20 min) — systemic observations, not personal complaints
4. What shall we change? (20 min) — 1–3 concrete experiments with owners and success criteria
5. Close loop on previous experiments (10 min) — what happened? Continue, adjust, or stop?

**PM participation:** Not recommended. PMs are stakeholders, not team members. Their concerns belong in the SDR and Replenishment.

## 6. Risk Review

**Frequency:** Monthly. **Duration:** 60 minutes. **Participants:** EM/TL + engineering leadership + optional PMs.

**Purpose:** Identify and mitigate systemic threats to delivery — technical, operational, organizational, and market risks that will become next quarter's service failures if left unaddressed.

**Risk categories for shared teams:**
- **Technical/architectural:** Accrued tech debt, legacy dependencies, SPOFs
- **Capacity/skill:** Skills concentrated in one or two engineers, bus factor
- **Dependency:** External teams, vendors, data providers multiple portfolios depend on
- **Operational/incident:** Recurring incident patterns suggesting systemic reliability issues
- **Market/regulatory:** Incoming compliance deadlines, competitive pressures

**Agenda:**
1. Risk register review (15 min) — existing risks, status changes, completed mitigations
2. Operational signal review (15 min) — blocker log, expedite frequency, WIP aging
3. Forward-looking risk identification (15 min) — calendar scan, roadmap scan, architecture scan
4. Mitigation planning (10 min) — likelihood, impact, owner, trigger
5. Policy updates (5 min) — unplanned work buffer, expedite criteria, cross-training
6. Escalation decisions (5 min) — risks requiring leadership authorization

## 7. Strategy Review

**Frequency:** Quarterly. **Duration:** 2–4 hours. **Participants:** CTO/CPO/VP Eng + portfolio leaders + EM/TL.

**Purpose:** The highest-level cadence. Review whether portfolio capacity allocations reflect organizational priorities. Set the strategic parameters that will govern the next quarter of Replenishment decisions.

**Agenda:**
1. Operational evidence review (45 min) — throughput vs. targets, lead time trends, risk register
2. Market and business context (30 min) — what changed externally?
3. Cost-of-Delay analysis (30 min) — CD3 ranking of next quarter's major initiatives
4. Allocation revision (30 min) — new allocation splits for next quarter
5. Structural decisions (30 min) — headcount, skills investment, team composition
6. Commitment and communication (15 min) — document decisions, assign communications

The EM/TL is the bridge between strategy and execution — they bring operational truth upward to strategy and bring strategic decisions downward to the weekly cadences.
