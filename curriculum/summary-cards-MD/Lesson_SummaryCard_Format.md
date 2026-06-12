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
- **Do not use Unicode arrow/special characters (`→`, `—`) with Helvetica** — they may render as black boxes. Use ASCII equivalents (`->`, `-`) or switch to `DV` for those strings.

---

## Color Palette

| Name | Hex | Used for |
|---|---|---|
| `TEAL` | `#2D6B6B` | Section bar bg (primary), header bg, footer bg |
| `TEAL_LT` | `#EAF4F4` | Box fill (teal sections) |
| `PURPLE` | `#6B4A9B` | Section bar bg (secondary) |
| `PURPLE_LT` | `#F0ECF8` | Box fill (purple sections) |
| `ORANGE` | `#B8762A` | Section bar bg (tertiary) |
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
│  THE SETUP WORKFLOW  │ │  AFTER THIS LESSON │  capped so bottom row gets
│  (teal, left col)    │ │  (purple, right)   │  at least 42% of available space
└──────────────────────┘ └────────────────────┘
  [CARD_GAP = 10]
┌──────────────────────┐ ┌────────────────────┐  ROW2_BOT_H = fills remaining
│  BOTTOM-LEFT SECTION │ │  KEY VOCABULARY    │  space above footer
│  (lesson-specific)   │ │  (teal, right)     │
└──────────────────────┘ └────────────────────┘
  [CARD_GAP = 10]
┌─────────────────────────────────────────────┐  FOOTER_H = 26, pinned to MB
│  FOOTER (teal bar)                          │
└─────────────────────────────────────────────┘
```

**Height rules:**
- `ROW2_TOP_H = min(max(SETUP_H, AFTER_H), max_top_h)` — driven by content, but capped to protect bottom row
- `ROW2_BOT_H` — dynamically expands to fill all remaining space above the footer. Always touches the footer gap.
- **Bottom row priority:** bottom row gets at least 42% of available space between concepts and footer. Cap the top row height accordingly: `max_top_h = available - CARD_GAP - max(90, available * 0.42)`
- If total content overflows, `CARD_GAP` is reduced proportionally (minimum 3 pt)

---

## Section Box Drawing

Every content section is drawn as:

1. **Rounded rectangle** (r=5) with light fill and `RULE` stroke, lw=0.75
2. **Colored bar** on top — rounded at top corners only. Achieved by drawing a full `roundRect` extending `r` below the bar top, then covering the unwanted bottom rounding with a plain `rect`.
3. **White bar label text** — `Helvetica-Bold` 7.5 pt, left-aligned, 8 pt from left edge, vertically centered in bar

```python
def section_box(c, x, y, w, h, label, bar_color, box_fill, r=5, bar_h=22):
    # 1. outer box
    c.setFillColor(box_fill); c.setStrokeColor(RULE); c.setLineWidth(0.75)
    c.roundRect(x, y, w, h, r, fill=1, stroke=1)
    # 2. bar — rounded top only
    c.setFillColor(bar_color); c.setLineWidth(0)
    c.roundRect(x, y+h-bar_h, w, bar_h+r, r, fill=1, stroke=0)  # extends r below
    c.rect(x, y+h-bar_h, w, r, fill=1, stroke=0)                 # cover bottom round
    # 3. label
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 7.5)
    c.drawString(x+8, y+h-bar_h/2-3.5, label)
```

---

## Header

- Teal rounded rectangle (`r=6`) spanning full content width, height 68 pt
- **Left side:**
  - Module line: `"MODULE X  —  LESSON XX"` — `Helvetica-Bold` 8 pt, color `#A8D4D4`, 10 pt from left, 15 pt from top
  - Title: lesson title — `Helvetica-Bold` 20 pt, `WHITE`, 10 pt from left, 50 pt from top
  - **Title length rule:** keep short enough to fit ~400 pt at 20 pt bold without touching the badge. Shorten from the official lesson title if needed; update `site-config.js` to match.
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
- Card width: `card_w = (CW - 4*4) / 5`
- Cards sit inside the section box with `card_pad_top = 5` and `card_pad_bot = 5` below the bar
- Card height: `card_h = CONCEPTS_H - BAR_H - card_pad_top - card_pad_bot`

