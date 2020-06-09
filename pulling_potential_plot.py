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

plt.scatter(time, force, s = 2)
plt.show()
