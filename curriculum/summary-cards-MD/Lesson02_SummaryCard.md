# Lesson 02 Summary Card — Content Variables
# Matches Lesson_SummaryCard_Format.md spec exactly.

---

## HEADER

module_line  = "MODULE 1  —  LESSON 02"
title        = "Template Structure + File Roles"
badge_num    = "02"

---

## BIG IDEA

big_idea_bold   = "Every file has one job. Know which file to edit before you touch anything."
big_idea_italic = "The BearBots project adds AdvantageKit logging and a clean constants structure to the WPILib template."

---

## KEY CONCEPTS (5 cards)

concepts = [
    ("Robot.java",          "Lifecycle manager",  "Extends LoggedRobot.\nRuns CommandScheduler.\nCalled every 20ms."),
    ("RobotContainer",      "Wiring hub",         "Subsystems created here.\nButton bindings here.\nIO layer injected here."),
    ("Constants.java",      "Source of truth",    "Motor ports, speed limits.\nInner classes group values.\nChange once, updates everywhere."),
    ("AdvantageKit",        "Logging layer",      "Logger.start() at boot.\nNT4Publisher feeds AScope.\nEvery loop cycle captured."),
    ("Simulator",           "Test bench",         "Simulate before hardware.\nDrag Keyboard 0 → Joystick[0].\nGraph encoders in AScope."),
]

---

## SETUP WORKFLOW (left col, TEAL)

left_col_label = "THE SETUP WORKFLOW"

steps = [
    ("1", "Create XRP-Template project → explore vanilla file structure"),
    ("2", "Install Git → git config name + email → clone bearbots-xrp-code"),
    ("3", "git pull → build project → BUILD SUCCESSFUL"),
    ("4", "Simulate Robot Code → enable halsim_gui → sim window opens"),
    ("5", "Connect AdvantageScope → Drive/ folder → graph LeftPositionMeters"),
    ("6", "Drive with WASD → predict graph shape before each maneuver"),
    ("7", "Broken Robot Lab — fix 4 bugs using symptom descriptions only"),
]

---

## AFTER THIS LESSON I CAN... (right col, PURPLE)

checks = [
    "Name the job of each file: Main, Robot, RobotContainer, Constants, build.gradle",
    "Explain why extends LoggedRobot instead of TimedRobot",
    "Use git add / commit / pull to save my work",
    "Launch the simulator and connect AdvantageScope",
    "Read encoder graphs and describe what the robot is doing",
    "Find a bug from a symptom description alone",
]

---

## KEY VOCABULARY (right col, TEAL)

vocab = [
    ("LoggedRobot",    "AdvantageKit base class — wraps each 20ms loop with data capture"),
    ("RobotContainer", "Where subsystems are created and buttons are wired to commands"),
    ("Constants.java", "Central file for fixed values — inner classes group related constants"),
    ("git commit",     "Saves a labeled snapshot of code you can return to"),
    ("NT4Publisher",   "Streams AdvantageKit log data to NetworkTables for AdvantageScope"),
]

---

## FOOTER

footer_left   = "FRC Programming Curriculum — Lesson 02"
footer_center = "Next: Lesson 03 — What is a subsystem?"
footer_right  = "Keep this. Collect all 8."

