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

def get_one_work(one_xvg, velocity):
    one_run = open(one_xvg, 'r')
    lines = one_run.readlines()
    time, force = read_inputs(lines)
    # delta time
    dt = time[1] - time[0]

    # moving mean window
    time_window = 0.1 #ns or 100 ps
    N = int(time_window / velocity / dt)
    move_mean = get_average_force(force, N)
    work = calculate_work(time, move_mean, velocity)

    return work

# data structure that contains all runs
work_runs = np.array([])

# pulling rate
velocity = float(sys.argv[2])

for file in os.scandir(directory):
    filename = os.fsdecode(file)
     # only reads xvgs
    if filename.endswith(".xvg"): 
        one_work = get_one_work(filename, velocity)
        work_runs = np.append(work_runs, one_work)
