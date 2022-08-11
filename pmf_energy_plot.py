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
    p0 = input_arr[0, :]
    deviations = input_arr - p0
    
    mean_dx = np.mean(deviations[:, 0])
    mean_dy = np.mean(deviations[:, 1])
    mean_dz = np.mean(deviations[:, 2])

    return mean_dx, mean_dy, mean_dz

def get_average_energy(input_xvg, k):
    with open(input_xvg, 'r') as f:
        data_str = [line.split()[1:] for line in f if '#' not in line and '@' not in line]

    data = np.array(data_str)
    data = data.astype(float) * 10 #convert to angstroms
    
    mean_dx, mean_dy, mean_dz = get_avg_deviation(data)
    mean_energy = (mean_dx ** 2 + mean_dy ** 2 + mean_dz ** 2) * k

    return mean_energy

def plot_average_energy_vs_site(input_xvgs, k):
    mean_energy = []
    for xvg in input_xvgs:
        mean_energy.append(get_average_energy(xvg,k))

    site_number = np.arange(1, len(mean_energy)+1)
    plt.scatter(site_number, mean_energy)
    plt.xlabel("site number")
    plt.ylabel("average energy [kJ/mol]")
    plt.show()
    pass

if __name__ == '__main__':
    path = sys.argv[1]
    pos_files = sorted(glob(path + "/*_water.xvg"), key=os.path.getmtime)
    k = 10 # kJ/mol/A^2
    plot_average_energy_vs_site(pos_files, k)
    pass