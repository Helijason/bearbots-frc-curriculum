# FRC Programming Curriculum — Module 2, Lesson 07

# Make It Reliable — Closed-Loop Auto and Competition Prep

*Close the loop on autonomous. Tune on real hardware. Lock strategy. Commit code.*

> **Instructor Edition — Not for student distribution**

---

## At a Glance

| Field | Detail |
|---|---|
| **Target audience** | Students who completed Lesson 06 and have a working park or scoring auto |
| **Hardware** | XRP robot — Orbit Odyssey field set up and ready |
| **Session length** | 3 hours |
| **Key tools** | WPILib `PIDController`, AdvantageScope for tuning, Orbit Odyssey field |

---

## Learning Objectives

- Students can explain why open-loop auto is unreliable across different conditions
- Students can write the three lines of P-control math and explain each variable
- Students can convert their existing `DriveDistance` command from open-loop to closed-loop
- Students can tune kP empirically using AdvantageScope response curves
- Students can run their autonomous on the real field and verify it lands in the target zone
- Students can commit their code with a meaningful message and a strategy decision documented

---

## Before You Start

### Room setup

- Orbit Odyssey field fully set up — rubble placed, zones marked
- XRP robots charged and ready
- VSCode open on projector with a student's Lesson 06 open-loop `DriveDistance`
- AdvantageScope open with a saved Lesson 06 sim log showing overshoot — this is the hook
- Floor space for at least 2–3 robots running simultaneously

### Have ready

- A Lesson 06 log that clearly shows open-loop overshoot — graph position vs time
- A post-conversion log showing clean P-control settling — same graph, different curve
- Tape on the field marking the edge of the Low Rubble Zone parking area

> **Instructor mindset for this lesson**
>
> This is not a teaching day. Students are not learning new patterns today — they're applying what they know to make their code work reliably. Your job is to keep them moving, unstick anyone who's blocked on a bug, and enforce the discipline of constants-only tuning once they're on the field. Resist the urge to introduce anything new. If a student finishes early, they help a partner — not explore new features.

> **Fast finishers**
>
> Students who finish closed-loop conversion and field tuning early move to their scoring routine — add it as a second AutoChooser option, verify in sim, then run it on the field. They work their own code the whole session. Extension is more depth, not tutoring.

---

## Session Timing

| Time | Phase | You do | Students do |
|---|---|---|---|
| **0–10 min** | **Hook** | Side-by-side AdvantageScope: open-loop overshoot vs closed-loop settle. Ask: what's the difference? | Watch. Identify the problem they already have. |
| **10–40 min** | **Concept + live code** | Explain P-control in 3 lines. Live-convert `DriveDistance`. Show kP tuning in sim. | Follow along. Ask questions. |
| **40–90 min** | **Sim build phase** | Circulate. Enforce sim-first. Push everyone through closed-loop conversion before field. | Convert their own `DriveDistance` to closed-loop. Verify in sim. Tune kP in sim first. |
| **90–150 min** | **Field iteration** | Manage field access. Circulate. Constants-only rule enforced. | Run auto on real field. Tune `PARK_DISTANCE_METERS` and kP in `Constants.java` only. |
| **150–165 min** | **Strategy lock** | Facilitate decision. Every student commits. | Choose final auto strategy. Document it. Commit code. |
| **165–180 min** | **Practice matches (if time)** | Run informal Orbit Odyssey matches. Keep score. | Drive. Compete. See their auto work in a real match context. |

---

## Phase 1 — Hook (0–10 min)

*Make the open-loop problem visceral before offering the solution.*

### Opening

Open AdvantageScope on the projector. Show two position-vs-time graphs side by side — or two tabs:

- **Tab 1:** last lesson's open-loop auto. Position climbs past the target, overshoots, stops wherever momentum ran out.
- **Tab 2:** closed-loop version. Position approaches target, slows near it, settles cleanly within 2cm.

> **Script**
>
> *"Same command. Same target distance. Same field. One of these parks in the zone every time. The other parks in the zone sometimes — when the battery is fresh and the floor is smooth and you're feeling lucky. Which one do you want at competition?"*

Pause.

> *"The difference is three lines of math. That's today."*

---

## Phase 2 — Concept + Live Code (10–40 min)

*Fast. This is review territory — students have the command framework. Just add the math.*

### The problem with open loop

```java
// Open loop — Lesson 06 version
@Override public void execute() {
    drive.setVoltage(6.0, 6.0);  // fixed power, no feedback
}

@Override public boolean isFinished() {
    return drive.getLeftPositionMeters() - startMeters >= targetMeters;
}
```

What breaks: battery drops from 12V to 10V mid-match. The robot moves slower. The encoder hits the target but the robot was moving slower, so it stops 15cm short. Or the floor has more friction. Or less. Open loop ignores all of this.

