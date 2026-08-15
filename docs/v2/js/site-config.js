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
      subtitle: "Clone the repo, install the tools, and drive a virtual robot in the simulator. Everything else builds on this.",
      description: "Clone the repo, install the tools, and drive a virtual robot in the simulator. Everything else builds on this.",
      hardware: "Laptop",
      prereq: null,
      tools: "USB drive/Internet: VS Code WPILib, AdvantageKit",
      duration: "3 hours",
      filename: "lesson-01-setup.html",
      status: "review",  // "ready", "current", "review", "soon"
      prev: null,
      next: "02"
    },
    "02": {
      module: 1,
      lesson: "02",
      title: "Subsystem structure + build day",
      subtitle: "See how AdvantageKit subsystems are organized, then build Scoop and Elevator from snippets.",
      description: "See how AdvantageKit subsystems are organized, then build Scoop and Elevator from snippets.",
      hardware: "Laptop",
      prereq: "Lesson 01",
      tools: "VS Code WPILib, AdvantageKit",
      duration: "3 hours",
      filename: "lesson-02-vscode-template.html",
      status: "review",  // "ready", "current", "review", "soon"
      prev: "01",
      next: "03"
    },
    "03": {
      module: 1,
      lesson: "03",
      title: "Connect to XRP + plan your code",
      subtitle: "Deploy to real hardware, learn the command toolkit, and plan your Orbit Odyssey strategy.",
      description: "Deploy to real hardware, learn the command toolkit, and plan your Orbit Odyssey strategy.",
      hardware: "Laptop + XRP robot",
      prereq: "Lesson 02",
      tools: "VS Code WPILib, AdvantageKit, XRP robot",
      duration: "3 hours",
      filename: "lesson-03-subsystems.html",
      status: "soon",  // "ready", "current", "review", "soon"
      prev: "02",
      next: "04"
    },
    "04": {
      module: 2,
      lesson: "04",
      title: "Build session 1",
      subtitle: "Independent work: implement your planned commands and test on the XRP.",
      description: "Independent work: implement your planned commands and test on the XRP.",
      hardware: "Laptop + XRP robot",
      prereq: "Lesson 03",
      tools: "VS Code WPILib, AdvantageKit, XRP robot",
      duration: "3 hours",
      filename: "lesson-04-io-pattern.html",
      status: "soon",  // "ready", "current", "review", "soon"
      prev: "03",
      next: "05"
    },
    "05": {
      module: 2,
      lesson: "05",
      title: "Build session 2",
      subtitle: "Keep building. Tune constants, add autonomous modes, fix what broke.",
      description: "Keep building. Tune constants, add autonomous modes, fix what broke.",
      hardware: "Laptop + XRP robot",
      prereq: "Lesson 04",
      tools: "VS Code WPILib, AdvantageKit, XRP robot",
      duration: "3 hours",
      filename: "lesson-05-closed-loop.html",
      status: "soon",  // "ready", "current", "review", "soon"
      prev: "04",
      next: "06"
    },
    "06": {
      module: 2,
      lesson: "06",
      title: "Build session 3",
      subtitle: "Final features, edge cases, and practice runs before competition.",
      description: "Final features, edge cases, and practice runs before competition.",
      hardware: "Laptop + XRP robot",
      prereq: "Lesson 05",
      tools: "VS Code WPILib, AdvantageKit, XRP robot",
      duration: "3 hours",
      filename: "lesson-06-commands.html",
      status: "soon",  // "ready", "current", "review", "soon"
      prev: "05",
      next: "07"
    },
    "07": {
      module: 2,
      lesson: "07",
      title: "Build session 4",
      subtitle: "Last chance to code. Lock in your strategy and do a full competition rehearsal.",
      description: "Last chance to code. Lock in your strategy and do a full competition rehearsal.",
      hardware: "Laptop + XRP robot",
      prereq: "Lesson 06",
      tools: "VS Code WPILib, AdvantageKit, XRP robot",
      duration: "3 hours",
      filename: "lesson-07-competition.html",
      status: "soon",  // "ready", "current", "review", "soon"
      prev: "06",
      next: "08"
    },
    "08": {
      module: 2,
      lesson: "08",
      title: "Competition Day - Orbit Odyssey",
      subtitle: "Everything you built. One field. Real matches. 1v1 round-robin — every student competes individually.",
      description: "Final tweaks, practice runs, competitive matches, awards, and curriculum close.",
      hardware: "Laptop + XRP robot",
      prereq: "Lesson 07",
      tools: "XRP robot, Game Field",
      duration: "3 hours",
      filename: "lesson-08-competition.html",
      status: "soon",  // "ready", "current", "review", "soon"
      prev: "07",
      next: null
    }
  }
};
const ORBIT_KEY = 'orbit_unlocked_02';
const BYPASS_CODE = 'ORBIT!';