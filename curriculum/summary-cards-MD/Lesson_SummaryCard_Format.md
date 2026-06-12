# Summary Card Format Specification

*Reference for generating all BearBots lesson summary cards. Match this exactly.*

---

## Overview

- **2 pages**, designed for duplex (front/back) printing on US Letter
- **Page 1** — all lesson content
- **Page 2** — notes page (header repeated, full lined box, footer)
- Built with **ReportLab canvas** (direct drawing, not Platypus flowables)
- All coordinates in **points** (72 pt = 1 inch)

---

## Fonts

```python
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('DV',  '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVB', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
```

- `DV` / `DVB` — used for step numbers, checkboxes, and any text needing proper Unicode rendering
- `Helvetica` / `Helvetica-Bold` / `Helvetica-Oblique` — used everywhere else

---

## Color Palette

| Name | Hex | Used for |
|---|---|---|
| `TEAL` | `#2D6B6B` | Section bar bg (primary), header bg, footer bg |
| `TEAL_LT` | `#EAF4F4` | Box fill (teal sections) |
| `PURPLE` | `#6B4A9B` | Section bar bg (secondary) |
| `PURPLE_LT` | `#F0ECF8` | Box fill (purple sections) |
| `ORANGE` | `#B8762A` | Section bar bg (tertiary / questions) |
| `ORANGE_LT` | `#FAF3E8` | Box fill (orange sections, My Notes) |
| `RULE` | `#CCCCCC` | Box stroke, ruled lines |
| `TXT` | `#222222` | Body text |
| `TXT_MED` | `#555555` | Secondary text, italic prompts |
| `WHITE` | `#FFFFFF` | Bar text, badge text |
| `HDR_BG` | `#2D6B6B` | Header background (same as TEAL) |
| `BADGE_GRN` | `#4DAF82` | Lesson number badge circle |

**Key concept card colors** (5 cards, in order):

| Card | Hex |
|---|---|
| 1st | `#2D6B6B` (teal) |
| 2nd | `#6B4A9B` (purple) |
| 3rd | `#B8762A` (orange) |
| 4th | `#2D6B6B` (teal) |
| 5th | `#6B4A9B` (purple) |

---

## Page Geometry

```python
W, H     = letter          # 612 × 792 pt
ML = MR  = 0.42 * inch     # 30.2 pt left/right margins
MT = MB  = 0.38 * inch     # 27.4 pt top/bottom margins
CW       = W - ML - MR     # ≈ 551 pt content width
GAP      = 7               # pt gap between side-by-side boxes
COL_W    = (CW - GAP) / 2  # ≈ 272 pt each column (exactly equal)
```

---

## Layout Constants

```python
HDR_H      = 68    # header height
BIG_IDEA_H = 58    # Big Idea section height (bar 22 + content 36)
CONCEPTS_H = 100   # Key Concepts section height (bar 22 + cards 78)
BAR_H      = 22    # all section bar heights
PAD        = 6     # internal padding top/bottom inside boxes
CARD_GAP   = 10    # vertical gap between sections
FOOTER_H   = 26    # footer bar height
```

---

## Page 1 Structure (top to bottom)

```
┌─────────────────────────────────────────────┐  HDR_H = 68
│  HEADER                                     │
└─────────────────────────────────────────────┘
  [CARD_GAP = 10]
┌─────────────────────────────────────────────┐  BIG_IDEA_H = 58
│  THE BIG IDEA                               │
└─────────────────────────────────────────────┘
  [CARD_GAP = 10]
┌─────────────────────────────────────────────┐  CONCEPTS_H = 100
│  KEY CONCEPTS (5 cards)                     │
└─────────────────────────────────────────────┘
  [CARD_GAP = 10]
┌──────────────────────┐ ┌────────────────────┐  ROW2_TOP_H = max(left, right)
│  THE SETUP WORKFLOW  │ │  AFTER THIS LESSON │
│  (teal, left col)    │ │  (purple, right)   │
└──────────────────────┘ └────────────────────┘
  [CARD_GAP = 10]
┌──────────────────────┐ ┌────────────────────┐  ROW2_BOT_H = expands to fill
│  QUESTIONS I STILL   │ │  KEY VOCABULARY    │  remaining space above footer
│  HAVE (orange, left) │ │  (teal, right)     │
└──────────────────────┘ └────────────────────┘
  [CARD_GAP = 10]
┌─────────────────────────────────────────────┐  FOOTER_H = 26, pinned to MB
│  FOOTER (teal bar)                          │
└─────────────────────────────────────────────┘
```

