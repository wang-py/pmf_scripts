import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import os
import sys

def get_energy_from_xvg(input_xvg):
    with open(input_xvg, 'r') as xvg:
        data_str = [line.split()[1:] for line in xvg if '#' not in line and '@' not in line]
    
    data = np.array(data_str).astype(float)

    return data

def get_site_number_from_energy_file(energy_file):
    filename = os.path.basename(energy_file)
    site_number = float(filename.split('_')[5])

    return site_number
    
def get_energy_vs_site(energy_files):
    """
    function that gets individual average energies from input xvgs
    """
    num_of_pts = len(energy_files)
    total_energies = np.zeros(num_of_pts)
    site_number = np.zeros(num_of_pts)
    for i in range(num_of_pts):
        energy = get_energy_from_xvg(energy_files[i])
        site_number[i] = get_site_number_from_energy_file(energy_files[i])
        coulomb = energy[:, 0]
        LJ = energy[:, 1]
        avg_total_energy = np.mean(coulomb + LJ)
        total_energies[i] = avg_total_energy

    return total_energies, site_number

def plot_energy_vs_site(total_energies, sites, dowser_energies=None):
    cal_to_joules = 4.1868
    fig, ax = plt.subplots()
    plt.plot(sites, total_energies / cal_to_joules, 'bo', label='gromacs')
    ax.set_xticks(sites)
    if dowser_energies.any():
        plt.plot(sites, dowser_energies, 'ro', label='dowser')
    plt.title("total energy vs site number")
    bulk_energy = -42 / cal_to_joules
    plt.axhline(bulk_energy, color='k', linestyle='--', label='energy of water in bulk %.1f kCal/mol'%bulk_energy)
    plt.xlabel("site number")
    plt.ylabel("energy (Coulomb + LJ) [kCal/mol]")
    plt.legend()
    plt.show()
    pass

def plot_gmx_dowser_energy_vs_site(total_energies, sites, dowser_energies, dowser_hit_stats):
    cal_to_joules = 4.1868
    fig, ax = plt.subplots()
    plt.plot(sites, total_energies / cal_to_joules, 'bo', label='gromacs')
    ax.set_xticks(sites)
    plt.plot(sites, dowser_energies, 'ro', label='dowser')
    plt.title("total energy vs site number")
    bulk_energy = -42 / cal_to_joules
    plt.axhline(bulk_energy, color='k', linestyle='--', label='energy of water in bulk %.1f kCal/mol'%bulk_energy)
    plt.xlabel("site number")
    plt.ylabel("energy (Coulomb + LJ) [kCal/mol]")
    plt.legend()
    plt.show()
    pass

def get_dowser_energies(dowser_energy_file):
    with open(dowser_energy_file, 'r') as DE:
        dowser_energies = [float(line) for line in DE.readlines()]
    return np.array(dowser_energies)

if __name__ == "__main__":
    input_path = sys.argv[1]
    energy_files = sorted(glob(input_path + "/*_energy.xvg"), key=os.path.getmtime)
    dowser_energy_file = input_path + "/dowser_energies.txt"
    energies, sites = get_energy_vs_site(energy_files)
    dowser_energies= get_dowser_energies(dowser_energy_file)
    plot_energy_vs_site(energies, sites, dowser_energies)

    pass