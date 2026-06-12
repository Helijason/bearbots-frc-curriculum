# FRC Programming Curriculum — Module 2, Lesson 04

# The IO Pattern and AdvantageKit Architecture

*The IO Pattern and AdvantageKit Architecture — applied to the BearBots elevator, scoop, and arm.*

> **Instructor Edition — Not for student distribution**

---

## At a Glance

| Field | Detail |
|---|---|
| **Target audience** | HS freshmen & sophomores, completed Lessons 02 and 03 |
| **Hardware** | XRP robot with arm (existing), elevator + scoop (students wire today) |
| **Session length** | 3 hours |
| **Key tools** | WPILib VSCode, Simulator, AdvantageScope, WPILib XRP documentation |
| **Prerequisites** | Lesson 03: What is a subsystem? |

---

## Learning Objectives

- Students can explain why the IO pattern separates hardware from logic
- Students can identify the three files in an AdvantageKit subsystem and state each file's job
- Students can read an existing IO implementation (`ArmIO`) and explain every line
- Students can design a new IO interface on a whiteboard before writing any code
- Students can implement `ScoopIO` and `ScoopIOXRP` from a designed interface
- Students can look up XRP hardware documentation to find encoder channel numbers
- Students can implement `ElevatorIO` and `ElevatorIOXRP` with correct unit conversions
- Students can connect the physical XRP and watch elevator encoder values change live in AdvantageScope
- Students can explain the startup position contract: elevator down, scoop flat before enabling

---

## Before You Start

### Room and hardware setup

- XRP robots assembled with elevator and scoop attachment — one per student or pair
- Elevator carriage manually positioned at the bottom before class
- Scoop servo manually positioned flat before class
- VSCode open on projector with the BearBots starter project
- AdvantageScope open and ready
- WPILib XRP documentation open in a browser tab on the projector:
  `https://docs.wpilib.org/en/stable/docs/xrp-robot/`
- Starter project folder structure visible in the Explorer panel

### File tree students are working toward by end of session

```
subsystems/
  drive/
    DriveSubsystem.java     ← exists, IO pattern reference
    DriveIO.java            ← exists, IO pattern reference
    DriveIOXRP.java         ← exists, IO pattern reference
  arm/
    ArmSubsystem.java       ← exists, IO pattern reference
    ArmIO.java              ← exists, IO pattern reference
    ArmIOXRP.java           ← exists, IO pattern reference
  elevator/
    ElevatorSubsystem.java  ← students build today
    ElevatorIO.java         ← students build today
    ElevatorIOXRP.java      ← students build today
  scoop/
    ScoopSubsystem.java     ← students build today
    ScoopIO.java            ← students build today
    ScoopIOXRP.java         ← students build today
```

### Startup position contract — say this before every session with hardware

> **Script — say this at the start of every hardware session**
>
> *"Before we enable the robot today — two things. Elevator carriage at the bottom. Scoop servo flat. Every time. The code assumes this. If the robot starts in the wrong position, the code will try to move from wherever it is, not from where it thinks it is. This is a real pre-match checklist item on competition robots. Get in the habit now."*

### Mental preparation

> **The most common mistake in this lesson**
>
> Explaining the IO pattern before students feel the pain it solves. Do not open with "today we're learning about interfaces." Start with the hook demo. Let the problem create the need for the solution.

> **The second most common mistake**
>
> Letting students jump to implementation before the whiteboard is done. The whiteboard phase is not optional pre-work — it is the design phase. Students who skip it write code they don't understand and can't debug.

---

## Session Timing

