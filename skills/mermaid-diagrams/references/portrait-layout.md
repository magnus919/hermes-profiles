# Portrait Layout for Mermaid Diagrams

When producing diagrams for PDF, print, or portrait-oriented screens (GitHub, GitLab, mobile), use `flowchart TD` (top-down) instead of `flowchart LR` (left-to-right). This stacks the diagram vertically so it fills a portrait page rather than shrinking to fit between paragraphs.

## Forcing Portrait Output from the Dagre Engine

Mermaid's default dagre layout engine optimizes for compactness, which often produces wide diagrams even with `flowchart TD`. Two techniques reliably force portrait output:

### Technique 1: Wrapper Subgraph with `direction TB`

Wrap ALL nodes and edges inside a single subgraph with `direction TB`. This constrains the layout engine to a tall container:

```mermaid
flowchart TD
  subgraph C["Diagram Title"]
    direction TB
    A[Node A]
    B[Node B]
    C[Node C]
    A --> B
    B --> C
  end
```

This transformed a container diagram from 2271×1100 (landscape) to 641×928 (portrait) in testing.

### Technique 2: Invisible Chain Edges (`~~~`)

When nodes at the same level still spread horizontally, add invisible chain edges to force vertical stacking:

```mermaid
flowchart TD
  subgraph C["Stacked Diagram"]
    direction TB
    A[Node A]
    B[Node B]
    C[Node C]
    D[Node D]

    A --> B
    A ~~~ C
    B ~~~ D
  end
```

The `~~~` edges are invisible but tell dagre "these nodes must be in different rows." Chain them through all nodes that dagre would otherwise place side by side.

### Splitting Complex Diagrams

Diagrams with more than 12-15 nodes or with dense cross-connections cannot be made portrait. Split into multiple sub-diagrams of 5-10 nodes each.

| Original (landscape) | Split into | Portrait results |
|---------------------|------------|-----------------|
| 20-node component diagram (1261×799) | 4 sub-diagrams (5 nodes each) | All 281×661 or better |
| 10-node architecture pattern (913×580) | 2 sub-diagrams (5-6 nodes each) | Both 367×799 and 368×532 |

## QA: ViewBox Dimension Check

Before delivery, extract the viewBox from every rendered SVG and verify width < height:

```bash
python3 -c "
import re
with open('diagram.svg') as f:
    c = f.read()
vb = re.search(r'viewBox=\"([^\"]*)\"', c)
w, h = float(vb.group(1).split()[2]), float(vb.group(1).split()[3])
if w > h:
    print(f'LANDSCAPE: {w:.0f}x{h:.0f} — FIX')
"
```

Text-pattern checks for "flowchart LR" are insufficient — Mermaid's dagre engine can produce landscape output from TD input.

## PDF Embedding Rules

- **Always base64-inline SVGs** — Raw SVG tags passed through Pandoc get CSS corrupted (especially `@keyframes`). Use `<img src="data:image/svg+xml;base64,...">`.
- **Never use filesystem paths** — `<img src="/tmp/...svg">` breaks in PDF generation. Only base64 data URIs survive Pandoc → HTML → Puppeteer.
- **`width:100%` on all `<img>` tags** — `style="width:100%;height:auto;max-width:100%;display:block;margin:0 auto;"`

## Rules for Portrait-Oriented Diagrams

1. **Always use `flowchart TD`** for architecture diagrams destined for PDF or portrait screens
2. **Page break before and after** each full-page diagram:
   ```html
   <div style="page-break-before: always;"></div>
   <img src="data:image/svg+xml;base64,...">
   <div style="page-break-after: always;"></div>
   ```
3. **Keep the viewBox taller than wide.** The rendered SVG's viewBox must have height > width.
4. **Max 4 nodes per row, max 12-15 nodes per diagram.** Split complex diagrams into sub-diagrams.
5. **Short labels under 30 characters.** Use `<br/>` for multi-line. Abbreviate: "scraper-svc" not "Web Scraping Service".
6. **Sequence diagrams: max 4 participants.** More creates wide layout. Split into separate diagrams.
7. **Within TD, use `direction LR` on 2-3 node chains only.**
8. **Light background for print** — dark themes waste toner in PDF.
9. **Render at `--width 800`** via mmdc for A4/Letter fit.
10. **Node shapes: `[()]` for databases, `[text]` for services.**

## Verification Checklist

- [ ] `flowchart TD` not `LR`
- [ ] Wrapper subgraph with `direction TB` applied
- [ ] Page break divs before and after each diagram
- [ ] Base64-inlined SVGs (no raw SVG tags, no filesystem paths)
- [ ] Every rendered SVG viewBox: width < height
- [ ] Node labels under 30 chars
- [ ] Light background for print
- [ ] Max 4 participants per sequence diagram
- [ ] No ASCII art — all diagrams are rendered Mermaid SVG
