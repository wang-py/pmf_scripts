# this script is used for plotting the distribution of the position of a chosen
# atom
# Author: Panyue Wang (pywang@ucdavis.edu)

import numpy as np
import matplotlib.pyplot as plt
import sys
from color_histogram import *

def find_position_deviation(p0, pn):
    dx = pn[0] - p0[0]
    dy = pn[1] - p0[1]
    dz = pn[2] - p0[2]
    return dx, dy, dz

# read file from command line
coor_buffer_file = sys.argv[1]

coor_buffer = open(coor_buffer_file, 'r')
lines = coor_buffer.readlines()

# initial position of atom
first_entry = lines[1].split()
init_position_str = np.array([first_entry[5], first_entry[6], first_entry[7]])
init_position = init_position_str.astype(np.float)

# data arrays for analysis
dx_arr = []
dy_arr = []
dz_arr = []

for line in lines:
    line_entry = line.split()
    # skip frame index
    if line_entry[0] != "frame":
        # process data
        curr_position_str = np.array([line_entry[5], \
        line_entry[6], line_entry[7]])
        curr_position = curr_position_str.astype(np.float)
        # find deviations in three dimensions
        dx, dy, dz = find_position_deviation(init_position, curr_position)
        dx_arr.append(dx)
        dy_arr.append(dy)
        dz_arr.append(dz)

# plotting
fig, ax = plt.subplots(1, 3, sharey = True, sharex = True, figsize=(10,6))
bins = 8
fig.suptitle("atom movement distribution in three directions")
common_xlabel = "deviation from initial position [Å]"
fig.text(0.5, 0.04, common_xlabel, ha='center')
# distribution of dx
ax[0].set(ylabel = "Frequency")
plot_one_dist(ax[0], bins, dx_arr, 0, False)
# distribution of dy
plot_one_dist(ax[1], bins, dy_arr, 0, False)
# distribution of dz
plot_one_dist(ax[2], bins, dz_arr, 0, False)

plt.show()