| Time | Phase | You do | Students do |
|---|---|---|---|
| **0–15 min** | **Hook** | Live demo: hardware change breaks everything vs IO version. Count the errors. Don't explain yet. | Watch. Form opinions. Wonder why. |
| **15–45 min** | **Model** | Live-code `ElevatorIO` + `ElevatorIOXRP` from scratch. Intentional bugs. Think out loud. | Watch the process. Ask questions as they form. |
| **45–75 min** | **Whiteboard** | Facilitate arm read-through, then elevator/scoop interface design. Don't settle debates too fast. | Read existing arm IO. Design elevator and scoop interfaces on whiteboard. |
| **75–135 min** | **Practice** | Circulate. Ask "what do you expect?" before every run. Redirect with questions, not answers. | Bronze: ScoopIO + ScoopIOXRP. Silver: ElevatorIOXRP full implementation. Gold: ElevatorSubsystem + coordination question. |
| **135–160 min** | **Broken robot lab** | Circulate. Don't give answers — give direction. | Find and fix three bugs. Confirm each fix in sim before moving on. |
| **160–175 min** | **Physical verification** | Connect XRP on projector. Demo elevator encoder live in AdvantageScope. | Connect their own XRP. Move elevator by hand. Watch values in AdvantageScope. |
| **175–180 min** | **Connect + wrap** | Exit check. Tease Lesson 05. | 60-second exit check. |

---

## Phase 1 — Hook (0–15 min)

*Make the pain of hardcoded hardware visceral before offering the solution.*

### Preparation — two projects before students arrive

Do not set this up in front of students. The demo loses impact if you are fumbling with files while explaining.

> **Project 1 — hardcoded hardware (the bad version)**
> A drivetrain subsystem that directly imports and instantiates `XRPDrivetrain` inside the subsystem class. No interface. No abstraction.

> **Project 2 — IO pattern version (the good version)**
> Same behavior. `DriveIO` interface + `DriveIOXRP` implementation. The subsystem imports only `DriveIO`.

### The demo

Open Project 1 on the projector.

> **Script — Hook**
>
> *"Here's a drivetrain subsystem. It drives. It works. Now watch what happens when I make one change — just one. I'm switching the motor type from `XRPMotor` to `TalonFX`."*
>
> [Make the change. Let the compiler errors cascade. Count them out loud as they appear.]
>
> *"That's [X] files broken from one change. Now here's the same robot built differently."*
>
> [Switch to Project 2. Make the same change. One file changes. Nothing else breaks.]
>
> *"I haven't explained anything yet. But I think you want to know why that happened."*

### Why the expanded hook time matters

The 45-minute version of this lesson gives the hook 5 minutes. At 3 hours, take 15. After the demo, let students talk for a few minutes:

- *"What's different between the two projects?"*
- *"Where did the errors come from in the first version?"*
- *"Why didn't the second version break?"*

Don't answer these questions yet. Let students build hypotheses. The model phase confirms or corrects them — and it sticks better that way.

---

## Phase 2 — Model (15–45 min)

*Live-code the IO pattern for the elevator from scratch. Do not paste finished code. The mistakes are the lesson.*

### What to build

Build `ElevatorIO` and `ElevatorIOXRP`. Use the elevator specifically — not the drivetrain — because students will implement this themselves in the practice phase. Watching you build it first gives them a model to follow, and the bugs you make intentionally are the same bugs they will hit.

### Step 1 — Start with the inputs struct (5 min)

```java
@AutoLog
public class ElevatorIOInputs {
    public double positionMeters = 0.0;
    public double velocityMetersPerSec = 0.0;
    public double appliedVolts = 0.0;
}
```

> **Say out loud while typing**
>
> *"Three fields. Position, velocity, voltage. These are the things we want to log from the elevator every cycle. Notice they're all public — AdvantageKit needs direct access to serialize them. And notice they all have defaults — if the hardware isn't connected, we get zeros, not null pointer exceptions."*
>
> *"The `@AutoLog` annotation is what makes the magic happen. Without it, the annotation processor won't generate `ElevatorIOInputsAutoLogged`, and none of this logs. We'll see what that failure looks like in the broken robot lab."*

### Step 2 — Write the interface (5 min)

```java
public interface ElevatorIO {
    void updateInputs(ElevatorIOInputs inputs);
    void setVoltage(double volts);
    void stop();
}
```

> **Say out loud while typing**
>
> *"Count the imports in this file. Zero. This interface has no idea what hardware the elevator uses. No `XRPMotor`. No `TalonFX`. No `Encoder`. It knows about nothing except the contract — what an elevator can do. That's the point."*
>
> *"Three methods. `updateInputs` reads hardware into the struct. `setVoltage` commands the motor. `stop` puts the mechanism in a safe state. Every IO interface we write follows this shape."*

### Step 3 — Implement it for the XRP (15 min)

