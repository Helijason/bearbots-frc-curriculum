// Copyright (c) 2025 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.subsystems.scoop;

import edu.wpi.first.wpilibj.xrp.XRPServo;
import static frc.robot.Constants.ScoopHardware.*;

public class ScoopIOXRP implements ScoopIO {
  private final XRPServo servo = new XRPServo(kScoopServoDeviceNumber);

  private double commandedAngleDeg = ScoopConstants.kFlatAngleDeg;

  @Override
  public void updateInputs(ScoopIOInputs inputs) {
    inputs.commandedAngleDeg = commandedAngleDeg;
  }

  @Override
  public void setAngle(double angleDeg) {
    commandedAngleDeg = angleDeg;
    servo.setAngle(commandedAngleDeg);
  }
}