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
| **Session length** | 3 hours |
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
> This is also the lesson where students should feel the curriculum land. After the code review, take 60 seconds to tell them what they just accomplished — seven lessons, foundational FRC programming, a working mental model. They earned it.

---

## Session Timing

| Time | Phase | You do | Students do |
|---|---|---|---|
| **0–5 min** | **Hook** | Demo Lesson 06's auto twice — fresh battery, then partly drained. Show the difference in distance. | Watch. Realize 'set and pray' isn't reliable. |
| **5–30 min** | **Concept** | Open loop vs closed loop. Three sensors. Reading them through the IO layer. Log both velocity and position — explain why. | Follow on digital handout. Add the new fields to `DriveIOInputs`. |
| **30–60 min** | **Closing the loop** | Live-code: convert `DriveDistance` to P-control. Show kP tuning live in AdvantageScope. Show overshoot/oscillation/just-right. Show WPILib `PIDController`. | Replicate on their own laptops. |
| **60–120 min** | **Practice** | Circulate during tiered challenge. Bronze pushes everyone; Silver and Gold for confident students. | Bronze: P-control `DriveDistance`. Silver: gyro drift correction. Gold: P-control `TurnToAngle` using `PIDController`. |
| **120–150 min** | **Physical XRP tuning** | Students tune kP on real hardware, compare to sim behavior. | Run closed-loop auto on XRP. Find best kP. Record in log. |
| **150–165 min** | **Code review** | Walk through code review on the projector. Three notes, each tied back to a previous lesson. | Spot the 3 review notes. Recognize each from a previous lesson. |
| **165–180 min** | **Close** | Curriculum summary. "Go read your team's code." | Recognize what they've built. Hear the closing message. Pack up cards. |

> **45-minute compressed version**
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

## Phase 2 — Concept (5–30 min)

*Three things to teach: open vs closed, the three XRP sensors, reading them through the IO layer.*

### Open loop vs closed loop

Frame it as a question of what you're commanding:

- **Open loop ("set and pray"):** you command the actuator. *"Set motor to 0.5."* Whatever happens, happens. Fine for simple movements, prototyping, when accuracy doesn't matter.
- **Closed loop ("measure and adjust"):** you command the goal. *"Reach 1 meter."* The code reads sensors, compares to the goal, and adjusts the motor output every cycle (50 times per second). Self-correcting.

*Use 'set and pray' for open loop. Students remember it.*

### The three sensors

Connect each to a use case students already understand:

- **Encoder:** *'How far has each wheel turned?'* — counts pulses, converts to inches via gear-ratio constant. XRP: `getLeftDistanceInch()`, `getRightDistanceInch()`, `getLeftEncoderRate()`, `getRightEncoderRate()`.
- **Gyro:** *'Which way are we pointing?'* — single axis, reports heading in degrees relative to last reset. XRP: `gyro.getAngle()`.
- **Reflectance:** *'Is there a line under us?'* — two analog sensors, 0.0–1.0, high on dark surfaces. Used for line following. Won't be needed today.

*Mention units explicitly: encoders give inches, gyro gives degrees. Conversions live in the reference card.*

### Through the IO layer, always

This is review of Lesson 04. Open `DriveIOInputs.java` on the projector. Add the new fields:

```java
@AutoLog
public class DriveIOInputs {
    // ... existing fields ...
    public double leftPositionMeters = 0.0;
    public double rightPositionMeters = 0.0;

    // new for Lesson 07:
    public double leftVelocityMetersPerSec = 0.0;
    public double rightVelocityMetersPerSec = 0.0;
    public double headingDegrees = 0.0;
}
```

Then `DriveIOXRP.updateInputs()`:

```java
inputs.leftPositionMeters        = drivetrain.getLeftDistanceInch()   * 0.0254;
inputs.rightPositionMeters       = drivetrain.getRightDistanceInch()  * 0.0254;
inputs.leftVelocityMetersPerSec  = drivetrain.getLeftEncoderRate()    * 0.0254;
inputs.rightVelocityMetersPerSec = drivetrain.getRightEncoderRate()   * 0.0254;
inputs.headingDegrees            = gyro.getAngle();
```