```java
public class ElevatorIOXRP implements ElevatorIO {
    private final XRPMotor motor = new XRPMotor(3);
    private final Encoder encoder = new Encoder(/* channels — TBD */);

    @Override
    public void updateInputs(ElevatorIOInputs inputs) {
        inputs.positionMeters = encoder.getDistance(); // BUG — units
        inputs.velocityMetersPerSec = encoder.getRate(); // BUG — units
        inputs.appliedVolts = motor.get() * 12.0;
    }

    @Override
    public void setVoltage(double volts) {
        motor.set(volts); // BUG — range
    }

    @Override
    public void stop() {
        motor.set(0.0);
    }
}
```

> **Intentional mistakes to make and catch**
>
> **Bug 1 — encoder channels:** Leave the encoder constructor blank or with placeholder values. Say: *"I don't know these channel numbers off the top of my head. Neither should you. This is what documentation is for — we'll look it up together in the whiteboard phase."*
>
> **Bug 2 — units:** `encoder.getDistance()` returns inches by default. Type it wrong, run the sim, show the position value. Say: *"The elevator thinks it moved 12 meters. It moved about 30 centimeters. That's a 39x error. Where's it coming from?"* Let students answer. Then fix: `* 0.0254`.
>
> **Bug 3 — range:** `motor.set()` wants `-1.0` to `1.0`. Pass volts directly. Show what happens. Say: *"We sent 6 volts. The motor received... 1.0. It clamped us."* Fix: `volts / 12.0`.

> **Note on the encoder channels**
>
> Leave this as a genuine open question in the model phase. You will resolve it as a class during the whiteboard phase using the WPILib XRP documentation. This is intentional — it models the real workflow of reading hardware documentation before implementing.

### Step 4 — Write the subsystem shell (5 min)

```java
public class ElevatorSubsystem extends SubsystemBase {
    private final ElevatorIO io;
    private final ElevatorIOInputsAutoLogged inputs = new ElevatorIOInputsAutoLogged();

    public ElevatorSubsystem(ElevatorIO io) {
        this.io = io;
    }

    @Override
    public void periodic() {
        io.updateInputs(inputs);
        Logger.processInputs("Elevator", inputs);
    }

    public void setVoltage(double volts) {
        io.setVoltage(volts);
    }

    public void stop() {
        io.stop();
    }

    public double getPositionMeters() {
        return inputs.positionMeters;
    }
}
```

> **Key point to make here**
>
> *"Search this file for the word 'XRP'. You won't find it. This subsystem genuinely does not know what hardware it's running on. That's the pattern working correctly. In sim, we pass it a sim implementation. On the real robot, we pass it `ElevatorIOXRP`. The subsystem doesn't care which."*

### Handling questions during live coding

- **Why questions:** answer fully, even if it breaks your flow. These are the good ones.
- **"Can't I just hardcode it?" questions:** validate first. *"Yes, you can. Let's talk about what that costs you in three weeks when we switch to a different motor controller."*
- **Syntax questions:** answer briefly, promise to revisit after the demo.
- **Silence:** ask the room *"what should I type next?"* and wait. Comfortable silence is fine.

---

## Phase 3 — Whiteboard (45–75 min)

*Design before implementation. Students who skip this phase write code they cannot debug.*

### Part A — Arm IO read-through (10 min)

Open `ArmIO.java` and `ArmIOXRP.java` on the projector. Ask students to read them — not you. Call on different students to read each method signature out loud.

Ask these questions in order, waiting for student answers before moving on:

- *"What does this interface know about hardware?"* (Nothing — no imports)
- *"What's in the inputs struct? Why those fields?"*
- *"What does `stop()` do to a servo?"* (This is a genuine question — servo stop behavior is different from motor stop behavior. Let students think about it.)
- *"If we switched from this servo to a different servo brand, which file changes?"* (Only `ArmIOXRP`. Interface and subsystem stay identical.)

The arm is a reference implementation. Students have seen the pattern on the drivetrain in previous lessons — the arm confirms it's not a drivetrain-specific pattern. It works for any mechanism.

### Part B — Elevator interface design (15 min)

Clear the whiteboard. Tell students: *"We're designing `ElevatorIO` together. No code yet — just the contract. What methods does an elevator need? What should we log?"*

Facilitate the debate. Don't settle it too fast.

