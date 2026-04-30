'''
Live sweep test for Stepper + AS5600Sensor.

Sweeps the motor between MIN_DEGREES and MAX_DEGREES (absolute sensor angle,
0-360) and plots raw, degrees, and magnitude live.

Run from VS Code Remote SSH - matplotlib will display in VS Code's Plots panel.
Kill with Ctrl+C; the motor is released in the finally block.
'''
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg for SSH with X11 forwarding, or remove this
                         # line if running directly through VS Code Remote Python.
import matplotlib.pyplot as plt
import board
import busio

from robot_control.stepper import Stepper
from robot_control.as5600_sensor import AS5600Sensor

MIN_DEGREES = 10.0   # Reverse direction when sensor reads below this.
MAX_DEGREES = 60.0   # Reverse direction when sensor reads above this.
STEPS_PER_READ = 25  # Steps per batch before checking sensor and updating plot.

i2c = busio.I2C(board.SCL, board.SDA)
motor = Stepper(i2c=i2c, terminal=2)
sensor = AS5600Sensor(i2c=i2c)
motor.add_sensor(sensor)

step_counts = []
raw_vals = []
degree_vals = []
magnitude_vals = []

fig, (ax_raw, ax_deg, ax_mag) = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
fig.suptitle('Steering Sensor Live Test')

line_raw, = ax_raw.plot([], [], 'b-')
line_deg, = ax_deg.plot([], [], 'g-')
line_mag, = ax_mag.plot([], [], 'r-')

ax_raw.set_ylabel('Raw')
ax_deg.set_ylabel('Degrees')
ax_mag.set_ylabel('Magnitude')
ax_mag.set_xlabel('Step Count')

plt.tight_layout()
plt.ion()
plt.show()

step_count = 0
direction = 'cw'

try:
    while True:
        motor.step(direction=direction, count=STEPS_PER_READ, mode='d')
        step_count += STEPS_PER_READ

        reading = sensor.read()
        step_counts.append(step_count)
        raw_vals.append(reading.raw)
        degree_vals.append(reading.degrees)
        magnitude_vals.append(reading.magnitude)

        if reading.degrees >= MAX_DEGREES:
            direction = 'ccw'
        elif reading.degrees <= MIN_DEGREES:
            direction = 'cw'

        line_raw.set_data(step_counts, raw_vals)
        line_deg.set_data(step_counts, degree_vals)
        line_mag.set_data(step_counts, magnitude_vals)

        for ax in (ax_raw, ax_deg, ax_mag):
            ax.relim()
            ax.autoscale_view()

        plt.pause(0.001)

except KeyboardInterrupt:
    pass

finally:
    motor.release()
    print('Motor released.')
