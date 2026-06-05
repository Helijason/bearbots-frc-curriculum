# Module 1 — Lesson 01: Setup + First Drive

**Stack:** Java | AdvantageKit | XRP
**Card #:** 01 — *Keep this. Add it to your binder.*

---

## The Big Idea

> Get every tool installed and run your first robot code.
> Everything else in the curriculum builds on what you set up today.

---

## Key Concepts

| Concept | Role | What it does |
|---|---|---|
| **WPILib + VS Code** | Editor | The FRC editor. Java + libraries. Purple = correct. |
| **AdvantageScope** | Dashboard | Bundled with WPILib. Sees the robot. Real-time graphs and 2D/3D field view. |
| **Starter project** | Code base | Complete working robot. Build with Ctrl+Shift+P. `BUILD SUCCESSFUL` = good. |
| **Simulator** | Test bench | Runs code on laptop. No hardware today. Drive with W, S, A, D keys. |
| **Reference card** | Cheat sheet | Two pages of patterns. Methods + conversions. Look up, then ask. |

---

## The Setup Workflow

1. Run WPILib installer → launch WPILib VS Code
2. Extract `Lesson01-Project.zip` → open `Lesson01\First Drive` folder in WPILib VS Code → Build
3. `Ctrl+Shift+P` → Simulate Robot Code → check `halsim_gui`
4. Set up keyboard: drag Keyboard 0 to Joystick[0] → enable Teleoperated
5. `Ctrl+Shift+P` → WPILib: Start Tool → select AdvantageScope
6. File → Connect to Simulator → select Default: NetworkTables 4 (`Ctrl+Shift+K`) → time bar starts at top
7. Line Graph tab → expand AdvantageKit → Drive → drag `LeftVelocityMetersPerSec` and `RightVelocityMetersPerSec` to Left Axis → drive with W/S/A/D
8. 2D Field tab → expand AdvantageKit → RealOutputs → Drive → drag Robot (Pose2d) to Poses → drive → watch robot move
9. 3D Field tab → add Robot pose again + FinalComponentPoses (arm) → App → Use Custom Assets Folder → restart AdvantageScope → right-click robot pose → select XRP Robot → drive with W/S/A/D, arm with Z/X

---

## The Core Loop You'll Use

> **Code → Build → Simulate → Drive → Watch values**

You'll run this loop hundreds of times.

- Code lives in VS Code.
- Values live in AdvantageScope.
- The loop is the curriculum.

---

## After This Lesson I Can…

- [ ] Open WPILib VS Code (purple theme)
- [ ] Launch AdvantageScope via WPILib: Start Tool
- [ ] Build the **First Drive** project to `BUILD SUCCESSFUL`
- [ ] Drive a simulated robot with W, S, A, D
- [ ] Connect AdvantageScope (time bar starts) and graph `LeftVelocityMetersPerSec` / `RightVelocityMetersPerSec`
- [ ] View the robot moving in AdvantageScope's 2D field view
- [ ] View the robot and arm moving in AdvantageScope's 3D field view with the XRP robot model
- [ ] Find the reference card and locate its main sections

---

## Key Vocabulary

- **WPILib** — The official FRC software suite — VS Code + Java + libraries + tools + AdvantageScope in one installer
- **AdvantageScope** — Log viewer for robot data — real-time graphs, 2D/3D field views, replay from saved logs
- **Simulator** — Runs robot code on your laptop with no hardware — same Java logic as a real robot
- **Build** — Compiles your Java source files into runnable bytecode — must succeed before you simulate
- **Reference card** — Two-page printable cheat sheet — XRP methods, unit conversions, the patterns you'll forget

---

## Questions I Still Have

*Write your questions here. Bring them to the next session.*

## My Notes

*Write anything here — surprises, connections, things to look up later.*

---

---

## Competition Connection

> **Orbit Odyssey** is the game you're building toward. Every tool you set up today — VS Code, the simulator, AdvantageScope — is what you'll use to write and debug the code that competes on that field.
>
> The loop you ran today (**Code → Build → Simulate → Drive → Watch values**) is the same loop you'll run in every lesson from here to competition day.

---

*FRC Programming Curriculum — Lesson 01*
*Next: Lesson 02 — WPILib template structure and file roles.*
*Keep this. Collect all 8.*