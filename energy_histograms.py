from color_histogram import *
import sys

def get_data_from_xvg(input_xvg):
    with open(input_xvg, 'r') as xvg:
        data_str = [line.split()[1:] for line in xvg if '#' not in line and '@' not in line]
    
    data = np.array(data_str).astype(float)

    return data

def plot_one_dist(ax, bins, this_xlabel, distribution, save = False):

    # get standard deviation of the distribution's
    distribution_std = np.std(distribution)
    distribution_std_str = f"{distribution_std:.2f}"

    # get mean of distribution
    distribution_mean = np.mean(distribution)
    distribution_mean_str = f"{distribution_mean:.2f}"

    # plotting distribution 
    #ax.set(title = 'Distribution of movement in one direction')
    if this_xlabel:
        ax.set(xlabel = this_xlabel + ' energy distribution [kJ/mol]')
    #ax.set(ylabel = 'Frequency')

    # average line
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

if __name__ == "__main__":
    energy_xvg = sys.argv[1]
    xvg_data = get_data_from_xvg(energy_xvg)
    fig, ax = plt.subplots(1, 2, sharey = False, sharex = True, figsize=(14,10))
    bins = 50
    plot_one_dist(ax[0], bins, "Coulomb",xvg_data[:, 0])
    plot_one_dist(ax[1], bins, "LJ", xvg_data[:, 1])
    plt.show()
    pass
