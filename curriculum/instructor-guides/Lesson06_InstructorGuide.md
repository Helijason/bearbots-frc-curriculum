# FRC Programming Curriculum — Module 2, Lesson 06

# How Does the Robot Know When It's Done?

*Commands, the four lifecycle methods, composition, and the AutoChooser pattern.*

> **Instructor Edition — Not for student distribution**

---

## At a Glance

| Field | Detail |
|---|---|
| **Target audience** | Students who completed Lesson 05 and have driven the XRP autonomously at least once |
| **Hardware** | XRP robot — same setup as Lesson 05 |
| **Session length** | 3 hours |
| **Key tools** | WPILib Command framework, AutoChooser via SmartDashboard, AdvantageScope for verification |

---

## Learning Objectives

- Students can name the four methods of a Command (`initialize`, `execute`, `isFinished`, `end`) and explain when each runs
- Students can write a new command from scratch — the `TurnToAngle` case is the proof point
- Students can explain why `addRequirements()` is necessary and what happens without it
- Students can compose commands using `SequentialCommandGroup`, `ParallelCommandGroup`, and the `.andThen()` decorator
- Students can wire up an AutoChooser and verify their selection runs in autonomous mode
- Students can spot and explain the three classic command bugs: wrong group type, `isFinished` returns false, `end()` doesn't stop motors

---

## Before You Start

### Room setup

- VSCode open on projector with the Lesson 05 starter project, plus the L-shape lab code prepared as a separate branch
- AdvantageScope installed; a known-good auto log from a previous run ready to demo
- Digital handout open: `lesson-06-autonomous.html`
- XRP robots available — students need physical hardware for Bronze and Gold tiers
- Floor space — students will be running multi-step autos that travel ~2 meters

### Have ready

- A pre-broken `AutoRoutines.java` with the three lab bugs in place — for live triage
- A complete reference implementation of `TurnToAngle` (see Phase 4 notes below)
- Tape on the floor marking 1m and 2m gridlines so students can verify auto distances visually

> **The most important instructor mindset for this lesson**
>
> This is the lesson where students stop being told what to write and start writing their own commands. Resist the urge to dictate. When a student's `TurnToAngle` doesn't work, ask *"which of the four methods is wrong?"* before showing them the answer. Most bugs at this stage are 'isFinished always false' or 'forgot to stop in end' — the broken robot lab covers both, and the more students hit those bugs themselves, the better they'll remember.

---

## Session Timing

| Time | Phase | You do | Students do |
|---|---|---|---|
| **0–5 min** | **Hook** | Run a working auto routine on the projector. Then run one with a missing `isFinished`. Ask which is which. | Watch. Predict. Realize the difference is one method. |
| **5–30 min** | **Concept** | Walk through the four methods of Command. Read `DriveDistance.java` line-by-line. Cover `addRequirements`. CommandScheduler lifecycle. | Follow on digital handout. Match each method to its purpose. |
| **30–60 min** | **Composition** | `SequentialCommandGroup`, parallel variants, decorators. AutoChooser wiring on projector. | Replicate AutoChooser setup. Add an option. |
| **60–120 min** | **Practice** | Circulate during tiered challenge. Push Bronze finishers to Silver. Catch the four common bugs early. | Bronze: run existing auto + read AdvantageScope. Silver: write `TurnToAngle`. Gold: compose L-shape. |
| **120–150 min** | **Broken robot lab** | Circulate. Redirect with questions, not answers. | Find and fix 3 bugs. Predict what each would look like in AdvantageScope. |
| **150–170 min** | **Physical XRP auto** | Students run autonomous on real hardware. Compare sim vs physical behavior. | Run DriveDistance on XRP. Measure actual vs expected distance. |
| **170–180 min** | **Connect + wrap** | Tease Lesson 07. Exit check. | Exit check: name the four methods. Tease closed-loop control. |

> **45-minute compressed version**
> Drop the composition deep dive. Cover only the four lifecycle methods and the broken robot lab. Assign Silver/Gold tiers as homework. Students will know commands but not how to compose them — the composition concepts are still in the digital handout for self-study.

---

## Phase 1 — Hook (0–5 min)

*Show a working auto, then a broken one. Make the difference visceral.*

### Opening

On the projector, run a working `DriveDistance` auto. The robot drives 1 meter and stops. Reset, run a version where `isFinished()` returns `false`. The robot drives off the field. Don't explain yet.

