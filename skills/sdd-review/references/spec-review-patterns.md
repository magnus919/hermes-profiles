# Spec Review Patterns

Reviewing a SPEC.md before it proceeds to work decomposition.

## Completeness Checklist

- [ ] Problem statement is present and specific
- [ ] Success criteria are measurable, not aspirational
- [ ] In-scope and out-of-scope are equally explicit
- [ ] User stories are prioritized and traceable to acceptance criteria
- [ ] Every AC passes the testability test (produces clear PASS/FAIL)
- [ ] Edge cases are enumerated, not implied
- [ ] NFRs have measurable thresholds, not adjectives
- [ ] Data contracts are specified at independent-implementation granularity
- [ ] Assumptions are documented with impact assessments
- [ ] Open questions have resolution plans

## Ambiguity Detection

Read the spec as if you cannot ask for clarification. Mark every phrase that could be interpreted more than one way. Common ambiguity patterns:

| Phrase | Problem | Fix |
|--------|---------|-----|
| "common formats" | What counts as common? | "jpg, png, gif, webp" |
| "standard behavior" | Standard where? | "Returns 404 with error body" |
| "handle gracefully" | What does graceful look like? | "Returns 200 with error field in response" |
| "reasonable time" | What number? | "Under 500ms at P95" |
| "appropriate error" | What error? | "Returns 422 with field-level validation errors" |

## Testability Assessment

For each AC, ask: "Could I write a script that checks this automatically and returns pass or fail?" If the answer is no, the AC fails the spec review. Acceptable responses:

- YES → AC is well-formed
- YES, with test data → AC needs example data to be tested. Acceptable, flag the data requirement.
- NO → AC is not testable. Must be rewritten or removed.

## Review Mindset

Spec review is not editorial review. You are not checking grammar, style, or clarity for human readers. You are evaluating whether this spec is safe to give to an AI coding agent that cannot ask clarifying questions.

The standard to hold: "If an agent implements exactly what this spec says, will the result be correct?" If any section of the spec could produce a wrong implementation when interpreted literally, that section fails the review.
