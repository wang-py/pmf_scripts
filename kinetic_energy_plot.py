import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from glob import glob
from removal_energy_plot import plot_one_dist
from gromacs_energy_plot import get_energy_from_xvg

def get_total_kinetic_energy(translational, rotational):
    total_kinetic_energy = rotational + translational
    return total_kinetic_energy

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
    if len(sys.argv) > 2:
        output_fig_filename = sys.argv[2]
    else:
        output_fig_filename = "output_fig"
    translational_xvgs = sorted(glob(input_path + "/*trans_energy.xvg"), key=os.path.getmtime)
    rotational_xvgs = sorted(glob(input_path + "/*rot_energy.xvg"), key=os.path.getmtime)

    translational_energies = get_total_energy(translational_xvgs)[1:]
    rotational_energies = get_total_energy(rotational_xvgs)[1:]
    total_kinetic_energies = get_total_kinetic_energy(translational_energies, rotational_energies)[1:]

    fig, ax = plt.subplots(3, 1,figsize=(9, 8))
    bins = 40
    plot_one_dist(ax[0], bins, "total translational energy", translational_energies, bestfit=False, save=False)
    plot_one_dist(ax[1], bins, "total rotational energy", rotational_energies, bestfit=False, save=False)
    plot_one_dist(ax[2], bins, "total kinetic energy", total_kinetic_energies, bestfit=False, save=False)
    plt.show()

    pass