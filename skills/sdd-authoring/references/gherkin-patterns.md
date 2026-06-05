# Gherkin Patterns for SDD

Writing Given/When/Then scenarios for machine-executable specifications.

## Standard Scenario Structure

```gherkin
Scenario: <Descriptive title of the behavior>
  Given <precondition state>
  When <action or event>
  Then <expected outcome>
```

Every scenario has exactly one Given (the setup), one When (the trigger), and one or more Then clauses (observable outcomes). Multiple Given clauses are valid when the setup requires multiple preconditions, but prefer a single combined setup.

## Common Patterns

### CRUD Operations

```gherkin
Scenario: Create a resource with valid data
  Given the user is authenticated as a "member"
  When the user submits a POST request to /api/resources with:
    | field  | value          |
    | name   | "Test Resource" |
    | type   | "document"      |
  Then the response status is 201
  And the response body contains a resource with:
    | field   | value           |
    | name    | "Test Resource" |
    | type    | "document"      |

Scenario: Create a resource with invalid data is rejected
  Given the user is authenticated as a "member"
  When the user submits a POST request to /api/resources with:
    | field | value |
    | name  | ""    |
  Then the response status is 422
  And the response body contains field "name" with error "required"
```

### State Transitions

```gherkin
Scenario: State transition with correct preconditions
  Given a ticket exists with status "open"
  When the assignee transitions the ticket to "in_progress"
  Then the ticket status is "in_progress"
  And the ticket history contains a transition from "open" to "in_progress"

Scenario: State transition with incorrect preconditions is rejected
  Given a ticket exists with status "closed"
  When the assignee transitions the ticket to "in_progress"
  Then the response status is 409
  And the error message explains the invalid state transition
```

### Error and Edge Cases

```gherkin
Scenario: Concurrent modification is detected
  Given a resource exists with version "1"
  And user A loads the resource
  And user B updates the resource to version "2"
  When user A attempts to update the resource with version "1"
  Then the response status is 409
  And the response contains the current version "2"

Scenario: Rate limit is enforced
  Given the API rate limit is 10 requests per minute
  When the client sends 11 requests within 1 minute
  Then the 11th response status is 429
  And the response contains a Retry-After header

Scenario: Resource not found
  Given a resource with id "nonexistent" does not exist
  When a client requests GET /api/resources/nonexistent
  Then the response status is 404
```

## Scenario Organization

Group related scenarios under a feature file:

```gherkin
Feature: Resource Management
  As an API consumer
  I want to manage resources
  So that I can organize my data

  Background:
    Given the API is available at /api/v2

  @happy-path
  Scenario: Create resource

  @error
  Scenario: Create resource with invalid data

  @edge-case
  Scenario: Create resource with maximum allowed size
```

## Writing Good Scenarios

1. **One behavior per scenario.** If a scenario tests "create resource" and "update resource" and "delete resource," split it into three scenarios. Each scenario is one test.
2. **Specific data, not placeholders.** "valid email" is vague. Use "user@example.com" — specific data makes the test debuggable and prevents ambiguity about what "valid" means.
3. **Observable outcomes only.** "Then the user should feel confident" is not testable. "Then the confirmation message displays 'Your account has been created'" is testable.
4. **Independent scenarios.** A scenario should not depend on a previous scenario running first. Each scenario sets up its own preconditions.
