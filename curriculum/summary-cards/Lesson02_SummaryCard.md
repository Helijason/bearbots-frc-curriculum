# Module 1 — Lesson 02: What Did VSCode Just Create?

**Stack:** Java | AdvantageKit | XRP
**Card #:** 02 — *Keep this. Add it to your binder.*

---

## The Big Idea

> Understand the template before you modify it.
> Editing files you don't understand is how you create bugs you can't explain.

---

## Key Concepts

| File | Role | What it does |
|---|---|---|
| **Main.java** | Entry point | Starts the robot. Do not modify. Ever. |
| **Robot.java** | Lifecycle | `extends LoggedRobot`. Runs `CommandScheduler`. Logger setup lives here. |
| **RobotContainer** | Switchboard | Creates subsystems. Wires buttons. Provides auto command. |
| **Constants.java** | Number vault | Motor IDs live here. Mode enum lives here. Never hardcode numbers. |
| **build.gradle** | Build recipe | WPILib version. Vendor deps. Don't edit by hand. |

---

## Simulation GUI Panels

| Panel | Purpose |
|---|---|
| **Robot State** | Enable/disable. Switch modes. Enable before driving — nothing works disabled. |
| **Joysticks** | Map keyboard or controller to robot inputs. Drag `Keyboard 0` to `Joystick[0]`. |
| **System Console** | Print statements, errors, stack traces. Check here first when something is wrong. |
| **NetworkTables** | Live values published by the robot. AdvantageKit data appears as `AdvantageKit/...` |

---

## The Simulator Workflow

1. `Ctrl+Shift+P` → Simulate Robot Code
2. Select `halsim_gui` → OK
3. Joysticks: drag `Keyboard 0` to `Joystick[0]`
4. Open AdvantageScope → Connect to Simulator
5. Robot State → Teleoperated → Enable
6. Click Sim GUI → drive with W/A/S/D
7. In AdvantageScope: drag `LeftPositionMeters` and `GyroYawDegrees` to graphs

---

## Keyboard Driving Keys

| Key | Action |
|---|---|
| **W** | Forward (Left stick Y −) |
| **S** | Backward (Left stick Y +) |
| **A** | Turn left (Left stick X −) |
| **D** | Turn right (Left stick X +) |

> Sim GUI must be focused for keys to work.
> Enable robot before driving — nothing moves disabled.
> These match the default arcade drive command in RobotContainer.

---

## After This Lesson I Can…

- [ ] Name every template file and its job
- [ ] Use `Ctrl+Shift+P` to build and simulate
- [ ] Launch sim and identify all four Simulation GUI panels
- [ ] Drive with keyboard and verify inputs in the Joysticks panel
- [ ] Connect AdvantageScope to simulator and graph `LeftPositionMeters`
- [ ] Explain why `LoggedRobot` extends `TimedRobot`
- [ ] Find and fix the three common Robot.java bugs

---

## Key Vocabulary

- **LoggedRobot** — AdvantageKit base class extending `TimedRobot` — adds logging to each cycle
- **CommandScheduler** — The engine that runs commands — must be called in `robotPeriodic()`
- **Simulator** — Runs robot code on your laptop — same logic, no hardware needed
- **AdvantageScope** — Visualization tool that shows logged data from sim or real robot — bundled with WPILib
- **System Console** — The simulator panel that shows errors and print output — check here first when debugging
- **vendordeps** — JSON files specifying which third-party libraries (like AdvantageKit) to include

---

## Questions I Still Have

*Write your questions here. Bring them next session.*

## My Notes

*Write anything here — surprises, connections, things to look up later.*

---

---

## Competition Connection

> **First look at Orbit Odyssey.** This lesson ends with a pair brainstorm — what does this robot need to DO to score points? Keep your answers. Next lesson you'll map them directly to subsystem files.
>
> Every file you learned today has a job on the competition robot. `Constants.java` holds your park distance and kP. `RobotContainer` wires your auto command to the AutoChooser. Understanding the template now means you won't be guessing later.

---

*FRC Programming Curriculum — Lesson 02*
*Next: Lesson 03 — What is a subsystem?*
*Keep this. Collect all 8.*
