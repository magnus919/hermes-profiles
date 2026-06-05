# Error Handling

## Error Classification

| Category | HTTP analogue | What it means | Example |
|----------|--------------|---------------|---------|
| Validation | 400 | The client sent something wrong | Missing required field |
| AuthN/AuthZ | 401/403 | The caller can't do this | Expired token, insufficient permissions |
| Not Found | 404 | The resource doesn't exist | Invalid ID, deleted entity |
| Conflict | 409 | The operation can't complete due to state | Duplicate, stale version |
| Rate Limited | 429 | Too many requests | Quota exceeded |
| Internal | 500 | Something went wrong on the server | DB down, unhandled exception |
| Unavailable | 503 | The service can't handle the request right now | Circuit open, overloaded |

## Exception Handling Strategy

| Catch location | What to do | Example |
|---------------|------------|---------|
| Repository | Wrap DB errors in domain exceptions | `UserNotFoundException`, `DuplicateEmailError` |
| Service | Handle domain exceptions, orchestrate recovery | Retry on conflict, fallback on unavailable |
| Controller boundary | Map domain exceptions to error responses | `UserNotFoundException` → 404 with error body |
| Middleware boundary | Catch unhandled exceptions, log, return 500 | Global error handler, structured log + trace |

## Structured Logging Fields

Every log entry at service level should include:

- `request_id` — correlation ID from request header or generated at middleware
- `service` — service name
- `operation` — what operation was being performed
- `duration_ms` — how long it took
- `error_code` — if error, machine-readable code
- `caller` — function/module that produced the log

## Error Response Body

```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Too many requests. Please retry after the specified time.",
    "retry_after_seconds": 30,
    "request_id": "req_abc123"
  }
}
```
