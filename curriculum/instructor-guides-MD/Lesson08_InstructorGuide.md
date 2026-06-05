# FRC Programming Curriculum — Module 2, Lesson 08

# Competition Day — Orbit Odyssey

*Everything you built. One field. Real matches.*

> **Instructor Edition — Not for student distribution**

---

## At a Glance

| Field | Detail |
|---|---|
| **Target audience** | Students who completed Lesson 07 with committed, field-tested auto code |
| **Hardware** | XRP robot — Orbit Odyssey field fully set up |
| **Session length** | 3 hours |
| **Format** | 1v1 round-robin — every student competes individually |

---

## Before Students Arrive

### Field setup
- Full Orbit Odyssey field assembled and inspected
- Rubble pieces counted and placed at starting positions
- Amplifier on the Earth Pedestal
- Centerline marked clearly
- Scoring zones verified against game manual dimensions

### Match schedule
Generate a 1v1 round-robin schedule before the session. For 8–10 students:
- 8 students: 16 matches (each student plays 4)
- 10 students: 20 matches (each student plays 4)

Use the ChatGPT prompt from the game manual adapted for 1v1:
> *"Create a round-robin 1v1 tournament schedule for [N] players where each player plays [4] matches and no two players face each other more than once."*

Print the schedule. Post it visibly. Students should know their match order before tweaks begin.

### Scorecards
Print individual scorecards (one per student, tracks all their matches). Adapted from the game manual for 1v1:

| Category | Points |
|---|---|
| Rubble in Low Zone (auto) | 1 pt each |
| Rubble in High Zone (auto) | 3 pts each |
| Park in Low Zone (auto) | 5 pts |
| Lap completion (teleop) | 5 pts each |
| Lap with Amplifier (teleop) | +3 pts per lap |
| Amplifier returned to Earth (endgame) | 10 pts |
| Low Zone Parking (endgame) | 5 pts |

> **No Coopertition bonus in 1v1.** Remove that row from scorecards.

### Robot inspection checklist
Run every robot through inspection before tweaks begin:

- [ ] Fits in 10-inch cube at starting configuration
- [ ] Weight under 1 kg
- [ ] Alliance color marker mounted and visible
- [ ] Team number on marker
- [ ] No loose parts or unsafe stored energy
- [ ] Code committed — no uncommitted changes

---

## Session Timing

| Time | Phase | You do | Students do |
|---|---|---|---|
| **0–10 min** | **Opening + inspection** | Welcome. Post match schedule. Run robot inspection. | Check in. Review match schedule. Inspect robot. |
| **10–40 min** | **Final tweak window** | Enforce constants-only and sim-first rules. Circulate. Hard stop at 40 min. | Last tuning adjustments — constants only. Must verify in sim before any field run. |
| **40–55 min** | **Practice matches** | Run 2–3 casual matches. No score kept. Field familiarization only. | Drive. Get comfortable with the field. Confirm auto works from match start position. |
| **55–160 min** | **Competitive matches** | Run match schedule. Keep time. Score each match. Post running totals. | Compete. Between matches: observe, strategize, cheer. |
| **160–175 min** | **Awards + debrief** | Announce results. Give awards. Run curriculum close. | Celebrate. Reflect. |
| **175–180 min** | **Pack up** | Supervise. | Disassemble field. Pack robots. |

---

## Phase 1 — Opening + Inspection (0–10 min)

### Opening

> **Script**
>
> *"Everything you've built over the last seven lessons comes down to today. You have working code. You have a strategy. You have a robot that does something on its own for 30 seconds. That's real. Let's see how it does."*

Post the match schedule where everyone can see it. Give students 2 minutes to find their matches and their first opponent.

### Robot inspection

Run every robot through the checklist before tweaks begin. If a robot fails inspection:
- Weight/size: student fixes mechanically — no code involved
- Missing marker: have spares ready
- Uncommitted code: student commits before anything else happens

---

## Phase 2 — Final Tweak Window (10–40 min)

*30 minutes. Hard stop. Constants only. Sim first.*

> **Script — set the rules clearly at the start**
>
> *"You have 30 minutes. Two rules: constants only — no rewriting commands, no new files, no structural changes. And sim first — if you change a constant, run it in sim before you touch the field. At 40 minutes, laptops close and we run practice matches. Use your time well."*

### What counts as constants-only

Allowed:
- `PARK_DISTANCE_METERS` in `Constants.java`
- `kP` in `Constants.java`
- `AUTO_TIMEOUT_SECONDS` in `Constants.java`
- AutoChooser default option selection

Not allowed:
- Rewriting `DriveDistance.java`
- Adding new commands
- Changing subsystem logic
- Any new files

### What to watch for

