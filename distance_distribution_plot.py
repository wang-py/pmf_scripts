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
