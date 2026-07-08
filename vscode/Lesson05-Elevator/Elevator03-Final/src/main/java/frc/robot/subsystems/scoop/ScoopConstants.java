// Copyright (c) 2026 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.subsystems.scoop;

public final class ScoopConstants {
  private ScoopConstants() {}

  // Named setpoints. Bind these directly:
  //   button.onTrue(xxx.setAngleDegCommand(ScoopConstants.kFlatAngleDeg));
  public static final double kFlatAngleDeg = 45.0;
  public static final double kCarryAngleDeg = 90.0;
  public static final double kDumpAngleDeg = 0.0;

  // Startup target. periodic drives here until told otherwise.
  public static final double kDefaultAngleDeg = kFlatAngleDeg;

  // Travel limits. setAngle clamps to this band.
  public static final double kMinAngleDeg = 0.0;
  public static final double kMaxAngleDeg = 90.0;

  // Stepped-move finish window.
  public static final double kAngleToleranceDeg = 0.5;
}