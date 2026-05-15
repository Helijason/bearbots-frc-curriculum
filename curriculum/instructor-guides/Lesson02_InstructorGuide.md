# FRC Programming Curriculum — Module 2, Lesson 02

# WPILib Template Structure and File Roles

*Understanding the WPILib project template, file responsibilities, and the simulator.*

> **Instructor Edition — Not for student distribution**

---

## At a Glance

| Field | Detail |
|---|---|
| **Target audience** | HS freshmen & sophomores, new to FRC |
| **Hardware** | None — VSCode and simulator only |
| **Session length** | 3 hours |
| **Key tools** | VSCode command palette, WPILib sim, AdvantageScope |

---

## Learning Objectives

- Students can name every file in the WPILib template and state its job in one sentence
- Students can use the WPILib command palette to build, simulate, and create new classes
- Students can launch the simulator, connect AdvantageScope, and drive using the keyboard or a game controller
- Students can explain why `LoggedRobot` is used instead of `TimedRobot`
- Students can move a hardcoded value into `Constants.java` and verify nothing breaks
- Students can add a logged output and find it by name in AdvantageScope
- Students can find and fix at least two bugs in a broken robot project

---

## Before You Start

### Room setup

- VSCode open on projector with a freshly generated WPILib project
- AdvantageScope installed on instructor laptop and all student laptops
- Student laptops have WPILib 2024 installed
- Digital handout open in browser: `lesson-01-vscode-template.html`

> **The most important instructor mindset for this lesson**
>
> Resist the urge to skip the file tour. Students who don't understand the template will spend the rest of the season editing the wrong files. 20 minutes of foundation here prevents hours of confusion later.

---

## Session Timing

| Time | Phase | You do | Students do |
|---|---|---|---|
| 0–5 min | **Hook** | Open fresh project. Count the files. Ask: what is all this? | Explore the file tree. Guess what each file does. |
| 5–30 min | **File tour** | Walk through each file. Click to expand on projector. Think out loud. | Follow along. Ask questions. Note anything surprising. |
| 30–60 min | **Simulator** | Live demo: launch sim, connect AdvantageScope, drive with keyboard. | Watch the demo, then replicate it on their own laptop. |
| 60–90 min | **Constants scavenger hunt** | Seed the starter project with misplaced magic numbers. Circulate. | Find hardcoded values in wrong files. Move them to `Constants.java`. Rebuild and verify. |
| 90–110 min | **"Add your name to the robot"** | Demo: add a string constant, log it with `Logger.recordOutput`, find it in AdvantageScope. | Add their own name constant. Verify it appears live in AdvantageScope. |
| 110–140 min | **Graph racing** | Facilitate. Call out interesting moments. Ask "what do you expect?" before each run. | Take turns driving. Add logged values to a shared graph. Experiment with patterns. |
| 140–160 min | **Controller Bingo / "What's the Robot Thinking?"** | Run the activity. For Bingo: print cards. For guessing game: drive a hidden pattern. | Controller Bingo: match axis/button values to squares. Guessing game: sketch what the robot did from graphs alone. |
| 160–175 min | **Broken robot lab** | Circulate. Redirect with questions, not answers. | Find and fix three bugs in a broken project independently. |
| 175–180 min | **Connect + wrap** | Open the Lesson 04 starter project. Show how the template grew into structure. | Recognize the template files in a real project. |

> **Activity notes**
>
> Controller Bingo and "What's the Robot Thinking?" are alternatives — pick one based on student energy and available controllers. Bingo works better early in the block; the guessing game works better as a closer. Both can be cut if the scavenger hunt or graph racing runs long — they are enrichment, not essential. The broken robot lab should always happen.

> **If running short**
> The scavenger hunt and graph racing are the highest-value new activities. Cut Controller Bingo first, then "Add your name," keeping the broken robot lab intact.

---

## Phase 1 — Hook (0–5 min)

### Opening

Open a fresh WPILib project on the projector. Don't say anything. Just scroll through the file tree slowly. Let students see the files. Then ask:

> **Script**
>
> *"VSCode just created these files. You didn't write any of them. Before we touch anything — does anyone want to guess what each one does?"*
>
> Wait for guesses. Even wrong guesses are useful — they tell you what students already know. Validate the good ones. Defer the rest to the file tour.

---

## Phase 2 — File Tour (5–15 min)

### Walking through each file

