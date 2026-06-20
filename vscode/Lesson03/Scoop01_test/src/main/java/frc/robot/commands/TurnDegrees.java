// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot.commands;

import edu.wpi.first.wpilibj2.command.Command;
import frc.robot.subsystems.drive.Drive;
import frc.robot.subsystems.drive.DriveConstants;

public class TurnDegrees extends Command {
  private final Drive m_drive;
  private final double m_degrees;
  private final double m_speed;

  /**
   * Creates a new TurnDegrees. This command will turn your robot for a desired rotation (in
   * degrees) and rotational speed.
   *
   * @param speed The speed which the robot will drive. Negative is in reverse.
   * @param degrees Degrees to turn. Leverages encoders to compare distance.
   * @param drive The drive subsystem on which this command will run
   */
  public TurnDegrees(double speed, double degrees, Drive drive) {
    m_degrees = degrees;
    m_speed = speed;
    m_drive = drive;
    addRequirements(drive);
  }

  // Called when the command is initially scheduled.
  @Override
  public void initialize() {
    // Set motors to stop, read encoder values for starting point
    m_drive.stop();
    m_drive.resetEncoders();
  }

  // Called every time the scheduler runs while the command is scheduled.
  @Override
  public void execute() {
    m_drive.arcadeDrive(0, m_speed);
  }

  // Called once the command ends or is interrupted.
  @Override
  public void end(boolean interrupted) {
    m_drive.stop();
  }

  // Returns true when the command should end.
  @Override
  public boolean isFinished() {
    /*
     * Need to convert distance traveled to degrees.
     * The standard XRP chassis has a wheel placement diameter of 163 mm.
     * Subtracting the approximate wheel width of 8 mm gives an effective
     * turning diameter of about 155 mm, or 0.155 meters.
     *
     * For a point turn, each wheel travels along the circumference of that
     * turning circle. The distance per degree is:
     *
     *   pi * turningDiameterMeters / 360
     */
    return getAverageTurningDistanceMeters()
        >= (DriveConstants.kTurnMetersPerDegree * m_degrees);
  }

  private double getAverageTurningDistanceMeters() {
    double leftDistanceMeters = Math.abs(m_drive.getLeftPositionMeters());
    double rightDistanceMeters = Math.abs(m_drive.getRightPositionMeters());
    return (leftDistanceMeters + rightDistanceMeters) / 2.0;
  }
}
