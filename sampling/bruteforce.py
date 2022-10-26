""""
Generates every possible combination of H and Ps within a matrix of size 2n where n is the size of the input sequence.
"""

import cProfile, pstats, io
import pprint

import pandas as pd
import tabulate


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


# print("Valid paths are ====> ", paths)


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
    for idx, point in enumerate(path):
        if point[1] == 'H':
            for neighbour in get_neighbours(point[0][0], point[0][1]):
                index = path.index((neighbour, 'H')) if (neighbour, 'H') in path else -1
                if index != -1 and index not in range(idx - 1, idx + 2):
                    energy -= 1

    return energy/2 # divide by 2 to avoid double counting


# add energies to paths
paths = [(get_energy(path), path) for path in paths]
# print("Paths with energies ====> ", paths)

# isolate all paths with minimum energy
min_energy = min([path[0] for path in paths])
print("Minimum energy is ====> ", min_energy)
min_energy_paths = [path for path in paths if path[0] == min_energy]

# join all paths into dataframe
df = pd.DataFrame(paths, columns=['Energy', 'Path'])
df = df.sort_values(by='Energy', ascending=True)
# print(tabulate.tabulate(df, headers='keys', tablefmt='psql'))

# TODO : SUPER TIME CONSUMING
# iterate through all paths with min E in df and plot them
df_min_e = df.loc[df['Energy'] == min_energy]
# print(tabulate.tabulate(df_min_e, headers='keys', tablefmt='psql'))

# size of df
print("Size of df is ====> ", df_min_e.shape)


import matplotlib.pyplot as plt

# convert all paths to dataframes


def plot_path(path):
    df = pd.DataFrame(path)
    # Annotate H and Ps in the plot
    for i, row in df.iterrows():
        if row[1] == 'H':
            plt.annotate(row[1], (row[0][0], row[0][1]), color='red')
            #plot points
            plt.scatter(row[0][0], row[0][1], color='red')
            #trace lines between points
            if i > 0:
                plt.plot([df.iloc[i-1][0][0], row[0][0]], [df.iloc[i-1][0][1], row[0][1]], color='dimgray')

        else:
            plt.annotate(row[1], (row[0][0], row[0][1]), color='blue')
            #plot points
            plt.scatter(row[0][0], row[0][1], color='blue')

            #trace lines between points
            if i > 0:
                plt.plot([df.iloc[i-1][0][0], row[0][0]], [df.iloc[i-1][0][1], row[0][1]], color='dimgray')

    df.columns = ['Point', 'Element']


    plt.show()


# plot all paths with min energy
for path in df_min_e['Path']:
    plot_path(path)
