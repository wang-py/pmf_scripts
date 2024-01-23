from gromacs_energy_plot import *
import matplotlib.colors as colors

def plot_one_dist(ax, bins, this_xlabel, distribution, save = False):

    # get standard deviation of the distribution's
    distribution_std = np.std(distribution)
    distribution_std_str = f"{distribution_std:.2f}"

    # get mean of distribution
    distribution_mean = np.mean(distribution)
    distribution_mean_str = f"{distribution_mean:.2f}"

    # plotting distribution distribution
    #ax.set(title = 'Distribution of movement in one direction')
    if this_xlabel:
        ax.set(xlabel = this_xlabel + ' deviation from fixed point [kJ/mol]')
    #ax.set(ylabel = 'Frequency')

    # crystal structure line
    ax.axvline(distribution_mean, color = 'k', linestyle = '--', \
    label = 'mean = ' + distribution_mean_str + ' kJ/mol')

    # standard deviation
    ax.plot([], [], ' ', \
    label = 'standard deviation = ' + distribution_std_str + ' kJ/mol')

    # histogram with colors
    N, bin_min, patches = ax.hist(distribution, bins, density = True)
    fracs = N / N.max()
    norm = colors.Normalize(fracs.min(), fracs.max())
    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)

    # best fit line
    y = ((1 / (np.sqrt(2 * np.pi) * distribution_std)) * \
         np.exp(-0.5 * (1 / distribution_std * (bin_min - distribution_mean))**2))
    ax.plot(bin_min, y, '-', color = 'r', label = 'best fit')

    ax.legend(loc = 'best')
    if save:
        plt.savefig(this_xlabel+".png", dpi=200)
    # return the plot object
    return distribution_mean

def get_initial_cluster_energy(cluster_energy_xvg):
    """
    function that gets average energy of water cluster from input xvg
    """
    energy = get_energy_from_xvg(cluster_energy_xvg)
    #coulomb = energy[:, 3]
    #LJ = energy[:, 4]
    #avg_total_energy = np.mean(coulomb)
    #avg_total_energy = np.mean(LJ)
    #coulomb = energy[:, [0,2]]
    #LJ = energy[:, [1,3]]
    total_energy = np.sum(energy, axis=1)
    fig, ax = plt.subplots()
    plot_one_dist(ax, 30, this_xlabel=None, distribution=total_energy, save=False)
    avg_total_energy = np.mean(total_energy)
    return avg_total_energy

def get_removal_energy_and_std(cluster_energy_xvg, minus_one_energy_files):
    num_of_pts = len(minus_one_energy_files)
    removal_energies = np.zeros(num_of_pts)
    std_removal_energies = np.zeros(num_of_pts)
    site_number = np.zeros(num_of_pts)
    cluster_energy = np.mean(np.sum(get_energy_from_xvg(cluster_energy_xvg), axis=1))
    #cluster_energy = np.sum(get_energy_from_xvg(cluster_energy_xvg), axis=1)
    var_cluster_energy = np.var(np.sum(get_energy_from_xvg(cluster_energy_xvg), axis=1))
    std_cluster_energy = np.std(np.sum(get_energy_from_xvg(cluster_energy_xvg), axis=1))
    print(f"variance and std of initial cluster energy: {var_cluster_energy}, {std_cluster_energy}")
    for i in range(num_of_pts):
        site_number[i] = get_site_number_from_energy_file(minus_one_energy_files[i])
        minus_one_energy = np.mean(np.sum(get_energy_from_xvg(minus_one_energy_files[i]), axis=1))
        #minus_one_energy = np.sum(get_energy_from_xvg(minus_one_energy_files[i]), axis=1)
        var_minus_one_energy = np.var(np.sum(get_energy_from_xvg(minus_one_energy_files[i]), axis=1))
        std_minus_one_energy = np.std(np.sum(get_energy_from_xvg(minus_one_energy_files[i]), axis=1))
        print(f"variance and std of minus {i+1} cluster: {var_minus_one_energy}, {std_minus_one_energy}")
        energy_diff = cluster_energy - minus_one_energy
        removal_energy = energy_diff
        #removal_energy = np.mean(energy_diff)
        std_removal_energy = np.sqrt(var_cluster_energy + var_minus_one_energy) # - 2*std_cluster_energy*std_minus_one_energy)
        #std_removal_energy = np.std(energy_diff)
        removal_energies[i] = removal_energy
        std_removal_energies[i] = std_removal_energy

    return removal_energies, std_removal_energies, site_number

