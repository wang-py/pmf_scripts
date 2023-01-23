from dowser_hitrate_functions import *
from gromacs_energy_plot import *
if __name__ == "__main__":
    input_path = sys.argv[1]
    dowser_water_pdb = sys.argv[2]
    exp_water_pdb = sys.argv[3]
    energy_files = sorted(glob(input_path + "/*_energy.xvg"), key=os.path.getmtime)
    dowser_energy_file = input_path + "/dowser_energies.txt"
    energies, sites = get_energy_vs_site(energy_files)
    dowser_energies= get_dowser_energies(dowser_energy_file)
    # hit stats calculation
    dowser_water_arr = dowser_water_pruning(dowser_water_pdb)
    exp_water_arr = read_exp_water(exp_water_pdb)
    threshold = 1.4
    dowser_hit_stats = get_hit_stats_dowser(exp_water_arr, dowser_water_arr, threshold)
    plot_energy_vs_site(energies, sites, dowser_energies)