### The fix — three lines of P-control

```java
double error  = targetMeters - traveled;  // how far off?
double output = error * kP;               // push proportional to error
drive.setVoltage(output, output);         // apply it
```

When far from target: `error` is large, `output` is large — drives hard.
When near target: `error` is small, `output` is small — coasts in gently.
At target: `error` is zero, `output` is zero — stops.

*Physics does the rest.*

### Live-code the conversion

Open the student's Lesson 06 `DriveDistance` on the projector. Make the changes live:

```java
private static final double kP        = 4.0;   // tune this
private static final double tolerance = 0.02;  // 2cm — tune if needed

@Override public void execute() {
    double traveled = drive.getLeftPositionMeters() - startMeters;
    double error    = targetMeters - traveled;
    double output   = error * kP;
    drive.setVoltage(output, output);
}

@Override public boolean isFinished() {
    double traveled = drive.getLeftPositionMeters() - startMeters;
    return Math.abs(targetMeters - traveled) < tolerance;
}
```

> **Key point to make while typing**
>
> *"`isFinished` changed from 'have we passed the target?' to 'are we within 2cm?' That's the tolerance. The robot might oscillate slightly around the target — that's fine as long as it's within tolerance. We don't need perfection. We need reliability."*

### Show kP tuning in sim — live

Run the auto three times with different kP values. Graph `LeftPositionMeters` in AdvantageScope alongside a horizontal line at the target.

- **kP = 0.5:** creeps, stops short. Can't overcome friction.
- **kP = 4.0:** smooth approach, settles cleanly.
- **kP = 20.0:** slams past, oscillates, never settles.

> **The tuning loop — say this explicitly**
>
> *"Start at 1.0. Run it. Too slow? Double it. Oscillating? Halve it. Watch the curve. The curve tells you everything. This is not guessing — it's reading data."*

### WPILib `PIDController` — optional shortcut

Show this as an option for Gold students or fast finishers. Same behavior, cleaner code:

```java
private final PIDController pid = new PIDController(4.0, 0.0, 0.0);

@Override public void execute() {
    double output = pid.calculate(drive.getLeftPositionMeters() - startMeters, targetMeters);
    drive.setVoltage(output, output);
}

@Override public boolean isFinished() { return pid.atSetpoint(); }
```

Call `pid.setTolerance(0.02)` in the constructor. Don't introduce I and D today.

---

## Phase 3 — Sim Build Phase (40–90 min)

*Everyone converts their `DriveDistance` before touching the field. No exceptions.*

### The sim-first gate

> **Script — enforce this clearly**
>
> *"Here's the rule for today: nobody runs on the field until their auto ends cleanly in sim. That means the command initializes, runs, and ends — AdvantageScope shows the command lifecycle in the Commands folder. If it doesn't end in sim, it won't end on the field. Sim first."*

### What students do

1. Copy their Lesson 06 `DriveDistance` into the new project
2. Add kP and tolerance constants to `Constants.java`
3. Rewrite `execute()` and `isFinished()` with P-control math
4. Build → simulate → run auto → watch AdvantageScope
5. Tune kP in sim until the position curve settles cleanly
6. Show instructor the AdvantageScope graph before getting field time

### What to circulate for

| Symptom | Response |
|---|---|
| Robot doesn't move in sim | kP too small or tolerance too large — check both |
| Robot oscillates in sim | kP too big — halve it |
| `isFinished` never returns true | Tolerance too tight or error sign wrong — add `Math.abs()` |
| Position reads in wrong units | Inches-to-meters conversion missing — `* 0.0254` |
| Student skips straight to field | Send them back to sim — politely but firmly |

### Fast finishers

If a student has their sim verified and tuned before 90 minutes:
- Add their scoring routine as a second AutoChooser option in sim
- Tune kP for the scoring routine separately — different distances may need different constants

---

## Phase 4 — Field Iteration (90–150 min)

*60 minutes on the real field. This is the payoff.*

### Field access rules

- **Sim-verified only:** no student runs on the field without an instructor seeing their AdvantageScope graph first
- **Constants only:** once on the field, the only allowed changes are in `Constants.java`. No structural code changes. No rewriting commands. This is competition discipline.
- **Log every run:** connect XRP to AdvantageScope after each run. Pull the log. Look at the position curve. Tune from data, not from guessing.

> **Why constants-only matters — say this explicitly**
>
> *"At competition you don't get to rewrite commands between matches. You get to change constants. Get in that habit now. If your auto is consistently 10cm short, you change `PARK_DISTANCE_METERS`. You don't rewrite `DriveDistance`."*

### What students do

