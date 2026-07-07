// Copyright (c) 2026 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.subsystems.elevator;

import edu.wpi.first.math.MathUtil;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.SubsystemBase;
import org.littletonrobotics.junction.AutoLogOutput;
import org.littletonrobotics.junction.Logger;
import static frc.robot.Constants.kMaxBatteryVoltage;
import org.littletonrobotics.junction.networktables.LoggedNetworkNumber;

import frc.robot.Constants;

public class Elevator extends SubsystemBase {
  public enum Goal {
    BOTTOM,
    MIDDLE,
    TOP
  }

  private final ElevatorIO io;
  private final ElevatorIOInputsAutoLogged inputs = new ElevatorIOInputsAutoLogged();

  private final LoggedNetworkNumber kP =    // temporary, use to tune from AK.
    new LoggedNetworkNumber("/Tuning/Elevator/kP",
    Constants.currentMode == Constants.Mode.SIM
        ? ElevatorConstants.kPSim
        : ElevatorConstants.kPReal);

  @AutoLogOutput(key = "Elevator/Goal")
  private Goal goal = Goal.BOTTOM;

  public Elevator(ElevatorIO io) {
    this.io = io;
  }

  public void setGoal(Goal newGoal) {
    goal = newGoal;
  }

  public Command setGoalCommand(Goal newGoal) {
    return runOnce(() -> setGoal(newGoal));
  }

  public void stop() {
    io.stop();
  }

  @Override
  public void periodic() {
    io.updateInputs(inputs);
    Logger.processInputs("Elevator", inputs);

    double targetMeters = switch (goal) {
      case BOTTOM -> ElevatorConstants.kBottomHeightMeters;
      case MIDDLE -> ElevatorConstants.kMiddleHeightMeters;
      case TOP -> ElevatorConstants.kTopHeightMeters;
    };
    // ********* uncomment once kP has been found
    // double kP = Constants.currentMode == Constants.Mode.SIM
    //     ? ElevatorConstants.kPSim
    //     : ElevatorConstants.kPReal;
    double clampedTarget = MathUtil.clamp(
        targetMeters,
        ElevatorConstants.kMinHeightMeters,
        ElevatorConstants.kMaxHeightMeters);

    Logger.recordOutput("Elevator/TargetMeters", clampedTarget);

    // P-control: drive voltage proportional to position error.
    double error = clampedTarget - inputs.positionMeters;
    //double volts = ElevatorConstants.kP * error;  // Volts Calculating from ElevatorConstants.kP
    double volts = kP.get() * error;                // Volts calculated from AK tunned kP.
    volts = MathUtil.clamp(volts, -kMaxBatteryVoltage, kMaxBatteryVoltage);

    io.setVoltage(volts);
  }
}