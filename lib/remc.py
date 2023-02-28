from copy import deepcopy
import math
import random
import numpy as np
import native_fold
import pivot_moves


def HP_matrix(positions, matrix):
    '''This function takes a list of sequence positions and a matrix and returns a matrix with the positions of the list marked on the matrix in H and P.
    The positions list is a list of lists containing the amino acid, the x coordinate and the y coordinate of the amino acid.
    The format is [['H', 4, 5], ['P', 5, 5], ['H', 6, 5]]
    The numpy matrix acts as a background for the positions.'''
    graphic_matrix = matrix.copy().astype(np.int32).astype(str)
    for i in range(len(positions)):
        graphic_matrix[positions[i][1]][positions[i][2]] = positions[i][0]
    return graphic_matrix


def num_matrix(positions, matrix):
    '''This function takes a list of sequence positions and a matrix and returns a matrix with the positions of the list marked on the matrix numerically.
    The positions list is a list of lists containing the amino acid, the x coordinate and the y coordinate of the amino acid.
    The format is [['H', 4, 5], ['P', 5, 5], ['H', 6, 5]]
    The numpy matrix acts as a background for the positions.'''
    graphic_matrix = matrix.copy().astype(np.int32)
    for i in range(len(positions)):
        graphic_matrix[positions[i][1]][positions[i][2]] = i + 1
    return graphic_matrix


def positions2path(positions):
    '''This function takes a list of sequence positions and returns a list of tuple coordinates of the path and a string of the sequence residues.
    The positions list is a list of lists containing the amino acid, the x coordinate and the y coordinate of the amino acid.
    The format is [['H', 4, 5], ['P', 5, 5], ['H', 6, 5]]'''
    path = []
    seq = ''
    for i in range(len(positions)):
        path.append((positions[i][1], positions[i][2]))
        seq += positions[i][0]
    return path, seq

# generate replicas with info matrix,path,energy,temp


def genreplicalist(start_matrix, positions, number_of_things, start_temp, end_temp):
    z = []
    # Convert the positions to a path
    path, sequence = positions2path(positions)
    energy = native_fold.compute_energy([path], sequence)[
        0][0]  # Compute the energy of the path
    # generate a list of replicas with info about the matrix, path, energy, and temperature
    for i in range(number_of_things):
        # equation for temperature assignment
        tempstep = start_temp+(i)*(end_temp-start_temp)/(number_of_things-1)
        z.append([start_matrix, positions, energy, tempstep])
    return z

# Determines whether to keep the new matrix or the old matrix based on the energy difference and the temperature


def srmc(old_mat, new_mat, best_energy, possibles, temp, positionsj, positions_old):
    positions = deepcopy(positions_old)
    result = deepcopy(old_mat)
    path_old, sequence = positions2path(positions_old)
    guess_e = native_fold.compute_energy([path_old], sequence)[0][0]

    path_new, sequence = positions2path(positionsj)
    current_energy = native_fold.compute_energy([path_new], sequence)[0][0]

    # calculate differences in energy between matrices
    delt = current_energy-guess_e

    # depending on whether the new energy is better or not choose three states
    if delt > 0:
        # if new energy is closer to ground state, switch structure.
        result = new_mat
        # if the newenergy is actually the best we've seen so far. Reset best energy and degen list
        if current_energy == best_energy:
            possibles.append(result)
        if current_energy > best_energy:
            best_energy = current_energy
            possibles = [result]
        positions = deepcopy(positionsj)
        return possibles, result, best_energy, current_energy, positions

    # if the energies are equal, go with new structure
    elif delt == 0:
        # if the energy equal to best energy, add it to degeneracy list
        result = new_mat
        if current_energy == best_energy:
            possibles.append(result)
        positions = deepcopy(positionsj)

        return possibles, result, best_energy, current_energy, positions

    else:
        # if the new_mat is worse than old_mat, probabilistically switch to new_mat
        p = random.random()
        if p < math.exp(speedfactor*delt/temp):
            result = new_mat
            positions = deepcopy(positionsj)
        # possibles=[possibles]
        return possibles, result, best_energy, current_energy, positions


# generate replicalist off random sequences
def single_step(replica_list, possibles, true_best_energy, sequence):
    # do this for each replica
    for i in range(len(replica_list)):
        # save our initials
        old_mat = deepcopy(replica_list[i][0])
        old_mat_memory = deepcopy(replica_list[i][0])
        temp = replica_list[i][3]
        positions12 = deepcopy(replica_list[i][1])
        best_energy1 = true_best_energy
        n = len(sequence)
        # create a set of new matrices with a single move difference
        new_matrix, positions13 = pivot_moves.vsdh_move(sequence, n, old_mat)
        # decide whether to keep the new or old matrix based on delta energy difference
        possibles, result, best_energy, current_energy, positions15 = srmc(
            old_mat_memory, new_matrix, best_energy1, possibles, temp, positions13, positions12)
        # update the replica
        replica_list[i][0], replica_list[i][1], replica_list[i][2] = result, positions15, current_energy

        # potentially update best energy seen so far
        if current_energy > true_best_energy:
            true_best_energy = current_energy

    return replica_list, true_best_energy, possibles

# replicalist is a list of {matrix,energy,temperature}
# fix to be matrix,positions,energy,temperature


