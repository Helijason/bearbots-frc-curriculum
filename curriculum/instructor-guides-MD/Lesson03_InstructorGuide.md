# FRC Programming Curriculum — Module 1, Lesson 03

# What Is a Subsystem?

*Subsystem structure, WPILib tools, simulator verification, AdvantageScope.*

> **Instructor Edition — Not for student distribution**

---

## At a Glance

| Field | Detail |
|---|---|
| **Target audience** | Students who completed Lesson 02 |
| **Hardware** | None — VSCode and simulator only |
| **Session length** | 3 hours |
| **Key tools** | WPILib: Create a new class, Simulator, AdvantageScope |

---

## Learning Objectives

- Students can explain what a subsystem is and why robots use them
- Students can identify subsystem boundaries from a robot description — what deserves its own file and what doesn't
- Students can create a subsystem file using the WPILib tool and explain what the tool does and does not generate
- Students can add AdvantageKit structure on top of the WPILib-generated shell (`@AutoLogOutput`, logging loop)
- Students can register a subsystem in `RobotContainer` and verify it loads in simulation
- Students can explain why motor control belongs in commands, not `periodic()`
- Students can explain the relationship between `LoggedRobot`, `TimedRobot`, and the command framework
- Students can find and fix subsystem ownership bugs in a broken robot project

---

## Before You Start

### Setup

- Lesson 02 starter project open in VSCode on projector
- Simulator confirmed working from Lesson 02
- AdvantageScope confirmed connecting from Lesson 02
- Digital handout open: `lesson-03-subsystems.html`

> **The most important hook for this lesson**
>
> Show two projects side by side: one with 600 lines of `Robot.java` containing everything, one with proper subsystems. Ask which one they'd rather debug at 11pm. Don't explain subsystems yet — let the comparison create the need.

---

## Session Timing

| Time | Phase | You do | Students do |
|---|---|---|---|
| 0–10 min | **Hook** | Side-by-side comparison: monolithic vs structured. Count the lines. Ask which they'd rather debug at 11pm. | Look at both. Form opinions. Argue. |
| 10–25 min | **Concept** | Cafeteria analogy. `periodic()` vs commands table. `CommandScheduler` relationship. | Follow along. Ask questions. |
| 25–55 min | **"Design the Robot" whiteboard** | Present Orbit Odyssey game. Facilitate the boundary debate — don't settle it too fast. Reveal BearBots robot design at end. | Whiteboard which subsystems they'd create. Justify every boundary decision. Argue about edge cases. |
| 55–80 min | **Tools demo** | Live demo: create subsystem with WPILib tool. Show what it generates and what it doesn't. Add AdvantageKit structure on top. Register in `RobotContainer`. Run sim. Verify in AdvantageScope. | Replicate on their own laptop. Verify subsystem folder appears. |
| 80–120 min | **Bronze/Silver/Gold practice** | Circulate. Ask "what do you expect?" before every run. Redirect with questions, not answers. | Bronze: identify + create. Silver: add `@AutoLogOutput` and verify in AdvantageScope. Gold: full architecture design from scratch. |
| 120–150 min | **Broken robot lab** | Circulate. Don't give answers — give direction. Require sim confirmation for every fix. | Find and fix the three bugs. Must run the sim to confirm each fix, not just read the code. |
| 150–165 min | **`@AutoLogOutput` race** | Facilitate. Keep energy up. | Add as many logged fields to their subsystem as possible. Race to get the most values showing in AdvantageScope. |
| 165–175 min | **Peer code review** | Prompt the review questions. Circulate. | Swap laptops. Try to register a partner's subsystem in `RobotContainer`. Find what's missing or wrong. |
| 175–180 min | **Connect + wrap** | Pull up real `Indexer.java` from team code. Ask three questions. Tease Lesson 04. | Recognize the pattern in competition code. |

> **Activity notes**
>
> The "Design the Robot" whiteboard is the highest-value new activity — protect it if time gets tight elsewhere. The `@AutoLogOutput` race comes after the hardest cognitive work of the session and should feel like a game, not an assignment. The peer code review is short but high-value — teaching something is the best way to solidify it.

> **If running short**
> Cut the `@AutoLogOutput` race first, then peer code review. Never cut the broken robot lab — students must confirm fixes by running the sim, not just reading the code.

---

## Phase 1 — Hook (0–10 min)

### Side-by-side comparison

