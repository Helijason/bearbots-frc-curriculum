"""
BearBots FRC — Program Execution Flow Reference  v4

Key architectural change: ALL boxes are measured and positioned FIRST,
then arrows are drawn between known coordinates. No dynamic positioning
during drawing — this eliminates all overlap.

Page plan:
  P1: Startup part 1 (Main → configureAutonomous)           11x17 landscape
  P2: Startup part 2 (DS mode) + Loop part 1 (Notifier → modePeriodic)  11x17 landscape
  P3: Loop part 2 (robotPeriodic → CommandScheduler 4 steps → watchdog)  11x17 landscape
  P4: Detail (call chains inside periodic and execute)       11x17 landscape
  P5-P14: File cards (one per page)                         Letter portrait
"""

from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

for name, path in [
    ('DV',  r'C:\Windows\Fonts\arial.ttf'),
    ('DVB', r'C:\Windows\Fonts\arialbd.ttf'),
    ('DVI', r'C:\Windows\Fonts\ariali.ttf'),
    ('DVM', r'C:\Windows\Fonts\consola.ttf'),
    ('DVMB',r'C:\Windows\Fonts\consolab.ttf'),
]:
    pdfmetrics.registerFont(TTFont(name, path))

# ── colours ────────────────────────────────────────────────────────────────
def rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))

TEAL    = rgb('#2D6B6B'); TEAL_LT  = rgb('#D8EEEE')
PURPLE  = rgb('#6B4A9B'); PURPLE_LT= rgb('#E4DCEF')
ORANGE  = rgb('#B8762A'); ORANGE_LT= rgb('#F5E8D2')
GREEN   = rgb('#2D7A4F'); GREEN_LT = rgb('#D2EBDC')
RED     = rgb('#A32D2D'); RED_LT   = rgb('#F0D4D4')
GRAY_BG = rgb('#EEEEEE'); GRAY_BD  = rgb('#AAAAAA')
INK     = rgb('#1A1A1A'); INK_MED  = rgb('#555555'); INK_MUT = rgb('#888888')
WHITE   = (1,1,1)
DARK_GRAY   = (0.35, 0.35, 0.35)
MID_GRAY    = (0.50, 0.50, 0.50)
LIGHT_GRAY  = (0.70, 0.70, 0.70)
PALE_GRAY   = (0.82, 0.82, 0.82)

def sf(c,col): c.setFillColorRGB(*col)
def ss(c,col): c.setStrokeColorRGB(*col)
def blend(c1, c2, t):
    """Blend c1 toward c2 by t. t=0 keeps c1, t=1 becomes c2."""
    return tuple(c1[i] * (1 - t) + c2[i] * t for i in range(3))

# ── page geometry ─────────────────────────────────────────────────────────
TW, TH   = 11*72, 17*72       # tabloid: 792 x 1224
TLW, TLH = TH, TW             # landscape: 1224 x 792
PW, PH   = letter              # portrait: 612 x 792

ML, MR   = 38, 38
MT, MB   = 28, 28
HDR_H    = 50
FOOTER_H = 22
SGAP     = 8

# flowchart column positions (landscape, origin bottom-left as usual in PDF)
# We work in top-down coords, converting at draw time.
S_X  = ML + 4;    S_W  = 200   # spine
B1_X = S_X + S_W + 28; B1_W = 280  # branch level 1
B2_X = B1_X + B1_W + 28; B2_W = 220  # branch level 2
B3_X = B2_X + B2_W + 24; B3_W = 200  # branch level 3
B4_X = B3_X + B3_W + 24; B4_W = 165  # branch level 4
# B4_X + B4_W = 38+4+200+32+230+28+220+24+200+24+165 = 1165 < 1186 (right content edge) ✓

MONO_SZ  = 7.5
LINE_H   = 11.0
BOX_PAD  = 8    # top and bottom padding inside boxes
BOX_L    = 8    # left padding inside boxes
V_GROUP_GAP = 10  # vertical gap between groups (spine box + its branches)
V_INNER_GAP = 10  # gap between stacked branch boxes in same column

TOTAL_PAGES = '?'

# ── text utilities ─────────────────────────────────────────────────────────
def sw(c, txt, font, size):
    return c.stringWidth(txt, font, size)

