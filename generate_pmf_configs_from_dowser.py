# script that reads dowser water positions and puts water in the structure
import sys
import os
import numpy as np
from generate_pmf_configs_from_tunnel import *

def read_dowser_water_pdb(dowser_water_pdb):
    with open(dowser_water_pdb, 'r') as dpdb:
        dowser_data = [line.split()[6:9] for line in dpdb.readlines() if 'ATOM' in line]
    dowser_waters = []
    for i in np.arange(0, len(dowser_data), 3):
        one_dowser = dowser_data[i:i+3]
        dowser_waters.append(one_dowser)
    dowser_waters = np.array(dowser_waters)
    dowser_waters = dowser_data.astype(float)
    
    return dowser_waters

def dock_one_dowser_water(dowser_water, structure_pdb_data):
    """
    function that takes the tunnel positions and docks water in the input structure
    ----------------------------------------------------------------------------
    tunnel_point:
    structure_pdb_data:
    ----------------------------------------------------------------------------
    Returns: structure_pdb_data_new
    updated structure data with new water position
    """
    water_i = get_water_index(structure_pdb_data)
    # shift hydrogens to new positions as well
    new_water_pos = np.array([dowser_water[0], dowser_water[1], dowser_water[2]])

    structure_pdb_data_new = update_water_position(structure_pdb_data, water_i, new_water_pos)

    return structure_pdb_data_new

def generate_dowser_configs(dowser_waters, structure_pdb, prefix_filename):
    """
    function that iterates through all tunnel positions and generate pdb configs with water
    ----------------------------------------------------------------------------
    dowser_waters: ndarray
    N x 3 x 3 array of xyz positions of dowser waters

    structure_pdb: string
    filename of the pdb structure that has the protein with one water

    prefix_filename: string
    prefix filename of all config files

    ----------------------------------------------------------------------------
    """
    box_data, structure_data = get_structure_data(structure_pdb)
    i = 0
    for dowser_water in dowser_waters:
        i += 1
        new_structure = dock_one_dowser_water(dowser_water, structure_data)
        with open(prefix_filename + "_%d"%i + ".pdb", 'w') as output:
            output.write(box_data)
            output.writelines(new_structure)
    
    pass

if __name__ == "__main__":
    input_structure = sys.argv[1]
    input_dowser = sys.argv[2]
    output_prefix = sys.argv[3]
    dowser_waters = read_dowser_water_pdb(input_dowser)
    generate_dowser_configs(dowser_waters, input_structure, output_prefix)

    pass