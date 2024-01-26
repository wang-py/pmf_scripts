import numpy as np
import matplotlib.pyplot as plt
import sys
from removal_energy_plot import plot_one_dist
from gromacs_energy_plot import get_energy_from_xvg

def get_total_kinetic_energy(translational, rotational):
    total_kinetic_energy = rotational + translational
    return total_kinetic_energy

if __name__ == "__main__":
    translational_xvg = sys.argv[1]
    rotational_xvg = sys.argv[2]

    translational_energies = get_energy_from_xvg(translational_xvg)
    rotational_energies = get_energy_from_xvg(rotational_xvg)
    total_kinetic_energies = get_total_kinetic_energy(translational_energies, rotational_energies)

    fig, ax = plt.subplots()
    bins = 40
    plot_one_dist(ax, bins, "total kinetic energy", total_kinetic_energies, bestfit=False, save=False)
    plt.show()

    pass