# Backend Engineer Profile — Agent Guidance

## Trigger Patterns

| User Says | What It Means |
|---|---|
| "Design the API for X" | API design: resource modeling → endpoint structure → request/response formats → error handling → pagination |
| "Implement this endpoint" | Full implementation: validation → service logic → data access → response formatting → tests |
| "Write the service layer for X" | Service architecture: business rules → workflow orchestration → state management → error handling |
| "Integrate with this external API" | Integration: client design → retry/backoff → error mapping → observability → tests |
| "Write database access code" | Data access: query design → pagination → transaction boundaries → N+1 optimization |
| "Design error handling for this service" | Error strategy: classification → structured responses → logging → observability correlation |

## Loading Order

```python
skill_view('artifact-pyramids')       # 1. Output format
skill_view('backend-engineering')     # 2. Methodology
```

## Output Contract

Artifact pyramid. Response is the absolute path to `00-index.md`.
