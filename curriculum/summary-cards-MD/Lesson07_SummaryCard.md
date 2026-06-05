# Module 2 — Lesson 07: Make It Reliable

**Stack:** Java | AdvantageKit | XRP
**Card #:** 07 — *Keep this. Add it to your binder.*

---

## The Big Idea

> Open loop sets the power and hopes for the best.
> Closed loop measures where you are and adjusts every 20ms.
> One of these works at competition. The other works when you're lucky.

---

## The P-Control Loop — Three Lines

```java
double error  = targetMeters - traveled;  // how far off?
double output = error * kP;               // push proportional to error
drive.setVoltage(output, output);         // apply it
```

> When far from target: big error → big push.
> When near target: small error → gentle coast.
> At target: zero error → zero output → stops.

---

## `isFinished()` — Tolerance, Not Exact

```java
return Math.abs(targetMeters - traveled) < tolerance;
```

> `tolerance = 0.02` means "within 2cm counts as done."
> Don't try for exactly zero — the robot will oscillate forever.
> Reliable beats perfect.

---

## Tuning kP — What the Curve Tells You

| What you see in AdvantageScope | What it means | What to do |
|---|---|---|
| Creeps slowly, stops short | kP too small | Double it |
| Smooth approach, settles cleanly | kP just right | Stop tuning |
| Slams past, oscillates | kP too big | Halve it |

> **The tuning loop:** start at 1.0 → run → watch the curve → double or halve → repeat.
> Always tune in sim first. Then verify on hardware.

---

## Constants to Tune Today

All of these live in `Constants.java` — nowhere else:

| Constant | What it controls |
|---|---|
| `PARK_DISTANCE_METERS` | How far the robot drives to reach the parking zone |
| `kP` | How aggressively it corrects error |
| `tolerance` | How close is "close enough" |
| `AUTO_TIMEOUT_SECONDS` | Safety cutoff if something goes wrong |

---

## The Sim-First Rule

1. Change a constant in `Constants.java`
2. Run in simulator — watch AdvantageScope
3. Position curve looks good? → deploy to XRP
4. Run on field — pull log, compare curve to sim
5. Still needs adjustment? → back to step 1

> **Never skip sim.** If it doesn't work in sim, it won't work on the field.

---

## Strategy Lock

Before you leave today:

- [ ] Auto runs cleanly in sim 3 times in a row
- [ ] Auto parks reliably on the real field 3 times in a row
- [ ] AutoChooser default is set to your chosen strategy
- [ ] Constants committed to git with a meaningful message
- [ ] Comment in `RobotContainer.java`: `// Competition strategy: [Park / Score + Park] — tuned [date]`

---

## After This Lesson I Can…

- [ ] Explain why open-loop auto fails across different conditions
- [ ] Write the three lines of P-control math from memory
- [ ] Tune kP by reading AdvantageScope response curves
- [ ] Change my auto's behavior by editing `Constants.java` only
- [ ] Commit code with a message that describes what I changed and why

---

## Key Vocabulary

- **Open loop** — set motor power directly with no feedback. Reliable when conditions never change.
- **Closed loop** — measure current state, compare to target, adjust output every cycle. Self-correcting.
- **Error** — `target − current`. The gap to close. Sign tells direction.
- **kP** — proportional gain. Scales how hard the robot pushes per unit of error.
- **Tolerance** — how close counts as done. Too tight = oscillation. Too loose = imprecise.

---

## Questions I Still Have

*Write your questions here. Bring them to competition day.*

## My Notes

*kP that worked in sim: _____ kP that worked on hardware: _____*
*Park distance: _____ meters. Strategy choice: _____*

---

## Competition Connection

> **Today is what makes your auto reliable.** The difference between a robot that parks 60% of the time and one that parks 95% of the time is closed-loop control and a tuned kP.
>
> Tomorrow you compete. Your autonomous runs for 30 seconds with no human input. The code you commit today is what runs. Make it count.

---

*FRC Programming Curriculum — Lesson 07*
*Next: Lesson 08 — Competition Day.*
*Keep this. Collect all 8.*
