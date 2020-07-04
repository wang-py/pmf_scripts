# this script is used for plotting the pulling potential along the trajectory
# Author: Panyue Wang (pywang@ucdavis.edu)

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
from pulling_potential_plot import *

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

    return time, N, work, move_mean

def get_average_search_work(work_runs, force_runs):
    # array for all search work
    search_work_arr = []
    for one_run, mean_force in zip(work_runs, force_runs):
        index, one_run_search_work = find_end_of_search(mean_force, one_run)
        search_work_arr.append(one_run_search_work)

    average_search_work = np.mean(search_work_arr)
    return average_search_work

def get_average_search_work_from_file(search_work_file):
    search_work = open(search_work_file, 'r')
    lines = search_work.readlines()
    
    search_arr = []
    for line in lines:
        if line[0] != '.':
            search_arr.append(float(line))

    average_search_work = np.mean(search_arr)

    return average_search_work


def get_jarzynski_work(work_runs):
    R = 8.314 #J/K/mol
    T = 310 #K
    RT = R * T / 1000 #convert RT to kJ/mol
    work_runs_exp = []
    for one_run in work_runs:
        one_run_exp = np.exp(-one_run / RT)
        work_runs_exp.append(one_run_exp)

    mean_work_runs_exp = np.mean(work_runs_exp, axis=0)
    jarzynski_work = np.log(mean_work_runs_exp) * -RT

    return jarzynski_work

# plotting function
# time: array of time steps
# N: moving average window
# runs: number of runs
# mean_work: average work calculated using standard averaging
# jarzynski_work: average work calculated using Jarzynski equation
# save_figure: option to save figure as a PDF

def plot_average_work(time, N, runs, mean_work, jarzynski_work, \
                      mean_search_work, plot_search_work, save_figure=False):
    # pull force and pulling work
    fig, ax = plt.subplots(2, 1, sharex=True, figsize=(9.5,10))
    fig.suptitle("average work, " + fig_title) 
    
    # mean work
    ax[0].plot(time[N-1:-N], mean_work[N-1:-N], \
               label = "average work over " + str(runs) + " runs")
    ax[0].set(ylabel = "Work [kJ/mol]")

    # option to not plot search work
    if plot_search_work:
        ax[0].hlines(mean_search_work, xmin=0, xmax=time[-1], \
                     label = "average first passage work = " + \
                     f"{mean_search_work:.0f}" + " kJ/mol", \
                     color='k', linestyle='--')
    ax[0].legend(loc = 'best')
    
    # Jayzynsky mean work
    ax[1].plot(time[N-1:-N], jarzynski_work[N-1:-N], \
               label = "Jarzynski average work over " + str(runs) + " runs")
    ax[1].set(ylabel = "Work [kJ/mol]")
    ax[1].set(xlabel = "time [ps]")
    ax[1].legend(loc = 'best')

    # option to save figure
    if save_figure:
        plt.savefig(fig_title+".jpg", dpi=200)
        plt.savefig(fig_title+".png")
    else:
        plt.show()

if __name__ == "__main__":
    # folder that contains all xvgs
    xvg_folder = sys.argv[1]

    # pulling rate
    velocity = float(sys.argv[2])
    
    # option to plot search work
    plot_search_work = bool(int(sys.argv[3]))

    # file that contains all search work
    search_work_file = sys.argv[4]

    # customize title
    if len(sys.argv) > 5:
        fig_title = sys.argv[5]
    else:
        fig_title = ""
    
    directory = os.fsencode(xvg_folder)

    # data structure that contains all runs
    work_runs = []
    
    # data structure that contains all forces
    force_runs = []
    
    
    for file in os.scandir(directory):
        filename = os.fsdecode(file)
         # only reads xvgs
        if filename.endswith(".xvg"): 
            one_time, N, one_work, force = get_one_work(filename, velocity)
            work_runs.append(one_work)
            force_runs.append(force)
    
    num_of_runs = len(work_runs)
    # standard mean work
    mean_work = np.mean(work_runs, axis=0)
    jarzynski_work = get_jarzynski_work(work_runs)
    average_search_work = get_average_search_work_from_file(search_work_file)
    plot_average_work(one_time, N, num_of_runs, mean_work, jarzynski_work, \
                      average_search_work, plot_search_work, save_figure=True)
