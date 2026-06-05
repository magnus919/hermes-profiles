# Acceptance Criteria Design

Crafting acceptance criteria that produce deterministic pass/fail verdicts.

## The No-Surprises Test

An acceptance criterion passes the no-surprises test if: when two different implementers implement against the same AC, they produce the same behavior for every input. If they could produce different implementations that both "satisfy" the AC, the AC is too vague.

## AC Patterns

### Pattern 1: Given/When/Then (for interactive systems)

Best for: UI interactions, API endpoints, stateful workflows.

```
Given the user is on the checkout page with 3 items in cart
When the user applies coupon code "SAVE20"
Then the subtotal is reduced by 20%
And the discount line item shows "-$X.XX"
```

### Pattern 2: Input/Output (for functions and transformations)

Best for: data processing, calculations, validation logic.

```
AC: validateEmail("user@example.com") returns true
AC: validateEmail("not-an-email") returns false
AC: validateEmail("") returns false
```

### Pattern 3: Behavioral Constraints (for non-functional and compliance)

Best for: security rules, performance thresholds, compliance requirements.

```
AC: A request without an Authorization header returns 401
AC: A request with an expired token returns 401
AC: A request with a valid token for a different resource returns 403
```

## Edge Case Enumeration

For every AC, enumerate at least these categories of edge cases:

| Category | Examples |
|----------|----------|
| Empty/null inputs | "", null, [], {} |
| Boundary values | Min/max length, min/max numeric, first/last item |
| Invalid formats | Wrong type, wrong encoding, unexpected characters |
| Missing preconditions | Unauthenticated, resource doesn't exist, wrong state |
| Concurrent access | Two simultaneous writes, race conditions |
| External failures | Downstream service timeout, database unavailable |

## The Substitution Test

For each AC, substitute the implementation with a hardcoded response. If the substitution passes the AC, the AC is too weak — it tests for structure, not correctness.

**Example of a weak AC:**
```
AC: The /register endpoint returns a JSON response
```
→ Substitution: `{"status": "ok"}` — passes. The AC is satisfied by literally any JSON.

**Example of a strong AC:**
```
AC: POST /register with {"email": "a@b.com", "password": "secret123"} returns 201
and response body contains {"email": "a@b.com"}
```
→ Substitution must return the correct email. Stronger.
