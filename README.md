# BearBots 6964 — FRC Programming Curriculum

A structured, seven-lesson curriculum for teaching FRC robot programming to high school students using Java, WPILib, AdvantageKit, and XRP robots.

**Live site:** [helijason.github.io/bearbots-frc-curriculum](https://helijason.github.io/bearbots-frc-curriculum/)

---

## Overview

This curriculum takes students with little or no prior experience and progressively builds them toward reading and writing competition-ready robot code. The central concept is the **IO pattern** — a three-file abstraction separating hardware from subsystem logic — introduced in Lesson 4 and reinforced through every lesson that follows.

Lessons are organized in two phases:

- **Phase 1 (Lessons 1–3):** No hardware required. Students work in VSCode with the WPILib simulator and AdvantageScope.
- **Phase 2 (Lessons 4–7):** XRP robot hardware introduced. Students apply the IO pattern to real mechanisms.

Each lesson includes a hook question, a student summary card, and an instructor guide with timing, scripts, common bugs, and tiered challenge notes.

---

## Lessons

| # | Title | Phase |
|---|-------|-------|
| 01 | Setup + First Drive | Simulator |
| 02 | WPILib Template Structure and File Roles | Simulator |
| 03 | What Is a Subsystem? | Simulator |
| 04 | The IO Pattern and AdvantageKit Architecture | XRP |
| 05 | How Do I Debug a Robot That Isn't Here? | XRP |
| 06 | How Does the Robot Know When It's Done? | XRP |
| 07 | Why Doesn't It Stop Where I Told It To? | XRP |

---

## Tech Stack

- **Java + WPILib** — primary programming environment
- **AdvantageKit + AdvantageScope** — logging and telemetry
- **XRP robot** — accessible hardware platform for Phase 2
- **VSCode** — WPILib-integrated development environment

---

## Repo Structure

```
/curriculum          Student summary cards and reference sheet
/curriculum/instructor-guides    Instructor guides for each lesson
/docs                Live website source
/setup               Setup scripts and resources
/vscode              VS Code snippets for AdvantageKit patterns
```

---

## For Other Teams

Feel free to use or adapt this curriculum for your own team. If you have improvements or corrections, open an issue or pull request.