For each file: open it on the projector, explain its job in one sentence, explain what breaks if it's missing, and explain the one thing students will most likely get wrong about it.

### `Main.java`

- **Job:** entry point. Calls `startRobot(Robot::new)`. That's all it does.
- **Missing:** robot doesn't start. Not even a compile error — just silence.
- **Most likely mistake:** adding code here. The comment says not to. People do it anyway.

### `Robot.java`

- **Job:** lifecycle manager. Contains `robotPeriodic()`, `autonomousInit()`, `teleopInit()`, etc.
- **Key point:** extends `LoggedRobot`, not `TimedRobot`. `LoggedRobot` extends `TimedRobot` — all the same methods work, plus AdvantageKit logging around each cycle.
- **Most important line:** `CommandScheduler.getInstance().run()` in `robotPeriodic()`. Without it, no commands ever execute.
- **Most likely mistake:** removing the CommandScheduler call or recreating `RobotContainer` in `teleopInit()`.

### `RobotContainer.java`

- **Job:** the switchboard. Creates subsystems. Wires buttons to commands. Provides auto command.
- **Missing:** robot builds but no subsystems exist. Nothing responds to input.
- **Most likely mistake:** putting subsystem logic here instead of in subsystem classes.

### `Constants.java`

- **Job:** number vault. Motor IDs, speeds, PID gains, the Mode enum for AdvantageKit.
- **Missing:** constants are hardcoded in five different files. One wiring change breaks everything.
- **Most likely mistake:** not using it at all, then spending 2 hours finding hardcoded motor ID 4 when it should be 5.

> **The `LoggedRobot` vs `TimedRobot` question**
>
> Students will ask about this. The answer: `LoggedRobot` extends `TimedRobot`. Same lifecycle methods, same timing. AdvantageKit adds a logging wrapper around each cycle. The command framework isn't a base class — it's opt-in through `CommandScheduler.run()` in `robotPeriodic()`.

---

## Phase 3 — Simulator Demo (15–30 min)

### Live simulator walkthrough

Do this live on the projector. Students follow along on their own laptops. Go slowly — this workflow is new and every step matters.

#### Step 1 — Launch the simulator

- `Ctrl+Shift+P` → WPILib: Simulate Robot Code
- When prompted: check `halsim_gui`, click OK
- Wait for build. Simulation GUI opens automatically.

#### Step 2 — Set up keyboard driving

- In Simulation GUI → Joysticks panel
- Drag 'Keyboard 0' to `Joystick[0]` slot
- Robot State panel → Teleoperated → Enable
- Click back on Simulation GUI (keyboard only works when this window is focused)

#### Step 3 — Connect AdvantageScope

- Open AdvantageScope
- File → Connect to Simulator (or `Ctrl+K`)
- Left panel shows log key tree
- Connect BEFORE enabling the robot — otherwise first seconds of data are lost

#### Step 4 — Drive and observe

- Press `W` to drive forward, `S` backward, `A`/`D` to turn
- In AdvantageScope: find `Drive/` folder, drag `LeftPositionMeters` to graph
- Watch the graph update as the robot moves
- Ask: *'What happens to the graph when you spin in place?'*

> **Keyboard default mappings**
>
> - `W` — Forward (Left stick Y negative)
> - `S` — Backward (Left stick Y positive)
> - `A` — Turn left (Left stick X negative)
> - `D` — Turn right (Left stick X positive)

> **If a student has a real controller**
>
> Plug it in before launching sim. It appears automatically in the Joysticks panel. Drag to `Joystick[0]`. Left stick Y = forward/back, Left stick X = turn. Confirm by watching axis values move in the panel.

> **Common simulator mistakes to watch for**
>
> - Robot not enabled — nothing moves, students think code is broken. Check Robot State panel.
> - AdvantageScope not connected — graphs show nothing. Connect before enabling.
> - Keyboard not working — Simulation GUI window must be focused. Click it.

---

## Phase 4 — Constants Scavenger Hunt (60–90 min)

*Students learn where things go by finding things in the wrong place.*

### Setup

Before class, seed the starter project with misplaced values — motor IDs in `Robot.java`, a drive speed hardcoded in `RobotContainer`, a PID gain buried in a comment. Students get this version.

### What students do

- Find every hardcoded number or string that doesn't belong where it is
- Move each one to `Constants.java` with a descriptive name
- Rebuild. Verify `BUILD SUCCESSFUL`. Verify behavior in sim is unchanged.

