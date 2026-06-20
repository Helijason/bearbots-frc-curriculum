package frc.robot.subsystems.arm;
 
import edu.wpi.first.math.MathUtil;
 
public class ArmIOSim implements ArmIO {
  private double commandedAngleDeg = ArmConstants.kStowedAngleDeg;
 
  @Override
  public void updateInputs(ArmIOInputs inputs) {
    inputs.commandedAngleDeg = commandedAngleDeg;
  }
 
  @Override
  public void setAngle(double angleDeg) {
    // Clamp to valid servo range — mirrors ArmIOXRP behavior.
    commandedAngleDeg =
        MathUtil.clamp(
            angleDeg,
            ArmConstants.kMinAngleDeg,
            ArmConstants.kMaxAngleDeg);
  }
}
 