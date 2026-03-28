import time
from adafruit_motorkit import MotorKit

kit = MotorKit()

print("Spinning motor forward at 50% speed...")
kit.motor1.throttle = 0.5
time.sleep(2)

print("Stopping motor.")
kit.motor1.throttle = 0