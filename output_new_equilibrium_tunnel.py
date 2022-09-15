from optimize_tunnel_pos_by_force import *

def get_new_eq_tunnel_point(tunnel_pdb_data, pos_files):
    num_of_pts = len(tunnel_pdb_data)
    new_tunnel_pdb_data = []
    for i in range(num_of_pts):
        pos_file = pos_files[i]
        new_tp = get_avg_position(get_data_from_xvg(pos_file))
        one_tp_string = tunnel_pdb_data[i]
        one_tp_string = update_atom_position(one_tp_string, new_tp)
        new_tunnel_pdb_data.append(one_tp_string)
    
    return new_tunnel_pdb_data

if __name__ == '__main__':
    # working directory that contains all water position xvgs
    pos_folder = sys.argv[1]
    pos_files = sorted(glob(pos_folder + "/*_water.xvg"), key=os.path.getmtime)
    # pdb file of the tunnel points
    tunnel_pdb = sys.argv[2]
    tunnel_points = read_tunnel_pdb(tunnel_pdb)
    # output tunnel pdb filename
    output_tunnel_pdb = sys.argv[3]
    tunnel_pdb_data = get_pdb_data(tunnel_pdb)[1]
    equilibrated_pdb_data = get_new_eq_tunnel_point(tunnel_pdb_data, pos_files)
    write_tunnel_points(equilibrated_pdb_data, output_tunnel_pdb)
    pass