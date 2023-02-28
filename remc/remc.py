import numpy as np
import sys
import pivot_moves


def graphicchain(positions, matrix):
    '''This function takes a list of sequence positions and a matrix and returns a matrix with the positions of the list marked on the matrix.
    The positions list is a list of lists containing the amino acid, the x coordinate and the y coordinate of the amino acid.
    The format is [['H', 4, 5], ['P', 5, 5], ['H', 6, 5]]
    The matrix acts as a background for the positions.'''
    graphic_matrix = matrix.copy().astype(np.int).astype(np.str)
    for i in range(len(positions)):
        graphic_matrix[positions[i][1]][positions[i][2]] = positions[i][0]
    return graphic_matrix




if __name__ == "__main__":
    forwardbias = 1
    offset = 0
    bestenergy = 0
    sequence = "HHHHHHHHPHHHHPHH"
    speedfactor = 2
    possibles = []
    n = len(sequence)

    # create a test matrix of size 11X11 where the origin is at the center [5,5]
    test_matrix = np.zeros((10, 10)) # Initialize a matrix of zeros
    positions1 = [['H', 4, 5], ['H', 5, 5], ['H', 5, 4], ['H', 6, 4],
                  ['H', 6, 5], ['H', 7, 5], ['H', 7, 4], ['H', 7, 3],
                  ['P', 7, 2], ['H', 6, 2], ['H', 6, 3], ['H', 5, 3],
                  ['H', 5, 2], ['P', 4, 2], ['H', 4, 3], ['H', 4, 4]] # List of positions
    test_matrix = graphicchain(positions1, test_matrix) # Mark the positions on the matrix