- Place robot at starting position
- Run auto mode — watch where it stops
- Pull log from USB, open in AdvantageScope
- Compare position curve to sim curve — same shape? Different stopping point?
- Adjust `PARK_DISTANCE_METERS` or kP in `Constants.java`
- Repeat until the robot reliably parks in the zone across 3 consecutive runs

### What to watch for

- kP that worked in sim oscillates on hardware — real friction varies. Usually need slightly higher kP.
- Robot parks correctly on smooth floor but not on field surface — note this, it's a real competition variable
- Students who change kP wildly between runs — redirect: *"What does the curve tell you? Double or halve based on the shape, not the feeling."*
- Students who declare victory after one good run — require 3 consecutive successful runs before strategy lock

### Fast finishers on the field

If a student has their park auto reliably working before others finish:
- Add their scoring routine as a second AutoChooser option
- Verify the new option in sim before running it on the field
- Run it on the field, log it, tune it — same constants-only discipline

---

## Phase 5 — Strategy Lock (150–165 min)

*Every student commits to a final auto strategy. No more changes after this — Lesson 08 is competition day.*

### The decision

Bring the group together. Each student (or pair) answers out loud:

> *"What is your autonomous strategy for competition tomorrow? Park only, or scoring attempt? Why?"*

Arguments to surface:
- Park is 5 guaranteed points. Scoring attempt adds risk.
- If your scoring routine works 80%+ of the time in practice, it's worth it.
- If your alliance partner is also parking, maybe one of you attempts scoring.
- Strategy depends on what you can do reliably — not what's theoretically possible.

Don't settle the debate for them. Let them make the call.

### The commit

Every student must:

1. Set their AutoChooser default to their chosen strategy
2. Add a comment in `RobotContainer.java`: `// Competition strategy: [Park / Score + Park / High Zone] — tuned [date]`
3. Run one final sim verification
4. Git commit: `git commit -m "Competition auto: [strategy] — kP=[value], dist=[value]m"`

> **Why the commit message format matters**
>
> *"If something goes wrong at competition and you need to roll back, that commit message tells you exactly what you had. 'Fixed stuff' is not a commit message."*

---

## Phase 6 — Practice Matches (165–180 min, if time)

*Only if strategy lock finished early. Don't rush it.*

Run informal 1v1 or 2v2 Orbit Odyssey matches using the actual game manual scoring. Keep score on the whiteboard. Each student runs their locked auto, then drives teleop.

- Keep matches short — 90 seconds total (30s auto + 60s teleop)
- Between matches: 5-minute debrief only. One observation per student.
- No code changes between matches.

> **What to watch for**
>
> Students who want to change their auto after seeing it work (or fail) in a match — this is the right instinct, wrong timing. *"Write it down. That's what Lesson 08 is for — but even there, constants only."*

---

## Common Student Questions

**Q: My kP is different on hardware than in sim. Is that wrong?**
A: *"Normal. Sim doesn't model friction or battery sag. Real hardware usually needs a higher kP — the sim version is a starting point, not a final answer. That's why we iterate on the field."*

**Q: Should I use `PIDController` or the hand-rolled version?**
A: *"Either works. `PIDController` is cleaner and has `atSetpoint()` built in. Hand-rolled makes the math more visible. Pick one and stick with it — don't mix them in the same command."*

**Q: My auto works 4 out of 5 times. Is that good enough?**
A: *"Depends. 80% reliable is better than most teams at their first competition. If the 1 failure is a complete miss of the zone, that's a problem. If it's 5cm short of the zone, tune the distance constant. What does the AdvantageScope curve look like on the failure run?"*

**Q: Can I change my auto strategy at competition?**
A: *"Yes — that's what the AutoChooser is for. You pick your strategy before each match from the dashboard. But the code for all your options needs to be committed and working today. You can't write new commands at competition."*

**Q: What if my partner's auto and mine conflict?**
A: *"That's alliance strategy — talk to your partner before the match. The AutoChooser lets you pick independently. In Orbit Odyssey the field is divided so robots mostly stay on their side during auto."*

---

## Post-Session — Instructor Homework

### Before Lesson 08

- Confirm every student has committed code with a valid commit message
- Verify every robot's auto runs in sim cleanly — check AdvantageScope before competition day
- Set up the full Orbit Odyssey field if not done already
- Generate match schedule (use the ChatGPT prompt from the game manual, or assign manually for your group size)
- Print scorecards from the game manual

### Track

- Which students are park-only — pair them with scoring students as alliance partners where possible
- Any robots with persistent hardware issues — schedule 10-minute troubleshoot at the start of Lesson 08
- kP and distance constants per student — if you need to help someone tune at competition, knowing their baseline saves time

---

*Instructor Edition — Not for student distribution*
