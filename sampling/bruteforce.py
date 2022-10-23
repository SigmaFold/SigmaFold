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
input_sequence = list(input("Enter the input sequence: "))
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


# plot all points in path

# Define densitu as the number of neighbours between points within a path. sum 1 for each neighbour
def get_neighbours(x, y):
    neighbours = []
    # create list of directions with diagonals
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]  # right, down, left, up
    for dir in dirs:
        new_x = x + dir[0]
        new_y = y + dir[1]
        neighbours.append((new_x, new_y))
    return neighbours


for path in paths:
    density = 0
    for coordinate in path:
        neighbours = get_neighbours(coordinate[0], coordinate[1])
        for neighbour in neighbours:
            if neighbour in path:
                density += 1
    path.insert(0, density)

densities = [path[0] for path in paths]

# print(densities)
max_density = max(densities)

import matplotlib.pyplot as plt

# if density is greater or equal to 5 plot
for path in paths:
    if path[0] == max_density:
        x = [coordinate[0] for coordinate in path[1:]]
        y = [coordinate[1] for coordinate in path[1:]]
        plt.scatter(x, y)
        plt.plot(x, y)
        plt.show()
