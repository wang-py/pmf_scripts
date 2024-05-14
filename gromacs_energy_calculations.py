import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import os
import sys
import re

def get_energy_from_xvg(input_xvg):
    with open(input_xvg, 'r') as xvg:
        data_str = [line.split()[1:] for line in xvg if '#' not in line and '@' not in line]
    
    data = np.array(data_str).astype(float)

    return data

def get_site_number_from_energy_file(energy_file):
    filename = os.path.basename(energy_file)
    sn = re.findall(r'\_\d+\_', filename)
    sn = str(sn[0])
    sn = sn.strip('_')
    site_number = float(sn)
    #site_number = float(filename.split('_')[5])

    return site_number
    
def get_energy_vs_site(energy_files):
    """
    function that gets individual average energies from input xvgs
    output is in kJ/mol
    """
    num_of_pts = len(energy_files)
    total_energies = np.zeros(num_of_pts)
    std_energies = np.zeros(num_of_pts)
    site_number = np.zeros(num_of_pts)
    for i in range(num_of_pts):
        energy = get_energy_from_xvg(energy_files[i])
        site_number[i] = get_site_number_from_energy_file(energy_files[i])
        #coulomb = energy[:, 3]
        #LJ = energy[:, 4]
        #avg_total_energy = np.mean(coulomb)
        #avg_total_energy = np.mean(LJ)
        coulomb = energy[:, 0] + energy[:,2]
        LJ = energy[:,1] + energy[:,3]
        avg_total_energy = np.mean(coulomb + LJ)
        std_energies[i] = np.std(LJ + coulomb)
        total_energies[i] = avg_total_energy

    return total_energies, std_energies, site_number

def write_gmx_energies_to_file(energies, std_energies, energy_filename, std_filename):
    energies.tofile(energy_filename, sep='\n')
    std_energies.tofile(std_filename, sep='\n')
    pass

if __name__ == "__main__":
    input_path = sys.argv[1]
    if len(sys.argv) > 2:
        output_filename = sys.argv[2]
    else:
        output_filename = "gmx_energies.txt"

    output_std_filename = "std_" + output_filename
    energy_files = sorted(glob(input_path + "/*_energy.xvg"), key=os.path.getmtime)
    #dowser_energy_file = "dowser_energies.txt"
    #dowser_energy_file = input_path + "/dowser_energies.txt"
    energies, std_energies, sites = get_energy_vs_site(energy_files)
    #dowser_energies= get_dowser_energies(dowser_energy_file)
    #gmx_energies = get_gmx_energies('gmx_energies_strong_restraint.txt')
    write_gmx_energies_to_file(energies, std_energies, output_filename, output_std_filename)
    pass
