// Copyright (c) 2025 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.subsystems.drive;
 
import org.littletonrobotics.junction.AutoLog;
 
public interface DriveIO {
  @AutoLog
  public static class DriveIOInputs {
    public int leftEncoderCount = 0;
    public int rightEncoderCount = 0;
 
    public double leftPositionMeters = 0.0;
    public double rightPositionMeters = 0.0;
 
    public double leftVelocityMetersPerSec = 0.0;
    public double rightVelocityMetersPerSec = 0.0;
 
    public double leftAppliedVolts = 0.0;
    public double rightAppliedVolts = 0.0;
 
    public double accelX = 0.0;
    public double accelY = 0.0;
    public double accelZ = 0.0;
 
    public double gyroAngleXDeg = 0.0;
    public double gyroAngleYDeg = 0.0;
    public double gyroAngleZDeg = 0.0;
  }
 
  public default void updateInputs(DriveIOInputs inputs) {}
 
  public default void setVoltage(double leftVolts, double rightVolts) {}
 
  public default void resetEncoders() {}
 
  public default void resetGyro() {}
 
  public default void stop() {
    setVoltage(0.0, 0.0);
  }
}