> **Script — what to ask**
>
> *"Both of these are autonomous routines. Both compile. Both run. One does what it says. The other doesn't. What's the difference?"*
>
> Wait for answers. Most students will guess sensors, motor speeds, encoder problems. Let those answers sit.
>
> Then: *"There's exactly one method different between these two. Today we learn what that method does, and three others — and once you know all four, you can write any auto you can imagine."*

---

## Phase 2 — Concept (5–30 min)

*Three things to teach: the four lifecycle methods, why subsystem requirements matter, why commands beat `autonomousPeriodic`.*

### The four methods of a Command

Open `DriveDistance.java` on the projector. Walk through it method by method, asking students to name each one's job before you reveal it.

- `initialize()` — *"What's special about the first cycle?"* — runs once, record the start position, reset sensors
- `execute()` — *"What runs forever while we're driving?"* — runs every 20ms, set motor outputs
- `isFinished()` — *"How do we know we're there?"* — runs every cycle after `execute()`, return `true` to stop
- `end(boolean interrupted)` — *"What do we do when we stop?"* — runs once on stop or interrupt, stop the motors here always

> **The line that has to land**
>
> ***"`end()` always runs. Even if the command was interrupted, even if it never reached its target, `end()` runs. Use it to put the subsystem in a safe state. If you don't, the motors keep their last setpoint forever and the robot keeps driving."***
>
> *This is bug #3 in the lab. Drill it now and the lab finds it for itself.*

### The CommandScheduler lifecycle

Explain what calls these methods — students don't call `initialize()` themselves:

> **The scheduler's loop, every 20ms:**
>
> 1. For each scheduled command, if it just got scheduled this cycle: call `initialize()`
> 2. Call `execute()`
> 3. Call `isFinished()`. If it returns `true` → call `end(false)` and remove from schedule
> 4. If a higher-priority command takes the same subsystem → call `end(true)` on the loser, schedule the winner
>
> You write the four methods. The scheduler does the rest.

### `addRequirements()` — why it matters

Two commands wanting the same subsystem at once is a recipe for chaos. `addRequirements` declares ownership; the scheduler enforces it. Without it, two commands calling `drive.drive()` in `execute()` at the same time means whichever ran last wins for that cycle — effectively random motor commands.

*If you have time: demonstrate. Schedule two commands that both write to the drivetrain. Show the robot doing nothing useful. Add `addRequirements`; show the scheduler interrupting the first when the second starts.*

### Why this beats `autonomousPeriodic`

Four wins — make the students name them before you say them:

- **Composable:** `SequentialCommandGroup(driveDist, turn, driveDist)` is one line
- **Interruptible:** driver aborts → scheduler calls `end(true)`, motors stop
- **Reusable:** same `DriveDistance` works in auto, teleop, test routines
- **Loggable:** CommandScheduler logs every `initialize`, `execute`, `end` — visible in AdvantageScope's Commands folder

---

## Phase 3 — Composition (30–60 min)

*Where the framework's actual power shows up. Demo on the projector.*

### `SequentialCommandGroup` demo

```java
public Command driveLShape(DriveSubsystem drive) {
    return new SequentialCommandGroup(
        new DriveDistance(drive, 1.0),   // drive 1m forward
        new TurnToAngle(drive, 90.0),    // then turn 90°
        new DriveDistance(drive, 1.0)    // then drive another 1m
    );
}
```

- Run it in sim. Watch the robot draw an L.
- Open AdvantageScope. Show the Commands folder with three back-to-back command init/end events.
- **Key point:** each child has its own four methods. The group manages who runs when. A `SequentialCommandGroup` is itself a `Command` — you can nest them.

### Parallel groups

| Group type | Ends when | Use case |
|---|---|---|
| `ParallelCommandGroup` | All children finish | Drive while spinning up shooter |
| `ParallelDeadlineGroup` | First child (the "deadline") finishes — kills the rest | Drive 3 seconds while running intake; when drive ends, stop intake too |
| `ParallelRaceGroup` | Any child finishes — kills the rest | Try to score, but cancel after 2 seconds (`WaitCommand(2)` racing the score command) |

> **Parallel groups can't share subsystems.** Two commands needing the drivetrain can't run in parallel — only one command can own a subsystem at a time. Compose them sequentially or use different subsystems.

### Decorators — the fluent shortcuts

