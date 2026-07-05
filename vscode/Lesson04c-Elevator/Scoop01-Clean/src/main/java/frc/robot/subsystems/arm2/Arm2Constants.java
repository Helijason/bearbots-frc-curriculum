// Copyright (c) 2026 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.subsystems.arm2;

public final class Arm2Constants {
  private Arm2Constants() {}

  // Named setpoints. Bind these directly:
  //   button.onTrue(xxx.setAngleCommand(Arm2Constants.kStowedAngleDeg));
  public static final double kStowedAngleDeg = 0.0;
  public static final double kRaisedAngleDeg = 90.0;

  // Startup target. periodic drives here until told otherwise.
  public static final double kDefaultAngleDeg = kStowedAngleDeg;

  // Travel limits. setAngle clamps to this band.
  public static final double kMinAngleDeg = 0.0;
  public static final double kMaxAngleDeg = 90.0;

  // Stepped-move finish window.
  public static final double kAngleToleranceDeg = 0.5;
}