# Integration Patterns

## External Call Resilience

| Pattern | What it protects against | Implementation |
|---------|------------------------|----------------|
| Retry with backoff | Transient failures | Exponential backoff + jitter, max retries |
| Circuit breaker | Sustained failures | Open after N failures, half-open after timeout |
| Timeout | Hanging connections | Connect + read + write timeouts per operation |
| Bulkhead | Cascading failures | Separate thread pool / connection pool per dependency |
| Idempotency key | Duplicate requests | Client-generated key, server deduplicates |

## Idempotency Key Pattern

```http
POST /api/payments
Idempotency-Key: 7c3d5e8f-a1b2-4c3d-8e5f-6a7b8c9d0e1f
```

| Aspect | Design |
|--------|--------|
| Key generation | Client UUID v4 |
| Storage | Key-value store with TTL (24h) |
| First request | Process normally, store result keyed by idempotency key |
| Duplicate request | Return stored result, no side effects |
| Expired key | Process as new request |
| In-flight request | Return 409 Conflict |

## Webhook Verification

| Mechanism | What it verifies | Implementation |
|-----------|-----------------|----------------|
| HMAC signature | Payload integrity, sender authenticity | Shared secret → HMAC of body → compare header |
| Webhook secret | Sender identity | Pre-shared secret, rotated periodically |
| Timestamp freshness | Replay prevention | Reject webhooks older than N minutes |

## Message Queue Consumer Patterns

| Pattern | When to use |
|---------|-------------|
| At-least-once delivery | Default — requires idempotent processing |
| Exactly-once (dedup) | When duplicates are unacceptable — requires dedup store |
| Batch processing | High throughput, latency-tolerant |
| Dead letter queue | Messages that can't be processed after max retries |

Every consumer should: acknowledge after processing, retry on transient failure, DLQ on permanent failure, and log at every stage.
