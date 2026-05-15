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
| **Session length** | 45 minutes |
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
- AdvantageScope installed; a saved log from a prior session ready to demo (best: a log with visible bugs/anomalies)
- Digital handout open: `lesson-04-logging.html`
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
| **5–15 min** | **Concept** | Walk through `@AutoLog` code-gen, the input/output split, the ordering rule, three modes diagram. | Follow along on digital handout. Ask questions. |
| **15–30 min** | **AdvantageScope** | Live demo: open log, drag fields, scrub timeline, switch tabs, set up replay mode. | Replicate on their own laptops with their own logs from Lesson 04. |
| **30–40 min** | **Practice** | Circulate during tiered challenge. Push students who finish Bronze toward Silver immediately. | Work through challenge tiers. Add a new logged field. Try replay. |
| **40–45 min** | **Lab + connect** | Walk through broken robot lab on projector if time. Tease Lesson 06 (autonomous needs logging). | Find the 3 bugs in the lab. Recognize them on sight. |

> **20-minute compressed version**
> Skip the AdvantageScope visualization tour. Cover only `@AutoLog`, the order rule, and the lab. Assign the digital handout's tiered challenge as homework. Students will lose some AdvantageScope skill but retain the underlying discipline.

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

## Phase 2 — Concept (5–15 min)

*Three things to teach: what `@AutoLog` generates, the input/output split, and the ordering rule.*

### `@AutoLog` — the annotation processor

Open `DriveIOInputs.java` on the projector. Show students the `@AutoLog` annotation.

- Explain that `@AutoLog` is processed at compile time, not runtime
- The annotation processor generates a sibling class (`DriveIOInputsAutoLogged`) with the `toLog`/`fromLog` methods
- If you have time: show the generated file in `build/generated/` — students don't need to read it, just see that it exists
- **Driving point:** if `@AutoLog` is missing, no `AutoLogged` class exists, no `toLog`/`fromLog`, no logging. Silent failure.

### Inputs vs outputs — two annotations, two purposes

> **The split, plain English**
>
> **Inputs** = things you read (sensors, button states). Wrap them in a struct, slap `@AutoLog` on the struct.
>
> **Outputs** = things you decide (target velocities, computed poses, mode names). Use `@AutoLogOutput` on a field, or call `Logger.recordOutput()` directly.
>
> *Test: "Did the world tell me this, or did my code decide this?" That's the question that picks the annotation.*

### The ordering rule

This is the most important sentence of the lesson:

> **Say it out loud, twice**
>
> ***"`updateInputs` first. `processInputs` second. Always."***
>
> If you swap them, you log stale data. Replay reproduces a fiction. Auto routines drift in ways nobody can explain. The bug surfaces three weeks later, far from where it actually was.

### Three modes, one code path

Briefly: **REAL** = real hardware + write log. **SIM** = simulated hardware + write log. **REPLAY** = stub hardware + read FROM log. The same `periodic()` works in all three because the IO layer abstracts the source.

*Don't dwell here. Students see this in action when they run replay in Phase 4.*

---

## Phase 3 — AdvantageScope Live Demo (15–30 min)

*Demo every feature on the projector before students touch their laptops. Then watch them replicate.*

### Demo sequence

Run this top to bottom on the projector. Don't skip steps. ~5 minutes total.

#### Step 1 — Open a saved log

- File → Open Log… → point at a sim log from Lesson 04
- Confirm the timeline at the bottom shows the full duration

#### Step 2 — Find values in the sidebar

- Expand `AdvantageKit/RealOutputs/Drive/` — show the inputs that got logged
- Expand `RealOutputs/` — show the outputs
- Mention `NT/` and `DS/` briefly so students know they exist

#### Step 3 — Visualization tabs

- Drag `LeftPositionMeters` and `RightPositionMeters` onto a Line Graph — show divergence during turns
- Switch to the Table tab — pick a timestamp, read off all input values
- Open the Console tab — show any debug prints (run a `System.out.println` in the demo if you want a guaranteed entry)

#### Step 4 — Time scrubbing

- Click in the timeline — show all visualizations jumping to that moment
- Press right arrow — advance one robot loop (20ms)
- Hit play — watch real-time replay

#### Step 5 — Replay mode

This is the moment they came for. Don't rush it.

