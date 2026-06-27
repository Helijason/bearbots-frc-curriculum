// Copyright (c) 2025 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.commands;

import edu.wpi.first.math.MathUtil;
import edu.wpi.first.wpilibj2.command.Command;
import frc.robot.subsystems.drive.Drive;
import frc.robot.subsystems.drive.DriveConstants;

public class TurnDegrees extends Command {
  private final Drive m_drive;
  private final double m_degrees;
  private final double m_speed;
  private double m_startAngleDeg;

  /**
   * Creates a new TurnDegrees. Rotates the robot a fixed number of degrees using
   * the gyro, with speed ramping near the target to reduce overshoot.
   *
   * @param speed    The maximum turn speed [-1.0, 1.0].
   * @param degrees  Degrees to turn. Positive = left.
   * @param drive    The drive subsystem on which this command will run.
   */
  public TurnDegrees(double speed, double degrees, Drive drive) {
    m_degrees = degrees;
    m_speed = speed;
    m_drive = drive;
    addRequirements(drive);
  }

  @Override
  public void initialize() {
    m_drive.stop();
    m_startAngleDeg = m_drive.getGyroAngleZ();
  }

  @Override
  public void execute() {
    double turned = Math.abs(m_drive.getGyroAngleZ() - m_startAngleDeg);
    double remaining = m_degrees - turned;
    double rampedSpeed = m_speed
        * MathUtil.clamp(remaining / DriveConstants.kTurnRampWindowDegrees,
            DriveConstants.kTurnMinSpeed, 1.0);
    m_drive.arcadeDrive(0, rampedSpeed);
  }

  @Override
  public void end(boolean interrupted) {
    m_drive.stop();
  }

  @Override
  public boolean isFinished() {
    double turned = Math.abs(m_drive.getGyroAngleZ() - m_startAngleDeg);
    return turned >= m_degrees;
  }
}