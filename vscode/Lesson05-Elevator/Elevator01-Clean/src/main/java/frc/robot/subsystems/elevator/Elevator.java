// Copyright (c) 2026 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.subsystems.elevator;

import edu.wpi.first.math.MathUtil;
import edu.wpi.first.math.controller.ElevatorFeedforward;
import edu.wpi.first.math.controller.PIDController;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.SubsystemBase;
import org.littletonrobotics.junction.AutoLogOutput;
import org.littletonrobotics.junction.Logger;
import org.littletonrobotics.junction.networktables.LoggedNetworkNumber;
import static frc.robot.Constants.kMaxBatteryVoltage;

import frc.robot.Constants;

public class Elevator extends SubsystemBase {
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

  private double targetMeters = ElevatorConstants.kDefaultHeightMeters;

  public Elevator(ElevatorIO io) {
    this.io = io;
    controller.setTolerance(ElevatorConstants.kHeightToleranceMeters);
  }

  // Single source of truth. Every setpoint, named or raw, lands here.
  public void setHeightMeters(double meters) {
    targetMeters = MathUtil.clamp(
        meters,
        ElevatorConstants.kMinHeightMeters,
        ElevatorConstants.kMaxHeightMeters);
  }

  // Jump to a height immediately. Bind to a button:
  //   button.onTrue(elevator.setHeightMetersCommand(ElevatorConstants.kTopHeightMeters));
  public Command setHeightMetersCommand(double meters) {
    return runOnce(() -> setHeightMeters(meters));
  }

  // Go to a height and finish once within tolerance. Use this inside sequences.
  public Command goToHeightMetersCommand(double meters) {
    return run(() -> setHeightMeters(meters)).until(this::atGoal);
  }

  public Command homeCommand() {
    return run(() -> io.setVoltage(ElevatorConstants.kHomingVolts))   // small down voltage
      .until(() -> Math.abs(inputs.velocityMetersPerSec) < ElevatorConstants.kHomingStallMetersPerSec)
      .withTimeout(ElevatorConstants.kHomingTimeoutSecs)             // safety
      .andThen(runOnce(() -> {
            io.stop();
            io.resetEncoder();
            setHeightMeters(ElevatorConstants.kDefaultHeightMeters);
          }))
      .ignoringDisable(false);   // moving motor -> must be enabled
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

    Logger.recordOutput("Elevator/TargetMeters", targetMeters);

    // TUNE: apply live gains each loop. Delete when you bake.
    controller.setPID(kP.get(), kI.get(), kD.get());
    feedforward = new ElevatorFeedforward(kS.get(), kG.get(), kV.get());

    // Feedback (PID) + feedforward (gravity/static hold). velocity setpoint 0 = hold.
    double volts = controller.calculate(inputs.positionMeters, targetMeters)
        + feedforward.calculate(0.0);
    volts = MathUtil.clamp(volts, -kMaxBatteryVoltage, kMaxBatteryVoltage);

    io.setVoltage(volts);
  }
}