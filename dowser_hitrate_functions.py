import numpy as np
import sys
import matplotlib.pyplot as plt

def dowser_water_pruning(dowser_water_pdb):
    """
    function that extracts the positions of oxygen atoms and gets rid of 
    duplicates in the input file
    ---------------------------------------------------------------------------
    dowser_water_pdb: str
    filename of the dowser water pdb
    ---------------------------------------------------------------------------
    Returns:
    dowser_water_arr: ndarray
    n x 4 array that contains the position and energy of the dowser predicted waters
    """
    with open(dowser_water_pdb, 'r') as dwp:
        data = dwp.readlines()
        data = np.array([line[32:66] for line in data if ' O ' in line]).astype(str)
        # get rid of duplicates
        data = np.unique(data)
    
    dowser_water_xyz = np.array([line[0:23].split() for line in data]).astype(float)
    dowser_water_energy = np.array([line[28:] for line in data]).astype(float)
    dowser_water_arr = []
    for i in range(len(dowser_water_energy)):
        dowser_water_arr.append(np.append(dowser_water_xyz[i], dowser_water_energy[i]))
    
    dowser_water_arr =  np.array(dowser_water_arr).astype(float)
    dowser_water_arr = dowser_water_arr[np.argsort(dowser_water_arr[:, -1])]

    return dowser_water_arr

def read_exp_water(exp_water_pdb):
    """
    reads the pdb file of experimental water and returns array of positions
    ----------------------------------------------------------------------------
    exp_water_pdb: str
    filename of experimental water pdb
    ----------------------------------------------------------------------------
    Returns:
    exp_water_arr: ndarray
    N x 3 array of experimental water positions
    """

    with open(exp_water_pdb, 'r') as ewp:
        exp_data = [line.split()[6:9] for line in ewp.readlines() if 'HETATM' in line]
    exp_data = np.array(exp_data)
    exp_water_arr = exp_data.astype(float)
    
    return exp_water_arr

def dowser_hit_index(one_dowser_water, exp_water, distance_threshold):
    distance = calculate_distance(exp_water[:, 0:3], one_dowser_water[0:3])
    hit = np.where(distance < distance_threshold)[0]
    return hit

def get_hit_stats_dowser(exp_water, dowser_water, distance_threshold):
    hit_array = []
    for one_dowser in dowser_water:
        hit_exp_water_index = dowser_hit_index(one_dowser, exp_water, distance_threshold)
        exp_water = np.delete(exp_water, hit_exp_water_index, axis=0)
        is_hit = hit_exp_water_index.any()
        hit_array.append(is_hit)
    return np.array(hit_array)

def get_hit_rate(exp_water, dowser_water, distance_threshold):
    """
    function that detects if dowser prediction matches with experimental data
    ----------------------------------------------------------------------------
    exp_water: ndarray
    array of positions of experimental water

    dowser_water: ndarray
    array of positions and energies of dowser predictions

    distance_threshold: float
    hit detection radius in angstroms
    ----------------------------------------------------------------------------
    Returns:
    hitrate: float
    The pecentage of predictions that match experimental data
    """
    hit_count = 0
    dowser_count = dowser_water.shape[0]
    for one_exp in exp_water:
        distance = calculate_distance(one_exp, dowser_water[:, 0:3])
        hit = np.where(distance < distance_threshold)[0]
        if hit:
            # remove water that's on point
            dowser_water = np.delete(dowser_water, hit, axis=0)
            # add to hit count
            hit_count += len(hit)
    print("number of hits: %d"%hit_count)
    print("total number of water predicted: %d"%dowser_count)
    hitrate = hit_count / dowser_count
    print("hit rate is %.2f"%(hitrate))

    return hitrate

def calculate_distance(exp_water, dowser_water):
    """
    function that calculated the distance between one exp water and 
    all dowser waters
    ----------------------------------------------------------------------------
    ----------------------------------------------------------------------------
    Returns:
    distance_arr: ndarray
    N x 1 array of distances between one exp water and all dowser waters
    """
    distance_arr = np.linalg.norm(dowser_water - exp_water, axis=1)
    
    return distance_arr

def plot_hitrate_vs_cutoff(hitrate, cutoff):
    plt.plot(cutoff, hitrate*100, 'o')
    plt.title("dowser hitrate vs energy cutoff")
    plt.xlabel("energy cutoff [kCal/mol]")
    plt.ylabel("hitrate [%]")
    plt.show()
    pass