# script that reads the tunnel profile and docks water molecules at each tunnel point
import sys
import os
import numpy as np

# function that reads the tunnel pdb file and return an array of positions
def read_tunnel_pdb(tunnel_pdb):
    with open(tunnel_pdb, 'r') as tpdb:
        tunnel_data = [line.split()[6:9] for line in tpdb.readlines() if 'ATOM' in line]
    tunnel_data = np.array(tunnel_data)
    tunnel_data = tunnel_data.astype(float)
    
    return tunnel_data

# extract water position from input structure
def get_water_position(structure_pdb_data):
    OW = np.array([water.split()[6:9] for water in structure_pdb_data if 'OW' in water]).astype(float)[0]
    HW1 = np.array([water.split()[6:9] for water in structure_pdb_data if 'HW1' in water]).astype(float)[0]
    HW2 = np.array([water.split()[6:9] for water in structure_pdb_data if 'HW2' in water]).astype(float)[0]
    
    return OW, HW1, HW2

def format_atom_position(atom_pos):
    """
    takes an xyz array and formats it into pdb coordinates
    """
    x_pos = str("{0:.3f}".format(atom_pos[0])).rjust(8)
    y_pos = str("{0:.3f}".format(atom_pos[1])).rjust(8)
    z_pos = str("{0:.3f}".format(atom_pos[2])).rjust(8)
    atom_pos_pdb = x_pos + y_pos + z_pos

    return atom_pos_pdb

def update_atom_position(input_str, new_pos):
    x_i = 30
    new_pos_pdb = format_atom_position(new_pos)
    input_str = input_str.replace(input_str[x_i:x_i+24], new_pos_pdb)

    return input_str

def update_water_position(structure_pdb_data, water_i, new_water_pos):
    for i in range(3):
        structure_pdb_data[water_i+i] = update_atom_position(structure_pdb_data[water_i+i], new_water_pos[i])

    return structure_pdb_data

# function that takes the tunnel positions and docks water in the input structure
def dock_one_water(tunnel_point, structure_pdb_data):
    OW, HW1, HW2 = get_water_position(structure_pdb_data)
    # shift hydrogens to new positions as well
    delta_pos = tunnel_point - OW
    new_HW1 = HW1 + delta_pos 
    new_HW2 = HW2 + delta_pos 
    new_water_pos = np.array([tunnel_point, new_HW1, new_HW2])
    water_i = 6507

    structure_pdb_data_new = update_water_position(structure_pdb_data, water_i, new_water_pos)

    return structure_pdb_data_new

# function that iterate through all tunnel positions and generate pdb configs with water
def generate_configs(tunnel_points, structure_pdb, prefix_filename):
    with open(structure_pdb, 'r') as spdb:
        structure_data = [line for line in spdb.readlines() if 'ATOM' in line]
    
    i = 0
    for tunnel_point in tunnel_points:
        i += 1
        new_structure = dock_one_water(tunnel_point, structure_data)
        with open(prefix_filename + "_%d"%i + ".pdb", 'w') as output:
            output.writelines(new_structure)

    pass

if __name__ == "__main__":
    input_structure = sys.argv[1]
    input_tunnel = sys.argv[2]
    output_prefix = sys.argv[3]
    tunnel_points = read_tunnel_pdb(input_tunnel)
    generate_configs(tunnel_points, input_structure, output_prefix)

    pass