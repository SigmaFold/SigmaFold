"""
Provides a set a function to find and compute the energy of all possible paths with speedups where possible.
"""
import heapq
from math import ceil

import networkx as nx
import matplotlib.pyplot as plt


# from tools import profile


def step_function(x):
    """Returns 1 if x > 0, 0 otherwise"""
    return 1 if x > 0 else 0


# @profile
def fold_n(n):
    """Takes the previous n's path as input and attempts to add the next element in the sequence to the end of the path"""

    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    paths = []  # new paths to be generated
    cap_x = ceil(n / 2) - 1

    # TODO: Optimise using numpy arrays for the visited set potentially
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


# @profile
def compute_energy(paths, sequence):
    """ Match the sequence to each paths and compute the energy. Return all minimum energy structures. Stores paths in a heap.
        H-H bond = -1
        P-P bond = 0
    """

    # Create a heap to store the paths
    # TODO: Optimise to to use the odd-even contact rule
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


# Not yet in use but could be useful.
def generateWalks(n):
    """Generates a graph of all possible walks of length n starting at (0,0). numbers te entire grid"""
    G = nx.DiGraph()
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    # travel to every node in the graph and add every neighbour and direction
    for x in range(-n, n):
        for y in range(-n + abs(x), n - abs(x)):
            for dir in dirs:
                if (x + dir[0] < n and y + dir[1] < n):
                    G.add_edge((x, y), (x + dir[0], y + dir[1]), dir=dir)
                    # add edge between neighbours
    # add edge between (0,0) and (0,1)

    # nx.draw(G, with_labels=True)
    # plt.show()

    return G


def native_fold(heap, return_energy=False):
    """Returns all native folds and the degeneracy"""
    energy = heap[0][0]
    folds = []
    while heap and heap[0][0] == energy:
        folds.append(heapq.heappop(heap))

    if return_energy:
        return folds, len(folds), energy
    return folds, len(folds)


if __name__ == "__main__":
    x = 0
    y = 0
    # G = generateWalks(n)
    sequence = "PHPPHPPH"
    n = len(sequence)
    paths = fold_n(n)
    heap = compute_energy(paths, sequence)
    # pop from heap until energy changes
    energy = heap[0][0]
    # print(n)
    while heap[0][0] == energy:
        path = heapq.heappop(heap)
        # print(path)
        # plot the path
        x = [coord[0] for coord in path[1]]
        y = [coord[1] for coord in path[1]]
        # print h and p on graph
        for i in range(n):
            if sequence[i] == 'H':
                plt.text(x[i], y[i], 'H')
            else:
                plt.text(x[i], y[i], 'P')
        plt.plot(x, y, 'ro')
        plt.plot(x, y)
        plt.show()