```java
// Same as new SequentialCommandGroup(a, b):
a.andThen(b);

// Same as new ParallelCommandGroup(a, b):
a.alongWith(b);

// Run a until 3 seconds pass, whichever comes first:
a.withTimeout(3.0);

// Run a until some condition becomes true:
a.until(() -> someBoolean);

// Chain them — they all return Commands you can keep decorating:
driveDist.andThen(turn).andThen(driveDist).withTimeout(15.0);
```

Show both the group constructor form and the decorator form for the same routine. Decorator form reads better and appears more in real code.

### AutoChooser wiring

```java
// In RobotContainer.java
private final SendableChooser<Command> autoChooser = new SendableChooser<>();

public RobotContainer() {
    autoChooser.setDefaultOption("Drive 1m", new DriveDistance(drive, 1.0));
    autoChooser.addOption("L-shape", driveLShape(drive));
    autoChooser.addOption("Score and back up", scoreAndBackUp(drive, shooter));
    SmartDashboard.putData("Auto Choice", autoChooser);
}

public Command getAutonomousCommand() {
    return autoChooser.getSelected();
}
```

In `Robot.java`'s `autonomousInit()`: schedule whatever `getAutonomousCommand()` returns. In `teleopInit()`: cancel the auto command if it's still running — otherwise it fights the driver.

*Most of this is already in the starter project. Show students where it is and what to add an option to.*

---

## Phase 4 — Practice (60–120 min)

*Tiered challenge. Push students upward — Bronze finishers go straight to Silver. Never sit down during this phase.*

### Reference implementation — `TurnToAngle`

Have this ready but don't show it until a student has been stuck for 10+ minutes on Silver:

```java
public class TurnToAngle extends Command {
    private final DriveSubsystem drive;
    private final double targetDegrees;
    private double startDegrees;

    public TurnToAngle(DriveSubsystem drive, double degrees) {
        this.drive = drive;
        this.targetDegrees = degrees;
        addRequirements(drive);
    }

    @Override public void initialize() {
        startDegrees = drive.getHeadingDegrees();
    }

    @Override public void execute() {
        double rotation = Math.signum(targetDegrees) * 0.5;
        drive.drive(0.0, rotation);
    }

    @Override public boolean isFinished() {
        double turned = drive.getHeadingDegrees() - startDegrees;
        return Math.abs(turned) >= Math.abs(targetDegrees);
    }

    @Override public void end(boolean interrupted) {
        drive.stop();
    }
}
```

> **Gyro gotchas to know before students hit them:**
> - `Math.signum(targetDegrees)` handles both positive and negative target angles correctly
> - `Math.abs()` on both sides of the comparison handles sign issues
> - Gyro might wrap around 180° or 360° for large angles — for the 90° XRP case this is not a problem, but flag it

### What to circulate for

- **Bronze:** students who can't find the AutoChooser in SmartDashboard — show them where it appears (Shuffleboard or SmartDashboard tab; look for `SmartDashboard/Auto Choice` in AdvantageScope)
- **Bronze:** students who can't find the Commands folder in AdvantageScope — check `CommandScheduler.getInstance().onCommandInitialize(...)` is in `Robot.java`
- **Silver:** students whose `TurnToAngle` never ends — probably wrong sign or wrong direction in `isFinished`. Ask: *"What's your start angle? What's your current angle? When should you stop?"*
- **Silver:** students whose `TurnToAngle` ends instantly — forgot to record `startDegrees` in `initialize`, so `current - 0` already exceeds the target
- **Gold:** students who used `ParallelCommandGroup` by accident — exactly bug #1 in the lab. Let them discover it, then point at line 3 of the lab code
- **Gold:** add `WaitCommand(0.5)` between moves as a bonus challenge; `withTimeout(15.0)` wrapping the whole routine as a double bonus

### The high-leverage question

When a student says *"my command isn't working,"* ask: *"which of the four methods has the bug?"* Force them to localize. Eight times out of ten, they say it themselves. That self-diagnosis is the point of the framework.

---

## Phase 5 — Broken Robot Lab (120–150 min)

*Three bugs. Each must be confirmed by running the sim — reading the code is not enough.*

### Bug 1 — `ParallelCommandGroup` instead of `SequentialCommandGroup`

Line 3: the group type is wrong. `ParallelCommandGroup` tries to run all three children at once. Two of them require the drivetrain. The scheduler refuses to run two commands sharing a subsystem in parallel — the group fails to start, or only one child runs. Students see *"the robot drives once but never turns."*

