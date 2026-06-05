# FRC Programming Curriculum — Module 2, Lesson 05

# How Do I Debug a Robot That Isn't Here?

*`@AutoLog`, the input/output split, AdvantageScope navigation, and replay mode.*

> **Instructor Edition — Not for student distribution**

---

## At a Glance

| Field | Detail |
|---|---|
| **Target audience** | Students who completed Lesson 04 and have driven the XRP |
| **Hardware** | XRP robot — same setup as Lesson 04 |
| **Session length** | 3 hours |
| **Key tools** | AdvantageScope, a saved log file, AdvantageKit annotations |

---

## Learning Objectives

- Students can explain what `@AutoLog` generates at compile time and why it matters
- Students can distinguish inputs (struct, `@AutoLog`) from outputs (field, `@AutoLogOutput`) and decide which to use for any given value
- Students can state the ordering rule (`updateInputs` before `processInputs`) and explain why it matters
- Students can navigate AdvantageScope: live mode, log mode, sidebar tree, time scrubbing, multiple visualization tabs
- Students can switch a project into REPLAY mode and run their code against a saved log

---

## Before You Start

### Room setup

- VSCode open on projector with the Lesson 04 starter project
- AdvantageScope open; a saved log from a prior session ready to demo (best: a log with visible bugs/anomalies)
- Digital handout open: `lesson-05-logging.html`
- Student laptops have XRPs available — a few will need to drive briefly during practice

### Have ready

- A real team's match log if you can get one — show students what a 2:30 of competition looks like in AdvantageScope
- A pre-broken `DriveSubsystem.java` matching the broken robot lab — for live triage

> **The most important instructor mindset for this lesson**
>
> Don't drown students in AdvantageScope features. The point of this lesson is the underlying discipline — log everything, log it in the right order, name your keys consistently. Once that's internalized, AdvantageScope's UI is just buttons. Cover the mechanics quickly; spend the bulk of class on why `@AutoLog` exists and why `processInputs` goes second.

---

## Session Timing

| Time | Phase | You do | Students do |
|---|---|---|---|
| **0–5 min** | **Hook** | Pull up a real match log. Find a moment where something looks wrong. Ask: how would you debug this? | Watch. Form ideas. Realize they need the log, not the robot. |
| **5–30 min** | **Concept** | Walk through `@AutoLog` code-gen, the input/output split, the ordering rule, three modes diagram. | Follow along on digital handout. Ask questions. |
| **30–75 min** | **AdvantageScope deep dive** | Live demo: open log, sidebar structure, visualization tabs, time scrubbing, replay mode. | Replicate on their own laptops with their own logs from Lesson 04. |
| **75–120 min** | **Practice** | Circulate during tiered challenge. Push students who finish Bronze toward Silver immediately. | Bronze: navigate a saved log. Silver: add a new logged input field. Gold: run replay mode. |
| **120–150 min** | **Broken robot lab** | Walk through broken robot lab on projector. Circulate during independent work. | Find the 3 bugs in the lab independently. Confirm each fix by checking AdvantageScope. |
| **150–165 min** | **Physical XRP drive + log** | Have students drive their XRP and save a real log for replay. | Drive, record log, open in AdvantageScope. Find at least one interesting moment. |
| **165–180 min** | **Connect + wrap** | Tease Lesson 06. Exit check. | 60-second exit check. Recognize why logging matters for autonomous. |

> **45-minute compressed version**
> Skip the AdvantageScope visualization tour and the physical XRP drive. Cover only `@AutoLog`, the order rule, and the lab. Assign the digital handout's tiered challenge as homework. Students will lose some AdvantageScope skill but retain the underlying discipline.

---

## Phase 1 — Hook (0–5 min)

*Frame the problem before introducing the solution.*

### Opening

Pull up a real-world match log on the projector — ideally one with a visible glitch (a sudden velocity drop, a brief disable, an autonomous that ran into a wall). Don't say what's wrong. Just scrub through it for 30 seconds and ask:

> **Script — what to ask**
>
> *"This robot did something weird at second 23. The match is over. The robot is in the truck on its way back to the school. How do you figure out what happened?"*
>
> Wait for answers. Most students will say things like *"plug it in and try again"* or *"have someone watch the next match"*. Let those answers sit.
>
> Then: *"Today we make sure you can answer that question without the robot in the room — using only the file the robot left behind."*

---

## Phase 2 — Concept (5–30 min)

*Three things to teach: what `@AutoLog` generates, the input/output split, and the ordering rule.*

### `@AutoLog` — the annotation processor

Open `DriveIOInputs.java` on the projector. Show students the `@AutoLog` annotation.

