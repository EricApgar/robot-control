import time
from adafruit_motorkit import MotorKit
from gpiozero import RotaryEncoder

ENCODER_A = 17
ENCODER_B = 27
CPR = 1920          # Counts per revolution after gearbox (64 * 30).
SAMPLE_INTERVAL = 0.5  # Seconds between RPM calculations.
MOTOR_SPEED = 0.5   # 50% throttle.

kit = MotorKit()
encoder = RotaryEncoder(a=ENCODER_A, b=ENCODER_B, max_steps=1000000)


def calculate_rpm(delta_steps: int, interval: float) -> float:
    """Calculate RPM from encoder step delta over a time interval."""
    revolutions = abs(delta_steps) / CPR
    minutes = interval / 60
    return revolutions / minutes


print("Running motor and measuring RPM. Press Ctrl+C to stop.")
kit.motor1.throttle = MOTOR_SPEED

last_steps = encoder.steps
last_time = time.time()

try:
    while True:
        time.sleep(SAMPLE_INTERVAL)
        now = time.time()
        current_steps = encoder.steps
        delta_steps = current_steps - last_steps
        delta_time = now - last_time
        rpm = calculate_rpm(delta_steps, delta_time)
        print(f"RPM: {rpm:.1f}  |  Total steps: {current_steps}")
        last_steps = current_steps
        last_time = now

except KeyboardInterrupt:
    print("\nStopping motor.")
    kit.motor1.throttle = 0