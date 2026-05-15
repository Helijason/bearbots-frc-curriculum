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
| **`isFinished()`** | Am I done? | Return `true` to end. Always `false` = forever. Check encoder/timer. |
| **`end()`** | Cleanup | Runs once at stop. **STOP THE MOTORS HERE.** Even if interrupted. |
| **Sequential** | Composition | Commands one by one. Wait for child finish. `.andThen()` does same. |

---

## The Command Lifecycle

1. **Schedule** → `initialize()` runs once
2. Every 20ms: `execute()` → `isFinished()`
3. `isFinished()` returns `true` → `end(false)`
4. Or another command takes over → `end(true)`
5. Scheduler removes the command. Done.

> The CommandScheduler runs this loop for every scheduled command, every cycle.

---

## The Two Rules You Can't Break

**Rule 1 — Every command must end.**
`isFinished() = false` forever = routine stalls.

**Rule 2 — `end()` must put the subsystem in a safe state.**
`drive.stop()` in `end()`. Always.
Break it: motors keep last setpoint forever.

---

## After This Lesson I Can…

- [ ] Name the four methods of a command
- [ ] Write a new command (`TurnToAngle`) from scratch
- [ ] Compose commands with `SequentialCommandGroup`
- [ ] Wire an `AutoChooser` into SmartDashboard
- [ ] Spot 'doesn't end' and 'doesn't stop' bugs on sight

---

## Key Vocabulary

- **Command** — WPILib base class with four lifecycle methods — extend it to make any robot action
- **CommandScheduler** — WPILib singleton that calls `initialize/execute/isFinished/end` on every scheduled command
- **SequentialCommandGroup** — Runs child commands one after another — the workhorse of every autonomous routine
- **`addRequirements()`** — Declares which subsystems a command exclusively owns — prevents two commands fighting
- **AutoChooser** — SmartDashboard widget that lets the driver pick which auto routine to run before the match

---

## Questions I Still Have

*Write your questions here. Bring them to the next session.*

## My Notes

*Write anything here — surprises, connections, things to look up later.*

---

*FRC Programming Curriculum — Lesson 06*
*Next: Lesson 07 — Sensors and feedback*
*Keep this. Collect all 7.*