> **The line that has to land**
>
> ***"Encoders give inches. Code wants meters. Multiply by `0.0254`. If you don't, your '1 meter' auto will travel 39 meters — off the field, through the wall, into the parking lot."***
>
> *Half the class will hit this bug on Bronze. Drill it now and they spot it themselves.*

> **Why log velocity AND position?**
>
> Position tells you "how far you've gone." Velocity tells you "how fast you're going." When debugging, you'll want both. If position looks right but velocity is jumpy — sensor noise problem. If velocity looks right but position is wrong — sign or units bug. Log both, debug faster.

---

## Phase 3 — Closing the Loop (30–60 min)

*Live-code the conversion of `DriveDistance` from open loop to P-control. Show kP tuning visually in AdvantageScope.*

### The P-control math — three lines

```java
double error  = target - current;   // how far off are we?
double output = error * kP;         // push proportional to error
drive.setVoltage(output);           // apply it
```

*kP is a constant you tune. Start with 1.0 and adjust based on what the robot does.*

### Complete closed-loop `DriveDistance`

Show this side-by-side with the Lesson 06 version. Same four-method structure — just smarter `execute()` and `isFinished()`.

```java
public class DriveDistance extends Command {
    private final DriveSubsystem drive;
    private final double targetMeters;
    private double startMeters;

    private static final double kP        = 4.0;   // volts per meter of error
    private static final double tolerance = 0.02;  // 2 cm

    public DriveDistance(DriveSubsystem drive, double meters) {
        this.drive = drive;
        this.targetMeters = meters;
        addRequirements(drive);
    }

    @Override public void initialize() {
        startMeters = drive.getLeftPositionMeters();
    }

    @Override public void execute() {
        double traveled = drive.getLeftPositionMeters() - startMeters;
        double error    = targetMeters - traveled;
        double volts    = error * kP;
        drive.setVoltage(volts, volts);
    }

    @Override public boolean isFinished() {
        double traveled = drive.getLeftPositionMeters() - startMeters;
        return Math.abs(targetMeters - traveled) < tolerance;
    }

    @Override public void end(boolean interrupted) {
        drive.stop();
    }
}
```

**Make the point:** same four-method structure. `isFinished()` changed from "have we passed?" to "are we within tolerance?" The framework didn't change. Just the brain.

### Live tuning demo

Run the auto with three different kP values. Open AdvantageScope. Graph `LeftPositionMeters` alongside the target.

- **kP = 0.5 (too small):** position lazily approaches target, never reaches it — can't overcome friction
- **kP = 4.0 (good):** smooth approach, slows near target, settles cleanly
- **kP = 50.0 (too big):** overshoots target, oscillates around it, may never settle

> **The tuning loop**
>
> 1. Start with kP = 1.0
> 2. Run the auto. Watch in AdvantageScope — graph target alongside current position.
> 3. Too slow? Double kP. Too oscillatory? Halve it.
> 4. Repeat until current converges smoothly to target.
>
> This is the actual workflow on real robots. AdvantageScope is what makes it possible — you can *see* the response curve and react.

### WPILib's `PIDController` — same math, less code

```java
private final PIDController pid = new PIDController(4.0, 0.0, 0.0);  // kP, kI, kD

@Override public void execute() {
    double output = pid.calculate(drive.getLeftPositionMeters(), targetMeters);
    drive.setVoltage(output, output);
}

@Override public boolean isFinished() {
    return pid.atSetpoint();  // uses configured tolerance
}
```

Show students: same behavior as the hand-rolled version. Pass `kI` and `kD` later if needed. Most teams use this from day one. Now students know what's under the hood.

### I and D in 60 seconds

- **I (Integral):** for steady-state error P can't tune away — accumulates error over time and builds extra push. Use when the robot consistently settles short.
- **D (Derivative):** damps oscillation — subtracts a term proportional to the rate of change of error. Use when kP alone oscillates and you can't reduce it without going too slow.

*Move on. Most teams use P-only most of the time.*

---

## Phase 4 — Practice (60–120 min)

