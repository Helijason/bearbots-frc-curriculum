# FRC Programming Curriculum — Module 2, Lesson 07

# Why Doesn't It Stop Where I Told It To?

*Sensors, P-control, tuning kP, and a closing code review on real team code.*

> **Instructor Edition — Not for student distribution**

---

## At a Glance

| Field | Detail |
|---|---|
| **Target audience** | Students who completed Lesson 06 and have run a working autonomous routine |
| **Hardware** | XRP robot — same setup as Lessons 04–06 |
| **Session length** | 45 minutes (the closer) |
| **Key tools** | Encoder/gyro reads via the IO layer, WPILib `PIDController`, AdvantageScope for tuning |

---

## Learning Objectives

- Students can explain open loop vs closed loop and predict why open loop fails on real hardware
- Students can name the three XRP sensors (encoder, gyro, reflectance), say what each measures, and read their values through the IO layer
- Students can write the three lines of P-control math without looking at the handout
- Students can tune kP empirically: identify the symptoms of too-small / just-right / too-large
- Students can convert a fixed-power command from Lesson 06 into a closed-loop command and verify it works in AdvantageScope
- Students can read a real team's subsystem and articulate three things a code reviewer would ask them to fix

---

## Before You Start

### Room setup

- VSCode open on projector with the Lesson 06 starter project, plus the open-loop `DriveDistance` you've been using
- AdvantageScope open and ready, with a saved sim log from Lesson 06 to show 'overshoot' visually
- Digital handout open: `lesson-07-sensors.html`
- XRPs available — students will tune kP on hardware
- Same floor space as Lesson 06 (1–2 meter runs)

### Have ready

- A version of `DriveDistance` with kP set deliberately wrong (kP = 0.5 too small, kP = 50.0 too big) to demo each tuning failure mode
- The code-review subsystem from the handout's Part 4 — pulled out as a standalone file, ready to project
- If possible, an actual snippet of your team's competition code from a recent year — for the *'now read your team's code'* moment at the end

> **The most important instructor mindset for this lesson**
>
> This is the closer. Students who reach Lesson 07 have built up a lot of trust in the framework — subsystems, IO, logging, commands. This lesson rewards that trust by showing that everything they've learned was a setup for this moment: now you can write the same kind of feedback control that ships at competition.
>
> Resist teaching all of PID. Cover P only. Ship students out the door with a working closed-loop command and the correct intuition, not a half-understood textbook chapter on integral and derivative terms. They'll meet I and D when they need them, and by then they'll have the framework to absorb them quickly.
>
> This is also the lesson where students should feel the curriculum land. After the code review, take 30 seconds to tell them what they just accomplished — seven lessons, foundational FRC programming, a working mental model. They earned it.

---

## Session Timing

| Time | Phase | You do | Students do |
|---|---|---|---|
| **0–5 min** | **Hook** | Demo Lesson 06's auto twice — fresh battery, then partly drained. Show the difference in distance. | Watch. Realize 'set and pray' isn't reliable. |
| **5–15 min** | **Concept** | Open loop vs closed loop. Three sensors. Reading them through the IO layer. | Follow on digital handout. Add the new fields to `DriveIOInputs`. |
| **15–25 min** | **Closing the loop** | Live-code: convert `DriveDistance` to P-control. Show kP tuning live in AdvantageScope. Show overshoot/oscillation/just-right. | Replicate on their own laptops. |
| **25–40 min** | **Practice** | Circulate during tiered challenge. Bronze pushes everyone; Silver and Gold for confident students. | Bronze: P-control `DriveDistance`. Silver: gyro drift correction. Gold: P-control `TurnToAngle`. |
| **40–45 min** | **Code review** | Walk through the code review on the projector. Tie back to all six lessons. Send them off. | Spot the 3 review notes in the lab. Recognize each from a previous lesson. |

> **20-minute compressed version**
> Skip the live tuning demo and the gyro-drift Silver tier. Cover only the P-control concept, do Bronze tier as a class, and do the code review. Students will know what closed loop is and have one example, but won't have hands-on tuning practice — assign that as homework.

---

## Phase 1 — Hook (0–5 min)

*Make the failure of open loop visceral. Run the same auto twice and show the difference.*

### Opening

Power on an XRP with a fresh battery. Run last lesson's `DriveDistance(1.0)`. Mark on the floor where it stops with tape. Reset. Do it again. Should land in the same spot.

Now drain the battery a little — or simulate the same effect by adding extra weight, or having a student push back lightly on the robot during the run. Run the same auto. It will stop in a noticeably different place.

