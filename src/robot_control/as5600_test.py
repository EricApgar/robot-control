import time
import board
import busio
import adafruit_as5600

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_as5600.AS5600(i2c)

print("Reading AS5600 sensor (Ctrl+C to stop)...")
print()

# Print initial blank lines so the cursor-up trick works from the first iteration
print("Magnet Status: ")
print("Raw Angle:     ")
print("Scaled Angle:  ")
print("Magnitude:     ")

while True:
    if not sensor.magnet_detected:
        status = "Missing"
    elif sensor.min_gain_overflow:
        status = "Too strong"
    elif sensor.max_gain_overflow:
        status = "Too weak"
    else:
        status = "Good"

    raw = sensor.raw_angle
    degrees = raw * 360 / 4096

    lines = [
        f"Magnet Status: {status}",
        f"Raw Angle:     {raw}",
        f"Scaled Angle:  {degrees:.2f}°",
        f"Magnitude:     {sensor.magnitude}",
    ]

    # Move cursor up 4 lines, then overwrite each line
    print("\033[4A", end="")
    for line in lines:
        print(f"\r{line}\033[K")

    time.sleep(0.1)
