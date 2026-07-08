// Copyright (c) 2026 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.subsystems.elevator;

import edu.wpi.first.math.MathUtil;
import edu.wpi.first.math.controller.ElevatorFeedforward;
import edu.wpi.first.math.controller.PIDController;
import edu.wpi.first.math.geometry.Pose3d;
import edu.wpi.first.math.geometry.Rotation3d;
import edu.wpi.first.math.util.Units;
import edu.wpi.first.wpilibj.util.Color;
import edu.wpi.first.wpilibj.util.Color8Bit;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.SubsystemBase;
import java.util.function.BooleanSupplier;
import org.littletonrobotics.junction.AutoLogOutput;
import org.littletonrobotics.junction.Logger;
import org.littletonrobotics.junction.mechanism.LoggedMechanism2d;
import org.littletonrobotics.junction.mechanism.LoggedMechanismLigament2d;
import org.littletonrobotics.junction.mechanism.LoggedMechanismRoot2d;
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
  private boolean homing = false;

  // Mechanism2d canvas: narrow vertical rail, not a square block. Height (0.2) still gives
  // the 0.135m max travel plenty of room; width is just enough to draw the carriage.
  // Root is shifted 4 inches forward (+X) to match the elevator's real mounting position.
  private static final double kForwardOffsetMeters = Units.inchesToMeters(9.5);
  private final LoggedMechanism2d mechanism =
      new LoggedMechanism2d(0.1 + kForwardOffsetMeters, 0.2);
  private final LoggedMechanismRoot2d root =
      mechanism.getRoot("ElevatorBase", 0.05 + kForwardOffsetMeters, 0.02);
  private final LoggedMechanismLigament2d carriageLigament =
      root.append(new LoggedMechanismLigament2d(
          "Carriage", 0.01, 90, 4, new Color8Bit(Color.kOrange)));

  private Pose3d componentPose = new Pose3d();

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
    return run(() -> setHeightMeters(meters))
        .until(this::atGoal)
        .finallyDo(interrupted -> {
          // Cancelled early: hold where we are instead of chasing the old target.
          if (interrupted) setHeightMeters(inputs.positionMeters);
        });
  }

  // Stall-stop homing. Drives toward the hard stop, zeros the encoder there.
  public Command homeCommand() {
    // Stall-stop, but only after the carriage has actually started moving,
    // otherwise the initial velocity of 0 ends it on the first loop.
    BooleanSupplier stalled = new BooleanSupplier() {
      boolean moved = false;
      public boolean getAsBoolean() {
        double v = Math.abs(inputs.velocityMetersPerSec);
        if (v > ElevatorConstants.kHomingMovingMetersPerSec) moved = true;
        return moved && v < ElevatorConstants.kHomingStallMetersPerSec;
      }
    };
    return startRun(
            () -> homing = true,
            () -> io.setVoltage(ElevatorConstants.kHomingVolts))
        .until(stalled)
        .withTimeout(ElevatorConstants.kHomingTimeoutSecs)
        .finallyDo(() -> {
              io.stop();
              io.resetEncoder();
              setHeightMeters(ElevatorConstants.kDefaultHeightMeters);
              homing = false;
            });
  }

  @AutoLogOutput(key = "Elevator/AtGoal")
  public boolean atGoal() {
    return controller.atSetpoint();
  }

  public void stop() {
    io.stop();
  }

  /** Returns the current 3D pose of the elevator carriage for AdvantageScope aggregation. */
  public Pose3d getComponentPose() {
    return componentPose;
  }

  /** Returns the current carriage height in meters, for subsystems mounted on the elevator. */
  public double getPositionMeters() {
    return inputs.positionMeters;
  }

  @Override
  public void periodic() {
    io.updateInputs(inputs);
    Logger.processInputs("Elevator", inputs);

    // Update 2D visualization. Floor the length so the carriage stays visible at height 0.
    carriageLigament.setLength(Math.max(inputs.positionMeters, 0.01));
    Logger.recordOutput("Elevator/Mechanism2d", mechanism);

    // Update 3D component pose. Elevator mounts to the XRP frame, shifted 4 inches forward
    // (+X). Scoop mounts to the elevator, not the frame, and inherits this offset via the
    // pose composition in Robot.java. PLACEHOLDER Y/base-Z: tune by eye in AdvantageScope.
    componentPose = new Pose3d(
        Units.inchesToMeters(4.0), 0.0, inputs.positionMeters, new Rotation3d());

    if (homing) return;   // homing owns the motor; skip PID this loop

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