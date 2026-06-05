# Provenance Artifacts — Auxiliary Failover Metadata

The Artifact Pyramid is not just for research outputs. Any system that generates a chain of attempts with variable depth of detail is a natural fit. The auxiliary failover system in Hermes Agent (PR #32411, issue #36797) is a worked example.

## The Problem

The `_FailoverChatCompletions` wrapper walks a fallback chain when the primary provider fails. It logs each attempt but returns a bare result — downstream consumers have no way to tell *which* provider actually served the request without correlating timestamps against log files.

## The Pyramid Shape

The same call chain — a single walk across N providers with one winner — has natural progressive disclosure structure:

### Layer 1 — `served_by` (always present)

```
{
  "served_by": "openrouter/gpt-4o-mini",
  "fallback_chain_used": true,
  "fallback_count": 1
}
```

Every auxiliary response carries this. A single field, no overhead for the common case. UI surfaces and downstream agents that just need to know "who handled this" stop here.

### Layer 2 — Provenance trail (machine-readable, opt-in)

```
{
  "provenance": [
    {
      "provider": "opencode-go",
      "model": "deepseek-v4-flash",
      "status": "failed",
      "failure": "502 Bad Gateway",
      "latency_ms": 3200
    },
    {
      "provider": "openrouter",
      "model": "gpt-4o-mini",
      "status": "success",
      "latency_ms": 890
    }
  ]
}
```

Ordered array of every attempt. Added as an optional response field — consumers opt in by requesting it. No token cost for consumers that don't need it. A downstream RAG agent that needs to reason about extraction quality reads this layer.

### Layer 3 — Full diagnostic trace (debug endpoint only)

```
{
  "trace_id": "aux_comp_172832",
  "attempts": [
    {
      "provider": "opencode-go",
      "model": "deepseek-v4-flash",
      "request": {"messages_len": 4, "estimated_tokens": 24000},
      "error": "APIStatusError: 502 Bad Gateway\nbody: upstream unavailable",
      "started_at": "2026-06-01T12:00:01.234Z",
      "duration_ms": 3200
    },
    {
      "provider": "openrouter",
      "model": "gpt-4o-mini",
      "response": {"choices": [], "usage": {"total_tokens": 485}},
      "started_at": "2026-06-01T12:00:04.500Z",
      "duration_ms": 890
    }
  ]
}
```

Full error payloads, request context, timing watermarks. Gated behind a debug endpoint or explicit request — not attached to the response by default. An operator debugging a production incident reads this layer. Nobody else pays the token cost.

## Why This Fits

The `_FailoverChatCompletions` wrapper already has all three layers of information at runtime:

- **L1**: it knows the winning provider — trivially available
- **L2**: it tracks each attempt's status and failure reason in the `last_error` variable
- **L3**: it catches the full exception objects before deciding to continue or raise

The pyramid is the structured capture of that same walk, organized by consumer depth. The wrapper currently logs it and drops it — this frames what to capture instead.

## Related

- Issue #36797 — feature request for provenance-as-artifact-pyramid
- PR #32411 — adds `_FailoverAuxiliaryClient` with the wrapper that generates this data
- Reference: `references/artifact-pyramid-framework.md` for the general framework