Prepare two projects before class:

> **Project 1 — monolithic:** A `Robot.java` with 600+ lines containing drivetrain logic, shooter logic, intake logic, and autonomous all in one file. Real teams have written code like this.
>
> **Project 2 — structured:** The same robot behavior split into proper subsystems. Each file is under 100 lines. `Robot.java` is nearly empty.

Open both on the projector. Scroll slowly through the monolithic version. Count the lines out loud. Then ask:

> **Script**
>
> *"It's 11pm. Your autonomous isn't working. Which of these would you rather debug?"*

Don't explain subsystems yet. Let the comparison create the need. Students who argue for the monolithic version are doing you a favor — ask them to defend it. The debate is the lesson.

---

## Phase 2 — Concept (10–25 min)

### The cafeteria analogy

Use this before showing any code. Students need the mental model first.

> **Script**
>
> *"Imagine your school cafeteria. Pizza station, salad bar, dessert section. Each one does its job. If the pizza oven breaks, the ice cream is fine. Your robot works the same way — each subsystem owns one mechanism. If the shooter breaks, the drivetrain keeps driving."*

### The `LoggedRobot` and command framework question

Students from Lesson 02 will ask about this. Address it directly:

> **Inheritance chain:** `Robot` extends `LoggedRobot` extends `TimedRobot`
>
> **Command framework is NOT a base class.** It runs because of this one line in `robotPeriodic()`:
> ```java
> CommandScheduler.getInstance().run()
> ```
> Remove that line = no commands ever execute.
>
> **AdvantageKit and command-based are two separate systems** that work together through that one method call. You could have a `TimedRobot` with no commands at all — command-based is a pattern we choose to use by running the scheduler.

### `periodic()` vs commands

This distinction trips up students all season. Make it explicit:

| `periodic()` | Commands |
|---|---|
| Runs every 20ms regardless | Runs when scheduled |
| Read sensors | Control motors |
| Log data to AdvantageKit | Respond to button presses |
| Update alerts / state | Run autonomous actions |
| Cannot be stopped | Can be interrupted |

### Common student questions

**Q: Can a subsystem control two mechanisms?**
Technically yes. It's almost always a bad idea. If two mechanisms are so tightly coupled that they must always be controlled together, they might belong in one subsystem. Otherwise separate them.

**Q: How does a subsystem communicate with another subsystem?**
Through commands in RobotContainer. Subsystems don't talk to each other directly — that would create dependencies that make debugging much harder. Commands coordinate between subsystems.

---

## Phase 3 — "Design the Robot" Whiteboard (25–55 min)

*Students decide what deserves to be a subsystem before they write any code. The debate is the lesson. This session uses Orbit Odyssey — the game they will compete in — as the design target.*

### Setup

- Orbit Odyssey game manual on projector (field diagram visible)
- Remind students of the pair brainstorm from Lesson 02: *"Last session you listed what the robot needs to do. Let's use that."*
- Whiteboard cleared and ready

### Round 1 — Pairs brainstorm (10 min)

Each pair works independently first. Prompt:

> *"Based on the Orbit Odyssey game, what mechanisms does this robot need? Write down every physical system — not code, not files — just the things that move or sense."*

**Circulate with these prompts if pairs stall:**
- *"What does the robot need to do in autonomous to score?"* (navigate, park, score rubble)
- *"How does it pick up or carry the amplifier?"* (some kind of intake or holder)
- *"How does it deliver rubble to the High Rubble Zone?"* (needs to lift — elevator)
- *"What's on the back of the robot?"* (arm — for game piece control or endgame)

**Expected outputs from pairs:** drivetrain, some kind of intake/scoop, something that lifts, maybe an arm. Let them arrive at these — don't name them yet.

### Round 2 — Group share-out and subsystem mapping (15 min)

Pairs share. Write every mechanism on the whiteboard without editing. Then facilitate:

> *"We have a list of mechanisms. Now let's group them. Which of these are separate enough to get their own file?"*

**The productive debates to let run:**
- *"Does the scoop that carries the amplifier need its own subsystem, or is it part of the drivetrain?"* — It's separate. It can fail without affecting driving.
- *"Does the thing that lifts need its own file separate from the thing that scoops?"* — Yes. One job each.
- *"Does the drivetrain own the encoders and gyro?"* — Yes. Sensors belong to the subsystem that reads them.

