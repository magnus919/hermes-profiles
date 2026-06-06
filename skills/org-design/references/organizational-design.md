# Organizational Design

## Team Topologies

The four fundamental team types, from Matthew Skelton and Manuel Pais:

### Stream-Aligned Team

Aligned to a single, valuable stream of work (product, service, feature, user journey).

| Characteristic | Description |
|----------------|-------------|
| **Focus** | Delivering value directly to the end customer |
| **Skills** | Cross-functional — development, testing, operations, product |
| **Boundary** | Owns one stream end-to-end |
| **Cognitive load** | Matched to the complexity of the stream |
| **Interaction mode** | Collaborates with enabling teams for capability building |

**When to use:** Default team type for most modern product development. One team per stream of value.

### Enabling Team

Supports stream-aligned teams by building capabilities in specific technical domains.

| Characteristic | Description |
|----------------|-------------|
| **Focus** | Increasing the effectiveness of other teams |
| **Skills** | Deep expertise in a specific domain (CI/CD, security, testing, observability) |
| **Boundary** | No permanent code ownership — builds capabilities, not products |
| **Lifecycle** | Exists as long as the capability gap exists |
| **Interaction mode** | Collaborates (short bursts) → transitions to facilitating (long-term) |

**When to use:** When stream-aligned teams lack capability in a critical domain. Enable them to become self-sufficient, then dissolve or move to the next gap.

### Complicated-Subsystem Team

Owns a subsystem that requires specialized, deep expertise.

| Characteristic | Description |
|----------------|-------------|
| **Focus** | Building and maintaining a technically complex component |
| **Skills** | Deep specialization in one domain (video encoding engine, ML model, payment reconciliation) |
| **Boundary** | Clear, well-defined API boundary with the rest of the system |
| **Interaction mode** | X-as-a-Service — stream-aligned teams consume via API |

**When to use:** When a subsystem's complexity exceeds what a stream-aligned team can reasonably carry. The cognitive load of the subsystem is isolated to one team.

### Platform Team

Provides internal services and tools that reduce the cognitive load of stream-aligned teams.

| Characteristic | Description |
|----------------|-------------|
| **Focus** | Building internal developer platform capabilities |
| **Skills** | Platform engineering, infrastructure, developer experience |
| **Boundary** | Self-service APIs and tools that stream-aligned teams consume |
| **Interaction mode** | X-as-a-Service — platform team provides, stream teams consume |
| **Mindset** | Platform is a product; stream teams are the customers |

**When to use:** Beyond 5-8 stream-aligned teams, a platform team becomes necessary to prevent fragmentation and toil.

### Team Topologies Interaction Modes

| Mode | Description | When to use |
|------|-------------|-------------|
| **Collaboration** | Two teams work together for a limited time on a shared goal | New capability discovery, integration points |
| **X-as-a-Service** | One team consumes another's service via a well-defined interface | Platform → stream, complicated-subsystem → stream |
| **Facilitating** | One team helps another develop a capability, then steps back | Enabling → stream-aligned teams |

## Span of Control

| Layer | Ideal span | Notes |
|-------|------------|-------|
| **First-line manager** | 4-8 direct reports | Hands-on coaching, career development, technical guidance |
| **Director** | 3-6 managers | Coordination, strategy translation, resource allocation |
| **VP** | 3-5 directors | Organizational strategy, cross-functional alignment |
| **C-Suite** | 4-8 VPs/C-suite | Enterprise strategy, external representation |

**Rule of thumb:** The more complex and interdependent the work, the narrower the span. The more standardized and independent, the wider.

### The Dunbar-Heuristic for Teams

- **5-8 people**: Optimal for stream-aligned teams (all members can maintain high-bandwidth relationships)
- **15-20 people**: Maximum for a single manager's span in complex work
- **50-150 people**: "Dunbar number" — maximum for a community where everyone can know each other
- **>150 people**: Formal processes, hierarchy, and systems are required

## Reporting Structures

### Functional (Traditional)

```
CEO
├── Engineering VP
│   ├── Engineering Manager → 5 engineers
│   └── Engineering Manager → 6 engineers
├── Product VP
│   ├── PM Director → 3 PMs
│   └── Design Director → 4 designers
└── Marketing VP
    ├── Growth Director → 4 marketers
    └── Brand Director → 3 marketers
```

**Best for:** Stable organizations, deep specialization, clear career ladders
**Worst for:** Cross-functional collaboration, customer-centricity

### Matrix

```
                    Product A        Product B        Product C
Engineering         Eng lead A       Eng lead B       Eng lead C
Design              Designer A       Designer B       Designer C
Product             PM A             PM B             PM C
```

**Best for:** Resource sharing across multiple priorities
**Worst for:** Clear decision-making, dual reporting creates tension

### Product/Stream-Aligned (Modern)

```
CEO
├── Stream Alpha (cross-functional team)
├── Stream Beta (cross-functional team)
├── Platform Team
└── Enabling Team (CI/CD)
```

**Best for:** Speed, autonomy, customer focus
**Worst for:** Deep specialization (mitigated by enabling teams and communities of practice)

## Organizational Health Metrics

| Metric | What it measures | Diagnostic |
|--------|-----------------|------------|
| **Span of control ratio** | Middle management efficiency | >1:8 suggests potential bottlenecks or micromanagement |
| **Org depth** | Levels from IC to CEO | >5 levels slows decision-making |
| **Team size distribution** | How many teams are at optimal size | >8 members per team → likely fragmentation |
| **Dependency count** | Cross-team blockers | High → reorganize to reduce (Conway's Law) |
| **Decision velocity** | Time from proposal to decision | >2 weeks for operational decisions → process is broken |
| **Manager-to-IC ratio** | Proportion of people managers vs individual contributors | >1:3 might indicate too many managers |
