// Copyright (c) 2026 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.subsystems.elevator;

import org.littletonrobotics.junction.AutoLog;

public interface ElevatorIO {
  @AutoLog
  static class ElevatorIOInputs {
    public int encoderCount = 0;
    public double positionMeters = 0.0;
    public double velocityMetersPerSec = 0.0;
    public double appliedVolts = 0.0;
  }

  default void updateInputs(ElevatorIOInputs inputs) {}

  default void setVoltage(double volts) {}

  default void resetEncoder() {}

  default void stop() {
    setVoltage(0.0);
  }
}