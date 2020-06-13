# this script is used for plotting the pulling potential along the trajectory
# Author: Panyue Wang (pywang@ucdavis.edu)

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
from pulling_potential_plot import *

xvg_folder = sys.argv[1]
# customize title
if len(sys.argv) > 3:
    fig_title = sys.argv[3]
else:
    fig_title = ""


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

    return time, N, work

def plot_average_work(time, N, mean_work, jarzynsky_work, save_figure=False):
    # pull force and pulling work
    fig, ax = plt.subplots(2, 1, sharex=True, figsize=(9.5,10))
    fig.suptitle("mean work and Jarzynsky mean work along the trajectory " + fig_title)

    runs = 20
    
    # mean work
    ax[0].plot(time[N-1:-N], mean_work[N-1:-N], \
               label = "average work over " + str(runs) + " runs")
    ax[0].set(ylabel = "Work [kJ/mol]")
    ax[0].legend(loc = 'best')
    
    # Jayzynsky mean work
    ax[1].plot(time[N-1:-N], jarzynsky_work[N-1:-N], \
               label = "Jarzynsky average work over " + str(runs) + " runs")
    ax[1].set(ylabel = "Work [kJ/mol]")
    ax[1].set(xlabel = "time [ps]")
    ax[1].legend(loc = 'best')

    # option to save figure
    if save_figure:
        plt.savefig(fig_title+".png", dpi=200)
    else:
        plt.show()


# data structure that contains all runs
work_runs = []

# pulling rate
velocity = float(sys.argv[2])

for file in os.scandir(directory):
    filename = os.fsdecode(file)
     # only reads xvgs
    if filename.endswith(".xvg"): 
        one_time, N, one_work = get_one_work(filename, velocity)
        work_runs.append(one_work)

mean_work = np.mean(work_runs, axis=0)
plot_average_work(one_time, N, mean_work, mean_work, save_figure=False)
