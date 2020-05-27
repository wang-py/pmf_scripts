# this script is used for plotting the distribution of the position of a chosen
# atom
# Author: Panyue Wang (pywang@ucdavis.edu)

import numpy as np
import matplotlib.pyplot as plt
import sys

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
dx_arr = np.array([])
dy_arr = np.array([])
dz_arr = np.array([])

for line in lines:
    line_entry = line.split()
    # skip frame index
    if line_entry[0] != "frame":
        # process data
        curr_position_str = np.array([line_entry[5], \
        line_entry[6], line_entry[7]])
        curr_position = curr_position_str.astype(np.float)
        dx, dy, dz = find_position_deviation(init_position, curr_position)
        np.append(dx_arr, dx)
        np.append(dy_arr, dy)
        np.append(dz_arr, dz)
