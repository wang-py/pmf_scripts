# this script is used for plotting the distribution of the distance a chosen
# atom moves from its initial position
# Author: Panyue Wang (pywang@ucdavis.edu)

import numpy as np
import matplotlib.pyplot as plt
import sys
from color_histogram import *

# find deviation from initial point
def find_distance_moved(p0, pn):
    dx = pn[0] - p0[0]
    dy = pn[1] - p0[1]
    dz = pn[2] - p0[2]
    distance = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
    return distance

# read file from command line
coor_buffer_file = sys.argv[1]

coor_buffer = open(coor_buffer_file, 'r')
lines = coor_buffer.readlines()

# initial position of atom
first_entry = lines[1].split()
init_position_str = np.array([first_entry[5], first_entry[6], first_entry[7]])
init_position = init_position_str.astype(np.float)

# distance travelled
dist_arr = []
for line in lines:
    line_entry = line.split()
    # skip frame index
    if line_entry[0] != "frame":
        # process data
        curr_position_str = np.array([line_entry[5], \
        line_entry[6], line_entry[7]])
        curr_position = curr_position_str.astype(np.float)
        # find deviations in three dimensions
        dist = find_distance_moved(init_position, curr_position)
        dist_arr.append(dist)

# plotting
fig, ax = plt.subplots(figsize=(10,6))
bins = 20
fig.suptitle("atom distance travelled distribution")
common_xlabel = "deviation from initial position [Å]"
fig.text(0.5, 0.04, common_xlabel, ha='center')
# distribution of distance
ax.set(ylabel = "Frequency")
plot_one_dist(ax, bins, dist_arr, 0, False, False)

plt.show()
