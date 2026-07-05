// Copyright (c) 2025 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.subsystems.arm;

public final class ArmConstants {
  private ArmConstants() {
    // Prevent instantiation.
  }

  /** Minimum allowed servo angle in degrees. */
  public static final double kMinAngleDeg = 0.0;

  /** Maximum allowed servo angle in degrees. */
  public static final double kMaxAngleDeg = 180.0;

  /** Safe/stowed arm position in degrees. */
  public static final double kStowedAngleDeg = 180.0;

  /** Example low arm position in degrees. */
  public static final double kLowAngleDeg = 135.0;

  /** Example high arm position in degrees. */
  public static final double kHighAngleDeg = 90.0;
}