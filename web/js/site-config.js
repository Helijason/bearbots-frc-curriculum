/* ============================================================
   FRC Programming Curriculum — Site Configuration
   ============================================================ */
 
const SITE_CONFIG = {
  workInProgress: true,   // ← flip to false to hide WIP banner + badge
  siteName: "BearBots 6964 - FRC Programming Curriculum",
 
  lessons: {
    "01": {
      module: 1,
      lesson: "01",
      title: "Setup + first drive",
      subtitle: "Get everything installed, run your first robot code, and drive in the simulator. The whole rest of the curriculum builds on this.",
      description: "Install everything, build a project, and drive a virtual robot with your keyboard. The foundation everything else builds on.",
      hardware: "No hardware needed",
      duration: "~2-3 hours",
      filename: "lesson-01-setup.html",
      prev: null,
      next: "02"
    },
    "02": {
      module: 1,
      lesson: "02",
      title: "WPILib Template Structure and File Roles",
      subtitle: "Walk through every generated file and understand why it exists before touching anything.",
      description: "Walk through every generated file and understand why it exists before touching anything.",
      hardware: "No hardware needed",
      duration: "~2-3 hours",
      filename: "lesson-02-vscode-template.html",
      prev: "01",
      next: "03"
    },
    "03": {
      module: 1,
      lesson: "03",
      title: "What is a subsystem?",
      subtitle: "Why robots have separate files for separate mechanisms, and what happens when they don't.",
      description: "Why robots have separate files for separate mechanisms, and what happens when they don't.",
      hardware: "No hardware needed",
      duration: "~2-3 hours",
      filename: "lesson-03-subsystems.html",
      prev: "02",
      next: "04"
    },
    "04": {
      module: 1,
      lesson: "04",
      title: "The IO Pattern and AdvantageKit Architecture",
      subtitle: "The IO pattern and AdvantageKit architecture. The most important concept in the curriculum.",
      description: "The IO pattern and AdvantageKit architecture. The most important concept in the curriculum.",
      hardware: "XRP robot",
      duration: "~2-3 hours",
      filename: "lesson-04-io-pattern.html",
      prev: "03",
      next: "05"
    },
    "05": {
      module: 1,
      lesson: "05",
      title: "How do I debug a robot that isn't here?",
      subtitle: "@AutoLog, AdvantageScope navigation, and replay mode. Turn \"it broke at competition\" into \"I can see exactly what happened.\"",
      description: "@AutoLog, AdvantageScope navigation, and replay mode. Turn \"it broke at competition\" into \"I can see exactly what happened.\"",
      hardware: "XRP robot",
      duration: "~2-3 hours",
      filename: "lesson-05-logging.html",
      prev: "04",
      next: "06"
    },
    "06": {
      module: 1,
      lesson: "06",
      title: "How does the robot know when it's done?",
      subtitle: "Commands, the four lifecycle methods, composition with SequentialCommandGroup, and the AutoChooser pattern.",
      description: "Commands, the four lifecycle methods, composition with SequentialCommandGroup, and the AutoChooser pattern.",
      hardware: "XRP robot",
      duration: "~2-3 hours",
      filename: "lesson-06-autonomous.html",
      prev: "05",
      next: "07"
    },
    "07": {
      module: 1,
      lesson: "07",
      title: "Why doesn't it stop where I told it to?",
      subtitle: "Encoders, gyro, P-control tuning. Continued work on competition program.",
      description: "Encoders, gyro, P-control tuning. Continued work on competition program.",
      hardware: "XRP robot",
      duration: "~2-3 hours",
      filename: "lesson-07-sensors.html",
      prev: "06",
      next: null
    }
  }
};