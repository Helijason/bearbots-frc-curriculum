// Copyright (c) 2025 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.subsystems.drive;

import static frc.robot.Constants.kMaxBatteryVoltage;

import edu.wpi.first.math.MathUtil;
import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.geometry.Rotation2d;
import edu.wpi.first.math.kinematics.DifferentialDriveOdometry;
import edu.wpi.first.wpilibj2.command.SubsystemBase;
import org.littletonrobotics.junction.Logger;

public class Drive extends SubsystemBase {
  private final DriveIO io;
  private final DriveIOInputsAutoLogged inputs = new DriveIOInputsAutoLogged();

  private final DifferentialDriveOdometry odometry = 
      new DifferentialDriveOdometry(new Rotation2d(), 0.0, 0.0,
          new Pose2d(0.5, 0.5, new Rotation2d()));

  /** Creates a new Drive subsystem. */
  public Drive(DriveIO io) {
    this.io = io;
  }

  @Override
  public void periodic() {
    io.updateInputs(inputs);
    Logger.processInputs("Drive", inputs);

    // Update odometry with latest gyro heading and wheel positions.
    odometry.update(
        Rotation2d.fromDegrees(-inputs.gyroAngleZDeg),
        inputs.leftPositionMeters,
        inputs.rightPositionMeters);

    Logger.recordOutput("Drive/Pose", odometry.getPoseMeters());
  }

  /**
   * Drives the robot using arcade controls.
   *
   * @param xaxisSpeed  Forward/backward speed as a percent [-1.0, 1.0]. Positive
   *                    = forward.
   * @param zaxisRotate Rotation speed as a percent [-1.0, 1.0]. Positive = left.
   */
  public void arcadeDrive(double xaxisSpeed, double zaxisRotate) {
    // Clamp inputs to valid range.
    // Clamping ensures any value above or below some certain number gets "clamped"
    // to that number, so it stays within some range.
    xaxisSpeed = MathUtil.clamp(xaxisSpeed, -1.0, 1.0);
    zaxisRotate = MathUtil.clamp(zaxisRotate, -1.0, 1.0);

    // Arcade IK: convert forward/rotation percent to left/right percent.
    double leftPercent = xaxisSpeed + zaxisRotate;
    double rightPercent = xaxisSpeed - zaxisRotate;

    // Scale to volts and send to IO layer.
    io.setVoltage(leftPercent * kMaxBatteryVoltage, rightPercent * kMaxBatteryVoltage);

    Logger.recordOutput("Drive/Commanded/XAxisSpeed", 0.0);
    Logger.recordOutput("Drive/Commanded/ZAxisRotate", 0.0);
  }

  /** Stops the drive motors. */
  public void stop() {
    io.stop();

    Logger.recordOutput("Drive/Commanded/XAxisSpeed", 0.0);
    Logger.recordOutput("Drive/Commanded/ZAxisRotate", 0.0);
  }

  /** Resets both drive encoders to zero. */
  public void resetEncoders() {
    io.resetEncoders();
  }

  /**
   * Resets encoders and re-seeds odometry at the current pose.
   * Use this between autonomous legs so odometry stays continuous.
   */
  public void resetEncodersKeepPose() {
    Pose2d currentPose = odometry.getPoseMeters();
    io.resetEncoders();
    odometry.resetPosition(
        Rotation2d.fromDegrees(-inputs.gyroAngleZDeg),
        0.0,
        0.0,
        currentPose);
  }

  /** Returns the current estimated pose of the robot. */
  public Pose2d getPose() {
    return odometry.getPoseMeters();
  }

  /**
   * Resets odometry to the given pose.
   *
   * @param pose The pose to reset to
   */
  public void resetOdometry(Pose2d pose) {
    io.resetEncoders();
    odometry.resetPosition(
        Rotation2d.fromDegrees(-inputs.gyroAngleZDeg),
        0.0,
        0.0,
        pose);
  }

  /** Returns the left encoder count in raw pulses. */
  public int getLeftEncoderCount() {
    return inputs.leftEncoderCount;
  }

  /** Returns the right encoder count in raw pulses. */
  public int getRightEncoderCount() {
    return inputs.rightEncoderCount;
  }

  /** Returns the left wheel position in meters. */
  public double getLeftPositionMeters() {
    return inputs.leftPositionMeters;
  }

  /** Returns the right wheel position in meters. */
  public double getRightPositionMeters() {
    return inputs.rightPositionMeters;
  }

  /** Returns the average of left and right wheel positions in meters. */
  public double getAveragePositionMeters() {
    return (inputs.leftPositionMeters + inputs.rightPositionMeters) / 2.0;
  }

  /** Returns X-axis acceleration in Gs. */
  public double getAccelX() {
    return inputs.accelX;
  }

  /** Returns Y-axis acceleration in Gs. */
  public double getAccelY() {
    return inputs.accelY;
  }

  /** Returns Z-axis acceleration in Gs. */
  public double getAccelZ() {
    return inputs.accelZ;
  }

  /** Returns the gyro angle around the X axis in degrees. */
  public double getGyroAngleX() {
    return inputs.gyroAngleXDeg;
  }

  /** Returns the gyro angle around the Y axis in degrees. */
  public double getGyroAngleY() {
    return inputs.gyroAngleYDeg;
  }

  /** Returns the gyro angle around the Z axis in degrees (heading). */
  public double getGyroAngleZ() {
    return inputs.gyroAngleZDeg;
  }

  /** Resets the gyro to zero. */
  public void resetGyro() {
    io.resetGyro();
  }
}