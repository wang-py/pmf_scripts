from pkgutil import get_data
import sys
import os
from glob import glob
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import mpl_axes_aligner

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

def get_avg_displacement(input_data):
    deviation = get_avg_deviation(input_data)
    displacement = np.linalg.norm(deviation)
    return displacement

def get_avg_position(input_data):
    return np.mean(input_data, axis=0)

def get_std_displacement(input_data):
    p0 = input_data[0, :]
    deviations = input_data - p0
    displacements = [np.linalg.norm(x) for x in deviations]
    std = np.std(displacements)

    return std

def get_displacement_and_std_vs_site(input_xvgs):
    num_of_pts = len(input_xvgs)
    displacement_vs_site = np.zeros(num_of_pts)
    std_vs_site = np.zeros(num_of_pts)
    for i in range(num_of_pts):
        data = get_data_from_xvg(input_xvgs[i])
        displacement_vs_site[i] = get_avg_displacement(data)
        std_vs_site[i] = get_std_displacement(data)

    return displacement_vs_site, std_vs_site

def get_reaction_coordinate(input_xvgs):
    coord = np.zeros(len(input_xvgs))
    disp_i = 0
    for i in range(1, len(input_xvgs)):
        pos_i = get_avg_position(get_data_from_xvg(input_xvgs[i]))
        pos_prev = get_avg_position(get_data_from_xvg(input_xvgs[i-1]))
        disp_i += np.linalg.norm(pos_i - pos_prev)
        coord[i] = disp_i
    
    return coord

def get_force(delta_pos, force_constant):
    return -delta_pos * force_constant

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
        data_next = get_data_from_xvg(input_xvgs[i+1])
        mean_deviation = get_avg_deviation(data)
        mean_deviation_next = get_avg_deviation(data_next)
        force = get_force(mean_deviation, k)
        force_next = get_force(mean_deviation_next, k)
        avg_force = (force + force_next) / 2
        # evaluate work at new equilibrium
        p1 = tunnel_points[i] + mean_deviation
        p2 = tunnel_points[i+1] + mean_deviation_next
        vector = get_vector(p1, p2)
        work = get_work(avg_force, vector)
        work_vs_site[i+1] = work
    
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

def get_site_numbering_from_xvgs(input_xvgs):
    site_number = []
    for xvg in input_xvgs:
        number = xvg.split('_')[4]
        site_number.append(number)

    return site_number

def sort_files_by_number(input):
    return float(input.split('_')[4])

def sort_energy_files_by_number(input):
    return float(input.split('_')[5])

def plot_average_displacement_vs_site(input_xvgs):
    displacement_vs_site, std_vs_site = get_displacement_and_std_vs_site(input_xvgs)
    sites = np.arange(1, len(displacement_vs_site) + 1)
    plt.plot(sites, displacement_vs_site, 'o')
    plt.errorbar(sites, displacement_vs_site, yerr=std_vs_site, capsize=3, ls='none', label="errorbar") 
    plt.xlabel("site number")
    plt.ylabel("average displacement [A]")
    plt.title("average displacement vs. site number")
    plt.legend()
    plt.show()
    pass

def plot_average_energy_vs_site(energy_vs_site, react_coord, site_number):
    fig, ax1 = plt.subplots()
    plt.suptitle("energy along the reaction coordinate")
    ax1.set_xlabel("reaction coordinate [A]")
    ax1.set_ylabel("energy [kJ/mol]")
    ax1.axhline(-42, color='k', linestyle='--', label='energy of water in bulk -42 kJ/mol')
    ax1.vlines(react_coord, 0, 1, transform=ax1.get_xaxis_transform(), linestyles='solid', linewidth=1, color='k')
    ax1.set_xticks(react_coord)
    ax1.set_xticklabels(react_coord)
    ax1.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f'))
    ax1.tick_params(axis='x', labelsize=8)
    ax2 = ax1.secondary_xaxis('top')
    ax2.set_xticks(react_coord)
    ax2.set_xticklabels(site_number)
    ax2.set_xlabel("site number")
    plt.setp(ax1.get_xticklabels(), rotation=45, horizontalalignment='right')
    ax1.plot(react_coord, energy_vs_site, 'bo-', label='gromacs energy')
    ax1.legend()
    plt.show()
    pass

