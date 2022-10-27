""""
Generates every possible combination of H and Ps within a matrix of size 2n where n is the size of the input sequence.
"""

import matplotlib.pyplot as plt
from rules import bond_rules

origin = (0,0)
dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
dirs_full = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]  # right, down, left, up + all the diagonals
visited = set() # locations that have been visited

def generate_paths(x, y, visited, path, paths, n, sequence):
    """Recursive function
    """
    if len(path) < n:
        if origin not in path:
            path.append(origin)
            visited.add(origin)
        for dir in dirs:
            new_x = x + dir[0]
            new_y = y + dir[1]
            if (new_x, new_y) not in visited:
                visited.add((new_x, new_y))
                generate_paths(new_x, new_y, visited, path + [(new_x, new_y)], paths, n, sequence)  # Change in the data structure!
                visited.remove((new_x, new_y))
    else:
        paths.append(path)

def get_neighbours(x, y):
    neighbours = []
    # create list of directions with diagonals
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]  # right, down, left, up + all the diagonals
    for dir in dirs:
        new_x = x + dir[0]
        new_y = y + dir[1]
        neighbours.append((new_x, new_y))
    return neighbours

def get_energy(path, sequence):
    energy = 0
    for node in path:
        node_index = path.index(node)
        for dir in dirs:
            cur_x = node[0] + dir[0]
            cur_y = node[1] + dir[1]
            if (cur_x, cur_y) in path:
                neighbour_index = path.index((cur_x, cur_y))
                if abs(neighbour_index - node_index) != 1:
                    bond = f'{sequence[node_index]}-{sequence[neighbour_index]}'
                    energy += bond_rules[bond]
    return energy/2


def handle_sequence(sequence):
    stable_paths = []
    paths = []
    n = len(sequence)
    generate_paths(0, 0, visited, [], paths, n, list(sequence))
    # print("Total Possible Paths ====  > ", len(paths))

    energy_list = []
    for path in paths:
        cur_energy = (get_energy(path, sequence))
        energy_list.append(cur_energy)

    current_energy_min = min(energy_list)
    stability = energy_list.count(current_energy_min)

    for i in range(len(energy_list)):
        if energy_list[i] == current_energy_min:
            stable_paths.append(paths[i])

    # Stability is the number of lowest energy configuration for a given sequence
    # The lower the stability indicator, the more stable the sequence is (uhmm)
    # print(stability)
    return stability, stable_paths

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