**Card structure (top to bottom):**

```
┌──────────────────┐  ← rounded rect, white fill, RULE stroke lw=0.75, r=4
│  CONCEPT NAME    │  Helvetica-Bold 7.5 pt (6.5 if too wide), white, centered
│  Role label      │  Helvetica 7 pt, white, centered
├──────────────────┤  ← bottom of coloured bar
│  description     │  Helvetica 7.5 pt, TXT, centered, 3 lines max
│  (3 lines)       │  vertically centered in remaining card height
└──────────────────┘
```

- **Bar heights:** name row = 16 pt, role row = 12 pt, total bar = 28 pt
- Bar draw: `roundRect` for top rounding + `rect` to cover bottom rounding (same pattern as section_box)
- Description: split on `\n`, 3 lines max, line height 9 pt, vertically centered in `card_h - total_bar_h`
- If concept name is too wide at 7.5 pt, reduce to 6.5 pt

---

## 2×2 Grid Sections

**Column widths:** both columns = `COL_W = (CW - GAP) / 2` exactly. Gap between = 7 pt.

**Row height rule:** within each row, both boxes drawn at the same height.
- Top row: `min(max(SETUP_H, AFTER_H), max_top_h)` — see bottom row priority rule above
- Bottom row: fills all remaining space

### THE SETUP WORKFLOW (top-left, TEAL)

- Numbered steps: bold step number (`DVB` 7.5 pt) + regular text (`DV` 7.5 pt)
- Step number at x+8; text at x+8+14 (14 pt indent)
- Line height 11 pt, 3 pt gap between steps
- Text wraps within `COL_W - 16 - 14` pt
- Start y: `box_top_y + box_h - BAR_H - PAD - line_h` (first baseline below bar)

### AFTER THIS LESSON I CAN... (top-right, PURPLE)

- Checkbox items with drawn checkboxes (not unicode)
- Checkbox: 8×8 pt white rect, `#888888` stroke, lw=0.75
- **Checkbox vertical alignment:** centre the checkbox on the first line baseline of each item: `cb_y = cy - cb_size/2 + font_size/2 - 1`
- Text: `DV` 7.5 pt, starts at x+8+14 (14 pt indent from box left)
- Line height 11 pt, 3 pt gap between items
- Start y: same formula as Setup Workflow

### BOTTOM-LEFT SECTION (lesson-specific, TEAL by default)

The bottom-left section label and content vary per lesson. Examples:

| Lesson | Label | Content type |
|---|---|---|
| 01 | QUESTIONS I STILL HAVE | Ruled lines (ORANGE bar) |
| 02 | PROGRAM FLOW | Embedded image (TEAL bar) |

**Ruled lines variant:**
- Italic prompt: `Helvetica-Oblique` 8 pt, `TXT_MED`, 14 pt below bar
- Lines: `RULE` color, lw=0.5, spaced 18 pt, 8 pt from left/right edges

**Embedded image variant:**
- Use `c.drawImage(path, x, y, w, h, preserveAspectRatio=True, mask='auto')`
- Pad image 6 pt inside the section box on all sides
- Available image area: `w - 12` wide, `h - BAR_H - 12` tall
- Maintain aspect ratio: compare box aspect to image aspect, constrain by the binding dimension, centre on the other axis
- Bar color: TEAL, fill: TEAL_LT

### KEY VOCABULARY (bottom-right, TEAL)

- **Two-column layout:** terms left-aligned, definitions left-aligned at a fixed indent
- **Column break:** measure widest term with `Helvetica-Bold` at 7.5 pt; add 8 pt gap → `col_break = max_term_w + 8`
- Term: `Helvetica-Bold` 7.5 pt, `TXT`
- Definition: `Helvetica` 7.5 pt, `TXT`, wraps within `COL_W - 16 - col_break`
- **No dash separator between term and definition**
- Line height 11 pt, 3 pt gap between entries
- Start y: same formula as other sections

---

## Footer

