// Copyright (c) 2026 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.subsystems.scoop;

import edu.wpi.first.math.MathUtil;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.SubsystemBase;
import org.littletonrobotics.junction.Logger;
import frc.robot.Constants;

public class Scoop extends SubsystemBase {
  private final ScoopIO io;
  private final ScoopIOInputsAutoLogged inputs = new ScoopIOInputsAutoLogged();

  private double targetAngleDeg = ScoopConstants.kDefaultAngleDeg;

  public Scoop(ScoopIO io) {
    this.io = io;
  }

  // Single source of truth. Every setpoint, named or raw, lands here.
  public void setAngleDeg(double angleDeg) {
    targetAngleDeg = MathUtil.clamp(
        angleDeg,
        ScoopConstants.kMinAngleDeg,
        ScoopConstants.kMaxAngleDeg);
  }

  // Jump to a setpoint immediately. Bind to a button:
  //   button.onTrue(xxx.setAngleDegCommand(XxxConstants.kDeployedAngleDeg));
  public Command setAngleDegCommand(double angleDeg) {
    return runOnce(() -> setAngleDeg(angleDeg));
  }

  // Slew to a setpoint at a capped rate, finish within tolerance.
  public Command setAngleDegSteppedCommand(double angleDeg, double degPerSec) {
    double target = MathUtil.clamp(
        angleDeg,
        ScoopConstants.kMinAngleDeg,
        ScoopConstants.kMaxAngleDeg);
    return run(() -> {
      double step = degPerSec * Constants.kLoopPeriodSecs;
      double delta = MathUtil.clamp(target - targetAngleDeg, -step, step);
      setAngleDeg(targetAngleDeg + delta);
    }).until(() -> Math.abs(target - targetAngleDeg)
        < ScoopConstants.kAngleToleranceDeg);
  }

  @Override
  public void periodic() {
    io.updateInputs(inputs);
    Logger.processInputs("Scoop", inputs);
    Logger.recordOutput("Scoop/TargetAngleDeg", targetAngleDeg);

    io.setAngleDeg(targetAngleDeg);
  }
}