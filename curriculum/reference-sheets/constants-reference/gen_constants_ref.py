"""
BearBots FRC — Constants Quick Reference Sheet  (v3)
Fixes:
  - Keywords block: bullet list instead of inline annotations
  - Type table: expanded with more FRC-relevant types
  - FRC wild note: extra space above it, separated from table
  - Inner class example: shows correct per-file pattern (DriveConstants.java, not Constants.java blob)
  - Label spacing: 4pt gap between label and code block below it
  - Tip/warning boxes: bottom padding enforced (min 5pt gap below last text line)
  - Common mistakes: 4pt gap after divider line before next title
  - Footer: two lines instead of three to avoid overlap
  - Header: no lesson range reference
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('DV',   '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVB',  '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DVI',  '/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf'))
pdfmetrics.registerFont(TTFont('DVM',  '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'))
pdfmetrics.registerFont(TTFont('DVMB', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'))

def rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))

TEAL      = rgb('#2D6B6B'); TEAL_LT   = rgb('#EAF4F4')
PURPLE    = rgb('#6B4A9B'); PURPLE_LT = rgb('#F0ECF8')
ORANGE    = rgb('#B8762A'); ORANGE_LT = rgb('#FAF3E8')
GREEN     = rgb('#2D7A4F')
RULE      = rgb('#CCCCCC'); TXT       = rgb('#222222')
TXT_MED   = rgb('#555555'); TXT_MUT   = rgb('#888888')
WHITE     = (1,1,1)
CODE_BG   = rgb('#F5F5F5'); CODE_BD   = rgb('#DDDDDD')
KW_COL    = rgb('#2D6B6B'); NUM_COL   = rgb('#6B4A9B')
CMT_COL   = rgb('#999999'); RED       = rgb('#CC4444')

W,H   = letter
ML=MR = 0.42*inch; MT=MB = 0.38*inch
CW    = W-ML-MR; GAP = 7
COL_W = (CW-GAP)/2
HDR_H=56; FOOTER_H=26; BAR_H=20; PAD=7; SGAP=8
INNER_PAD = 6   # horizontal inset inside section boxes

def sf(c,col): c.setFillColorRGB(*col)
def ss(c,col): c.setStrokeColorRGB(*col)

def section_box(c,x,y,w,h,label,bar_color,fill,r=5,bh=BAR_H):
    sf(c,fill); ss(c,RULE); c.setLineWidth(0.75)
    c.roundRect(x,y,w,h,r,fill=1,stroke=1)
    sf(c,bar_color); c.setLineWidth(0)
    c.roundRect(x,y+h-bh,w,bh+r,r,fill=1,stroke=0)
    sf(c,bar_color); c.rect(x,y+h-bh,w,r,fill=1,stroke=0)
    sf(c,WHITE); c.setFont('Helvetica-Bold',7.5)
    c.drawString(x+8,y+h-bh/2-3.5,label)

def wrap(c,text,font,size,maxw):
    c.setFont(font,size)
    words=text.split(); lines=[]; cur=''
    for word in words:
        t=(cur+' '+word).strip()
        if c.stringWidth(t,font,size)<=maxw: cur=t
        else:
            if cur: lines.append(cur)
            cur=word
    if cur: lines.append(cur)
    return lines

def code_block(c,x,top_y,w,line_tokens,lh=9.0,pad=5):
    """Draw shaded code block; returns bottom y."""
    h = len(line_tokens)*lh + pad*2
    sf(c,CODE_BG); ss(c,CODE_BD); c.setLineWidth(0.4)
    c.roundRect(x, top_y-h, w, h, 3, fill=1, stroke=1)
    cy = top_y - pad - lh + 2
    for toks in line_tokens:
        cx = x+pad
        for text,col in toks:
            sf(c,col); c.setFont('DVM',6.8)
            c.drawString(cx,cy,text)
            cx += c.stringWidth(text,'DVM',6.8)
        cy -= lh
    return top_y - h   # bottom edge

def tip_box(c,x,top_y,w,title,body_lines,title_col,bg_col,bd_col,lh=9,pad=6):
    """Draw a coloured tip/warning box; returns bottom y.
    Ensures pad pts of space below last text line."""
    content_h = 9 + len(body_lines)*lh   # title + lines
    h = content_h + pad*2
    sf(c,bg_col); ss(c,bd_col); c.setLineWidth(0.6)
    c.roundRect(x, top_y-h, w, h, 3, fill=1, stroke=1)
    ty = top_y - pad - 8
    sf(c,title_col); c.setFont('Helvetica-Bold',7.5)
    c.drawString(x+pad, ty, title)
    ty -= lh
    sf(c,TXT); c.setFont('Helvetica',7)
    for ln in body_lines:
        c.drawString(x+pad, ty, ln)
        ty -= lh
    return top_y - h

# ── Header ─────────────────────────────────────────────────────────────────
def draw_header(c,top_y,page=1):
    x,y,w,h = ML,top_y-HDR_H,CW,HDR_H
    sf(c,TEAL); c.setLineWidth(0)
    c.roundRect(x,y,w,h,6,fill=1,stroke=0)
    sf(c,rgb('#A8D4D4')); c.setFont('Helvetica-Bold',7.5)
    c.drawString(x+10,y+h-13,'BEARBOTS TEAM 6964  —  FRC PROGRAMMING CURRICULUM')
    sf(c,WHITE); c.setFont('Helvetica-Bold',20)
    c.drawString(x+10,y+h-38,'Constants Quick Reference')
    sf(c,rgb('#A8D4D4')); c.setFont('Helvetica-Bold',8)
    c.drawRightString(x+w-12,y+h-18,'Java  |  WPILib  |  XRP')
    sf(c,rgb('#BBDDDD')); c.setFont('Helvetica-Oblique',7.5)
    c.drawRightString(x+w-12,y+h-30,'Keep this. Add it to your binder.')
    sf(c,rgb('#BBDDDD')); c.setFont('Helvetica-Oblique',7)
    c.drawRightString(x+w-12,y+h-41,f'Page {page} of 2')
    return y

# ── Footer ─────────────────────────────────────────────────────────────────
def draw_footer(c):
    y = MB
    sf(c,TEAL); c.setLineWidth(0)
    c.roundRect(ML,y,CW,FOOTER_H,4,fill=1,stroke=0)
    my = y+FOOTER_H/2-3.5
    sf(c,WHITE)
    c.setFont('Helvetica-Bold',7.5)
    c.drawString(ML+8,my,'BearBots FRC — Constants Quick Reference')
    c.setFont('Helvetica',7.5)
    c.drawRightString(ML+CW-8,my,'public static final — define once, use everywhere')

# ══════════════════════════════════════════════════════════════════════════
# PAGE 1  Section 1 — THE DECLARATION RECIPE  (full width)
# ══════════════════════════════════════════════════════════════════════════
def draw_declaration(c,top_y):
    # ── content data ──────────────────────────────────────────────────
    type_rows=[
        ('double',  '64-bit decimal',  'kSpeedLimit = 0.8',           'Speeds, distances, PID gains, voltages'),
        ('int',     'Whole number',    'kLeftMotorPort = 0',           'Port numbers, CAN IDs, counts'),
        ('String',  'Text',            'kProjectName = "BearBots"',    'Logger keys, auto mode names'),
        ('boolean', 'True / false',    'kIsRightInverted = true',      'Inversion flags, feature toggles'),
        ('long',    '64-bit integer',  'kLoopPeriodUs = 20_000L',      'Microsecond timestamps, large counts'),
        ('float',   '32-bit decimal',  'kGearRatio = 6.75f',           'Lightweight calculations, sensor values'),
    ]

    # ── measure ───────────────────────────────────────────────────────
    bullet_lh   = 12   # per bullet line
    bullet_block= 3*bullet_lh + 4   # 3 bullets + small gap
    intro_h     = 11
    code_lh     = 11
    code_h      = code_lh + 4       # single example line + vertical padding
    row_h       = 13
    table_h     = (len(type_rows)+1)*row_h + 4
    note_h      = 18   # 2-line FRC wild note with top gap
    callout_h   = 54   # why-not-others box (gap + title + 3 lines + padding)
    h = BAR_H+PAD + intro_h+4 + code_h+4 + bullet_block+8 + table_h + note_h + callout_h + PAD

    y = top_y-h
    section_box(c,ML,y,CW,h,'THE DECLARATION RECIPE',TEAL,TEAL_LT)

    iy = y+h-BAR_H-PAD-2

    # intro line
    sf(c,TXT); c.setFont('Helvetica',8)
    c.drawString(ML+INNER_PAD, iy, 'Every constant uses three keywords before the type and name:')
    iy -= intro_h+4

    # colour-coded example line
    parts=[('public ',TEAL),('static ',PURPLE),('final ',ORANGE)]
    kx=ML+INNER_PAD
    for kw,col in parts:
        sf(c,col); c.setFont('DVMB',9.5)
        c.drawString(kx,iy,kw); kx+=c.stringWidth(kw,'DVMB',9.5)
    sf(c,TXT_MED); c.setFont('DVM',9.5)
    c.drawString(kx,iy,'double  kSpeedLimit  =  0.8 ;')
    iy -= code_h+4

    # bullet list — one keyword per bullet
    bullets=[
        (TEAL,   'public',  ' — any file in the project can read it'),
        (PURPLE, 'static',  ' — belongs to the class itself; no new Constants() required'),
        (ORANGE, 'final',   ' — value is locked at startup and can never be reassigned'),
    ]
    for col,kw,desc in bullets:
        sf(c,col);  c.setFont('DVB',8)
        bx=ML+INNER_PAD
        c.drawString(bx, iy, '\u2022 ')
        bx += c.stringWidth('\u2022 ','DVB',8)
        c.setFont('DVMB',8)
        c.drawString(bx, iy, kw)
        bx += c.stringWidth(kw,'DVMB',8)
        sf(c,TXT); c.setFont('Helvetica',8)
        c.drawString(bx, iy, desc)
        iy -= bullet_lh
    iy -= 8

    # type table
    tcols=[ML+INNER_PAD, ML+62, ML+145, ML+295]
    sf(c,TEAL); c.setLineWidth(0)
    c.rect(ML+INNER_PAD, iy-row_h+3, CW-INNER_PAD*2, row_h-1, fill=1, stroke=0)
    sf(c,WHITE); c.setFont('Helvetica-Bold',7)
    for txt,tx in zip(['Type','Meaning','BearBots example','Common uses in FRC'],tcols):
        c.drawString(tx+3, iy-row_h+3+3, txt)
    iy -= row_h

    for ri,(typ,meaning,example,use) in enumerate(type_rows):
        bg = TEAL_LT if ri%2==0 else WHITE
        sf(c,bg); c.setLineWidth(0)
        c.rect(ML+INNER_PAD, iy-row_h+3, CW-INNER_PAD*2, row_h-1, fill=1, stroke=0)
        sf(c,KW_COL);  c.setFont('DVMB',7);     c.drawString(tcols[0]+3, iy-row_h+3+3, typ)
        sf(c,TXT_MED); c.setFont('Helvetica',7); c.drawString(tcols[1]+3, iy-row_h+3+3, meaning)
        sf(c,TXT);     c.setFont('DVM',6.5);     c.drawString(tcols[2]+3, iy-row_h+3+3, example)
        sf(c,TXT_MED); c.setFont('Helvetica',6.5);c.drawString(tcols[3]+3, iy-row_h+3+3, use)
        iy -= row_h

    iy -= 8   # deliberate space above FRC wild note
    sf(c,TXT_MED); c.setFont('Helvetica-Oblique',7)
    c.drawString(ML+INNER_PAD, iy,
        'In the FRC wild you\u2019ll also see: TunerConstants, FieldConstants, VisionConstants \u2014 same')
    iy -= 8
    c.drawString(ML+INNER_PAD, iy,
        'public static final pattern, split into separate files as codebases grow.')

    # why-not-others callout
    iy -= 6
    tip_box(
        c, ML+INNER_PAD, iy, CW-INNER_PAD*2,
        title='\u2139  Why not the other keywords?',
        body_lines=[
            'private makes a constant unreadable from other files \u2014 defeats the purpose.',
            'No static means you need an object instance to read it \u2014 no new Constants() needed.',
            'No final means the value can be overwritten at runtime \u2014 it becomes a variable, not a constant.',
        ],
        title_col=TEAL,
        bg_col=TEAL_LT,
        bd_col=RULE,
        lh=9, pad=6
    )
    return y

# ══════════════════════════════════════════════════════════════════════════
# PAGE 1  Section 2 — Constants File Pattern (left) + How to Use (right)
# ══════════════════════════════════════════════════════════════════════════
def draw_structure_usage(c,top_y,bottom_limit):
    avail = top_y-bottom_limit
    y = bottom_limit
    section_box(c,ML,           y,COL_W,avail,'CONSTANTS FILE PATTERN',TEAL,TEAL_LT)
    section_box(c,ML+COL_W+GAP, y,COL_W,avail,'HOW TO USE A CONSTANT',PURPLE,PURPLE_LT)

    # ── LEFT: recommended separate-file pattern ────────────────────────
    # Show each class living in its own file — the encouraged pattern
    L=[
        # DriveConstants.java
        [('// DriveConstants.java',CMT_COL)],
        [('public final class ',KW_COL),('DriveConstants',TXT),('{',TXT)],
        [('  public static final double',KW_COL)],
        [('    kSpeedLimit = ',TXT),('0.8',NUM_COL),(';',TXT)],
        [('  public static final double',KW_COL)],
        [('    kDeadband = ',TXT),('0.1',NUM_COL),(';',TXT)],
        [('  public static final int',KW_COL)],
        [('    kLeftMotorPort = ',TXT),('0',NUM_COL),(';',TXT)],
        [('  public static final int',KW_COL)],
        [('    kRightMotorPort = ',TXT),('1',NUM_COL),(';',TXT)],
        [('}',TXT)],
        [('',TXT)],
        # ArmConstants.java
        [('// ArmConstants.java',CMT_COL)],
        [('public final class ',KW_COL),('ArmConstants',TXT),('{',TXT)],
        [('  public static final double',KW_COL)],
        [('    kMaxAngleDeg = ',TXT),('120.0',NUM_COL),(';',TXT)],
        [('  public static final double',KW_COL)],
        [('    kStowedAngleDeg = ',TXT),('5.0',NUM_COL),(';',TXT)],
        [('}',TXT)],
        [('',TXT)],
        # AutoConstants.java
        [('// AutoConstants.java',CMT_COL)],
        [('public final class ',KW_COL),('AutoConstants',TXT),('{',TXT)],
        [('  public static final double',KW_COL)],
        [('    kDriveTimeSeconds = ',TXT),('2.0',NUM_COL),(';',TXT)],
        [('  public static final double',KW_COL)],
        [('    kTurnTimeSeconds = ',TXT),('1.3',NUM_COL),(';',TXT)],
        [('}',TXT)],
        [('',TXT)],
        # OperatorConstants.java
        [('// OperatorConstants.java',CMT_COL)],
        [('public final class ',KW_COL),('OperatorConstants',TXT),('{',TXT)],
        [('  public static final int',KW_COL)],
        [('    kDriverControllerPort = ',TXT),('0',NUM_COL),(';',TXT)],
        [('}',TXT)],
    ]

    lh = 8.6
    code_top = y+avail-BAR_H-PAD
    max_lines = int((code_top-(y+PAD+16))/lh)
    L_draw = L[:max_lines]

    # tip note above code
    note_y = code_top-4
    sf(c,TXT_MED); c.setFont('Helvetica-Oblique',6.5)
    c.drawString(ML+INNER_PAD, note_y,
        'Each class lives in its own file. Start small, add files as subsystems grow.')
    code_top = note_y-6

    code_block(c, ML+INNER_PAD, code_top, COL_W-INNER_PAD*2, L_draw, lh=lh)

    # ── RIGHT: import + usage ──────────────────────────────────────────
    rx = ML+COL_W+GAP
    ry = y+avail-BAR_H-PAD-2
    rw = COL_W-INNER_PAD*2

    LABEL_GAP = 3   # gap between label baseline and top of code block below
    BOX_GAP   = 5   # gap between bottom of code block and next label text

    def rlabel(txt):
        nonlocal ry
        sf(c,TXT_MED); c.setFont('Helvetica-Bold',6.5)
        c.drawString(rx+INNER_PAD, ry, txt)
        ry -= (8+LABEL_GAP)

    def rcode(lines):
        nonlocal ry
        ry = code_block(c, rx+INNER_PAD, ry, rw, lines, lh=9.0) - BOX_GAP

    rlabel('1  Import the constants file')
    rcode([
        [('// top of Drive.java',CMT_COL)],
        [('import ',KW_COL),('frc.robot.DriveConstants',TXT),(';',TXT)],
    ])

    rlabel('2  Use a constant by name')
    rcode([
        [('double speed = DriveConstants',TXT),('.kSpeedLimit;',TXT)],
        [('double dead  = DriveConstants',TXT),('.kDeadband;',TXT)],
    ])

    rlabel('3  OR use the fully-qualified path (no import)')
    rcode([
        [('double speed =',TXT)],
        [('  DriveConstants',KW_COL),('.kSpeedLimit;',TXT)],
    ])

    rlabel('4  Add a constant to an existing file')
    rcode([
        [('// inside DriveConstants.java',CMT_COL)],
        [('public static final double',KW_COL)],
        [('  kMaxTurnSpeed = ',TXT),('0.6',NUM_COL),(';',TXT)],
    ])

    rlabel('5  Create a new constants file')
    rcode([
        [('// new file: ScoopConstants.java',CMT_COL)],
        [('public final class ',KW_COL),('ScoopConstants',TXT),('{',TXT)],
        [('  public static final double',KW_COL)],
        [('    kServoCarryPos = ',TXT),('0.3',NUM_COL),(';',TXT)],
        [('}',TXT)],
    ])

    ry -= 4
    # Ctrl+. tip box — clamped so it never escapes the purple panel
    TIP_PAD = 6
    tip_lines = [
        'Red underline on a class name? Hover it and press',
        'Ctrl+.  \u2192  Add import.  VS Code writes the line for you.',
    ]
    tip_h = TIP_PAD*2 + 9 + len(tip_lines)*9   # pad + title + body lines
    tip_floor = y + TIP_PAD   # must stay inside the purple section box
    if ry - tip_h < tip_floor:
        # shrink: drop to one body line if needed
        tip_lines = ['Hover red underline  \u2192  Ctrl+.  \u2192  Add import.']
        tip_h = TIP_PAD*2 + 9 + len(tip_lines)*9
    if ry - tip_h >= tip_floor:
        tip_box(
            c, rx+INNER_PAD, ry, rw,
            title='\u2605  VS Code quick-fix  (Ctrl+.)',
            body_lines=tip_lines,
            title_col=ORANGE,
            bg_col=rgb('#FFF8E8'),
            bd_col=rgb('#E6C96A'),
            lh=9, pad=TIP_PAD
        )

# ══════════════════════════════════════════════════════════════════════════
# PAGE 2  Section 3 — THE k NAMING RULE  (full width)
# ══════════════════════════════════════════════════════════════════════════
def draw_naming(c,top_y):
    naming_rows=[
        ('Speeds / power',  'kSpeedLimit',               'kMaxTurnSpeed',           'kAutodriveSpeed'),
        ('Angles',          'kMaxAngleDeg',              'kStowedAngleDeg',         'kScoringAngleDeg'),
        ('Distances',       'kWheelCircumferenceMeters', 'kTrackWidthMeters',       'kWheelRadiusMeters'),
        ('Timing',          'kDriveTimeSeconds',         'kTurnTimeSeconds',        'kWaitTimeSeconds'),
        ('Ports / IDs',     'kLeftMotorPort',            'kRightMotorPort',         'kControllerPort'),
        ('Strings',         'kProjectName',              'kAutoDefault',            'kLogPrefix'),
        ('Booleans',        'kIsRightInverted',          'kEnableLogging',          'kIsSimulation'),
    ]
    rules=[
        ('Always start with k',          'speedLimit \u2717',                 'kSpeedLimit \u2713'),
        ('Include unit when ambiguous',   'kMaxAngle \u2717',                  'kMaxAngleDeg \u2713'),
        ('No abbreviations',              'kWC \u2717',                        'kWheelCircumferenceMeters \u2713'),
        ('Drop the class name',           'DriveConstants.kDriveSpeed \u2717', 'DriveConstants.kSpeed \u2713'),
        ('Booleans: kIs or kEnable',      'kMotorInverted \u2717',             'kIsRightMotorInverted \u2713'),
    ]

    row_h=12; rule_h=12
    BOX_PAD = 8   # enforced bottom padding inside warning box
    warn_body = ('A function expecting radians and receiving degrees overshoots by 57\u00d7. '
                 'Unit in the name = free sanity check every time you read the code.')
    # measure warning box height properly
    # two text lines + title + padding
    warn_h = 9 + 9 + 9 + BOX_PAD*2 + 2   # title + 2 body lines + padding

    table_h  = (len(naming_rows)+1)*row_h+4
    rules_h  = (len(rules)+1)*rule_h + 4  # +1 for header row
    h = BAR_H+PAD + 11+4 + table_h + 8 + rules_h + 6 + warn_h + PAD

    y = top_y-h
    section_box(c,ML,y,CW,h,'THE  k  NAMING RULE',PURPLE,PURPLE_LT)

    iy = y+h-BAR_H-PAD-2
    sf(c,TXT); c.setFont('Helvetica',8)
    c.drawString(ML+INNER_PAD, iy,
        'Every WPILib constant: lowercase \u2018k\u2019 + UpperCamelCase. '
        'You\u2019ll see this across every WPILib source file.')
    iy -= 14

    # naming table
    tcols=[ML+INNER_PAD, ML+128, ML+285, ML+420]
    sf(c,PURPLE); c.setLineWidth(0)
    c.rect(ML+INNER_PAD, iy-row_h+3, CW-INNER_PAD*2, row_h-1, fill=1, stroke=0)
    sf(c,WHITE); c.setFont('Helvetica-Bold',7)
    for txt,tx in zip(['Category','Example 1','Example 2','Example 3'],tcols):
        c.drawString(tx+3, iy-row_h+3+3, txt)
    iy -= row_h

    for ri,(cat,e1,e2,e3) in enumerate(naming_rows):
        bg = PURPLE_LT if ri%2==0 else WHITE
        sf(c,bg); c.setLineWidth(0)
        c.rect(ML+INNER_PAD, iy-row_h+3, CW-INNER_PAD*2, row_h-1, fill=1, stroke=0)
        sf(c,TXT);    c.setFont('Helvetica-Bold',7); c.drawString(tcols[0]+3,iy-row_h+3+3,cat)
        sf(c,KW_COL); c.setFont('DVM',6.5)
        c.drawString(tcols[1]+3,iy-row_h+3+3,e1)
        c.drawString(tcols[2]+3,iy-row_h+3+3,e2)
        c.drawString(tcols[3]+3,iy-row_h+3+3,e3)
        iy -= row_h

    iy -= 8
    # rules header
    sf(c,TXT);   c.setFont('Helvetica-Bold',7.5); c.drawString(ML+INNER_PAD,iy,'Rules:')
    sf(c,RED);   c.setFont('Helvetica-Bold',7);   c.drawString(ML+185,iy,'Avoid')
    sf(c,GREEN); c.setFont('Helvetica-Bold',7);   c.drawString(ML+355,iy,'Use instead')
    iy -= rule_h

    for label,bad,good in rules:
        sf(c,TXT);   c.setFont('Helvetica',7);  c.drawString(ML+12,iy,label)
        sf(c,RED);   c.setFont('DVM',6.5);      c.drawString(ML+185,iy,bad)
        sf(c,GREEN); c.setFont('DVM',6.5);      c.drawString(ML+355,iy,good)
        iy -= rule_h

    iy -= 5
    # warning box — use tip_box for enforced padding
    tip_box(
        c, ML+INNER_PAD, iy, CW-INNER_PAD*2,
        title='\u26a0  The unit rule prevents real bugs:',
        body_lines=wrap(c, warn_body, 'Helvetica', 7, CW-INNER_PAD*2-20),
        title_col=ORANGE,
        bg_col=rgb('#FFF8E8'),
        bd_col=rgb('#D4A84B'),
        lh=9, pad=BOX_PAD
    )
    return y

# ══════════════════════════════════════════════════════════════════════════
# PAGE 2  Section 4 — COMMON MISTAKES (left) + IN THE FRC WILD (right)
# ══════════════════════════════════════════════════════════════════════════
def draw_mistakes_wild(c,top_y,bottom_limit):
    avail = top_y-bottom_limit
    y = bottom_limit
    section_box(c,ML,           y,COL_W,avail,'COMMON MISTAKES',ORANGE,ORANGE_LT)
    section_box(c,ML+COL_W+GAP, y,COL_W,avail,'IN THE FRC WILD',TEAL,TEAL_LT)

    AFTER_LINE = 5   # gap between divider line and next title

    # ── LEFT: mistakes ─────────────────────────────────────────────────
    mistakes=[
        ('Magic number in subsystem file',
         [('double speed = ',TXT),('0.8',NUM_COL),(';  ',TXT),('// \u2717 hardcoded',CMT_COL)],
         'Hard to find; one wiring change means hunting across multiple files.'),
        ('Missing static',
         [('public final double',KW_COL),(' kSpeed = ',TXT),('0.8',NUM_COL),(';  ',TXT),('// \u2717',RED)],
         'Requires a Constants() instance. Won\'t compile the way you expect.'),
        ('Missing final',
         [('public static double',KW_COL),(' kSpeed = ',TXT),('0.8',NUM_COL),(';  ',TXT),('// \u2717',RED)],
         'Can be reassigned at runtime. Not a true constant.'),
        ('No unit in name',
         [('kMaxAngle  ',TXT),('// \u2717  vs  ',CMT_COL),('kMaxAngleDeg  ',KW_COL),('// \u2713',CMT_COL)],
         'Caller can\'t tell: degrees or radians? Wrong choice = robot overshoots by 57\u00d7.'),
        ('Moved constant, forgot to update reference',
         [('speed = ',TXT),('0.8',NUM_COL),(';  ',TXT),('// \u2717 still in Drive.java',CMT_COL)],
         'Build fails. Good \u2014 the compiler tells you exactly where to fix it.'),
    ]
    lx = ML+INNER_PAD; lw = COL_W-INNER_PAD*2
    ly = y+avail-BAR_H-PAD-2

    for i,(title,code_toks,desc) in enumerate(mistakes):
        if ly < y+18: break
        sf(c,TXT); c.setFont('Helvetica-Bold',7)
        c.drawString(lx, ly, title); ly -= 9
        cx2 = lx+4
        for text,col in code_toks:
            sf(c,col); c.setFont('DVM',6.5)
            c.drawString(cx2,ly,text); cx2+=c.stringWidth(text,'DVM',6.5)
        ly -= 9
        sf(c,TXT_MED); c.setFont('Helvetica',6.5)
        for ln in wrap(c,desc,'Helvetica',6.5,lw-4):
            if ly<y+14: break
            c.drawString(lx+4,ly,ln); ly-=8
        ly -= 4
        if i < len(mistakes)-1:   # don't draw after last item
            ss(c,RULE); c.setLineWidth(0.35)
            c.line(lx,ly+3,lx+lw,ly+3)
            ly -= AFTER_LINE   # enforced gap after the line

    # ── RIGHT: FRC wild ────────────────────────────────────────────────
    rx = ML+COL_W+GAP+INNER_PAD; ry = y+avail-BAR_H-PAD-2; rw = COL_W-INNER_PAD*2

    sf(c,TXT); c.setFont('Helvetica',7.5)
    intro = ('BearBots starts with one file per subsystem. As codebases grow, '
             'teams add more. Some common ones you\u2019ll see in other FRC repos:')
    for ln in wrap(c,intro,'Helvetica',7.5,rw):
        if ry<y+14: break
        c.drawString(rx,ry,ln); ry-=9
    ry -= 5

    patterns=[
        ('TunerConstants.java',
         'Auto-generated by Phoenix Tuner X for TalonFX motors. Contains PID gains, gear ratios, encoder offsets. Never edit by hand.'),
        ('FieldConstants.java',
         'Field element positions: AprilTag poses, scoring zone coordinates. Used by vision and autonomous routines.'),
        ('VisionConstants.java',
         'Camera transforms, pipeline IDs, trust thresholds, and latency compensation values.'),
        ('OperatorConstants.java',
         'Controller port numbers and deadband values. Already in the BearBots project.'),
        ('Constants.java',
         'Some teams keep a single file with inner classes (DriveConstants, ArmConstants) instead of separate files. Either pattern works \u2014 pick one and stay consistent.'),
    ]

    for fname,desc in patterns:
        if ry<y+16: break
        sf(c,TEAL); c.setFont('DVMB',7)
        c.drawString(rx,ry,fname); ry-=9
        sf(c,TXT_MED); c.setFont('Helvetica',6.5)
        for ln in wrap(c,desc,'Helvetica',6.5,rw):
            if ry<y+10: break
            c.drawString(rx+4,ry,ln); ry-=8
        ry -= 4

    if ry>y+16:
        ry -= 2
        sf(c,TXT_MED); c.setFont('Helvetica-Oblique',6.5)
        closing = ('Pattern matters more than file count. Pick one and stay consistent.')
        for ln in wrap(c,closing,'Helvetica-Oblique',6.5,rw):
            if ry<y+8: break
            c.drawString(rx,ry,ln); ry-=8

# ══════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════
def build():
    out='/mnt/user-data/outputs/BearBots_Constants_Reference.pdf'
    c=canvas.Canvas(out,pagesize=letter)

    avail_top    = H-MT-HDR_H-SGAP
    avail_bottom = MB+FOOTER_H+SGAP

    # Page 1
    draw_header(c,H-MT,page=1)
    draw_footer(c)
    s1_bot = draw_declaration(c,avail_top)
    draw_structure_usage(c, s1_bot-SGAP, avail_bottom)

    # Page 2
    c.showPage()
    draw_header(c,H-MT,page=2)
    draw_footer(c)
    s3_bot = draw_naming(c,avail_top)
    draw_mistakes_wild(c, s3_bot-SGAP, avail_bottom)

    c.save()
    print(f'Saved: {out}')

build()
