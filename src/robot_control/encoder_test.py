import time
from gpiozero import RotaryEncoder

CPR = 1920  # Counts per revolution after gearbox (64 * 30).

encoder = RotaryEncoder(a=17, b=27, max_steps=100000)

print("Reading encoder for 5 seconds, spin the motor shaft by hand...")

start = time.time()
while time.time() - start < 5:
    time.sleep(0.5)
    print(f"Step count: {encoder.steps}")

print(f"Total steps: {encoder.steps}")
print(f"Estimated revolutions: {encoder.steps / CPR:.2f}")