def pdb_to_tunnel_points_radii(tunnel_pdb):
    """
    a function that parses the tunnel profiles pdb. 
    This function outputs an array of coordinates and sizes.
    ---------------------------------------------------------------------------
    tunnel_pdb: str
    filename of the tunnel profile pdb

    ----------------------------------------------------------------------------
    Returns:
    tunnel_points: ndarray
    n x 1 numpy array of tunnel point radii in Angstroms

    """
    # read in the pdb file
    tunnel_points_radii = []
    pdb_file = open(tunnel_pdb)
    pdb_file = [line for line in pdb_file if 'ATOM' in line]
    for line in pdb_file:
        line_arr = line.split()
        # read in the b-factor(radius)
        radius = float(line_arr[10])
        tunnel_points_radii.append(radius)

    return np.array(tunnel_points_radii)

def plot_radii_energy_vs_site(radii_vs_site, energy_vs_site, react_coord, react_coord_caver, site_number):
    fig, ax1 = plt.subplots()
    plt.suptitle("energy along the reaction coordinate")
    ax1.set_xlabel("reaction coordinate [A]")
    ax1.set_ylabel("energy [kJ/mol]")
    ax1.axhline(-42, color='k', linestyle='--', label='energy of water in bulk -42 kJ/mol')
    ax1.vlines(react_coord, 0, 1, transform=ax1.get_xaxis_transform(), linestyles='solid', linewidth=1, color='k')
    ax1.set_xticks(react_coord)
    ax1.set_xticklabels(react_coord)
    ax1.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f'))
    ax1.tick_params(axis='x', labelsize=8)
    plot_1 = ax1.plot(react_coord, energy_vs_site, 'bo-', label='gromacs energy')
    ax2 = ax1.secondary_xaxis('top')
    ax2.set_xticks(react_coord)
    ax2.set_xticklabels(site_number)
    ax2.set_xlabel("site number")
    ax3 = ax1.twinx()
    plot_2 = ax3.plot(react_coord_caver, radii_vs_site, 'ro-', label='caver radii')
    ax3.set_ylabel("caver radii [A]")
    mpl_axes_aligner.align.yaxes(ax1, -42, ax3, 1.4)
    plt.setp(ax1.get_xticklabels(), rotation=45, horizontalalignment='right')
    lns = plot_1 + plot_2
    labels = [l.get_label() for l in lns]
    plt.legend(lns, labels, loc=0)
    plt.show()
    pass

def plot_work_and_total_work(work_vs_site, react_coord):
    total_work = get_total_work_vs_site(work_vs_site)
    #site_number = np.arange(work_vs_site.shape[0])+1
    fig, ax = plt.subplots(2, 1, sharex=True)
    plt.suptitle("Work done along the path")
    ax[0].plot(react_coord, work_vs_site, 'o')
    ax[0].set_ylabel("Work (FdS) [kJ/mol]", fontsize=10)
    ax[1].plot(react_coord, total_work, 'o-')
    ax[1].set_ylabel("Total work [kJ/mol]", fontsize=10)
    ax[1].set_xlabel("reaction coordinate [A]", fontsize=10)

    plt.show()

def plot_work_and_energy(work_vs_site, energy_vs_site, react_coord, k):
    total_work = get_total_work_vs_site(work_vs_site)
    shift = total_work[0] - energy_vs_site[0]
    total_work -= shift
    site_number = np.arange(total_work.shape[0]) + 1
    fontsize=12
    fig, ax1 = plt.subplots()
    plt.suptitle("Work and energy at k=%.1f kJ/mol/A^2"%k)
    ax1.set_xlabel("reaction coordinate [A]")
    ax1.set_ylabel("energy and work [kJ/mol]")
    ax1.axhline(-42, color='k', linestyle='--', label='energy of water in bulk -42 kJ/mol')
    ax1.vlines(react_coord, 0, 1, transform=ax1.get_xaxis_transform(), linestyles='solid', linewidth=1, color='k')
    ax1.set_xticks(react_coord)
    ax1.set_xticklabels(react_coord)
    ax1.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f'))
    ax1.tick_params(axis='x', labelsize=8)
    ax2 = ax1.secondary_xaxis('top')
    ax2.set_xticks(react_coord)
    ax2.set_xticklabels(site_number)
    ax2.set_xlabel("site number")
    plt.setp(ax1.get_xticklabels(), rotation=45, horizontalalignment='right')
    ax1.plot(react_coord, total_work, 'ro-',label='total work')
    ax1.plot(react_coord, energy_vs_site, 'bo-', label='gromacs energy')
    ax1.legend()
    plt.show()