// Copyright (c) 2026 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.subsystems.arm;

import edu.wpi.first.math.MathUtil;
import edu.wpi.first.math.geometry.Pose3d;
import edu.wpi.first.math.geometry.Rotation3d;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.SubsystemBase;
import org.littletonrobotics.junction.Logger;
import org.littletonrobotics.junction.mechanism.LoggedMechanism2d;
import org.littletonrobotics.junction.mechanism.LoggedMechanismLigament2d;
import org.littletonrobotics.junction.mechanism.LoggedMechanismRoot2d;
import edu.wpi.first.math.util.Units;

import frc.robot.Constants;

public class Arm extends SubsystemBase {
  private final ArmIO io;
  private final ArmIOInputsAutoLogged inputs = new ArmIOInputsAutoLogged();

  private double targetAngleDeg = ArmConstants.kDefaultAngleDeg;

  // Mechanism2d canvas: wide enough for arm sweep, tall enough for full extension
  private final LoggedMechanism2d mechanism = new LoggedMechanism2d(3, 3);
  private final LoggedMechanismRoot2d root = mechanism.getRoot("ArmPivot", 1.2, 0.18);
  private final LoggedMechanismLigament2d armLigament =
      root.append(new LoggedMechanismLigament2d("Arm", Units.feetToMeters(3), 0));

  private Pose3d componentPose = new Pose3d();

  public Arm(ArmIO io) {
    this.io = io;
  }

  // Single source of truth. Every setpoint, named or raw, lands here.
  public void setAngleDeg(double angleDeg) {
    targetAngleDeg = MathUtil.clamp(
        angleDeg,
        ArmConstants.kMinAngleDeg,
        ArmConstants.kMaxAngleDeg);
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
        ArmConstants.kMinAngleDeg,
        ArmConstants.kMaxAngleDeg);
    return run(() -> {
      double step = degPerSec * Constants.kLoopPeriodSecs;
      double delta = MathUtil.clamp(target - targetAngleDeg, -step, step);
      setAngleDeg(targetAngleDeg + delta);
    }).until(() -> Math.abs(target - targetAngleDeg)
        < ArmConstants.kAngleToleranceDeg);
  }

  @Override
  public void periodic() {
    io.updateInputs(inputs);
    Logger.processInputs("Arm", inputs);
    Logger.recordOutput("Arm/TargetAngleDeg", targetAngleDeg);
    // Update 2D visualization
    armLigament.setAngle(inputs.commandedAngleDeg);
    Logger.recordOutput("Arm/Mechanism2d", mechanism);
    
    componentPose = new Pose3d(-0.052, 0.007, 0.0645,
        new Rotation3d(0.0, Math.toRadians(inputs.commandedAngleDeg), 0.0));

    io.setAngleDeg(targetAngleDeg);
  }
  
  /** Returns the current 3D pose of the arm for AdvantageScope aggregation. */
  public Pose3d getComponentPose() {
    return componentPose;
  }
}