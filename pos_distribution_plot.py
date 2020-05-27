# this script is used for plotting the distribution of the position of a chosen
# atom
# Author: Panyue Wang (pywang@ucdavis.edu)

import numpy as np
import matplotlib.pyplot as plt
import sys

# read file from command line
coor_buffer_file = sys.argv[1]

coor_buffer = open(coor_buffer_file, 'r')
lines = coor_buffer.readlines()

for line in lines:
    line_entry = line.split()
    # skip frame index
    if line_entry[0] != "frame":
        # print coordinates
        print(line_entry[5], line_entry[6], line_entry[7])