- Explain that `@AutoLog` is processed at compile time, not runtime
- The annotation processor generates a sibling class (`DriveIOInputsAutoLogged`) that extends yours and adds `toLog(LogTable)` and `fromLog(LogTable)` methods you never wrote
- If you have time: show the generated file in `build/generated/` — students don't need to read it, just see that it exists
- **Driving point:** if `@AutoLog` is missing, no `AutoLogged` class exists, no `toLog`/`fromLog`, no logging. Silent failure. AdvantageScope's Drive folder appears empty.

### Inputs vs outputs — two annotations, two purposes

> **The split, plain English**
>
> **Inputs** = things you read (sensors, button states). Wrap them in a struct, slap `@AutoLog` on the struct.
>
> **Outputs** = things you decide (target velocities, computed poses, mode names). Use `@AutoLogOutput` on a field, or call `Logger.recordOutput()` directly.
>
> *Test: "Did the world tell me this, or did my code decide this?" That's the question that picks the annotation.*

> **When to use which**
>
> Reading a sensor? It's an input. Goes in the Inputs struct.
> Computing a value from sensor readings? It's an output. `@AutoLogOutput` field, or `Logger.recordOutput("Drive/AveragePosition", value)` directly.
> Setting a motor voltage? The voltage you decided is an output (log it). The current the motor reports back is an input (log it via the inputs struct).
>
> Inputs and outputs go to different folders in the AdvantageScope sidebar. You'll see `RealOutputs/`, `ReplayOutputs/`, and the AdvantageKit-prefixed input folders.

### The ordering rule

This is the most important sentence of the lesson:

> **Say it out loud, twice**
>
> ***"`updateInputs` first. `processInputs` second. Always."***

```java
io.updateInputs(inputs);                  // Step 1: read hardware into struct
Logger.processInputs("Drive", inputs);    // Step 2: log the struct (or read from log in REPLAY)
```

If you swap them, you log whatever was in the struct from the previous cycle — or zeros on the first cycle. Your data is always one tick stale. Students will not notice this immediately. They will notice it three weeks later when odometry is off by exactly 20 milliseconds and nobody can explain why. The bug surfaces far from where it actually was.

### Three modes, one code path

The same `periodic()` method behaves three different ways, controlled by `Constants.currentMode`:

| Mode | `updateInputs()` does | `processInputs()` does |
|---|---|---|
| **REAL** | Reads from real hardware | Writes struct to log file on roboRIO USB drive |
| **SIM** | Reads from physics sim | Writes to log file on laptop |
| **REPLAY** | Does nothing (no-op stub) | Reads FROM the log file INTO the struct, overwriting whatever was there |

*Don't dwell here. Students see this in action when they run replay in Phase 3.*

> **Why replay is the killer feature**
>
> You saved the log from yesterday's match. The robot crashed at second 42. You're at home with a laptop and no XRP. Set `Constants.currentMode = REPLAY`, hand AdvantageKit the log file, and run your robot code. Your subsystems get the exact same sensor inputs as during the match — byte for byte. Put a breakpoint anywhere. Change the logic and see what would have happened. Do this on a plane. This is impossible without disciplined logging. It's why the order of those two lines matters.

---

## Phase 3 — AdvantageScope Deep Dive (30–75 min)

*Demo every feature on the projector before students touch their laptops. Then watch them replicate.*

### Live mode vs log mode

AdvantageScope has two ways to get data — students conflate them constantly. Cover this explicitly:

| Mode | How | When |
|---|---|---|
| **Live** — Connect to Robot/Sim | File → Connect to Simulator (or to Robot) | Robot or simulator is running right now |
| **Log** — Open Log File | File → Open Log… (point at a .wpilog file) | Reviewing saved data; full timeline immediately available |

### How to find your log files

- **Sim logs:** by default in `logs/` next to your project folder, named with date and time
- **Real-robot logs:** on the USB stick plugged into the roboRIO. Pull the USB after the match, plug into laptop.
- If you don't see a `logs/` folder: Logger isn't writing files — check `Logger.addDataReceiver(new WPILOGWriter())` is in the Robot constructor

### The sidebar — how to find anything

The left sidebar is a tree of every key in the log. Knowing the structure speeds up debugging:

| Folder | Contains |
|---|---|
| `RealOutputs/` | Everything logged via `Logger.recordOutput()` during real run or sim — values your code *decided* |
| `ReplayOutputs/` | Same outputs recomputed during a replay run — compare against `RealOutputs/` to see what changed |
| `AdvantageKit/RealOutputs/` + subsystem folders | Inputs from `@AutoLog` structs — e.g., `Drive/LeftPositionMeters`. Folder name = first arg of `processInputs()` |
| `NT/` and `DS/` | NetworkTables (SmartDashboard, Shuffleboard) and driver station state — useful for cross-checking dashboard vs. reality |

