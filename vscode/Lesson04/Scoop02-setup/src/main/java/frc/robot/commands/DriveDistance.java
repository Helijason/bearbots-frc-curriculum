// Copyright (c) 2025 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.commands;

import edu.wpi.first.math.MathUtil;
import edu.wpi.first.wpilibj2.command.Command;
import frc.robot.subsystems.drive.Drive;
import frc.robot.subsystems.drive.DriveConstants;

public class DriveDistance extends Command {
  private final Drive m_drive;
  private final double m_distanceMeters;
  private final double m_speed;
  private double m_startMeters;

  /**
   * Creates a new DriveDistance. Drives forward a fixed distance with speed ramping
   * near the target to reduce overshoot.
   *
   * @param speed   The maximum speed [-1.0, 1.0]. Positive = forward.
   * @param meters  The number of meters to drive.
   * @param drive   The drive subsystem on which this command will run.
   */
  public DriveDistance(double speed, double meters, Drive drive) {
    m_distanceMeters = meters;
    m_speed = speed;
    m_drive = drive;
    addRequirements(drive);
  }

  @Override
  public void initialize() {
    m_drive.stop();
    m_startMeters = m_drive.getAveragePositionMeters();
  }

  @Override
  public void execute() {
    double traveled = Math.abs(m_drive.getAveragePositionMeters() - m_startMeters);
    double remaining = m_distanceMeters - traveled;
    double rampedSpeed = m_speed
        * MathUtil.clamp(remaining / DriveConstants.kDriveRampWindowMeters,
            DriveConstants.kDriveMinSpeed, 1.0);
    m_drive.arcadeDrive(rampedSpeed, 0);
  }

  @Override
  public void end(boolean interrupted) {
    m_drive.stop();
  }

  @Override
  public boolean isFinished() {
    double traveled = Math.abs(m_drive.getAveragePositionMeters() - m_startMeters);
    return traveled >= m_distanceMeters;
  }
}