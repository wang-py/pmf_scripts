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
    OW = np.array([water.split()[6:9] for water in structure_pdb_data if 'OW' in water]).astype(float)
    HW1 = np.array([water.split()[6:9] for water in structure_pdb_data if 'HW1' in water]).astype(float)
    HW2 = np.array([water.split()[6:9] for water in structure_pdb_data if 'HW1' in water]).astype(float)
    
    return OW, HW1, HW2

# function that takes the tunnel positions and docks water in the input structure
def dock_one_water(tunnel_point, structure_pdb_data):
    OW, HW1, HW2 = get_water_position(structure_pdb_data)
    # shift hydrogens to new positions as well
    delta_pos = tunnel_point - OW
    new_HW1 = HW1 + delta_pos 
    new_HW2 = HW2 + delta_pos 

    i = 0
    while i < len(structure_pdb_data):
        if 'OW' in structure_pdb_data[i]:
            print("found")


    pass


# function that iterate through all tunnel positions and generate pdb configs with water
def generate_configs(tunnel_points, structure_pdb):
    with open(structure_pdb, 'r') as spdb:
        structure_data = [line for line in spdb.readlines() if 'ATOM' in line]
    
    for tunnel_point in tunnel_points:
        dock_one_water(tunnel_point, structure_data)

    pass

if __name__ == "__main__":
    input_structure = sys.argv[1]
    input_tunnel = sys.argv[2]
    tunnel_points = read_tunnel_pdb(input_tunnel)
    generate_configs(tunnel_points, input_structure)

    pass