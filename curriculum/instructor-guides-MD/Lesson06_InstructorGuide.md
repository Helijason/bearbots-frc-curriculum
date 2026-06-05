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
| **60–120 min** | **Practice** | Circulate during tiered challenge. Push Bronze finishers to Silver. Catch the four common bugs early. | Bronze: park auto (5 pts). Silver: rubble scoring auto. Gold: high zone auto + strategy math. |
| **120–150 min** | **Broken robot lab** | Circulate. Redirect with questions, not answers. | Find and fix 3 bugs. Predict what each would look like in AdvantageScope. |
| **150–170 min** | **Physical XRP auto on field** | Enforce sim-first gate. Circulate during field runs. Watch for open-loop overshoot. | Run auto on Orbit Odyssey field. Log it. Compare sim vs hardware. Note the gap. |
| **170–180 min** | **Strategy discussion + wrap** | Facilitate break-even discussion. Exit check. Tease Lesson 07. | Debate risky vs safe auto. Exit check. |

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

*Tiered challenge — but every tier is building real competition auto code, not toy exercises. Push students upward as they finish each tier. Never sit down during this phase.*

> **The framing to give students before they start**
>
> *"Every command you write in this phase is a candidate for your Orbit Odyssey autonomous routine. Bronze gets you a robot that parks. Silver gets you a robot that scores rubble. Gold gets you a robot that does both. Real points, real strategy."*

### Bronze tier — Park auto (30–40 min for most students)

**Target:** robot drives from start position and parks in the Low Rubble Zone by end of autonomous. Worth 5 points guaranteed.

Students build `DriveDistance` and wire it into the AutoChooser as the default option.

```java
// In RobotContainer — default auto: drive to parking zone and stop
autoChooser.setDefaultOption("Park (5 pts)", new DriveDistance(drive, PARK_DISTANCE_METERS));
```

`PARK_DISTANCE_METERS` goes in `Constants.java` — students will tune this in Lesson 07.

**Success criteria:** robot drives and stops. AutoChooser shows "Park (5 pts)". Run in sim first, verify in AdvantageScope that the command initializes, runs, and ends cleanly.

**Common Bronze struggles:**

| Struggle | Response |
|---|---|
| AutoChooser not visible in SmartDashboard | Look for `SmartDashboard/Auto Choice` in AdvantageScope sidebar |
| Robot doesn't stop | Bug #3 from the lab — `end()` is empty. *"What should happen to motors when the command ends?"* |
| Commands folder empty in AdvantageScope | `CommandScheduler.onCommandInitialize` not wired in `Robot.java` |

### Silver tier — Rubble scoring auto (30–40 min for students who finish Bronze)

**Target:** robot drives to the Low Rubble Zone, pauses to score preloaded rubble, then parks. Worth up to 6 points (1 per rubble + 5 park).

Students add a `TurnToAngle` command and compose a sequence:

```java
autoChooser.addOption("Score + Park (6 pts)",
    new SequentialCommandGroup(
        new DriveDistance(drive, SCORE_DISTANCE_METERS),
        new WaitCommand(0.5),   // pause to let rubble settle
        new DriveDistance(drive, PARK_DISTANCE_METERS - SCORE_DISTANCE_METERS)
    )
);
```

### Reference implementation — `TurnToAngle`

Have this ready but don't show it until a student has been stuck for 10+ minutes:

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

> **Gyro gotchas:**
> - `Math.signum(targetDegrees)` handles positive and negative angles correctly
> - Gyro might wrap around 360° for large angles — for the XRP's 90° turns this is not a problem, but flag it

### Gold tier — High Rubble Zone auto (remaining time)

**Target:** robot drives to High Rubble Zone (elevated platform, 2 pts per rubble vs 1 pt in Low Zone). Worth more points but harder to execute reliably.

Students add a second AutoChooser option that attempts the High Zone approach:

```java
autoChooser.addOption("High Zone (2 pts/rubble)",
    new SequentialCommandGroup(
        new DriveDistance(drive, HIGH_ZONE_APPROACH_METERS),
        new TurnToAngle(drive, HIGH_ZONE_ANGLE_DEGREES),
        new DriveDistance(drive, HIGH_ZONE_PUSH_METERS),
        new WaitCommand(0.3)
    ).withTimeout(28.0)  // must finish before 30-second auto ends
);
```

**Gold discussion question:** *"Your high zone auto is riskier than park. When is it worth the risk? What's the break-even point?"* Let students work out: if park is 5 pts guaranteed and high zone is 0 pts if it fails, you need to score at least 3 rubble to come out ahead. That's strategy, not just code.

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

## Phase 6 — Physical XRP Auto on the Field (150–170 min)

*First time students run their autonomous on the actual Orbit Odyssey field. Sim verified — now prove it on hardware.*

### Before running — sim verification gate

Every student must run their auto in sim and confirm it ends cleanly in AdvantageScope before getting field time. Not negotiable. This is the real workflow: sim first, hardware second.

### What students do

- Deploy code to XRP
- Place robot at starting position on the field
- Run their chosen auto (park or scoring routine)
- Watch where it stops — does it land in the zone?
- Pull the log, open in AdvantageScope, find the command sequence in the Commands folder
- Ask: *"Did the sim and hardware behave the same? If not, why not?"*

### What to watch for

- Students whose robot overshoots the parking zone — open loop issue, tease Lesson 07 fix
- Students whose robot stops short — kP or power too low, or encoder units bug from Lesson 04
- Students whose robot doesn't stop at all — bug #3 still in their code. Stop them immediately.
- Students who want to immediately change distances — remind them: *"Note it down, put the value in Constants.java, tune in Lesson 07. Don't restructure code on the field."*

> **The key discipline to introduce here**
>
> *"Write down your target distance and your actual stopping point. That gap is what Lesson 07 closes. Today we're proving the command structure works — not that the numbers are perfect yet."*

---

## Phase 7 — Strategy Discussion + Wrap (170–180 min)

*Commands are working. Students have a park auto running. Now connect code choices to strategy choices.*

### Strategy discussion (8 min)

Ask the whole group:

> *"You now have a working park auto worth 5 guaranteed points. Your AutoChooser has options. Here's the question: when would you choose the risky high zone auto over the safe park auto?"*

Let students debate. Seed it if needed:
- *"What if your alliance partner can definitely park? Do you still park?"*
- *"What if your rubble-scoring routine only works 60% of the time? Is that better than guaranteed park?"*
- *"What does 'reliable' mean for an autonomous routine?"*

Don't resolve it — this is the question they'll be answering with data in Lesson 07.

### Exit check (2 min)

Two questions before packing up:

1. *"Name the four methods of a command."*
2. *"Your park auto overshoots by 10cm. Which file do you change, and what do you change in it?"* (Answer: `Constants.java`, update `PARK_DISTANCE_METERS`. Not the command class.)

### Teaser for Lesson 07

> *"Your park auto stops in roughly the right place. Sometimes. The problem is it's open loop — you set a power and hope. Battery voltage changes, floor friction changes, the robot doesn't care. Next session we close the loop: the robot measures where it is and adjusts every 20ms until it's exactly where you told it to be. Same four-method command structure. Same AutoChooser. Just smarter math in `execute()`."*

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
