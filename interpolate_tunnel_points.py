from generate_pmf_configs_from_tunnel import *

def get_interpolated_positions(p1, p2):
    return (p1 + p2) / 2

def generate_interpolated_configs(tunnel_points, intervals, structure_pdb, prefix_filename):
    """
    function that interpolates between intervals of tunnel positions and generate pdb configs with water
    ----------------------------------------------------------------------------
    tunnel_points: ndarray
    N x 3 array of xyz positions of all tunnel points

    intervals: ndarray
    array of tuples that contains the intervals for position interpolations

    structure_pdb: string
    filename of the pdb structure that has the protein with one water

    prefix_filename: string
    prefix filename of all config files

    ----------------------------------------------------------------------------
    """
    box_data, structure_data = get_structure_data(structure_pdb)
    
    for interval in intervals:
        i = interval[1] + 0.5
        p1 = tunnel_points[interval[0]]
        p2 = tunnel_points[interval[1]]
        interp = get_interpolated_positions(p1, p2)
        new_structure = dock_one_water(interp, structure_data)
        with open(prefix_filename + "_%.1f"%i + ".pdb", 'w') as output:
            output.write(box_data)
            output.writelines(new_structure)

    pass

if __name__ == "__main__":
    input_structure = sys.argv[1]
    input_tunnel = sys.argv[2]
    output_prefix = sys.argv[3]
    intervals = np.array([(21, 22)])#(2, 3), (14, 15), (21, 22), (27, 28)
    tunnel_points = read_tunnel_pdb(input_tunnel)
    generate_interpolated_configs(tunnel_points, intervals, input_structure, output_prefix)
    
    pass