- Open `Constants.java` on the projector. Change `simMode` from `SIM` to `REPLAY`.
- Set the replay log path constant to point at the log you just opened in AdvantageScope
- Run WPILib: Simulate Robot Code
- After it finishes, open the new log file
- Point at the `ReplayOutputs/` folder — explain it's the same code's outputs, recomputed against the saved inputs
- **Bonus:** change one line of subsystem logic, re-run replay, show the `ReplayOutputs` differ from `RealOutputs`

---

## Phase 4 — Practice (30–40 min)

*Students work the tiered challenge. Push them upward — Bronze finishers go straight to Silver. Don't let anyone coast.*

### What to circulate for

- **Bronze:** students stuck because the Drive folder is empty in AdvantageScope — likely a logging bug from Lesson 04 (this is your moment to teach the lab)
- **Silver:** students who added the new field but didn't rebuild — *"`@AutoLog` runs at compile time"* is the magic phrase
- **Gold:** students who set REPLAY mode but forgot the log path constant — they'll get a cryptic error; show them which constant to set

### The high-leverage question

Before students run anything, ask: *"What do you expect to see in AdvantageScope?"* Force the prediction. Then they run it. The gap between prediction and reality is where learning happens — not in passively watching graphs update.

---

## Phase 5 — Lab + Connect (40–45 min)

*If time permits, walk the broken robot lab on the projector. If not, assign as homework — the answers below are the teaching points either way.*

### Broken robot lab — answers

Three bugs in the same `DriveSubsystem`. Each teaches a different lesson:

#### Bug 1 — missing `@AutoLog`

The `DriveIOInputs` class has fields but no `@AutoLog` annotation. Without it, the annotation processor doesn't generate `DriveIOInputsAutoLogged`. `Logger.processInputs()` silently does nothing useful — your inputs never reach the log. AdvantageScope's Drive folder appears empty.
**Fix:** add `@AutoLog` above the class declaration.

#### Bug 2 — `processInputs` called BEFORE `updateInputs`

On line 17, `processInputs` runs first. The struct still holds whatever it had at the end of the last cycle (or zeros, on the first cycle). The log captures stale data. Real values come in on line 18 — too late, this cycle's log entry is already written. Every value in the log is delayed by one tick.
**Fix:** swap lines 17 and 18.

#### Bug 3 — output key missing the subsystem prefix

`Logger.recordOutput("avgPosition", ...)` puts the value in the root namespace of the log. AdvantageScope's sidebar tree is built on slash-separated paths — without `"Drive/"` prefix, the value floats free, easy to miss, and collides with anything else named `"avgPosition"`.
**Fix:** change the key to `"Drive/AvgPosition"`. Use this teaching moment to standardize on PascalCase under the subsystem prefix for all outputs.

### Connect — what's next

Lesson 06 is autonomous routines. Tease it directly:

> **Teaser for Lesson 06**
>
> *"Next time, we build an autonomous that drives a fixed distance and ends. The hardest part isn't writing the code — it's knowing whether your code worked. The only way to know is the log. Bring this lesson with you."*

---

## Common Student Questions

**Q: Can I just use SmartDashboard? It seems easier.**
A: *"SmartDashboard publishes live to NetworkTables — useless after the match. AdvantageKit writes a binary log file you can replay. Use both: SmartDashboard for live driver displays, AdvantageKit for everything you might want to debug later."*

**Q: Does logging slow the robot down?**
A: *"Negligibly. Log files are 2–5 MB per match, the writes are buffered, the serialization is fast. You will never measure the performance hit."*

**Q: What happens if I forget `@AutoLog`?**
A: *"Compile might succeed, but `DriveIOInputsAutoLogged` won't exist — so anywhere you reference it will fail. If you use the un-AutoLogged class directly, `processInputs` has nothing to serialize. Either way: empty log."*

**Q: Why are there `RealOutputs` AND `ReplayOutputs`?**
A: *"When you run a replay, the original `RealOutputs` from the live run are preserved in the new log, alongside the freshly-computed `ReplayOutputs`. Compare them: same code = identical. Different code = the differences are exactly what your change caused."*

**Q: My log file is huge / tiny — is something wrong?**
A: *"Sim logs of 10–30 seconds are usually small (~100 KB). A real match log is a few MB. If yours is 0 bytes, the WPILOGWriter probably isn't connected — check `Robot.java`'s Logger setup. If it's hundreds of MB, you might be logging an array on every cycle — investigate."*

---

*Instructor Edition — Not for student distribution*