// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot.commands;
 
import edu.wpi.first.wpilibj2.command.RunCommand;
import edu.wpi.first.wpilibj2.command.SequentialCommandGroup;
import frc.robot.subsystems.drive.Drive;
 
public class AutonomousTime extends SequentialCommandGroup {
  /**
   * Creates a new Autonomous Drive based on time. Drives forward, turns around,
   * drives forward again, then turns back — mimicking an out-and-back routine.
   *
   * @param drive The drive subsystem on which this command will run
   */
  public AutonomousTime(Drive drive) {
    addCommands(
        new RunCommand(() -> drive.arcadeDrive(0.6, 0.0), drive).withTimeout(2.0),
        new RunCommand(() -> drive.arcadeDrive(0.0, 0.5), drive).withTimeout(1.3),
        new RunCommand(() -> drive.arcadeDrive(0.6, 0.0), drive).withTimeout(2.0),
        new RunCommand(() -> drive.arcadeDrive(0.0, -0.5), drive).withTimeout(1.3));
  }
}
