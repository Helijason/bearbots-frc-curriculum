// Copyright (c) 2026 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.subsystems.elevator;

public class ElevatorConstants {

    private ElevatorConstants() {}                        // prevent instantiation

    /* ********************************************************************* */
    /* *** XRP CONFIGURATION CONSTANTS                                       */

    /** encoder counts per motor revolution */
    public static final double kCountsPerMotorShaftRev = 12.0;

    /** Motor revolutions per output revolution. Set to your gearbox. */
    public static final double kGearRatio = 48.75;

    public static final double kCountsPerOutputRev =
        kCountsPerMotorShaftRev * kGearRatio;

    /** Spool/pulley diameter the cable wraps around. */
    public static final double kSpoolDiameterMeters = 0.020;

    public static final double kOutputDistancePerRev =
        Math.PI * kSpoolDiameterMeters;

    public static final double kEncoderDistancePerPulseMeters =
        kOutputDistancePerRev / kCountsPerOutputRev;
    
    /* ********************************************************************* */
    /* *** CONTROL CONSTANTS                                                 */

    /** Proportional gain: volts per meter of position error. */
    public static final double kPReal = 40.0;
    public static final double kPSim = 25.0;

    
    /* ********************************************************************* */
    /* *** POSITIONAL CONSTANTS                                              */

    /** Elevator Bottom height in meters. */
    public static final double kBottomHeightMeters  = 0.003;

    /** Elevator Middle height in meters. */
    public static final double kMiddleHeightMeters  = 0.064;

    /** Elevator Top height in meters. */
    public static final double kTopHeightMeters  = 0.127;

    /** Minimum allowed Height in meters. */
    public static final double kMinHeightMeters   = 0.0;

    /** Maximum allowed Height in meters. */
    public static final double kMaxHeightMeters   = 0.135;

    /** Height tolerance in meters. */
    public static final double kHeightToleranceMeters   = 0.005;

    /* ********************************************************************* */
    /* *** SIMULATOR CONSTANTS                                               */
    /** Output speed at full voltage. Measure or estimate from motor free speed + gearing. */
    public static final double kSimMaxSpeedMetersPerSec = 0.15;

    /** Voltage needed just to hold the carriage against gravity (kG feedforward). */
    public static final double kGravityVolts = 0.5;
}