# mmdc Spacing Configuration

A JSON config file passed via `mmdc -c config.json` to control Mermaid diagram rendering for PDF/print output.

## Use Case

Complex flowcharts, ER diagrams, and sequence diagrams render with overlapping labels at mmdc's default spacing. This config increases node/rank/padding values to produce legible output suitable for print.

## Config File

Save as `mermaid-config.json`:

```json
{
  "flowchart": {
    "useMaxWidth": false,
    "htmlLabels": true,
    "padding": 25,
    "nodeSpacing": 60,
    "rankSpacing": 80,
    "curve": "basis"
  },
  "er": {
    "diagramPadding": 30,
    "layoutDirection": "TB",
    "minEntityWidth": 100,
    "minEntityHeight": 40,
    "entityPadding": 20,
    "fontSize": 11,
    "useMaxWidth": false
  },
  "sequence": {
    "diagramMarginX": 50,
    "diagramMarginY": 30,
    "actorMargin": 50,
    "width": 150,
    "height": 65,
    "boxMargin": 10,
    "boxTextMargin": 5,
    "noteMargin": 10,
    "messageMargin": 35,
    "mirrorActors": true,
    "bottomMarginAdj": 10,
    "useMaxWidth": false,
    "rightAngles": false,
    "showSequenceNumbers": false
  },
  "theme": "default",
  "themeVariables": {
    "fontSize": "11px",
    "fontFamily": "Inter, sans-serif",
    "primaryColor": "#f5ede4",
    "primaryTextColor": "#2a2018",
    "primaryBorderColor": "#65413a",
    "lineColor": "#65413a",
    "secondaryColor": "#132345",
    "tertiaryColor": "#e8d9c0",
    "noteBkgColor": "#1a2f5a",
    "noteTextColor": "#eceae5",
    "clusterBkg": "#f5ede4",
    "clusterBorder": "#132345",
    "edgeLabelBackground": "#f5ede4",
    "nodeBorder": "#65413a"
  },
  "maxTextSize": 50000
}
```

## Usage

```bash
# Render with custom spacing
mmdc -i diagram.mmd -o diagram.png -c mermaid-config.json

# Render at higher resolution with config
mmdc -i diagram.mmd -o diagram.png -c mermaid-config.json -w 2400 --backgroundColor '#f5ede4'
```

## Key Values

| Setting | Default | This Config | Effect |
|---------|---------|-------------|--------|
| `nodeSpacing` | 30-40 | 60 | Horizontal space between nodes in flowchart |
| `rankSpacing` | 50 | 80 | Vertical space between ranks in flowchart |
| `padding` | 15 | 25 | Internal padding around flowchart diagrams |
| `actorMargin` | 25 | 50 | Space between actors in sequence diagrams |
| `messageMargin` | 20 | 35 | Space between messages in sequence diagrams |
| `er.diagramPadding` | 15 | 30 | Padding around ER diagram entities |

## Post-Render Resizing

After rendering with `-w 2400`, the PNG will be too large for A4 pages. Resize for print:

```python
from PIL import Image
img = Image.open('diagram.png')
w, h = img.size
MAX_W, MAX_H = 1300, 2100
scale = min(1.0, MAX_W / w, MAX_H / h)
img.resize((int(w * scale), int(h * scale)), Image.LANCZOS).save('diagram.png')
```

This produces ~200dpi output that fits A4 portrait pages with 2.2cm margins.
