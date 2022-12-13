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

def plot_energy_vs_site(total_energies):
    sites = np.arange(total_energies.shape[0]) + 1
    cal_to_joules = 4.1868
    plt.plot(sites, total_energies / cal_to_joules, 'o')
    plt.title("total energy vs site number")
    bulk_energy = -42 / cal_to_joules
    plt.axhline(bulk_energy, color='k', linestyle='--', label='energy of water in bulk %.1f kCal/mol'%bulk_energy)
    plt.xlabel("site number")
    plt.ylabel("energy (Coulomb + LJ) [kCal/mol]")
    plt.legend()
    plt.show()
    pass

if __name__ == "__main__":
    input_path = sys.argv[1]
    energy_files = sorted(glob(input_path + "/*_energy.xvg"), key=os.path.getmtime)
    energies = get_energy_vs_site(energy_files)
    plot_energy_vs_site(energies)

    pass