# PDF Rendering Pipeline

Full pipeline for converting architecture documentation (markdown with Mermaid diagrams) into a PDF with properly rendered, full-page diagrams.

This reference captures the lessons from a session where six PDF iterations were needed to fix defects: ASCII art not converted, Mermaid code blocks unrendered, SVGs constrained by max-width, data URI images not filling the page, and Pandoc math-parsing SVG CSS.

## Pipeline Overview

```bash
# Step 1: Pre-render all Mermaid diagrams to SVG
npx @mermaid-js/mermaid-cli -i diagram.mmd -o diagram.svg --width 800

# Step 2: Embed SVGs in markdown (NOT as data URI img tags)
# Use raw <svg> tags inline in the markdown file

# Step 3: Convert markdown to HTML via Pandoc
pandoc report.md -f markdown -t html5 --embed-resources --standalone \
  -o report.html --metadata title="Title" \
  --syntax-highlighting=none -f markdown-raw_tex

# Step 4: Strip max-width constraints from SVG tags in HTML
sed -i '' 's/max-width: [0-9]*\.[0-9]*px/max-width: 100%/g' report.html

# Step 5: Add width:100% to all img tags (catches data-URI SVGs)
# Add style="width:100%;height:auto;max-width:100%;display:block;margin:0 auto;"

# Step 6: Generate PDF via Puppeteer
node generate-pdf.js
```

## Critical Rules

### Rule 1: Pre-render, don't serve code blocks

Mermaid code blocks (```mermaid```) do NOT render in the Pandoc → HTML → Puppeteer pipeline. Pandoc converts them to static `<pre>` blocks, and Puppeteer does not execute JavaScript to render them.

**Always:** Pre-render to SVG via mmdc, then embed the SVG.

### Rule 2: Embed SVG as raw markup, not data URIs

When SVGs are embedded as `<img src="data:image/svg+xml;base64,...">`, the SVG's internal `max-width` and `viewBox` cannot be overridden by page-level CSS. The image stays at its native size.

**Preferred:** Insert the raw `<svg>...</svg>` markup directly into the markdown or HTML. This lets page-level CSS (width:100%, max-width:100%) control scaling.

**Fallback (img tags):** If using `<img>` tags, add explicit `style="width:100%;height:auto;max-width:100%;display:block;"` to the `<img>` element itself. Do NOT rely on SVG-internal CSS.

### Rule 3: Strip SVG max-width constraints

Mermaid-generated SVGs have hardcoded `max-width` values:
```html
<svg style="max-width: 881.07px; ..."> 
```
These override any `width: 100%` you try to apply. Replace all instances with `max-width: 100%`.

```bash
# For inline SVGs:
sed -i '' 's/max-width: [0-9]*\.[0-9]*px/max-width: 100%/g' report.html

# For base64 data URIs, the max-width is inside the base64 encoding
# and cannot be fixed by sed. Avoid data URIs.
```

### Rule 4: Portrait orientation (TD over LR)

All diagrams destined for PDF must use `flowchart TD` (top-down), not `flowchart LR` (left-to-right). See `portrait-layout.md` for:
- Max 4 nodes per subgraph row
- Labels under 30 characters
- Sequence diagrams with max 4 participants
- viewBox must have height > width

### Rule 5: Page breaks before/after full-page diagrams

```html
<div style="page-break-before: always;"></div>

<!-- Diagram content here -->

<div style="page-break-after: always;"></div>
```

### Rule 6: Pandoc TeX/SVG conflicts

Pandoc interprets CSS selectors with `[id=` patterns as TeX math. This produces warnings like:
```
[WARNING] Could not convert TeX math ="-arrowhead"] path{fill:#333...
```

These warnings are **harmless** when SVGs are pre-rendered and embedded as `<svg>` or `<img>` tags. The warnings don't affect the output. Use `--syntax-highlighting=none -f markdown-raw_tex` flags to minimize issues.

## Puppeteer Setup

```javascript
const puppeteer = require("/Users/magnus/.npm/_npx/d2654f9a588e9579/node_modules/puppeteer");

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"]
  });
  const page = await browser.newPage();

  const htmlPath = "file:///tmp/report.html";
  await page.goto(htmlPath, { waitUntil: "networkidle0", timeout: 30000 });
  await page.evaluate(() => new Promise(r => setTimeout(r, 2000)));

  await page.pdf({
    path: "/tmp/output.pdf",
    format: "Letter",
    printBackground: true,
    margin: { top: "0.5in", bottom: "0.5in", left: "0.5in", right: "0.5in" }
  });
  await browser.close();
})();
```

Puppeteer is available as a dependency of `@mermaid-js/mermaid-cli` at the path above. It is NOT installed globally.

## QA Checklist for PDF Output

Before sending any PDF to the user, verify ALL of these:

- [ ] No ASCII art diagrams (grep for box-drawing chars: ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ─ │)
- [ ] No raw ```mermaid code blocks (grep for '```mermaid')
- [ ] All SVGs pre-rendered (not relying on CDN JS execution)
- [ ] SVGs fill page width (check html for width:100% on svg/img tags)
- [ ] No hardcoded max-width pixel values in SVGs (check for 'max-width: Npx')
- [ ] Flowcharts use TD not LR (grep for 'flowchart LR')
- [ ] Page breaks before/after each full-page diagram (grep for 'page-break')
- [ ] PDF file size > 100KB (diagrams rendered)
- [ ] Visual verification: open the HTML in a browser before generating PDF
