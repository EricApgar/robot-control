import time
import board
import busio
import adafruit_as5600
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

STEPS_PER_REV = 3200        # Microsteps per revolution in MICROSTEP mode.
RPM = 10.0
STEP_DELAY = 60.0 / (RPM * STEPS_PER_REV)
TOLERANCE_DEGREES = 0.5     # Stop stepping when within this many degrees of target.

i2c = busio.I2C(board.SCL, board.SDA)
kit = MotorKit(i2c=i2c)
sensor = adafruit_as5600.AS5600(i2c)

_previous_raw = sensor.angle
_cumulative = 0.0


def read_angle() -> float:
    """Return the sensor angle in degrees relative to the starting position."""
    global _previous_raw, _cumulative
    current_raw = sensor.angle
    delta = current_raw - _previous_raw
    # Unwrap: if the raw jump is >2048 the sensor crossed the 0/4095 boundary.
    if delta > 2048:
        delta -= 4096
    elif delta < -2048:
        delta += 4096
    _cumulative += delta * 360 / 4096
    _previous_raw = current_raw
    return _cumulative


def move_to(target_degrees: float) -> None:
    """Step the motor toward target_degrees, stopping when the sensor confirms arrival."""
    print(f"Moving to {target_degrees:+.1f} degrees...")
    next_step = time.monotonic()
    while True:
        angle = read_angle()
        error = target_degrees - angle
        if abs(error) < TOLERANCE_DEGREES:
            break
        direction = stepper.FORWARD if error > 0 else stepper.BACKWARD
        while time.monotonic() < next_step:
            pass
        kit.stepper2.onestep(direction=direction, style=stepper.MICROSTEP)
        next_step += STEP_DELAY
    print(f"  Arrived at {read_angle():+.1f} degrees")


print("Starting stepper + sensor test. Zeroing at current position...")

move_to(10.0)
move_to(-10.0)
move_to(0.0)

kit.stepper2.release()
print("Done.")
