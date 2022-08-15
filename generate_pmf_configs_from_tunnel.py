# script that reads the tunnel profile and docks water molecules at each tunnel point
import sys
import os
import glob

# function that reads the tunnel pdb file and return an array of positions
def read_tunnel_pdb(tunnel_pdb):
    with open(tunnel_pdb, 'r') as tpdb:
        tunnel_data = [line for line in tpdb.readlines() if 'ATOM' in line]
    pass

# function that takes the tunnel positions and docks water in the input structure
def dock_one_water(tunnel_point, structure_pdb_data):
    

    pass

# function that iterate through all tunnel positions and generate pdb configs with water
def generate_configs(tunnel_pos, structure_pdb):
    with open(structure_pdb, 'r') as spdb:
        data = [line for line in spdb.readlines() if 'ATOM' in line]
    pass

if __name__ == "__main__":
    input_structure = sys.argv[1]
    input_tunnel = sys.argv[2]

    pass