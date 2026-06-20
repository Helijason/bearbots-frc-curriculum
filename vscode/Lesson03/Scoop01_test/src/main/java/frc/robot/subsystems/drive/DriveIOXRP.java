package frc.robot.subsystems.drive;

import static frc.robot.Constants.DriveHardware.*;

import edu.wpi.first.util.sendable.SendableRegistry;
import edu.wpi.first.wpilibj.BuiltInAccelerometer;
import edu.wpi.first.wpilibj.Encoder;
import edu.wpi.first.wpilibj.drive.DifferentialDrive;
import static frc.robot.Constants.kMaxBatteryVoltage;
import edu.wpi.first.wpilibj.xrp.XRPGyro;
import edu.wpi.first.wpilibj.xrp.XRPMotor;

public class DriveIOXRP implements DriveIO {
  // The XRP has the left and right motors set to channels 0 and 1 respectively.
  private final XRPMotor m_leftMotor = new XRPMotor(kLeftMotorChannel);
  private final XRPMotor m_rightMotor = new XRPMotor(kRightMotorChannel);

  // The XRP has onboard encoders.
  private final Encoder m_leftEncoder =
    new Encoder(kLeftEncoderChannelA, kLeftEncoderChannelB);
  private final Encoder m_rightEncoder =
    new Encoder(kRightEncoderChannelA, kRightEncoderChannelB);

  private final DifferentialDrive m_diffDrive =
      new DifferentialDrive(m_leftMotor::set, m_rightMotor::set);

  private final XRPGyro m_gyro = new XRPGyro();
  private final BuiltInAccelerometer m_accelerometer = new BuiltInAccelerometer();

  public DriveIOXRP() {
    SendableRegistry.addChild(m_diffDrive, m_leftMotor);
    SendableRegistry.addChild(m_diffDrive, m_rightMotor);

    // Invert one side so positive commands move both sides forward.
    m_rightMotor.setInverted(true);

    // Calculate distance per pulse
    m_leftEncoder.setDistancePerPulse(DriveConstants.kEncoderDistancePerPulseMeters);
    m_rightEncoder.setDistancePerPulse(DriveConstants.kEncoderDistancePerPulseMeters);

    resetEncoders();
  }

  @Override
  public void updateInputs(DriveIOInputs inputs) {
    inputs.leftEncoderCount = m_leftEncoder.get();
    inputs.rightEncoderCount = m_rightEncoder.get();

    inputs.leftPositionMeters = m_leftEncoder.getDistance();
    inputs.rightPositionMeters = m_rightEncoder.getDistance();

    inputs.leftVelocityMetersPerSec = m_leftEncoder.getRate() * 0.0254;
    inputs.rightVelocityMetersPerSec = m_rightEncoder.getRate() * 0.0254;

    inputs.accelX = m_accelerometer.getX();
    inputs.accelY = m_accelerometer.getY();
    inputs.accelZ = m_accelerometer.getZ();

    inputs.gyroAngleXDeg = m_gyro.getAngleX();
    inputs.gyroAngleYDeg = m_gyro.getAngleY();
    inputs.gyroAngleZDeg = m_gyro.getAngleZ();
  }

  @Override
  public void setVoltage(double leftVolts, double rightVolts) {
    // Convert volts to percent output [-1.0, 1.0] for DifferentialDrive.
    m_diffDrive.tankDrive(-leftVolts / kMaxBatteryVoltage, -rightVolts / kMaxBatteryVoltage);
  }

  @Override
  public void resetEncoders() {
    m_leftEncoder.reset();
    m_rightEncoder.reset();
  }

  @Override
  public void resetGyro() {
    m_gyro.reset();
  }

  @Override
  public void stop() {
    m_diffDrive.stopMotor();
  }
}