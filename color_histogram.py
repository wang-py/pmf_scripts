import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

def plot_one_dist(ax, bins, this_xlabel, distribution, crystal,\
                  starting_point = True,save = False):

    # get standard deviation of the distribution's
    distribution_std = np.std(distribution)
    distribution_std_str = f"{distribution_std:.2f}"

    # get mean of distribution
    distribution_mean = np.mean(distribution)
    distribution_mean_str = f"{distribution_mean:.2f}"

    # plotting distribution distribution
    #ax.set(title = 'Distribution of movement in one direction')
    if this_xlabel:
        ax.set(xlabel = this_xlabel + ' deviation from fixed point [Å]')
    #ax.set(ylabel = 'Frequency')

    # crystal structure line
    if starting_point:
        ax.axvline(crystal, color = 'k', linestyle = '--', \
        label = 'starting position = ' + str(crystal) + ' Å')
        # mean
        ax.plot([], [], ' ', label = 'mean = ' + distribution_mean_str + ' Å')
    else:
        ax.axvline(distribution_mean, color = 'k', linestyle = '--', \
        label = 'mean = ' + distribution_mean_str + ' Å')

    # standard deviation
    ax.plot([], [], ' ', \
    label = 'standard deviation = ' + distribution_std_str + ' Å')

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