*Tiered challenge. Bronze should land for everyone. Silver and Gold for students who finish early.*

### Silver tier — full solution reference

```java
private double startHeading;
private static final double kP       = 4.0;
private static final double kHeading = 0.05;

@Override public void initialize() {
    startMeters  = drive.getLeftPositionMeters();
    startHeading = drive.getHeadingDegrees();
}

@Override public void execute() {
    double traveled      = drive.getLeftPositionMeters() - startMeters;
    double distanceError = targetMeters - traveled;
    double baseVolts     = distanceError * kP;

    double headingError  = drive.getHeadingDegrees() - startHeading;
    double rotation      = headingError * kHeading;

    drive.setVoltage(baseVolts - rotation, baseVolts + rotation);
}
```

### Gold tier — `PIDController` for `TurnToAngle`

Key details from the handout:
- `new PIDController(kP, 0.0, 0.0)` with kP starting at 0.05
- `pid.setTolerance(2.0)` in the constructor (degrees)
- `execute()`: `double rot = pid.calculate(currentHeading - startHeading, targetDegrees);` — set left/right to `-rot, +rot`
- `isFinished()`: `return pid.atSetpoint();`
- If `atSetpoint()` never returns true (oscillating in/out of tolerance): `pid.setTolerance(2.0, 5.0)` adds a velocity tolerance requirement

### What to circulate for

- **Bronze:** robot doesn't move → kP too small. `error * kP` isn't producing enough voltage to overcome static friction. Try kP = 8.0.
- **Bronze:** robot oscillates → kP too big. Halve it.
- **Bronze:** completely wrong behavior → sign error or units bug (forgot `0.0254` conversion). Send to reference card.
- **Silver:** drift correction makes drift WORSE → sign error in rotation correction. Flip the variable, not the math.
- **Gold:** `pid.atSetpoint()` never returns true → needs velocity tolerance. Show `setTolerance(2.0, 5.0)`.

### The high-leverage question

Before any student touches a kP value: *"Right now, what do you expect to see in AdvantageScope?"* Then they run it. Compare prediction to reality. The prediction → run → compare loop is what makes them a tuning engineer instead of a button-presser. **This is the most important habit you can install in this lesson.**

---

## Phase 5 — Physical XRP Tuning (120–150 min)

*Students tune kP on real hardware and compare to sim.*

### What students do

- Deploy closed-loop `DriveDistance` to XRP
- Run 1-meter auto; pull log from USB
- Open in AdvantageScope — graph position vs time
- Tune kP until the response curve matches the sim "just right" shape
- Record the best kP value; note if it differs from sim

### What to watch for

- Students whose sim kP works but hardware oscillates — real hardware has more friction variation
- Students who declare "good enough" at first attempt without checking AdvantageScope
- Students who find their kP needs to be 2–3× higher on hardware than sim — normal; discuss why (motor back-EMF, encoder noise)

---

## Phase 6 — Code Review (150–165 min)

*Walk the code-review section on the projector. This is where the curriculum lands.*

### Code review — answers

The Lesson 07 lab is a code review, not a bug hunt. The code compiles and runs — but a senior teammate would flag three things. Each ties back to a previous lesson:

#### Review note 1 — hardware in the subsystem (ties to Lesson 04)

Line 3: `new TalonFX(13)` is direct hardware in the subsystem. Without an IO interface, the code can't run in sim, can't be replayed, and can't switch motor controllers without rewriting the subsystem.

**Fix:** introduce `ShooterIO` interface, `ShooterIOTalonFX` implementation, `ShooterIOSim` for simulation.

```java
private final ShooterIO io;
public ShooterSubsystem(ShooterIO io) { this.io = io; }
```

#### Review note 2 — magic numbers (ties to Lesson 02)

Line 10: `* 60.0` converts rotations-per-second to RPM with no name, no context, no source of truth. If the gear ratio is anything other than 1:1, this is wrong; nobody would find the bug without reading every `getRpm()` call. Same for `kP = 0.0001` and `tolerance = 50.0` — all belong in `Constants.java` with explanatory names.

