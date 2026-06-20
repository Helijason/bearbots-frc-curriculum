package frc.robot.subsystems.drive;
 
public final class DriveConstants {
  private DriveConstants() {
    // Prevent instantiation.
  }
 
  // --- Hardware constants ---
 
  public static final double kGearRatio =
      (30.0 / 14.0) * (28.0 / 16.0) * (36.0 / 9.0) * (26.0 / 8.0); // 48.75:1
 
  public static final double kCountsPerMotorShaftRev = 12.0;
 
  public static final double kCountsPerWheelRevolution =
      kCountsPerMotorShaftRev * kGearRatio;
 
  public static final double kWheelDiameterMeters = 0.060;
 
  public static final double kWheelRadiusMeters = kWheelDiameterMeters / 2.0;
 
  public static final double kWheelCircumferenceMeters = Math.PI * kWheelDiameterMeters;
 
  public static final double kEncoderDistancePerPulseMeters =
      kWheelCircumferenceMeters / kCountsPerWheelRevolution;
 
  /** Distance between left and right wheels (track width). */
  public static final double kTrackWidthMeters = 0.155;
 
  public static final double kTurnMetersPerDegree =
      (Math.PI * kTrackWidthMeters) / 360.0;
 
  // --- Simulation constants ---
 
  /** WPILib command scheduler loop period in seconds. */
  public static final double kLoopPeriodSecs = 0.020;
 
  /**
   * XRP no-load wheel speed at 4.5V (90 RPM output).
   * Used in sim to scale voltage → velocity linearly.
   * Calculated: 2 * pi * kWheelRadiusMeters * 90 / 60 = ~0.283 m/s
   */
  public static final double kSimMaxWheelSpeedMetersPerSec =
      2.0 * Math.PI * kWheelRadiusMeters * 90.0 / 60.0;
}