- Students who want to rewrite commands because their auto "almost works" — redirect: *"What constant would fix this? Change that."*
- Students whose sim shows a problem they can't fix with constants — acknowledge it, move on. One session can't fix every problem. The competition runs regardless.
- Students who are already good — let them relax, observe the field, think about teleop strategy

### Hard stop at 40 minutes

No exceptions. If a student's auto isn't working at 40 minutes, it isn't going to get fixed in the next 5. Close laptops. Move to practice.

---

## Phase 3 — Practice Matches (40–55 min)

*2–3 casual matches. No score kept. Field familiarization only.*

Run matches with whoever is available — doesn't need to follow the schedule. Goals:

- Every student confirms their auto runs from the correct starting position
- Every student gets at least one teleop drive on the actual field
- Any catastrophic auto failures surface here, not during competitive play

> **If a student's auto completely fails in practice**
>
> Give them 5 minutes with their laptop — constants only, sim first. If it still doesn't work: their competition strategy becomes park-by-driving-manually. That's a valid teleop decision. Don't let a broken auto derail the whole session.

---

## Phase 4 — Competitive Matches (55–160 min)

*~100 minutes, ~20 matches for 10 students. Keep it moving.*

### Match cadence

Target 4–5 minutes per match cycle:
- 30 sec: robots to starting positions, rubble placed
- 30 sec: auto period
- 30 sec: transition (students pick up controllers)
- 120 sec: teleop + endgame
- 60 sec: score, record, reset field

### Scoring

Two students serve as scorers per match — rotate the role so everyone does it at least once. Scorers:
- Watch the auto period and count rubble scored
- Count laps during teleop
- Verify amplifier return and parking at endgame
- Call out the score to the instructor for recording

Post running totals on the whiteboard after every match. Students should be able to see where they stand.

### Between matches

Students are not on their laptops between matches. They:
- Watch the match in progress
- Note what's working for other robots
- Think about their teleop strategy for their next match

> **The one adjustment allowed between matches**
>
> If a student's auto consistently fails the same way (always 10cm short, always turns the wrong direction), they may change one constant between matches — confirmed with instructor, sim-run if time allows. This mirrors real competition pit workflow.

### Managing the field

- Reset rubble to starting positions between every match
- Verify robots start within frame perimeter on their side
- Call out "Autonomous — GO" clearly; use a timer
- Call "Teleop — GO" after the transition period
- Call "Endgame" at 30 seconds remaining
- Call "STOP" clearly — drivers must stop immediately

### If a match goes wrong

- Robot leaves the field: stop the match, return robot, restart if time allows
- Robot stops responding: student may briefly interact with robot to reset (1 ticket per the game manual)
- Two robots collide: apply penalty rules from the game manual — but keep it light, this is camp

---

## Phase 5 — Awards + Debrief (160–175 min)

### Awards

Announce final standings from the scoreboard. Consider awards beyond just winning:

| Award | Description |
|---|---|
| **Most Reliable Auto** | Highest auto score average across all matches |
| **Most Improved** | Biggest gap between first match score and last match score |
| **Best Driver** | Highest teleop score average |
| **Gracious Professionalism** | Student who helped others, called their own penalties, competed with the best attitude |
| **Innovation Award** | Most creative autonomous strategy |

> **Gracious Professionalism is not a consolation prize.** In FRC culture it carries real weight. Present it seriously.

### Curriculum close — 5 minutes

After awards, brief close. This is the moment that's been waiting since Lesson 01:

> **Script**
>
> *"Seven lessons ago you installed a software environment and drove a simulated robot with your keyboard. Today you competed with code you wrote — autonomous routines that scored real points on a real field without you touching the controller.*
>
> *Everything in between: subsystems, the IO pattern, logging, commands, closed-loop control — those aren't just curriculum topics. They're the same patterns that FRC teams use at competition. The code structure you built here is the same structure you'll find in any well-written FRC codebase.*
>
> *You're not starting from zero anymore. You have a mental model that transfers. When you open your team's code this fall, you'll recognize it. And when something breaks at 11pm before a match, you'll know where to look."*

Take 2 minutes for open reflection — ask the room:
- *"What was the hardest thing you built?"*
- *"What would you do differently if you started over?"*
- *"What do you want to learn next?"*

---

## Phase 6 — Pack Up (175–180 min)

- Students disassemble field elements and return to storage
- Robots packed up
- Laptops closed and stored
- Reference cards and summary cards collected or kept — student's choice

---

## Post-Session — Instructor Notes

### Send to students after camp

- Final standings
- Their git repository link — they own this code
- What to do next: link to WPILib docs, FRC Java programming resources, team code repositories to explore

### What to improve before next year

- Note any lesson where time consistently ran over
- Note any concept students consistently struggled with
- Note any hardware issues (encoder channels, servo ports) that caused repeated confusion
- Note which auto strategies scored most reliably — update `Constants.java` defaults in the starter project

---

*Instructor Edition — Not for student distribution*
