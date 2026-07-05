// Copyright (c) 2026 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.subsystems.arm2;

import edu.wpi.first.wpilibj.xrp.XRPServo;
import static frc.robot.Constants.Arm2Hardware.*;

public class Arm2IOXRP implements Arm2IO {
  private final XRPServo servo = new XRPServo(kArmServoDeviceNumber);

  private double commandedAngleDeg = Arm2Constants.kDefaultAngleDeg;

  @Override
  public void updateInputs(Arm2IOInputs inputs) {
    inputs.commandedAngleDeg = commandedAngleDeg;
  }

  @Override
  public void setAngle(double angleDeg) {
    commandedAngleDeg = angleDeg;
    servo.setAngle(commandedAngleDeg);
  }
}