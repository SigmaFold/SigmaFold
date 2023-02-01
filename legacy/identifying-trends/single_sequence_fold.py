""""
Super naive and outdated implementation of the folding logic. Only kept as there's quite a lot of random plotting functionality that may be useful. For updated folding logic e.g. get energy, see lib/native_fold.py.

"""

import cProfile, pstats, io
import pprint

import pandas as pd
import tabulate
import numpy as np
from math import ceil


# Take a list of H and Ps as input
# input_sequence = list(input("Enter the input sequence: "))
input_sequence = "HPHHPHHPPH"
print(input_sequence)

origin = (0, 0)
dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
visited = set()

# generate every possible path of length n going through coordinates x,y
paths = []
n = len(input_sequence)

def step_function(x):
    """Returns 1 if x > 0, 0 otherwise"""
    return 1 if x > 0 else 0


def generate_paths(path, visited):
        """Generate all possible paths of length n starting at (0, 0)"""
        if len(path) == n:
            paths.append(path)
            return

        for dir in dirs:
            new_x = path[-1][0] + dir[0]
            new_y = path[-1][1] + dir[1]
            cap_y = ceil((n/(abs(new_x)+1)) - 1) if abs(new_x) > 0 else cap_x

            if  abs(new_y) > cap_y or abs(new_x) > cap_x:
                continue
            
            elif (new_x, new_y) not in visited:
                visited.add((new_x, new_y))
                generate_paths(path + [(new_x, new_y)], visited)
                visited.remove((new_x, new_y))

 # new paths to be generated
visited.add((0, 0))
visited.add((1, 0))
cap_x = ceil(n/2) -1 

generate_paths([(0,0), (1,0)], visited)


visited_input = np.zeros((2*n, 2*n), dtype=bool)
visited_input[0, 0] = True
visited_input[1, 0] = True





# generate_paths_bis([(0, 0), (1, 0)], visited)
print("Total Possible Paths ====  > ", len(paths))

# map each element in each path to the corresponding element in the input sequence
paths_ = [list(zip(path, input_sequence)) for path in paths]


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

def get_neighbours_diagonals(x, y):
    neighbours = []
    # create list of directions with diagonals
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0), (1,1), (-1,-1),(1,-1), (-1,1) ]  # right, down, left, up
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

def get_energy_diagonals(path):
    energy = 0
    for idx, point in enumerate(path):
        if point[1] == 'H':
            for neighbour in get_neighbours_diagonals(point[0][0], point[0][1]):
                index = path.index((neighbour, 'H')) if (neighbour, 'H') in path else -1
                if index != -1 and index not in range(idx - 1, idx + 2):
                    energy -= 1

    return energy/2

# add energies to paths
paths = [(get_energy(path), path) for path in paths_]

# isolate all paths with minimum energy
min_energy = min([path[0] for path in paths])
print("Minimum energy is ====> ", min_energy)
min_energy_paths = [path for path in paths if path[0] == min_energy]
df = pd.DataFrame(paths, columns=['Energy', 'Path'])
df = df.sort_values(by='Energy', ascending=True)
# iterate through all paths with min E in df and plot them
df_min_e = df.loc[df['Energy'] == min_energy]
# size of df
print("Size of df is ====> ", df_min_e.shape)

# Do same as previous but for diagonals
paths_diagonals = [(get_energy_diagonals(path), path) for path in paths_]
min_energy_diagonals = min([path[0] for path in paths_diagonals])
print("Minimum energy is ====> ", min_energy_diagonals)
min_energy_paths_diagonals = [path for path in paths_diagonals if path[0] == min_energy_diagonals]

df_diagonals = pd.DataFrame(paths_diagonals, columns=['Energy', 'Path'])
df_diagonals = df_diagonals.sort_values(by='Energy', ascending=True)

df_min_e_diagonals = df_diagonals.loc[df_diagonals['Energy'] == min_energy_diagonals]
print("Size of df is ====> ", df_min_e_diagonals.shape)

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


# Plot the paths with minimum energy for both cases
for path in df_min_e['Path']:
    plot_path(path)
    # add title
    plt.title('Minimum Energy Paths without diagonals')


for path in df_min_e_diagonals['Path']:
    plot_path(path)
    # add title
    plt.title('Minimum Energy Paths with diagonals')




