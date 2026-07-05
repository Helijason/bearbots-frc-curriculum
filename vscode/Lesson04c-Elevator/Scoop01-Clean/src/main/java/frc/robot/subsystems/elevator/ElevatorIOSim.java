// Copyright (c) 2026 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.subsystems.elevator;

import static frc.robot.Constants.kLoopPeriodSecs;
import static frc.robot.Constants.kMaxBatteryVoltage;
import edu.wpi.first.math.MathUtil;

public class ElevatorIOSim implements ElevatorIO {
  private double appliedVolts = 0.0;
  private double positionMeters = 0.0;
  private double velocityMetersPerSec = 0.0;

  @Override
public void updateInputs(ElevatorIOInputs inputs) {
    // Gravity pulls the carriage down: it takes voltage just to hold position.
    double effectiveVolts = appliedVolts - ElevatorConstants.kGravityVolts;

    // Linear model: velocity scales with effective voltage.
    velocityMetersPerSec =
        (effectiveVolts / kMaxBatteryVoltage)
            * ElevatorConstants.kSimMaxSpeedMetersPerSec;

    // Integrate velocity into position each loop tick.
    positionMeters +=
        velocityMetersPerSec * kLoopPeriodSecs;

    // Stop at the physical limits; carriage can't sink through the bottom or fly off the top.
    positionMeters =
        MathUtil.clamp(
            positionMeters,
            ElevatorConstants.kMinHeightMeters,
            ElevatorConstants.kMaxHeightMeters);

    inputs.appliedVolts = appliedVolts;
    inputs.positionMeters = positionMeters;
    inputs.velocityMetersPerSec = velocityMetersPerSec;
    inputs.encoderCount =
        (int) (positionMeters / ElevatorConstants.kEncoderDistancePerPulseMeters);
  }

  @Override
  public void setVoltage(double volts) {
    appliedVolts = volts;
  }

  @Override
  public void resetEncoder() {
    positionMeters = 0.0;
  }

  @Override
  public void stop() {
    appliedVolts = 0.0;
  }
}