> **The question that cuts through every edge case**
>
> *"If this mechanism broke completely, what else on the robot would stop working?"*
> If the answer is "nothing else," it's a good subsystem boundary.

> **What to watch for**
>
> Students who want one subsystem for everything — push back: *"So if your scoop breaks, you can't drive?"*
> Students who want a subsystem for every motor — push back: *"The elevator moves one thing. Does it matter how many motors do it?"*

### What the whiteboard should converge toward

Don't force it — but guide the debate until the board shows something close to:

```
DriveSubsystem      — moves the robot, owns encoders and gyro
ElevatorSubsystem   — lifts the scoop mechanism up and down
ScoopSubsystem      — tilts to retain or dump game pieces
ArmSubsystem        — rear arm for game piece control
```

If students arrive at this naturally: perfect. If they're close but not quite: *"Look at what you have. Does each of these have exactly one job?"*

---

## Phase 4 — Tools Demo (55–80 min)

### What the WPILib tool actually generates

Be honest about this upfront. The tool creates a correct but minimal shell:

```java
package frc.robot.subsystems;  // matches your folder structure

import edu.wpi.first.wpilibj2.command.SubsystemBase;

public class Indexer extends SubsystemBase {

    public Indexer() {
        // Constructor — runs once when subsystem is created
        // Good place to configure hardware (motors, sensors)
    }

    @Override
    public void periodic() {
        // Runs every 20ms (50Hz)
        // Read sensors, log data, update state
        // DO NOT put motor control here — use commands
    }
}
```

It gives you: correct package declaration, `SubsystemBase` extension, empty constructor, empty `periodic()`.

It does NOT give you: IO interface, inputs struct, `@AutoLog`, `Logger.processInputs()`, or any AdvantageKit imports.

> **What to say**
>
> *"The tool gets you started in the right place. Everything AdvantageKit-related — the logging, the IO pattern — we add on top. Think of the tool as 'correct blank page,' not 'finished subsystem.'"*

> **Forward reference — snippets coming**
>
> Once the global VS Code snippet file is set up, students will use `aksubsystem` + Tab instead of the WPILib tool and get the full AdvantageKit-ready structure in one step. For now, we build it manually so students understand what each piece is for.

### Live demo steps

- Right-click `subsystems/` folder in Explorer → Create a new class/command → `SubsystemBase`
- Alternatively: `Ctrl+Shift+P` → `WPILib: Create a new class` → `SubsystemBase`
- Name it `Indexer`. Show the generated file. Point out what's there and what's missing.
- Add `@AutoLogOutput` to a field. Add `Logger.processInputs()` to `periodic()`. Show the imports needed.
- Open `RobotContainer`. Add: `private final Indexer indexer = new Indexer();`
- Build: `Ctrl+Shift+P` → WPILib: Build Robot Code. Must succeed.
- Simulate. Connect AdvantageScope. Enable in Teleop.
- Drive with keyboard (W/A/S/D). Watch AdvantageScope for the Indexer folder.

### Simulator verification workflow

Teach this as a standard habit: after every structural change, verify in sim before adding logic.

1. Build succeeds → no compile errors
2. Sim launches → no runtime errors in System Console
3. AdvantageScope connects → subsystem folder appears in log tree
4. Enable and drive → `Drive/LeftPositionMeters` updates in AdvantageScope graphs

> **AdvantageScope verification for subsystems**
>
> If the subsystem folder doesn't appear in AdvantageScope after enabling: check that `Logger.processInputs()` is called in `periodic()`, AND that the subsystem is instantiated in `RobotContainer` (not just declared).

---

## Phase 5 — Practice (80–120 min)

### Instructor notes by tier

#### Bronze — identify and create

Students identify subsystems from a robot description (drivetrain, flywheel shooter + angle servo, ball sensor, LED strip), then create one using the WPILib tool and add it to `RobotContainer`. Watch for: students trying to create files by hand, putting too many mechanisms in one subsystem, or treating sensors as their own subsystem.

> **Key teaching point for Bronze:** a sensor belongs inside whichever subsystem reads it — it doesn't get its own subsystem.

#### Silver — add AdvantageKit structure

Students take their Bronze subsystem and add `@AutoLogOutput` to at least two fields, verify they appear in AdvantageScope, and confirm `Logger.processInputs()` is in `periodic()`. If students get stuck: *"Add `@AutoLogOutput` directly above the field declaration. Rebuild. Then look for it in AdvantageScope."*

