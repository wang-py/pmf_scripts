import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from glob import glob
from removal_energy_plot import plot_one_dist, get_initial_cluster_energy
from gromacs_energy_plot import get_energy_from_xvg

def get_total_kinetic_energy(translational, rotational):
    total_kinetic_energy = rotational + translational
    return total_kinetic_energy

def get_potential_energy(energy_file):
    """
    function that gets potential energies from input xvgs
    output is in kJ/mol
    """
    energy = get_energy_from_xvg(energy_file)
    #coulomb = energy[:, 3]
    #LJ = energy[:, 4]
    #avg_total_energy = np.mean(coulomb)
    #avg_total_energy = np.mean(LJ)
    total_energies = energy[:,0] + energy[:,1]

    return total_energies

def get_cluster_potential_energy(energy_file):
    """
    function that gets potential energies from input xvgs
    output is in kJ/mol
    """
    energy = get_energy_from_xvg(energy_file)
    #coulomb = energy[:, 3]
    #LJ = energy[:, 4]
    #avg_total_energy = np.mean(coulomb)
    #avg_total_energy = np.mean(LJ)
    protein_water = energy[:, 0] + energy[:,1]
    water_water = energy[:,2] + energy[:,3]
    total_energies = protein_water + water_water

    return total_energies

def get_restraint_energy(energy_file):
    """
    function that gets restraint energies from input xvgs
    output is in kJ/mol
    """
    energy = get_energy_from_xvg(energy_file)
    #coulomb = energy[:, 3]
    #LJ = energy[:, 4]
    #avg_total_energy = np.mean(coulomb)
    #avg_total_energy = np.mean(LJ)
    restraint_energies = energy[:, 4] 

    return restraint_energies

def get_total_energy(energy_files):
    """
    function that gets individual average energies from input xvgs
    output is in kJ/mol
    """
    num_of_pts = len(energy_files)
    total_energies = 0
    for i in range(num_of_pts):
        total_energies += get_energy_from_xvg(energy_files[i])

    return total_energies

if __name__ == "__main__":
    input_path = sys.argv[1]
    gmx_potential_energy_file = sys.argv[2]
    if len(sys.argv) > 2:
        output_fig_filename = sys.argv[3]
    else:
        output_fig_filename = "output_fig"
    translational_xvgs = sorted(glob(input_path + "/*trans_energy.xvg"), key=os.path.getmtime)
    rotational_xvgs = sorted(glob(input_path + "/*rot_energy.xvg"), key=os.path.getmtime)

    #total_potential_energies = get_cluster_potential_energy(gmx_potential_energy_file)
    total_potential_energies = get_potential_energy(gmx_potential_energy_file)
    #total_restraint_energies = get_restraint_energy(gmx_potential_energy_file)
    translational_energies = get_total_energy(translational_xvgs)
    rotational_energies = get_total_energy(rotational_xvgs)
    total_kinetic_energies = get_total_kinetic_energy(translational_energies, rotational_energies)

    #total_potential_and_restraint = total_potential_energies + total_restraint_energies
    #total_energies = total_potential_and_restraint + total_kinetic_energies[:, 0] 
    total_energies = total_potential_energies + total_kinetic_energies[:, 0] 

    fig, ax = plt.subplots(3, 1,figsize=(8, 10))
    bins = 40
    plot_one_dist(ax[0], bins, "total potential energy", total_potential_energies, bestfit=True, save=False)
    plot_one_dist(ax[1], bins, "total kinetic energy", total_kinetic_energies, bestfit=True, save=False)
    total_energy_std = plot_one_dist(ax[2], bins, "total energy", total_energies, bestfit=True, save=False)[1]
    print(f"Standard deviation of total energy is {total_energy_std} kJ/mol")
    plt.savefig(output_fig_filename + '.png', dpi=200)
    plt.show()

    pass