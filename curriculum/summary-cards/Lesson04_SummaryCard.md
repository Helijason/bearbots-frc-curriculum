# Module 2 — Lesson 04: Why Two Files for One Motor?

**Stack:** Java | AdvantageKit | XRP
**Card #:** 04 — *Keep this. Add it to your binder.*

---

## The Big Idea

> Your subsystem should never know what hardware it's running on.
> If it does, changing one motor means changing every file that touched that motor. At 11pm. Before competition.

---

## Three Files. Three Jobs. They Never Swap.

### `DriveIO.java` — The contract
Defines what a drivetrain can do.
**Zero hardware imports. Ever.**
Think: job description.

### `DriveIOXRP.java` — The implementation
Talks to XRP hardware.
The only file allowed to know what hardware this is.

### `DriveSubsystem.java` — The subsystem
Calls interface methods.
Has no idea what's on the other end. Doesn't care.

---

## The Two Rules You Cannot Break

**Rule 1 — `DriveSubsystem` must NEVER `import XRPDrivetrain`.**
Break it: changing hardware breaks every file.

**Rule 2 — `stop()` sets motors to `0.0`. Not `1.0`. Not ever.**
Break it: `stop()` launches game pieces. Awkward.

---

## The AdvantageKit Logging Loop

1. `io.updateInputs(inputs)` — Read hardware into struct
2. `Logger.processInputs(...)` — AdvantageKit logs inputs
3. Use `inputs.someValue` — Now use the data
4. Open AdvantageScope — See everything logged

> This loop runs every 20ms. Every loop cycle.
> If `processInputs()` isn't in `periodic()`, nothing logs.

---

## After This Lesson I Can…

- [ ] Explain why the IO pattern uses three files
- [ ] Name each file and describe its job in one sentence
- [ ] Implement `DriveIOXRP` from a given interface
- [ ] Find and fix a units bug in an IO implementation
- [ ] Describe what `Logger.processInputs()` does and when

---

## Key Vocabulary

- **Interface** — A Java contract that defines method signatures without implementing them
- **Implementation** — A class that fulfills an interface contract with real code
- **IO layer** — The AdvantageKit abstraction separating hardware from subsystem logic
- **Logged inputs** — Sensor readings captured by AdvantageKit every loop cycle for replay
- **Replay mode** — Running robot logic against a saved log file without needing hardware

---

## Questions I Still Have

*Write your questions here. Bring them to the next session.*

## My Notes

*Write anything here — things that surprised you, connections you made, stuff to look up later.*

---

*FRC Programming Curriculum — Lesson 04*
*Next: Lesson 05 — Logging and AdvantageScope*
*Keep this. Collect all 7.*
