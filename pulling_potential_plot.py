# this script is used for plotting the pulling potential along the trajectory
# Author: Panyue Wang (pywang@ucdavis.edu)

import numpy as np
import matplotlib.pyplot as plt
import sys

# read file from command line
xvg_file = open(sys.argv[1], 'r')
lines = xvg_file.readlines()

# data arrays for analysis

# pulling force at each time step
force = [] #kJ/mol/nm

# pulling velocity, assumed to be constant
velocity = 0.01 #nm/ps

# time step dt, constant
dt = 0.05 #ps

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

# pull force and pulling energy
fig, ax = plt.subplots(2, 1, sharex=True, figsize=(12,10))
fig.suptitle("pulling force and energy along the trajectory")

# pull force
ax[0].scatter(time, force, s = 2)
ax[0].set(ylabel = "Force [kJ/mol/nm]")

# pull energy
ax[1].set(ylabel = "Energy [kJ/mol]")
ax[1].set(xlabel = "time [ps]")

plt.show()
