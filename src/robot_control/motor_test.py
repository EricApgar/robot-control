import time
from adafruit_motorkit import MotorKit

kit = MotorKit()

TARGET_SPEED = 1
RAMP_STEPS = 50
RAMP_DURATION = 1.0  # Seconds to complete the ramp.
HOLD_DURATION = 2.0  # Seconds to hold at target speed.

step_delay = RAMP_DURATION / RAMP_STEPS


def ramp(start: float, end: float) -> None:
    """Gradually transition motor throttle from start to end."""
    for i in range(RAMP_STEPS + 1):
        throttle = start + (end - start) * (i / RAMP_STEPS)
        kit.motor1.throttle = throttle
        time.sleep(step_delay)


print("Ramping up...")
ramp(0.0, TARGET_SPEED)

print(f"Holding at {TARGET_SPEED * 100:.0f}% speed...")
time.sleep(HOLD_DURATION)

print("Ramping down...")
ramp(TARGET_SPEED, 0.0)

print("Done.")