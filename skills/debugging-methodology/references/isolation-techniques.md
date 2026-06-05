# Isolation Techniques

## Binary Search (Divide and Conquer)

For identifying which component, commit, or input causes a failure:

1. Split the search space in half
2. Test each half independently
3. Recurse on the failing half
4. Stop when you've isolated to a single unit

## Component Isolation

Test components independently when possible:
- Mock external dependencies
- Test the component in isolation with controlled inputs
- Verify the component's behavior before testing integration

## Minimal Reproduction

To eliminate unrelated factors:
1. Start with the simplest possible reproduction case
2. Add complexity one factor at a time until the failure reproduces
3. The minimal reproduction reveals the essential conditions for the failure
