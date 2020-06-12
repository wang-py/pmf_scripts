# this script is used for plotting the pulling potential along the trajectory
# Author: Panyue Wang (pywang@ucdavis.edu)

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys

# read file from command line
xvg_file = open(sys.argv[1], 'r')
lines = xvg_file.readlines()

# customize title
if len(sys.argv) > 3:
    fig_title = sys.argv[3]
else:
    fig_title = ""

# data arrays for analysis

# pulling force at each time step
force = [] #kJ/mol/nm

# pulling velocity, assumed to be constant
velocity = float(sys.argv[2]) #nm/ps

# time
time = [] #ps

# data entry
for line in lines:
    line_entry = line.split()
    # skip comments
    first_charactor = line_entry[0]
    if first_charactor[0] != '#' and first_charactor[0] != '@':
        # read data
        force.append(float(line_entry[1]))
        time.append(float(line_entry[0]))

# time step dt, constant
dt = time[1] - time[0] #ps

# window
N = int(0.1 / velocity / dt)

# moving mean
move_mean = np.convolve(force, np.ones((N,))/N, mode = 'same')

# moving standard deviation
force_pd = pd.Series(force)
move_std = force_pd.rolling(N).std()

# energy calculation
energy_one_sum = move_mean * dt * velocity
energy = np.cumsum(energy_one_sum)

# pull force and pulling energy
fig, ax = plt.subplots(2, 1, sharex=True, figsize=(9.5,10))
fig.suptitle("pulling force and energy along the trajectory " + fig_title)

# pull force
ax[0].scatter(time, force, s = 2)
# plotting moving mean
ax[0].plot(time[N-1:-N], move_mean[N-1:-N], 'r', \
           label = "moving average over " + str(N*dt) + " ps")
ax[0].set(ylabel = "Force [kJ/mol/nm]")

# pull energy
ax[1].scatter(time[N-1:-N], energy[N-1:-N], s = 2)
ax[1].set(ylabel = "Work [kJ/mol]")
ax[1].set(xlabel = "time [ps]")

ax[0].legend(loc = 'best')
plt.show()