> **What to say**
>
> *"A future teammate — or future you — is going to need to change the drive speed at 11pm before a competition. If it's buried in `RobotContainer` line 47, good luck. If it's `Constants.DRIVE_SPEED`, it takes 10 seconds."*

### Common struggles

| Issue | Response |
|---|---|
| Student isn't sure something counts as a magic number | Ask: "Would a new teammate know what that number means without context?" |
| Student breaks the build moving a constant | Walk through the import or reference error — this is a useful mistake |
| Student finishes early | Ask them to add two new constants that don't exist yet but probably should |

---

## Phase 5 — "Add Your Name to the Robot" (90–110 min)

*First time a student's code produces visible output in a real data stream.*

### What students do

- Add a `public static final String PILOT_NAME = "YourName";` to `Constants.java`
- In `Robot.java` or `RobotContainer.java`, add: `Logger.recordOutput("Pilot", Constants.PILOT_NAME);`
- Run the simulator. Open AdvantageScope. Find `Pilot` in the log tree.

### Why this works

It's silly, but every student sees their name appear in a robot data stream for the first time. The concept — that anything you log shows up in AdvantageScope — becomes concrete and personal before they need to rely on it for debugging.

> **Extension**
> Ask students to also log the current timestamp or a random number. Watching a value update live in AdvantageScope every 20ms is more memorable than any explanation of the logging loop.

---

## Phase 6 — Graph Racing (110–140 min)

*Competitive enough to be fun. Teaches graph reading as a side effect.*

### What students do

- Each student adds one logged value to a shared AdvantageScope graph: left velocity, right velocity, heading, or a value of their choosing
- Students take turns driving the simulated robot while the rest of the class watches the graph
- Between turns, instructor asks: *"What do you expect the graph to do if they spin in place? Floor it and brake? Drive a perfect square?"*

### Facilitation notes

- Keep turns short — 60–90 seconds each
- After each run, ask the driver: "Did the graph match what you expected?"
- The most interesting moments are mismatches — student expects symmetry, gets asymmetry. That's a conversation about the robot, not a failure.

> **If a student has a real game controller**
> Plug it in before launching sim. It appears automatically in the Joysticks panel. Drag to `Joystick[0]`. This is worth doing live in front of the class — the plug-and-play moment is satisfying.

---

## Phase 7 — Controller Bingo / "What's the Robot Thinking?" (140–160 min)

*Pick one based on student energy and available hardware.*

### Option A — Controller Bingo

Print bingo cards with axis/button values (e.g., "Left stick Y > 0.8", "Button 3 pressed", "Both triggers held"). Students plug in a controller and watch raw values in the Simulation GUI joystick panel. First to complete a row wins.

- Works best with multiple controller types — different controllers map differently
- Teaches controller mapping without any lecture
- Prep: generate bingo cards before class

### Option B — "What's the Robot Thinking?"

Instructor drives a secret pattern (figure-8, square, stop-and-go) while students watch only the AdvantageScope graphs — no simulator window visible. Students sketch what they think the robot did. Then reveal and compare.

- Teaches graph literacy directly
- Best conceptual bridge to Week 5 (replay mode) — logs are the robot's memory
- No prep required beyond a planned driving pattern

> **If time is short, cut this phase entirely.** The broken robot lab is more essential.

---

## Phase 8 — Broken Robot Lab (160–175 min)

*Students find and fix three bugs in a broken project independently. Redirect with questions, not answers.*

### Broken robot lab answers

- **Bug 1:** `extends TimedRobot` — should be `LoggedRobot`
- **Bug 2:** `CommandScheduler` never called in `robotPeriodic()` — no commands run
- **Bug 3:** `RobotContainer` recreated in `teleopInit()` — destroys all subsystems and bindings

---

## Phase 9 — Connect + Wrap (175–180 min)

### Connect Show students the same files they just learned about — now with AdvantageKit wired in. Ask: which parts look familiar?

- `Main.java` — identical to template
- `Robot.java` — same structure, plus Logger setup block
- `Constants.java` — same structure, plus Mode enum
- `RobotContainer.java` — more complete, but same job

> **Teaser for Lesson 03**
>
> *"Next lesson we figure out what goes in those subsystem files — and why putting everything in `Robot.java` is a terrible idea that always sounds fine until it isn't."*

---

*Instructor Edition — Not for student distribution*