**Acceptable hint:** *"Three commands. Same subsystem. Parallel group. What's the rule about parallel groups and shared subsystems?"*

**Fix:** change `ParallelCommandGroup` to `SequentialCommandGroup`.

### Bug 2 — `isFinished` returns `false` forever

Line 25: the command never reports it's done. `execute()` keeps running, motors keep getting set, the robot drives until sim timeout or crashes. The next command in the sequence never starts.

**Acceptable hint:** *"What should this return when the robot has traveled the right distance?"*

**Fix:** `return drive.getLeftPositionMeters() - startMeters >= targetMeters;`

### Bug 3 — `end()` doesn't stop the motors

Line 26: `end()` is empty. When the command finishes or gets interrupted, the motors keep their last setpoint of `0.5`. The robot keeps driving.

**This is THE bug to drill. Every team's first auto has this bug, every season.**

**Acceptable hint:** *"What should happen to the motors when the command ends?"*

**Fix:** `drive.stop();` in `end()`.

> **Confirm every fix in sim before moving on**
>
> Students must run the simulator and verify the symptom is gone. Reading the code and spotting the bug is not enough.

---

## Phase 6 — Physical XRP Auto (150–170 min)

*Students run autonomous on real hardware and compare to sim.*

### What students do

- Deploy code to XRP
- Run `DriveDistance(drive, 1.0)` in autonomous mode
- Measure actual stopping distance with tape measure
- Compare to the 1m target
- Ask: *"If it overshot, why? How would you fix it without changing the target distance?"*

### What to watch for

- Students who get different distances on hardware vs sim — unit conversion issue or encoder calibration
- Students who run the auto and the robot doesn't stop — bug #3 still in their code
- Students who want to reduce the power to improve accuracy — let them try, then tease Lesson 07 (closed-loop control fixes this properly)

---

## Phase 7 — Connect + Wrap (170–180 min)

### Exit check — 60 seconds, no grades

Two questions:

1. *"Name the four methods of a command."*
2. *"Why does `end()` need to stop the motors even if `isFinished()` already returned true?"*

### Teaser for Lesson 07

> *"Today's commands work because we time things by encoder distance — we drive at 0.5 power and wait for the encoder to hit 1 meter. The robot overshoots because it has momentum. Next time, we close the loop: instead of 'drive at 0.5 power until 1 meter', we say 'drive at exactly 1 m/s, with PID feedback, until exactly 1 meter.' Same four-method structure. Same composition. Just smarter `execute()`."*

---

## Common Student Questions

**Q: Why doesn't the robot stop right at 1 meter? It overshoots.**
A: *"Because the command is open-loop — it sets motors to 0.5 power and waits for the encoder to hit 1m. By the time the encoder reaches 1m, the robot has momentum. Lesson 07 fixes this with feedback control. For now, an auto that ends at 1.05m is fine."*

**Q: My SequentialCommandGroup feels weird — why are commands inside another command?**
A: *"That's the recursion. A `SequentialCommandGroup` IS a `Command`. So you can put one inside another. You can build very complex routines this way without any new framework — just nesting. This is why we say 'commands compose.'"*

**Q: When do I use a Command class vs an InstantCommand lambda?**
A: *"`InstantCommand` is for one-line actions: 'reset gyro,' 'open intake.' Command class is when you have state, want to track progress, or care about the `end()` cleanup. Rule of thumb: if you'd write more than 5 lines of action, make it a class."*

**Q: What if I want my command to run forever — like a default command?**
A: *"Then `isFinished` can return `false`. Default commands are the exception to Rule 1. The scheduler interrupts them when another command needs the subsystem, so they end via interruption, not via finishing."*

**Q: My auto works in sim but not on the XRP. Why?**
A: *"Most likely: encoder units. The XRP gives positions in inches; sim might give meters. Check `getLeftPositionMeters()` and confirm it's actually meters on hardware. This is the unit bug from the Lesson 04 reference card."*

**Q: Why is `end()` called even if I get interrupted? I didn't finish.**
A: *"Because cleanup matters either way. If you were driving forward and got interrupted, the motors are still running — `end()` needs to stop them or the robot keeps going. The `interrupted` boolean is just a hint about why you're ending. The cleanup is the same."*

**Q: Can't I just schedule the next command in `end()`?**
A: *"You can. It works for two commands and falls apart at three. Composition is what WPILib gives you instead. It's what every team is using by championships. Learn it now."*

---

*Instructor Edition — Not for student distribution*
