// Copyright (c) 2025 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.subsystems.scoop;

import edu.wpi.first.math.MathUtil;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.SubsystemBase;
import org.littletonrobotics.junction.Logger;

public class Scoop extends SubsystemBase {
    public enum Goal {
        FLAT,
        CARRY,
        DUMP
    }

    private final ScoopIO io;
    private final ScoopIOInputsAutoLogged inputs = new ScoopIOInputsAutoLogged();
    private Goal goal = Goal.FLAT;

    public Scoop(ScoopIO io) {
    this.io = io;
  }

  public void setGoal(Goal newGoal) {
    goal = newGoal;
  }

  public Command setGoalCommand(Goal newGoal) {
    return runOnce(() -> setGoal(newGoal));
  }

  public void stop() {
    setGoal(Goal.FLAT);
  }

  @Override
  public void periodic() {
      io.updateInputs(inputs);
      Logger.processInputs("Scoop", inputs);

      double targetAngle = switch (goal) {
          case FLAT  -> ScoopConstants.kFlatAngleDeg;
          case CARRY -> ScoopConstants.kCarryAngleDeg;
          case DUMP  -> ScoopConstants.kDumpAngleDeg;
      };

      double clamped = MathUtil.clamp(
          targetAngle,
          ScoopConstants.kMinAngleDeg,
          ScoopConstants.kMaxAngleDeg);

      io.setAngle(clamped);
      Logger.recordOutput("Scoop/Goal", goal.toString());
  }
}