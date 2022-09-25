# script that calculates energy from average drift and plots it.
from pmf_functions import *
from generate_pmf_configs_from_tunnel import read_tunnel_pdb
from gromacs_energy_plot import *
import subprocess

if __name__ == '__main__':
    # working directory that contains all xvgs
    path = sys.argv[1]
    energy_path = path + "/PMF_energy"
    # pdb for tunnel points
    tunnel_pdb = sys.argv[2]
    # force constant in kJ/mol/A^2
    force_constant = float(sys.argv[3])
    pos_files = sorted(glob(path + "/*_water.xvg"), key=sort_files_by_number)
    pos_files_caver = [file for file in pos_files if '.5' not in file]
    site_number = get_site_numbering_from_xvgs(pos_files)
    energy_files = sorted(glob(energy_path + "/*_energy.xvg"), key=sort_energy_files_by_number)
    #energy_files = [file for file in energy_files if 'adjusted' not in file]
    energies = get_energy_vs_site(energy_files)
    tunnel_points = read_tunnel_pdb(tunnel_pdb)
    #work_vs_site = get_work_vs_site(tunnel_points, pos_files, force_constant)
    react_coord = get_reaction_coordinate(pos_files)
    react_coord_caver = get_reaction_coordinate(pos_files_caver)
    #plot_work_and_energy(work_vs_site, energies, react_coord, force_constant)
    #plot_work_and_total_work(work_vs_site, react_coord)
    #plot_average_energy_vs_site(energies, react_coord, site_number)
    radii_vs_site = pdb_to_tunnel_points_radii(tunnel_pdb)
    plot_radii_energy_vs_site(radii_vs_site, energies, react_coord, react_coord_caver, site_number)
    #force_vs_site = get_force_vs_site(tunnel_points, pos_files, force_constant)
    pass