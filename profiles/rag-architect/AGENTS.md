# RAG Architect Profile: Agent Guidance

Use this profile when the user asks for production RAG, AI agent workflow architecture, evaluation design, observability, or implementation-ready AI system planning.

## Trigger Patterns

| User says | What it means |
|---|---|
| "Design a RAG system" | Full RAG architecture engagement |
| "Review my retrieval pipeline" | Retrieval quality, metadata, chunking, and eval review |
| "Make this AI feature production-ready" | Architecture, eval, observability, rollout, and issue backlog |
| "Write implementation issues for this agent" | Agent workflow decomposition and acceptance criteria |
| "Add RAG evals" | Golden dataset, metrics, scoring, regression gate, and sampling plan |

## Loading Order

Start with:

```python
skill_view('artifact-pyramids')
skill_view('architecture')
skill_view('data-architect')
skill_view('ml-engineering')
skill_view('software-architecture-analysis')
skill_view('verification-methodology')
```

Load optional skills as needed:

```python
skill_view('mermaid-diagrams')
skill_view('implementation-planning')
skill_view('technical-documentation')
```

## Output Contract

Return a durable artifact path whenever the user asks for architecture, planning, or review work. The recommended handoff is an artifact pyramid with:

- `00-index.md`
- `01-summary/`
- `02-analysis/`
- `03-dossiers/`

Include assumptions, tradeoffs, metrics, risks, and verification gates. Do not leave implementation agents with vague tasks.

## Quality Checks

Before finalizing, verify that the architecture includes:

- Ingestion and chunk identity strategy.
- Metadata and authorization boundaries.
- Retrieval routing and reranking policy.
- Citation and context assembly rules.
- Evaluation dataset and metrics.
- Observability and production feedback plan.
- Rollout and rollback strategy.
- Implementation-ready issues or next steps.
