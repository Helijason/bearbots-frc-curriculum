package frc.robot.subsystems.arm;

import org.littletonrobotics.junction.AutoLog;

public interface ArmIO {
  @AutoLog
  public static class ArmIOInputs {
    public double commandedAngleDeg = ArmConstants.kStowedAngleDeg;
  }

  public default void updateInputs(ArmIOInputs inputs) {}

  public default void setAngle(double angleDeg) {}
}
