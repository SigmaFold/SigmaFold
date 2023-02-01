""""
Generates every possible combination of H and Ps within a matrix of size 2n where n is the size of the input sequence.
# TODO: CURRENTLY BROKEN KECAUSE IT NEEDS TO BE REFACTORED TO WORK WITH THE NEW LIB AND I CBF

"""

import matplotlib.pyplot as plt
import numpy as np
from path_generator import handle_sequence, remove_duplicates

import os, sys
# this allows us to import from the lib folder which is two folders up from this one
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) # THIS WILL BREAK IF YOU MOVE FILES AROUND
from lib.native_fold import compute_energy, native_fold





def handle_sequence(sequence):
    stable_paths = []
    paths = []
    n = len(sequence)
    native_fold(0, 0, visited, [], paths, n, list(sequence))  # generates all the paths for the sequence
    # print("Total Possible Paths ====  > ", len(paths))

    energy_list = []
    # Gets the free energy for every path generated and appends it to energy_list
    for path in paths:
        cur_energy = (compite_energy (path, sequence))
        energy_list.append(cur_energy)

    # Finds the minimum free energy and finds all the stable paths with that free energy level
    current_energy_min = min(energy_list)  # Finds minimum free energy from all paths
    stability = energy_list.count(current_energy_min)  # Finds number of paths with min free energy
    for i in range(len(energy_list)):
        if energy_list[i] == current_energy_min:
            stable_paths.append(paths[i])  # All paths with min free energy

    # Stability is the number of lowest energy configuration for a given sequence
    # The lower the stability indicator, the more stable the sequence is (*to be experimentally verified*)
    # print(stability)
    return stability, stable_paths

def remove_duplicates(path_list):
    """Removes rotations and reflections from a list of paths"""
    filtered_paths = path_list.copy()

    # we will be performing path list dot product with rotation_matrix/reflection matrix.
    # Hence, the rotation matrices have already been transposed

    # Rotation matrices
    rotation_90_anticlockwise = np.array([[0, 1], [-1, 0]])
    rotation_180_anticlockwise = np.array([[-1, 0], [0, -1]])
    rotation_270_anticlockwise = np.array([[0, -1], [1, 0]])

    # Reflection matrices
    reflection_x = np.array([[1, 0], [0, -1]])
    reflection_y = np.array([[-1, 0], [0, 1]])

    # Remove reflections
    for i in range(len(path_list)):
        path_array = np.array(path_list[i])
        for other_path in path_list[i + 1:]:
            other_path_array = np.array(other_path)
            rot_90 = np.dot(other_path_array, rotation_90_anticlockwise)  # 90 degree anticlockwise rot of other_path
            rot_180 = np.dot(other_path_array, rotation_180_anticlockwise)  # 180 degree anticlockwise rot of other_path
            rot_270 = np.dot(other_path_array, rotation_270_anticlockwise)  # 270 degree anticlockwise rot of other_path
            ref_x = np.dot(other_path_array, reflection_x)
            ref_y = np.dot(other_path_array, reflection_y)
            if ((np.all(rot_90 == path_array)) or (np.all(rot_180 == path_array)) or (
                np.all(rot_270 == path_array)) or (np.all(ref_x == path_array)) or (
                np.all(ref_y == path_array))) and other_path in filtered_paths:
                filtered_paths.remove(other_path)

    return filtered_paths

