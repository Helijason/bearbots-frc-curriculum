// Copyright (c) 2025 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot;
/**
 * The Constants class provides a convenient place for teams to hold robot-wide numerical or boolean
 * constants. This class should not be used for any other purpose. All constants should be declared
 * globally (i.e. public static). Do not put anything functional in this class.
 *
 * <p>It is advised to statically import this class (or one of its inner classes) wherever the
 * constants are needed, to reduce verbosity.
 */
public final class Constants {
  private Constants() {
    // Prevent instantiation.
  }
 
  /**
   * Selects which IO implementations are used at runtime.
   *
   * <p>REAL: running on physical XRP hardware.
   * <p>SIM: running in the WPILib simulator (no hardware).
   * <p>REPLAY: replaying a previously recorded AdvantageKit log.
   *
   * <p>Change this to REAL before deploying to the XRP.
   * Change to SIM to run the simulator on your laptop.
   */
  public enum Mode { REAL, SIM, REPLAY }
  public static final Mode currentMode = Mode.SIM;          // SIM = live XRP; set REPLAY to replay a log
  //public static final Mode simMode = Mode.REAL;          // SIM = live XRP; set REPLAY to replay a log
  //public static final Mode currentMode = RobotBase.isReal() ? Mode.REAL : simMode;
 
  /**
   * Nominal battery voltage for the XRP robot (4x AA alkaline batteries).
   * Used to normalize voltage commands to the [-1.0, 1.0] range expected by
   * XRPMotor. Any subsystem that converts volts to motor percent output should
   * use this constant rather than a magic number.
   */
  public static final double kMaxBatteryVoltage = 4.5;
 
  public static final class OperatorConstants {
    private OperatorConstants() {}
 
    public static final int kDriverControllerPort = 0;
 
    /** Xbox controller axis for forward/backward (left stick Y). */
    public static final int kForwardAxis = 1;
 
    /** Xbox controller axis for rotation (left stick X). */
    public static final int kRotationAxis = 0;
  }
 
  public static final class DriveHardware {
    private DriveHardware() {}
 
    /** XRP left drive motor PWM channel. */
    public static final int kLeftMotorChannel = 1;
 
    /** XRP right drive motor PWM channel. */
    public static final int kRightMotorChannel = 0;
 
    /** XRP left encoder DIO channel A. */
    public static final int kLeftEncoderChannelA = 4;
 
    /** XRP left encoder DIO channel B. */
    public static final int kLeftEncoderChannelB = 5;
 
    /** XRP right encoder DIO channel A. */
    public static final int kRightEncoderChannelA = 6;
 
    /** XRP right encoder DIO channel B. */
    public static final int kRightEncoderChannelB = 7;
  }
 
  public static final class ArmHardware {
    private ArmHardware() {}
 
    /** XRP servo device number. Device 4 maps to physical Servo 1 on the XRP. */
    public static final int kArmServoDeviceNumber = 4;
  }
}