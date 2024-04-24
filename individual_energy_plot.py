import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from glob import glob
from kinetic_energy_plot import plot_one_dist
from gromacs_energy_plot import get_energy_from_xvg

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
    protein_water = energy[:, 0] + energy[:,1]
    water_water = (energy[:,2] + energy[:,3]) / 2
    total_energies = protein_water + water_water

    return total_energies

if __name__ == "__main__":
    kinetic_path = sys.argv[1]
    potential_path = sys.argv[2]
    if len(sys.argv) > 3:
        output_fig_filename = sys.argv[3]
    else:
        output_fig_filename = "output_fig"
    translational_xvgs = sorted(glob(kinetic_path + "/*trans_energy.xvg"), key=os.path.getmtime)
    rotational_xvgs = sorted(glob(kinetic_path + "/*rot_energy.xvg"), key=os.path.getmtime)
    potential_xvgs = sorted(glob(potential_path + "/*_energy.xvg"), key=os.path.getmtime)

    num_of_pts = len(potential_xvgs)
    for i in range(num_of_pts):
        # find translational, rotational and potential energy
        E_tr = get_energy_from_xvg(translational_xvgs[i])
        E_rot = get_energy_from_xvg(rotational_xvgs[i])
        V = get_potential_energy(potential_xvgs[i])
        # find total energy
        data_pts = E_tr.shape[0]
        total_energy = E_tr + E_rot + V.reshape(data_pts, 1)
        fig, ax = plt.subplots(figsize=(12, 10))
        bins = 40
        total_energy_avg, total_energy_std = plot_one_dist(ax, bins, f"total energy water {i+1}", total_energy, bestfit=True, save=False)
        print("%.2f %.2f"%(total_energy_avg, total_energy_std))
        #print("Standard deviation of total energy of water %i is %.3f kJ/mol"%(i+1, total_energy_std))
        plt.savefig(output_fig_filename + f'_{i+1}.png', dpi=200)


    pass