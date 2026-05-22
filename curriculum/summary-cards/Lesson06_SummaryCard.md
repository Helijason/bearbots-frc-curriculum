# Module 2 — Lesson 06: How Does the Robot Know When It's Done?

**Stack:** Java | AdvantageKit | XRP
**Card #:** 06 — *Keep this. Add it to your binder.*

---

## The Big Idea

> A command has a beginning, a middle, and an end.
> Autonomous is just commands ending in the right order. Compose them and you have a routine.

---

## Key Concepts

| Concept | Role | What it does |
|---|---|---|
| **`initialize()`** | Run once | At command start. Record start state. Reset sensors here. |
| **`execute()`** | Every cycle | Runs every 20ms. Set motor outputs here. Body of the loop. |
| **`isFinished()`** | Am I done? | Runs after `execute()`. Return `true` to end. Always `false` = forever. |
| **`end(boolean)`** | Cleanup | Runs once at stop OR interrupt. **STOP THE MOTORS HERE. Always.** |
| **Sequential** | Composition | Commands one by one. Wait for child finish. |

---

## The Command Lifecycle (per scheduler loop)

1. If just scheduled this cycle → `initialize()` runs once
2. Every 20ms: `execute()` runs
3. `isFinished()` runs after `execute()`. If `true` → `end(false)`, command removed
4. If another command takes the subsystem → `end(true)` on the loser, new command wins

> The CommandScheduler runs this for every scheduled command, every loop.
> You write the four methods. The scheduler does the rest.

---

## Composition — Combining Commands

```java
// Sequential — one after another:
new SequentialCommandGroup(driveForward, turn, driveForward)

// Parallel — all at once (ends when ALL finish):
new ParallelCommandGroup(driveForward, spinUpShooter)

// DeadlineGroup — ends when FIRST finishes, kills rest:
new ParallelDeadlineGroup(drive3sec, runIntake)

// RaceGroup — ends when ANY finishes, kills rest:
new ParallelRaceGroup(tryToScore, new WaitCommand(2.0))
```

> Two parallel commands cannot share a subsystem.

---

## Decorators — Fluent Shortcuts

```java
a.andThen(b)          // same as SequentialCommandGroup(a, b)
a.alongWith(b)        // same as ParallelCommandGroup(a, b)
a.withTimeout(3.0)    // ends after 3 seconds, whichever comes first
a.until(() -> done)   // ends when condition becomes true
driveDist.andThen(turn).andThen(driveDist).withTimeout(15.0)  // chain them
```

---

## The Two Rules You Can't Break

**Rule 1 — Every command must end.**
`isFinished() = false` forever = routine stalls. Next command never starts.

**Rule 2 — `end()` must put the subsystem in a safe state.**
`drive.stop()` in `end()`. Always. Even if interrupted.
Break it: motors keep last setpoint forever.

---

## AutoChooser Pattern

```java
private final SendableChooser<Command> autoChooser = new SendableChooser<>();

autoChooser.setDefaultOption("Drive 1m", new DriveDistance(drive, 1.0));
autoChooser.addOption("L-shape", driveLShape(drive));
SmartDashboard.putData("Auto Choice", autoChooser);

public Command getAutonomousCommand() { return autoChooser.getSelected(); }
```

> In `autonomousInit()`: schedule the selected command.
> In `teleopInit()`: cancel it — otherwise it fights the driver.

---

## After This Lesson I Can…

- [ ] Name the four methods of a command and when each runs
- [ ] Write a new command (`TurnToAngle`) from scratch
- [ ] Compose commands with `SequentialCommandGroup`
- [ ] Use decorators: `andThen`, `withTimeout`, `until`
- [ ] Wire an `AutoChooser` into SmartDashboard
- [ ] Spot 'doesn't end' and 'doesn't stop' bugs on sight

---

## Key Vocabulary

- **Command** — WPILib base class with four lifecycle methods — extend it to make any robot action
- **CommandScheduler** — WPILib singleton that calls `initialize/execute/isFinished/end` on every scheduled command
- **SequentialCommandGroup** — Runs child commands one after another — the workhorse of every autonomous routine
- **`addRequirements()`** — Declares which subsystems a command exclusively owns — prevents two commands fighting
- **AutoChooser** — `SendableChooser<Command>` that lets the driver pick which auto routine to run before the match
- **`WaitCommand`** — Built-in command that does nothing for a given duration — useful between auto steps
- **Decorator** — Method on `Command` that wraps it in a group (e.g., `.andThen()`, `.withTimeout()`)

---

## Questions I Still Have

*Write your questions here. Bring them to the next session.*

## My Notes

*Write anything here — surprises, connections, things to look up later.*

---

*FRC Programming Curriculum — Lesson 06*
*Next: Lesson 07 — Sensors and feedback*
*Keep this. Collect all 7.*
