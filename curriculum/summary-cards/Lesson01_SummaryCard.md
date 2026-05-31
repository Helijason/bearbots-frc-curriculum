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
2. Extract `FRC-XRP-Starter.zip`
3. Open folder in WPILib VS Code → Build
4. `Ctrl+Shift+P` → Simulate Robot Code → check `halsim_gui`
5. Set up keyboard: drag Keyboard 0 to Joystick[0] → enable Teleoperated
6. `Ctrl+Shift+P` → WPILib: Start Tool → select AdvantageScope
7. File → Connect to Simulator → select Default: NetworkTables 4 (`Ctrl+Shift+K`) → time bar starts at top
8. Line Graph tab → expand AdvantageKit → Drive → drag `LeftVelocityMetersPerSec` and `RightVelocityMetersPerSec` to Left Axis → drive with W/S/A/D
9. 2D Field tab → expand AdvantageKit → RealOutputs → Odometry → drag Robot (Pose2d) to Poses → drive → watch robot move
10. 3D Field tab → add Robot pose again → drive → use mouse to rotate/zoom/pan

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
- [ ] Build a project to `BUILD SUCCESSFUL`
- [ ] Drive a simulated robot with W, S, A, D
- [ ] Connect AdvantageScope (time bar starts) and graph `LeftVelocityMetersPerSec` / `RightVelocityMetersPerSec`
- [ ] View the robot moving in AdvantageScope's 2D field view
- [ ] View the robot moving in AdvantageScope's 3D field view
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