> **Script — what to say**
>
> *"Same code. Same target. Different reality. The code said 'drive at 0.5 power until 1 meter.' What it actually did was 'apply 50% throttle, hope for the best.' At a competition, your battery is never fresh; the field never has the same friction; gravity never quite cooperates. If you want the robot to stop where you said it would, you have to measure where you are and adjust. That's today."*

---

## Phase 2 — Concept (5–15 min)

*Three things to teach: open vs closed, the three XRP sensors, reading them through the IO layer.*

### Open loop vs closed loop

Frame it as a question of what you're commanding:

- **Open loop:** you command the actuator. *"Set motor to 0.5."* Whatever happens, happens.
- **Closed loop:** you command the goal. *"Reach 1 meter."* The code figures out the actuator value, recomputed every cycle.

*Use the words 'set and pray' for open loop. Students remember it.*

### The three sensors

Don't just list them — connect each to a use case students already understand:

- **Encoder:** *'How far has each wheel turned?'* — what makes `DriveDistance` work
- **Gyro:** *'Which way are we pointing?'* — what makes `TurnToAngle` work
- **Reflectance:** *'Is there a line under us?'* — used for line following, won't be needed today

*Mention units explicitly: encoders give inches, gyro gives degrees. Conversions live in the reference card.*

### Through the IO layer, always

This is review of Lesson 04, but it bears repeating. Show `DriveIOInputs.java` on the projector. Add the new fields:

```java
public double leftVelocityMetersPerSec = 0.0;
public double rightVelocityMetersPerSec = 0.0;
public double headingDegrees = 0.0;
```

Then `DriveIOXRP.updateInputs()`: fill them from `drivetrain.getLeftEncoderRate()` etc., with the unit conversion. Drill the `*0.0254` conversion.

> **The line that has to land**
>
> ***"Encoders give inches. Code wants meters. Multiply by `0.0254`. If you don't, your '1 meter' auto will travel 39 meters into the wall."***
>
> *This is the unit bug from the reference card. Half the class will hit it on Bronze. Drill it now and they spot it themselves later.*

---

## Phase 3 — Closing the Loop (15–25 min)

*Live-code the conversion of `DriveDistance` from open loop to P-control. Show kP tuning visually in AdvantageScope.*

### Convert `DriveDistance` to P-control

On the projector, side-by-side with the Lesson 06 version, replace `execute()`:

- **Old:** `drive.drive(0.5, 0.0);`
- **New:**
```java
double error = targetMeters - traveled;
double volts = error * kP;
drive.setVoltage(volts, volts);
```

Update `isFinished()` from 'have we passed?' to 'are we within tolerance?': `return Math.abs(error) < tolerance;`

**Make the point:** same four-method structure. Just smarter `execute()` and `isFinished()`. The framework didn't change.

### Live tuning demo

This is the moment AdvantageScope earns its place in the curriculum. Run the auto with three different kP values. Open AdvantageScope. Graph `LeftPositionMeters` alongside the target.

- **kP = 0.5 (too small):** graph shows current position lazily approaching target, never reaches it
- **kP = 4.0 (good):** graph shows smooth approach, slows near target, settles cleanly
- **kP = 50.0 (too big):** graph shows current overshooting target, oscillating around it

This is what tuning looks like in practice. Show students the visual signature of each failure mode — they'll recognize it during the challenge.

### WPILib's `PIDController` — quick mention

Show that WPILib provides `PIDController` with the same math built in. Demo `.calculate()` and `.atSetpoint()`. Tell students: use the WPILib version in real code; we wrote the bare math today so you understand what's inside the helper.

### I and D in 60 seconds

Acknowledge that PID has three letters. Briefly:

- **I (Integral):** for steady-state error you can't tune away with P alone
- **D (Derivative):** damps oscillation when P alone is too aggressive

*Move on. Most teams use P-only most of the time. If a student asks deeper questions after class, recommend the WPILib PID documentation. Don't burn class time on it.*

---

## Phase 4 — Practice (25–40 min)

*Tiered challenge. Bronze should land for everyone. Silver and Gold for students who finish early.*

### What to circulate for

