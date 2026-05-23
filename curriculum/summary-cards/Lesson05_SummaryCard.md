# Module 2 — Lesson 05: How Do I Debug a Robot That Isn't Here?

**Stack:** Java | AdvantageKit | XRP
**Card #:** 05 — *Keep this. Add it to your binder.*

---

## The Big Idea

> If it's not logged, it didn't happen.
> Your only witness to the bug at competition is the log file. Make it a good one.

---

## Key Concepts

| Concept | Role | What it does |
|---|---|---|
| **`@AutoLog`** | Annotation | Goes on inputs class. Generates `AutoLogged`. No annotation = no logs. |
| **`updateInputs()`** | You write | Reads real hardware. Fills the inputs struct. Runs first in `periodic()`. |
| **`processInputs()`** | AdvantageKit | Logs struct to disk. REPLAY: reads from log. Runs second. Always. |
| **`@AutoLogOutput`** | Other side | Goes on a field. Logs computed values. Use `Logger.recordOutput` too. |
| **Replay mode** | The payoff | Runs code on saved log. No hardware needed. Compare Real vs Replay. |

---

## The Logging Loop

1. Hardware values change every loop
2. `io.updateInputs(inputs)` → fill struct
3. `Logger.processInputs("Drive", inputs)`
4. Subsystem uses `inputs.leftPositionMeters`
5. Open log in AdvantageScope → debug

> Same loop in REAL, SIM, and REPLAY.
> Only what's behind the IO changes.

---

## The Two Rules You Can't Break

**Rule 1 — `updateInputs()` BEFORE `processInputs()`. Always.**
Swap them and your data is one tick stale. Replay reproduces wrong reality.

**Rule 2 — Every `recordOutput` key starts with subsystem name.**
`"Drive/AvgPos"` not `"avgPos"`. No prefix = lost in the sidebar.

---

## AdvantageScope Sidebar Structure

| Folder | Contains |
|---|---|
| `RealOutputs/` | Values your code decided — `Logger.recordOutput()` calls |
| `ReplayOutputs/` | Same outputs, recomputed during replay — compare to find what changed |
| `AdvantageKit/RealOutputs/` + subsystem folders | Inputs from `@AutoLog` structs — folder name = first arg of `processInputs()` |
| `NT/` and `DS/` | NetworkTables and driver station state |

---

## Visualization Tabs

| Tab | Use it for |
|---|---|
| **Line Graph** | Numbers over time. Drag any field. The 90% case. |
| **Odometry / 2D Field** | Drop a `Pose2d` — see where the robot went. Best for autonomous debugging. |
| **Table** | Every value at every timestamp. Find "what was X at t=42.0?" |
| **Console** | All `System.out.println()` from the robot. |

---

## Finding Your Log Files

- **Sim logs:** `logs/` folder next to your project, named by date/time
- **Real robot logs:** USB stick in the roboRIO. Pull it after the match.
- **Nothing in `logs/`?** Check `Logger.addDataReceiver(new WPILOGWriter())` is in Robot constructor.

---

## After This Lesson I Can…

- [ ] Explain what `@AutoLog` generates at compile time
- [ ] Add a new field to an Inputs class and see it logged
- [ ] Open a saved log and scrub through it in AdvantageScope
- [ ] Find values in `RealOutputs/` and `AdvantageKit/` sidebar folders
- [ ] Switch a project into REPLAY mode and re-run a log
- [ ] Explain why `updateInputs` must come before `processInputs`

---

## Key Vocabulary

- **`@AutoLog`** — AdvantageKit annotation — goes on an inputs class to auto-generate `toLog`/`fromLog` serialization code
- **`@AutoLogOutput`** — AdvantageKit annotation — goes on a field to auto-log its value every cycle
- **Inputs struct** — A bag of public fields read from hardware each cycle — wraps everything you log via the IO
- **Replay mode** — Running robot code against a saved log instead of hardware — same inputs, same code, no robot
- **WPILOG** — The binary log format AdvantageKit writes — opened by AdvantageScope, replayable, sharable
- **`RealOutputs/`** — AdvantageScope sidebar folder containing values logged during a live or sim run
- **`ReplayOutputs/`** — AdvantageScope sidebar folder containing values recomputed during a replay run

---

## Questions I Still Have

*Write your questions here. Bring them to the next session.*

## My Notes

*Write anything here — surprises, connections, things to look up later.*

---

---

## Competition Connection

> **Logging is what turns "something went wrong" into "here's exactly what happened."** Your competition autonomous runs for 30 seconds with no human input. If it fails, the log is your only witness.
>
> After every practice run in Lessons 06 and 07, you'll pull the log and open it in AdvantageScope. The position curve tells you whether to increase kP or adjust your distance constant. Without this lesson, you'd be guessing.

---

*FRC Programming Curriculum — Lesson 05*
*Next: Lesson 06 — How does the robot know when it's done?*
*Keep this. Collect all 8.*
