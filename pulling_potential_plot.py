# this script is used for plotting the pulling potential along the trajectory
# Author: Panyue Wang (pywang@ucdavis.edu)

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks
import sys

def read_inputs(lines):
    # data arrays for analysis
    # pulling force at each time step
    force = [] #kJ/mol/nm
    
    # time
    time = [] #ps
    
    # data entry
    for line in lines:
        line_entry = line.split()
        # skip comments
        first_charactor = line_entry[0]
        if first_charactor[0] != '#' and first_charactor[0] != '@' and len(line_entry) > 1:
            # read data
            force.append(float(line_entry[1]))
            time.append(float(line_entry[0]))
    return time, force

def get_average_force(force, N):
    # moving mean
    move_mean = np.convolve(force, np.ones((N,))/N, mode = 'same')
    # pd.Series(force).rolling(N).mean()
    return move_mean

# this function finds the time step when searching is over
def find_end_of_search(mean_force, work):
    #index = np.where(mean_force == np.amax(mean_force))[0][0]
    index = find_peaks(mean_force, height=150, width=200, distance=200)[0][-1]
    total_work = work[index]
    return index, total_work;

# this function plots a vertical dotted line to indicate the end of searching
def plot_end_of_search(bottom, time_step, work, ax, show_text=True):
    # pull indicators
    transparency = 0.7
    text_spacing = bottom * 0.02
    offset_from_indicator = 1
    if show_text:
        text = "end of search\nwork = " + f"{work:.2f}" + " kJ/mol"
    else:
        text = ""

    # time step indicator
    ax.axvline(time_step, alpha=transparency)
    ax.text(time_step + offset_from_indicator, bottom + text_spacing, text)

def calculate_work(time, move_mean, velocity):
    # time step dt, constant
    dt = time[1] - time[0] #ps
    
    # work calculation
    work_one_sum = move_mean * dt * velocity
    work = np.cumsum(work_one_sum)
    return work

def plotting(time, force, move_mean, work, N, save_figure=False):
    spacing = np.amax(work) * 0.01
    bottom = np.amin(work) + spacing
    # find the end of search
    end_of_search, search_work = find_end_of_search(move_mean, work)
    # pull force and pulling work
    fig, ax = plt.subplots(2, 1, sharex=True, figsize=(9.5,10))
    fig.suptitle("pulling force and work along the trajectory " + fig_title)
    
    # pull force
    ax[0].scatter(time, force, s = 2)
    # plotting moving mean
    ax[0].plot(time[N-1:-N], move_mean[N-1:-N], 'r', \
               label = "moving average over " + str(N*dt) + " ps")
    ax[0].set(ylabel = "Force [kJ/mol/nm]")
    # plottind end of search
    plot_end_of_search(bottom, time[end_of_search], search_work, ax[0], \
                       show_text=False)
    
    # pull work
    ax[1].scatter(time[N-1:-N], work[N-1:-N], s = 2)
    ax[1].set(ylabel = "Work [kJ/mol]")
    ax[1].set(xlabel = "time [ps]")
    # plottind end of search
    plot_end_of_search(bottom, time[end_of_search], search_work, ax[1])
    
    ax[0].legend(loc = 'best')
    # option to save figure
    if save_figure:
        plt.savefig(fig_title+".png", dpi=200)
    else:
        plt.show()

if __name__ == "__main__":
    # read file from command line
    xvg_file = open(sys.argv[1], 'r')
    lines = xvg_file.readlines()

    # option to save as png
    save_figure = bool(int(sys.argv[3]))
    
    # customize title
    if len(sys.argv) > 4:
        fig_title = sys.argv[4]
    else:
        fig_title = ""

    # pulling velocity, assumed to be constant
    velocity = float(sys.argv[2]) #nm/ps

    # reading from xvg
    time, force = read_inputs(lines)
    dt = time[1] - time[0]

    # moving mean window
    time_window = 0.1 #ns or 100 ps
    N = int(time_window / velocity / dt)
    move_mean = get_average_force(force, N)
    work = calculate_work(time, move_mean, velocity)
    plotting(time, force, move_mean, work, N, save_figure)
