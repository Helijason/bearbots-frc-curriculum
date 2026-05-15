# Module 2 — Lesson 07: Why Doesn't It Stop Where I Told It To?

**Stack:** Java | AdvantageKit | XRP
**Card #:** 07 — *Keep this. Add it to your binder.*

---

## The Big Idea

> Open loop sets the power. Closed loop sets the goal.
> Measure where you are. Compare to where you want to be. Push proportionally. Repeat 50 times a second.

---

## Key Concepts

| Concept | Role | What it does |
|---|---|---|
| **Encoder** | Distance | Counts wheel rotations. Reports inches → m. Use for distance/speed. |
| **Gyro** | Heading | Reports angle in degrees. Resets on robot start. Use for turns/drift. |
| **Error** | `target − current` | The gap to close. Sign tells direction. Magnitude tells urgency. |
| **kP** | Tuning knob | `output = error × kP`. Too small: too slow. Too big: oscillates. |
| **PIDController** | WPILib helper | Wraps the error math. Adds tolerance + reset. `.atSetpoint()` = done. |

---

## The P-Control Loop

1. Read sensor: `current = drive.getPos()`
2. Compute error: `error = target − current`
3. Compute output: `volts = error × kP`
4. Apply: `drive.setVoltage(volts)`
5. `isFinished`: `|error| < tolerance`

> This loop runs every cycle of `execute()`.
> Same shape for distance, heading, RPM, anything.

---

## Tuning kP — What You See

**kP too small:** Robot creeps. Stops short. Never reaches target. → Double kP.

**kP just right:** Smooth approach. Slows near target. Settles. → Stop tuning. Ship it.

**kP too big:** Slams past. Overshoots. Oscillates. Never settles. → Halve kP.

---

## After This Lesson I Can…

- [ ] Explain open loop vs closed loop in one sentence
- [ ] Read encoder and gyro values from the IO layer
- [ ] Convert a fixed-power command to proportional control
- [ ] Tune kP by watching response curves in AdvantageScope
- [ ] Read real team code and spot the IO/logging/PID patterns

---

## Key Vocabulary

- **Open loop** — Set motor power directly. No feedback. *"Drive at 0.5 until 1m."*
- **Closed loop** — Read sensors, compare to target, adjust output every cycle. Self-correcting.
- **Proportional** — `output = error × kP`. Push harder when farther from target. The 'P' in PID.
- **Tolerance** — How close to the target counts as 'done'. e.g. 2 cm for distance, 2° for heading.
- **PIDController** — WPILib class doing the error math, with tolerance and `atSetpoint()` built in.

---

## Questions I Still Have

*Write your questions here. Bring them when you read team code.*

## My Notes

*Write anything here — surprises, connections, things to look up later.*

---

*FRC Programming Curriculum — Lesson 07*
*End of curriculum. Now go read your team's code.*
*Keep this. Collect all 7.*
