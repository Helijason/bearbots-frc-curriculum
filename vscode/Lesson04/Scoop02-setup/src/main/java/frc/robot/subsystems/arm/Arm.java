// Copyright (c) 2025 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.subsystems.arm;

import edu.wpi.first.math.MathUtil;
import edu.wpi.first.math.geometry.Pose3d;
import edu.wpi.first.math.geometry.Rotation3d;
import edu.wpi.first.math.util.Units;
import org.littletonrobotics.junction.mechanism.LoggedMechanism2d;
import org.littletonrobotics.junction.mechanism.LoggedMechanismLigament2d;
import org.littletonrobotics.junction.mechanism.LoggedMechanismRoot2d;
import edu.wpi.first.wpilibj2.command.SubsystemBase;
import org.littletonrobotics.junction.Logger;

public class Arm extends SubsystemBase {
  private final ArmIO io;
  private final ArmIOInputsAutoLogged inputs = new ArmIOInputsAutoLogged();

  // Mechanism2d canvas: wide enough for arm sweep, tall enough for full extension
  private final LoggedMechanism2d mechanism = new LoggedMechanism2d(3, 3);
  private final LoggedMechanismRoot2d root = mechanism.getRoot("ArmPivot", 1.2, 0.18);
  private final LoggedMechanismLigament2d armLigament =
      root.append(new LoggedMechanismLigament2d("Arm", Units.feetToMeters(3), 0));

  private Pose3d componentPose = new Pose3d();

  /** Creates a new Arm. */
  public Arm(ArmIO io) {
    this.io = io;
  }

  @Override
  public void periodic() {
    io.updateInputs(inputs);
    Logger.processInputs("Arm", inputs);

    // Update 2D visualization
    armLigament.setAngle(180 - inputs.commandedAngleDeg);
    Logger.recordOutput("Arm/Mechanism2d", mechanism);
    componentPose = new Pose3d(-0.052, 0.007, 0.0645,
        new Rotation3d(0.0, Math.toRadians(inputs.commandedAngleDeg), 0.0));
  } 

  /**
   * Set the current angle of the arm in degrees.
   *
   * @param angleDeg desired arm angle in degrees
   */
  public void setAngle(double angleDeg) {
      double clamped = MathUtil.clamp(
          angleDeg, ArmConstants.kMinAngleDeg, ArmConstants.kMaxAngleDeg);
      io.setAngle(clamped);
      Logger.recordOutput("Arm/Commanded/AngleDeg", clamped);
  }

  /** Move the arm to its safe/stowed position. */
  public void stop() {
    setAngle(ArmConstants.kStowedAngleDeg);
  }

  public double getCommandedAngleDeg() {
    return inputs.commandedAngleDeg;
  }

  /** Returns the current 3D pose of the arm for AdvantageScope aggregation. */
  public Pose3d getComponentPose() {
    return componentPose;
  }
}
