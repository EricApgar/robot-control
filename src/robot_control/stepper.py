'''
Class for stepper motor.
'''
from dataclasses import dataclass
import time
from typing import Literal

import board
import busio
import adafruit_as5600
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper


@dataclass
class Limits:
    cw: int
    ccw: int
    midpoint: int


@dataclass(frozen=True)
class Constants:
    STEPS_PER_REV: int = 3200  # Microsteps per revolution in MICROSTEP mode.
    RPM: float = 10.0
    STEP_DELAY: float = 60.0 / (RPM * STEPS_PER_REV)
    TOLERANCE_DEGREES: float = 0.5  # Stop stepping when within this many degrees of target.

    # Steps taken between sensor checks during limit sweep. Each step is ~0.11 degrees,
    # so 20 steps = ~2.25 degrees of commanded motion per check.
    LIMIT_STEPS_PER_CHECK = 20
    # If the sensor moves less than this over LIMIT_STEPS_PER_CHECK steps, we're at a limit.
    LIMIT_MOVEMENT_THRESHOLD = 0.2


class Stepper:

    def __init__(self):
        
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.kit = MotorKit(i2c=self.i2c)
        self.sensor = adafruit_as5600.AS5600(i2c=self.i2c)

        self.limits = None

        self.cw = stepper.FORWARD
        self.ccw = stepper.BACKWARD


    def zero(self):
        '''
        Sweep CW and CCW to find limits. Set Limits.
        '''

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
        return


    def flip(self):
        '''
        Internally flips cw and ccw so that you can set this once for a motor
        and not have to keep track of which motor needs to be always cw and which
        needs to be ccw if the motors are oriented differently.
        '''

        if self.cw == stepper.FORWARD:
            self.cw == stepper.BACKWARD
            self.ccw == stepper.FORWARD
        else:
            self.cw == stepper.FORWARD
            self.ccw == stepper.BACKWARD

        return


    def turn_to(self, direction: Literal['cw', 'ccw']='cw', percent: float=0.0):
        '''
        Since angle measurements are not necessarily a standard degree,
        all desired positions should be passed in as the percent of the full range
        of motion capable in either the cw or ccw direction. i.e., turn 100% to cw
        means turn the cw limit. This avoids the user needing to know units.
        '''

        return


    def turn_by(self, direction: Literal['cw', 'ccw']='cw', revolutions: float=0.0):
        '''
        On the off chance that a sensor is not available or not used, turn the motor
        by telling it to turn in fractions or multiples of a revolution.
        '''

        return