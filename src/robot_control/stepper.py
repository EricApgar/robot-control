'''
Class for stepper motor specifically designed for working with
the "Adafruit DC and Stepper Motor HAT for Raspberry Pi".

https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/using-stepper-motors
'''
from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace
import time
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from robot_control.magnet_sensor import MagnetSensor

import board
import busio
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper


# Realistically, a user needs to be able to update these constants for their
# specific type of stepper motor that they connect to the HAT. This class is
# really a "AdafruitMotorHatStepper()" class, and so the motor details need
# to be adjustable for whatever you connect.
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
    '''
    Control a stepper motor via the Adafruit DC/Stepper Motor HAT for RPi.

    If sensor feedback is included, use it to when determining motion.
    Otherwise, do your best guess based on math.
    '''

    def __init__(self,
        i2c: busio.I2C=busio.I2C(board.SCL, board.SDA),
        terminal: int=1,  # Terminal 1 = M1/M2, Termainal 2 = M3/M4.
        ):  # Optionally use AS5600 sensor for positioning.

        if terminal == 1:
            self.motor = MotorKit(i2c=i2c).stepper1
        elif terminal == 2:
            self.motor = MotorKit(i2c=i2c).stepper2
        else:
            raise ValueError(f'Input arg "terminal" must be 1 or 2! (was {terminal})')

        self.directions = SimpleNamespace(
            cw=stepper.FORWARD,
            ccw=stepper.BACKWARD)

        self.sensor: MagnetSensor = None
        self.limits: SimpleNamespace = None  # Only set if sensor is available.


    def release(self):
        '''
        Release motor coils from holding energy. This is exposed to the user to give
        them a way to actively shut everything down if they try something and things
        aren't working and your panicking because the motor is unresponsive and just
        keeps whining and getting hotter and hotter...
        '''

        self.motor.release()

        return


    def add_sensor(self, sensor: MagnetSensor):

        self.sensor = sensor

        return


    def zero(self):
        '''
        Sweep CW and CCW to find limits. Set Limits.
        Sweep may cross reset point so deal with that.
        '''

        if not self.sensor:
            raise ValueError('Must have connected sensor! See "add_sensor()".')

        return


    def flip(self):
        '''
        Internally flips cw and ccw so that you can set this once for a motor
        and not have to keep track of which motor needs to be always cw and which
        needs to be ccw if the motors are oriented differently.
        '''

        self.directions.cw, self.directions.ccw = self.directions.ccw, self.directions.cw

        return


    def turn_to(self, direction: Literal['cw', 'ccw']='cw', percent: float=0.0):
        '''
        Since angle measurements are not necessarily a standard degree,
        all desired positions should be passed in as the percent of the full range
        of motion capable in either the cw or ccw direction. i.e., turn 100% to cw
        means turn the cw limit. This avoids the user needing to know units.
        '''

        return


    def turn_for(self, direction: Literal['cw', 'ccw']='cw', revolutions: float=0.0):
        '''
        On the off chance that a sensor is not available or not used, turn the motor
        by telling it to turn in fractions or multiples of a revolution.
        '''

        return


    def turn_by():

        return
    

    def turn(self,
        speed: float=.5,
        direction: Literal['cw', 'ccw']='cw'):
        '''
        Different ways we can turn:
        time: turn for x seconds.
        revolutions: turn for x revolutions.
            -If no sensor, calculate number of steps required for full revolution.
            -If sensor, turn until revolutions reached. First determine that that revolutions within range.
        percentage: turn x percent of total ability in a direction.
            -Sensor dependent.
            -Only valid if limits are set.
            -Ex: turn 20% (of total) ccw. O% in either direction is reset to midpoint.

        Things that influence turning:
        -Speed (as a percentage of total top speed).
        -Direction.


        Determine if you have a sensor.
        '''
        return


    def step(self,
        direction: Literal['cw', 'ccw']='cw',
        count: int=100,
        style: str='d',
        speed: float=None,
        hold: bool=False):
        '''
        Options for style:
        
        stepper.SINGLE: jerky, intermittent. doesn't work as expected.
        stepper.DOUBLE: works.
        stepper.INTERLEAVE: works.
        stepper.MICROSTEP: works - very tiny steps.
        '''


        direction = getattr(self.directions, direction)

        # if style == 's':  # NOT CURRENTLY WORKING.
        #     style = stepper.SINGLE
        if style == 'd':
            style = stepper.DOUBLE
        elif style == 'i':
            style = stepper.INTERLEAVE
        elif style == 'm':
            style = stepper.MICROSTEP
        else:
            raise ValueError('Unsupported style.')

        for _ in range(count):
            self.motor.onestep(direction=direction, style=style)

        if not hold:
            self.motor.release()

        return