### The visualization tabs

Walk through each tab during the demo:

| Tab | Use it for |
|---|---|
| **Line Graph** | Y = numeric value, X = time. Drag any number-valued key. The 90% case. Multiple keys on one graph for direct comparison. |
| **Odometry / 2D Field** | Drop a `Pose2d` onto a top-down field view. Best way to debug autonomous routines and see where the robot actually went. |
| **Table** | Scrubbable spreadsheet of every value at every timestamp. Slow for long logs but unbeatable for "what was the value at exactly t=42.0?" |
| **Console** | All `System.out.println()` output from the robot. If you printed a debug message, this is where it shows up. |

### Time scrubbing

```
1. Open a log file (or pause a live connection)
2. Click anywhere on the timeline — every visualization jumps to that moment
3. Use arrow keys to step frame-by-frame (one robot loop = 20ms per press)
4. Play button replays at real-time speed; speed slider goes faster or slower
```

This is how you find the exact moment something went wrong.

### Demo sequence — run this on the projector

#### Step 1 — Open a saved log

- File → Open Log… → point at a sim log from Lesson 04
- Confirm the timeline at the bottom shows the full duration

#### Step 2 — Find values in the sidebar

- Expand `AdvantageKit/RealOutputs/Drive/` — show the inputs that got logged
- Expand `RealOutputs/` — show the outputs
- Point out `NT/` and `DS/` briefly

#### Step 3 — Visualization tabs

- Drag `LeftPositionMeters` and `RightPositionMeters` onto a Line Graph — show divergence during turns
- Switch to the Table tab — pick a timestamp, read off all input values
- Open the Console tab — show any debug prints

#### Step 4 — Time scrubbing

- Click in the timeline — show all visualizations jumping to that moment
- Press right arrow — advance one robot loop (20ms)
- Hit play — watch real-time replay

#### Step 5 — Replay mode

This is the moment they came for. Don't rush it.

- Open `Constants.java` on the projector. Change `simMode` from `SIM` to `REPLAY`.
- Set the replay log path constant to point at the log just opened in AdvantageScope
- Run WPILib: Simulate Robot Code
- After it finishes, open the new log file
- Point at the `ReplayOutputs/` folder — same code's outputs, recomputed against the saved inputs
- **Bonus:** change one line of subsystem logic, re-run replay, show the `ReplayOutputs` differ from `RealOutputs`

> **Replay only works if logging was disciplined**
>
> If a sensor reading was never logged, replay can't reproduce it. If `processInputs()` wasn't called, the log is empty. If `@AutoLog` was missing, the struct didn't get serialized. Bad logging during the match means no debugging after — this is why the rules in Phase 2 are not optional.

### Students replicate

Students open their own logs from Lesson 04. Walk the room. Minimum check per student:

- Can they find `Drive/LeftPositionMeters` in the sidebar?
- Can they drag it onto a graph?
- Can they click a point in the timeline and read the value at that moment?

---

## Phase 4 — Practice (75–120 min)

*Students work the tiered challenge. Push them upward — Bronze finishers go straight to Silver. Don't let anyone coast.*

### Tiers

**Bronze — navigate a saved log:** drive XRP for ~30 seconds, open the log, find `Drive/LeftPositionMeters`, drag both position fields onto one graph, find a turning moment in the gyro, open the Console and Table tabs.

**Silver — add a new logged input:** add `totalDistanceMeters` to `DriveIOInputs`, compute it in `updateInputs()`, rebuild, verify it appears in AdvantageScope.

**Gold — run replay mode:** save a sim log, switch `Constants.simMode` to `REPLAY`, set the log path, run simulate, open the new log, compare `RealOutputs/` and `ReplayOutputs/`.

### What to circulate for

- **Bronze stuck:** Drive folder empty in AdvantageScope → logging bug from Lesson 04. Teach the lab on the spot.
- **Silver stuck:** Added field but it doesn't appear → didn't rebuild. *"`@AutoLog` runs at compile time"* is the magic phrase.
- **Gold stuck:** Set REPLAY mode but forgot log path constant → cryptic error. Show them which constant to set.

### The high-leverage question

Before students run anything: *"What do you expect to see in AdvantageScope?"* Force the prediction. Then run. The gap between prediction and reality is where learning happens.

---

## Phase 5 — Broken Robot Lab (120–150 min)

