import time
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

STEPS_PER_REV = 400  # Half-steps per revolution in INTERLEAVE mode (200 full steps * 2).
STEP_DELAY = 0.02    # Seconds between steps. Increase if motor misses steps.

kit = MotorKit()


def rotate(direction: int, steps: int) -> None:
    """Step the motor in the given direction for the given number of steps."""
    for _ in range(steps):
        kit.stepper2.onestep(direction=direction, style=stepper.INTERLEAVE)
        time.sleep(STEP_DELAY)


print("Rotating clockwise 360 degrees...")
rotate(stepper.FORWARD, STEPS_PER_REV)

print("Rotating counterclockwise 360 degrees...")
rotate(stepper.BACKWARD, STEPS_PER_REV)

kit.stepper2.release()
print("Done.")
