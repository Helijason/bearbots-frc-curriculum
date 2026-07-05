// Copyright (c) 2025 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.commands;

import edu.wpi.first.wpilibj2.command.SequentialCommandGroup;
import frc.robot.subsystems.drive.Drive;

public class AutonomousDistance extends SequentialCommandGroup {
  /**
   * Creates a new Autonomous Drive based on distance. This will drive out for a specified distance,
   * turn around and drive back.
   *
   * @param drivetrain The drivetrain subsystem on which this command will run
   */
  public AutonomousDistance(Drive drivetrain) {
    addCommands(
        new DriveDistance(0.6, 0.254, drivetrain),
        new TurnDegrees(0.6, 180, drivetrain),
        new DriveDistance(0.6, 0.254, drivetrain),
        new TurnDegrees(0.6, 180, drivetrain));
  }
}
