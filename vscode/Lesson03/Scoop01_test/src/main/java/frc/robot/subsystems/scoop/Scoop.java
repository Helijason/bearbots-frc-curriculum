// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot.subsystems.scoop;

import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.SubsystemBase;
import edu.wpi.first.wpilibj.xrp.XRPServo;
import org.littletonrobotics.junction.AutoLogOutput;

public class Scoop extends SubsystemBase {
    
    public enum Goal {
        FLAT,   // servo at 0° - resting position
        CARRY,  // servo at 45° - holding game piece
        DUMP    // servo at 90° - releasing game piece
    }

  /** Creates a new scoop. */
  private final XRPServo scoopServo = new XRPServo(4);
  @AutoLogOutput
  private Goal goal = Goal.FLAT;

  public Scoop() {
      // Constructor - runs once at startup
      switch (goal) {
        case FLAT  -> scoopServo.setAngle(0.0);
        case CARRY -> scoopServo.setAngle(45.0);
        case DUMP  -> scoopServo.setAngle(90.0);
    }    
  }

    // ← add this method - simple setter, changes the goal field
  public void setGoal(Goal newGoal) {
      goal = newGoal;
  }

  // ← add this method - returns a command that sets the goal once, then ends
  // runOnce() = run the lambda once, then the command is done
  public Command setGoalCommand(Goal newGoal) {
      return runOnce(() -> setGoal(newGoal));
  }

  // ← add this method - safe state, called when a command is interrupted
  public void stop() {
      setGoal(Goal.FLAT);  // return to resting position
  }

  @Override
  public void periodic() {
    // Called every 20ms (50Hz)
    // Sensors and logging only - no motor control
  }
}
