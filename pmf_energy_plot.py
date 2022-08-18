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

def get_data_from_xvg(input_xvg):
    with open(input_xvg, 'r') as xvg:
        data_str = [line.split()[1:] for line in xvg if '#' not in line and '@' not in line]
    
    data = np.array(data_str).astype(float) * 10

    return data

def get_avg_deviation(input_arr):
    p0 = input_arr[0, :]
    deviations = input_arr - p0
    mean_deviation = np.zeros(3)
    
    mean_deviation[0] = np.mean(deviations[:, 0])
    mean_deviation[1] = np.mean(deviations[:, 1])
    mean_deviation[2] = np.mean(deviations[:, 2])

    return mean_deviation

def get_force(delta_pos, force_constant):
    return delta_pos * force_constant

def get_vector(point_A, point_B):
    return point_B - point_A

def get_work(force, path):
    return np.dot(force, path)

def get_work_vs_site(tunnel_points, input_xvgs, k):
    number_of_sites = len(input_xvgs)
    total_work = []
    current_work = 0
    for i in range(number_of_sites - 1):
        data = get_data_from_xvg(input_xvgs[i])
        mean_deviation = get_avg_deviation(data)
        force = get_force(mean_deviation, k)
        vector = get_vector(tunnel_points[i], tunnel_points[i+1])
        work = get_work(force, vector)
        current_work += work
        total_work.append(total_work)
    
    return total_work


def get_average_energy(input_xvg, k):
    data = get_data_from_xvg(input_xvg)
    
    mean_deviation = get_avg_deviation(data)
    mean_energy = (mean_deviation[0] ** 2 + mean_deviation[1] ** 2 + mean_deviation[2] ** 2) * k / 2

    return mean_energy

def plot_average_energy_vs_site(input_xvgs, k):
    mean_energy = []
    for xvg in input_xvgs:
        mean_energy.append(get_average_energy(xvg,k))

    site_number = np.arange(1, len(mean_energy)+1)
    plt.scatter(site_number, mean_energy)
    plt.title("average energy vs. dowser prediction sites")
    plt.xlabel("site number")
    plt.ylabel("average energy [kJ/mol]")
    plt.show()
    pass

if __name__ == '__main__':
    path = sys.argv[1]
    force_constant = sys.argv[2]
    pos_files = sorted(glob(path + "/*_water.xvg"), key=os.path.getmtime)
    pass