def remc(replica_list, offset):
    # offset to allow comparisons between different pairs
    i = offset + 1
    while i + 1 < len(replica_list):
        # basically compare each replica with the one next over with weighting from the temperature
        j = i + 1
        delta = (-replica_list[j][3]+replica_list[i][3]) * \
            (-replica_list[i][2]+replica_list[j][2])
        if delta < 0:
            # this means either the temoperature or energy is wrong, so we need to switch the temperatures (I chose to switch the matrices instead)
            replica_list[j][0], replica_list[i][0] = replica_list[i][0], replica_list[j][0]
            replica_list[j][1], replica_list[i][1] = replica_list[i][1], replica_list[j][1]
            replica_list[j][2], replica_list[i][2] = replica_list[i][2], replica_list[j][2]
        else:
            p = random.random()
            if p < math.exp(-delta):
                # probability of switching if actually the first is better than the second
                replica_list[j][0], replica_list[i][0] = replica_list[i][0], replica_list[j][0]
                replica_list[j][1], replica_list[i][1] = replica_list[i][1], replica_list[j][1]
                replica_list[j][2], replica_list[i][2] = replica_list[i][2], replica_list[j][2]
    # change the offset
        i += 1

    offset = 1 - offset
    return replica_list, offset


def remc_complete(positions, number_of_things, start_temp, end_temp, lattice_size, guess_true_best, offset, time):
    empty_matrix = np.zeros((lattice_size, lattice_size))
    start_matrix = num_matrix(positions, empty_matrix)
    print(f'starting matrix is {start_matrix}')
    _, sequence = positions2path(positions)

    possibles = []
    avgs = [0, 0, 0, 0, 0]
    deltatime = 0  # can change this to time step to choose number of iterations
    true_best_energy = guess_true_best

    # Generate base replicates off some guess positions
    # Generate a list of replicas
    replicates = genreplicalist(
        start_matrix, positions, number_of_things, start_temp, end_temp)
    zees = deepcopy(replicates)  # deepcopy to avoid changing the original
    iterations = 0

    while deltatime < time:
        # generate a replicalist of the size specified at the start
        # choose replicas to keep/changes to make
        zees, true_best_energy, possibles = single_step(
            zees, possibles, true_best_energy, sequence)
        print('----- NEXT ITERATION -----')
        for i in range(len(zees)):
            print(zees[i][0])
        # correct the temperature accordingly via remc
        zees, offset = remc(zees, offset)
        deltatime = deltatime + 1
        positions0 = zees[0][1]
        positions4 = zees[4][1]
        path0, _ = positions2path(positions0)
        path4, _ = positions2path(positions4)
        avgs[0] = avgs[0] + native_fold.compute_energy([path0], sequence)[0][0]
        avgs[4] = avgs[4] + native_fold.compute_energy([path4], sequence)[0][0]
        if iterations == 5:
            break
        iterations += 1
    # print("end")
    return zees, true_best_energy, possibles


if __name__ == "__main__":

    speedfactor = 2
    positions1 = [['H', 4, 5], ['H', 5, 5], ['H', 5, 4], ['H', 6, 4],
                  ['H', 6, 5], ['H', 7, 5], ['H', 7, 4], ['H', 7, 3],
                  ['P', 7, 2], ['H', 6, 2], ['H', 6, 3], ['H', 5, 3],
                  ['H', 5, 2], ['P', 4, 2], ['H', 4, 3], ['H', 4, 4]]  # List of positions
    number_of_things = 5
    start_temp = 160
    end_temp = 220
    lattice_size = 10
    guess_true_best = 0
    offset = 0
    time = 600

    replicas, true_best_energy, possibles = remc_complete(
        positions1, number_of_things, start_temp, end_temp, lattice_size, guess_true_best, offset, time)
    print(f'Replicas: {replicas}')
    print(f'True best energy: {true_best_energy}')
    print(f'Possibles: {possibles}')

    # num_mat = np.array[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                    [0, 0, 15, 16, 0, 0, 0, 0, 0, 0],
    #                    [0, 0, 14, 0, 0, 1, 0, 0, 0, 0],
    #                    [0, 12, 13, 0, 3, 2, 0, 0, 0, 0],
    #                    [0, 11, 10, 0, 4, 5, 0, 0, 0, 0],
    #                    [0, 0, 9, 8, 7, 6, 0, 0, 0, 0],
    #                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],]
    
    # # To check if pivot is working properly
    # path, seq = positions2path(positions1)
    # num_mat = num_matrix(positions1, np.zeros((10, 10)))
    # print(num_mat)
    # pivot_moves.vsdh_move(seq, len(seq), num_mat)

    # # create a test matrix of size 11X11 where the origin is at the center [5,5]
    # test_matrix = np.zeros((10, 10))  # Initialize a matrix of zeros
    # positions1 = [['H', 4, 5], ['H', 5, 5], ['H', 5, 4], ['H', 6, 4],
    #               ['H', 6, 5], ['H', 7, 5], ['H', 7, 4], ['H', 7, 3],
    #               ['P', 7, 2], ['H', 6, 2], ['H', 6, 3], ['H', 5, 3],
    #               ['H', 5, 2], ['P', 4, 2], ['H', 4, 3], ['H', 4, 4]]  # List of positions
    # # Mark the positions on the matrix in H and P
    # HP_mat = HP_matrix(positions1, test_matrix)
    # # Mark the positions on the matrix numerically
    # num_mat = num_matrix(positions1, test_matrix)
    # # print(f'HP Matrix: {HP_mat}')
    # # print(f'Numbered Matrix: {num_mat}')

    # # find the energy of the sequence in the text_matrix
    # path, seq = positions2path(positions1)  # Convert the positions to a path
    # # print(f'Path: {path}')
    # # print(f'Sequence: {seq}')
    # energy = native_fold.compute_energy([path], sequence)[
    #     0][0]  # Compute the energy of the path
    # # print(f'Energy of the path: {energy}')

    # # generate a list of replicas with info about the matrix, path, energy, and temperature
    # replica_list = genreplicalist(num_mat, positions1, 5, 160, 220)
    # print(f'Replica List: {replica_list}')
