"""
Provides a set a function to find and compute the energy of all possible paths with speedups where possible.
"""
import sys
sys.path.append('c:/Users/ec_pe/OneDrive - Imperial College London/DAPP3/SigmaFold/')

import heapq
from math import ceil
import json
import matplotlib.pyplot as plt
# import permutations_helper as ph

# Brute Force Folding Functions

def fold_n(n):
    """Exhaustively enumerates all possible paths of length n  starting at (0, 0)
    
    :params
    n: the length of the path to be generated

    :returns
    paths: a list of all possible paths of length n
    """

    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    paths = []  # new paths to be generated
    cap_x = ceil(n / 2) - 1

    def generate_paths(path, visited):
        """Generate all possible paths of length n starting at (0, 0)"""
        if len(path) == n:
            paths.append(path)
            return

        for dir in dirs:
            new_x = path[-1][0] + dir[0]
            new_y = path[-1][1] + dir[1]
            cap_y = ceil((n / (abs(new_x) + 1)) - 1) if abs(new_x) > 0 else cap_x

            if abs(new_y) > cap_y or abs(new_x) > cap_x:
                continue

            elif (new_x, new_y) not in visited:
                visited.add((new_x, new_y))
                generate_paths(path + [(new_x, new_y)], visited)
                visited.remove((new_x, new_y))

    generate_paths([(0, 0), (0, 1)], {(0, 1), (0, 0)})  # start at (0, 1) to avoid double counting

    return paths


def compute_energy(paths, sequence):
    """ Match the sequence to each paths and compute the energy. Return all minimum energy structures. Stores paths in a heap.
        H-H bond = -1
        P-P bond = 0

        :param paths: list of paths that have been pre-computed by brute-force algorithm 
        :param sequence: the sequence to be folded
        :return: list of paths with minimum energy
    """

    # Create a heap to store the paths
    heap = []
    for path in paths:
        H_coords_even = []
        H_coords_odd = []
        energy = 0
        j = -1  # tracks the last time we saw an H along the chain
        for i in range(len(sequence)):
            if sequence[i] == 'H':
                # Compute the energy of interaction with any Hs before it
                curr_x, curr_y = path[i]
                if i == j + 1:  # that means that the last time we encountered an H, it was adjacent to the current H
                    if i % 2 == 0:
                        H_coords_even.append((curr_x, curr_y))
                        for coord in H_coords_odd[:-1]:  # skip last element
                            distance = abs(curr_x - coord[0]) + abs(curr_y - coord[1])  # calculate distance between 2 Hs using city block distance
                            if distance == 1:
                                energy -= 1
                    else:
                        H_coords_odd.append((curr_x, curr_y))
                        for coord in H_coords_even[:-1]:  # skip last element
                            distance = (curr_x - coord[0]) ** 2 + (
                                    curr_y - coord[1]) ** 2  # calculate distance between 2 Hs
                            if distance == 1:
                                energy -= 1

                else:
                    if i % 2 == 0:
                        H_coords_even.append((curr_x, curr_y))
                        for coord in H_coords_odd:  # skip last element
                            distance = (curr_x - coord[0]) ** 2 + (
                                    curr_y - coord[1]) ** 2  # calculate distance between 2 Hs
                            if distance == 1:
                                energy -= 1
                    else:
                        H_coords_odd.append((curr_x, curr_y))
                        for coord in H_coords_even:  # skip last element
                            distance = (curr_x - coord[0]) ** 2 + (
                                    curr_y - coord[1]) ** 2  # calculate distance between 2 Hs
                            if distance == 1:
                                energy -= 1
                j = i

        heapq.heappush(heap, (energy, path))

    return heap

def native_fold(heap, return_energy=False):
    """Returns all native folds and the degeneracy
    
    :param heap: heap of paths with minimum energy (input from compute_energy)
    :param return_energy: if True, returns the energy of the native fold
    :return: list of native folds, degeneracy, energy (if return_energy is True)
    """
    energy = heap[0][0]
    folds = []
    while heap and heap[0][0] == energy:
        folds.append(heapq.heappop(heap))

    if return_energy:
        return folds, len(folds), energy
    return folds, len(folds)

def plot_shape(path, seq):
    """Plots the shape of the path"""
    for i in range(len(seq)):
        if seq[i] == 'H':
            plt.plot(path[i][0], path[i][1], 'ro')
        else:
            plt.plot(path[i][0], path[i][1], 'bo')
    for i in range(len(seq)):
        # plot the line between the current point and the next point
        if i != len(seq) - 1:
            plt.plot([path[i][0], path[i + 1][0]], [path[i][1], path[i + 1][1]], 'k-')
    plt.axis('equal')
    plt.show()


# ========================= Executing and Saving Folds =========================
def execute_and_save_native_fold(n):
    fold = fold_n(n)
    # save the fold as a json file
    with open(f"data/folds/fold_{n}.json", "w") as f:
        json.dump(fold, f)
    
def read_fold_from_json(n):
    with open(f"data/folds/fold_{n}.json", "r") as f:
        fold = json.load(f)
    
    # convert every coordinate in the nest to tuples
    for i, path in enumerate(fold):
        fold[i] = [tuple(coord) for coord in path]

    return fold


if __name__ == "__main__":
    import time
    start = time.time()
    seq = 'PHPPPPHPHPHHHPPH'
    i = len(seq)
    paths = fold_n(i)
    # chains = ph.perm_gen(i,2)
    theheap = compute_energy(paths, seq)
    folds, numFolds = native_fold(theheap)
    # print(f"Time taken for n = {i} : {time.time() - start}")
    print(folds)
    print(numFolds)
    plot_shape(folds[0][1], seq)




