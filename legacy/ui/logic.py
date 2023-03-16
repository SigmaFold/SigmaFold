import math

import networkx as nx  # graph library
import numpy as np


def create_pathmat(testing):
    # Reformats the test matrix from a matrix of 1s and 0s to a numbered matrix
    grid_size = len(testing)
    step = 1
    for i in range(len(testing)):
        for k in range(len(testing[1])):
            if testing[i][k] == 1:
                testing[i][k] = step
                step = step + 1

    # create placeholder and test matrix
    goalshape1 = np.array([[1, 2, 3], [4, 0, 6], [7, 8, 9]])
    goalshape = np.array(testing)
    places = goalshape - 1
    choices = ["H", "P"]
    sequences = []

    # create adjacency matrix
    adjamat = np.zeros([max(np.ndarray.flatten(goalshape)), max(np.ndarray.flatten(goalshape))])
    for i in range(len(goalshape[1])):
        for j in range(len(goalshape)):
            if j < len(goalshape) - 1:
                if goalshape[j][i] > 0 and goalshape[j + 1][i] != 0:
                    adjamat[places[j + 1][i]][places[j][i]] = 1

            if j > 0:
                if goalshape[j][i] > 0 and goalshape[j - 1][i] != 0:
                    adjamat[places[j - 1][i]][places[j][i]] = 1
            if i < len(goalshape[1]) - 1:
                if goalshape[j][i] > 0 and goalshape[j][i + 1] != 0:
                    adjamat[places[j][i]][places[j][i + 1]] = 1

            if i > 0:
                if goalshape[j][i] > 0 and goalshape[j][i - 1] != 0:
                    adjamat[places[j][i]][places[j][i - 1]] = 1

    # Creates a list of possible paths
    pathlist = []
    G = nx.from_numpy_matrix(adjamat)
    for x in range(max(np.ndarray.flatten(places) + 1)):
        for y in range(max(np.ndarray.flatten(places) + 1)):
            for path in nx.all_simple_paths(G, source=x, target=y, cutoff=max(np.ndarray.flatten(goalshape))):

                if len(path) > max(np.ndarray.flatten(places)):
                    pathlist.append(path)

    # This is for accounting for any zeros in the middle within the path
    addzeros = []
    for i in range(len(np.ndarray.flatten(goalshape))):
        if np.ndarray.flatten(goalshape)[i] == 0:
            addzeros.append(i)

    # Fix path list
    for k in range(len(addzeros)):
        for j in range(len(pathlist)):
            for i in range(len(pathlist[j])):
                if addzeros[k] < pathlist[j][i] or addzeros[k] == pathlist[j][i]:
                    pathlist[j][i] = pathlist[j][i] + 1

    # Paths in matrix form
    pathmat = []
    for i in range(len(pathlist)):
        count = 0
        specpath = []
        current = pathlist[i]

        for j in range(len(pathlist[1])):
            if goalshape[math.floor(pathlist[i][j] / len(goalshape[1])), pathlist[i][j] % len(goalshape[1])] != 0:
                specpath.append(
                    [math.floor(pathlist[i][j] / len(goalshape[1])), pathlist[i][j] % len(goalshape[1]), int(j + 1)])
            else:
                count = count + 1

        pathmat.append(specpath)

    return pathmat, grid_size


def graphicchain(chains, size):
    """Changes the pathmat into a matrix where the numbers indicate the path"""
    lattice = np.ndarray.tolist(np.zeros([size, size]))
    if len(chains) > 1:
        chain = chains[0]
        for n in range(len(chain)):
            lattice[chain[n][0]][chain[n][1]] = chain[n][2]
        lattice = np.array(lattice).astype(int)
    return lattice


if __name__ == '__main__':
    testing = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    chains, size = create_pathmat(testing)
    latt = graphicchain(chains, size)
    print(latt)