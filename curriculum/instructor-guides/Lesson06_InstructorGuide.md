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
| **Session length** | 45 minutes |
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
- A complete reference implementation of `TurnToAngle`, in case students need a tutorial walk-through
- Tape on the floor marking 1m and 2m gridlines so students can verify auto distances visually

> **The most important instructor mindset for this lesson**
>
> This is the lesson where students stop being told what to write and start writing their own commands. Resist the urge to dictate. When a student's `TurnToAngle` doesn't work, ask *"which of the four methods is wrong?"* before showing them the answer. Most bugs at this stage are 'isFinished always false' or 'forgot to stop in end' — the broken robot lab covers both, and the more students hit those bugs themselves, the better they'll remember.

---

## Session Timing

| Time | Phase | You do | Students do |
|---|---|---|---|
| **0–5 min** | **Hook** | Run a working auto routine on the projector. Then run one with a missing `isFinished`. Ask which is which. | Watch. Predict. Realize the difference is one method. |
| **5–15 min** | **Concept** | Walk through the four methods of Command. Read `DriveDistance.java` line-by-line. Cover `addRequirements`. | Follow on digital handout. Match each method to its purpose. |
| **15–25 min** | **Composition** | `SequentialCommandGroup`, `ParallelCommandGroup`, decorators. Show AutoChooser wiring on projector. | Replicate AutoChooser setup. Add an option. |
| **25–40 min** | **Practice** | Circulate during tiered challenge. Push Bronze finishers to Silver. Catch the four common bugs early. | Bronze: run existing auto. Silver: write `TurnToAngle`. Gold: compose L-shape. |
| **40–45 min** | **Lab + connect** | Walk through broken robot lab. Tease Lesson 07 (sensors close the loop on these commands). | Find the 3 bugs in the lab. Predict what each would look like in AdvantageScope. |

> **20-minute compressed version**
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

## Phase 2 — Concept (5–15 min)

*Three things to teach: the four lifecycle methods, why subsystem requirements matter, why commands beat `autonomousPeriodic`.*

### The four methods of a Command

Open `DriveDistance.java` on the projector. Walk through it method by method, asking students to name each one's job before you reveal it.

- `initialize()` — *"What's special about the first cycle?"* — record the start position
- `execute()` — *"What runs forever while we're driving?"* — set the motors
- `isFinished()` — *"How do we know we're there?"* — compare current to start
- `end()` — *"What do we do when we stop?"* — stop the motors, always

> **The line that has to land**
>
> ***"`end()` always runs. Even if the command was interrupted, even if it never reached its target, `end()` runs. Use it to put the subsystem in a safe state. If you don't, the motors keep their last setpoint forever and the robot keeps driving."***
>
> *This is bug #2 in the lab. Drill it now and the lab finds it for itself.*

### `addRequirements()` — why it matters

Two commands wanting the same subsystem at once is a recipe for chaos. `addRequirements` declares ownership; the scheduler enforces it. Skip this and you get random motor commands as commands fight.

*If you have time: demonstrate. Schedule two commands that both write to the drivetrain in `execute()`. Show the robot doing nothing useful. Add `addRequirements`; show the scheduler interrupting the first when the second starts.*

### Why this beats `autonomousPeriodic`

Quickly hit the four wins: composable, interruptible, reusable, loggable. Don't dwell here. Students who care will ask. Students who don't will see it in Phase 3.

---

## Phase 3 — Composition (15–25 min)

*Where the framework's actual power shows up. Demo on the projector.*

### `SequentialCommandGroup` demo

- Open `RobotContainer.java`. Add a method that returns `new SequentialCommandGroup(driveDist, turn, driveDist)`
- Run it in sim. Watch the robot draw an L.
- Open AdvantageScope. Show the Commands folder with three back-to-back command init/end events.
- **Make a teaching point:** each child has its own four methods. The group manages who runs when.

### Parallel groups — quick mention

Show `ParallelCommandGroup`, `ParallelDeadlineGroup`, `ParallelRaceGroup`. Don't go deep — students will reach for these in real team code, not in this lesson. Make sure they know:

- `ParallelCommandGroup`: all run, ends when all finish
- `ParallelDeadlineGroup`: all run, ends when first one finishes
- `ParallelRaceGroup`: all run, ends when any finishes
- Two parallel commands cannot share a subsystem

### Decorators — quick demo

Show how `a.andThen(b)` is the same as `new SequentialCommandGroup(a, b)`. Show `.withTimeout(3.0)`. Mention these read better and you'll see them in real code. Don't drill.

### AutoChooser wiring

This is what makes autonomous practical at competition. Walk through the `SendableChooser` pattern in `RobotContainer.java`:

