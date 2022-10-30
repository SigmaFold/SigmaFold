""""
Generates every possible combination of H and Ps within a matrix of size 2n where n is the size of the input sequence.
"""

import matplotlib.pyplot as plt
from rules import bond_rules
import numpy as np

origin = (0, 0)
dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
dirs_full = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1),
             (1, -1)]  # right, down, left, up + all the diagonals
visited = set()  # locations that have been visited


def generate_paths(x, y, visited, path, paths, n, sequence):
    """Recursive function
    """
    if len(path) < n:
        # ensures (0, 0) is teh starting point of the path
        if origin not in path:
            path.append(origin)
            visited.add(origin)
        # adds a new node in every direction unless there is already an existing node in that direction
        for dir in dirs:
            new_x = x + dir[0]
            new_y = y + dir[1]
            if (new_x, new_y) not in visited:
                visited.add((new_x, new_y))
                generate_paths(new_x, new_y, visited, path + [(new_x, new_y)], paths, n,
                               sequence)  # Change in the data structure!
                visited.remove((new_x, new_y))
    # path is complete
    else:
        paths.append(path)


def get_neighbours(x, y):
    """Finds all the neighbours of a certain node in the sequence"""
    neighbours = []
    # create list of directions with diagonals
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1),
            (1, -1)]  # right, down, left, up + all the diagonals

    for dir in dirs:  # adds all the neighbours into a list
        new_x = x + dir[0]
        new_y = y + dir[1]
        neighbours.append((new_x, new_y))
    return neighbours


def get_energy(path, sequence):
    """Finds the free energy in the lattice"""
    energy = 0
    for node in path:
        node_index = path.index(node)
        for dir in dirs:
            cur_x = node[0] + dir[0]
            cur_y = node[1] + dir[1]
            if (cur_x, cur_y) in path:
                neighbour_index = path.index((cur_x, cur_y))
                if abs(neighbour_index - node_index) != 1:  # check if neighbour is the subsequent amino acid
                    # convert the relationship between the two nodes into a string and verify the free energy with
                    # the rules stated in rules.py
                    bond = f'{sequence[node_index]}-{sequence[neighbour_index]}'
                    energy += bond_rules[bond]
    return energy / 2  # divided by 2 because the neighbours count twice


def handle_sequence(sequence):
    stable_paths = []
    paths = []
    n = len(sequence)
    generate_paths(0, 0, visited, [], paths, n, list(sequence))  # generates all the paths for the sequence
    # print("Total Possible Paths ====  > ", len(paths))

    energy_list = []
    # Gets the free energy for every path generated and appends it to energy_list
    for path in paths:
        cur_energy = (get_energy(path, sequence))
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


# if density is greater or equal to 5 plot
# for path in paths:
#     print(path)
#     if path[0] == max_density:
#         x = [coordinate[0] for coordinate in path[1:][1]]
#         y = [coordinate[1] for coordinate in path[1:][1]]
#         print(x, y)
#         plt.scatter(x, y)
#         plt.plot(x, y)
#         plt.show()


if __name__ == '__main__':
    energy = handle_sequence("HPPHPPHPHH")