- Teal (`TEAL`) rounded rectangle (`r=4`), height 26 pt, **pinned to `MB`**
- Three text elements in white, all vertically centered at `y + h/2 - 3.5`:
  - Left: `"FRC Programming Curriculum — Lesson XX"` — `Helvetica-Bold` 7.5 pt
  - Center: `"Next: Lesson XX — [next lesson title]"` — `Helvetica` 7.5 pt, `drawCentredString`
  - Right: `"Keep this. Collect all 8."` — `Helvetica` 7.5 pt, `drawRightString`

---

## Page 2 Structure

- **Header** — identical to page 1
- **MY NOTES section** — full content width, `TEAL` bar, `ORANGE_LT` fill
  - Y position: `MB + FOOTER_H + CARD_GAP`
  - Height: fills from that y to `hdr_y - CARD_GAP`
  - Italic prompt: `"Write anything here — surprises, connections, things to look up later."` — 14 pt below bar
  - Ruled lines: `RULE` lw=0.5, spaced 22 pt, starting 32 pt below bar top, stopping 8 pt from bottom
- **Footer** — identical to page 1

---

## Content Variables Per Lesson

When generating a new lesson card, change only these:

```python
# ── HEADER ────────────────────────────────────────────────────────────────────
module_line  = "MODULE X  —  LESSON XX"   # e.g. "MODULE 1  —  LESSON 02"
title        = "Lesson title here"         # shortened to fit header at 20pt bold
badge_num    = "02"                        # lesson number as string

# ── BIG IDEA ──────────────────────────────────────────────────────────────────
big_idea_bold   = "The bold headline statement."
big_idea_italic = "The supporting sentence in italics."

# ── KEY CONCEPTS (always exactly 5 entries) ───────────────────────────────────
concepts = [
    ("Concept Name",  "Role label",  "Line 1\nLine 2\nLine 3"),
    ...
]

# ── SETUP WORKFLOW ────────────────────────────────────────────────────────────
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

# ── BOTTOM-LEFT SECTION ───────────────────────────────────────────────────────
# Define bot_left_label and a draw_bot_left(c, x, y, w, h) function per lesson.
# Default: ruled lines. Alternative: embedded image.

# ── VOCABULARY ────────────────────────────────────────────────────────────────
vocab = [
    ("Term",  "Definition text — no dash, two-column layout"),
    ...  # 4-6 entries
]

# ── FOOTER ───────────────────────────────────────────────────────────────────
footer_left   = "FRC Programming Curriculum — Lesson XX"
footer_center = "Next: Lesson XX — Next lesson title here."
footer_right  = "Keep this. Collect all 8."
```

---

## Generation Notes

- **Unicode safety:** avoid `→`, `—`, and other non-ASCII in Helvetica strings. Use `->` and `-` or switch to `DV`/`DVB` fonts.
- **Bottom row always expands** to fill remaining page height. Never hard-code its height.
- **Bottom row priority:** give it at least 42% of the space between concepts and footer. Cap top row height to enforce this.
- **Overflow guard:** auto-reduce `CARD_GAP` if total content height exceeds available space (minimum 3 pt). Keep this logic — content-heavy lessons need it.
- **Concept card descriptions:** 3 lines max. Content beyond 3 lines won't fit.
- **Checklist items:** keep concise — 1–2 wrapped lines at 7.5 pt per item.
- **Step text:** keep concise — steps wrapping to 3+ lines push the top row very tall, starving the bottom row.
- **Checkbox alignment:** always vertically centre checkbox on the first line baseline of its item, not a fixed offset from the box top.
- **Vocab column break:** always measured dynamically from the widest term. Never hardcode the indent.
- **Title length:** the card header title at 20 pt bold must fit in ~400 pt. Shorten from the official lesson title where needed and update `site-config.js` to match.
- **Bottom-left section:** varies by lesson. Label, bar color, and content type are all per-lesson decisions. Define a `draw_bot_left()` function per lesson rather than hardcoding ruled lines.
- **Image embedding:** use `preserveAspectRatio=True, mask='auto'`. Always compute draw dimensions maintaining aspect ratio — never stretch.