- Create the chooser as a field
- In the constructor: `setDefaultOption` + `addOption` + `putData`
- Expose `getAutonomousCommand()` that returns `autoChooser.getSelected()`
- In `Robot.java`, `autonomousInit()` schedules whatever `getAutonomousCommand()` returns

*Most of this is already in the starter project. Show students where it is and what to add an option to.*

---

## Phase 4 — Practice (25–40 min)

*Tiered challenge: Bronze (run existing auto), Silver (write `TurnToAngle`), Gold (compose L-shape). Push students upward.*

### What to circulate for

- **Bronze:** students who can't find the AutoChooser in SmartDashboard — show them where it appears (often hidden if they've never opened SmartDashboard before)
- **Silver:** students whose `TurnToAngle` never ends — they probably have the gyro sign wrong, or are checking the wrong direction in `isFinished`. Magic phrase: *"What's your start angle? What's your current angle? When should you stop?"*
- **Silver:** students whose `TurnToAngle` ends instantly — they probably forgot to record `startDegrees` in `initialize`, so the math is `current - 0 = current`, which already exceeds the target
- **Gold:** students who used `ParallelCommandGroup` by accident — exactly the bug in the lab. Let them discover it, then point at line 3 of the lab code

### The high-leverage question

When a student says *"my command isn't working,"* never ask *"what's wrong?"* Ask *"which of the four methods has the bug?"* Force them to localize. Eight times out of ten, they say it themselves: *"I think `isFinished` is wrong."* That self-diagnosis is the point of the framework.

---

## Phase 5 — Lab + Connect (40–45 min)

*Walk the broken robot lab on the projector. Each bug is a teaching moment.*

### Broken robot lab — answers

Three bugs. Two are in `DriveDistance`, one is in the composition. Different parts of today's lesson:

#### Bug 1 — `ParallelCommandGroup` instead of `SequentialCommandGroup`

Line 3: the group type is wrong. `ParallelCommandGroup` tries to run all three children at once. Two of them require the drivetrain. The scheduler refuses to run two commands sharing a subsystem in parallel. The group fails to start, or one child runs while the others are silently rejected. Students see *"the robot drives once but never turns."*
**Fix:** change `ParallelCommandGroup` to `SequentialCommandGroup`.

#### Bug 2 — `isFinished` returns `false` forever

Line 25: the command never reports it's done. `execute()` keeps running, motors keep getting set to `0.5`, the robot drives until the simulation timeout or until it crashes into a wall. The next command in the sequence (`TurnToAngle`) never starts.
**Fix:** return a comparison between the current position and the target.

#### Bug 3 — `end()` doesn't stop the motors

Line 26: `end()` is empty. When the command finishes (after fixing bug 2) or gets interrupted, the motors keep their last setpoint of `0.5`. The next command might re-set them, but if it doesn't, the robot keeps driving. The fix is one line: `drive.stop()`.
**This is THE bug to drill — every team's first auto has this bug, every season.**

### Connect — what's next

> **Teaser for Lesson 07**
>
> *"Today's commands work because we time things by encoder distance — the gyro and encoder are reading. Next time, we close the loop: instead of 'drive at 0.5 power until 1 meter', we say 'drive at exactly 1 m/s, with PID feedback, until exactly 1 meter'. The same four-method structure. The same composition. Just smarter `execute()`."*

---

## Common Student Questions

**Q: Why doesn't the robot stop right at 1 meter? It overshoots.**
A: *"Because the command is open-loop — it just sets motors to 0.5 power and waits for the encoder to hit 1m. By the time the encoder reaches 1m, the robot has momentum. Lesson 07 fixes this with feedback control. For now, an auto that ends at 1.05m is fine."*

**Q: My SequentialCommandGroup feels weird — why are commands inside another command?**
A: *"That's the recursion. A `SequentialCommandGroup` IS a `Command`. So you can put one inside another. You can build very complex routines this way without any new framework — just nesting. This is why we say 'commands compose.'"*

**Q: When do I use a Command class vs an InstantCommand lambda?**
A: *"`InstantCommand` is for one-line actions: 'reset gyro,' 'open intake.' Command class is when you have state, want to track progress, or care about the `end()` cleanup. Rule of thumb: if you'd write more than 5 lines of action, make it a class."*

**Q: What if I want my command to run forever — like a default command?**
A: *"Then `isFinished` can return `false`. Default commands are the exception to Rule 1. The scheduler interrupts them when another command needs the subsystem, so they end via interruption, not via finishing."*

**Q: My auto works in sim but not on the XRP. Why?**
A: *"Most likely: encoder units. The XRP gives positions in inches; sim might give meters. Check `getLeftPositionMeters()` and confirm it's actually meters on hardware. This is the unit bug from the Lesson 04 reference card."*

---

*Instructor Edition — Not for student distribution*