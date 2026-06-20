package frc.robot.subsystems.drive;
 
import static frc.robot.Constants.kMaxBatteryVoltage;
 
public class DriveIOSim implements DriveIO {
  private double leftAppliedVolts = 0.0;
  private double rightAppliedVolts = 0.0;
 
  private double leftPositionMeters = 0.0;
  private double rightPositionMeters = 0.0;
 
  private double leftVelocityMetersPerSec = 0.0;
  private double rightVelocityMetersPerSec = 0.0;
 
  private double gyroAngleZDeg = 0.0;
 
  @Override
  public void updateInputs(DriveIOInputs inputs) {
    // Linear velocity model: voltage / maxVoltage * maxSpeed
    leftVelocityMetersPerSec =
        (leftAppliedVolts / kMaxBatteryVoltage)
            * DriveConstants.kSimMaxWheelSpeedMetersPerSec;
    rightVelocityMetersPerSec =
        (rightAppliedVolts / kMaxBatteryVoltage)
            * DriveConstants.kSimMaxWheelSpeedMetersPerSec;
 
    // Integrate velocity → position each loop tick.
    leftPositionMeters += leftVelocityMetersPerSec * DriveConstants.kLoopPeriodSecs;
    rightPositionMeters += rightVelocityMetersPerSec * DriveConstants.kLoopPeriodSecs;
 
    // Derive yaw from differential wheel speeds and track width.
    double angularVelocityRadPerSec =
        (rightVelocityMetersPerSec - leftVelocityMetersPerSec)
            / DriveConstants.kTrackWidthMeters;
    gyroAngleZDeg += Math.toDegrees(angularVelocityRadPerSec) * DriveConstants.kLoopPeriodSecs;
 
    // Populate inputs.
    inputs.leftAppliedVolts = leftAppliedVolts;
    inputs.rightAppliedVolts = rightAppliedVolts;
 
    inputs.leftPositionMeters = leftPositionMeters;
    inputs.rightPositionMeters = rightPositionMeters;
 
    // Derive encoder counts from position.
    inputs.leftEncoderCount =
        (int) (leftPositionMeters / DriveConstants.kEncoderDistancePerPulseMeters);
    inputs.rightEncoderCount =
        (int) (rightPositionMeters / DriveConstants.kEncoderDistancePerPulseMeters);

    inputs.leftVelocityMetersPerSec = leftVelocityMetersPerSec;
    inputs.rightVelocityMetersPerSec = rightVelocityMetersPerSec;
 
    // Sim has no accelerometer — leave accel fields at default (0.0).
 
    // Only Z (yaw) is meaningful in a 2D ground robot sim.
    inputs.gyroAngleZDeg = gyroAngleZDeg;
  }
 
  @Override
  public void setVoltage(double leftVolts, double rightVolts) {
    leftAppliedVolts = leftVolts;
    rightAppliedVolts = rightVolts;
  }
 
  @Override
  public void resetEncoders() {
    leftPositionMeters = 0.0;
    rightPositionMeters = 0.0;
  }
 
  @Override
  public void resetGyro() {
    gyroAngleZDeg = 0.0;
  }
 
  @Override
  public void stop() {
    setVoltage(0.0, 0.0);
  }
}