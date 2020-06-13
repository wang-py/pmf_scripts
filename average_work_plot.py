# this script is used for plotting the pulling potential along the trajectory
# Author: Panyue Wang (pywang@ucdavis.edu)

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
from pulling_potential_plot import *

xvg_folder = sys.argv[1]

directory = os.fsencode(xvg_folder)

for file in os.scandir(directory):
     filename = os.fsdecode(file)
     # only reads xvgs
     if filename.endswith(".xvg"): 
         one_xvg = os.path.join(xvg_folder, filename)
