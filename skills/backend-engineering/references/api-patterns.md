# API Patterns

## Endpoint Design

| Aspect | REST | gRPC | GraphQL |
|--------|------|------|---------|
| Resource modeling | Nouns as resources, verbs as methods | Services with RPC methods | Schema-defined types and queries |
| Request structure | Path params, query params, headers, body | Protobuf messages | Query/mutation with variables |
| Response structure | JSON with envelope | Protobuf messages | Shape matches query structure |
| Error reporting | HTTP status codes + error body | gRPC status codes + details | Errors in `errors` array |
| Versioning | URL path or header | Package version in proto | Schema evolution with deprecation |
| Pagination | Cursor-based preferred | Token-based in proto args | Connection/edges pattern (Relay) |

## Versioning Strategies

| Strategy | Mechanism | Breaking change handling |
|----------|-----------|------------------------|
| URL path | `/v1/resources`, `/v2/resources` | New path, old path maintained |
| Header | `Accept: application/vnd.api+json; version=2` | New accept header value |
| Query param | `?version=2` | New param value, old default maintained |
| No versioning | Evolve in place with additive changes | Only additive changes permitted |

Prefer URL path versioning for public APIs — it's the most visible and least ambiguous.

## Pagination

| Strategy | Pros | Cons | Best for |
|----------|------|------|----------|
| Cursor-based | Stable under writes, no offset drift | Opaque cursors, can't jump to page N | Real-time data, feeds |
| Offset-based | Simple, can jump to any page | Skips/duplicates on writes | Static datasets, admin UIs |
| Keyset | Fast, stable | Requires sort key, complex multi-column | Large datasets, ordered data |

Always include pagination metadata: `{data: [...], next_cursor: "...", has_more: true}`.

## Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request body is malformed.",
    "details": [
      {"field": "email", "reason": "must be a valid email address"},
      {"field": "age", "reason": "must be a positive integer"}
    ],
    "request_id": "req_abc123"
  }
}
```

Every error response should include: machine-readable code, human-readable message, request ID for tracing, and structured details for programmatic handling.