**Height rules:**
- `ROW2_TOP_H = max(SETUP_H, AFTER_H)` — both boxes in the row are the same height, driven by whichever has more content
- `ROW2_BOT_H` — dynamically expands to fill all remaining space above the footer. The bottom row always touches the footer gap.
- If total content overflows, `CARD_GAP` is reduced proportionally (minimum 3 pt)

---

## Section Box Drawing

Every content section (Big Idea, Key Concepts, Setup Workflow, etc.) is drawn as:

1. **Rounded rectangle** (r=5) with light fill and `RULE` stroke, lw=0.75
2. **Colored bar** on top — rounded at top corners only (achieved by drawing a full roundRect extending below and covering the bottom round with a plain rect)
3. **White bar label text** — `Helvetica-Bold` 7.5 pt, left-aligned, 8 pt from left edge, vertically centered in bar

```python
def section_box(c, x, y, w, h, label, bar_color, box_fill, r=5, bar_h=22):
    # 1. outer box
    c.setFillColor(box_fill); c.setStrokeColor(RULE); c.setLineWidth(0.75)
    c.roundRect(x, y, w, h, r, fill=1, stroke=1)
    # 2. bar — rounded top only
    c.setFillColor(bar_color); c.setLineWidth(0)
    c.roundRect(x, y+h-bar_h, w, bar_h+r, r, fill=1, stroke=0)  # extends r below
    # 3. label
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 7.5)
    c.drawString(x+8, y+h-bar_h/2-3.5, label)
```

---

## Header

- Teal rounded rectangle (`r=6`) spanning full content width, height 68 pt
- **Left side:**
  - Module line: `"MODULE X  —  LESSON XX"` — `Helvetica-Bold` 8 pt, color `#A8D4D4`, 10 pt from left, 15 pt from top
  - Title: lesson title — `Helvetica-Bold` 24 pt, `WHITE`, 10 pt from left, 50 pt from top
- **Right side (right-aligned, 50 pt from right edge to leave room for badge):**
  - Stack line: `"Java  |  AdvantageKit  |  XRP"` — `Helvetica-Bold` 8.5 pt, `#A8D4D4`
  - Keep line: `"Keep this card. Add it to your binder."` — `Helvetica-Oblique` 7.5 pt, `#BBDDDD`
- **Badge:** circle radius 20, fill `BADGE_GRN` (`#4DAF82`), stroke `WHITE` lw=2, centered 24 pt from right edge at vertical midpoint. Lesson number in `Helvetica-Bold` 18 pt white, centered.

---

## Big Idea Section

- Full content width, `TEAL` bar, `TEAL_LT` fill
- **Bold line:** lesson's big idea statement — `Helvetica-Bold` 11 pt, `TXT`, centered
- **Italic line:** supporting sentence — `Helvetica-Oblique` 8.5 pt, `TXT_MED`, centered
- Both lines centered horizontally in the box below the bar

---

## Key Concepts Section

- Full content width, `TEAL` bar, `TEAL_LT` fill
- Contains **5 concept cards** in a horizontal row with 4 pt gaps between them
- Each card: `card_w = (CW - 4*4) / 5`

**Card structure (bottom to top in canvas coords):**

```
┌──────────────────┐  ← rounded rect, white fill, RULE stroke
│  description     │  centered text, Helvetica 7.5 pt, 3 lines
│  (3 lines)       │  vertically centered in lower portion
├──────────────────┤  ← colored bar, flat bottom / rounded top
│  Role label      │  Helvetica 7 pt, white, centered (lower bar)
│  CONCEPT NAME    │  Helvetica-Bold 7.5 pt, white, centered (upper bar)
└──────────────────┘
```

- **Bar heights:** name row = 16 pt, role row = 12 pt, total bar = 28 pt
- If title wraps to 2 lines: reduce font to 6.5 pt, line height 8.5 pt
- Description: split on `\n`, centered, vertically centered in remaining card height

---

## 2×2 Grid Sections

**Column widths:** both columns = `COL_W = (CW - GAP) / 2` exactly. Gap between = 7 pt.

**Row height rule:** within each row, both boxes are drawn at `max(left_h, right_h)`.

### THE SETUP WORKFLOW (top-left, TEAL)

- Numbered steps: bold step number (`DVB` 7.5 pt) + regular text (`DV` 7.5 pt)
- Step number drawn at x+8, text at x+8+14 (14 pt indent)
- Line height 11 pt, 3 pt gap between steps
- Text wraps within `COL_W - 16 - 14` pt

### AFTER THIS LESSON I CAN... (top-right, PURPLE)

