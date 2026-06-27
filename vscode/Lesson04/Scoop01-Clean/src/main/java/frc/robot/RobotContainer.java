// Copyright (c) 2025 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot;
 
import static frc.robot.Constants.OperatorConstants.*;
 
import edu.wpi.first.wpilibj.XboxController;
import edu.wpi.first.wpilibj.xrp.XRPOnBoardIO;
import org.littletonrobotics.junction.networktables.LoggedDashboardChooser;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.Commands;
import edu.wpi.first.wpilibj2.command.PrintCommand;
import edu.wpi.first.wpilibj2.command.button.JoystickButton;
import edu.wpi.first.wpilibj2.command.button.POVButton;
import edu.wpi.first.wpilibj2.command.button.Trigger;
import frc.robot.commands.ArcadeDrive;
import frc.robot.commands.AutonomousDriveStraight;
import frc.robot.commands.AutonomousSpin;
import frc.robot.commands.AutonomousPattern;
import frc.robot.subsystems.arm.Arm;
import frc.robot.subsystems.arm.ArmConstants;
import frc.robot.subsystems.arm.ArmIO;
import frc.robot.subsystems.arm.ArmIOXRP;
import frc.robot.subsystems.arm.ArmIOSim;
import frc.robot.subsystems.drive.Drive;
import frc.robot.subsystems.drive.DriveIO;
import frc.robot.subsystems.drive.DriveIOSim;
import frc.robot.subsystems.drive.DriveIOXRP;
import frc.robot.subsystems.scoop.Scoop;
 
/**
 * This class is where the bulk of the robot should be declared. Since Command-based is a
 * "declarative" paradigm, very little robot logic should actually be handled in the {@link Robot}
 * periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
 * subsystems, commands, and button mappings) should be declared here.
 */
public class RobotContainer {
 
  // Subsystems
  private final Drive drive;
  private final Arm arm;
  private final Scoop scoop;
  private final XRPOnBoardIO onboardIO = new XRPOnBoardIO();
 
  // Controller
  private final XboxController controller = new XboxController(kDriverControllerPort);
 
  // Autonomous chooser
private final LoggedDashboardChooser<Command> autonomousChooser = new LoggedDashboardChooser<>("Auto Choices");
 
  /** The container for the robot. Contains subsystems, OI devices, and commands. */
  public RobotContainer() {
    // Change instantiation process based on current mode.
    switch (Constants.currentMode) {
      case REAL: // Real hardware
        drive = new Drive(new DriveIOXRP());
        arm = new Arm(new ArmIOXRP());
        break;
      case SIM: // Simulated code
        drive = new Drive(new DriveIOSim());
        arm = new Arm(new ArmIOSim());
        break;
      default: // Log replay
        drive = new Drive(new DriveIO() {});
        arm = new Arm(new ArmIO() {});
        break;
    }
    scoop = new Scoop();
    
    configureButtonBindings();
    configureAutonomous();
  }
 
  private void configureButtonBindings() {
    // Default command: arcade drive with left stick.
    // Axis 1 (left stick Y) is negated — joystick forward = negative value.
    drive.setDefaultCommand(
        new ArcadeDrive(
            drive,
            () -> -controller.getRawAxis(kForwardAxis),
            () -> -controller.getRawAxis(kRotationAxis)));
 
    // Onboard user button — prints to console.
    Trigger userButton = new Trigger(onboardIO::getUserButtonPressed);
    userButton
        .onTrue(new PrintCommand("USER Button Pressed"))
        .onFalse(new PrintCommand("USER Button Released"));
 
    // A button — arm low position.
    new JoystickButton(controller, XboxController.Button.kA.value)
        .onTrue(Commands.runOnce(() -> arm.setAngle(ArmConstants.kLowAngleDeg), arm))
        .onFalse(Commands.runOnce(() -> arm.stop(), arm));
        
    // B button — arm high position, stow on release.
    new JoystickButton(controller, XboxController.Button.kB.value)
        .onTrue(Commands.runOnce(() -> arm.setAngle(ArmConstants.kHighAngleDeg), arm))
        .onFalse(Commands.runOnce(() -> arm.stop(), arm));
    
    // add this - D-pad controls the scoop
    new POVButton(controller, 90)  // 6
        .onTrue(scoop.setGoalCommand(Scoop.Goal.FLAT));
    new POVButton(controller, 0)   // 8
        .onTrue(scoop.setGoalCommand(Scoop.Goal.CARRY));
    new POVButton(controller, 180) // 2
        .onTrue(scoop.setGoalCommand(Scoop.Goal.DUMP));

  }
 
  private void configureAutonomous() {
    autonomousChooser.addDefaultOption("Pattern 1", new AutonomousDriveStraight(drive));
    autonomousChooser.addOption("Pattern 2", new AutonomousSpin(drive));
    autonomousChooser.addOption("Pattern 3", new AutonomousPattern(drive));
  }
 
  /**
   * Returns the autonomous command selected in SmartDashboard.
   *
   * @return the selected autonomous command
   */
  public Command getAutonomousCommand() {
    return autonomousChooser.get();
  }

  public frc.robot.subsystems.arm.Arm getArm() {
    return arm;
  }

  public frc.robot.subsystems.scoop.Scoop getScoop() {
    return scoop;
  }
}