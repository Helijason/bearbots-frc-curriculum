// Copyright (c) 2026 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.subsystems.scoop;

import edu.wpi.first.math.MathUtil;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.SubsystemBase;
import org.littletonrobotics.junction.Logger;
import frc.robot.Constants;
import edu.wpi.first.math.geometry.Pose3d;
import edu.wpi.first.math.geometry.Rotation3d;
import edu.wpi.first.wpilibj.util.Color;
import edu.wpi.first.wpilibj.util.Color8Bit;

import org.littletonrobotics.junction.mechanism.LoggedMechanism2d;
import org.littletonrobotics.junction.mechanism.LoggedMechanismLigament2d;
import org.littletonrobotics.junction.mechanism.LoggedMechanismRoot2d;

public class Scoop extends SubsystemBase {
  private final ScoopIO io;
  private final ScoopIOInputsAutoLogged inputs = new ScoopIOInputsAutoLogged();

  private double targetAngleDeg = ScoopConstants.kDefaultAngleDeg;
  
  // Mechanism2d: vertical column on the front of the robot
  private final LoggedMechanism2d mechanism = new LoggedMechanism2d(2, 1);
  private final LoggedMechanismRoot2d root = mechanism.getRoot("ScoopPivot", 1.125, 0.016);
  private final LoggedMechanismLigament2d scoopLigament =
      root.append(new LoggedMechanismLigament2d("Scoop", 0.05, 0, 3.25, new Color8Bit(Color.kDarkGray)));
  private Pose3d componentPose = new Pose3d();

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

    // FLAT, CARRY, DUMP
    scoopLigament.setAngle(inputs.commandedAngleDeg - 45);
    Logger.recordOutput("Scoop/Mechanism2d", mechanism);
    componentPose = new Pose3d(0.0, 0.0, 0.0,
        new Rotation3d(0.0, Math.toRadians(scoopLigament.getAngle()), 0.0));

    io.setAngleDeg(targetAngleDeg);
  }

  /** Returns the current 3D pose of the scoop for AdvantageScope aggregation. */
  public Pose3d getComponentPose() {
    return componentPose;
  }
}  