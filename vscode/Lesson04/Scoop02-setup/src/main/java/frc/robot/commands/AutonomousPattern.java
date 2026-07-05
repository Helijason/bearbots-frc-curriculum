// Copyright (c) 2025 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.commands;

import edu.wpi.first.wpilibj2.command.SequentialCommandGroup;
import frc.robot.AutonomousConstants.MysteryPatternConstants;
import frc.robot.subsystems.drive.Drive;

public class AutonomousPattern extends SequentialCommandGroup {
  /**
   * Creates a new Autonomous Drive based on time. Drives forward, turns around,
   * drives forward again, then turns back — mimicking an out-and-back routine.
   *
   * @param drive The drive subsystem on which this command will run
   */
  public AutonomousPattern(Drive drive) {
    addCommands(
        new DriveDistance(MysteryPatternConstants.kDriveSpeed, MysteryPatternConstants.kLegMeters1, drive),
        new TurnDegrees(MysteryPatternConstants.kTurnSpeed, MysteryPatternConstants.kTurnDegrees1, drive),
        new DriveDistance(MysteryPatternConstants.kDriveSpeed, MysteryPatternConstants.kLegMeters2, drive),
        new TurnDegrees(MysteryPatternConstants.kTurnSpeed, MysteryPatternConstants.kTurnDegrees2, drive),
        new DriveDistance(MysteryPatternConstants.kDriveSpeed, MysteryPatternConstants.kLegMeters3, drive),
        new TurnDegrees(MysteryPatternConstants.kTurnSpeed, MysteryPatternConstants.kTurnDegrees3, drive),
        new DriveDistance(MysteryPatternConstants.kDriveSpeed, MysteryPatternConstants.kLegMeters4, drive),
        new TurnDegrees(MysteryPatternConstants.kTurnSpeed, MysteryPatternConstants.kTurnDegrees4, drive));
        
  }
}