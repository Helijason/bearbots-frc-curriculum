# Module 1, Lesson 03: What Is a Subsystem?

**Stack:** Java | AdvantageKit | XRP
**Card #:** 03, Keep this. Add it to your binder.

---

## The Big Idea

> Each subsystem owns exactly one mechanism and controls it completely.
> One job, one file. If the scoop breaks, the drivetrain keeps driving.

---

## Key Concepts

| Concept | Role | What it does |
|---|---|---|
| **One job** | Separation | One mechanism. One subsystem. One file. WPILib enforces it. |
| **`periodic()`** | Sensors only | Runs every 20ms, unconditionally. Reads sensors, logs data. No motor control. |
| **Commands** | Motor control | Start, stop, interrupt. Set a goal. The scheduler controls the lifecycle. |
| **Goal pattern** | Coordination | Commands set a goal. `periodic()` reads the goal and applies it. |
| **Superstructure** | Preview | A coordinator above multiple subsystems for multi-mechanism moves. Named today, built later. |

---

## Why periodic() Cannot Control Motors

Every 20ms loop, the CommandScheduler runs the same sequence: subsystem `periodic()` first, then triggers and buttons, then active commands.

**`periodic()` runs unconditionally.** The scheduler cannot skip it, delay it, or interrupt it. It has no requirements, so the scheduler's conflict resolution cannot touch it.

**Commands are different.** They can be started, stopped, interrupted, and coordinated. A disable stops a command cleanly. A disable has no effect on `periodic()`.

Motor output in `periodic()` runs forever, ignores robot state, and cannot be emergency-stopped. That is the whole reason the rule exists.

---

## Reference

> **`BearBots_Program_Flow.pdf`** , the 15-page program execution flow reference (flowcharts + file cards for `Main.java`, `Robot.java`, `RobotContainer.java`, `Drive.java`, `Arm.java`, and IO files). Keep this out during Part 2 and Part 4 for tracing how `periodic()` and the scheduler connect to real files.

---

## The Four Parts of a Subsystem

1. **Fields:** hardware objects, goal state, current state. Private.
2. **Constructor:** runs once at startup. Configure hardware, set initial state.
3. **`periodic()`:** runs every loop, forever. Sensors and logging only.
4. **Methods & Commands:** the public API. Often return `Command` objects to schedule.

---

## Building Scoop (the goal pattern)

1. Create the file with the WPILib tool (`SubsystemBase`), never by hand
2. Add the hardware field (servo)
3. Add a `Goal` enum (e.g. `FLAT`, `CARRY`, `DUMP`)
4. Add `@AutoLogOutput` on the goal field so it shows in AdvantageScope
5. Add `setGoal()` and a `setGoalCommand()`
6. Wire `periodic()` to read the goal and apply it to hardware
7. Register in `RobotContainer`, bind a button
8. Build, Simulate, verify in AdvantageScope

> Commands set the goal. `periodic()` applies it. The servo always tracks the current goal, this is not motor control in periodic(), it's state application.

---

## After This Lesson I Can…

- [ ] Explain why `periodic()` cannot contain motor control
- [ ] Name the four parts of every subsystem
- [ ] Build a subsystem using the goal pattern (command sets goal, periodic applies it)
- [ ] Use the `aksubsystem` snippet to scaffold a new subsystem
- [ ] Spot all four Broken Robot Lab bug types in unfamiliar code
- [ ] Explain what a superstructure is and why it isn't built yet

---

## Key Vocabulary

- **SubsystemBase** , WPILib base class. Extending it registers the subsystem with the CommandScheduler automatically
- **Goal** , the target state a subsystem should move toward, set by a command and read by `periodic()`
- **Superstructure** , a coordinator above multiple subsystems for moves that require more than one mechanism at once
- **`@AutoLogOutput`** , AdvantageKit annotation that automatically logs a field to AdvantageScope
- **Requirement** , the subsystem(s) a command claims; the scheduler prevents two commands from sharing a requirement at once

---

## Broken Robot Lab: 4 Bugs

1. **Wrong subsystem ownership:** scoop servo declared inside `Drive`
2. **Motor control in `periodic()`:** drives forward unconditionally, never stops
3. **Misattributed requirement:** a scoop command defined inside `Drive` locks out driving
4. **Emergency stop that doesn't stop:** a `runOnce()` setting motors to 0 gets overridden by `periodic()` on the very next loop, 20ms later

---

## Questions I Still Have

*Write your questions here. Bring them next session.*

## My Notes

*Write anything here, surprises, connections, things to look up later.*

---

---

## Competition Connection

> **The BearBots robot has four subsystems:** `Drive`, `Elevator`, `Scoop`, `Arm`. You designed these, or something very close, on the whiteboard today before seeing the answer.
>
> Each subsystem owns exactly one mechanism. If the scoop breaks, the drivetrain keeps driving. If the elevator breaks, the arm still works. That independence is why the robot can compete even when something goes wrong.

---

*FRC Programming Curriculum, Lesson 03*
*Next: Lesson 04, Why two files for one motor?*
*Keep this. Collect all 8.*