**Fix:** `return motor.getVelocity().getValue() * Constants.Shooter.RPM_PER_RPS;`

#### Review note 3 — motor control in `periodic()` (ties to Lesson 03)

Line 13: PID calculation + `setVoltage` inside `periodic()` means the shooter is always being driven. No default command takeover, no clean interruption, no emergency stop. Same bug as Lesson 03's broken-robot-lab #2.

**Fix:** expose `runAtRpm(double)` on the subsystem, write a `RunShooter` command that calls it from `execute()`. `periodic()` should only do `io.updateInputs()` and `Logger.processInputs()`.

```java
// In ShooterSubsystem:
public void runAtRpm(double rpm) { io.setVoltage(pid.calculate(...)); }

// New command RunShooter calls runAtRpm() in execute()
```

---

## Phase 7 — Close (165–180 min)

### Tying the curriculum together

After the third review note, take 60 seconds to make the curriculum land:

> **Closing script**
>
> *"Three review notes. Lesson 04, Lesson 02, Lesson 03 — every one of them connects back to a pattern we built earlier. The code I just showed you compiles and ships. It runs at competition. But a programmer who knows these patterns spots the issues in 30 seconds because they're not new — they're the same patterns you saw in Module 1 played out at scale."*

Walk through what students actually built:

- **Lesson 01:** working environment, first robot code in simulation
- **Lesson 02:** every file in a WPILib project and what it does
- **Lesson 03:** separating mechanisms into subsystems, motor control in commands
- **Lesson 04:** IO pattern — subsystem, interface, implementation — making sim and replay possible
- **Lesson 05:** `@AutoLog`, AdvantageScope, replay mode, logging discipline
- **Lesson 06:** commands as four lifecycle methods, composition, AutoChooser
- **Lesson 07:** closing the loop with sensors, P-control, reading real team code with a critical eye

> **Final send-off**
>
> *"Everything from here is a longer version of the same patterns. New mechanisms, more sensors, harder routines — same subsystems, same IO pattern, same logging, same commands, same feedback loops. You're ready to read your team's competition code now."*
>
> *"Open the most recent year's code, find a subsystem, read it. Ask: 'Is this the IO pattern?' Then 'Are commands separated from periodic?' Then 'What's logged?' Then propose one change that brings it closer to what we built. That's how you become useful to a team."*

### Exit — last thing to do

> *"Save your seven summary cards somewhere you'll find them. Print them if you can. Tape the reference card to your laptop. The next time you're at competition at 11pm trying to figure out why the auto isn't working, you'll want all of this within reach."*

---

## Common Student Questions

**Q: My kP needs to be huge — like 50. Is that wrong?**
A: *"It depends on the units. If your error is in meters and your output is in volts, kP needs to convert meters → volts. That's a big number. If your error is in degrees and output is in normalized motor power, kP is small. There's no universal kP. Always think about what units kP is bridging."*

**Q: When do I use I or D?**
A: *"When P alone has a problem you can't tune away. Use I if the robot consistently settles short — there's friction P can't overcome, and the integral term builds up to fight it. Use D if you can't reduce kP without going too slow — D damps the response. Most of the time, neither is needed."*

**Q: Why doesn't the robot stop exactly at the target?**
A: *"Because the output is proportional to error, and at the target error is zero — so the output is zero, but the robot still has momentum. Either you tune kP higher to brake harder, or you accept a tolerance. Real teams use tolerance. `atSetpoint()` with tolerance is the answer."*

**Q: Should I always use closed loop?**
A: *"No. Open loop is fine when accuracy doesn't matter — driver-controlled teleop, simple intakes, anything where you adjust by feel. Closed loop is for autonomous distances, shooter RPM, arm angles — anything that needs to land precisely without a human in the loop."*

**Q: Where do I learn more?**
A: *"Your team's competition code from a recent year. Read a subsystem. Ask: 'Is this the IO pattern? Is motor control in `periodic` or in commands? What's logged? Where's the PID?' That's what you do next. The WPILib documentation on PID is the second-best place."*

---

*Instructor Edition — Not for student distribution*
