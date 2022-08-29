# script that calculates energy from average drift and plots it.
from pmf_functions import *
from generate_pmf_configs_from_tunnel import read_tunnel_pdb

if __name__ == '__main__':
    # working directory that contains all xvgs
    path = sys.argv[1]
    # pdb for tunnel points
    tunnel_pdb = sys.argv[2]
    # force constant in kJ/mol/A^2
    force_constant = float(sys.argv[3])
    pos_files = sorted(glob(path + "/*_water.xvg"), key=os.path.getmtime)
    tunnel_points = read_tunnel_pdb(tunnel_pdb)
    work_vs_site = get_work_vs_site(tunnel_points, pos_files, force_constant)
    plot_work_and_total_work(work_vs_site)
    force_vs_site = get_force_vs_site(tunnel_points, pos_files, force_constant)
    pass