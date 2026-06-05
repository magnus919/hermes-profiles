# Sequence Diagrams

Best for: interaction protocols, API call flows, agent handoffs, multi-service communication.

## Basic Syntax

```mermaid
sequenceDiagram
  participant A as Service A
  participant B as Service B

  A->>B: Request
  B-->>A: Response
```

## Participant Types (v11+)

```mermaid
sequenceDiagram
  participant A as 🧑 User
  participant G as ⚙️ API Gateway
  participant B as 🕸️ Browser
  database D as 📦 Database
  actor E as 🌐 External

  A->>G: scrape(url)
  G->>B: render(url)
  B->>D: cache result
  B-->>A: markdown
```

## Loops and Conditions

```mermaid
sequenceDiagram
  participant A as Agent
  participant S as Search-Svc

  loop Until goal satisfied
    A->>S: search(query)
    S-->>A: results
    alt results sufficient
      A->>S: stop
    else need more
      A->>S: refine query
    end
  end
```

## Activation (Lifecycle)

```mermaid
sequenceDiagram
  participant A as A
  participant B as B

  activate A
  A->>B: Request
  activate B
  B-->>A: Response
  deactivate B
  deactivate A
```

## Critical Rules

- `activate`/`deactivate` must be balanced
- `alt`/`else`/`end` for conditional branches
- `loop`/`end` for iterations
- `par`/`and`/`end` for parallel
- `break`/`end` for exit conditions
- `critical`/`option`/`end` for critical sections
