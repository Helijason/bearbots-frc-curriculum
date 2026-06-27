// Copyright (c) 2025 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.subsystems.arm;

import org.littletonrobotics.junction.AutoLog;

public interface ArmIO {
  @AutoLog
  static class ArmIOInputs {
    public double commandedAngleDeg = ArmConstants.kStowedAngleDeg;
  }

  default void updateInputs(ArmIOInputs inputs) {}

  default void setAngle(double angleDeg) {}
}
