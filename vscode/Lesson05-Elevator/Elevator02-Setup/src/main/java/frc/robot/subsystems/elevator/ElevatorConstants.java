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

    public static final double kHomingVolts = -1.0;              // gentle, toward bottom
    public static final double kHomingStallMetersPerSec = 0.002; // "stopped" threshold
    public static final double kHomingMovingMetersPerSec = 0.010; // "clearly moving" threshold
    public static final double kHomingTimeoutSecs = 3.0;
    
    /* ********************************************************************* */
    /* *** CONTROL CONSTANTS                                                 */

    /** Real Proportional gain: volts per meter of position error. */
    public static final double kPReal = 40.0;
    public static final double kIReal = 0.0;
    public static final double kDReal = 0.0;
    /** Real Feedforward, start at 0 and tune up. */
    public static final double kSVoltsReal = 0.0;            // static friction
    public static final double kGVoltsReal = 0.0;            // gravity hold
    public static final double kVVoltSecPerMeterReal = 0.0;  // velocity

    /** SIM Proportional gain: volts per meter of position error. */
    public static final double kPSim = 25.0;
    public static final double kISim = 0.0;
    public static final double kDSim = 0.0;
    /** SIM Feedforward, start at 0 and tune up. */
    public static final double kSVoltsSim = 0.0;            // static friction
    public static final double kGVoltsSim = 0.0;            // gravity hold
    public static final double kVVoltSecPerMeterSim = 0.0;  // velocity
    
    
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

    /** Default/startup height in meters. */
    public static final double kDefaultHeightMeters = kBottomHeightMeters;

    /** Height tolerance in meters. */
    public static final double kHeightToleranceMeters   = 0.005;

    /* ********************************************************************* */
    /* *** SIMULATOR CONSTANTS                                               */
    /** Output speed at full voltage. Measure or estimate from motor free speed + gearing. */
    public static final double kSimMaxSpeedMetersPerSec = 0.15;

    /** Voltage needed just to hold the carriage against gravity (kG feedforward). */
    public static final double kGravityVolts = 0.5;
}