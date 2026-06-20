package frc.robot.subsystems.arm;

import edu.wpi.first.math.MathUtil;
import edu.wpi.first.wpilibj.xrp.XRPServo;
import static frc.robot.Constants.ArmHardware.*;

public class ArmIOXRP implements ArmIO {
  private final XRPServo armServo =
      new XRPServo(kArmServoDeviceNumber);

  private double commandedAngleDeg = ArmConstants.kStowedAngleDeg;

  @Override
  public void updateInputs(ArmIOInputs inputs) {
    inputs.commandedAngleDeg = commandedAngleDeg;
  }

  @Override
  public void setAngle(double angleDeg) {
    commandedAngleDeg =
        MathUtil.clamp(
            angleDeg,
            ArmConstants.kMinAngleDeg,
            ArmConstants.kMaxAngleDeg);

    armServo.setAngle(commandedAngleDeg);
  }
}
