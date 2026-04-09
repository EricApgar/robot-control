import time
import board
import busio
import adafruit_as5600

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_as5600.AS5600(i2c)

print("Reading AS5600 angle. Move a magnet near the sensor (Ctrl+C to stop)...")
print()

while True:
    angle = sensor.angle
    print(f"\rAngle: {angle:6.1f} degrees", end="", flush=True)
    time.sleep(0.1)
