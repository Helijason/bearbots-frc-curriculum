# FRC Programming — Student Reference Card

*Tape this to your laptop. You'll thank yourself.*

**Stack:** Java | AdvantageKit | XRP

---

# Page 1 — Foundations (Lessons 1–4)

## The IO Pattern — 3 Files, 3 Jobs

```
DriveSubsystem.java  ─uses→  DriveIO.java  ←implements─  DriveIOXRP.java
(calls interface           (the contract,                (talks to XRP
 methods)                   no hardware)                  hardware)
```

> **FORBIDDEN:** `import XRPDrivetrain` inside `DriveSubsystem`.
> If `DriveSubsystem` imports `XRPDrivetrain`, the pattern is broken. (Buy the team snacks.)

---

## IO Pattern — Minimum Code

```java
public interface DriveIO {
    void updateInputs(DriveIOInputs inputs);
    void setVoltage(double left, double right);
    void stop();
}
```

```java
public class DriveIOXRP implements DriveIO {
    private final XRPDrivetrain dt = new XRPDrivetrain();

    @Override
    public void setVoltage(double l, double r) {
        dt.setVoltage(l, r);
    }

    @Override
    public void stop() {
        dt.stopMotor();
    }
}
```

---

## Subsystem + Logging Loop

```java
public class DriveSubsystem extends SubsystemBase {
    private final DriveIO io;
    private final DriveIOInputsAutoLogged inputs = new DriveIOInputsAutoLogged();

    @Override
    public void periodic() {
        io.updateInputs(inputs);                  // 1. read
        Logger.processInputs("Drive", inputs);    // 2. log
        // 3. use inputs.* below
    }
}
```

> Every `periodic()`, in this exact order:
> **1. updateInputs → 2. processInputs → 3. use**
> Swap 1 and 2 → data is one tick stale.

### DriveIOInputs — Typical Fields

```java
@AutoLog
public class DriveIOInputs {
    public double leftPositionMeters        = 0.0;
    public double rightPositionMeters       = 0.0;
    public double leftVelocityMetersPerSec  = 0.0;  // L07
    public double rightVelocityMetersPerSec = 0.0;  // L07
    public double headingDegrees            = 0.0;  // L07
}
```

Fill them in `DriveIOXRP.updateInputs()`:
```java
inputs.leftPositionMeters        = dt.getLeftDistanceInch()  * 0.0254;
inputs.leftVelocityMetersPerSec  = dt.getLeftEncoderRate()   * 0.0254;
inputs.headingDegrees            = gyro.getAngle();
```

> Log both position AND velocity. Jumpy velocity + clean position = sensor noise. Clean velocity + wrong position = units bug.

---

## The Three Modes

| Mode | Source | Output | Used for |
|---|---|---|---|
| **REAL** | Hardware → inputs | Writes log to USB | Competition |
| **SIM** | Physics sim → inputs | Writes log on laptop | `Ctrl+Shift+P` → Simulate |
| **REPLAY** | Saved log → inputs | No hardware needed | Re-runs old logs |

### Wiring — `RobotContainer.java`

```java
var drive = switch (Constants.currentMode) {
    case REAL   -> new DriveIOXRP();
    case SIM    -> new DriveIOSim();
    case REPLAY -> new DriveIO() {};
};
// pass to subsystem constructor
```

---

## XRP Hardware — Method Quick Reference

| Method | What it returns / does |
|---|---|
| `dt.getLeftDistanceInch()` | Left distance — **INCHES** |
| `dt.getRightDistanceInch()` | Right distance — **INCHES** |
| `dt.getLeftEncoderRate()` | Left rate — inches/sec |
| `dt.getRightEncoderRate()` | Right rate — inches/sec |
| `dt.tankDrive(left, right)` | Drive — needs `−1.0…1.0` |
| `dt.arcadeDrive(fwd, rot)` | Drive — needs `−1.0…1.0` |
| `dt.stopMotor()` | Stops both motors cleanly |
| `gyro.getAngle()` | Heading — degrees |
| `gyro.getRate()` | Turn rate — degrees/sec |
| `gyro.reset()` | Zero the heading |

---

## Sensors — Roles at a Glance

| Sensor | What it measures | Unit | Use for |
|---|---|---|---|
| **Encoder** | Wheel rotation → distance | inches → convert to meters | Distance commands, P-control |
| **Gyro** | Robot heading | degrees (resets on start) | Turns, drift correction |
| **Reflectance** | Surface brightness | 0.0–1.0 (high on dark) | Line following |

---

## Unit Conversions — Get These Right

```java
// Inches → meters (XRP encoders give in.)
double m = inches * 0.0254;

// Volts → percent (tankDrive: −1.0…1.0)
double pct = volts / 12.0;

// Degrees ↔ radians
double rad = Math.toRadians(degrees);
double deg = Math.toDegrees(radians);

// Rotations → radians
double rad = rotations * 2 * Math.PI;
```

---

## Common Bugs — Symptoms & Fixes

| Symptom | Fix |
|---|---|
| Position 39× too high | Inches not meters — `× 0.0254` |
| Robot always full speed | Volts → tankDrive — `/ 12.0` |
| `stop()` doesn't stop | Used `tankDrive(1,1)` — call `stopMotor()` |
| Drive folder empty in log | Missing `@AutoLog` on inputs class |
| Data is one tick behind | `processInputs` before `updateInputs` |
| Output isn't in folder | Key needs prefix: `"Drive/Pos"` |
| Robot creeps but never arrives | kP too small — double it |
| Robot overshoots, oscillates | kP too big — halve it |
| `atSetpoint()` never true | Tolerance not set — call `setTolerance()` in constructor |

