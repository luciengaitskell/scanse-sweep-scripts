"""A Python3 script to live plot the data from the Scanse Sweep sensor, with a fixed distance limit on graph."""

from sweeppy import Sweep
import matplotlib.pyplot as plt
import math
import os

DEV = os.environ['SCANSE_SWEEP_PORT']


# Create figure:
fig1 = plt.figure(1)

# Clear figure:
plt.clf()

# Enable interactive mode:
plt.ion()

# Create polar subplot:
sbp = plt.subplot(111, projection='polar')

# Create axis:
ax = fig1.add_axes(sbp)

# Set radius limit:
ax.set_ylim(0, 600)


if __name__ == "__main__":
    with Sweep(DEV) as sweep:
        speed = sweep.get_motor_speed()
        rate = sweep.get_sample_rate()

        print('Motor Speed: {} Hz'.format(speed))
        print('Sample Rate: {} Hz'.format(rate))

        # Starts scanning as soon as the motor is ready
        sweep.start_scanning()

        # Initial plot:
        sct, = plt.plot([], [], lw=1, marker='+')

        # Get next scan, using 'get_scans()', which is a generator
        for scan in sweep.get_scans():
            # Create angle and distance lists:
            angles = []
            distances = []
            for smp in scan.samples:
                angles.append((smp.angle/1000)*(math.pi/180))
                distances.append(smp.distance)

            # Update plot data:
            sct.set_xdata(angles)
            sct.set_ydata(distances)

            # Draw new plot:
            plt.draw()

            # Pause for plot update:
            plt.pause(0.1)