Silver also adds: an `IndexerGoal` enum (`IDLE`, `ACTIVE`), a `setGoalCommand()` method, and a controller button binding. Goal should appear in AdvantageScope as `IndexerSubsystem/Goal`.

#### Gold — full architecture design

Students design a complete subsystem architecture for a given robot description — not just one subsystem but all of them, with justified boundary decisions. Key Gold insight: subsystems coordinate through commands, not direct method calls. Don't rush Gold students to implementation. The design document is the deliverable.

---

## Phase 6 — Broken Robot Lab (120–150 min)

*Students find and fix three bugs. Every fix must be confirmed by running the sim — reading the code is not enough.*

### Broken robot lab answers

- **Bug 1:** `indexerMotor` in `DriveSubsystem` — wrong ownership; when an indexer command runs, it requires `DriveSubsystem` and locks out drive commands
- **Bug 2:** motor control in `periodic()` — runs forever at full power, can't be stopped or interrupted by any command
- **Bug 3:** `runIndexer()` method in `DriveSubsystem` — method is on the wrong subsystem; any command calling it requires `DriveSubsystem`, preventing driving while indexing

> **Instructor approach**
>
> Don't give answers — give direction. Acceptable hints:
> - Bug 1: *"Which subsystem owns the indexer motor? Where does it live right now?"*
> - Bug 2: *"What happens to this motor call when teleop is disabled?"*
> - Bug 3: *"What subsystem does a command need to call `runIndexer()`? Is that the right one?"*

---

## Phase 7 — `@AutoLogOutput` Race (150–165 min)

*Low-stakes, energetic. Comes after the hardest cognitive work of the session — it should feel like a game.*

### What students do

- Add as many `@AutoLogOutput` fields to their subsystem as they can in 15 minutes
- Every field must actually appear in AdvantageScope to count
- Student with the most verified logged fields wins

### What to watch for

- Students logging meaningless values (a field that's always `0`) — push back: *"Would this help you debug anything?"*
- Students adding fields without rebuilding — remind them `@AutoLogOutput` requires a rebuild to take effect
- Good moment to introduce naming conventions: fields should be named so a teammate can tell what they mean without reading the code

---

## Phase 8 — Peer Code Review (165–175 min)

*Short but high-value. Teaching something is the best way to solidify it.*

### What students do

- Swap laptops with a partner
- Try to register the partner's subsystem in `RobotContainer` without asking for help
- Run the sim and verify it loads in AdvantageScope
- Report back: what was clear, what was confusing, what was missing

### What you do

- Prompt the review: *"Could you figure out what this subsystem does just by reading it?"*
- Listen for patterns — if multiple students report the same confusion, address it for the group

---

## Phase 9 — BearBots Robot Reveal + Wrap (175–180 min)

*The payoff for the whiteboard. Students designed a robot. Now they find out what the team actually decided — and why it matches.*

### The reveal

After the peer code review or `@AutoLogOutput` race wraps up, call the group together.

> **Script — the reveal**
>
> *"You spent the last 30 minutes arguing about what this robot needs. Drivetrain, something that lifts, something that scoops, something on the back. Here's what the BearBots team decided."*

Draw or show the BearBots robot diagram:

```
FRONT:  Scoop (servo-controlled tilt) mounted on Elevator (vertical lift)
REAR:   Arm (for game piece control)
BASE:   Drivetrain (tank drive, encoders, gyro)
```

> *"Notice anything? Your whiteboard and our design aren't that different. That's not a coincidence — the game tells you what the robot needs. You worked it out from first principles. We worked it out the same way, then built it and prototyped different intake concepts before landing on the scoop-on-elevator approach."*

**Ask the class:**
- *"What's different from what your pair had?"*
- *"Does anything about this design surprise you?"*
- *"Which subsystem do you think is the hardest to code?"*

Let the discussion run for 3–4 minutes. Don't resolve everything — leave questions open.

### Connect to Lesson 04

> **Teaser for Lesson 04**
>
> *"Next lesson you'll meet these subsystems in code. The elevator, the scoop, the arm — they'll all be files. And here's the twist: the subsystem file itself won't know what hardware it's running on. You'll find out why that's actually a great idea, and build the whole pattern from scratch. Bring your XRP."*

---

*Instructor Edition — Not for student distribution*
