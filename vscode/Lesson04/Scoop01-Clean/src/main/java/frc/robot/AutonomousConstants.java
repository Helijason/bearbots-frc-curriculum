// Copyright (c) 2025 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot;

/**
 * Tunable values for the Lesson 02 autonomous modes. Change values here, not in the
 * command files.
 */
public final class AutonomousConstants {

  /** Pattern 1 — Drive Straight (fixed distance, no turn). */
  public static final class DriveStraightConstants {
    public static final double kSpeed = 0.6;
    public static final double kDistanceMeters = 0.5;

    private DriveStraightConstants() {}
  }

  /** Pattern 2 — Spin In Place (single point turn). */
  public static final class SpinConstants {
    public static final double kSpeed = 0.6;
    public static final double kDegrees = 360.0;

    private SpinConstants() {}
  }

  /** Pattern 3 — Drive + Turn Mystery Pattern (out, turn, out, turn back). */
  public static final class MysteryPatternConstants {
    public static final double kDriveSpeed = 0.6;
    public static final double kTurnSpeed = 0.5;

    // Drive legs (meters)
    public static final double kLegMeters1 = 0.5;
    public static final double kLegMeters2 = 0.5;
    public static final double kLegMeters3 = 0.5;
    public static final double kLegMeters4 = 0.5;
 
    // Turns (degrees)
    public static final double kTurnDegrees1 = 90.0;
    public static final double kTurnDegrees2 = 90.0;
    public static final double kTurnDegrees3 = 90.0;
    public static final double kTurnDegrees4 = 90.0;

    private MysteryPatternConstants() {}
  }

  private AutonomousConstants() {}
}