# script that optimizes the tunnel points by shifting them in the direction
# of force exerted by the protein
from pmf_functions import *
from generate_pmf_configs_from_tunnel import *

def get_pdb_data(structure_pdb):
    with open(structure_pdb, 'r') as spdb:
        box_data = [line for line in spdb.readlines() if 'CRYST' in line][0]
        spdb.seek(0,0)
        structure_data = [line for line in spdb.readlines() if 'ATOM' in line]
    
    return box_data, structure_data

def get_norm_of_force_vectors(force_vs_site):
    norm = [np.linalg.norm(x) for x in force_vs_site]

    return norm

def normalize_force_vectors(force_vs_site):
    max_norm = np.max(get_norm_of_force_vectors(force_vs_site))    

    return force_vs_site / max_norm

def update_tunnel_point_position(tunnel_pdb_data, tunnel_points, force_vs_site, delta_pos):
    num_of_pts = len(tunnel_pdb_data)
    normalized_force = normalize_force_vectors(force_vs_site)
    new_tunnel_pdb_data = []
    for i in range(num_of_pts):
        one_tp = tunnel_points[i]
        one_force = normalized_force[i]
        shift = delta_pos * one_force 
        new_tp = one_tp + shift
        one_tp_string = tunnel_pdb_data[i]
        one_tp_string = update_atom_position(one_tp_string, new_tp)
        new_tunnel_pdb_data.append(one_tp_string)
    
    new_tunnel_pdb_data = np.array(new_tunnel_pdb_data).astype(str)

    return new_tunnel_pdb_data

def write_tunnel_points(tunnel_pdb_data, output_tunnel_pdb):
    with open(output_tunnel_pdb, 'w') as output:
        for line in tunnel_pdb_data:
            output.write(line)
    pass

if __name__ == "__main__":
    # working directory that contains all water position xvgs
    pos_folder = sys.argv[1]
    pos_files = sorted(glob(pos_folder + "/*_water.xvg"), key=os.path.getmtime)
    # pdb file of the tunnel points
    tunnel_pdb = sys.argv[2]
    tunnel_points = read_tunnel_pdb(tunnel_pdb)
    # force constant in kJ/mol/A^2
    k = float(sys.argv[3])
    # step size
    step_size = float(sys.argv[4])
    # output tunnel pdb filename
    output_tunnel_pdb = sys.argv[5]
    force_vs_site = get_force_vs_site(tunnel_points, pos_files, k)
    tunnel_pdb_data = get_pdb_data(tunnel_pdb)[1]
    optimized_pdb_data = update_tunnel_point_position(tunnel_pdb_data, tunnel_points, force_vs_site, step_size)
    write_tunnel_points(optimized_pdb_data, output_tunnel_pdb)
    pass
