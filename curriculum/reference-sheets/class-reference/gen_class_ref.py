"""
BearBots FRC Team 6964
Java Class Structure & AdvantageKit Reference — PDF Generator
Landscape US Letter, color-coded code blocks by class section category
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

pdfmetrics.registerFont(TTFont('Mono',  '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'))
pdfmetrics.registerFont(TTFont('MonoB', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Sans',  '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('SansB', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

W, H = landscape(letter)   # 792 x 612
ML   = 0.45 * inch
MR   = 0.45 * inch
MT   = 0.40 * inch
MB   = 0.35 * inch
CW   = W - ML - MR         # ~727 pt

HDR_BG     = HexColor('#1C2541')
HDR_TXT    = HexColor('#FFFFFF')
SUB_TXT    = HexColor('#A8B4CC')
FOOTER_BG  = HexColor('#1C2541')
RULE_COLOR = HexColor('#CCCCCC')
BODY_TXT   = HexColor('#1A1A2E')

CAT = {
    'shell':       (HexColor('#2B2D42'), HexColor('#EEEEF4'), 'Class Shell'),
    'field':       (HexColor('#1A508B'), HexColor('#E8F0FE'), 'Fields'),
    'constructor': (HexColor('#7A4100'), HexColor('#FEF3E2'), 'Constructor'),
    'method':      (HexColor('#1A5C38'), HexColor('#E8F5EE'), 'Methods'),
    'akit':        (HexColor('#005F5F'), HexColor('#E2F0F0'), 'AKit Infrastructure'),
    'io':          (HexColor('#4A2080'), HexColor('#EEE8F8'), 'IO / Delegation'),
    'comment':     (HexColor('#666666'), HexColor('#F5F5F5'), 'Comments'),
    'viz':         (HexColor('#7A3000'), HexColor('#FDF0E8'), 'Visualization'),
}

HDR_H   = 52
FOOT_H  = 22
CODE_FS = 7.0
CODE_LH = 10.5
GAP     = 10   # column gap

def content_top():    return H - MT - HDR_H - 10
def content_bottom(): return MB + FOOT_H + 8
def avail_h():        return content_top() - content_bottom()  # 466 pt

# ── Drawing helpers ───────────────────────────────────────────────────────────
def draw_header(c, title, subtitle, page_num, total_pages):
    x, y = ML, H - MT - HDR_H
    c.setFillColor(HDR_BG); c.roundRect(x, y, CW, HDR_H, 5, fill=1, stroke=0)
    c.setFillColor(HDR_TXT); c.setFont('SansB', 13)
    c.drawString(x+12, y+HDR_H-22, title)
    c.setFillColor(SUB_TXT); c.setFont('Sans', 8)
    c.drawString(x+12, y+10, subtitle)
    c.setFont('Sans', 7.5)
    c.drawRightString(x+CW-12, y+10, f'Page {page_num} of {total_pages}')

def draw_footer(c, left_text):
    x, y = ML, MB
    c.setFillColor(FOOTER_BG); c.roundRect(x, y, CW, FOOT_H, 4, fill=1, stroke=0)
    c.setFillColor(HDR_TXT); c.setFont('Sans', 7)
    c.drawString(x+10, y+7, left_text)
    c.drawRightString(x+CW-10, y+7, 'BearBots FRC Team 6964')

def draw_col_header(c, x, y, w, label):
    c.setFont('SansB', 9); c.setFillColor(HDR_BG)
    c.drawString(x, y, label)
    c.setStrokeColor(HDR_BG); c.setLineWidth(0.75)
    c.line(x, y-2, x+w, y-2)

def draw_code_block(c, x, y, w, lines):
    pad_x, pad_y = 8, 0
    cur_y = y - pad_y
    for cat_key, text in lines:
        bar_color, fill_color, _ = CAT[cat_key]
        line_y = cur_y - CODE_LH
        c.setFillColor(fill_color); c.rect(x, line_y, w, CODE_LH, fill=1, stroke=0)
        c.setFillColor(bar_color);  c.rect(x, line_y, 3, CODE_LH, fill=1, stroke=0)
        c.setFillColor(bar_color);  c.setFont('Mono', CODE_FS)
        c.drawString(x+pad_x, line_y+2.5, text)
        cur_y = line_y
    block_h = y - pad_y - cur_y + pad_y
    c.setStrokeColor(RULE_COLOR); c.setLineWidth(0.75)
    c.rect(x, cur_y, w, block_h+pad_y, fill=0, stroke=1)
    return cur_y

def draw_callout_box(c, x, y, w, cat_key, title, lines):
    bar_color, fill_color, _ = CAT[cat_key]
    box_h = len(lines)*10 + 22
    if y - box_h < content_bottom() + 6:
        return y
    c.setFillColor(fill_color); c.setStrokeColor(bar_color); c.setLineWidth(0.75)
    c.roundRect(x, y-box_h, w, box_h, 4, fill=1, stroke=1)
    c.setFillColor(bar_color)
    c.roundRect(x, y-14, w, 18, 4, fill=1, stroke=0)
    c.rect(x, y-14, w, 4, fill=1, stroke=0)
    c.setFillColor(HexColor('#FFFFFF')); c.setFont('SansB', 6.5)
    c.drawString(x+6, y-10, title)
    c.setFillColor(bar_color); c.setFont('Sans', 6.5)
    for i, ln in enumerate(lines):
        c.drawString(x+6, y-14-(i+1)*10, ln)
    return y - box_h - 6

def draw_legend(c, x, y, w):
    items = list(CAT.values())
    item_w = w / len(items); box_size = 8
    c.setFont('Sans', 6)
    for i, (bar_c, fill_c, label) in enumerate(items):
        ix = x + i*item_w
        c.setFillColor(fill_c); c.setStrokeColor(bar_c); c.setLineWidth(0.75)
        c.rect(ix+2, y, box_size, box_size, fill=1, stroke=1)
        c.setFillColor(bar_c); c.rect(ix+2, y, 2.5, box_size, fill=1, stroke=0)
        c.setFillColor(BODY_TXT)
        c.drawString(ix+2+box_size+3, y+1.5, label)

def draw_table(c, x, y, w, headers, rows, col_widths, row_h=13):
    hdr_h = 15
    c.setFillColor(HDR_BG); c.rect(x, y-hdr_h, w, hdr_h, fill=1, stroke=0)
    c.setFillColor(HDR_TXT); c.setFont('SansB', 7)
    cx = x+5
    for i, h in enumerate(headers):
        c.drawString(cx, y-hdr_h+4, h); cx += col_widths[i]
    cur_y = y - hdr_h
    for ri, row in enumerate(rows):
        bg = HexColor('#F0F4F8') if ri%2==0 else HexColor('#FFFFFF')
        c.setFillColor(bg); c.setStrokeColor(RULE_COLOR); c.setLineWidth(0.4)
        c.rect(x, cur_y-row_h, w, row_h, fill=1, stroke=1)
        c.setFillColor(BODY_TXT); cx = x+5
        for ci, cell in enumerate(row):
            c.setFont('Sans', 6.5)
            c.drawString(cx, cur_y-row_h+3.5, str(cell)); cx += col_widths[ci]
        cur_y -= row_h
    return cur_y

# ── Page 1: Java Primer ───────────────────────────────────────────────────────
# col_w=261pt => ~59 chars. Max lines per col = 44 to stay within 466pt.

PRIMER_LEFT = [
    ('comment',     '// An interface declares WHAT a class must do, not HOW.'),
    ('comment',     '// Implementors must provide all non-default methods.'),
    ('shell',       'public interface Soundable {'),
    ('io',          '  void makeSound();'),
    ('comment',     '    // no body — implementor decides'),
    ('io',          '  default void breathe() {'),
    ('comment',     '    // default = optional to override'),
    ('io',          '    System.out.println("breathing");'),
    ('io',          '  }'),
    ('shell',       '}'),
    ('comment',     '// A class bundles data (fields) and behavior (methods).'),
    ('shell',       'public class Animal {'),
    ('comment',     ''),
    ('field',       '  private String name;'),
    ('comment',     '    // private: only accessible inside Animal'),
    ('field',       '  private int    age;'),
    ('field',       '  public static int count = 0;'),
    ('comment',     '    // static: one copy shared by ALL instances'),
    ('field',       '  public final  String species;'),
    ('comment',     '    // final: assigned once, never changed'),
    ('comment',     '  // Constructor: runs once on new Animal(...)'),
    ('constructor', '  public Animal(String name, int age, String species) {'),
    ('constructor', '    this.name    = name;'),
    ('comment',     '      // this.name = field, name = parameter'),
    ('constructor', '    this.age     = age;'),
    ('constructor', '    this.species = species;'),
    ('constructor', '    count++;'),
    ('comment',     '      // increment shared counter'),
    ('constructor', '  }'),
    ('method',      '  public String getName() {'),
    ('method',      '    return name;  // getter: reads a private field'),
    ('method',      '  }'),
    ('method',      '  public void birthday() {'),
    ('method',      '    age++;  // void: returns nothing'),
    ('method',      '  }'),
    ('method',      '  public String describe() {'),
    ('comment',     '    // can be overridden by subclasses'),
    ('method',      '    return name + " is a " + species;'),
    ('method',      '  }'),
    ('shell',       '}'),
]  # 45 lines — fits in 466pt (45*10.5+8 = 480.5... trim 1 more)

# trim the blank line after constructor closing brace — saves 1 line => 44 lines = 470pt
# Actually let's reduce CODE_LH slightly for primer only, or just accept 45 is close.
# 45 lines * 10.5 + 8 = 480.5 > 466. Need 44 lines max.
# Remove one blank comment line:

PRIMER_LEFT = [l for i,l in enumerate(PRIMER_LEFT) if not (l == ('comment','') and i in [13,21])]
# That removes 2 blank lines => 43 lines = 459.5pt. Good.

PRIMER_RIGHT = [
    ('comment',     '// extends: Dog IS-A Animal'),
    ('comment',     '// implements: Dog fulfills the Soundable contract'),
    ('shell',       'public class Dog extends Animal implements Soundable {'),
    ('comment',     ''),
    ('field',       '  private String breed;'),
    ('comment',     '    // Dog-specific field'),
    ('constructor', '  public Dog(String name, int age, String breed) {'),
    ('constructor', '    super(name, age, "Dog");'),
    ('comment',     '      // calls Animal constructor first'),
    ('constructor', '    this.breed = breed;'),
    ('constructor', '  }'),
    ('comment',     '  // @Override: compiler checks method exists in Animal'),
    ('method',      '  @Override'),
    ('method',      '  public String describe() {'),
    ('method',      '    return super.describe() + ", breed: " + breed;'),
    ('method',      '  }'),
    ('comment',     '  // Required by Soundable — must be provided'),
    ('method',      '  @Override'),
    ('method',      '  public void makeSound() {'),
    ('method',      '    System.out.println("Woof!");'),
    ('method',      '  }'),
    ('comment',     '  // breathe() not overridden — uses Soundable default'),
    ('shell',       '}'),
    ('comment',     ''),
    ('comment',     '// Using the classes'),
    ('method',      'Animal a = new Animal("Felix", 3, "Cat");'),
    ('method',      'Dog    d = new Dog("Rex", 5, "Labrador");'),
    ('method',      'Animal r = new Dog("Buddy", 2, "Poodle");'),
    ('comment',     '  // Dog IS-A Animal — valid assignment'),
    ('comment',     ''),
    ('method',      'System.out.println(a.describe());'),
    ('comment',     '  // Felix is a Cat'),
    ('method',      'System.out.println(d.describe());'),
    ('comment',     '  // Rex is a Dog, breed: Labrador'),
    ('method',      'd.makeSound();'),
    ('comment',     '  // Woof!'),
    ('method',      'd.breathe();'),
    ('comment',     '  // breathing  (from default)'),
    ('method',      'System.out.println(Animal.count);'),
    ('comment',     '  // 3  (static field, shared by all)'),
]  # 43 lines = 459.5pt. Fits.

PRIMER_CALLOUTS = [
    ('shell',       'Class Declaration',
     ['public class Name { }',
      'public = accessible from other files',
      'Filename must match class name exactly']),
    ('field',       'Fields',
     ['private = only this class can read/write',
      'static  = one copy shared by all instances',
      'final   = assigned once, never reassigned',
      'static final = constant (team standard: prefix k)']),
    ('constructor', 'Constructor',
     ['Runs once when you write new ClassName(...)',
      'this.field = field disambiguates from parameter',
      'super(...) calls the parent class constructor']),
    ('method',      'Methods',
     ['void = returns nothing',
      'String/int/etc. = must return that type',
      'public/private controls who can call it']),
    ('shell',       'extends (one parent only)',
     ['Dog IS-A Animal: inherits all fields and methods',
      'Use @Override to replace a parent method',
      'super.method() calls the parent version']),
    ('io',          'implements (multiple allowed)',
     ['Promises to provide all interface methods',
      'default methods are optional to override',
      'A class can implement multiple interfaces']),
    ('comment',     'Annotations',
     ['Metadata read by the compiler or build tools',
      '@Override verifies method exists in parent',
      'Other annotations can trigger code generation']),
]  # total = 7*(3*10+22+6) = 7*64 = 448pt. Fits 466pt.

def page_primer(c):
    draw_header(c, 'Java Class Primer',
        'Class anatomy: fields, constructor, methods, extends, implements, annotations',
        1, 4)
    draw_footer(c, 'Part 1 of 4: Java Fundamentals')

    y = content_top()

    callout_w = CW * 0.245
    code_w    = (CW - callout_w - GAP*2) / 2
    lx = ML
    rx = ML + code_w + GAP
    cx = ML + code_w*2 + GAP*2

    draw_col_header(c, lx, y, code_w,    'Interface + Base Class')
    draw_col_header(c, rx, y, code_w,    'Subclass + Usage')
    draw_col_header(c, cx, y, callout_w, 'Concept Callouts')
    y -= 14

    draw_code_block(c, lx, y, code_w, PRIMER_LEFT)
    draw_code_block(c, rx, y, code_w, PRIMER_RIGHT)

    ny = y
    for cat_key, title, lines in PRIMER_CALLOUTS:
        ny = draw_callout_box(c, cx, ny, callout_w, cat_key, title, lines)

    draw_legend(c, ML, content_bottom() + 4, CW)


# ── Page 2: IO Layer ──────────────────────────────────────────────────────────
# col_w = (727-12)/2 = 357pt => ~82 chars

ARM_CODE = [
    ('comment',     '// ArmConstants.java — static constants only, no logic'),
    ('shell',       'public final class ArmConstants {'),
    ('field',       '  public static final double kMinAngleDeg    = 0.0;'),
    ('field',       '  public static final double kMaxAngleDeg    = 180.0;'),
    ('field',       '  public static final double kStowedAngleDeg = 180.0;'),
    ('field',       '  public static final double kLowAngleDeg    = 135.0;'),
    ('field',       '  public static final double kHighAngleDeg   = 90.0;'),
    ('shell',       '}'),
    ('comment',     ''),
    ('comment',     '// ArmIO.java — interface: what any ArmIO must do'),
    ('shell',       'public interface ArmIO {'),
    ('akit',        '  @AutoLog'),
    ('comment',     '    // generates ArmIOInputsAutoLogged at compile time'),
    ('akit',        '  public static class ArmIOInputs {'),
    ('akit',        '    public double commandedAngleDeg = kStowedAngleDeg;'),
    ('akit',        '  }'),
    ('comment',     ''),
    ('io',          '  public default void updateInputs(ArmIOInputs inputs) {}'),
    ('comment',     '    // empty body = safe no-op for replay'),
    ('io',          '  public default void setAngle(double angleDeg) {}'),
    ('shell',       '}'),
    ('comment',     ''),
    ('comment',     '// ArmIOXRP.java — hardware implementation'),
    ('shell',       'public class ArmIOXRP implements ArmIO {'),
    ('field',       '  private final XRPServo armServo ='),
    ('field',       '      new XRPServo(kArmServoDeviceNumber);'),
    ('field',       '  private double commandedAngleDeg = ArmConstants.kStowedAngleDeg;'),
    ('comment',     '    // tracked here; servo has no position sensor'),
    ('comment',     ''),
    ('method',      '  @Override'),
    ('method',      '  public void updateInputs(ArmIOInputs inputs) {'),
    ('akit',        '    inputs.commandedAngleDeg = commandedAngleDeg;'),
    ('method',      '  }'),
    ('comment',     ''),
    ('method',      '  @Override'),
    ('method',      '  public void setAngle(double angleDeg) {'),
    ('field',       '    commandedAngleDeg = angleDeg;'),
    ('method',      '    armServo.setAngle(angleDeg);'),
    ('method',      '  }'),
    ('shell',       '}'),
]  # 41 lines = 438.5pt. Fits.

SIM_CODE = [
    ('comment',     '// ArmIOSim.java — simulation implementation'),
    ('comment',     '// Symmetric with ArmIOXRP: no physics for servo'),
    ('shell',       'public class ArmIOSim implements ArmIO {'),
    ('field',       '  private double commandedAngleDeg = ArmConstants.kStowedAngleDeg;'),
    ('method',      '  @Override'),
    ('method',      '  public void updateInputs(ArmIOInputs inputs) {'),
    ('akit',        '    inputs.commandedAngleDeg = commandedAngleDeg;'),
    ('method',      '  }'),
    ('method',      '  @Override'),
    ('method',      '  public void setAngle(double angleDeg) {'),
    ('field',       '    commandedAngleDeg = angleDeg;'),
    ('method',      '  }'),
    ('shell',       '}'),
]  # 14 lines

ROBOT_CONTAINER_CODE = [
    ('comment',     '// RobotContainer.java — IO selection only'),
    ('shell',       'public class RobotContainer {'),
    ('field',       '  private final Drive drive;'),
    ('field',       '  private final Arm arm;'),
    ('field',       '  private final LoggedDashboardChooser<Command> autoChooser'),
    ('field',       '      = new LoggedDashboardChooser<>("Auto Choices"); // replaces SendableChooser'),
    ('constructor', '  public RobotContainer() {'),
    ('constructor', '    switch (Constants.currentMode) {'),
    ('constructor', '      case REAL:'),
    ('comment',     '        // physical XRP hardware'),
    ('io',          '        drive = new Drive(new DriveIOXRP());'),
    ('io',          '        arm   = new Arm(new ArmIOXRP());   break;'),
    ('constructor', '      case SIM:'),
    ('comment',     '        // WPILib simulator'),
    ('io',          '        drive = new Drive(new DriveIOSim());'),
    ('io',          '        arm   = new Arm(new ArmIOSim());   break;'),
    ('constructor', '      default:'),
    ('comment',     '        // log replay — anonymous empty impl'),
    ('io',          '        drive = new Drive(new DriveIO() {});'),
    ('io',          '        arm   = new Arm(new ArmIO() {});   break;'),
    ('constructor', '    }'),
    ('constructor', '    configureButtonBindings(); configureAutonomous();'),
    ('constructor', '  }'),
    ('shell',       '}'),
]  # 27 lines. SIM+RC = 40 lines = 428pt. Fits.

def page1(c):
    draw_header(c, 'Java Class Structure & AdvantageKit Reference',
        'IO Layer: ArmIO interface, ArmIOXRP implementation, ArmIOSim, RobotContainer wiring',
        2, 4)
    draw_footer(c, 'Part 2 of 4: IO Layer')

    y = content_top()
    col_w = (CW - GAP) / 2
    lx = ML
    rx = ML + col_w + GAP

    draw_col_header(c, lx, y, col_w, 'IO Interface + Hardware Implementation')
    draw_col_header(c, rx, y, col_w, 'Simulation Implementation + Wiring')
    y -= 14

    draw_code_block(c, lx, y, col_w, ARM_CODE)

    ry = y
    ry = draw_code_block(c, rx, ry, col_w, SIM_CODE)
    # Gap so RC block bottom aligns with left column bottom
    left_bottom = y - 14 - len(ARM_CODE) * CODE_LH
    right_remaining = len(ROBOT_CONTAINER_CODE) * CODE_LH + 14 + 8
    rc_gap = max(ry - right_remaining - left_bottom, 10)
    ry -= rc_gap
    draw_col_header(c, rx, ry, col_w, 'RobotContainer — IO Selection')
    ry -= 8
    draw_code_block(c, rx, ry, col_w, ROBOT_CONTAINER_CODE)

    draw_legend(c, ML, content_bottom() + 4, CW)


# ── Page 3: Arm.java subsystem ────────────────────────────────────────────────
# Split ARM_SUBSYSTEM_CODE into two code cols + callout col
# code_w = CW*0.36 = 262pt => ~59 chars, max 43 lines each
# callout_w = CW*0.28 = 204pt => ~46 chars

ARM_SUB_LEFT = [
    ('comment',     '// Arm.java — the subsystem'),
    ('shell',       'public class Arm extends SubsystemBase {'),
    ('comment',     ''),
    ('comment',     '  // ── AKit infrastructure (required) ──'),
    ('akit',        '  private final ArmIO io;'),
    ('akit',        '  private final ArmIOInputsAutoLogged inputs'),
    ('akit',        '      = new ArmIOInputsAutoLogged();'),
    ('comment',     ''),
    ('comment',     '  // ── Control math (motor-driven subsystems) ──'),
    ('comment',     '  // private final ProfiledPIDController controller'),
    ('comment',     '  //   = new ProfiledPIDController(kP, 0, kD,'),
    ('comment',     '  //       new TrapezoidProfile.Constraints('),
    ('comment',     '  //           kMaxVelDegPerSec, kMaxAccelDegPerSec));'),
    ('comment',     '  // private final ArmFeedforward feedforward'),
    ('comment',     '  //   = new ArmFeedforward(kS, kG, kV);'),
    ('comment',     ''),
    ('comment',     '  // ── State tracking ──'),
    ('field',       '  // @AutoLogOutput'),
    ('field',       '  // private double setpointDeg = 0.0;'),
    ('comment',     '      // logs automatically every loop'),
    ('comment',     ''),
    ('comment',     '  // ── WPILib utilities ──'),
    ('comment',     '  // private final Alert encoderAlert = new Alert('),
    ('comment',     '  //     "Arm encoder disconnected.", AlertType.kError);'),
    ('comment',     ''),
    ('comment',     '  // ── Visualization ──'),
    ('viz',         '  private final LoggedMechanism2d mechanism'),
    ('viz',         '      = new LoggedMechanism2d(3, 3);'),
    ('viz',         '  private final LoggedMechanismRoot2d root'),
    ('viz',         '      = mechanism.getRoot("ArmPivot", 1.2, 0.18);'),
    ('viz',         '  private final LoggedMechanismLigament2d armLigament'),
    ('viz',         '      = root.append(new LoggedMechanismLigament2d('),
    ('viz',         '          "Arm", feetToMeters(3), 0));'),
    ('viz',         '  private Pose3d componentPose = new Pose3d();'),
    ('comment',     ''),
    ('constructor', '  public Arm(ArmIO io) { this.io = io; }'),
    ('comment',     '    // IO impl chosen by RobotContainer'),
]  # 35 lines = 375.5pt. Fits.

ARM_SUB_RIGHT = [
    ('method',      '  @Override'),
    ('method',      '  public void periodic() {'),
    ('akit',        '    io.updateInputs(inputs);'),
    ('comment',     '      // always first'),
    ('akit',        '    Logger.processInputs("Arm", inputs);'),
    ('comment',     '      // always second'),
    ('comment',     ''),
    ('viz',         '    armLigament.setAngle(180 - inputs.commandedAngleDeg);'),
    ('viz',         '    Logger.recordOutput("Arm/Mechanism2d", mechanism);'),
    ('viz',         '    componentPose = new Pose3d('),
    ('viz',         '        -0.052, 0.007, 0.0645, new Rotation3d('),
    ('viz',         '        0, toRadians(inputs.commandedAngleDeg), 0));'),
    ('comment',     ''),
    ('comment',     '    // Motor-driven subsystems run PID+FF here:'),
    ('comment',     '    // double pid = controller.calculate('),
    ('comment',     '    //     inputs.positionDeg, setpointDeg);'),
    ('comment',     '    // double ff = feedforward.calculate('),
    ('comment',     '    //     controller.getSetpoint().position,'),
    ('comment',     '    //     controller.getSetpoint().velocity);'),
    ('comment',     '    // io.setVoltage(pid + ff);'),
    ('method',      '  }'),
    ('comment',     ''),
    ('comment',     '  // Clamp at subsystem boundary'),
    ('method',      '  public void setAngle(double angleDeg) {'),
    ('method',      '    double clamped = MathUtil.clamp(angleDeg,'),
    ('method',      '        ArmConstants.kMinAngleDeg,'),
    ('method',      '        ArmConstants.kMaxAngleDeg);'),
    ('io',          '    io.setAngle(clamped);'),
    ('comment',     '      // delegate to IO; never call hardware directly'),
    ('akit',        '    Logger.recordOutput("Arm/Commanded/AngleDeg", clamped);'),
    ('method',      '  }'),
    ('comment',     ''),
    ('method',      '  public void stop() {'),
    ('method',      '    setAngle(ArmConstants.kStowedAngleDeg);'),
    ('method',      '  }'),
    ('method',      '  public double getCommandedAngleDeg() {'),
    ('method',      '    return inputs.commandedAngleDeg;'),
    ('method',      '  }'),
    ('shell',       '}'),
]  # 39 lines = 417.5pt. Fits.

ARM_CALLOUTS = [
    ('akit',        'AKit Infrastructure',
     ['ArmIO io — interface reference injected via constructor.',
      'ArmIOInputsAutoLogged — generated class from @AutoLog.',
      'Never use ArmIOInputs directly in the subsystem.']),
    ('comment',     'Control Math (commented out)',
     ['ProfiledPIDController + feedforward belong here',
      'for any motor-driven subsystem.',
      'Drive will implement this in a later lesson.']),
    ('viz',         'Visualization',
     ['LoggedMechanism2d renders arm in AdvantageScope.',
      'Logger.recordOutput() for computed/derived values.',
      'FinalComponentPoses drives the 3D robot model.']),
    ('constructor', 'Constructor Rule',
     ['Subsystem does not know if it is REAL, SIM, or REPLAY.',
      'RobotContainer injects the correct IO implementation.']),
    ('akit',        'periodic() — always in this order',
     ['1. io.updateInputs(inputs)',
      '2. Logger.processInputs("Arm", inputs)',
      '3. All logic reads from inputs.*, never hardware']),
    ('io',          'IO Delegation Rule',
     ['io.setAngle() executes the command.',
      'The IO layer never decides — it only executes.',
      'Clamping belongs at the subsystem boundary.']),
    ('akit',        'inputs.commandedAngleDeg',
     ['Written by IO impl in updateInputs(),',
      'not by the subsystem directly.',
      'IO tracks it; subsystem reads inputs.*.']),
]  # 7*(3*10+22+6) = 448pt. Fits.

def page2(c):
    draw_header(c, 'Java Class Structure & AdvantageKit Reference',
        'The Subsystem: Arm.java with all class categories annotated',
        3, 4)
    draw_footer(c, 'Part 3 of 4: The Subsystem')

    y = content_top()

    callout_w = CW * 0.28
    code_w    = (CW - callout_w - GAP*2) / 2
    lx = ML
    rx = ML + code_w + GAP
    cx = ML + code_w*2 + GAP*2

    draw_col_header(c, lx, y, code_w,    'Arm.java — Fields, Constructor')
    draw_col_header(c, rx, y, code_w,    'Arm.java — Methods')
    draw_col_header(c, cx, y, callout_w, 'Callouts')
    y -= 14

    draw_code_block(c, lx, y, code_w, ARM_SUB_LEFT)
    draw_code_block(c, rx, y, code_w, ARM_SUB_RIGHT)

    ny = y
    for cat_key, title, lines in ARM_CALLOUTS:
        ny = draw_callout_box(c, cx, ny, callout_w, cat_key, title, lines)

    draw_legend(c, ML, content_bottom() + 4, CW)


# ── Page 4: Reference tables ──────────────────────────────────────────────────
WHERE_LOGIC_HEADERS = ['What', 'File']
WHERE_LOGIC_ROWS = [
    ('Hardware objects (motors, servos, sensors)',  'ArmIOXRP.java only'),
    ('Unit conversion (volts to motor %)',          'ArmIOXRP.java only'),
    ('Sensor reading / updateInputs()',             'ArmIOXRP.java (impl); ArmIO.java (sig)'),
    ('Reading sensor state in subsystem logic',     'inputs.* in Arm.java'),
    ('PIDController / ProfiledPIDController',       'Arm.java'),
    ('Feedforward (ArmFeedforward, etc.)',          'Arm.java'),
    ('@AutoLogOutput state fields',                 'Arm.java'),
    ('Timer, Alert',                               'Arm.java'),
    ('Clamping / safety logic',                    'Arm.java (subsystem boundary)'),
    ('Coordinating two subsystems',                'Command class only'),
    ('Choosing REAL vs SIM vs REPLAY',             'RobotContainer constructor'),
    ('Port numbers, setpoints, PID gains',         'ArmConstants.java'),
    ('Logger.start()',                             'Robot.robotInit() — line 1'),
    ('CommandScheduler.getInstance().run()',        'Robot.robotPeriodic()'),
]

KEY_TYPES_HEADERS = ['Type', 'Package', 'What it does']
KEY_TYPES_ROWS = [
    ('LoggedRobot',           'o.l.junction',          'Replaces TimedRobot as Robot.java base class'),
    ('Logger',                'o.l.junction',          'start(), processInputs(), recordOutput()'),
    ('SubsystemBase',         'e.w.f.wpilibj2.command','WPILib base; registers periodic() each loop'),
    ('@AutoLog',              'o.l.j.autolog',         'On inputs class; generates *AutoLogged'),
    ('@AutoLogOutput',        'o.l.junction',          'On subsystem field; auto-logs as output every loop'),
    ('@Override',             'Java built-in',         'Verifies method exists in parent/interface'),
    ('PIDController',         'e.w.f.math.controller', 'Feedback control for velocity or position'),
    ('ProfiledPIDController', 'e.w.f.math.controller', 'PID + trapezoidal motion profile'),
    ('SimpleMotorFeedforward','e.w.f.math.controller', 'Feedforward for flywheels and drive wheels'),
    ('ArmFeedforward',        'e.w.f.math.controller', 'Feedforward for rotating arms (gravity-aware)'),
    ('ElevatorFeedforward',   'e.w.f.math.controller', 'Feedforward for vertical elevators'),
    ('LoggedDashboardChooser','o.l.j.networktables',   'Logged replacement for SendableChooser'),
    ('Timer',                 'e.w.f.wpilibj',         'Timing events inside a subsystem'),
    ('Alert',                 'e.w.f.wpilibj',         'Persistent fault notification in DS + AScope'),
]

MISTAKES_ROWS = [
    ('Logger.getInstance().start()',       'Logger.start()  —  static method, no getInstance'),
    ('ArmIOInputs in Arm.java',            'Use ArmIOInputsAutoLogged (compiler-generated class)'),
    ('commandedAngleDeg = x in subsystem', 'Track in IO impl; subsystem reads via inputs.*'),
    ('Hardware objects in Arm.java',       'Hardware only in ArmIOXRP.java'),
    ('PIDController in ArmIOXRP.java',     'Control math belongs in Arm.java'),
    ('Clamping inside IO setAngle()',       'Clamp at subsystem boundary; IO just executes'),
    ('updateInputs() after logic',         'Must be the first two lines of periodic()'),
    ('SendableChooser for auto',           'Use LoggedDashboardChooser — selection is an input'),
    ('Subsystem coord in periodic()',      'Move coordination logic into a Command class'),
]

def page3(c):
    draw_header(c, 'Java Class Structure & AdvantageKit Reference',
        'Where Logic Lives + Key Types Cheat Sheet + Common Mistakes',
        4, 4)
    draw_footer(c, 'Part 4 of 4: Reference Tables')

    y = content_top()
    col_w = (CW - GAP) / 2
    lx = ML
    rx = ML + col_w + GAP

    # ── Left column: Where Logic Lives stacked above Key Types ────────────────
    draw_col_header(c, lx, y, col_w, 'Where Logic Lives')
    ly = y - 14
    ly = draw_table(c, lx, ly, col_w,
                    WHERE_LOGIC_HEADERS, WHERE_LOGIC_ROWS,
                    [col_w*0.52, col_w*0.48], row_h=13)
    ly -= 24
    draw_col_header(c, lx, ly, col_w, 'Key Types Cheat Sheet')
    ly -= 14
    draw_table(c, lx, ly, col_w,
               KEY_TYPES_HEADERS, KEY_TYPES_ROWS,
               [col_w*0.26, col_w*0.23, col_w*0.51], row_h=13)

    # ── Right column: Common Mistakes ─────────────────────────────────────────
    draw_col_header(c, rx, y, col_w, 'Common Mistakes')
    ry = y - 14
    draw_table(c, rx, ry, col_w,
               ['Mistake', 'Fix'],
               MISTAKES_ROWS,
               [col_w*0.38, col_w*0.62], row_h=13)


# ── Main ──────────────────────────────────────────────────────────────────────
OUT = '/mnt/user-data/outputs/BearBots_ClassReference.pdf'
c = canvas.Canvas(OUT, pagesize=landscape(letter))
c.setTitle('BearBots FRC Team 6964 — Java Class Structure & AdvantageKit Reference')

page_primer(c); c.showPage()
page1(c);       c.showPage()
page2(c);       c.showPage()
page3(c);       c.showPage()

c.save()
print(f'Saved: {OUT}')
