// Copyright (c) 2025 BearBots FRC Team 6964
// Open Source Software; you can modify and/or share it under the terms of
// the MIT License available in the root directory of this project.

package frc.robot.subsystems.scoop;

import org.littletonrobotics.junction.AutoLogOutput;

import edu.wpi.first.wpilibj.xrp.XRPServo;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.SubsystemBase;

public class Scoop extends SubsystemBase {
    public enum Goal {
        FLAT,   // resting position
        CARRY,  // holding game piece
        DUMP    // releasing game piece
    }

  private final XRPServo scoopServo = new XRPServo(4);
  
  @AutoLogOutput
  private Goal goal = Goal.FLAT; // start flat
  
  /** Creates a new Scoop. */
  public Scoop() {
    // Constructor - runs once at startup
  }

  // simple setter, changes the goal field
  public void setGoal(Goal newGoal) {
    goal = newGoal;
  }

  // returns a command that sets the goal once, then ends
  // runOnce() = run the lambda once, then the command is done
  public Command setGoalCommand(Goal newGoal) {
    return runOnce(() -> setGoal(newGoal));
  }

  // safe state, called when a command is interrupted
  public void stop() {
    setGoal(Goal.FLAT);  // return to resting position
  }


  @Override
  public void periodic() {
    // Called every 20ms (50Hz)
    // Sensors and logging only - no motor control
    switch (goal) {
        case FLAT  -> scoopServo.setAngle(0.0);
        case CARRY -> scoopServo.setAngle(45.0);
        case DUMP  -> scoopServo.setAngle(90.0);
    }
  }
}
