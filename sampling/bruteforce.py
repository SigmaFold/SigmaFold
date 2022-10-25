""""
Generates every possible combination of H and Ps within a matrix of size 2n where n is the size of the input sequence.
"""

import cProfile, pstats, io


def profile(fnc):
    """A decorator that uses cProfile to profile a function"""

    def inner(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return inner


# Take a list of H and Ps as input
# input_sequence = list(input("Enter the input sequence: "))
input_sequence = "HPHHHPHHPH"
print(input_sequence)

dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
visited = set()

# generate every possible path of length n going through coordinates x,y
paths = []
n = len(input_sequence)


def generate_paths(x, y, visited, path):
    if len(path) < n:
        for dir in dirs:
            new_x = x + dir[0]
            new_y = y + dir[1]
            if (new_x, new_y) not in visited:
                visited.add((new_x, new_y))
                generate_paths(new_x, new_y, visited, path + [(new_x, new_y)])
                visited.remove((new_x, new_y))
    else:
        paths.append(path)


generate_paths(0, 0, visited, [])
print("Total Possible Paths ====  > ", len(paths))

# map each element in each path to the corresponding element in the input sequence
paths = [list(zip(path, input_sequence)) for path in paths]
print("Valid paths are ====> ", paths)


# plot all points in path

# Define densitu as the number of neighbours between points within a path. sum 1 for each neighbour
def get_neighbours(x, y):
    neighbours = []
    # create list of directions with diagonals
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    for dir in dirs:
        new_x = x + dir[0]
        new_y = y + dir[1]
        neighbours.append((new_x, new_y))
    return neighbours


# sum all neighbours where second element of tuple is H
def get_energy(path):
    energy = 0
    for point in path:
        print(point)
        if point[1] == 'H':
            for neighbour in get_neighbours(point[0][0], point[0][1]):
                index = path.index((neighbour, 'H')) if (neighbour, 'H') in path else -1
                if index != -1:
                    energy -= 1

    return energy


# add energies to paths
paths = [(get_energy(path), path) for path in paths]
print("Paths with energies ====> ", paths)

# isolate all paths with minimum energy
min_energy = min([path[0] for path in paths])
print("Minimum energy is ====> ", min_energy)
min_energy_paths = [path for path in paths if path[0] == min_energy]
# print("Minimum energy paths are ====> ", min_energy_paths)

# Plot all paths with minimum energy
# Plot Hs and Ps in a different colour
# Plot all paths with minimum energy in a different plot

import matplotlib.pyplot as plt


# plot in a different colour if H or P
def plot_path(path):
    # use np.where




for path in min_energy_paths:
    plot_path(path[1])


#
# # print(densities)
# max_density = max(densities)
#
# import matplotlib.pyplot as plt
#
# # if density is greater or equal to 5 plot
# for path in paths:
#     if path[0] == max_density:
#         x = [coordinate[0] for coordinate in path[1:]]
#         y = [coordinate[1] for coordinate in path[1:]]
#         plt.scatter(x, y)
#         plt.plot(x, y)
#         plt.show()
