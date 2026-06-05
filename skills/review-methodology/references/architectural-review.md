# Architectural Review

Evaluating design decisions — coupling/cohesion, scalability, data flow, and abstraction boundaries.

## The Five Architectural Dimensions

### 1. Coupling — How connected are components?

| Coupling type | Low (good) | High (bad) |
|--------------|-----------|------------|
| **Tight vs loose** | Components communicate through well-defined interfaces | Components share internal state, rely on calling order |
| **Directional** | Dependencies flow in one direction (layered) | Circular dependencies, bidirectional coupling |
| **Knowledge** | Components know about interfaces, not implementations | Components know about each other's internals |

**Check:** Can you change one component without changing its callers? If every change propagates, coupling is too tight.

### 2. Cohesion — Does each component have a single responsibility?

| Signal | Good | Bad |
|--------|------|-----|
| Module size | Focused on one concern | Handles I/O, business logic, and presentation |
| Change pattern | Changes cluster in one module for one reason | One change touches files across unrelated modules |
| Naming | Module name describes its purpose | Module name is generic ("utils", "helpers", "common") |

**Check:** Can you describe what each module does in one sentence without using "and"? If not, cohesion is too low.

### 3. Abstraction Boundaries — Are the right things hidden?

| Signal | Good | Bad |
|--------|------|-----|
| Interface | Public API is minimal and intentional | Every function is public, nothing is encapsulated |
| Leakage | Implementation details stay internal | Database schema leaks into business logic, HTTP details leak into service layer |
| Testability | Components can be tested in isolation | Testing requires full system setup because boundaries are wrong |

**Check:** If the underlying infrastructure changed (file storage → S3, SQLite → Postgres), how many files would change? If more than the data access layer, abstraction boundaries are leaking.

### 4. Data Flow — Does data follow a clear path?

| Signal | Good | Bad |
|--------|------|-----|
| Direction | Data flows in one direction through the system | Data flows in loops, circles back through unexpected paths |
| Transformation | Each transformation is explicit and located | Data is mutated in multiple places, making it hard to track state |
| Validation | Data is validated at trust boundaries | Data enters the system, flows through multiple layers, and is validated far from the entry point |

**Check:** Trace the path of a single piece of user input from entry to storage. Is every transformation visible? Does validation happen at the boundary or deep inside?

### 5. Scalability — Does the design handle growth?

| Signal | Good | Bad |
|--------|------|-----|
| Data volume | Design acknowledges growth paths | Design assumes fixed dataset size |
| Users | Design considers concurrent access | Design assumes single-user or serial access |
| Team size | Design supports multiple contributors | Design assumes one person will maintain everything |
| Feature growth | Adding features doesn't require restructuring | Every new feature requires redesigning core abstractions |

**Check:** What breaks when inputs grow 10x? What breaks when the team doubles?

## Architectural Review Protocol

### Phase 1: Understand the Design
1. Read the design document, ADR, or PR description
2. Identify the core abstractions and their relationships
3. Trace the primary data flow

### Phase 2: Assess Each Dimension
1. **Coupling** — Map module dependencies. Identify circular or bidirectional links.
2. **Cohesion** — Check each module's scope. Is it doing one thing or many?
3. **Abstraction** — Find what's exposed vs hidden. Are internals leaking?
4. **Data flow** — Trace input to output. Where does data get transformed? Where validated?
5. **Scalability** — Ask "what breaks at 10x?"

### Phase 3: Identify Tradeoffs
Every architecture is a set of tradeoffs. Name them explicitly:

- "This approach favors [simplicity/composability/speed] at the cost of [flexibility/maintainability/scalability]."
- "The coupling between X and Y is justified because [reason]. If Z changes, we'll need to revisit."
- "This abstraction boundary is appropriate now. It will need to be re-evaluated when [specific trigger]."

### Phase 4: Recommend
- **Accept** — Design is sound for its context. Flag minor concerns.
- **Conditional accept** — Design is acceptable if specific concerns are addressed before production.
- **Request redesign** — Fundamental issues with coupling, cohesion, or abstraction boundaries.
