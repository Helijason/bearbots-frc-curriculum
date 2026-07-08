// Copyright (c) 2026 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.subsystems.elevator;

public final class ElevatorConstants {
  private ElevatorConstants() {}

  // Gearbox + encoder conversion. Measure from your mechanism, or read the datasheet.
  public static final double kCountsPerMotorShaftRev = 12.0;
  public static final double kGearRatio = 48.75;
  public static final double kCountsPerOutputRev = kCountsPerMotorShaftRev * kGearRatio;
  public static final double kSpoolDiameterMeters = 0.020;
  public static final double kOutputDistancePerRev = Math.PI * kSpoolDiameterMeters;
  public static final double kEncoderDistancePerPulseMeters = kOutputDistancePerRev / kCountsPerOutputRev;

  // Homing. Gentle voltage toward the hard stop; stall detected once movement starts.
  public static final double kHomingVolts = -1.0;
  public static final double kHomingStallMetersPerSec = 0.002;
  public static final double kHomingMovingMetersPerSec = 0.010;
  public static final double kHomingTimeoutSecs = 3.0;

  // Real robot PID + feedforward. Tune live via LoggedNetworkNumber, then bake in here.
  public static final double kPReal = 40.0;
  public static final double kIReal = 0.0;
  public static final double kDReal = 0.0;
  public static final double kSVoltsReal = 0.0;
  public static final double kGVoltsReal = 0.0;
  public static final double kVVoltSecPerMeterReal = 0.0;

  // Sim PID + feedforward. Usually needs different gains than the real robot.
  public static final double kPSim = 25.0;
  public static final double kISim = 0.0;
  public static final double kDSim = 0.0;
  public static final double kSVoltsSim = 0.0;
  public static final double kGVoltsSim = 0.0;
  public static final double kVVoltSecPerMeterSim = 0.0;

  // Named setpoints. Bind these directly:
  //   button.onTrue(xxx.setHeightMetersCommand(ElevatorConstants.kBottomHeightMeters));
  public static final double kBottomHeightMeters = 0.003;
  public static final double kTopHeightMeters = 0.127;
  public static final double kMiddleHeightMeters = 0.064;  // add more named setpoints here, one per line

  // Startup target. periodic drives here until told otherwise.
  public static final double kDefaultHeightMeters = kBottomHeightMeters;

  // Travel limits. setHeightMeters clamps to this band.
  public static final double kMinHeightMeters = 0.0;
  public static final double kMaxHeightMeters = 0.135;

  // PID finish window.
  public static final double kHeightToleranceMeters = 0.005;

  // Sim-only. Output speed at full voltage - measure or estimate from motor free speed + gearing.
  public static final double kSimMaxSpeedMetersPerSec = 0.15;

  // Sim-only. Voltage needed just to hold position against gravity (kG feedforward starting point).
  public static final double kGravityVolts = 0.5;
}
