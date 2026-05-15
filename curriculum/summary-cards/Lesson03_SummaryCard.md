# Module 2 — Lesson 03: What Is a Subsystem?

**Stack:** Java | AdvantageKit | XRP
**Card #:** 03 — *Keep this. Add it to your binder.*

---

## The Big Idea

> Each subsystem owns exactly one mechanism and controls it completely.
> One job, one file. If the shooter breaks, the drivetrain keeps driving.

---

## Key Concepts

| Concept | Role | What it does |
|---|---|---|
| **One job** | Separation | One mechanism. One subsystem. One file. |
| **`periodic()`** | Sensors only | Read sensors. Log data. **No motor control.** |
| **Commands** | Motor control | Control motors. Respond to buttons. Can be interrupted. |
| **WPILib tool** | Create files | Right-click folder. Create new class. Select `SubsystemBase`. |
| **Verify in sim** | Always check | Build succeeds. Folder in AdvantageScope. Drive and observe. |

---

## Creating a Subsystem (the right way)

1. Right-click `subsystems/` in Explorer
2. Create a new class/command
3. Select `SubsystemBase`
4. Name it (e.g. `Indexer`)
5. Add to `RobotContainer` as a field
6. Build → Simulate → verify in AdvantageScope

> **NEVER create subsystem files by hand.**

---

## The Two Rules of Subsystems

**Rule 1 — Motor control goes in commands, NOT in `periodic()`.**
`periodic()` runs forever; commands can be stopped and interrupted.

**Rule 2 — Each motor lives in ONE subsystem.**
Indexer motor → `IndexerSubsystem`. Not both.

---

## After This Lesson I Can…

- [ ] Explain what a subsystem is in plain English
- [ ] Create a subsystem file using the WPILib tool
- [ ] Register a subsystem in `RobotContainer`
- [ ] Explain why motor control belongs in commands
- [ ] Verify a subsystem loads correctly in AdvantageScope

---

## Key Vocabulary

- **SubsystemBase** — WPILib base class — extend this to create a subsystem
- **`periodic()`** — Method called every 20ms — for sensors and logging, not motor control
- **Command** — An action that can be scheduled, run, interrupted, and ended cleanly
- **Default command** — Command that runs when no other command is using the subsystem
- **`@AutoLogOutput`** — AdvantageKit annotation — automatically logs a field to AdvantageScope

---

## Questions I Still Have

*Write your questions here. Bring them next session.*

## My Notes

*Write anything here — surprises, connections, things to look up later.*

---

*FRC Programming Curriculum — Lesson 03*
*Next: Lesson 04 — Why two files for one motor?*
*Keep this. Collect all 7.*