**Questions to drive the whiteboard:**

- *"What does the elevator actually do?"* (Moves up and down)
- *"What do we need to measure?"* (Position, velocity)
- *"What do we command?"* (Voltage — not speed, not position — those are for commands to calculate)
- *"What units should position be in?"* (Meters — always SI units at the subsystem level)
- *"What goes in the inputs struct vs what's a method?"* (Sensor readings → inputs struct. Commands → methods.)

**Expected whiteboard output:**

```
ElevatorIOInputs:
  positionMeters
  velocityMetersPerSec
  appliedVolts

ElevatorIO methods:
  updateInputs(ElevatorIOInputs)
  setVoltage(double volts)
  stop()
```

**Encoder channel lookup — do this as a class:**

Pull up the WPILib XRP documentation on the projector. Ask a student to navigate to the motor/encoder section. Find the channel numbers for Motor 3 and Motor 4. Write them on the whiteboard. This is the answer to the open question from the model phase.

> **Why this matters as a teaching moment**
>
> *"I left the encoder channels blank in the model phase because I didn't know them from memory — and you shouldn't memorize them either. This is what the documentation is for. Every time you wire a new mechanism, you look this up. Get comfortable with that workflow."*

### Part C — Scoop interface design (15 min)

Keep the elevator on the whiteboard. Add a new section for the scoop.

*"The scoop is a servo. It tilts to retain balls while we carry them, and tilts further to dump them into the basket. What does `ScoopIO` need?"*

**Questions to drive the whiteboard:**

- *"What does the scoop actually do?"* (Rotate to different angles)
- *"What do we measure from a servo?"* (Current angle — though XRP servos may not report this. Let students discover the limitation.)
- *"What do we command?"* (Target angle in degrees)
- *"What's the flat position? What's the carry position? What's the dump position?"* (These are constants — they go in `Constants.java`, not hardcoded in the IO layer)
- *"Does the scoop have a `stop()` method?"* (Good debate — servos hold position when powered, so "stop" is ambiguous. Decide as a class: `stop()` returns to flat position.)

**Expected whiteboard output:**

```
ScoopIOInputs:
  angleDegrees  (if servo reports angle — check docs)

ScoopIO methods:
  updateInputs(ScoopIOInputs)
  setAngle(double degrees)
  stop()           // returns to flat — CONSTANTS.SCOOP_FLAT_DEGREES
```

**Coordination question — introduce for Gold students:**

Once both interfaces are on the whiteboard, ask: *"The scoop needs to angle up to retain balls as the elevator rises. Which file handles that coordination?"*

Let the debate happen. The answer is: neither IO class. The IO layer only talks to hardware. Coordination between elevator position and scoop angle belongs in a command or a superstructure layer. Don't resolve this fully — Gold students will explore it in the practice phase.

---

## Phase 4 — Practice (75–135 min)

*Tiered challenge. Push students upward as they finish each tier. Never sit down during this phase.*

### Bronze tier — ScoopIO + ScoopIOXRP (30–40 min for most students)

Students implement the scoop IO pair using the whiteboard design and the arm IO as a reference. The scoop is simpler than the elevator — one servo, no unit conversion — so Bronze students can succeed here without being overwhelmed.

**What students build:**

```
subsystems/scoop/
  ScoopIO.java
  ScoopIOXRP.java
  ScoopSubsystem.java
```

**Success criteria:** Build succeeds. Scoop folder appears in AdvantageScope when sim is running.

**Common Bronze struggles:**

| Struggle | Response |
|---|---|
| Servo constructor arguments | *"Look at how the arm servo is constructed in `ArmIOXRP`. Use that as your reference."* |
| What angle is "flat"? | *"That's a constants question. Add `SCOOP_FLAT_DEGREES` to `Constants.java` — pick a value and we'll tune it on hardware later."* |
| `stop()` implementation | *"We decided on the whiteboard that stop returns to flat. Which method on the servo gets you there?"* |
| Scoop folder not in AdvantageScope | *"Is the subsystem instantiated in `RobotContainer`? A subsystem that isn't constructed doesn't exist."* |

### Silver tier — ElevatorIOXRP full implementation (30–40 min for students who finish Bronze)

