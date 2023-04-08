"""
Provides helper functions to help handdling shapes for various purposes (database storage, training etc.)
"""
import numpy as np
import math


# Saving shapes based on their center of mass


def path_to_shape(path):
    """Returns a binary shape and new path given a pth

    :param path: list of tuples containing coordinates of a folding path
    :return: numpy array of the shape with 1s depicting filled positions and 0s empty,
             list of tuples relating to the new path within the numpy array shape
    """
    grid = np.asarray([[0]*25]*25, dtype=int)  # actual grid for mapping
    # temp grid to hold the array before alignment
    temp_grid = np.asarray([[0]*25]*25, dtype=int)
    for coord in path:
        # path transferred onto grid but uncentered
        temp_grid[coord[1]+13][coord[0]+13] = 1
    # zero padding to avoid multiplying by 0 when calculating moments
    temp_grid = np.pad(temp_grid, 1)

    # find centroid of temp_grid
    m_00 = len(path)  # non-zero residues
    m_01 = 0
    for row_n, row in enumerate(temp_grid):
        if np.any(row != 0):
            m_01 += row_n * np.count_nonzero(row)
    m_10 = 0
    for col_n in range(np.shape(temp_grid)[1]):
        if np.any(temp_grid[:, col_n] != 0):
            m_10 += col_n * np.count_nonzero(temp_grid[:, col_n])

    # coordinates of centroid
    n_centroid = math.floor((m_10/m_00))
    m_centroid = math.floor((m_01/m_00))
    centroid = (m_centroid, n_centroid)
    print("centroid ==>", centroid)
    # align temp_grid onto grid
    dev_m = 13-centroid[0]
    dev_n = 13-centroid[1]
    coord_list = np.nonzero(temp_grid)
    print("centroid ==>", (dev_m, dev_n))
    for i in range(len(coord_list[0])):
        grid[coord_list[0][i]+dev_m][coord_list[1][i]+dev_n] = 1

    return grid, path


def path_to_shape_numbered(path, sequence):
    """Returns a path shape, HP shape and new path given a path and sequence

    :param path: list of tuples containing coordinates of a folding path
           sequence: string containing the sequence
    :return: numpy array of the shape with numbers from 1 signifying the direction of a path,
             numpy array of the shape with 1s corresponding to H assignment and 2s to P assignments. 0s are empty posiitons,
             list of tuples relating to the new path within the numpy array shape
    """
    path_grid = np.asarray(
        [[0]*25]*25, dtype=int)  # actual path grid for mapping
    HP_grid = np.asarray([[0]*25]*25, dtype=int)  # actual HP grid for mapping
    # temp grid to hold the array before alignment
    temp_path_grid = np.asarray([[0]*25]*25, dtype=int)
    # temp grid to hold the array before alignment
    temp_HP_grid = np.asarray([[0]*25]*25, dtype=int)
    # replace H with 1 and P with 2 in sequence
    numbered_sequence = [1 if x == 'H' else 2 for x in sequence]
    for i, coord in enumerate(path):
        # path transferred onto grid but uncentered
        temp_path_grid[coord[1]+13][coord[0]+13] = i+1
        # HP transferred onto grid but uncentered
        temp_HP_grid[coord[1]+13][coord[0]+13] = numbered_sequence[i]
    # zero padding to avoid multiplying by 0 when calculating moments
    temp_path_grid = np.pad(temp_path_grid, 1)
    temp_HP_grid = np.pad(temp_HP_grid, 1)

    # find centroid of temp_path_grid
    m_00 = len(path)  # non-zero residues
    m_01 = 0
    for row_n, row in enumerate(temp_path_grid):
        if np.any(row != 0):
            m_01 += row_n * np.count_nonzero(row)
    m_10 = 0
    for col_n in range(np.shape(temp_path_grid)[1]):
        if np.any(temp_path_grid[:, col_n] != 0):
            m_10 += col_n * np.count_nonzero(temp_path_grid[:, col_n])

    # coordinates of centroid
    n_centroid = math.floor((m_10/m_00))
    m_centroid = math.floor((m_01/m_00))
    centroid = (m_centroid, n_centroid)
    # align temp_path_grid onto grid
    dev_m = 13-centroid[0]
    dev_n = 13-centroid[1]
    coord_list = np.nonzero(temp_path_grid)
    # create grid for path_shape
    for i in range(len(coord_list[0])):
        path_grid[coord_list[0][i]+dev_m][coord_list[1][i] +
                                          dev_n] = temp_path_grid[coord_list[0][i]][coord_list[1][i]]
    # create grid for HP_shape
    for i in range(len(coord_list[0])):
        HP_grid[coord_list[0][i]+dev_m][coord_list[1][i] +
                                        dev_n] = temp_HP_grid[coord_list[0][i]][coord_list[1][i]]

    # find element "1"
    pos = np.where(path_grid == 1)
    # add pos to each element of the path
    path = [(path[i][0]+pos[1][0], path[i][1]+pos[0][0])
            for i in range(len(path))]

    return path_grid, HP_grid, path


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

    def decode_count(char):
        if char.isdigit():
            return int(char)
        return ord(char)-87

    for i in range(0, len(string), 2):
        matrix = np.append(matrix, np.full(
            decode_count(string[i]), int(string[i+1])))
    return np.asarray(matrix).reshape(25, 25)


"""
The below functions allow us to convert between the database representation of a path and the actual path
"""


def serialize_path(path):
    """
    Store the path of tuples as a string in a way that can be easily decoded.
    """
    string = ""
    for coord in path:
        string += str(coord[0]) + "," + str(coord[1]) + " "
    return string


def deserialize_path(string):
    """
    Takes a string and decodes it into a path
    """
    path = []
    for coord in string.split():
        path.append(tuple(map(int, coord.split(","))))
    return path

def deserialize_point(point):
    """
    Takes a point on the db and deserialize it into a tuple
    """
    return tuple(map(int, point.split(",")))
    
if __name__ == "__main__":
    path2 = [(0, 0), (-1, 0), (-1, -1), (-1, -2), (0, -2), (0, -1), (1, -1)]
    print("OG path", path2)
    matrix, path = path_to_shape_numbered(path2)

    print(matrix)
    print("New path", path)
