// Copyright (c) 2026 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.subsystems.scoop;

import org.littletonrobotics.junction.AutoLogOutput;

import edu.wpi.first.wpilibj.xrp.XRPServo;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.SubsystemBase;
import org.littletonrobotics.junction.Logger;

public class Scoop extends SubsystemBase {
  private final XRPServo scoopServo = new XRPServo(5);
  
  @AutoLogOutput
  private double targetAngleDeg = 0.0; // Default starting point
  
  /** Creates a new Scoop. */
  public Scoop() {
    // Constructor - runs once at startup
  }

  // simple setter, changes the goal field
  public void setAngleDeg(double angleDeg) {
    targetAngleDeg = angleDeg;
    scoopServo.setAngle(targetAngleDeg);
  }

  // returns a command that sets the goal once, then ends
  // runOnce() = run the lambda once, then the command is done
  public Command setAngleDegCommand(double angleDeg) {
    return runOnce(() -> setAngleDeg(angleDeg));
  }

  @Override
  public void periodic() {
    // Called every 20ms (50Hz)
    // Sensors and logging only - no motor control
    Logger.recordOutput("Scoop/TargetAngleDeg", targetAngleDeg);
  }
}