- Checkbox items with drawn checkboxes (not unicode)
- Checkbox: 8×8 pt white rect, `#888888` stroke, lw=0.75, drawn at rx+8
- Text: `DV` 7.5 pt, starts at rx+8+14 (14 pt indent from left edge)
- Line height 11 pt, 3 pt gap between items

### QUESTIONS I STILL HAVE (bottom-left, ORANGE)

- Italic prompt: `Helvetica-Oblique` 8 pt, `TXT_MED`
- Ruled lines: `RULE` color, lw=0.5, spaced 18 pt apart, 8 pt from left/right edges
- Height expands dynamically to fill available space above footer

### KEY VOCABULARY (bottom-right, TEAL)

- Each entry: **bold term** (`Helvetica-Bold` 7.5 pt) + ` —` + regular definition (`Helvetica` 7.5 pt)
- Term and dash drawn separately to allow bold/normal on same line
- Line height 11 pt, 3 pt gap between entries
- Height matches Questions box (both set to `ROW2_BOT_H_draw`)

---

## Footer

- Teal (`TEAL`) rounded rectangle (`r=4`), height 26 pt, **pinned to `MB`** (bottom margin)
- Three text elements in white, all vertically centered:
  - Left: `"FRC Programming Curriculum — Lesson XX"` — `Helvetica-Bold` 7.5 pt
  - Center: `"Next: Lesson XX — [next lesson title]"` — `Helvetica` 7.5 pt, `drawCentredString`
  - Right: `"Keep this. Collect all 8."` — `Helvetica` 7.5 pt, `drawRightString`

---

## Page 2 Structure

- **Header** — identical to page 1
- **MY NOTES section** — full content width, `TEAL` bar, `ORANGE_LT` fill
  - Height: `notes_top - MB - FOOTER_H - CARD_GAP * 2` (fills between header gap and footer gap)
  - Y position: `MB + FOOTER_H + CARD_GAP`
  - Italic prompt at top: `"Write anything here — surprises, connections, things to look up later."`
  - Ruled lines: `RULE` lw=0.5, spaced 22 pt, starting 32 pt below bar, stopping 10 pt from bottom
- **Footer** — identical to page 1

---

## Content Variables Per Lesson

When generating a new lesson card, change only these:

```python
# ── HEADER ────────────────────────────────────────────────────────────────────
module_line  = "MODULE X  —  LESSON XX"   # e.g. "MODULE 1  —  LESSON 01"
title        = "Lesson title here"         # e.g. "Setup + first drive"
badge_num    = "01"                        # lesson number as string

# ── BIG IDEA ──────────────────────────────────────────────────────────────────
big_idea_bold   = "The bold headline statement."
big_idea_italic = "The supporting sentence in italics."

# ── KEY CONCEPTS (5 entries) ──────────────────────────────────────────────────
concepts = [
    ("Concept Name",  "Role label",  "Line 1\nLine 2\nLine 3"),
    ...  # always exactly 5 cards
]

# ── SETUP WORKFLOW (or equivalent left-column workflow) ───────────────────────
left_col_label = "THE SETUP WORKFLOW"      # or lesson-specific label
steps = [
    ("1", "Step description text"),
    ...
]

# ── AFTER THIS LESSON (checkboxes) ───────────────────────────────────────────
checks = [
    "I can do this thing",
    ...
]

# ── VOCABULARY ────────────────────────────────────────────────────────────────
vocab = [
    ("Term",  "Definition text"),
    ...  # 4–6 entries
]

# ── FOOTER ───────────────────────────────────────────────────────────────────
footer_left   = "FRC Programming Curriculum — Lesson 01"
footer_center = "Next: Lesson 02 — Next lesson title here."
footer_right  = "Keep this. Collect all 8."
```

---

## Generation Notes

- The **bottom row always expands** to fill remaining page height. Don't hard-code its height.
- The **overflow guard** auto-reduces `CARD_GAP` if total content height exceeds available space. Keep it — content-heavy lessons may need it.
- Keep concept card descriptions to **3 lines max**. Longer text won't fit in the card area.
- Keep checklist items **concise** — each item should fit in 1–2 wrapped lines at 7.5 pt.
- Keep step text **concise** — steps that wrap to 3+ lines push the box very tall.
- The right-column panel for lessons that aren't Lesson 01 may use a **different label and content type** (e.g. "KEYBOARD DRIVING KEYS" in Lesson 1's original). The bar color stays `PURPLE` and fill stays `PURPLE_LT`. The content inside can be any canvas-drawn elements.
