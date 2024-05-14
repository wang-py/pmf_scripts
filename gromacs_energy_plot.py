import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import re


def get_energy_from_xvg(input_xvg):
    with open(input_xvg, 'r') as xvg:
        data_str = [line.split()[1:] for line in xvg
                    if '#' not in line and '@' not in line]
    data = np.array(data_str).astype(float)

    return data


def get_site_number_from_energy_file(energy_file):
    filename = os.path.basename(energy_file)
    sn = re.findall('\_\d+\_', filename)
    sn = str(sn[0])
    sn = sn.strip('_')
    site_number = float(sn)
    # site_number = float(filename.split('_')[5])

    return site_number


def get_energy_vs_site(energy_input):
    """
    function that gets individual average energies from input xvgs
    output is in kJ/mol
    """
    total_energies = np.fromfile(energy_input, dtype=float, sep='\n')
    std_energies = np.fromfile("std_" + energy_input, dtype=float, sep='\n')
    num_of_pts = len(total_energies)
    site_number = np.arange(num_of_pts) + 1

    return total_energies, std_energies, site_number


def plot_energy_vs_site(total_energies, sites, output_filename, std_energies=None, dowser_energies=None):
    cal_to_joules = 4.1868
    label_fontsize = 16
    fig, ax = plt.subplots(figsize=(14, 7))
    total_energies_in_cal = total_energies / cal_to_joules
    plt.plot(sites, total_energies_in_cal, 'b^', label='gromacs', markersize=10)
    if std_energies.any():
        std_energies /= cal_to_joules  # convert to kCal
        # plt.errorbar(sites, total_energies_in_cal, std_energies, fmt='b', capsize=10, linestyle='', label='std gromacs')
    sites_and_gmx_energy = np.zeros((len(sites),2))
    for i in range(len(sites)):
        sites_and_gmx_energy[i] = [int(sites[i]), total_energies_in_cal[i]]
    # printing energy values
    print("Sites and gromacs energies: ")
    print(sites_and_gmx_energy)
    # energy_threshold = -7 #kCal/mol
    # print(f"water with energies higher than {energy_threshold} kCal/mol:")
    # print(np.array([x for x in sites_and_gmx_energy if x[1] > energy_threshold]))
    ax.set_xticks(sites)
    ax.tick_params(axis='x', labelsize=label_fontsize)
    ax.tick_params(axis='y', labelsize=label_fontsize)
    if dowser_energies.any():
        plt.plot(sites, dowser_energies, 'rv', label='dowser', markersize=10)
    # plt.title("total energy vs site number", fontsize=label_fontsize)
    bulk_energy = -42 / cal_to_joules
    plt.axhline(bulk_energy, color='k', linestyle='--', label='energy of water in bulk %.1f kCal/mol'%bulk_energy)
    plt.xlabel("site number", fontsize=label_fontsize)
    plt.ylabel("energy [kCal/mol]", fontsize=label_fontsize)
    plt.legend(loc="best")
    plt.savefig(output_filename+".png", dpi=200)
    plt.show()
    pass


def plot_gmx_energies_vs_site(total_energies1, total_energies2, sites, output_filename):
    cal_to_joules = 4.1868
    label_fontsize = 16
    fig, ax = plt.subplots(figsize=(14,7))
    total_energies1_in_cal = total_energies1 / cal_to_joules
    plt.plot(sites, total_energies1_in_cal, 'r^', label='gromacs k=5 kJ/mol', markersize=10)
    plt.plot(sites, total_energies2, 'bv', label='gromacs k=75 kJ/mol', markersize=10)
    sites_and_gmx_energy = np.zeros((len(sites),2))
    for i in range(len(sites)):
        sites_and_gmx_energy[i] = [int(sites[i]), total_energies1_in_cal[i]]
    # printing energy values
    print("Sites and gromacs energies: ")
    print(sites_and_gmx_energy)
    # energy_threshold = -7 #kCal/mol
    # print(f"water with energies higher than {energy_threshold} kCal/mol:")
    # print(np.array([x for x in sites_and_gmx_energy if x[1] > energy_threshold]))
    ax.set_xticks(sites)
    ax.tick_params(axis='x', labelsize=label_fontsize)
    ax.tick_params(axis='y', labelsize=label_fontsize)
    # plt.title("total energy vs site number", fontsize=label_fontsize)
    bulk_energy = -42 / cal_to_joules
    plt.axhline(bulk_energy, color='k', linestyle='--',
                label='energy of water in bulk %.1f kCal/mol' % bulk_energy)
    plt.xlabel("site number", fontsize=label_fontsize)
    plt.ylabel("energy [kCal/mol]", fontsize=label_fontsize)
    plt.legend(loc="best")
    plt.savefig(output_filename+".png", dpi=200)
    plt.show()
    pass


def plot_gmx_dowser_energy_vs_site(total_energies, sites,
                                   dowser_energies, dowser_hit_stats):
    cal_to_joules = 4.1868
    fig, ax = plt.subplots()
    plt.plot(sites, total_energies / cal_to_joules, 'bo', label='gromacs')
    ax.set_xticks(sites)
    dowser_hits = sites[dowser_hit_stats].astype(int)
    overpredictions = sites[~dowser_hit_stats].astype(int)
    plt.scatter(dowser_hits, dowser_energies[dowser_hits-1], marker='o',
                label='dowser hits', color='green')
    plt.scatter(overpredictions, dowser_energies[overpredictions-1],
                marker='o', label='dowser overpredictions', color='orange')
    plt.title("total energy vs site number")
    bulk_energy = -42 / cal_to_joules
    plt.axhline(bulk_energy, color='k', linestyle='--',
                label='energy of water in bulk %.1f kCal/mol' % bulk_energy)
    plt.xlabel("site number")
    plt.ylabel("energy (Coulomb + LJ) [kCal/mol]")
    plt.legend()
    plt.show()
    pass


def get_dowser_energies(dowser_energy_file):
    with open(dowser_energy_file, 'r') as DE:
        dowser_energies = [float(line) for line in DE.readlines()]
    return np.array(dowser_energies)


def get_gmx_energies(gmx_energy_file):
    gmx_energies = np.fromfile(gmx_energy_file, dtype=float, sep='\n')
    std_gmx_energies = np.fromfile("std_" + gmx_energy_file, dtype=float, sep='\n')
    return gmx_energies, std_gmx_energies


def write_gmx_energies_to_file(energies, std_energies):
    with open("gmx_energies.txt", 'w') as gmx_E:
        for i in range(energies.shape[0]):
            gmx_E.write(energies[i].astype(str) + ' ' + std_energies[i].astype(str)+'\n')
    pass


if __name__ == "__main__":
    energy_input = sys.argv[1]
    dowser_energy_file = sys.argv[2]
    if len(sys.argv) > 3:
        output_fig_filename = sys.argv[3]
    else:
        output_fig_filename = "output_fig"
    # dowser_energy_file = input_path + "/dowser_energies.txt"
    energies, std_energies, sites = get_energy_vs_site(energy_input)
    dowser_energies = get_dowser_energies(dowser_energy_file)
    # gmx_energies = get_gmx_energies('gmx_energies_strong_restraint.txt')
    # plot_gmx_energies_vs_site(energies, gmx_energies, sites, output_fig_filename)
    plot_energy_vs_site(energies, sites, output_fig_filename,
                        std_energies, dowser_energies)

    pass
