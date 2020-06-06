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

# customize title
fig_title = sys.argv[2]

# data arrays for analysis
x_arr = []
y_arr = []
z_arr = []

# data entry
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
frames_str = np.array([x_arr, y_arr, z_arr])
frames = frames_str.astype(np.float)
# convert to Angstroms
frames = frames * 10
frames = np.transpose(frames)
# find deviations
first_frame = frames[0, 0:]
deviations = frames - first_frame

# plotting
fig, ax = plt.subplots(1, 3, sharey = True, sharex = True, figsize=(10,6))
bins = 50
fig.suptitle("atom movement distribution in three directions " + fig_title)
# distribution of dx
ax[0].set(ylabel = "Frequency")
mean_dx = plot_one_dist(ax[0], bins, "x", deviations[:, 0], 0, save = False)
# distribution of dy
mean_dy = plot_one_dist(ax[1], bins, "y", deviations[:, 1], 0, save = False)
# distribution of dz
mean_dz = plot_one_dist(ax[2], bins, "z", deviations[:, 2], 0, save = False)

# added dr^2
dr_2 = mean_dx ** 2 + mean_dy ** 2 + mean_dz ** 2
common_xlabel = "dr^2 = " + f"{dr_2:.2f}" + " [Å^2]"
fig.text(0.5, 0.04, common_xlabel, ha='center')

plt.show()
