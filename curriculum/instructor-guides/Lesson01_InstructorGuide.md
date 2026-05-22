# FRC Programming Curriculum — Module 1, Lesson 01

# Setup + First Drive

*Get every student installed, building, and driving a simulated robot before they ever touch hardware.*

> **Instructor Edition — Not for student distribution**

---

## At a Glance

| Field | Detail |
|---|---|
| **Target audience** | HS freshmen & sophomores, brand new to FRC programming |
| **Hardware** | Student laptops only — no XRP needed today |
| **Session length** | 2–3 hours (one extended session, not 45 minutes) |
| **Key tools** | WPILib installer (includes AdvantageScope), USB drive with starter project |

---

## Learning Objectives

- Students have WPILib + VS Code installed and can launch WPILib VS Code
- Students have AdvantageScope installed (included with WPILib) and can open it
- Students can build the starter project to `BUILD SUCCESSFUL`
- Students can launch the simulator, enable teleop, and drive with the keyboard
- Students can connect AdvantageScope and watch logged values change in real time
- Students can view the robot pose in AdvantageScope's 2D/3D view
- Students know where the reference card lives and have skimmed it once

---

## Before You Start

### USB drive contents — prepare ONE per student (or one per pair)

- WPILib installer — Windows `.exe` + VS Code `.zip` (offline install)
- Starter project ZIP — `FRC-XRP-Starter.zip`
- Reference card PDF — `XRP-Reference-Card.pdf`

### Download locations

- WPILib: https://docs.wpilib.org/ → Installation
- AdvantageScope is bundled with WPILib — no separate download needed

### Backup laptops

- Have 2–3 pre-configured laptops ready with everything installed
- Use these for students whose installs fail — troubleshoot personal laptops later

### Network

- If possible, disable school firewall/content filtering for this session
- If not, USB-drive install works — Gradle dependencies will still need internet on first build

---

> **The most important instructor mindset for this lesson**
>
> Setup failures are not a moral failing. They are the cost of using real software on real laptops in a real school. Resist the urge to make students troubleshoot their personal machine for an hour. Switch to a backup laptop after 15 minutes of stuck. The goal today is everyone leaves with a working setup — not necessarily on their own laptop.

---

## Session Timing

| Time | Phase | You do | Students do |
|---|---|---|---|
| **0–10 min** | **Hook + setup** | Frame the day. Hand out USB drives. Verify everyone has one. | Plug in laptop. Copy USB contents to Documents folder. |
| **10–60 min** | **Install WPILib** | Live-demo on projector. Circulate. Triage stuck students into backup laptops after 15 min. | Run installer. Choose options. Wait. Launch WPILib VS Code 2026. Verify AdvantageScope opens (bundled). |
| **60–100 min** | **Build the starter** | Demo: open folder, build, see `BUILD SUCCESSFUL`. Watch for VS-Code-vs-WPILib-VS-Code mistakes. | Extract ZIP. Open in WPILib VS Code. Build. See `BUILD SUCCESSFUL`. |
| **100–150 min** | **First drive** | Demo simulator + AdvantageScope flow on projector first. This is the payoff — everyone must reach it. | Launch sim. Enable teleop. Drive with WASD/arrows. Connect AdvantageScope. Watch values move. |
| **150–170 min** | **2D/3D pose view** | Demo adding robot pose to AdvantageScope's 2D/3D tab. | Add pose field. Watch robot move on screen as they drive. |
| **170–180 min** | **Reference card + wrap** | Walk through reference card sections. Run end-of-session checklist student by student. | Save reference card. Run through checklist. Pack up laptop. |

> **90-minute compressed version**
> If you only have 90 minutes (single class period), accept that some students will leave with incomplete setups. Skip the 2D/3D pose view and the reference card walkthrough. Get everyone through Install → Build → First Drive at minimum. Schedule a follow-up for the pose view and the reference card before Lesson 02.

---

## Phase 1 — Hook + Setup (0–10 min)

*Set expectations and hand out materials.*

### Opening

Don't pretend this isn't a slow session. It is. Tell students up front.

> **Script — what to say at the start**
>
> *"Today's goal is simple: get everything installed and see your first robot code run. Installations fail sometimes — that's normal. If yours doesn't work, use one of the backup laptops and we'll troubleshoot your own laptop later. The important thing is everyone leaves today with a working setup."*

### Hand out USB drives

- Verify every student has a USB drive (or knows which pair-partner has one)
- Tell students to copy the contents to their Documents folder before running anything
- Don't run installers from the USB drive — copy first, then run

---

## Phase 2 — Install WPILib (10–60 min)

*The slow one. Plan for 50 minutes. Students will have time to chat — that's fine. Your job is to triage failures.*

### What students do

