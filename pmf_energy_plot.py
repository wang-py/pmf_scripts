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
from generate_pmf_configs_from_tunnel import read_tunnel_pdb

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

def get_force_vs_site(tunnel_points, input_xvgs, k):
    number_of_sites = len(input_xvgs)
    force_vs_site = []
    for i in range(number_of_sites):
        data = get_data_from_xvg(input_xvgs[i])
        mean_deviation = get_avg_deviation(data)
        force = get_force(mean_deviation, k)
        force_vs_site.append(force)
    
    return np.array(force_vs_site)

def get_vector(point_A, point_B):
    return point_B - point_A

def get_work(force, path):
    return np.dot(force, path)

def get_work_vs_site(tunnel_points, input_xvgs, k):
    number_of_sites = len(input_xvgs)
    work_vs_site = np.zeros(number_of_sites)
    for i in range(number_of_sites - 1):
        data = get_data_from_xvg(input_xvgs[i])
        mean_deviation = get_avg_deviation(data)
        force = get_force(mean_deviation, k)
        vector = get_vector(tunnel_points[i], tunnel_points[i+1])
        work = get_work(force, vector)
        work_vs_site[i] = work
    
    return work_vs_site

def get_total_work_vs_site(work_vs_site):
    total_work = 0
    number_of_sites = len(work_vs_site)
    total_work_vs_site = np.zeros(number_of_sites)
    for i in range(number_of_sites):
        total_work += work_vs_site[i]
        total_work_vs_site[i] = total_work
    
    return total_work_vs_site

def plot_work_vs_site(total_work):
    site_number = np.arange(1, len(total_work)+1)
    plt.plot(site_number, total_work, 'o-')
    plt.title("work along the path")
    plt.xlabel("site number")
    plt.ylabel("Work done by protein[kJ/mol]")
    plt.show()
    pass

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

def plot_work_and_total_work(work_vs_site):
    total_work = get_total_work_vs_site(work_vs_site)
    site_number = np.arange(work_vs_site.shape[0])+1
    fig, ax = plt.subplots(2, 1, sharex=True)
    ax[0].plot(site_number, work_vs_site, 'o')
    ax[0].set_ylabel("Work (FdS) [kJ/mol]", fontsize=10)
    ax[1].plot(site_number, total_work, 'o-')
    ax[1].set_ylabel("Total work [kJ/mol]", fontsize=10)
    ax[1].set_xlabel("site number", fontsize=10)

    plt.show()

if __name__ == '__main__':
    # working directory that contains all xvgs
    path = sys.argv[1]
    # pdb for tunnel points
    tunnel_pdb = sys.argv[2]
    # force constant in kJ/mol/A^2
    force_constant = float(sys.argv[3])
    pos_files = sorted(glob(path + "/*_water.xvg"), key=os.path.getmtime)
    tunnel_points = read_tunnel_pdb(tunnel_pdb)
    work_vs_site = get_work_vs_site(tunnel_points, pos_files, force_constant)
    plot_work_and_total_work(work_vs_site)
    force_vs_site = get_force_vs_site(tunnel_points, pos_files, force_constant)
    pass