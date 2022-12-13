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
    
def get_energy_vs_site(energy_files):
    """
    function that gets individual average energies from input xvgs
    """
    num_of_pts = len(energy_files)
    total_energies = np.zeros(num_of_pts)
    for i in range(num_of_pts):
        energy = get_energy_from_xvg(energy_files[i])
        coulomb = energy[:, 0]
        LJ = energy[:, 1]
        avg_total_energy = np.mean(coulomb + LJ)
        total_energies[i] = avg_total_energy

    return total_energies

def plot_energy_vs_site(total_energies, dowser_energies=None):

    sites = np.arange(total_energies.shape[0]) + 1
    cal_to_joules = 4.1868
    plt.plot(sites, total_energies / cal_to_joules, 'bo', label='gromacs')
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

def get_dowser_energies(dowser_energy_file):
    with open(dowser_energy_file, 'r') as DE:
        dowser_energies = [float(line) for line in DE.readlines()]
    return np.array(dowser_energies)

if __name__ == "__main__":
    input_path = sys.argv[1]
    energy_files = sorted(glob(input_path + "/*_energy.xvg"), key=os.path.getmtime)
    dowser_energy_file = input_path + "/dowser_energies.txt"
    energies = get_energy_vs_site(energy_files)
    dowser_energies= get_dowser_energies(dowser_energy_file)
    plot_energy_vs_site(energies, dowser_energies)

    pass