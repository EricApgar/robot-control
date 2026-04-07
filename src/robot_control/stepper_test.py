import time

from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

STEPS_PER_REV = 3200  # Microsteps per revolution in MICROSTEP mode (200 full steps * 16).
RPM = 2.0             # Target speed in revolutions per minute.

STEP_DELAY = 60.0 / (RPM * STEPS_PER_REV)  # Seconds per step.

kit = MotorKit()


def rotate(direction: int, steps: int) -> None:
    """Step the motor in the given direction for the given number of steps."""
    next_step = time.monotonic()
    for _ in range(steps):
        while time.monotonic() < next_step:
            pass
        kit.stepper2.onestep(direction=direction, style=stepper.MICROSTEP)
        next_step += STEP_DELAY


print("Rotating clockwise 360 degrees...")
rotate(stepper.FORWARD, STEPS_PER_REV)

kit.stepper2.release()

print("Rotating counterclockwise 360 degrees...")
rotate(stepper.BACKWARD, STEPS_PER_REV)

kit.stepper2.release()
print("Done.")
