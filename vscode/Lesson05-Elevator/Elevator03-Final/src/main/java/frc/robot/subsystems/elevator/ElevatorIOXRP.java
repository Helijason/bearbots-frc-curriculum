// Copyright (c) 2026 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.subsystems.elevator;

import edu.wpi.first.wpilibj.Encoder;
import edu.wpi.first.wpilibj.xrp.XRPMotor;
import static frc.robot.Constants.ElevatorHardware.*;
import static frc.robot.Constants.kMaxBatteryVoltage;

public class ElevatorIOXRP implements ElevatorIO {
  private final XRPMotor motor = new XRPMotor(kElevatorMotorChannel);
  private final Encoder encoder = new Encoder(kElevatorEncoderChannelA, kElevatorEncoderChannelB);

  private double appliedVolts = 0.0;

  public ElevatorIOXRP() {
    encoder.setDistancePerPulse(ElevatorConstants.kEncoderDistancePerPulseMeters);
  }

  @Override
  public void updateInputs(ElevatorIOInputs inputs) {
    inputs.encoderCount = encoder.get();
    inputs.positionMeters = encoder.getDistance();
    inputs.velocityMetersPerSec = encoder.getRate();
    inputs.appliedVolts = appliedVolts;
  }

  @Override
  public void setVoltage(double volts) {
    appliedVolts = volts;
    motor.set(appliedVolts / kMaxBatteryVoltage);
  }

  @Override
  public void resetEncoder() {
    encoder.reset();
  }

  @Override
  public void stop() {
    motor.set(0.0);
  }
}