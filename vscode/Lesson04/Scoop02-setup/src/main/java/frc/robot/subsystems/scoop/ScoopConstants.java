// Copyright (c) 2025 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.
 
package frc.robot.subsystems.scoop;

public final class ScoopConstants {
    private ScoopConstants() {}                               // prevent instantiation

    /** Servo angle for resting/flat position in degrees. */
    public static final double kFlatAngleDeg  = 0.0;

    /** Servo angle for carrying a game piece in degrees. */
    public static final double kCarryAngleDeg = 45.0;

    /** Servo angle for dumping a game piece in degrees. */
    public static final double kDumpAngleDeg  = 90.0;

    /** Minimum allowed servo angle in degrees. */
    public static final double kMinAngleDeg   = 0.0;

    /** Maximum allowed servo angle in degrees. */
    public static final double kMaxAngleDeg   = 90.0;
}
