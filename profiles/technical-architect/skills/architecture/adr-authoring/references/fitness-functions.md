# Fitness Functions for Decisions as Code

Fitness functions are automated checks, written as code, that verify architectural decisions are being maintained. An ADR documents the decision; a fitness function *assures* it.

**Concept origin:** https://github.com/architecture-decision-record/architecture-decision-record — based on the "Fitness Functions for Decisions as Code" document in the ADR community repo.

## How Fitness Functions Connect to ADRs

```
ADR: "We use event sourcing for audit requirements"
    ↓
Fitness function: CI test asserting that every state change produces an event
    ↓
If a commit introduces a code path that mutates state without emitting an event → test fails
```

The ADR captures the *intent*. The fitness function enforces the *execution*.

## Why Fitness Functions Matter

| Benefit | Description |
|---------|-------------|
| **Objective measurement** | Pass/fail, not opinions. Work is visible and clear. |
| **Continuous enforcement** | Run on every commit, build, and deployment. Living rules. |
| **Confidence to refactor** | Automated catching of decision-rule violations during changes. |
| **Scalable governance** | Assure standards across a growing codebase without creating human bottlenecks. |

## Fitness Function Approaches

### 1. Architecture Unit Testing (Java — ArchUnit)

[ArchUnit](https://www.archunit.org/) checks architecture rules using plain Java unit test frameworks (JUnit, TestNG).

```java
// Example: Enforce that services don't directly access repositories
@Test
public void services_should_not_access_repositories_directly() {
    JavaClasses classes = new ClassFileImporter().importPackages("com.myapp");
    ArchRule rule = classes()
        .that().resideInAPackage("..service..")
        .should().onlyAccessClassesThat()
        .resideInAnyPackage("..service..", "..api..");
    rule.check(classes);
}
```

**What ADR patterns it can enforce:**
- Layered architecture violations (UI → Service → Repository direction)
- Dependency injection rules (no `new` for certain interfaces)
- Package cycle detection
- Naming conventions matching architectural roles

### 2. Architecture Unit Testing (TypeScript — ArchUnitTS)

[ArchUnitTS](https://github.com/LukasNiessen/ArchUnitTS) provides the same pattern for TypeScript/JavaScript using Jest, Vitest, Jasmine, etc.

```typescript
// Example: Controllers should depend on services, not repositories
const rule = ArchRule.of('controllers')
    .should().onlyDependOn()
    .packages(['services', 'dto']);
```

### 3. AI-Assisted Fitness Functions

For decisions that can't be expressed as static code checks, use LLM-based fitness functions with a structured prompt template:

```txt
IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning.
IMPORTANT: Turn on extended thinking. Turn on expert advice. Turn on search.

This is a fitness function to evaluate if our work is
using all our decisions, and is correct and accurate.

- Our decisions are here: {url to ADR index}
- Our work to evaluate is here: {url to code/PR/design doc}

Explain any errors, problems, gaps, weaknesses. Be direct. Be decisive.
```

**When to use AI-assisted fitness functions:**
- Evaluating PRs against multiple ADRs simultaneously
- Checking logical consistency across a set of related decisions
- Validating architectural compliance in design documents or proposals
- Auditing decisions that don't have a mechanical enforcement mechanism

## Mapping to the Artifact Pyramid

| Layer | What Lives There | Fitness Function Relevance |
|-------|-----------------|---------------------------|
| L1 (01-summary/) | ADR navigation index | — |
| L2 (02-analysis/) | Active ADRs (decision rationale) | ADRs declare *what* should be enforced |
| L3 (03-dossiers/) | Superseded ADRs, operational artifacts | Fitness functions live HERE |

**Fitness functions are NOT part of the ADR itself.** They are operational governance artifacts — they live in the test suite or CI pipeline, not in the decision log. The ADR should *reference* any fitness function that enforces it (via a Links section or a `Confirmed by` note), but the function code itself belongs in the project's test infrastructure.

## When to Write a Fitness Function

| When | Example |
|------|---------|
| The decision affects a measurable architectural characteristic | "All services must log structured JSON" → Test asserting log output format |
| The decision has a clear pass/fail condition | "No circular dependencies between packages" → ArchUnit test |
| Decision compliance would be expensive to verify manually | "Every gRPC endpoint must have a rate limit" → CI integration test |
| Regulatory or compliance requirements demand audit trails | "All state mutations must be logged" → Middleware test |

When an ADR explicitly states a rule that can be mechanically verified, create a fitness function for it. If the decision is about cost or organizational trade-offs (where fitness functions don't apply), skip automated enforcement and rely on the ADR's rationale for governance.

## Relationship to Decision Governance

Fitness functions operationalize the **Governance** and **Confirmation** sections found in advanced ADR templates (NHS Wales, Gareth Morgan). If your ADR template includes a Governance section, list any fitness functions there:

```markdown
## Governance

Compliance with this decision is verified by:
- ArchUnit test `NoServiceDirectDatabaseAccessTest` (runs on every PR)
- AI-assisted audit every release cycle against {link to ADR index}
```

## Structurizr CI Checks as Fitness Functions

When using Structurizr DSL for C4 model documentation, the Structurizr CLI provides two commands that serve as fitness functions for architecture documentation consistency:

### validate

Checks that the DSL file is syntactically valid and structurally consistent:

```bash
structurizr-cli validate -w docs/arch/model/system.dsl
```

Use as a pre-merge CI gate: if the DSL doesn't parse, the architecture model is broken. This prevents commits that would produce no diagrams or corrupted diagrams.

### inspect

Checks for architectural drift against the model. Verifies that the C4 model remains consistent with the ADRs it references via `!adrs`:

```bash
structurizr-cli inspect -w docs/arch/model/system.dsl
```

Run in CI on every PR that touches either the DSL or the ADR directory. This catches:
- ADR files referenced but missing from the `!adrs` path
- Elements referenced in views that are not defined in the model
- Relationship inconsistencies between model and documentation

### CI Pipeline Integration

```yaml
# .github/workflows/architecture-checks.yml (or similar)
steps:
  - name: Validate Structurizr DSL
    run: structurizr-cli validate -w docs/arch/model/system.dsl

  - name: Inspect for drift
    run: structurizr-cli inspect -w docs/arch/model/system.dsl
```

These are syntactic and structural checks. For semantic validation (does the architecture match the ADRs?), pair them with the AI-assisted fitness function prompt from the "AI-Assisted Fitness Functions" section above. Together they form a complete verification pipeline: syntax → structure → rationale.

Full pipeline templates with validation, export, and deployment for GitHub Actions, GitLab CI, and ForgeJo are in `references/ci-pipeline-templates.md` (c4-diagramming skill).

## Further Reading

- ArchUnit: https://www.archunit.org/
- ArchUnitTS: https://github.com/LukasNiessen/ArchUnitTS
- ADR community repo fitness functions: https://github.com/architecture-decision-record/architecture-decision-record (see `locales/en/documents/fitness-functions-for-decisions-as-code/`)
