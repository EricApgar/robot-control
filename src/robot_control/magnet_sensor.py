from dataclasses import dataclass
import time

import busio
import board
import adafruit_as5600


@dataclass
class SensorValues:
    is_present: bool
    strength: str
    raw: int
    degrees: int
    magnitude: float


class MagnetSensor:
    '''
    Class for working with Adafruit AS5600 magnetic orientation sensor.
    '''

    def __init__(self, i2c: busio.I2C=busio.I2C(board.SCL, board.SDA)):
        
        self.sensor = adafruit_as5600.AS5600(i2c=i2c)


    def read(self):

        FULL_COUNT_12_BIT = 4096
        DEGREES_IN_CIRCLE = 360

        if self.sensor.magnet_detected:
            is_present = True
        else:
            is_present = False

        if self.sensor.min_gain_overflow:
            strength = "high"
        elif self.sensor.max_gain_overflow:
            strength = "low"
        else:
            strength = "optimal"

        raw = self.sensor.raw_angle
        degrees = raw * DEGREES_IN_CIRCLE / FULL_COUNT_12_BIT
        magnitude = self.sensor.magnitude

        output = SensorValues(
            is_present=is_present,
            strength=strength,
            raw=raw,
            degrees=degrees,
            magnitude=magnitude)

        return output


    def show(self):

        print("Magnet Status: ")
        print("Raw Angle:     ")
        print("Scaled Angle:  ")
        print("Magnitude:     ")

        while True:

            status = self.read()

            lines = [
                f"Magnet Status: {status.is_present}",
                f"Raw Angle:     {status.raw}",
                f"Scaled Angle:  {status.degrees:.2f}°",
                f"Magnitude:     {status.magnitude}"]

            # Move cursor up 4 lines, then overwrite each line
            print("\033[4A", end="")
            for line in lines:
                print(f"\r{line}\033[K")

            time.sleep(0.1)

        return