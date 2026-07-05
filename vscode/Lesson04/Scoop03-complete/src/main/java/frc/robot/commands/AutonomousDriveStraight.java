// Copyright (c) 2025 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.commands;

import edu.wpi.first.wpilibj2.command.SequentialCommandGroup;
import frc.robot.AutonomousConstants.DriveStraightConstants;
import frc.robot.subsystems.drive.Drive;

public class AutonomousDriveStraight extends SequentialCommandGroup {
  /**
   * Creates a new Autonomous Drive Straight. Drives forward a fixed distance, then stops.
   * No turning.
   *
   * @param drive The drive subsystem on which this command will run
   */
  public AutonomousDriveStraight(Drive drive) {
    addCommands(
        new DriveDistance(
            DriveStraightConstants.kSpeed, DriveStraightConstants.kDistanceMeters, drive));
  }
}