- Run the WPILib installer (`.exe` on Windows)
- Select the existing VS Code archive for offline install when prompted
- Accept Windows SmartScreen warnings
- Choose options: keep default install path, install everything
- Wait 10–15 minutes for extraction
- Launch WPILib VS Code 2026 (purple theme = correct one)
- Open AdvantageScope (bundled with WPILib — no separate install needed)

### What you do

- Circulate constantly. Don't sit at the front.
- Watch for the common issues below. Most show up early.
- After 15 minutes of stuck on one issue, redirect the student to a backup laptop

### Common issues — WPILib

| Issue | Solution |
|---|---|
| **"Not enough disk space"** | Free up ~5 GB or use a backup laptop. |
| **Installer hangs at extraction** | Wait longer — first install is genuinely slow. After 20 minutes of no progress, restart it. |
| **VS Code won't launch after install** | Restart computer, then try again. If still failing, use a backup laptop. |
| **Windows SmartScreen blocks installer** | Click "More info" → "Run anyway". |
| **Already had VS Code; opened wrong one** | WPILib VS Code is purple-themed. Pin it to taskbar to avoid the mistake again. |
| **AdvantageScope won't open** | It's under the WPILib install folder. Check Start menu for "AdvantageScope". |

> **Pacing check — by 60 minutes**
>
> Most students should have WPILib installed, WPILib VS Code launched, and AdvantageScope verified open. Anyone still stuck should be on a backup laptop now.

---

## Phase 3 — Build the Starter Project (60–100 min)

*First time real code touches their laptop. Watch for the WPILib-VS-Code-vs-regular-VS-Code mistake. Demo on projector first.*

### Demo on the projector first

- Show extracting the ZIP into Documents folder
- Show File → Open Folder in WPILib VS Code
- Show "Yes, I trust the authors"
- Show `Ctrl+Shift+P` → WPILib: Build Robot Code
- Show terminal output ending in `BUILD SUCCESSFUL`

### Then students replicate

Walk the room. Catch these mistakes early:

- Working from inside the ZIP without extracting
- Opening a single file instead of the project folder
- Using regular VS Code (no purple theme) instead of WPILib VS Code
- Cancelling the Gradle dependency download because "it's slow"

### Common issues — Starter project

| Issue | Solution |
|---|---|
| **"Could not find build.gradle"** | Student opened a single file, not the folder. Use File → Open Folder. |
| **Build fails with Gradle errors** | Check internet — first build downloads dependencies (~2–5 min). |
| **"Java not found"** | Opened regular VS Code, not WPILib VS Code. Switch. |
| **Build runs but no terminal output** | Terminal panel collapsed. Click the Terminal tab at bottom. |
| **"Trust the authors" dialog never closes** | Click in the editor area first to give it focus, then click Yes. |

> **Pacing check — by 100 minutes**
>
> Everyone has `BUILD SUCCESSFUL` on their screen. If anyone is still stuck on the build, switch them to a backup laptop now — they need to make it to the first drive in this session.

---

## Phase 4 — First Drive + AdvantageScope (100–150 min)

*This is the payoff. Make sure everyone gets here. Demo every step on the projector first — then watch students replicate. The wow moment is when the AdvantageScope graph spikes as they hold W.*

### Live demo sequence

Run this top-to-bottom on the projector. Don't skip steps. Students follow along on their own laptops afterward.

#### Step 1 — Launch the simulator

- `Ctrl+Shift+P` → WPILib: Simulate Robot Code
- Check `halsim_gui` → OK
- Wait for build (fast — already compiled)
- Simulation GUI window opens

#### Step 2 — Set up keyboard driving

- In Simulation GUI → System Joysticks panel → drag `Keyboard 0` to `Joystick[0]` slot
- Robot State panel → Teleoperated → Enable
- Click Simulation GUI window — keyboard only works when this window has focus
- Keys: W/↑ forward, S/↓ backward, A/← turn left, D/→ turn right

#### Step 3 — Connect AdvantageScope