- **Bronze:** students whose robot doesn't move — kP probably too small, `error * kP` isn't producing enough voltage to overcome static friction. *'Try kP = 8.0.'*
- **Bronze:** students whose robot oscillates — kP too big. *'Halve it.'*
- **Bronze:** students whose robot does something completely wrong — sign error, or units bug (forgot the `0.0254` conversion). Send them to the reference card.
- **Silver:** students whose drift correction makes the drift WORSE — sign error in the rotation correction. Have them flip the variable, not fight the math.
- **Gold:** students whose `pid.atSetpoint()` never returns true — they need to add a velocity tolerance. Show them `setTolerance(2.0, 5.0)`.

### The high-leverage question

Before any student touches a kP value, make them predict: *'Right now, what do you expect to see in AdvantageScope?'* Then they run it. Compare prediction to reality. The prediction → run → compare loop is what makes them a tuning engineer instead of a button-presser. **This is the most important habit you can install in this lesson.**

---

## Phase 5 — Code Review (40–45 min)

*Walk the code-review section on the projector. This is where the curriculum lands.*

### Code review — answers

The Lesson 07 lab is a code review, not a bug hunt. The code compiles and runs — but a senior teammate would still ask for changes. Three notes, each tying back to a previous lesson:

#### Review note 1 — hardware in the subsystem

Line 3: `new TalonFX(13)` is direct hardware in the subsystem. This is exactly the bug Lesson 04 warned about. Without an IO interface, the code can't run in sim, can't be replayed, and can't switch to a different motor controller without rewriting the subsystem.
**Refactor:** introduce `ShooterIO` interface, `ShooterIOTalonFX` implementation, `ShooterIOSim` for simulation.

#### Review note 2 — magic numbers

Line 10: `* 60.0` converts rotations-per-second to rotations-per-minute. Fine math, no source-of-truth. If the gear ratio is anything other than 1:1, this is wrong; nobody could find that bug without reading every `getRpm()` call. Same for `kP = 0.0001` and `tolerance = 50.0`. All belong in `Constants.java` with explanatory names.
**This connects to Lesson 02's 'never hardcode numbers' rule.**

#### Review note 3 — motor control in `periodic()`

Line 13: `pid.calculate` + `setVoltage` inside `periodic()` means the shooter is always being driven, always. No way for a default command to take over. No interruption. Same bug as Lesson 03's broken-robot-lab #2: motor control belongs in commands, `periodic()` is for sensors and logging.
**Refactor:** expose `runAtRpm(double)` on the subsystem, write a `RunShooter` command that calls it from `execute()`.

### Tying it all together

After the third review note, take 60 seconds to make the curriculum land:

> **Closing script**
>
> *"Three review notes. Lesson 04, Lesson 02, Lesson 03 — every one of them connects back to a pattern we built earlier. The code I just showed you compiles and ships. It runs at competition. But a programmer who knows these patterns spots the issues in 30 seconds because they're not actually new — they're the same patterns you saw in Module 1 played out at scale."*
>
> *"You finished six lessons. You built a working autonomous, you can read encoders and gyros, you can tune a P-controller, you can read other people's code with the right eye. The next year of your programming life is applying these six concepts to your team's actual robot. None of it will be harder than what you just did. It will just be more of it. Go read your team's competition code."*

---

## Common Student Questions

**Q: My kP needs to be huge — like 50. Is that wrong?**
A: *"It depends on the units. If your error is in meters and your output is in volts, kP needs to convert meters → volts. That's a big number. If your error is in degrees and output is in normalized motor power, kP is small. There's no universal kP. Always think about what units kP is bridging."*

**Q: When do I use I or D?**
A: *"When P alone has a problem you can't tune away. Use I if the robot consistently settles short of the target — there's friction P can't overcome, and the integral term builds up to fight it. Use D if you can't reduce kP without going too slow — D damps the response. Most of the time, neither is needed."*

**Q: Why doesn't the robot stop exactly at the target?**
A: *"Because the output is proportional to error, and at the target error is zero — so the output is zero, but the robot still has momentum. Either you tune kP higher to brake harder, or you accept a tolerance. Real teams use tolerance. `atSetpoint()` with tolerance is the answer."*

**Q: Should I always use closed loop?**
A: *"No. Open loop is fine when accuracy doesn't matter — driver-controlled teleop, simple intakes, anything where you adjust by feel. Closed loop is for autonomous distances, shooter RPM, arm angles — anything that needs to land precisely without a human in the loop."*

**Q: Where do I learn more?**
A: *"Your team's competition code from a recent year. Read a subsystem. Ask: 'Is this the IO pattern? Is motor control in `periodic` or in commands? What's logged? Where's the PID?' That's what you do next. The WPILib documentation on PID is the second-best place."*

---

*Instructor Edition — Not for student distribution*