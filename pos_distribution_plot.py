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
xvg_file = open(sys.argv[1], 'r')
lines = xvg_file.readlines()

# initial position of atom
#first_entry = lines[1].split()
#init_position_str = np.array([first_entry[1], first_entry[2], first_entry[3]])
#init_position = init_position_str.astype(np.float)

# data arrays for analysis
x_arr = []
y_arr = []
z_arr = []

for line in lines:
    line_entry = line.split()
    # skip comments
    first_charactor = line_entry[0]
    if first_charactor[0] != '#' and first_charactor[0] != '@':
        # read data
        x_arr.append(line_entry[1])
        y_arr.append(line_entry[2])
        z_arr.append(line_entry[3])

# numpy array of frames
frames_str = np.array(x_arr, y_arr, z_arr)
frames = frames_str.astype(np.float)
# convert to Angstroms
frames = frames * 10

# plotting
#fig, ax = plt.subplots(1, 3, sharey = True, sharex = True, figsize=(10,6))
#bins = 50
#fig.suptitle("atom movement distribution in three directions")
# common_xlabel = "deviation from initial position [Å]"
# fig.text(0.5, 0.04, common_xlabel, ha='center')
# distribution of dx
#ax[0].set(ylabel = "Frequency")
#plot_one_dist(ax[0], bins, "x", dx_arr, 0, save = False)
# distribution of dy
#plot_one_dist(ax[1], bins, "y", dy_arr, 0, save = False)
# distribution of dz
#plot_one_dist(ax[2], bins, "z", dz_arr, 0, save = False)

#plt.show()
