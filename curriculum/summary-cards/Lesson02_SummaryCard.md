# Module 2 — Lesson 02: What Did VSCode Just Create?

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

## The Simulator Workflow

1. `Ctrl+Shift+P` → Simulate Robot Code
2. Select `halsim_gui` → OK
3. Joysticks: drag `Keyboard 0` to `Joystick[0]`
4. Open AdvantageScope → Connect to Simulator
5. Robot State → Teleoperated → Enable
6. Click Sim GUI → drive with W/A/S/D

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

---

## After This Lesson I Can…

- [ ] Name every template file and its job
- [ ] Use `Ctrl+Shift+P` to build and simulate
- [ ] Launch sim and drive with keyboard
- [ ] Connect AdvantageScope to simulator
- [ ] Explain why `LoggedRobot` extends `TimedRobot`

---

## Key Vocabulary

- **LoggedRobot** — AdvantageKit base class extending `TimedRobot` — adds logging to each cycle
- **CommandScheduler** — The engine that runs commands — must be called in `robotPeriodic()`
- **Simulator** — Runs robot code on your laptop — same logic, no hardware needed
- **AdvantageScope** — Visualization tool that shows logged data from sim or real robot
- **vendordeps** — JSON files specifying which third-party libraries (like AdvantageKit) to include

---

## Questions I Still Have

*Write your questions here. Bring them next session.*

## My Notes

*Write anything here — surprises, connections, things to look up later.*

---

*FRC Programming Curriculum — Lesson 02*
*Next: Lesson 03 — What is a subsystem?*
*Keep this. Collect all 7.*
