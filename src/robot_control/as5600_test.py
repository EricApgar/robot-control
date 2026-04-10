import time
import board
import busio
import adafruit_as5600

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_as5600.AS5600(i2c)

print("Reading AS5600 angle. Move a magnet near the sensor (Ctrl+C to stop)...")
print()

previous = sensor.angle
cumulative = 0.0

while True:
    current = sensor.angle
    delta = current - previous

    # Unwrap: if the raw jump is >180 the sensor crossed the 0/360 boundary.
    if delta > 180:
        delta -= 360
    elif delta < -180:
        delta += 360

    cumulative += delta
    previous = current

    print(f"\rAngle: {cumulative:+.1f} degrees", end="", flush=True)
    time.sleep(0.1)
