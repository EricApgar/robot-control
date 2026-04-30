from types import SimpleNamespace

from src.robot_control.stepper import Stepper
from src.robot_control.as5600_sensor import AS5600Sensor


class Steering:

    def __init__(self,
        motor: Stepper,
        sensor: AS5600Sensor):
        
        self.motor = motor
        self.sensor: AS5600Sensor = sensor

        self.limits: SimpleNamespace = None


    def zero(self):
        '''
        is_present: bool
        strength: str
        raw: int
        degrees: int
        magnitude: float
        '''

        no_change_count = 0

        if not self.sensor.read().is_present:
            Warning('No sensor detected. Steering not possible.')
            return
        
        pre_value = self.sensor.read().magnitude

        while no_change_count < 2:
            
            self.motor.step(direction='cw', mode='m', count=5)

            post_value = self.sensor.read().magnitude

            # if change in magnitude over 3 steps is within 2, then set limit and break. 

            if 


        return