---

## AdvantageScope — View Your Data

1. Run robot or sim with Logger active
2. Open AdvantageScope
3. File → Connect to Sim, OR Open Log…
4. Find a key: `Drive/LeftPositionMeters`
5. Drag onto a Line Graph or Field view
6. Empty? Check `processInputs()` in `periodic()`

---

## File Naming Convention

| Filename | Role |
|---|---|
| `SubsystemName.java` | the subsystem class |
| `SubsystemNameIO.java` | the interface (no hardware) |
| `SubsystemNameIOXRP.java` | XRP implementation |
| `SubsystemNameIOSim.java` | simulation implementation |

---
---

# Page 2 — Commands & Control (Lessons 5–6)

## The Command Lifecycle — What the Scheduler Does

```
Schedule → initialize() ─once→  ┌──────────────┐
                                ↓              │
                          execute() every 20ms │
                                ↓              │
                         isFinished()? ────────┘ (false: loop)
                                ↓ true
                          end(false) → STOP MOTORS → Done
```

> **Interruption:** Another command takes the same subsystem → `end(true)` is called → Done.
> Cleanup runs either way.

---

## The Four Methods — What Goes Where

| Method | Purpose |
|---|---|
| `initialize()` | Record start state, reset sensors |
| `execute()` | Set motor outputs (every 20ms) |
| `isFinished()` | Return `true` to end. Check sensors. |
| `end(interrupted)` | **STOP MOTORS. Always. Always.** |

> Plus: `addRequirements(subsystem)` in the constructor.

---

## Command — Minimum Code

```java
public class DriveDist extends Command {
    public DriveDist(DriveSubsystem d) {
        this.d = d;
        addRequirements(d);
    }

    @Override
    public void initialize() {
        start = d.getPos();
    }

    @Override
    public void execute() {
        d.setVoltage(6.0, 6.0);
    }

    @Override
    public boolean isFinished() {
        return d.getPos() - start >= 1.0;
    }

    @Override
    public void end(boolean i) {
        d.stop(); // ALWAYS
    }
}
```

---

## Composition — Building Routines from Commands

### `SequentialCommandGroup` — A then B then C
```
A → B → C
```
B starts only after `A.isFinished() = true`.

### `ParallelCommandGroup` — A, B, C all at once
```
A ─┐
B ─┼→ ends when ALL finish
C ─┘
```

---

## Decorator Shortcuts — Return Commands

```java
a.andThen(b)         // sequential A then B
a.alongWith(b)       // parallel, ends when both finish
a.deadlineWith(b)    // parallel, ends when A finishes
a.raceWith(b)        // parallel, ends when ANY finishes
a.withTimeout(3.0)   // ends after 3 seconds, max
a.until(() -> done)  // ends when condition is true
a.unless(() -> skip) // skip command if true
```

---

## AutoChooser — Dropdown in SmartDashboard

```java
// In RobotContainer.java
private final SendableChooser<Command> auto = new SendableChooser<>();

public RobotContainer() {
    auto.setDefaultOption("Drive 1m", new DriveDistance(drive, 1.0));
    auto.addOption("L-shape", driveLShape(drive));
    SmartDashboard.putData(auto);
}

public Command getAutonomousCommand() {
    return auto.getSelected();
}
```

---

## P-Control — Closing the Loop

```
target ──→ (+) ──→ kP ──→ robot ──→ sensor
              ↑                        │
              └───── (negative ────────┘
                      feedback)
```

Three lines of math:

```java
double error  = target - current;
double output = error * kP;
subsystem.setVoltage(output);
```

---

## kP Tuning — What You See

| State | Symptom | Action |
|---|---|---|
| **kP too small** | Creeps, never reaches | Double kP |
| **kP just right** | Smooth approach, settles | Ship it |
| **kP too big** | Overshoots, oscillates | Halve kP |

---

## P-Control via `PIDController` — WPILib Helper

```java
// We use kI=0, kD=0 — pure P-control.

// Field declaration:
private final PIDController pid = new PIDController(kP, 0.0, 0.0);

// In constructor — set tolerance:
pid.setTolerance(0.02);        // position only (meters)
pid.setTolerance(2.0, 5.0);   // position + velocity tolerance

// In execute():
double out = pid.calculate(drive.getPos(), targetMeters);
drive.setVoltage(out, out);

// In isFinished():
return pid.atSetpoint();
```

---

## Quick Sanity Checks — Run Before Committing

- [ ] Subsystem files don't import hardware classes
- [ ] `Logger.processInputs()` is in `periodic()`, AFTER `updateInputs`
- [ ] Every command's `end()` stops the motors
- [ ] Every `recordOutput()` key starts with subsystem name
- [ ] Constants live in `Constants.java`, not scattered in code
- [ ] `addRequirements()` is called in every command's constructor
- [ ] `setTolerance()` called before using `atSetpoint()`
- [ ] Velocity fields in `DriveIOInputs` use `* 0.0254` (inches/sec → m/s)

---

*FRC Programming Curriculum — Lessons 1–7 reference*
