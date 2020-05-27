# this script is used for plotting the distribution of the position of a chosen
# atom
# Author: Panyue Wang (pywang@ucdavis.edu)

import numpy as np
import matplotlib.pyplot as plt
import sys

# read file from command line
coor_buffer_file = sys.argv[1]

coor_buffer = open(coor_buffer_file)
