// Copyright (c) 2026 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.subsystems.scoop;

import edu.wpi.first.math.MathUtil;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.SubsystemBase;
import org.littletonrobotics.junction.AutoLogOutput;
import org.littletonrobotics.junction.Logger;

public class Scoop extends SubsystemBase {
  public enum Goal {
    FLAT,
    CARRY,
    DUMP
  }

  private final ScoopIO io;
  private final ScoopIOInputsAutoLogged inputs = new ScoopIOInputsAutoLogged();

  @AutoLogOutput(key = "Scoop/Goal")
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

    double targetAngleDeg = switch (goal) {
      case FLAT -> ScoopConstants.kFlatAngleDeg;
      case CARRY -> ScoopConstants.kCarryAngleDeg;
      case DUMP -> ScoopConstants.kDumpAngleDeg;
    };

    double clamped = MathUtil.clamp(
        targetAngleDeg,
        ScoopConstants.kMinAngleDeg,
        ScoopConstants.kMaxAngleDeg);

    // io.setAngle assumes a matching IO setter of that name.
    // If the IO method is named differently (e.g. setAngle, setPosition,
    // setSpeed), rename the call below instead of the mirrored tabstop.
    io.setAngle(clamped);
  }
}