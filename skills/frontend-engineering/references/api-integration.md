# API Integration

## API Client Design

| Layer | Responsibility |
|-------|---------------|
| Client instance | Base URL, default headers, timeout, interceptors |
| Request interceptor | Auth token injection, request logging, request ID |
| Response interceptor | Token refresh on 401, error normalization, response logging |
| Service module | Typed API methods per domain, request/response transformation |
| Hook layer | Data fetching hooks with loading/error/empty states |

## Auth Token Flow

```
Login → Store token → Attach to requests → Detect expiry → Refresh → Retry
                                               ↓
                                         Re-login on refresh failure
```

| Storage location | Pros | Cons |
|-----------------|------|------|
| HTTP-only cookie | Secure against XSS | CSRF vulnerability, harder for SPA to read |
| Memory (variable) | Most secure, not persisted | Lost on page refresh |
| localStorage | Survives refresh, simple | Accessible by any JS on the page |
| Session storage | Survives refresh in same tab | Cleared on tab close |

## Real-Time Updates

| Protocol | When to use | Connection management |
|----------|-------------|---------------------|
| WebSocket | Bidirectional, low-latency | Reconnect with backoff, heartbeat, fallback to polling |
| SSE (Server-Sent Events) | Server-to-client only, simpler than WebSocket | Automatic reconnection, event ID for resume |
| Short polling | Simple, no server push support | Fixed interval, wasteful when idle |
| Long polling | When WebSocket/SSE unavailable | Persistent connection, complex timeout handling |