def wrap_lines(c, txt, font, size, maxw):
    if not txt.strip():
        return ['']
    if sw(c, txt, font, size) <= maxw:
        return [txt]
    words = txt.split(' ')
    lines, cur = [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if sw(c, t, font, size) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            # hard break
            while sw(c, w, font, size) > maxw:
                for i in range(len(w), 0, -1):
                    if sw(c, w[:i], font, size) <= maxw:
                        lines.append(w[:i]); w = w[i:]; break
            cur = w
    if cur:
        lines.append(cur)
    return lines or ['']

def measure_box(c, lines, box_w, bold_first=False):
    """Return height of a box given text lines."""
    inner_w = box_w - BOX_L * 2
    h = BOX_PAD * 2
    for i, line in enumerate(lines):
        font = 'DVMB' if (bold_first and i == 0) else 'DVM'
        h += len(wrap_lines(c, line, font, MONO_SZ, inner_w)) * LINE_H
    return h

def draw_hatch(c, x, bot, w, h, r, col, spacing=10, lw=0.25):
    """Diagonal hatch fill clipped to a rounded-rect region."""
    c.saveState()
    p = c.beginPath()
    p.roundRect(x, bot, w, h, r)
    c.clipPath(p, stroke=0, fill=0)

    ss(c, col)
    c.setLineWidth(lw)

    diag = w + h
    i = -h
    while i < diag:
        c.line(x + i, bot, x + i + h, bot + h)
        i += spacing

    c.restoreState()

def draw_box_at(c, x, top_y, w, lines, bg, border, bold_first=False, r=3, lw=0.9,
                framework=False, hatch_col=None, hatch_spacing=10, hatch_lw=0.25,
                hatch_blend=0.65):
    """Draw box with top-left at (x, top_y). Returns bottom_y.
    framework=True draws a dashed border + diagonal hatch overlay to flag
    boxes representing automatic framework calls (not team-written code)."""
    h = measure_box(c, lines, w, bold_first)
    bot = top_y - h
    sf(c, bg); ss(c, border); c.setLineWidth(lw)
    if framework:
        c.setDash([3, 2])
    c.roundRect(x, bot, w, h, r, fill=1, stroke=1)
    c.setDash([])
    if framework:
        base_hatch_col = hatch_col or border
        final_hatch_col = blend(base_hatch_col, WHITE, hatch_blend)

        draw_hatch(
            c, x, bot, w, h, r,
            final_hatch_col,
            spacing=hatch_spacing,
            lw=hatch_lw
    )
    ty = top_y - BOX_PAD - LINE_H + 2.5
    inner_w = w - BOX_L * 2
    for i, line in enumerate(lines):
        font = 'DVMB' if (bold_first and i == 0) else 'DVM'
        for wl in wrap_lines(c, line, font, MONO_SZ, inner_w):
            sf(c, WHITE if bg == INK else INK)
            c.setFont(font, MONO_SZ)
            c.drawString(x + BOX_L, ty, wl)
            ty -= LINE_H
    return bot

def draw_note_at(c, x, top_y, w, text, col):
    """Small italic note. Returns bottom_y."""
    inner_w = w - BOX_L * 2
    lines = wrap_lines(c, text, 'DVI', 7, inner_w)
    h = len(lines) * 9.5 + BOX_PAD * 1.5
    bot = top_y - h
    sf(c, rgb('#F8F8F8')); ss(c, col); c.setLineWidth(0.5)
    c.roundRect(x, bot, w, h, 2, fill=1, stroke=1)
    ty = top_y - BOX_PAD - 7
    for line in lines:
        sf(c, col); c.setFont('DVI', 7)
        c.drawString(x + BOX_L, ty, line)
        ty -= 9.5
    return bot

# ── arrow drawing ─────────────────────────────────────────────────────────
def ah_down(c, x, y, col, sz=5):
    sf(c, col); c.setLineWidth(0)
    p = c.beginPath()
    p.moveTo(x-sz/2, y+sz); p.lineTo(x+sz/2, y+sz); p.lineTo(x, y)
    p.close(); c.drawPath(p, fill=1, stroke=0)

def ah_up(c, x, y, col, sz=5):
    sf(c, col); c.setLineWidth(0)
    p = c.beginPath()
    p.moveTo(x - sz/2, y - sz); p.lineTo(x + sz/2, y - sz); p.lineTo(x, y)
    p.close(); c.drawPath(p, fill=1, stroke=0)

def ah_right(c, x, y, col, sz=5):
    sf(c, col); c.setLineWidth(0)
    p = c.beginPath()
    p.moveTo(x-sz, y-sz/2); p.lineTo(x-sz, y+sz/2); p.lineTo(x, y)
    p.close(); c.drawPath(p, fill=1, stroke=0)

def ah_left_open(c, x, y, col, sz=4):
    """Open (hollow) leftward arrowhead for return arrows."""
    ss(c, col); sf(c, WHITE); c.setLineWidth(0.7)
    p = c.beginPath()
    p.moveTo(x+sz, y-sz/2); p.lineTo(x+sz, y+sz/2); p.lineTo(x, y)
    p.close(); c.drawPath(p, fill=1, stroke=1)

def spine_down_arrow(c, spine_cx, y_from, y_to, col=INK):
    """Solid down arrow on spine centreline."""
    ss(c, col); c.setLineWidth(1.3); c.setDash([])
    c.line(spine_cx, y_from, spine_cx, y_to + 5)
    ah_down(c, spine_cx, y_to, col)

def call_arrow(c, from_x, from_y, to_x, to_y, border_col):
    """
    Solid horizontal call arrow.
    Leaves from_x at from_y (right edge of spine box at that y).
    Arrives at to_x (left edge of branch box) at to_y.
    If from_y != to_y, jogs vertically at to_x side.
    """
    ss(c, border_col); c.setLineWidth(1.1); c.setDash([])
    jog_x = to_x - 4
    c.line(from_x, from_y, jog_x, from_y)
    if abs(from_y - to_y) > 1:
        c.line(jog_x, from_y, jog_x, to_y)
    ah_right(c, to_x, to_y, border_col)
    # label
    label_x = from_x + 3
    sf(c, border_col); c.setFont('Helvetica-Oblique', 5.5)
    c.drawString(label_x, from_y + 2, 'calls →')

def return_arrow(c, from_x, from_y, to_x, to_y, col=INK_MUT):
    """
    Dashed return arrow from branch back to calling spine box.
    from_x, from_y = bottom-left of branch box
    to_x, to_y    = right edge of spine box at its bottom (the caller's bottom)
    Route: drop vertically from from_y to to_y on from_x side,
           then go horizontally left to to_x.
    """
    ss(c, col); c.setLineWidth(0.8); c.setDash([4, 3])
    if abs(from_y - to_y) > 2:
        # drop vertically on branch side to match spine bottom y
        c.line(from_x, from_y, from_x - 6, from_y)
        c.line(from_x - 6, from_y, from_x - 6, to_y)
        c.line(from_x - 6, to_y, to_x + 4, to_y)
    else:
        c.line(from_x, to_y, to_x + 4, to_y)
    c.setDash([])
    ah_left_open(c, to_x, to_y, col)
    sf(c, col); c.setFont('Helvetica-Oblique', 5.5)
    lbl_x = from_x - 8 if abs(from_y - to_y) > 2 else from_x - 2
    c.drawRightString(lbl_x, to_y + 2, '← returns')

def connect_down(c, x, y_from, y_to, col, lw=0.9):
    """Vertical connecting line between stacked branch boxes."""
    ss(c, col); c.setLineWidth(lw); c.setDash([])
    c.line(x, y_from, x, y_to + 4)
    ah_down(c, x, y_to, col, sz=4)

# ── page frame ─────────────────────────────────────────────────────────────
def draw_header(c, page_num, pw, ph, subtitle=''):
    x = ML; y = ph - MT - HDR_H; w = pw - ML - MR
    sf(c, TEAL); c.setLineWidth(0)
    c.roundRect(x, y, w, HDR_H, 5, fill=1, stroke=0)
    sf(c, rgb('#A8D4D4')); c.setFont('Helvetica-Bold', 7)
    c.drawString(x+10, y+HDR_H-12, 'BEARBOTS TEAM 6964  —  FRC PROGRAMMING CURRICULUM')
    sf(c, WHITE); c.setFont('Helvetica-Bold', 20)
    c.drawString(x+10, y+HDR_H-34, 'Program Execution Flow Reference')
    if subtitle:
        sf(c, rgb('#C8E8E8')); c.setFont('Helvetica-Bold', 7.5)
        c.drawString(x+10, y+HDR_H-46, subtitle)
    sf(c, rgb('#A8D4D4')); c.setFont('Helvetica-Bold', 7.5)
    c.drawRightString(x+w-12, y+HDR_H-14, 'Java  |  WPILib 2026  |  AdvantageKit  |  XRP')
    sf(c, rgb('#BBDDDD')); c.setFont('Helvetica-Oblique', 7)
    c.drawRightString(x+w-12, y+HDR_H-25, 'Keep this. Add it to your binder.')
    c.drawRightString(x+w-12, y+HDR_H-36, f'Page {page_num} of {TOTAL_PAGES}')

def draw_footer(c, pw, ph, right_txt=''):
    x = ML; w = pw - ML - MR
    sf(c, TEAL); c.setLineWidth(0)
    c.roundRect(x, MB, w, FOOTER_H, 4, fill=1, stroke=0)
    my = MB + FOOTER_H/2 - 3
    sf(c, WHITE); c.setFont('Helvetica-Bold', 7)
    c.drawString(x+8, my, 'BearBots FRC — Program Execution Flow Reference')
    c.setFont('Helvetica', 7)
    c.drawRightString(x+w-8, my, right_txt or 'Main → Robot → CommandScheduler → Subsystems → IO → Hardware')

def draw_legend(c, pw, ph):
    items = [
        (INK,    WHITE, 'Entry / JVM'),
        (TEAL,   WHITE, 'Every 20ms loop'),
        (ORANGE, WHITE, 'Once per mode change'),
        (PURPLE, WHITE, 'CommandScheduler'),
        (GREEN,  WHITE, 'AdvantageKit logging'),
        (RED,    WHITE, 'Hardware / IO layer'),
        (GRAY_BD,INK,   'Config / constants'),
    ]
    lw = pw - ML - MR
    ly = ph - MT - HDR_H - SGAP
    sf(c, GRAY_BG); ss(c, GRAY_BD); c.setLineWidth(0.4)
    c.roundRect(ML, ly-14, lw, 15, 2, fill=1, stroke=1)
    iw = lw / (len(items) + 1)
    for i,(bg,fg,label) in enumerate(items):
        ix = ML + i*iw + 4
        sf(c,bg); ss(c,GRAY_BD); c.setLineWidth(0.3)
        c.roundRect(ix, ly-11, 9, 9, 1, fill=1, stroke=1)
        sf(c,INK); c.setFont('Helvetica', 6.5)
        c.drawString(ix+12, ly-9, label)
    # framework-managed hatch swatch (final slot)
    fx = ML + len(items)*iw + 4
    sf(c, WHITE); ss(c, INK_MUT); c.setLineWidth(0.3); c.setDash([2,1.5])
    c.roundRect(fx, ly-11, 9, 9, 1, fill=1, stroke=1)
    c.setDash([])
    draw_hatch(c, fx, ly-11, 9, 9, 1, INK_MUT, spacing=4, lw=0.2)
    sf(c,INK); c.setFont('Helvetica', 6.5)
    c.drawString(fx+12, ly-9, 'Framework-managed')
    return ly - 14 - 6   # y below legend


def draw_legend_portrait(c, pw, ph):
    """Legend strip for portrait pages."""
    items = [
        (INK,    WHITE, 'Entry / JVM'),
        (TEAL,   WHITE, 'Every 20ms loop'),
        (ORANGE, WHITE, 'Once per mode change'),
        (PURPLE, WHITE, 'CommandScheduler'),
        (GREEN,  WHITE, 'AdvantageKit'),
        (RED,    WHITE, 'Hardware / IO'),
        (GRAY_BD,INK,   'Config / constants'),
    ]
    lw = pw - ML - MR
    ly = ph - MT - HDR_H - SGAP
    sf(c, GRAY_BG); ss(c, GRAY_BD); c.setLineWidth(0.4)
    c.roundRect(ML, ly-13, lw, 14, 2, fill=1, stroke=1)
    all_items = items + [('__hatch__', None, 'Framework-managed')]
    c.setFont('Helvetica', 6)
    gap = 14  # space after each item before next swatch
    widths = [8 + 2 + c.stringWidth(label, 'Helvetica', 6) + gap for _,_,label in all_items]
    total_w = sum(widths)
    scale = lw / total_w if total_w > lw else 1.0
    x = ML
    for i,(bg,fg,label) in enumerate(items):
        ix = x + 4*scale
        sf(c,bg); ss(c,GRAY_BD); c.setLineWidth(0.3)
        c.roundRect(ix, ly-10, 8, 8, 1, fill=1, stroke=1)
        sf(c,INK); c.setFont('Helvetica', 6)
        c.drawString(ix+10, ly-8.5, label)
        x += widths[i]*scale
    # framework-managed hatch swatch (final slot)
    fx = x + 4*scale
    sf(c, WHITE); ss(c, INK_MUT); c.setLineWidth(0.3); c.setDash([2,1.5])
    c.roundRect(fx, ly-10, 8, 8, 1, fill=1, stroke=1)
    c.setDash([])
    draw_hatch(c, fx, ly-10, 8, 8, 1, INK_MUT, spacing=4, lw=0.2)
    sf(c,INK); c.setFont('Helvetica', 6)
    c.drawString(fx+10, ly-8.5, 'Framework-managed')
    return ly - 13 - 5

def port_top(ph):
    """Top of content area on portrait page (below header + legend)."""
    return ph - MT - HDR_H - SGAP - 13 - 5 - 4

# content_top for flowchart pages
def fc_top(ph):
    return ph - MT - HDR_H - SGAP - 14 - 6   # below legend

def fc_bottom():
    return MB + FOOTER_H + SGAP

# ══════════════════════════════════════════════════════════════════════════
# GROUP-BASED LAYOUT ENGINE
# A "group" = one spine box + its branch columns
# Groups are pre-measured and laid out top-to-bottom.
# Arrows are drawn after all box positions are known.
# ══════════════════════════════════════════════════════════════════════════

class Group:
    """
    Stores all position data for one spine-box + branch columns.
    """
    def __init__(self, spine_top, spine_lines, spine_bg, spine_border,
                 bold_first=False,
                 b1=None, b2=None, b3=None, b4=None,
                 note=None, note_col=None, framework=False):
        self.spine_top    = spine_top
        self.spine_lines  = spine_lines
        self.spine_bg     = spine_bg
        self.spine_border = spine_border
        self.bold_first   = bold_first
        self.framework    = framework
        self.b1 = b1; self.b2 = b2; self.b3 = b3; self.b4 = b4
        self.note = note; self.note_col = note_col
        # computed after layout()
        self.spine_bot = None
        self.spine_mid = None
        self.b1_top = self.b1_bot = None
        self.b2_top = self.b2_bot = None
        self.b3_top = self.b3_bot = None
        self.b4_top = self.b4_bot = None
        self.note_bot = None
        self.group_bot = None   # lowest y of entire group

def layout_groups(c, groups, start_y):
    """
    Pre-compute all box positions for a list of groups.
    start_y = top y where first group begins.
    Returns groups with all positions filled in.
    """
    cy = start_y
    for g in groups:
        g.spine_top = cy
        sh = measure_box(c, g.spine_lines, S_W, g.bold_first)
        g.spine_bot = cy - sh
        g.spine_mid = cy - sh / 2

        # branch columns: each starts at same top as spine box
        lowest = g.spine_bot

        if g.b1:
            blines, bbg, bborder = g.b1
            bh1 = measure_box(c, blines, B1_W)
            g.b1_top = cy
            g.b1_bot = cy - bh1
            lowest = min(lowest, g.b1_bot)

            if g.b2:
                blines2, bbg2, bborder2 = g.b2
                bh2 = measure_box(c, blines2, B2_W)
                g.b2_top = cy
                g.b2_bot = cy - bh2
                lowest = min(lowest, g.b2_bot)

                if g.b3:
                    blines3, bbg3, bborder3 = g.b3
                    bh3 = measure_box(c, blines3, B3_W)
                    g.b3_top = cy
                    g.b3_bot = cy - bh3
                    lowest = min(lowest, g.b3_bot)

                    if g.b4:
                        blines4, bbg4, bborder4 = g.b4
                        bh4 = measure_box(c, blines4, B4_W)
                        g.b4_top = cy
                        g.b4_bot = cy - bh4
                        lowest = min(lowest, g.b4_bot)

        if g.note and g.b1:
            ncol = g.note_col or INK_MUT
            # measure note
            inner_w = B1_W - BOX_L * 2
            nlines = wrap_lines(c, g.note, 'DVI', 7, inner_w)
            nh = len(nlines) * 9.5 + BOX_PAD * 1.5
            g.note_top = lowest - 4
            g.note_bot = g.note_top - nh
            lowest = g.note_bot

        g.group_bot = lowest
        cy = g.group_bot - V_GROUP_GAP

    return groups

def draw_groups(c, groups):
    """Draw all boxes and arrows for a list of pre-laid-out groups."""
    S_CX = S_X + S_W / 2

    for i, g in enumerate(groups):
        # ── spine box ──
        draw_box_at(c, S_X, g.spine_top, S_W,
                    g.spine_lines, g.spine_bg, g.spine_border,
                    bold_first=g.bold_first,
                    framework=getattr(g, 'framework', False),
                    hatch_col=getattr(g, 'hatch_col', None),
                    hatch_spacing=getattr(g, 'hatch_spacing', 10),
                    hatch_lw=getattr(g, 'hatch_lw', 0.25),
                    hatch_blend=getattr(g, 'hatch_blend', 0.65),
        )

        # ── branch boxes ──
        if g.b1:
            blines, bbg, bborder = g.b1
            draw_box_at(c, B1_X, g.b1_top, B1_W, blines, bbg, bborder)

            # call arrow: spine right → b1 left, at spine_top - BOX_PAD
            call_y = g.spine_top - BOX_PAD - LINE_H / 2
            b1_arr_y = g.b1_top - BOX_PAD - LINE_H / 2
            call_arrow(c, S_X + S_W, call_y, B1_X, b1_arr_y, bborder)

            # return arrow: b1 left → spine right, below both boxes
            ret_y_from = g.b1_bot + 5
            ret_y_to   = g.spine_bot + 5
            return_arrow(c, B1_X, ret_y_from, S_X + S_W, ret_y_to)

        if g.b2 and g.b1:
            blines2, bbg2, bborder2 = g.b2
            draw_box_at(c, B2_X, g.b2_top, B2_W, blines2, bbg2, bborder2)
            _, bborder = g.b1[0], g.b1[2]
            call_y2 = g.b1_top - BOX_PAD - LINE_H / 2
            b2_arr_y = g.b2_top - BOX_PAD - LINE_H / 2
            call_arrow(c, B1_X + B1_W, call_y2, B2_X, b2_arr_y, bborder2)
            return_arrow(c, B2_X, g.b2_bot + 4, B1_X + B1_W, g.b1_bot + 4, INK_MUT)

        if g.b3 and g.b2:
            blines3, bbg3, bborder3 = g.b3
            draw_box_at(c, B3_X, g.b3_top, B3_W, blines3, bbg3, bborder3)
            call_y3 = g.b2_top - BOX_PAD - LINE_H / 2
            b3_arr_y = g.b3_top - BOX_PAD - LINE_H / 2
            call_arrow(c, B2_X + B2_W, call_y3, B3_X, b3_arr_y, bborder3)
            return_arrow(c, B3_X, g.b3_bot + 4, B2_X + B2_W, g.b2_bot + 4, INK_MUT)

        if g.b4 and g.b3:
            blines4, bbg4, bborder4 = g.b4
            draw_box_at(c, B4_X, g.b4_top, B4_W, blines4, bbg4, bborder4)
            call_y4 = g.b3_top - BOX_PAD - LINE_H / 2
            b4_arr_y = g.b4_top - BOX_PAD - LINE_H / 2
            call_arrow(c, B3_X + B3_W, call_y4, B4_X, b4_arr_y, bborder4)
            return_arrow(c, B4_X, g.b4_bot + 4, B3_X + B3_W, g.b3_bot + 4, INK_MUT)

        if g.note and g.b1:
            ncol = g.note_col or INK_MUT
            draw_note_at(c, B1_X, g.note_top, B1_W, g.note, ncol)

        # ── down arrow to next group ──
        if i < len(groups) - 1:
            next_g = groups[i + 1]
            if next_g.spine_top is not None:
                spine_down_arrow(c, S_CX, g.spine_bot, next_g.spine_top,
                                 col=g.spine_border)


STEP_BADGE_NUMS = [u'\u2460', u'\u2461', u'\u2462', u'\u2463']
STEP_BADGE_COLS_MAP = [TEAL, PURPLE, PURPLE, PURPLE]

def draw_sequential_steps(c, spine_group, step_groups, first_step_num=1):
    """
    Draw CommandScheduler steps as a vertical sequence in B1 column.
    Each step gets a coloured circle badge on its left side with the step number.
    step_groups: [(lines, bg, border), ...]
    first_step_num: 1-based index of first step (1 or 4)
    """
    cy = spine_group.spine_top
    spine_rx = S_X + S_W
    BADGE_R = 8
    BADGE_GAP = BADGE_R * 2 + 6   # total width taken by badge
    box_x = B1_X + BADGE_GAP
    box_w = B1_W - BADGE_GAP

    prev_bot = None
    for i, (lines, bg, border) in enumerate(step_groups):
        step_idx = first_step_num - 1 + i   # 0-based
        badge_num = str(step_idx + 1)
        badge_col = STEP_BADGE_COLS_MAP[step_idx] if step_idx < len(STEP_BADGE_COLS_MAP) else PURPLE

        if i == 0:
            top = cy
            call_arrow(c, spine_rx, cy - BOX_PAD - LINE_H / 2, box_x,
                       top - BOX_PAD - LINE_H / 2, border)
        else:
            top = prev_bot - V_INNER_GAP
            connect_down(c, box_x + box_w / 2, prev_bot, top, border)

        bot = draw_box_at(c, box_x, top, box_w, lines, bg, border)

        # Badge circle on left side, centred vertically on this box
        mid_y = (top + bot) / 2
        sf(c, badge_col); c.setLineWidth(0)
        c.circle(B1_X + BADGE_R + 2, mid_y, BADGE_R, fill=1, stroke=0)
        sf(c, WHITE); c.setFont('Helvetica-Bold', 9)
        tw = c.stringWidth(badge_num, 'Helvetica-Bold', 9)
        c.drawString(B1_X + BADGE_R + 2 - tw/2, mid_y - 3.5, badge_num)

        prev_bot = bot

    # return arrow from last step back to spine bottom
    return_arrow(c, box_x, prev_bot + 4, spine_rx, spine_group.spine_bot + 4, INK_MUT)
    return prev_bot



def make_group(spine_lines, spine_bg, spine_border, bold_first=False,
               b1=None, b2=None, b3=None, b4=None, note=None, note_col=None,
               framework=False, hatch_col=None, hatch_spacing=10, hatch_lw=0.25,
               hatch_blend=0.65):
    """Factory so we don't repeat the Group.__new__ boilerplate."""
    g = Group.__new__(Group)
    g.spine_top = g.spine_bot = g.spine_mid = None
    g.spine_lines = spine_lines
    g.spine_bg = spine_bg; g.spine_border = spine_border
    g.bold_first = bold_first
    g.framework = framework
    g.b1 = b1; g.b2 = b2; g.b3 = b3; g.b4 = b4
    g.note = note; g.note_col = note_col
    g.hatch_col = hatch_col
    g.hatch_spacing = hatch_spacing
    g.hatch_lw = hatch_lw
    g.hatch_blend = hatch_blend
    g.b1_top = g.b1_bot = None
    g.b2_top = g.b2_bot = None
    g.b3_top = g.b3_bot = None
    g.b4_top = g.b4_bot = None
    g.note_top = g.note_bot = None
    g.group_bot = None
    return g


# ── All startup groups (shared data) ────────────────────────────────────────
def startup_groups_p1():
    return [
        make_group(['Main.java', 'main()'], INK, INK, bold_first=True),
        make_group(['RobotBase.startRobot(Robot::new)',
                    '// framework creates Robot instance',
                    '// enters TimedRobot 20ms Notifier loop'],
                   GRAY_BG, GRAY_BD),
        make_group(['Robot()  constructor',
                    '// runs once at power-on'],
                   TEAL_LT, TEAL, bold_first=True,
                   b1=(['Logger.recordMetadata("ProjectName","BearBotsXRP")',
                         'Logger.addDataReceiver(new WPILOGWriter())',
                         '// writes .wpilog file to USB drive',
                         'Logger.addDataReceiver(new NT4Publisher())',
                         '// streams live to AdvantageScope via NT4',
                         'Logger.start()'],
                        GREEN_LT, GREEN),
                   note='AKit begins recording all inputs from this point forward.',
                   note_col=GREEN),
        make_group(['new RobotContainer()',
                    '// instantiates all subsystems'],
                   ORANGE_LT, ORANGE, bold_first=True,
                   b1=(['switch (Constants.currentMode) {',
                         '  case REAL:',
                         '    drive = new Drive(new DriveIOXRP())',
                         '    arm   = new Arm(new ArmIOXRP())',
                         '  case SIM:',
                         '    drive = new Drive(new DriveIOSim())',
                         '    arm   = new Arm(new ArmIOSim())',
                         '  case REPLAY:  // no hardware',
                         '    drive = new Drive(new DriveIO() {})',
                         '    arm   = new Arm(new ArmIO() {})',
                         '}'],
                        ORANGE_LT, ORANGE),
                   note='IO impl chosen once here. Subsystems never know which hardware they get.',
                   note_col=ORANGE),
        make_group(['configureButtonBindings()',
                    '// registers triggers — one time only'],
                   ORANGE_LT, ORANGE,
                   b1=(['// Registers triggers with CommandScheduler',
                         '// Does NOT call commands yet',
                         '// Scheduler polls these every loop at step 2',
                         'controller.a().onTrue(',
                         '  arm.setAngleCommand(kHighAngleDeg))',
                         'controller.b().onTrue(',
                         '  arm.setAngleCommand(kLowAngleDeg))',
                         'controller.x().onTrue(arm.runOnce(arm::stow))',
                         'drive.setDefaultCommand(',
                         '  drive.defaultDriveCommand(controller))'],
                        ORANGE_LT, ORANGE),
                   note='Registration only. Scheduler checks button state every loop at step 2.',
                   note_col=ORANGE),
    ]

def startup_groups_p2():
    return [
        make_group(['configureAutonomous()',
                    '// registers auto modes — one time only'],
                   ORANGE_LT, ORANGE,
                   b1=(['autoChooser.addOption("Drive Forward", driveForwardCmd)',
                         'autoChooser.addOption("Spin in Place", spinCmd)',
                         'SmartDashboard.putData("Auto Chooser", autoChooser)',
                         '// Driver selects before match via dashboard',
                         '// Retrieved in Robot.autonomousInit()'],
                        ORANGE_LT, ORANGE)),
        make_group(['DS mode state machine',
                    '// WPILib checks DS state each loop',
                    '// init() fires only when mode changes'],
                   ORANGE_LT, ORANGE, framework=True,
                   b1=(['disabledInit()  // on → disabled',
                         '  // runs only the code you write here (e.g. stop motors)',
                         'autonomousInit()  // on → autonomous',
                         '  autonomousCommand =',
                         '    robotContainer.getAutonomousCommand()',
                         '  autonomousCommand.schedule()',
                         'teleopInit()  // on → teleop',
                         '  if (autonomousCommand != null)',
                         '    autonomousCommand.cancel()'],
                        ORANGE_LT, ORANGE),
                   note='Each init() fires ONCE per transition. Most loops nothing fires here.',
                   note_col=ORANGE),
    ]


def loop_groups_p3():
    return [
        make_group(['Notifier fires  →  loopFunc()',
                    '// every 20ms — 50× per second',
                    '// START of one loop cycle'],
                    INK, INK,
                    bold_first=True,
                    framework=True,
                    hatch_col=DARK_GRAY,
                    hatch_spacing=8,
                    hatch_lw=0.45,
                    hatch_blend=0.0),
        make_group(['loopFunc(): DS mode changed?',
                    '// most loops: no change → skip'],
                   ORANGE_LT, ORANGE, framework=True,
                   b1=(['// IF mode changed — fires ONCE per transition:',
                         'disabledInit()   // runs only the code you write here (e.g. stop motors)',
                         'autonomousInit() // schedule auto command',
                         'teleopInit()     // cancel auto command',
                         '// Button triggers from configureButtonBindings()',
                         '// are polled by CommandScheduler at step 2 below'],
                        ORANGE_LT, ORANGE),
                   note='Most loops nothing fires here. Init methods are one-shot.',
                   note_col=ORANGE),
        make_group(['modePeriodic()  ← current mode only',
                    '// exactly one fires per loop'],
                   ORANGE_LT, ORANGE,
                   b1=(['disabledPeriodic()',
                         '  // update auto chooser from dashboard',
                         'autonomousPeriodic()',
                         '  // usually empty in command-based code',
                         '  // framework still calls this every teleop loop',
                         'teleopPeriodic()',
                         '  // usually empty in command-based code',
                         '  // framework still calls this every auto loop'],
                        ORANGE_LT, ORANGE),
                   note='CommandScheduler runs because Robot.robotPeriodic() calls CommandScheduler.getInstance().run().',
                   note_col=ORANGE),
        make_group(['Robot.robotPeriodic()',
                    '// runs EVERY loop in ALL modes'],
                   TEAL_LT, TEAL, bold_first=True),
        make_group(['Logger.periodicBeforeUser()',
                    '// AKit: lock this loop input snapshot'],
                   GREEN_LT, GREEN, framework=True),
        make_group(['CommandScheduler.getInstance().run()',
                    '// called from robotPeriodic() — required',
                    '// 4 steps shown alongside →'],
                   PURPLE_LT, PURPLE, bold_first=True),
    ]

def loop_groups_p4():
    return [
        make_group(['Logger.periodicAfterUser()',
                    '// AKit: write all captured data this loop',
                    '// flush log frame to WPILog file + NT4'],
                   GREEN_LT, GREEN, framework=True),
        make_group(['WPILib post-loop tasks',
                    'SmartDashboard.updateValues()',
                    'LiveWindow.updateValues()',
                    'NetworkTables flush',
                    '// framework-managed — no user code needed'],
                   GRAY_BG, GRAY_BD),
        make_group(['simulationPeriodic()  [sim only]',
                    '// updates WPILib physics simulation',
                    '// skipped entirely on real hardware'],
                   GRAY_BG, GRAY_BD),
        make_group(['Watchdog: check loop duration',
                    '// if loop took > 20ms: print warning',
                    '// "Loop time of 0.02s overrun"'],
                   GRAY_BG, GRAY_BD),
    ]


# ══════════════════════════════════════════════════════════════════════════
# DRAW PAGE HELPERS
# ══════════════════════════════════════════════════════════════════════════

BADGE_COLS = {
    'once':      (ORANGE,  WHITE),
    '50 Hz':     (TEAL,    WHITE),
    'output':    (RED,     WHITE),
    'AKit':      (GREEN,   WHITE),
    'getter':    (GRAY_BD, INK),
    'static':    (GRAY_BD, INK),
    'JVM entry': (INK,     WHITE),
    'contract':  (PURPLE,  WHITE),
    'reads HW':  (RED,     WHITE),
    'writes HW': (RED,     WHITE),
    'interface': (PURPLE,  WHITE),
}

P_CW = PW - ML - MR
CARD_BAR_H = 22
CARD_LINE_H = 11.5
CARD_MONO_SZ = 7.5
CARD_PAD_L = 10
CARD_PAD_B = 10
METH_GAP = 10

def card_method_height(c, m):
    inner_w = P_CW - CARD_PAD_L * 2 - 14
    h = CARD_LINE_H + 4  # method name line + gap
    for line in m.get('calls', []):
        h += len(wrap_lines(c, line, 'DVM', CARD_MONO_SZ, inner_w)) * CARD_LINE_H
    h += METH_GAP
    return h

def draw_one_card(c, card, page_num):
    c.setPageSize((PW, PH))
    draw_header(c, page_num, PW, PH, subtitle=f'FILE CARDS — {card["idx"]} of {card["total"]}')
    draw_footer(c, PW, PH)

    top_y = fc_top(PH) - 6
    bot_limit = fc_bottom()

    # Card outer box — full remaining height
    card_h = top_y - bot_limit
    bg = card['body_col']; border = card['bar_col']
    sf(c, bg); ss(c, GRAY_BD); c.setLineWidth(0.75)
    c.roundRect(ML, bot_limit, P_CW, card_h, 4, fill=1, stroke=1)

    # Bar
    sf(c, border); c.setLineWidth(0)
    c.roundRect(ML, top_y - CARD_BAR_H, P_CW, CARD_BAR_H + 4, 4, fill=1, stroke=0)
    c.rect(ML, top_y - CARD_BAR_H, P_CW, 4, fill=1, stroke=0)
    bar_mid = top_y - CARD_BAR_H / 2 - 3

    # Filename
    sf(c, WHITE); c.setFont('DVMB', 10)
    c.drawString(ML + CARD_PAD_L, bar_mid, card['fname'])

    # File badge
    lbl = card['badge']
    bcol, bfg = BADGE_COLS.get(lbl, (GRAY_BD, INK))
    bw = c.stringWidth(lbl, 'Helvetica-Bold', 7) + 12; bh = 14
    bx = ML + P_CW - CARD_PAD_L - bw
    sf(c, bcol); ss(c, WHITE); c.setLineWidth(0.5)
    c.roundRect(bx, bar_mid - 2, bw, bh, 2, fill=1, stroke=1)
    sf(c, bfg); c.setFont('Helvetica-Bold', 7)
    c.drawString(bx + 6, bar_mid + 1.5, lbl)

    # Path
    path_y = top_y - CARD_BAR_H - 12
    sf(c, INK_MUT); c.setFont('DVM', 7)
    c.drawRightString(ML + P_CW - CARD_PAD_L, path_y, card['fpath'])

    cur_y = path_y - 6

    inner_w = P_CW - CARD_PAD_L * 2 - 14
    for m in card['methods']:
        # separator rule
        ss(c, GRAY_BD); c.setLineWidth(0.4)
        c.line(ML + CARD_PAD_L, cur_y, ML + P_CW - CARD_PAD_L, cur_y)
        cur_y -= CARD_LINE_H + 3

        # method name + badge
        sf(c, INK); c.setFont('DVMB', CARD_MONO_SZ)
        c.drawString(ML + CARD_PAD_L, cur_y, m['name'])
        mbadge = m.get('badge', '')
        if mbadge:
            mbc, mbfg = BADGE_COLS.get(mbadge, (GRAY_BD, INK))
            mbw = c.stringWidth(mbadge, 'Helvetica-Bold', 6) + 10
            mbh = 11
            mbx = ML + P_CW - CARD_PAD_L - mbw
            sf(c, mbc); ss(c, GRAY_BD); c.setLineWidth(0.4)
            c.roundRect(mbx, cur_y - 2, mbw, mbh, 2, fill=1, stroke=1)
            sf(c, mbfg); c.setFont('Helvetica-Bold', 6)
            c.drawString(mbx + 5, cur_y + 1, mbadge)
        cur_y -= 5

        # call lines
        for line in m.get('calls', []):
            for wl in wrap_lines(c, line, 'DVM', CARD_MONO_SZ, inner_w):
                cur_y -= CARD_LINE_H
                sf(c, INK_MED); c.setFont('DVM', CARD_MONO_SZ)
                c.drawString(ML + CARD_PAD_L + 14, cur_y, wl)
        cur_y -= METH_GAP


FILE_CARDS = [
    {'fname':'Main.java','fpath':'frc/robot/','bar_col':INK,'body_col':GRAY_BG,'badge':'JVM entry',
     'methods':[
         {'name':'main()','badge':'JVM entry','calls':[
             'RobotBase.startRobot(Robot::new)',
             '// JVM entry point — OS calls this once at launch',
             '// framework instantiates Robot, then enters',
             '// the 20ms TimedRobot Notifier loop',
         ]},
     ]},
    {'fname':'Robot.java','fpath':'frc/robot/','bar_col':TEAL,'body_col':TEAL_LT,'badge':'50 Hz',
     'methods':[
         {'name':'Robot()  // constructor','badge':'once','calls':[
             'Logger.recordMetadata("ProjectName","BearBotsXRP")',
             'Logger.addDataReceiver(new WPILOGWriter())',
             '// → writes .wpilog file to USB drive',
             'Logger.addDataReceiver(new NT4Publisher())',
             '// → streams live data to NetworkTables',
             'Logger.start()',
             '// AKit starts capturing — must be called before',
             '// RobotContainer so all subsystems are logged',
             'robotContainer = new RobotContainer()',
         ]},
         {'name':'robotPeriodic()  // ALL modes, every loop','badge':'50 Hz','calls':[
             '// LoggedRobot wraps this call automatically — not called by us:',
             'Logger.periodicBeforeUser()  // ⋯ framework-managed ⋯',
             '// AKit: locks this loop\'s input snapshot',
             'CommandScheduler.getInstance().run()',
             '// runs all scheduler steps — this line IS ours',
             '// LoggedRobot wraps this call automatically — not called by us:',
             'Logger.periodicAfterUser()  // ⋯ framework-managed ⋯',
             '// AKit: flush log frame to file + NT4',
             '// Combine poses ONCE here (not per-subsystem) — avoids',
             '// two subsystems overwriting the same AKit key:',
             'Logger.recordOutput("FinalComponentPoses",',
             '    new Pose3d[]{ drive.getDrivePose3d(), arm.getArmPose3d() })',
         ]},
         {'name':'autonomousInit()','badge':'once','calls':[
             'autonomousCommand = robotContainer.getAutonomousCommand()',
             'if (autonomousCommand != null)',
             '    autonomousCommand.schedule()',
         ]},
         {'name':'teleopInit()','badge':'once','calls':[
             'if (autonomousCommand != null)',
             '    autonomousCommand.cancel()',
             '// stops auto command if still running',
         ]},
         {'name':'disabledInit()','badge':'once','calls':[
             '// Fires ONCE on transition. Runs ONLY code you write here —',
             '// nothing automatic (no auto motor stop). e.g. call',
             '// subsystem stop()/reset() or cancelAll() if desired.',
             '// Separately, EVERY LOOP while disabled, the scheduler ends',
             '// any active command not marked runsWhenDisabled() — that',
             '// ongoing check is NOT part of disabledInit().',
         ]},
         {'name':'disabledPeriodic()','badge':'50 Hz','calls':[
             '// update auto chooser selection from SmartDashboard',
         ]},
     ]},
    {'fname':'RobotContainer.java','fpath':'frc/robot/','bar_col':ORANGE,'body_col':ORANGE_LT,'badge':'once',
     'methods':[
         {'name':'RobotContainer()  // constructor','badge':'once','calls':[
             'switch (Constants.currentMode) {',
             '  case REAL:',
             '    drive = new Drive(new DriveIOXRP())',
             '    arm   = new Arm(new ArmIOXRP())',
             '  case SIM:',
             '    drive = new Drive(new DriveIOSim())',
             '    arm   = new Arm(new ArmIOSim())',
             '  case REPLAY:  // no hardware',
             '    drive = new Drive(new DriveIO() {})',
             '    arm   = new Arm(new ArmIO() {})',
             '}',
             'configureButtonBindings()',
             'configureAutonomous()',
         ]},
         {'name':'configureButtonBindings()  // registers once','badge':'once','calls':[
             '// Registers triggers — does NOT call commands yet',
             '// Scheduler polls these every loop at step 2',
             'controller.a().onTrue(',
             '    arm.setAngleCommand(ArmConstants.kHighAngleDeg))',
             'controller.b().onTrue(',
             '    arm.setAngleCommand(ArmConstants.kLowAngleDeg))',
             'controller.x().onTrue(arm.runOnce(arm::stow))',
             'drive.setDefaultCommand(',
             '    drive.defaultDriveCommand(controller))',
         ]},
         {'name':'configureAutonomous()  // registers once','badge':'once','calls':[
             'autoChooser.addOption("Drive Forward", driveForwardCmd)',
             'autoChooser.addOption("Spin in Place", spinCmd)',
             'SmartDashboard.putData("Auto Chooser", autoChooser)',
         ]},
         {'name':'getAutonomousCommand()','badge':'getter','calls':[
             'return autoChooser.getSelected()',
             '// called by Robot.autonomousInit()',
         ]},
     ]},
    {'fname':'Drive.java','fpath':'frc/robot/subsystems/drive/','bar_col':TEAL,'body_col':TEAL_LT,'badge':'50 Hz',
     'methods':[
         {'name':'Drive(DriveIO io)  // constructor','badge':'once','calls':[
             'this.io = io',
             '// SubsystemBase registers with CommandScheduler',
             '// periodic() will be called every loop at step 1',
         ]},
         {'name':'periodic()  // scheduler step 1','badge':'50 Hz','calls':[
             'io.updateInputs(inputs)',
             '// IO impl reads motors, encoders, gyro → fills inputs',
             'Logger.processInputs("Drive", inputs)',
             '// AKit logs inputs snapshot',
             'Logger.recordOutput("Drive/LeftPositionM",  inputs.leftPositionM)',
             'Logger.recordOutput("Drive/RightPositionM", inputs.rightPositionM)',
             'Logger.recordOutput("Drive/GyroAngleDeg",   inputs.gyroAngleDeg)',
             '// NOTE: does NOT write "FinalComponentPoses" directly —',
             '// that key is aggregated once in Robot.robotPeriodic()',
             '// (see Robot.java card) to avoid multiple subsystems',
             '// overwriting the same AdvantageScope key.',
         ]},
         {'name':'getDrivePose3d()','badge':'getter','calls':[
             'return new Pose3d(0, 0, 0,',
             '    new Rotation3d(0, 0, toRadians(inputs.gyroAngleDeg)))',
             '// Chassis pose for THIS subsystem only.',
             '// Robot.robotPeriodic() collects all subsystem poses',
             '// into ONE "FinalComponentPoses" array — see Robot.java card.',
             '// Teaching simplification: this visualizes heading only.',
             '// A full drivetrain would compute x/y pose from odometry.'
         ]},
         {'name':'setVoltage(double leftV, double rightV)','badge':'output','calls':[
             'io.setVoltage(leftV, rightV)',
             '// delegates to DriveIOXRP or DriveIOSim',
             'Logger.recordOutput("Drive/Commanded/LeftV",  leftV)',
             'Logger.recordOutput("Drive/Commanded/RightV", rightV)',
         ]},
         {'name':'stop()','badge':'output','calls':[
             'setVoltage(0.0, 0.0)',
         ]},
         {'name':'defaultDriveCommand(XboxController ctrl)','badge':'getter','calls':[
             '// Returns Command used as subsystem default',
             '// Scheduler runs this when no other Drive cmd is active',
             'return run(() -> {',
             '    double speed = -ctrl.getLeftY()',
             '    double turn  =  ctrl.getRightX()',
             '    setVoltage((speed + turn) * kMaxBatteryVoltage,',
             '               (speed - turn) * kMaxBatteryVoltage)',
             '})',
         ]},
     ]},
    {'fname':'Arm.java','fpath':'frc/robot/subsystems/arm/','bar_col':TEAL,'body_col':TEAL_LT,'badge':'50 Hz',
     'methods':[
         {'name':'Arm(ArmIO io)  // constructor','badge':'once','calls':[
             'this.io = io',
             'mechanism   = new LoggedMechanism2d(3, 3)',
             'root        = mechanism.getRoot("ArmPivot", 1.2, 0.18)',
             'armLigament = root.append(',
             '    new LoggedMechanismLigament2d("Arm", feetToMeters(3), 0))',
         ]},
         {'name':'periodic()  // scheduler step 1','badge':'50 Hz','calls':[
             'io.updateInputs(inputs)',
             '// reads servo state → inputs.commandedAngleDeg',
             'Logger.processInputs("Arm", inputs)',
             '// AKit logs inputs snapshot',
             'armLigament.setAngle(180 - inputs.commandedAngleDeg)',
             '// 180- flips coordinate convention for AdvantageScope',
             'Logger.recordOutput("Arm/Mechanism2d", mechanism)',
             '// 2D stick-figure diagram in AdvantageScope',
             '// NOTE: does NOT write "FinalComponentPoses" directly —',
             '// see getArmPose3d() below + Robot.robotPeriodic()',
         ]},
         {'name':'getArmPose3d()','badge':'getter','calls':[
             'return new Pose3d(-0.052, 0.007, 0.0645,',
             '    new Rotation3d(0, toRadians(inputs.commandedAngleDeg), 0))',
             '// 3D joint pose for THIS subsystem only.',
             '// Robot.robotPeriodic() collects all subsystem poses',
             '// into ONE "FinalComponentPoses" array — see Robot.java card.',
         ]},
         {'name':'setAngle(double angleDeg)','badge':'output','calls':[
             'io.setAngle(angleDeg)',
             '// delegates to ArmIOXRP or ArmIOSim',
             'Logger.recordOutput("Arm/Commanded/AngleDeg", angleDeg)',
         ]},
         {'name':'stow()','badge':'output','calls':[
             'setAngle(ArmConstants.kStowedAngleDeg)',
             '// safe stow = 180°',
             '// servo holds position — not cutting power',
         ]},
         {'name':'getCommandedAngleDeg()','badge':'getter','calls':[
             'return inputs.commandedAngleDeg',
         ]},
     ]},
    {'fname':'ArmIO.java','fpath':'frc/robot/subsystems/arm/','bar_col':PURPLE,'body_col':PURPLE_LT,'badge':'interface',
     'methods':[
         {'name':'@AutoLog  class ArmIOInputs','badge':'AKit','calls':[
             '// @AutoLog generates ArmIOInputsAutoLogged at compile time',
             '// Every field is auto-logged — no manual Logger calls needed',
             'public double commandedAngleDeg = ArmConstants.kStowedAngleDeg',
         ]},
         {'name':'updateInputs(ArmIOInputs inputs)','badge':'contract','calls':[
             'default void updateInputs(ArmIOInputs inputs) {}',
             '// default = no-op (log replay stub)',
             '// ArmIOXRP overrides:',
             '//   inputs.commandedAngleDeg = servo.getAngle()',
         ]},
         {'name':'setAngle(double angleDeg)','badge':'contract','calls':[
             'default void setAngle(double angleDeg) {}',
             '// default = no-op (log replay stub)',
             '// ArmIOXRP overrides:',
             '//   servo.setAngle(angleDeg)',
         ]},
     ]},
    {'fname':'ArmIOXRP.java','fpath':'frc/robot/subsystems/arm/','bar_col':RED,'body_col':RED_LT,'badge':'reads HW',
     'methods':[
         {'name':'ArmIOXRP()  // constructor','badge':'once','calls':[
             'servo = new XRPServo(5)',
             '// port 5 = Servo 2 on XRP board',
         ]},
         {'name':'updateInputs(ArmIOInputs inputs)','badge':'reads HW','calls':[
             'inputs.commandedAngleDeg = servo.getAngle()',
             '// reads current servo position from hardware',
             '// called by Arm.periodic() at scheduler step 1',
         ]},
         {'name':'setAngle(double angleDeg)','badge':'writes HW','calls':[
             'servo.setAngle(angleDeg)',
             '// XRPServo.setAngle() sends PWM signal',
             '// physical servo moves to requested angle',
         ]},
     ]},
    {'fname':'DriveIOXRP.java','fpath':'frc/robot/subsystems/drive/','bar_col':RED,'body_col':RED_LT,'badge':'reads HW',
     'methods':[
         {'name':'DriveIOXRP()  // constructor','badge':'once','calls':[
             'leftMotor    = new XRPMotor(0)   // port 0 = left motor',
             'rightMotor   = new XRPMotor(1)   // port 1 = right motor',
             'rightMotor.setInverted(true)     // right must be inverted',
             'leftEncoder  = new Encoder(4, 5) // DIO pins 4/5',
             'rightEncoder = new Encoder(6, 7) // DIO pins 6/7',
             'gyro         = new XRPGyro()',
         ]},
         {'name':'updateInputs(DriveIOInputs inputs)','badge':'reads HW','calls':[
             'inputs.leftPositionM     = leftEncoder.getDistance()',
             'inputs.rightPositionM    = rightEncoder.getDistance()',
             'inputs.leftVelocityMPS   = leftEncoder.getRate()',
             'inputs.rightVelocityMPS  = rightEncoder.getRate()',
             'inputs.gyroAngleDeg      = gyro.getAngle()',
             'inputs.gyroRateDegPerSec = gyro.getRate()',
         ]},
         {'name':'setVoltage(double leftV, double rightV)','badge':'writes HW','calls':[
             'leftMotor.set(MathUtil.clamp(',
             '    leftV / Constants.kMaxBatteryVoltage, -1.0, 1.0))',
             'rightMotor.set(MathUtil.clamp(',
             '    rightV / Constants.kMaxBatteryVoltage, -1.0, 1.0))',
             '// kMaxBatteryVoltage = 4.5 V  (4×AA XRP nominal)',
             '// XRPMotor.set() takes percent output: -1.0 to 1.0',
             '// (NOT 0.0–1.0 — motor needs negative values to reverse)',
         ]},
     ]},
    {'fname':'Constants.java','fpath':'frc/robot/','bar_col':GRAY_BD,'body_col':GRAY_BG,'badge':'static',
     'methods':[
         {'name':'RobotMode  // enum','badge':'static','calls':[
             'REAL,      // running on physical XRP hardware',
             'SIM,       // WPILib desktop simulation',
             'REPLAY     // log replay (no hardware, reads from log)',
         ]},
         {'name':'currentMode','badge':'static','calls':[
             'public static final RobotMode currentMode = RobotMode.REAL',
             '// Change to SIM for simulation, REPLAY for log replay',
         ]},
         {'name':'kMaxBatteryVoltage','badge':'static','calls':[
             'public static final double kMaxBatteryVoltage = 4.5',
             '// 4×AA alkaline cells — XRP nominal supply voltage',
             '// DriveIOXRP divides commanded volts by this value',
             '// to convert volts → -1.0 to 1.0 motor percent',
         ]},
     ]},
    {'fname':'ArmConstants.java','fpath':'frc/robot/subsystems/arm/','bar_col':GRAY_BD,'body_col':GRAY_BG,'badge':'static',
     'methods':[
         {'name':'Servo angle limits','badge':'static','calls':[
             'kMinAngleDeg   =   0.0  // minimum allowed servo angle (degrees)',
             'kMaxAngleDeg   = 180.0  // maximum allowed servo angle (degrees)',
         ]},
         {'name':'Named positions','badge':'static','calls':[
             'kStowedAngleDeg = 180.0  // safe / stowed arm position',
             'kLowAngleDeg    = 135.0  // low position',
             'kHighAngleDeg   =  90.0  // high position',
         ]},
     ]},
]

# ══════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════

def continues_down_arrow(c, spine_bot_y, label='continues on next page →'):
    """Draw a downward arrow at bottom of spine with continuation label."""
    cx = S_X + S_W / 2
    end_y = spine_bot_y - 18
    ss(c, INK_MUT); c.setLineWidth(1.2); c.setDash([3,2])
    c.line(cx, spine_bot_y, cx, end_y + 5)
    c.setDash([])
    ah_down(c, cx, end_y, INK_MUT)
    sf(c, INK_MUT); c.setFont('Helvetica-Oblique', 6.5)
    c.drawCentredString(cx, end_y - 9, label)

def loop_exit_arrow(c, ph, label='Loop continues on next page →'):
    """Green arrow exiting bottom of page for loop continuation."""
    cx = S_X + S_W / 2
    bot = fc_bottom() + 2
    ss(c, GREEN); c.setLineWidth(1.5); c.setDash([])
    c.line(cx, bot + 22, cx, bot + 4)
    ah_down(c, cx, bot, GREEN, sz=5)
    sf(c, GREEN); c.setFont('Helvetica-Bold', 6.5)
    c.drawCentredString(cx, bot - 10, label)
    # vertical label on right
    c.saveState()
    c.translate(S_X + S_W + 8, bot + 12)
    c.rotate(90)
    sf(c, GREEN); c.setFont('Helvetica-Oblique', 6)
    c.drawString(0, 0, 'Notifier fires again → new 20ms cycle (see previous page)')
    c.restoreState()

def loop_entry_arrow(c, ph, to_y, label='← loop continues from previous page'):
    """Green arrow entering top of page, pointing down to spine."""
    cx = S_X + S_W / 2
    top = port_top(ph) + 4
    ss(c, GREEN); c.setLineWidth(1.5); c.setDash([])
    c.line(cx, top, cx, to_y + 5)
    ah_down(c, cx, to_y, GREEN, sz=5)
    sf(c, GREEN); c.setFont('Helvetica-Oblique', 6.5)
    c.drawCentredString(cx, top + 6, label)


# ══════════════════════════════════════════════════════════════════════════
# PAGE 1 — STARTUP PART 1
# ══════════════════════════════════════════════════════════════════════════
def draw_page_startup_1(c, page_num):
    c.setPageSize((PW, PH))
    draw_header(c, page_num, PW, PH, subtitle='STARTUP — Part 1 of 2  (runs once at power-on)')
    draw_footer(c, PW, PH)
    draw_legend_portrait(c, PW, PH)
    start_y = port_top(PH)
    groups = startup_groups_p1()
    layout_groups(c, groups, start_y)
    draw_groups(c, groups)
    # Continuation arrow at bottom of last spine box
    continues_down_arrow(c, groups[-1].spine_bot,
                         'configureAutonomous() continues on next page →')


# ══════════════════════════════════════════════════════════════════════════
# PAGE 2 — STARTUP PART 2 + LOOP START
# ══════════════════════════════════════════════════════════════════════════

def draw_page_startup_2(c, page_num):
    """Page 2: configureAutonomous + DS mode + STARTUP COMPLETE + loop groups 0-2 (Notifier, DS changed, modePeriodic).
    Green left-rail loop-back arrow: runs from bottom of modePeriodic UP to bottom of Notifier fires box.
    """
    c.setPageSize((PW, PH))
    draw_header(c, page_num, PW, PH,
                subtitle='STARTUP — Part 2 of 2,  then  20ms LOOP — Part 1 of 2')
    draw_footer(c, PW, PH, right_txt='Loop continues on next page →')
    draw_legend_portrait(c, PW, PH)
    start_y = port_top(PH)

    # Continuation note
    sf(c, INK_MUT); c.setFont('Helvetica-Oblique', 6.5)
    c.drawString(S_X, start_y, u'\u2190 continuing from previous page: configureButtonBindings()')
    start_y -= 12

    # Startup groups
    groups = startup_groups_p2()
    layout_groups(c, groups, start_y)
    draw_groups(c, groups)

    # STARTUP COMPLETE bar
    bar_top = groups[-1].group_bot - 10
    sf(c, TEAL); c.setLineWidth(0)
    c.roundRect(S_X, bar_top - 20, S_W, 20, 3, fill=1, stroke=0)
    sf(c, WHITE); c.setFont('Helvetica-Bold', 7.5)
    c.drawCentredString(S_X + S_W/2, bar_top - 13, 'STARTUP COMPLETE')

    # Separator
    sep_y = bar_top - 30
    ss(c, TEAL); c.setLineWidth(1.5)
    c.line(S_X, sep_y, S_X + S_W + B1_W + 28, sep_y)
    sf(c, TEAL); c.setFont('Helvetica-Bold', 8)
    c.drawString(S_X, sep_y - 12, '20ms LOOP \u2014 Notifier fires 50\u00d7 per second')

    loop_start_y = sep_y - 26

    # Loop groups that fit: Notifier, DS changed, modePeriodic
    loop_g = loop_groups_p3()
    fit_groups = loop_g[:3]
    layout_groups(c, fit_groups, loop_start_y)
    draw_groups(c, fit_groups)

    # Green loop-back rail:
    # Extends from footer bottom edge UP to Notifier box bottom.
    # Arrowhead pointing RIGHT into the Notifier box.
    notifier_bottom = fit_groups[0].spine_bot
    rail_x = S_X - 20
    rail_bottom = fc_bottom() + 4   # extends all the way to footer
    ss(c, GREEN); c.setLineWidth(1.5); c.setDash([])
    # vertical line from footer up to Notifier bottom level
    c.line(rail_x, rail_bottom, rail_x, notifier_bottom + 5)
    # horizontal right from rail into Notifier box left edge
    c.line(rail_x, notifier_bottom + 5, S_X - 2, notifier_bottom + 5)
    # rightward arrowhead pointing INTO the Notifier box
    ah_right(c, S_X, notifier_bottom + 5, GREEN, sz=5)
    # rotated label mid-rail
    sf(c, GREEN); c.setFont('Helvetica-Bold', 6)
    c.saveState()
    mid_y = (notifier_bottom + rail_bottom) / 2
    c.translate(rail_x - 5, mid_y)
    c.rotate(90)
    c.drawCentredString(0, 0, 'loop cycles back here \u2014 Notifier fires every 20ms')
    c.restoreState()

    # Continuation note at bottom of last spine box
    continues_down_arrow(c, fit_groups[-1].spine_bot,
                         'Robot.robotPeriodic() continues on next page \u2192')


def draw_page_loop_combined(c, page_num):
    """Page 3: Robot.robotPeriodic + Logger.before + CommandScheduler (4 merged steps) + Logger.after + SmartDash + sim + watchdog.
    Green left-rail entry arrow: from top of page DOWN to Robot.robotPeriodic top.
    Teal loop-back arrow: from watchdog bottom, left rail, UP to top of page (pointing up off page toward page 2).
    """
    c.setPageSize((PW, PH))
    draw_header(c, page_num, PW, PH,
                subtitle='20ms LOOP \u2014 Part 2 of 2  (robotPeriodic through watchdog)')
    draw_footer(c, PW, PH)
    draw_legend_portrait(c, PW, PH)
    content_top = port_top(PH)

    # Continuation note — clearly below the legend strip
    note_y = content_top - 14
    sf(c, INK_MUT); c.setFont('Helvetica-Oblique', 6.5)
    c.drawString(S_X, note_y, u'\u2190 continuing from previous page: modePeriodic()')

    # Green entry arrow starts BELOW the continuation note (separate vertical space)
    entry_top = note_y - 14
    start_y = entry_top - 14   # spine boxes begin below the arrow

    # All remaining loop spine groups
    p3_spine = loop_groups_p3()[3:]   # Robot.robotPeriodic, Logger.before, CommandScheduler
    p4_spine = loop_groups_p4()   # Logger.after, SmartDash, sim, watchdog

    # Lay out all spine groups (no separate "continued" box needed —
    # all 4 scheduler steps now hang off the single CommandScheduler.run() box)
    all_spine = p3_spine + p4_spine
    layout_groups(c, all_spine, start_y)
    draw_groups(c, all_spine)

    # CommandScheduler steps, merged to 4 — matches the actual order in
    # CommandScheduler.run() (allwpilib source): conflict/requirement checks
    # happen INSIDE schedule() during step 2, not as a separate pass; execute
    # and end-of-command handling happen in the same iteration (step 3).
    cs_group = p3_spine[2]
    steps_merged = [
        (['Run periodic() for ALL registered subsystems',
          '  Drive.periodic() / Arm.periodic()',
          '  Elevator.periodic() / Scoop.periodic()'],
         TEAL_LT, TEAL),
        (['Poll triggers \u2192 schedule new commands',
          '  // checks every Trigger from configureButtonBindings()',
          '  // condition met \u2192 schedule(command)',
          '  // conflict checks happen HERE, inside schedule():',
          '  //   kCancelSelf     \u2192 cancel old, init new',
          '  //   kCancelIncoming \u2192 reject new, keep old'],
         PURPLE_LT, PURPLE),
        (['Execute active commands \u2192 end finished ones',
          '  // each active cmd runs execute() body',
          '  //   defaultDriveCommand.execute()',
          '  //   reads joystick \u2192 drive.setVoltage()',
          '  // isFinished()? \u2192 end(false), remove',
          '  // disabled + unsafe \u2192 end(true), remove'],
         PURPLE_LT, PURPLE),
        (['Schedule default commands',
          '  // subsystems with no active command this loop',
          '  // Drive \u2192 defaultDriveCommand'],
         PURPLE_LT, PURPLE),
    ]
    draw_sequential_steps(c, cs_group, steps_merged, first_step_num=1)

    # Green left-rail ENTRY arrow: from below the continuation note down to Robot.robotPeriodic top
    robot_top = all_spine[0].spine_top
    entry_x = S_X + S_W / 2
    ss(c, GREEN); c.setLineWidth(1.5); c.setDash([])
    c.line(entry_x, entry_top, entry_x, robot_top + 5)
    ah_down(c, entry_x, robot_top, GREEN, sz=5)

    # Teal loop-back arrow: left margin, from watchdog bottom UP and off the top of the page
    watchdog = all_spine[-1]
    wb = watchdog.spine_bot
    rail_x = S_X - 22
    # Teal rail stops at port_top minus extra space — below legend and continuation text
    top_y = port_top(PH) - 36   # well below legend + continuation text

    ss(c, TEAL); c.setLineWidth(1.5); c.setDash([])
    # down from watchdog
    c.line(S_X + S_W/2, wb, S_X + S_W/2, wb - 8)
    # left to rail
    c.line(S_X + S_W/2, wb - 8, rail_x, wb - 8)
    # UP to near top of content area
    c.line(rail_x, wb - 8, rail_x, top_y)
    # arrowhead pointing UP
    ah_up(c, rail_x, top_y, TEAL, sz=5)

    # rotated label on the teal rail
    sf(c, TEAL); c.setFont('Helvetica-Bold', 6)
    c.saveState()
    mid_y = (wb - 8 + top_y) / 2
    c.translate(rail_x - 5, mid_y)
    c.rotate(90)
    c.drawCentredString(0, 0, 'Notifier fires again \u2192 loop restarts at page 2')
    c.restoreState()


def draw_detail(c, page_num):
    c.setPageSize((TLW, TLH))
    draw_header(c, page_num, TLW, TLH,
                subtitle='CALL DETAIL — inside CommandScheduler steps 1 (periodic) and 3 (execute)')
    draw_footer(c, TLW, TLH)
    draw_legend(c, TLW, TLH)
    start_y = fc_top(TLH)

    def G(sl, sbg, sbd, bf=False, b1=None,b2=None,b3=None,b4=None,note=None,nc=None,fw=False):
        return make_group(sl,sbg,sbd,bf,b1,b2,b3,b4,note,nc,framework=fw)

    groups = [
        G(['1 Arm.periodic()  ← called by scheduler',
           '// step 1 for every registered subsystem'],
          TEAL_LT, TEAL, bf=True,
          b1=(['io.updateInputs(inputs)',
               '// IO impl reads hardware → fills struct'],
              GREEN_LT, GREEN),
          b2=(['ArmIOXRP.updateInputs():',
               '  inputs.commandedAngleDeg = servo.getAngle()',
               'DriveIOXRP.updateInputs():',
               '  inputs.leftPositionM = leftEncoder.getDistance()',
               '  inputs.rightPositionM = rightEncoder.getDistance()',
               '  inputs.gyroAngleDeg = gyro.getAngle()'],
              RED_LT, RED),
          b3=(['XRP Hardware reads:',
               'XRPServo(5).getAngle()  // Servo 2, port 5',
               'Encoder(4,5).getDistance()  // left DIO 4/5',
               'XRPGyro.getAngle()'],
              RED_LT, RED),
          note="inputs should now be treated as this cycle''s snapshot.\nDo not modify inputs directly after processInputs().",
          nc=GREEN),
        G(['Logger.processInputs("Arm", inputs)',
           '// REAL: writes to log  REPLAY: reads from log'],
          GREEN_LT, GREEN,
          b1=(['// REAL mode:',
               '//   inputs written to .wpilog file',
               '// REPLAY mode:',
               '//   inputs overwritten FROM .wpilog file',
               '//   subsystem sees identical values as real match',
               '// This is the key AKit replay guarantee'],
              GREEN_LT, GREEN),
          note='processInputs() = replay-critical hardware data. recordOutput() = calculated values and visualization.',
          nc=GREEN),
        G(['Arm.periodic() continues',
           'armLigament.setAngle(180 - inputs.commandedAngleDeg)',
           'Logger.recordOutput("Arm/Mechanism2d", mechanism)',
           '// pose collected later by Robot.robotPeriodic() →'],
          TEAL_LT, TEAL,
          b1=(['// 180- flips coordinate convention',
               '// 2D stick-figure in AdvantageScope',
               'getArmPose3d() returns:',
               '  new Pose3d(-0.052, 0.007, 0.0645,',
               '    new Rotation3d(0,',
               '      toRadians(inputs.commandedAngleDeg), 0))',
               '// Robot.robotPeriodic() combines this with',
               '// drive.getDrivePose3d() into ONE',
               '// "FinalComponentPoses" array — avoids two',
               '// subsystems overwriting the same AKit key.'],
              TEAL_LT, TEAL)),
        G(['3 defaultDriveCommand.execute()',
           '// called by scheduler for active commands'],
          TEAL_LT, TEAL, bf=True,
          b1=(['double speed = -controller.getLeftY()',
               'double turn  =  controller.getRightX()',
               'drive.setVoltage(',
               '  (speed+turn) * kMaxBatteryVoltage,',
               '  (speed-turn) * kMaxBatteryVoltage)'],
              TEAL_LT, TEAL),
          b2=(['DriveIOXRP.setVoltage(leftV, rightV)',
               'leftMotor.set(clamp(leftV / kMaxBatteryVoltage, -1, 1))',
               'rightMotor.set(clamp(rightV / kMaxBatteryVoltage, -1, 1))',
               '// kMaxBatteryVoltage = 4.5 V',
               '// rightMotor.setInverted(true) was set ONCE in the',
               '// constructor — do NOT also negate pct here, or the',
               '// right side double-inverts and drives backward.'],
              RED_LT, RED),
          b3=(['XRP Hardware writes:',
               'XRPMotor(0).set(pct)  // left motor',
               'XRPMotor(1).set(pct)  // right — already inverted',
               '                      // via setInverted(true)'],
              RED_LT, RED)),
        G(['arm command execute()  (if button held)'],
          TEAL_LT, TEAL,
          b1=(['arm.setAngle(angleDeg)',
               'io.setAngle(angleDeg)',
               'Logger.recordOutput(',
               '  "Arm/Commanded/AngleDeg", angleDeg)'],
              TEAL_LT, TEAL),
          b2=(['ArmIOXRP.setAngle(angleDeg)',
               'servo.setAngle(angleDeg)',
               '// XRPServo port 5'],
              RED_LT, RED),
          b3=(['XRP Hardware write:',
               'XRPServo(5).setAngle(deg)',
               '// Servo 2 on XRP board',
               '// physical arm moves'],
              RED_LT, RED)),
    ]
    layout_groups(c, groups, start_y)
    draw_groups(c, groups)


# ══════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════
def build():
    global TOTAL_PAGES
    n_cards = len(FILE_CARDS)
    TOTAL_PAGES = 4 + n_cards   # 3 portrait + 1 landscape + N cards

    out = 'BearBots_Program_Flow.pdf'
    c = rl_canvas.Canvas(out)

    for i, card in enumerate(FILE_CARDS):
        card['idx'] = i + 1
        card['total'] = n_cards

    draw_page_startup_1(c, 1)
    c.showPage()
    draw_page_startup_2(c, 2)
    c.showPage()
    draw_page_loop_combined(c, 3)
    c.showPage()
    draw_detail(c, 4)
    for i, card in enumerate(FILE_CARDS):
        c.showPage()
        draw_one_card(c, card, 5 + i)

    c.save()
    print(f'Saved: {out}')
    print(f'Total pages: {TOTAL_PAGES}  (3 portrait + 1 landscape + {n_cards} cards)')

build()