*Three bugs in the same `DriveSubsystem`. Confirm every fix by checking AdvantageScope — reading the code is not enough.*

### Bug 1 — missing `@AutoLog`

`DriveIOInputs` has fields but no `@AutoLog` annotation. The annotation processor doesn't generate `DriveIOInputsAutoLogged`. `Logger.processInputs()` silently does nothing — inputs never reach the log. AdvantageScope Drive folder is empty.

**Acceptable hint:** *"What annotation does the inputs class need? Where have you seen it before today?"*

**Fix:** Add `@AutoLog` above the `DriveIOInputs` class declaration.

### Bug 2 — `processInputs` called BEFORE `updateInputs`

```java
// BUGGY version
Logger.processInputs("Drive", inputs);  // logs stale data from last cycle
io.updateInputs(inputs);               // fills struct — too late
```

First cycle logs zeros. Every subsequent cycle logs the previous cycle's values. Data is always one tick stale. In replay, the logged data doesn't match reality.

**Acceptable hint:** *"What's the rule about order? Which has to come first?"*

**Fix:** Swap the two lines.

### Bug 3 — output key missing the subsystem prefix

`Logger.recordOutput("avgPosition", avg)` puts the value in the root namespace. Without `"Drive/"` prefix, the value floats free in AdvantageScope's sidebar, easy to miss, and collides with any other subsystem that names something `"avgPosition"`. AdvantageScope's sidebar tree is built on slash-separated paths — convention is PascalCase under the subsystem prefix.

**Acceptable hint:** *"Where in the AdvantageScope sidebar would you find a key named `'avgPosition'`?"*

**Fix:** Change the key to `"Drive/AvgPosition"`.

> **Confirm every fix in AdvantageScope, not just by reading the code**
>
> Build, simulate, drive, open the log. The fix isn't done until the value appears in the right folder.

---

## Phase 6 — Physical XRP Drive + Log (150–165 min)

*Students drive their own XRP and capture a real log — distinct from a sim log — to use for replay.*

### What students do

- Connect XRP, enable in Teleop, drive for ~30 seconds
- Locate the log file on the USB stick
- Open it in AdvantageScope
- Find at least one moment that matches something they remember doing ("I turned left here — does the gyro show that?")

### What to watch for

- Students who think sim logs and real-robot logs are different formats (they're not — same WPILOG format)
- Students who can't find the USB log (they didn't have a USB in the roboRIO, or Logger.addDataReceiver wasn't set up)

---

## Phase 7 — Connect + Wrap (165–180 min)

### Exit check — 60 seconds, no grades

Two questions before students pack up:

1. *"Name the two annotations. When do you use each one?"*
2. *"Which line comes first: `updateInputs` or `processInputs`?"*

### Teaser for Lesson 06

> *"Next session we build an autonomous routine that drives a fixed distance and ends. The hardest part isn't writing the code — it's knowing whether it worked. The only way to know is the log. Bring this lesson with you."*

---

## Common Student Questions

**Q: Can I just use SmartDashboard? It seems easier.**
A: *"SmartDashboard publishes live to NetworkTables — useless after the match. AdvantageKit writes a binary log file you can replay. Use both: SmartDashboard for live driver displays, AdvantageKit for everything you might want to debug later."*

**Q: Does logging slow the robot down?**
A: *"Negligibly. Log files are 2–5 MB per match, the writes are buffered, the serialization is fast. You will never measure the performance hit."*

**Q: What happens if I forget `@AutoLog`?**
A: *"Compile might succeed, but `DriveIOInputsAutoLogged` won't exist. If you reference it, you get a compile error. If you use the un-AutoLogged class directly, `processInputs` has nothing to serialize. Either way: empty log."*

**Q: Why are there `RealOutputs` AND `ReplayOutputs`?**
A: *"When you run a replay, the original `RealOutputs` from the live run are preserved in the new log, alongside the freshly-computed `ReplayOutputs`. Compare them: same code = identical. Different code = the differences are exactly what your change caused."*

**Q: My log file is huge / tiny — is something wrong?**
A: *"Sim logs of 10–30 seconds are usually small (~100 KB). A real match log is a few MB. If yours is 0 bytes, the WPILOGWriter probably isn't connected — check `Robot.java`'s Logger setup. If it's hundreds of MB, you might be logging an array on every cycle — investigate."*

**Q: Where are my sim log files?**
A: *"By default in a `logs/` folder next to your project folder, named with the date and time. If the folder doesn't exist, `Logger.addDataReceiver(new WPILOGWriter())` isn't in your Robot constructor."*

---

*Instructor Edition — Not for student distribution*