- Open AdvantageScope (don't close VS Code)
- File → Connect to Simulator (or `Ctrl+K`)
- Confirm "Connected" appears in bottom-left
- Connect BEFORE driving — otherwise the first seconds of data are lost

#### Step 4 — Drive and watch

- In AdvantageScope: expand Drive folder, drag `LeftVelocityRadPerSec` onto graph
- Drag `RightVelocityRadPerSec` onto the same graph
- Switch to Simulation GUI, hold `W` for 2–3 seconds, release
- Switch back to AdvantageScope — both lines spike up, then drop to zero
- Ask: *'What happens if you press A or D?'* Let them try.

### Common issues — First drive

| Issue | Solution |
|---|---|
| **Simulation GUI doesn't appear** | Check for popup blocker. Window may have opened off-screen — drag it back. |
| **Robot doesn't respond to keys** | Two causes: (1) Teleop not enabled, (2) Simulation GUI doesn't have focus. Click it. |
| **AdvantageScope won't connect** | Simulator must be running first. Restart sim, then connect. |
| **Connected, but no values appear** | Robot must be enabled in teleop. Disabled robots don't publish data. |
| **Values exist but graph stays flat** | Wrong fields dragged. Use `Drive/LeftVelocityRadPerSec`, not Setpoints. |

> **Pacing check — by 150 minutes**
>
> Every student has seen velocity values spike on the AdvantageScope graph. If anyone hasn't, stop the lesson and get them there before moving on.

---

## Phase 5 — 2D/3D Pose View (150–170 min)

*The bonus wow. AdvantageScope can render the robot's position on a field view. This is where simulation stops feeling abstract.*

### What students do

- In AdvantageScope, open a new tab → select **2D Field** (or **3D Field**)
- In the left sidebar, find the `Drive/Pose` field (or similar pose field logged by the starter project)
- Drag it onto the 2D/3D view
- Switch to the Simulation GUI and drive — the robot icon on the field should move

### Common issues — 2D/3D pose

| Issue | Solution |
|---|---|
| **No Pose field visible** | Robot must be enabled and running. Check the sidebar for any field with "Pose" in the name. |
| **Robot doesn't move on field** | Verify the correct field is dragged — not a velocity or encoder field. |
| **2D view shows robot but it's off the field** | Field image may need to be selected. Check AdvantageScope's field dropdown. |

> **Pacing check — by 170 minutes**
>
> Students have seen the robot move on the 2D/3D view. If time is short, this phase is the first to cut.

---

## Phase 6 — Reference Card + Wrap-Up (170–180 min)

*Cool down. Students are tired. Make this section short and concrete — checklist, save the reference card, send them home with a clear sense of what they accomplished.*

### Reference card walkthrough

Open the reference card on the projector. Spend 5 minutes pointing at sections — not reading them. The goal is recognition, not memorization.

- **XRP Drivetrain methods** — *"this is where you'll look up `arcadeDrive()` in Lesson 04"*
- **Unit conversions** — *"this prevents the most common bug in Lesson 04"*
- **AdvantageKit logging pattern** — *"the three lines you'll write in every subsystem"*
- **CommandScheduler** — *"the line that must be in `robotPeriodic()`"*

### End-of-session checklist

Walk through each student. Verify each item before they pack up:

- [ ] WPILib VS Code opens (purple theme)
- [ ] AdvantageScope opens
- [ ] Starter project builds successfully
- [ ] Simulator runs and responds to keyboard
- [ ] AdvantageScope shows values when driving
- [ ] AdvantageScope 2D/3D view shows robot moving
- [ ] Reference card saved

> **Script — what to say at the end**
>
> *"You just installed a complete development environment, compiled real robot code, drove a simulated robot, watched live data update on a graph, and saw the robot move on a 2D field view. That's a lot. Next lesson, we'll look at what VS Code actually created for us — and why the code is structured the way it is. Bring your laptop, your power cord, and the reference card."*

---

## Common Student Questions

**Q: Why do we need both VS Code and AdvantageScope?**
A: *"VS Code is where you write code. AdvantageScope is where you see what the robot is doing. They're different tools for different jobs. You'll have both open most of the time."*

**Q: When do we use the real XRP robot?**
A: *"Lesson 04. Today is about getting your laptop ready. The simulator lets us write and test code before we touch any hardware — that's how real teams work too."*

**Q: What if I already have VS Code installed?**
A: *"WPILib VS Code is different from regular VS Code — it has robot-specific tools built in. You need the WPILib version. Pin it to your taskbar so you don't accidentally open the wrong one."*

**Q: My install is stuck. Should I cancel?**
A: *"If the progress bar moved at all in the last 10 minutes, no — wait. If it's been frozen for more than 15 minutes with no disk activity, cancel and try again. After two failed attempts, switch to a backup laptop."*

**Q: Do I have to bring my laptop every session?**
A: *"Yes. Every session. With the power cord. The whole curriculum is hands-on — there's no useful version of these lessons without your laptop."*

---

## Post-Session — Your Homework as Instructor

### Send to students

- A reminder to bring laptop + power cord + reference card to Lesson 02
- Backup laptop assignments — who's borrowing which machine
- Optional: link to the digital handout (`lesson-01-setup.html`) for review

### Track for next session

- Which students are on backup laptops
- Which students had major issues — schedule 1-on-1 troubleshooting before Lesson 02
- Lessons learned — record any issues that should be fixed before next year's Lesson 01

---

## Lesson 01 Success Metrics

By the end of this session:

- 80%+ of students have installations working on their own laptops
- 100% of students have a working setup — own laptop or backup
- 100% of students have seen the simulator run successfully
- 100% of students have seen values change in AdvantageScope
- 100% of students have seen the robot move in AdvantageScope's 2D/3D view

> If these metrics aren't met, do not proceed to Lesson 02 yet. Schedule a follow-up session and finish the setup. Lesson 02 assumes a working environment.

---

*Instructor Edition — Not for student distribution*
