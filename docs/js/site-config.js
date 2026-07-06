/* ============================================================
   FRC Programming Curriculum - Site Configuration
   ============================================================ */

const SITE_CONFIG = {
  workInProgress: true,   // ← true - display work in progress banner and badge. flip to false to hide.
  wipBadgeText: "WIP",
  siteName: "BearBots 6964 - FRC Programming Curriculum",
  siteSubtitle: "Project-based learning for FRC student programmers. Java, AdvantageKit, XRP hardware.",
  banner: "🚧 Work in Progress - content may change",

  lessons: {
    "01": {
      module: 1,
      lesson: "01",
      title: "Setup + first drive",
      subtitle: "Get everything installed, run your first robot code, and drive in the simulator. The whole rest of the curriculum builds on this.",
      description: "Install everything, build a project, and drive a virtual robot with your keyboard. The foundation everything else builds on.",
      hardware: "Laptop",
      prereq: null,
      tools: "USB drive/Internet: VS Code WPILib, AdvantageKit",
      duration: "3 hours",
      filename: "lesson-01-setup.html",
      status: "ready",  // "ready", "current", "review", "soon"
      prev: null,
      next: "02"
    },
    "02": {
      module: 1,
      lesson: "02",
      title: "Template Structure + File Roles",
      subtitle: "Walk through every generated file and understand why it exists before touching anything.",
      description: "Walk through every generated file and understand why it exists before touching anything.",
      hardware: "Laptop",
      prereq: "Lesson 01",
      tools: "VS Code WPILib, AdvantageKit",
      duration: "3 hours",
      filename: "lesson-02-vscode-template.html",
      status: "ready",  // "ready", "current", "review", "soon"
      prev: "01",
      next: "03"
    },
    "03": {
      module: 1,
      lesson: "03",
      title: "What is a subsystem?",
      subtitle: "Why robots have separate files for separate mechanisms, and what happens when they don't.",
      description: "Why robots have separate files for separate mechanisms, and what happens when they don't.",
      hardware: "Laptop",
      prereq: "Lesson 02",
      tools: "VS Code WPILib, AdvantageKit",
      duration: "3 hours",
      filename: "lesson-03-subsystems.html",
      status: "ready",  // "ready", "current", "review", "soon"
      prev: "02",
      next: "04"
    },
    "04": {
      module: 2,
      lesson: "04",
      title: "Setting Up a Basic Subsystem",
      subtitle: "Convert a bare subsystem to the IO pattern, verify inputs in AdvantageScope, and run your first replay. Build day too.",
      description: "Convert the Scoop subsystem to the IO pattern using Arm as a reference. Verify logging in AdvantageScope and run replay mode for the first time.",
      hardware: "Laptop/XRP robot",
      prereq: "Lesson 03",
      tools: "VS Code WPILib, AdvantageKit, AdvantageScope",
      duration: "3 hours",
      filename: "lesson-04-io-pattern.html",
      status: "ready",  // "ready", "current", "review", "soon"
      prev: "03",
      next: "05"
    },
    "05": {
      module: 2,
      lesson: "05",
      title: "Closed-Loop Autonomous",
      subtitle: "Close the loop with P-control. Tune kP on the real XRP. Build your first reliable autonomous routine.",
      description: "Close the loop with P-control. Tune kP on the real XRP. Build your first reliable autonomous routine.",
      hardware: "Laptop/XRP robot",
      prereq: "Lesson 04",
      tools: "VS Code WPILib, AdvantageKit, AdvantageScope",
      duration: "3 hours",
      filename: "lesson-05-closed-loop.html",
      status: "soon",  // "ready", "current", "review", "soon"
      prev: "04",
      next: "06"
    },
    "06": {
      module: 2,
      lesson: "06",
      title: "Competition Prep",
      subtitle: "Commands, autonomous routines, and strategy. Write and tune everything you need for Orbit Odyssey. Competition is next session.",
      description: "Commands, the AutoChooser pattern, autonomous routines for Orbit Odyssey. Lock strategy, tune on the real field, commit code.",
      hardware: "Laptop/XRP robot",
      prereq: "Lesson 05",
      tools: "VS Code WPILib, AdvantageKit, AdvantageScope",
      duration: "3 hours",
      filename: "lesson-06-competition-prep.html",
      status: "soon",  // "ready", "current", "review", "soon"
      prev: "05",
      next: "07"
    },
    "07": {
      module: 2,
      lesson: "07",
      title: "Competition Day - Orbit Odyssey",
      subtitle: "Everything you built. One field. Real matches. 1v1 round-robin - every student competes individually.",
      description: "Final tweaks, practice runs, competitive matches, awards, and curriculum close.",
      hardware: "Laptop/XRP robot",
      prereq: "Lesson 06",
      tools: "XRP robot, Game Field",
      duration: "3 hours",
      filename: "lesson-07-competition.html",
      status: "soon",  // "ready", "current", "review", "soon"
      prev: "06",
      next: null
    }
  }
};
const ORBIT_KEY = 'orbit_unlocked_02';
const BYPASS_CODE = 'ORBIT!';