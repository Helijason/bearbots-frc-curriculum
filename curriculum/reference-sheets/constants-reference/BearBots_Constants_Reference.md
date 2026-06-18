# BearBots Constants Quick Reference — Content Variables
# Source of truth for BearBots_Constants_Reference.pdf
# Layout and geometry live in gen_constants_ref.py
# Update this file when content changes, then regenerate the PDF.

---

## HEADER

title       = "Constants Quick Reference"
subtitle    = "BEARBOTS TEAM 6964  —  FRC PROGRAMMING CURRICULUM"
stack_line  = "Java  |  WPILib  |  XRP"
keep_line   = "Keep this. Add it to your binder."
pages       = 2

---

## FOOTER

footer_left  = "BearBots FRC — Constants Quick Reference"
footer_right = "public static final — define once, use everywhere"

---

## PAGE 1

---

### Section 1 — THE DECLARATION RECIPE  (full width, teal)

intro = "Every constant uses three keywords before the type and name:"

example_line = "public static final double  kSpeedLimit  =  0.8 ;"
# public = teal, static = purple, final = orange (colour-coded in PDF)

#### Keyword bullets

bullets = [
    ("public",  "any file in the project can read it"),
    ("static",  "belongs to the class itself; no new Constants() required"),
    ("final",   "value is locked at startup and can never be reassigned"),
]

#### Why not the other keywords? (callout box, teal)

callout = [
    "private makes a constant unreadable from other files — defeats the purpose.",
    "No static means you need an object instance to read it — no new Constants() needed.",
    "No final means the value can be overwritten at runtime — it becomes a variable, not a constant.",
]

#### Type table

# Columns: Type | Meaning | BearBots example | Common uses in FRC

type_rows = [
    ("double",  "64-bit decimal",  "kSpeedLimit = 0.8",          "Speeds, distances, PID gains, voltages"),
    ("int",     "Whole number",    "kLeftMotorPort = 0",          "Port numbers, CAN IDs, counts"),
    ("String",  "Text",            'kProjectName = "BearBots"',   "Logger keys, auto mode names"),
    ("boolean", "True / false",    "kIsRightInverted = true",     "Inversion flags, feature toggles"),
    ("long",    "64-bit integer",  "kLoopPeriodUs = 20_000L",     "Microsecond timestamps, large counts"),
    ("float",   "32-bit decimal",  "kGearRatio = 6.75f",          "Lightweight calculations, sensor values"),
]

#### FRC wild note (italic, below table)

frc_wild_note = (
    "In the FRC wild you'll also see: TunerConstants, FieldConstants, VisionConstants — same "
    "public static final pattern, split into separate files as codebases grow."
)

---

### Section 2 — Left column: CONSTANTS FILE PATTERN  (teal)

note = "Each class lives in its own file. Start small, add files as subsystems grow."

# Code skeleton — one class per file, four files shown

code_skeleton = """
// DriveConstants.java
public final class DriveConstants {
  public static final double kSpeedLimit = 0.8;
  public static final double kDeadband = 0.1;
  public static final int    kLeftMotorPort = 0;
  public static final int    kRightMotorPort = 1;
}

// ArmConstants.java
public final class ArmConstants {
  public static final double kMaxAngleDeg = 120.0;
  public static final double kStowedAngleDeg = 5.0;
}

// AutoConstants.java
public final class AutoConstants {
  public static final double kDriveTimeSeconds = 2.0;
  public static final double kTurnTimeSeconds = 1.3;
}

// OperatorConstants.java
public final class OperatorConstants {
  public static final int kDriverControllerPort = 0;
}
"""

---

### Section 2 — Right column: HOW TO USE A CONSTANT  (purple)

# Five numbered steps, each with a label and a code example.

steps = [
    {
        "label": "1  Import the constants file",
        "code": """
// top of Drive.java
import frc.robot.DriveConstants;
"""
    },
    {
        "label": "2  Use a constant by name",
        "code": """
double speed = DriveConstants.kSpeedLimit;
double dead  = DriveConstants.kDeadband;
"""
    },
    {
        "label": "3  OR use the fully-qualified path (no import)",
        "code": """
double speed =
  DriveConstants.kSpeedLimit;
"""
    },
    {
        "label": "4  Add a constant to an existing file",
        "code": """
// inside DriveConstants.java
public static final double
  kMaxTurnSpeed = 0.6;
"""
    },
    {
        "label": "5  Create a new constants file",
        "code": """
// new file: ScoopConstants.java
public final class ScoopConstants {
  public static final double
    kServoCarryPos = 0.3;
}
"""
    },
]

#### VS Code quick-fix tip (orange callout, bottom of purple column)

