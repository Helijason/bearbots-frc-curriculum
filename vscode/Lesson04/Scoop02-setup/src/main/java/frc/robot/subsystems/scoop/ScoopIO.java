// Copyright (c) 2025 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.subsystems.scoop;

import org.littletonrobotics.junction.AutoLog;

public interface ScoopIO {
  @AutoLog
  static class ScoopIOInputs {
    public double commandedAngleDeg = ScoopConstants.kFlatAngleDeg;
  }

  default void updateInputs(ScoopIOInputs inputs) {}

  default void setAngle(double angleDeg) {}
}