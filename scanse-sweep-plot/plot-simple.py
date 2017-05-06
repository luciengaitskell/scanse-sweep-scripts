"""A simple Python3 script to live scatter plot the data from the Scanse Sweep sensor."""

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
ax = plt.subplot(111, projection='polar')


if __name__ == "__main__":
    with Sweep(DEV) as sweep:
        speed = sweep.get_motor_speed()
        rate = sweep.get_sample_rate()

        print('Motor Speed: {} Hz'.format(speed))
        print('Sample Rate: {} Hz'.format(rate))

        # Starts scanning as soon as the motor is ready
        sweep.start_scanning()

        # get_scans is coroutine-based generator lazily returning scans ad infinitum
        for scan in sweep.get_scans():
            # Create angle and distance lists:
            angles = []
            distances = []
            for smp in scan.samples:
                a = (smp.angle/1000)*(math.pi/180)
                angles.append(a)
                distances.append(smp.distance)

            # Update subplot:
            ax.cla()
            ax.scatter(angles, distances, lw=2.5, marker='+')

            # Pause for plot update:
            plt.pause(0.1)