vscode_tip = {
    "title": "VS Code quick-fix  (Ctrl+.)",
    "body": [
        "Red underline on a class name? Hover it and press",
        "Ctrl+.  →  Add import.  VS Code writes the line for you.",
    ],
}

---

## PAGE 2

---

### Section 3 — THE k NAMING RULE  (full width, purple)

intro = (
    "Every WPILib constant: lowercase 'k' + UpperCamelCase. "
    "You'll see this across every WPILib source file."
)

#### Naming examples table

# Columns: Category | Example 1 | Example 2 | Example 3

naming_rows = [
    ("Speeds / power",  "kSpeedLimit",               "kMaxTurnSpeed",           "kAutodriveSpeed"),
    ("Angles",          "kMaxAngleDeg",              "kStowedAngleDeg",         "kScoringAngleDeg"),
    ("Distances",       "kWheelCircumferenceMeters", "kTrackWidthMeters",       "kWheelRadiusMeters"),
    ("Timing",          "kDriveTimeSeconds",         "kTurnTimeSeconds",        "kWaitTimeSeconds"),
    ("Ports / IDs",     "kLeftMotorPort",            "kRightMotorPort",         "kControllerPort"),
    ("Strings",         "kProjectName",              "kAutoDefault",            "kLogPrefix"),
    ("Booleans",        "kIsRightInverted",          "kEnableLogging",          "kIsSimulation"),
]

#### Naming rules

# Columns: Rule | Avoid | Use instead

rules = [
    ("Always start with k",          "speedLimit ✗",                  "kSpeedLimit ✓"),
    ("Include unit when ambiguous",   "kMaxAngle ✗",                   "kMaxAngleDeg ✓"),
    ("No abbreviations",              "kWC ✗",                         "kWheelCircumferenceMeters ✓"),
    ("Drop the class name",           "DriveConstants.kDriveSpeed ✗",  "DriveConstants.kSpeed ✓"),
    ("Booleans: kIs or kEnable",      "kMotorInverted ✗",              "kIsRightMotorInverted ✓"),
]

#### Unit rule warning (orange callout)

unit_warning = (
    "A function expecting radians and receiving degrees overshoots by 57×. "
    "Unit in the name = free sanity check every time you read the code."
)

---

### Section 4 — Left column: COMMON MISTAKES  (orange)

# Each mistake: title | inline bad-code example | explanation

mistakes = [
    {
        "title": "Magic number in subsystem file",
        "bad_code": "double speed = 0.8;  // ✗ hardcoded",
        "desc": "Hard to find; one wiring change means hunting across multiple files.",
    },
    {
        "title": "Missing static",
        "bad_code": "public final double kSpeed = 0.8;  // ✗",
        "desc": "Requires a Constants() instance. Won't compile the way you expect.",
    },
    {
        "title": "Missing final",
        "bad_code": "public static double kSpeed = 0.8;  // ✗",
        "desc": "Can be reassigned at runtime. Not a true constant.",
    },
    {
        "title": "No unit in name",
        "bad_code": "kMaxAngle  // ✗  vs  kMaxAngleDeg  // ✓",
        "desc": "Caller can't tell: degrees or radians? Wrong choice = robot overshoots by 57×.",
    },
    {
        "title": "Moved constant, forgot to update reference",
        "bad_code": "speed = 0.8;  // ✗ still in Drive.java",
        "desc": "Build fails. Good — the compiler tells you exactly where to fix it.",
    },
]

---

### Section 4 — Right column: IN THE FRC WILD  (teal)

intro = (
    "BearBots starts with one file per subsystem. As codebases grow, "
    "teams add more. Some common ones you'll see in other FRC repos:"
)

frc_patterns = [
    {
        "file": "TunerConstants.java",
        "desc": (
            "Auto-generated by Phoenix Tuner X for TalonFX motors. "
            "Contains PID gains, gear ratios, encoder offsets. Never edit by hand."
        ),
    },
    {
        "file": "FieldConstants.java",
        "desc": (
            "Field element positions: AprilTag poses, scoring zone coordinates. "
            "Used by vision and autonomous routines."
        ),
    },
    {
        "file": "VisionConstants.java",
        "desc": "Camera transforms, pipeline IDs, trust thresholds, and latency compensation values.",
    },
    {
        "file": "OperatorConstants.java",
        "desc": "Controller port numbers and deadband values. Already in the BearBots project.",
    },
    {
        "file": "Constants.java",
        "desc": (
            "Some teams keep a single file with inner classes (DriveConstants, ArmConstants) "
            "instead of separate files. Either pattern works — pick one and stay consistent."
        ),
    },
]

closing = "Pattern matters more than file count. Pick one and stay consistent."
