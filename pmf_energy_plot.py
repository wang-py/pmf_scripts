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
    pos_files = sorted(glob(path + "/*_water.xvg"), key=os.path.getmtime)
    #pos_files = [file for file in pos_files if 'adjusted' not in file]
    #ls_args = ('ls', '-1', '-v', energy_path)
    #ls_with_numerical = subprocess.Popen(ls_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #energy_files = ls_with_numerical.communicate()[0]
    energy_files = sorted(glob(energy_path + "/*_energy.xvg"), key=os.path.getmtime)
    #energy_files = [file for file in energy_files if 'adjusted' not in file]
    energies = get_energy_vs_site(energy_files)
    tunnel_points = read_tunnel_pdb(tunnel_pdb)
    work_vs_site = get_work_vs_site(tunnel_points, pos_files, force_constant)
    react_coord = get_reaction_coordinate(pos_files)
    plot_work_and_energy(work_vs_site, energies, react_coord, force_constant)
    plot_work_and_total_work(work_vs_site, react_coord)
    #force_vs_site = get_force_vs_site(tunnel_points, pos_files, force_constant)
    pass