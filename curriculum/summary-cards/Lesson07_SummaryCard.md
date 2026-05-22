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
| **Encoder** | Distance | Counts wheel rotations. Reports inches → convert to meters (`× 0.0254`). |
| **Gyro** | Heading | Reports angle in degrees. Resets on robot start. Use for turns/drift. |
| **Reflectance** | Line detect | Two analog sensors, 0.0–1.0. High on dark. Used for line following. |
| **Error** | `target − current` | The gap to close. Sign tells direction. Magnitude tells urgency. |
| **kP** | Tuning knob | `output = error × kP`. Too small: too slow. Too big: oscillates. |
| **PIDController** | WPILib helper | Wraps the error math. Adds tolerance + reset. `.atSetpoint()` = done. |

---

## Reading Sensors — Through the IO Layer

```java
// DriveIOInputs — add these fields:
public double leftVelocityMetersPerSec  = 0.0;
public double rightVelocityMetersPerSec = 0.0;
public double headingDegrees            = 0.0;

// DriveIOXRP.updateInputs() — fill them:
inputs.leftPositionMeters        = drivetrain.getLeftDistanceInch()  * 0.0254;
inputs.leftVelocityMetersPerSec  = drivetrain.getLeftEncoderRate()   * 0.0254;
inputs.headingDegrees            = gyro.getAngle();
```

> Log both position AND velocity. Position = how far. Velocity = how fast.
> Jumpy velocity but clean position = sensor noise. Clean velocity but wrong position = units bug.

---

## The P-Control Loop

```java
double error  = target - current;   // how far off?
double output = error * kP;         // push proportionally
drive.setVoltage(output);           // apply it
```

In `isFinished()`: `return Math.abs(error) < tolerance;` (e.g. `tolerance = 0.02` for 2 cm)

> Same shape for distance, heading, RPM — anything.
> Start with kP = 1.0. Tune from there.

---

## Using WPILib's `PIDController`

```java
private final PIDController pid = new PIDController(4.0, 0.0, 0.0); // kP, kI, kD

// In execute():
double output = pid.calculate(currentValue, targetValue);
drive.setVoltage(output, output);

// In isFinished():
return pid.atSetpoint();  // uses configured tolerance
```

Call `pid.setTolerance(2.0)` in constructor. For both position and velocity tolerance: `pid.setTolerance(2.0, 5.0)`.

---

## Tuning kP — What You See

**kP too small:** Creeps. Stops short. Never reaches target. → Double kP.

**kP just right:** Smooth approach. Slows near target. Settles cleanly. → Stop tuning.

**kP too big:** Slams past. Overshoots. Oscillates. Never settles. → Halve kP.

> Tuning loop: start at 1.0 → run → watch AdvantageScope → double or halve → repeat.

---

## After This Lesson I Can…

- [ ] Explain open loop vs closed loop in one sentence
- [ ] Add encoder and gyro fields to `DriveIOInputs` with correct unit conversions
- [ ] Write the three-line P-control math from memory
- [ ] Convert a fixed-power command to proportional control
- [ ] Use `PIDController` with `atSetpoint()` as `isFinished()`
- [ ] Tune kP by watching response curves in AdvantageScope
- [ ] Read real team code and spot the IO/logging/PID patterns

---

## Key Vocabulary

- **Open loop** — Set motor power directly. No feedback. *"Drive at 0.5 until 1m."*
- **Closed loop** — Read sensors, compare to target, adjust output every cycle. Self-correcting.
- **Proportional** — `output = error × kP`. Push harder when farther from target. The 'P' in PID.
- **Tolerance** — How close to the target counts as 'done'. e.g. 2 cm for distance, 2° for heading.
- **PIDController** — WPILib class doing the error math, with tolerance and `atSetpoint()` built in.
- **I (Integral)** — Accumulates error over time; fixes steady-state error P can't tune away.
- **D (Derivative)** — Damps oscillation; subtracts a term based on the rate of change of error.

---

## Questions I Still Have

*Write your questions here. Bring them when you read team code.*

## My Notes

*Write anything here — surprises, connections, things to look up later.*

---

*FRC Programming Curriculum — Lesson 07*
*End of curriculum. Now go read your team's code.*
*Keep this. Collect all 7.*
