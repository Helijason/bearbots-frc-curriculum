// Copyright (c) 2025 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.commands;

import edu.wpi.first.wpilibj2.command.SequentialCommandGroup;
import frc.robot.AutonomousConstants.SpinConstants;
import frc.robot.subsystems.drive.Drive;

public class AutonomousSpin extends SequentialCommandGroup {
  /**
   * Creates a new Autonomous Spin. Rotates the robot in place a fixed number of degrees,
   * then stops. No forward motion.
   *
   * @param drive The drive subsystem on which this command will run
   */
  public AutonomousSpin(Drive drive) {
    addCommands(new TurnDegrees(SpinConstants.kSpeed, SpinConstants.kDegrees, drive));
  }
}