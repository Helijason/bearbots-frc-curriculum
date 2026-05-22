# AdvantageKit IO pattern — reference sheet

**Bear Bots FRC Curriculum**
**Stack:** Java | AdvantageKit | XRP

---

## The core idea

> The subsystem never imports hardware. Only what's behind the IO does.

In AdvantageKit, every subsystem talks to a hardware interface — never to hardware directly. That interface can be backed by three different things depending on mode:

| Mode | IO implementation | What it does |
|---|---|---|
| **REAL** | `DriveIOXRP` | Talks to physical XRP motors and encoders |
| **SIM** | `DriveIOSim` | Fakes hardware with a physics model |
| **REPLAY** | `DriveIO {}` | No-op methods — log provides the input values |

The subsystem (`DriveSubsystem`) is identical in all three modes. The switch happens in `RobotContainer`.

---

## The three-file structure

```
DriveSubsystem.java  ─method calls→  DriveIO.java  ←implements─  DriveIOXRP.java
(subsystem logic,                    (the interface,              (hardware driver,
 no hardware imports)                 no hardware)                 XRP only)
```

**DriveIO.java — the interface**
Defines what a drivetrain can do. Zero hardware imports. Ever.

**DriveIOXRP.java — the hardware driver**
The only file allowed to know what hardware this is. Imports `XRPDrivetrain` here and only here.

**DriveSubsystem.java — the subsystem**
Makes method calls to the interface. Has no idea what's on the other end. Doesn't care.

---

## Mode selector — how the swap happens

`Constants.currentMode` drives a switch in `RobotContainer`. One line. No magic.

```java
var driveIO = switch (Constants.currentMode) {
    case REAL   -> new DriveIOXRP();
    case SIM    -> new DriveIOSim();
    case REPLAY -> new DriveIO() {};   // no-op — log feeds inputs via processInputs()
};
drive = new DriveSubsystem(driveIO);
```

---

## Programming concept 1 — Java interfaces as contracts

An interface defines *what* can be done. An implementation defines *how*. The subsystem only speaks to the interface.

**Analogy: Subsystem, Interface, and Hardware Driver**

| Role label | Example class | Responsibility |
|---|---|---|
| **Subsystem** | `DriveSubsystem` | Makes method calls — no hardware knowledge |
| **Interface** | `DriveIO` | Lists the legal method calls — zero hardware details |
| **Hardware Driver** | `DriveIOXRP` | Implements the interface — only file that knows what XRP is |

`DriveSubsystem` never meets `DriveIOXRP`. Swap XRP for a swerve robot — the subsystem's method calls don't change. Zero edits to `DriveSubsystem`. Only the hardware driver gets replaced.

```java
// Interface (the contract — no hardware, ever)
interface DriveIO {
    void setVoltage(double left, double right);
    void stop();
    void updateInputs(DriveIOInputsAutoLogged inputs);
}

// Hardware Driver (one per hardware platform)
class DriveIOXRP implements DriveIO {
    private final XRPDrivetrain dt = new XRPDrivetrain();

    @Override
    public void stop() {
        dt.stopMotor(); // real hardware call lives here only
    }
}
```

---

## Programming concept 2 — Logging loop order

Three steps inside `periodic()` in `DriveSubsystem.java`, every 20ms. The order is not optional.

```java
// DriveSubsystem.java
@Override
public void periodic() {
    io.updateInputs(inputs);                 // step 1 — read hardware into struct
    Logger.processInputs("Drive", inputs);   // step 2 — log struct / REPLAY injects here
    double pos = inputs.leftPositionMeters;  // step 3 — safe to use inputs now
}
```

**What breaks if you swap steps 1 and 2:**
In REPLAY mode, AdvantageKit injects saved data at step 2. If step 1 runs after, it overwrites the injected data with zeros. Replay sees a robot that never moved. The bug looks impossible to reproduce.

**Why replay works:**
REPLAY's `DriveIO {}` has no-op methods that write nothing to the inputs struct. `processInputs()` feeds the saved log values in instead. Same subsystem code. Different inputs source.

---

## Programming concept 3 — Logging: inputs vs. outputs

AdvantageKit logs two kinds of data differently. Knowing which is which matters.

| Kind | What it is | How it's logged |
|---|---|---|
| **Inputs** | Data read *from* hardware (encoder positions, voltages, sensor readings) | `@AutoLogInput` annotation on fields in the inputs struct — AdvantageKit handles the rest |
| **Outputs** | Data sent *to* hardware (voltage commands, setpoints, calculated values) | `Logger.recordOutput("Drive/leftVoltage", value)` — you call it manually |

**The inputs struct — `DriveIOInputs`**

```java
// DriveIO.java
public static class DriveIOInputs {
    @AutoLogInput public double leftPositionMeters = 0.0;
    @AutoLogInput public double rightPositionMeters = 0.0;
    @AutoLogInput public double leftVelocityMetersPerSec = 0.0;
}
```

`@AutoLogInput` tells AdvantageKit to log this field automatically inside `processInputs()`. No annotation → field is invisible to the logger and invisible to REPLAY.

**`DriveIOInputsAutoLogged` — why the name is different**

AdvantageKit generates a subclass called `DriveIOInputsAutoLogged` at compile time. That's the class you actually instantiate. It handles the logging boilerplate so your struct stays clean.

```java
// DriveSubsystem.java
private final DriveIOInputsAutoLogged inputs = new DriveIOInputsAutoLogged();
```

**Recording outputs manually**

```java
// DriveSubsystem.java — inside periodic() after processInputs()
Logger.recordOutput("Drive/leftVoltageCommand", leftVoltage);
Logger.recordOutput("Drive/speedMetersPerSec", inputs.leftVelocityMetersPerSec);
```

Key: the string key must start with the subsystem name. `"Drive/..."` not `"leftVoltage"`. AdvantageScope uses this to organize the signal tree.

**Data flow summary**

```
Hardware → updateInputs() → @AutoLogInput fields → processInputs() → REPLAY / AdvantageScope
                                                                              ↑
Commands → subsystem logic → Logger.recordOutput() ───────────────────────────┘
```

---

## Quick sanity check

- [ ] `DriveSubsystem` has zero hardware imports
- [ ] `DriveIOXRP` is the only file that imports `XRPDrivetrain`
- [ ] `updateInputs()` is before `processInputs()`. Always.
- [ ] Every input field in `DriveIOInputs` has `@AutoLogInput` — plain fields are invisible to REPLAY
- [ ] Every `recordOutput()` key starts with the subsystem name (`"Drive/..."`)
- [ ] Mode switch lives in `RobotContainer`, driven by `Constants.currentMode`

---

*Bear Bots FRC Curriculum — IO Pattern Reference Sheet*
*Companion to: StudentReferenceCard.md*
