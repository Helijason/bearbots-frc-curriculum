// Copyright (c) 2026 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.subsystems.arm;

public class ArmIOSim implements ArmIO {
  private double commandedAngleDeg = ArmConstants.kDefaultAngleDeg;

  @Override
  public void updateInputs(ArmIOInputs inputs) {
    inputs.commandedAngleDeg = commandedAngleDeg;
  }

  @Override
  public void setAngleDeg(double angleDeg) {
    commandedAngleDeg = angleDeg;
  }
}