Students implement `ElevatorIOXRP` using the encoder channels from the whiteboard documentation lookup. The unit conversion bugs from the model phase are the main challenge.

**What students build:**

```
subsystems/elevator/
  ElevatorIO.java         (from whiteboard design)
  ElevatorIOXRP.java      (with correct unit conversions)
  ElevatorSubsystem.java  (shell — methods come in Gold)
```

**Success criteria:** Build succeeds. Elevator folder appears in AdvantageScope. Position value reads in meters (not inches).

**Common Silver struggles:**

| Struggle | Response |
|---|---|
| Encoder channels wrong | *"Which motor port is the elevator on? What channels does the documentation say that port uses?"* |
| Position reads ~39× too high | *"What units does the encoder give by default? What units do we want? What's the conversion?"* |
| `motor.set()` takes volts directly | *"What range does `motor.set()` accept? Check the documentation."* |
| Build fails with `ElevatorIOInputsAutoLogged not found` | *"Where is `@AutoLog`? Check the inputs class."* |

### Gold tier — ElevatorSubsystem + coordination question (remaining time)

Students complete `ElevatorSubsystem` with public methods that commands can call, then explore the coordination question from the whiteboard: how should scoop angle relate to elevator position?

**What students do:**

1. Add public methods to `ElevatorSubsystem`: `setVoltage()`, `stop()`, `getPositionMeters()`
2. Register both subsystems in `RobotContainer`
3. Wire a simple test: hold a button → elevator runs up. Release → stops.
4. Explore the coordination question: *"As the elevator rises, the scoop should angle up to retain balls. Where does that logic live?"*

**The coordination discussion:**

Don't give Gold students the answer. Ask:

- *"Could you put the scoop angle logic in `ElevatorSubsystem.periodic()`?"* (You could, but then `ElevatorSubsystem` knows about `ScoopSubsystem` — tight coupling)
- *"Could you put it in `ScoopSubsystem.periodic()`?"* (Same problem in reverse)
- *"What if there was a third class that owned both?"* (This is the superstructure pattern — introduce the vocabulary but don't require implementation today)

> **Bonus question for students who finish Gold early**
>
> *"Your teammate wants to add a second elevator stage next month. Which files change? Which ones stay the same? Write your answer before touching any code."*
>
> Expected answer: Only `ElevatorIOXRP` changes (hardware implementation). `ElevatorIO` interface may need new methods if the second stage has different capabilities. `ElevatorSubsystem` mostly stays the same. `RobotContainer` wiring stays the same.

### Instructor role during practice

| Do this | Not this |
|---|---|
| Ask "what do you expect to see in AdvantageScope?" before every run | Give the answer directly |
| When stuck: "What does the arm IO do here? Can you do the same thing?" | Sit down |
| Redirect to documentation before giving channel numbers | Skip a student who seems to be making progress |
| Push Bronze finishers to Silver immediately | Let a student stay frustrated on one tier for more than 10 minutes |
| Pair a Gold student with a stuck Silver student | Explain to the whole group unless 3+ students have the same question |

---

## Phase 5 — Broken Robot Lab (135–160 min)

*Three bugs, standalone phase. Every fix must be confirmed by running the sim — reading the code is not enough.*

### Setup

Distribute (or point students to) the broken `ElevatorSubsystem` starter file. Three bugs, each from a different category:

### Bug 1 — Missing `@AutoLog` on the inputs class

`ElevatorIOInputs` has fields but no `@AutoLog` annotation. The annotation processor doesn't generate `ElevatorIOInputsAutoLogged`. The build fails with a confusing error, or if the student uses the un-AutoLogged class directly, `Logger.processInputs()` silently does nothing useful. The Elevator folder never appears in AdvantageScope.

**Acceptable hint:** *"What annotation does the inputs class need? Where have you seen it before today?"*

**Fix:** Add `@AutoLog` above the `ElevatorIOInputs` class declaration.

### Bug 2 — `processInputs` called before `updateInputs`

In `periodic()`, the order is wrong:

```java
// BUGGY version
Logger.processInputs("Elevator", inputs);  // logs stale data
io.updateInputs(inputs);                   // fills struct — too late
```

The log captures whatever was in the struct from the previous cycle. In AdvantageScope, everything appears delayed by one tick. In replay, the logged data doesn't match reality.

**Acceptable hint:** *"What's the rule about order? Which has to come first?"*

**Fix:** Swap the two lines.

### Bug 3 — `stop()` sets voltage to `1.0` instead of `0.0`

```java
// BUGGY version
public void stop() {
    motor.set(1.0); // full speed — not stopped
}
```

When any command ends and calls `stop()`, the elevator runs at full speed instead of stopping. This is physically dangerous on hardware.

**Acceptable hint:** *"What should stop() do to the motor? What value means 'off'?"*

**Fix:** Change `1.0` to `0.0`.

> **Run every fix in sim before claiming it's fixed**
>
> Reading the code and spotting the bug is not enough. Students must run the simulator and confirm the symptom is gone before moving on. This is the discipline that matters — knowing what to look for in AdvantageScope when something is wrong.

---

## Phase 6 — Physical Verification (160–175 min)

*This is the "see what the code actually does" phase. Connect the real XRP and watch hardware values change live.*

### Before connecting — startup position check

Before any student connects hardware, run through the checklist out loud:

- [ ] Elevator carriage at the bottom
- [ ] Scoop servo in flat position
- [ ] Robot is disabled

*"Every time. Before every enable. Get in the habit now."*

### Demo on the projector first

Connect the XRP to the projector laptop. Open AdvantageScope. Connect to the robot (not the simulator).

- Enable in Teleop
- Expand the `Elevator/` folder in AdvantageScope
- Slowly move the elevator carriage up by hand while the robot is enabled
- Watch `positionMeters` increase in real time
- Release — watch it stop
- Ask: *"What does the value read at the top of travel? Does that match what you'd expect in meters?"*

Then show the velocity field:

- Move the carriage quickly — spike in velocity
- Move slowly — low velocity
- Hold still — velocity near zero
- Ask: *"If you were writing a command that needed to know whether the elevator was moving, which field would you use?"*

### Students replicate on their own robots

Walk the room. Every student should see at least:

- Position value changing as they move the elevator
- Velocity spiking on fast movement
- Values returning to near-zero when stationary

> **Common physical verification issues**

| Issue | Response |
|---|---|
| AdvantageScope shows no Elevator folder | Check `RobotContainer` — subsystem must be instantiated |
| Position reads in inches, not meters | Unit conversion bug in `ElevatorIOXRP.updateInputs()` |
| Values don't change when moving | Check encoder channels against documentation |
| Robot won't connect | Check USB cable, XRP powered on, correct COM port |

---

## Phase 7 — Connect + Wrap (175–180 min)

### Exit check — 60 seconds, no grades

Ask students to answer one question before they pack up:

> *"Name the three files in an AdvantageKit subsystem and the job of each one."*

| Ready for Lesson 05 | Needs reinforcement before Lesson 05 |
|---|---|
| Names all three files correctly | Can only name one or two |
| Describes each job in one sentence | Confuses the interface with the implementation |
| Mentions that the subsystem doesn't import hardware | Can't explain why the separation matters |
| Connects it to something they built today | Needs the handout open to answer |

### Teaser for Lesson 05

> *"Next session we're going to drive the XRP, record a log file, and then replay exactly what happened — without the robot in the room. The elevator position data you logged today is the raw material for that. If it's not logged, we can't replay it. If it's not logged correctly, the replay is wrong. That's why today mattered."*

---

## Common Student Questions

**Q: Why can't I just use `XRPMotor` directly in the subsystem?**
A: *"You can. It will work fine today. In three weeks when the team switches to a different motor controller, you will edit every file that touches that motor. The IO pattern means you edit one file. That's the trade."*

**Q: Do I really need three files for a servo that does one thing?**
A: *"Yes. The pattern scales — the scoop today is one servo, but competition mechanisms have multiple motors, sensors, and state. If you learn the pattern on the simple case, you won't have to learn it under pressure on the complex one."*

**Q: Why does the subsystem have public methods like `setVoltage()` if commands can just call `io.setVoltage()` directly?**
A: *"Commands don't have access to `io` — it's private. Commands talk to subsystems. Subsystems talk to IO. The boundary matters: if a command could call IO methods directly, the subsystem would be bypassed and the logging loop wouldn't run."*

**Q: What happens if the encoder channels are wrong?**
A: *"Either you get zeros — the encoder isn't connected to that channel — or you get values from the wrong encoder. AdvantageScope will tell you which: if position never changes when you move the elevator, the channel is wrong."*

**Q: Why does the elevator need `appliedVolts` in the inputs struct if we're the ones setting it?**
A: *"Logging what you commanded is how you debug the difference between 'I told it to do X' and 'it did Y.' If you log the commanded voltage and the actual position, you can tell in replay whether the motor did what you asked. Without it, you're guessing."*

**Q: What happens in simulation if I don't have a DriveIOSim?**
A: *"You use an empty default implementation — a DriveIO that does nothing. The robot runs, nothing moves, and AdvantageKit still logs everything. Great for testing command logic without hardware."*

**Q: Do I write a new DriveIO interface for every robot?**
A: *"No. One interface, multiple implementations. The interface is the contract — it doesn't change just because the hardware does. This is the whole point."*

**Q: What if I forget to implement a method from the interface?**
A: *"Java will refuse to compile. Loudly. This is actually a feature — the compiler is your mean but honest friend who catches mistakes before the robot does."*

**Q: The scoop angle and elevator position need to be coordinated. Why don't we put that in `periodic()`?**
A: *"`periodic()` runs every 20ms regardless of what's happening. If you put coordination logic there, it always runs — even during autonomous when you want explicit control. Commands are the right place for coordination because they can be scheduled, interrupted, and ended cleanly. We'll build that in Lesson 06."*

---

## Post-Session — Instructor Homework

### Track for next session

- Which students finished Bronze only — pair with a Silver student in Lesson 05 practice
- Which students reached the coordination question — they're ready for the superstructure discussion in Lesson 06
- Any encoder channel issues that suggest a wiring problem to fix before Lesson 05
- Any unit conversion bugs that persisted — reinforce at the start of Lesson 05

### Before Lesson 05

- Verify all XRP robots have working elevator encoder reads in AdvantageScope
- Prepare a saved log file from a Lesson 04 practice session for the Lesson 05 hook demo
- If any student's elevator folder was empty in AdvantageScope, debug the `@AutoLog` and `processInputs` ordering before next session

---

## Quick Reference — Tear-Out Sheet

### The IO pattern in three sentences

> `ElevatorIO.java` defines what an elevator can do. It knows nothing about hardware.
> `ElevatorIOXRP.java` talks to the actual XRP motor and encoder. It is the only file allowed to know about XRP hardware.
> `ElevatorSubsystem.java` calls `ElevatorIO` methods. It has no idea what hardware it's running on. It doesn't need to.

### Unit conversions for this session

| Conversion | Formula | Why |
|---|---|---|
| Encoder inches → meters | `inches * 0.0254` | XRP encoders report in inches by default |
| Volts → motor percent | `volts / 12.0` | `motor.set()` wants `-1.0…1.0` |

### The startup position contract

Before every enable:
- Elevator carriage → bottom
- Scoop servo → flat

The code assumes this. If the robot starts in a different position, all position-based logic is wrong.

### Common bugs and symptoms

| Symptom | Most likely cause |
|---|---|
| Elevator folder missing in AdvantageScope | `@AutoLog` missing, or subsystem not in `RobotContainer` |
| Position reads ~39× too high | Forgot `* 0.0254` inches-to-meters conversion |
| Motor runs at full speed regardless of command | Passing volts directly to `motor.set()` without `/ 12.0` |
| Data delayed by one tick in AdvantageScope | `processInputs` called before `updateInputs` |
| `ElevatorIOInputsAutoLogged` not found | `@AutoLog` missing from inputs class |
| Position never changes when moving elevator | Wrong encoder channels — check documentation |

### If something goes wrong with hardware

- XRP won't connect: check USB cable, verify XRP is powered on, check COM port in device manager
- Encoder reads zero always: verify encoder channels against WPILib XRP documentation
- Servo doesn't move: check servo port number, verify `ScoopSubsystem` is instantiated in `RobotContainer`
- AdvantageScope shows no data when robot enabled: verify `Logger.processInputs()` is in `periodic()`, not the constructor

---

*Instructor Edition — Not for student distribution*
