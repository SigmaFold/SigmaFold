"""
Provides helper functions to help handdling shapes for various purposes (database storage, training etc.)
"""
import numpy as np
import math

# Saving shapes based on their center of mass 
def path2shape(path):
    grid = np.asarray([[0]*25]*25, dtype=int) # actual grid for mapping
    temp_grid = np.asarray([[0]*25]*25, dtype=int) # temp grid to hold the array before alignment
    for coord in test_path:
        temp_grid[coord[0]+13][coord[1]+13] = 1 # path transferred onto grid but uncentered
    temp_grid = np.pad(temp_grid, 1) # zero padding to avoid multiplying by 0 when calculating moments

    # find centroid of temp_grid
    m_00 = len(path) # non-zero residues
    m_01 = 0
    for row_n, row in enumerate(temp_grid):
        if np.any(row!=0):
            m_01 += row_n * np.count_nonzero(row)
    m_10 = 0
    for col_n in range(np.shape(temp_grid)[1]):
        if np.any(temp_grid[:, col_n]!=0):
            m_10 += col_n *  np.count_nonzero(temp_grid[:, col_n])

    # coordinates of centroid
    n_centroid = math.floor((m_10/m_00))
    m_centroid = math.floor((m_01/m_00))
    centroid = (m_centroid, n_centroid)

    # align temp_grid onto grid
    dev_m = 13-centroid[0]
    dev_n = 13-centroid[1]
    coord_list = np.nonzero(temp_grid)
    for i in range(len(coord_list[0])):
        grid[coord_list[0][i]+dev_m][coord_list[1][i]+dev_n] = 1

    return grid


def serialize_shape(matrix):
    """
    Flattens matrix then condenses its elements into a string. When an element is repeated, it'll encode the number of repeats as follows:
    If its repeated 0-9 times it'll encode it as the count then the repeated digit 
    for 10-36 it'll encode it as a letter in the alphabet then the repeated digit.
    Beyond that, it'll just separate the repeated digit into 2 batches of 36 or less
    
    """

    matrix = matrix.flatten()
    string = ""
    count = 1

    def encode_count(count):
        if count < 10:
            return str(count)
        else:
            print(count)
        return chr(count+87)
    # CLUNKY AND WILL BE IMPROVED - JUST A POC RN 
    for i in range(len(matrix)-1):
        if matrix[i] == matrix[i+1]:
            count += 1
        else:
            string += encode_count(count)
            string += str(matrix[i])
            count = 1

    string += encode_count(count)
    string += str(matrix[-1])

    return string


def deserialize_shape(string):
    """
    Takes a string and decodes it into a matrix
    """
    matrix = np.array([])
    count = 0
    def decode_count(char):
        if char.isdigit():
            return int(char)
        return ord(char)-87
    
    for i in range(0,len(string), 2):
        matrix = np.append(matrix, np.full(decode_count(string[i]), int(string[i+1])))

    #print(matrix)
    


    return np.asarray(matrix).reshape(25, 25)


if __name__ == "__main__":
    # generate a random 25 by 25 matrix 
    matrix = np.random.randint(2, size=(25, 25))
    #print(matrix)
    print(len(serialize_shape(matrix)))
    deserialized = deserialize_shape(serialize_shape(matrix))
    assert np.array_equal(matrix, deserialized)


