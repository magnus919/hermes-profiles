# Spec-to-Test Mapping

Mapping specification acceptance criteria to test coverage.

## The Mapping

Every spec AC should map to at least one test. The mapping is:

```
SPEC.md AC-001.1 → Test: "create resource with valid data"
SPEC.md AC-001.2 → Test: "create resource with missing required field"
SPEC.md AC-001.3 → Test: "create resource with duplicate name"
```

The verification report traces this mapping in reverse:

```
Test: "create resource with valid data" → SPEC.md AC-001.1: PASS
Test: "create resource with missing required field" → SPEC.md AC-001.2: PASS
```

## Coverage Gap Detection

A coverage gap exists when:
- An AC has no corresponding test → untested requirement
- A test exists with no corresponding AC → untestable test (what was it supposed to verify?)
- Multiple tests map to the same AC without covering its full scope → over-testing without completeness

## Test Naming Convention

Tests should encode their AC mapping in their names:

```
test_ac_001_1_create_resource_with_valid_data
test_ac_001_2_create_resource_with_missing_field
test_nfr_001_response_time_under_200ms
```

This convention makes the spec-to-test mapping machine-readable and enables automated coverage reporting.
