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

# Steps taken between sensor checks during limit sweep. Each step is ~0.11 degrees,
# so 20 steps = ~2.25 degrees of commanded motion per check.
LIMIT_STEPS_PER_CHECK = 20
# If the sensor moves less than this over LIMIT_STEPS_PER_CHECK steps, we're at a limit.
LIMIT_MOVEMENT_THRESHOLD = 0.2

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


def find_limit(direction: int) -> float:
    """Step in direction until the sensor stops responding. Returns the limit angle."""
    dir_name = "right" if direction == stepper.FORWARD else "left"
    print(f"Sweeping to {dir_name} limit...")
    next_step = time.monotonic()
    while True:
        angle_before = read_angle()
        for _ in range(LIMIT_STEPS_PER_CHECK):
            while time.monotonic() < next_step:
                pass
            kit.stepper2.onestep(direction=direction, style=stepper.MICROSTEP)
            next_step += STEP_DELAY
        angle_after = read_angle()
        if abs(angle_after - angle_before) < LIMIT_MOVEMENT_THRESHOLD:
            limit = read_angle()
            print(f"  {dir_name.capitalize()} limit: {limit:+.1f} degrees")
            return limit


def home() -> None:
    """Sweep to both physical limits, then move to the midpoint and redefine it as zero."""
    global _previous_raw, _cumulative
    left_limit = find_limit(stepper.BACKWARD)
    right_limit = find_limit(stepper.FORWARD)
    midpoint = (left_limit + right_limit) / 2.0
    print(f"Range: {left_limit:+.1f} to {right_limit:+.1f} degrees ({right_limit - left_limit:.1f} total). Moving to midpoint...")
    move_to(midpoint)
    _previous_raw = sensor.angle
    _cumulative = 0.0
    print("Homed. Current position is now 0 degrees.")


def test_manual_zero() -> None:
    """Sweep +-10 degrees from wherever the motor is when the test starts."""
    print("Starting manual-zero test. Zeroing at current position...")
    move_to(10.0)
    move_to(-10.0)
    move_to(0.0)


def test_homing() -> None:
    """Auto-home by finding physical limits, then sweep +-10 degrees from neutral."""
    print("Starting homing test...")
    home()
    move_to(10.0)
    move_to(-10.0)
    move_to(0.0)


# --- Run test ---
try:
    test_homing()
finally:
    kit.stepper2.release()
    print("Motor released.")
