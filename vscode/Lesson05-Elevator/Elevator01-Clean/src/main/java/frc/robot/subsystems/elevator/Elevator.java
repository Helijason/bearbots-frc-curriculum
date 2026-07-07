// Copyright (c) 2026 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.subsystems.elevator;

import edu.wpi.first.math.MathUtil;
import edu.wpi.first.math.controller.PIDController;
import edu.wpi.first.math.controller.ElevatorFeedforward;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.SubsystemBase;
import org.littletonrobotics.junction.AutoLogOutput;
import org.littletonrobotics.junction.Logger;
import org.littletonrobotics.junction.networktables.LoggedNetworkNumber;
import static frc.robot.Constants.kMaxBatteryVoltage;

import frc.robot.Constants;

public class Elevator extends SubsystemBase {
  public enum Goal {
    BOTTOM,
    MIDDLE,
    TOP
  }

  private final ElevatorIO io;
  private final ElevatorIOInputsAutoLogged inputs = new ElevatorIOInputsAutoLogged();

  // One controller does the math: error in, volts out. Tolerance decides "close enough".
  private final PIDController controller = new PIDController(
      Constants.currentMode == Constants.Mode.SIM
          ? ElevatorConstants.kPSim
          : ElevatorConstants.kPReal,
      Constants.currentMode == Constants.Mode.SIM
          ? ElevatorConstants.kISim
          : ElevatorConstants.kIReal,
      Constants.currentMode == Constants.Mode.SIM
          ? ElevatorConstants.kDSim
          : ElevatorConstants.kDReal);

  // Rebuilt each loop from the tune handles below (ElevatorFeedforward gains are final).
  private ElevatorFeedforward feedforward = new ElevatorFeedforward(
      Constants.currentMode == Constants.Mode.SIM
          ? ElevatorConstants.kSVoltsSim
          : ElevatorConstants.kSVoltsReal,
      Constants.currentMode == Constants.Mode.SIM
          ? ElevatorConstants.kGVoltsSim
          : ElevatorConstants.kGVoltsReal,
      Constants.currentMode == Constants.Mode.SIM
          ? ElevatorConstants.kVVoltSecPerMeterSim
          : ElevatorConstants.kVVoltSecPerMeterReal);

  // TUNE handles. Bake winners into constants, then delete these + the setPID/feedforward lines.
  private final LoggedNetworkNumber kP =
      new LoggedNetworkNumber("/Tuning/Elevator/kP", controller.getP());
  private final LoggedNetworkNumber kI =
      new LoggedNetworkNumber("/Tuning/Elevator/kI", controller.getI());
  private final LoggedNetworkNumber kD =
      new LoggedNetworkNumber("/Tuning/Elevator/kD", controller.getD());
  private final LoggedNetworkNumber kS =
      new LoggedNetworkNumber("/Tuning/Elevator/kS", feedforward.getKs());
  private final LoggedNetworkNumber kG =
      new LoggedNetworkNumber("/Tuning/Elevator/kG", feedforward.getKg());
  private final LoggedNetworkNumber kV =
      new LoggedNetworkNumber("/Tuning/Elevator/kV", feedforward.getKv());

  @AutoLogOutput(key = "Elevator/Goal")
  private Goal goal = Goal.BOTTOM;

  public Elevator(ElevatorIO io) {
    this.io = io;
    controller.setTolerance(ElevatorConstants.kHeightToleranceMeters);
  }

  public void setGoal(Goal newGoal) {
    goal = newGoal;
  }

  // Jump to a goal and forget it. Bind to a button.
  public Command setGoalCommand(Goal newGoal) {
    return runOnce(() -> setGoal(newGoal));
  }

  // Go to a goal and finish once we're within tolerance. Use this inside sequences.
  // run() requires this subsystem, so nothing else can fight it while it settles.
  public Command goToGoalCommand(Goal newGoal) {
    return run(() -> setGoal(newGoal)).until(this::atGoal);
  }

  @AutoLogOutput(key = "Elevator/AtGoal")
  public boolean atGoal() {
    return controller.atSetpoint();
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

    double clampedTarget = MathUtil.clamp(
        targetMeters,
        ElevatorConstants.kMinHeightMeters,
        ElevatorConstants.kMaxHeightMeters);

    Logger.recordOutput("Elevator/TargetMeters", clampedTarget);

    // TUNE: apply live gains each loop. Delete when you bake.
    controller.setPID(kP.get(), kI.get(), kD.get());
    feedforward = new ElevatorFeedforward(kS.get(), kG.get(), kV.get());
 
    // Feedback (PID) + feedforward (gravity/static hold). velocity setpoint 0 = hold.
    double volts = controller.calculate(inputs.positionMeters, clampedTarget)
        + feedforward.calculate(0.0);
    volts = MathUtil.clamp(volts, -kMaxBatteryVoltage, kMaxBatteryVoltage);

    io.setVoltage(volts);
  }
}