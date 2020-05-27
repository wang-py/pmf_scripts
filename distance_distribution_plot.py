# this script is used for plotting the distribution of the distance a chosen
# atom moves from its initial position
# Author: Panyue Wang (pywang@ucdavis.edu)

import numpy as np
import matplotlib.pyplot as plt
import sys
from color_histogram import *

# read file from command line
coor_buffer_file = sys.argv[1]

coor_buffer = open(coor_buffer_file, 'r')
lines = coor_buffer.readlines()
