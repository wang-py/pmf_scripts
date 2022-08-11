# script that calculates energy from average drift and plots it.
# TODO: 
# 1. read in all xvgs that contains the positions of the focus atom.
# 2. calculate the energy from the average deviations using the spring constant
# 3. plot the energy vs points
import sys
import os
from glob import glob
import matplotlib.pyplot as plt
import numpy as np

def get_avg_deviation(input_arr):
    p0 = input_arr[0, 1:]
    dx = []
    dy = []
    dz = []
    for i in range(len(input_arr)):
        dx, dy, dz = get_position_deviation(p0, input_arr[i, 1:])
    
    mean_dx = np.mean(dx)
    mean_dy = np.mean(dy)
    mean_dz = np.mean(dz)

    return mean_dx, mean_dy, mean_dz

def get_position_deviation(p0, pn):
    dx = pn[0] - p0[0]
    dy = pn[1] - p0[1]
    dz = pn[2] - p0[2]
    return dx, dy, dz

def get_average_energy(input_xvg, k):
    with open(input_xvg, 'r') as f:
        data = [float(line) * 10 for line in f if '@' or '#' not in line]

    mean_dx, mean_dy, mean_dz = get_avg_deviation(data)
    mean_energy = (mean_dx ** 2 + mean_dy ** 2 + mean_dz ** 2) * k

    return mean_energy

def plot_average_energy_vs_site(input_xvgs):
    mean_energy = []
    for xvg in input_xvgs:
        mean_energy.append(get_average_energy(xvg))
    pass

if __name__ == '__main__':
    path = sys.argv[1]
    pos_files = sorted(glob(path + "/*_water.xvg"), key=os.path.getmtime)
    plot_average_energy_vs_site(pos_files)
    pass