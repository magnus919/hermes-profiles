# Scaling Frameworks

Organizational scaling is a discontinuous function. The operating model that works at 10 people breaks at 50. The model that works at 50 breaks at 200. Each stage requires deliberate redesign.

## The Scaling Stages

### Stage 1: Founding (1-10 People)

**Operating model:** Direct communication. Everyone knows everything. CEO makes most decisions.

**What works:**
- All-hands meetings, everyone talks to everyone
- CEO approves all hires and major decisions
- Informal processes, no documentation needed
- Generalists preferred over specialists

**What breaks:**
- Informal communication becomes unreliable
- CEO becomes bottleneck for decisions
- "Everyone does everything" leads to dropped balls
- Hiring starts to need structure (interview process, offer letters)

**Transition trigger:** CEO can no longer attend every meeting or review every decision. Typically at 8-15 people.

### Stage 2: The Team Phase (10-50 People)

**Operating model:** Functional teams with managers. CEO manages via team leads.

**What changes:**
- Department heads appointed (Engineering, Sales, Marketing)
- Weekly staff meetings with department leads
- Basic processes emerge (hiring, expense approval, customer support)
- First specialist hires (marketing, HR, finance)

**New challenges:**
- Communication across teams becomes a problem
- CEO is still in most decisions but now through team leads
- Hiring needs process (standardized interviews, offer approval)
- First performance management issues arise

**Transition trigger:** Team leads can't keep up with coordination. Cross-team projects fail due to poor communication. Typically at 40-60 people.

### Stage 3: The Department Phase (50-200 People)

**Operating model:** Functional departments with VP-level leaders. CEO manages the executive team.

**What changes:**
- VPs hired for each department
- Weekly exec team meeting, monthly all-hands
- Formal processes for hiring, budgeting, performance reviews
- Middle management layer added
- First attempt at OKRs or similar goal-setting

**New challenges:**
- Silos emerge between departments
- "Over the wall" syndrome — Engineering blames Sales, Sales blames Product
- Decision-making slows as more stakeholders are involved
- Culture dilution — new hires don't know the old ways
- First major process debt — too many processes or not enough

**Transition trigger:** Cross-functional coordination becomes the primary bottleneck. Silos prevent strategic initiatives. Typically at 150-250 people.

### Stage 4: The Enterprise Phase (200-1,000+ People)

**Operating model:** Business units or divisions with P&L responsibility. CEO manages business unit leaders.

**What changes:**
- Business units with their own P&L
- Shared services (IT, HR, Finance, Legal) as centralized functions
- Formal governance (board meetings, committee structure)
- Strategic planning process (annual + quarterly)
- Professional management systems (compensation bands, leveling, career frameworks)

**New challenges:**
- Maintaining startup culture at scale
- Bureaucracy and process bloat
- Innovation atrophies — everything requires a business case
- Talent density dilutes — average performers become the norm
- Coordination costs dominate operating expenses

**Survival strategies:**
- Break into autonomous units when possible
- Maintain small-team dynamics within units
- Invest in internal mobility and talent development
- Fight process creep actively — sunset unnecessary processes

---

## Delegation Patterns at Scale

### The Delegation Progression

| Stage | CEO Decisions | Delegated | Mechanisms |
|-------|--------------|-----------|------------|
| 1-10 | All major decisions | Minimal | Direct assign |
| 10-50 | Strategy, hiring, budget, product | Execution | Department leads |
| 50-200 | Strategy, exec hiring, major budget | Operations, product | VP delegation, OKRs |
| 200-1000 | Strategy, capital allocation, culture | Almost everything | Business unit P&L, governance |

### Scaling the Span of Control

| Level | Direct Reports | Notes |
|-------|---------------|-------|
| First-line manager | 4-8 | Direct contributors |
| Director/V-Level | 4-6 | Manager of managers |
| C-Suite | 4-8 | Direct reports and functional leaders |
| CEO (early) | 4-6 | Direct reports |
| CEO (scale) | 8-12 | Including functional heads |

### Span of Control Heuristics
- Technical ICs need more attention → smaller spans (4-6)
- Experienced managers → larger spans (6-10)
- Autonomous/empowered teams → larger spans
- New managers → smaller spans (3-4), grow over time

---

## Organizational Design Patterns

### Functional Structure

Pro: Deep expertise, clear career paths, efficient resource use
Con: Silos, slow cross-functional decisions, customer-blind
Best for: 10-200 person companies, stable markets

### Divisional/BU Structure

Pro: Customer-focused, fast decisions within unit, clear P&L ownership
Con: Duplication of resources, coordination across units is hard
Best for: 200+ person companies, multiple products/markets

### Matrix Structure

Pro: Combines functional expertise with project focus
Con: Dual reporting is confusing, slow decisions, "two bosses" problem
Best for: Project-based organizations (consulting, construction)

### Team Topologies (Conway's Law Applied)

Designed to align team structure with communication needs:

| Team Type | Purpose | Size | Interactions |
|-----------|---------|------|--------------|
| **Stream-aligned** | Owns a full value stream (feature, service, product area) | 6-8 | Collaborates with enabling teams |
| **Enabling** | Helps stream-aligned teams learn and adopt new capabilities | 4-6 | Collaborates, facilitates |
| **Complicated-subsystem** | Owns a domain that requires deep specialized knowledge | 4-8 | Provides, X-as-a-Service |
| **Platform** | Builds internal products that other teams use | 6-10 | Provides, X-as-a-Service |

---

## Conway's Law Applied

> "Organizations design systems that mirror their communication structure."

### The Principle

If you have 3 teams that need to coordinate to ship a feature, the system will have 3 components that need to coordinate to work. The architecture reflects the org chart.

**Implications:**
- To change the architecture, first change the team structure
- A microservices architecture requires a team structure that supports autonomous services
- A monolith is fine if the team is a monolith (small, colocated)

### Inverse Conway Maneuver

Restructure teams to match the desired architecture, then let the architecture follow.

1. Define the target architecture (e.g., 3 services: payments, inventory, orders)
2. Create 3 stream-aligned teams, each owning one service
3. The architecture will naturally converge on the target because teams can independently deliver

**Risk:** If the architecture isn't right, you've locked in a bad design. Test the architecture hypothesis before restructuring.

---

## Dunbar's Number

150 is the theoretical maximum number of stable social relationships a human can maintain.

### Applications to Organizational Design

| Number | Social Dynamic | Organizational Implication |
|--------|---------------|---------------------------|
| 5 | Intimate team | Everyone knows everyone deeply. Full trust. |
| 15 | Band | Can maintain shared context without process. |
| 50 | Tribe | Need some structure. Most people know most people. |
| 150 | Clan | Dunbar's number. Start of anonymity. Need formal systems. |
| 500 | Crowd | Cannot know everyone. Need full management hierarchy. |

### Practical Rules

- **Keep teams under 10** (preferably 6-8)
- **Keep departments under 150** — once a department exceeds 150, split it
- **All-hands becomes impractical > 150** — use cascading communication
- **Culture is carried by the 150 core** — the first 150 employees define the culture. After that, culture must be actively managed through systems and stories.