def get_minus_one_energy_vs_site(energy_files):
    """
    function that gets individual average energies from input xvgs
    """
    num_of_pts = len(energy_files)
    total_energies = np.zeros(num_of_pts)
    site_number = np.zeros(num_of_pts)
    for i in range(num_of_pts):
        energy = get_energy_from_xvg(energy_files[i])
        site_number[i] = get_site_number_from_energy_file(energy_files[i])
        avg_total_energy = np.mean(np.sum(energy, axis=1))
        total_energies[i] = avg_total_energy

    return total_energies, site_number

def plot_removal_energy_vs_site(removal_energies, gmx_energies, sites, output_filename, std_removal_energies, std_gmx_energies, dowser_energies):
    cal_to_joules = 4.1868
    label_fontsize=16
    fig, ax = plt.subplots(figsize=(14,9))

    removal_energies = removal_energies / cal_to_joules
    std_removal_energies /= cal_to_joules
    gmx_energies /= cal_to_joules
    std_gmx_energies /= cal_to_joules

    plt.plot(sites, removal_energies, 'g^', label='removal', markersize=10)
    plt.plot(sites, gmx_energies, 'b^', label='gromacs potential', markersize=10)
    plt.errorbar(sites, gmx_energies, std_gmx_energies, capsize=10, linestyle='none', fmt='b', label='std gromacs')
    plt.errorbar(sites, removal_energies, std_removal_energies, capsize=10, linestyle='none', fmt='g', label='std removal')

    sites_and_removal_energy = np.zeros((len(sites),2))
    for i in range(len(sites)):
        sites_and_removal_energy[i] = [int(sites[i]), removal_energies[i]]
    # printing energy values
    print("Sites and removal energies: ")
    print(sites_and_removal_energy)
    energy_threshold = -10 #kCal/mol
    print(f"water with energies higher than {energy_threshold} kCal/mol:")
    print(np.array([x for x in sites_and_removal_energy if x[1] > energy_threshold]))
    ax.set_xticks(sites)
    ax.tick_params(axis='x', labelsize=label_fontsize)
    ax.tick_params(axis='y', labelsize=label_fontsize)
    if dowser_energies.any():
        plt.plot(sites, dowser_energies, 'rv', label='dowser', markersize=10)
    #plt.title("total energy vs site number", fontsize=label_fontsize)
    bulk_energy = -42 / cal_to_joules
    plt.axhline(bulk_energy, color='k', linestyle='--', label='energy of water in bulk %.1f kCal/mol'%bulk_energy)
    plt.xlabel("site number", fontsize=label_fontsize)
    plt.ylabel("energy [kCal/mol]", fontsize=label_fontsize)
    plt.legend(loc="best")
    plt.savefig(output_filename+".png", dpi=200)
    plt.show()
    pass

if __name__ == '__main__':
    cluster_energy_xvg = sys.argv[1]
    minus_one_energy_path = sys.argv[2]
    gmx_potential_energy_file = sys.argv[3]
    if len(sys.argv) > 4:
        output_fig_filename = sys.argv[4]
    else:
        output_fig_filename = "output_fig"
    minus_one_energy_files = sorted(glob(minus_one_energy_path + "/*_energy.xvg"), key=os.path.getmtime)
    dowser_energy_file = "dowser_energies.txt"
    initial_cluster_energy = get_initial_cluster_energy(cluster_energy_xvg)
    print(f"the initial cluster energy is {initial_cluster_energy} kJ/mol")
    removal_energies, std_removal_energies, sites = get_removal_energy_and_std(cluster_energy_xvg, minus_one_energy_files)
    dowser_energies= get_dowser_energies(dowser_energy_file)
    gmx_potential_energy, gmx_std = get_gmx_energies(gmx_potential_energy_file)
    plot_removal_energy_vs_site(removal_energies, gmx_potential_energy, sites, output_fig_filename, std_removal_energies, gmx_std, dowser_energies)
    pass