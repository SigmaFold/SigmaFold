"""
OBSOLETE - DO NOT TOUCH THES.
"""
import math
import numpy as np
import random as rnd
from typing import List, Tuple
import mmh3
import json 

# =============================== Helper Functions ================================
def cartesian_to_matrix(path):
        """Function that encodes a cartesian set of coordinates into a matrix
        
        :param path: a list of tuples of coordinates
        :param return_matrix: if True, returns the matrix corresponding to the shape as well. This is a binary matrix.
        :returns: a shape id matching the ones on the database
        """
        # generate a 25 by 25 matrix in numpy
        matrix = np.zeros((25, 25))


        for x, y in path:
            matrix[y + 13, x + 13] = True
        return matrix

def matrix_to_shape_id(matrix):
    """Function that encodes a matrix into a shape id
        
    :param matrix: a binary matrix
    :returns: a shape id matching the ones on the database
    """
    # Array hashing
    matrix.flags.writeable = False
    curr_shape_id = mmh3.hash64(str(matrix), signed=True)[0]
    return curr_shape_id




# =============================== Main Logic  ================================
def get_shape(n=10, random=True, from_input=False):
    """
    Returns a shape based on the user input.

    :params random: if True, generates a random shape
    :params from_input: if user inputs their desired shape, it will be used.

    :returns: a shape
    """
    if from_input:
        return generate_shape_from_input(from_input)
    return generate_random_shape(n)




def generate_random_shape(n):
    """
    Generates a random shape that is compatible with the database format.

    :returns: a shape id
    """
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    cap_x = math.ceil(n / 2) - 1
    
    def generate_random_path():
        """Generate a random path with no duplicate coordinates"""
        path = set([(0, 0), (0, 1)])
        visited = set()
        visited.add((0, 0))
        visited.add((0, 1))

        last_x, last_y = 0, 1
        max_loop_iteration = n * 6
        loop = 0
        while len(path) < n:
            loop += 1
            if loop > max_loop_iteration:
                # reset the path, visited and start again. Algo got stuck in a loop
                path = set([(0, 0), (0, 1)])
                visited = set([(0, 0), (0, 1)])
                x, y = 0, 1
                last_x, last_y = 0, 1
                loop = 0

            x, y = last_x, last_y
            # choose a dir 
            dir_choice = rnd.choice(dirs)
            x += dir_choice[0]
            y += dir_choice[1]
            if (x, y) not in visited:
                visited.add((x, y))
                cap_y = math.ceil((n / (abs(x) + 1)) - 1) if abs(x) > 0 else cap_x
                if abs(x) > cap_x or abs(y) > cap_y:
                    continue
                else:
                    path.add((x, y))
                    last_x, last_y = x, y
        return list(path)
    
    path = generate_random_path()

    matrix = cartesian_to_matrix(path)
    shape_id = matrix_to_shape_id(matrix)
    return matrix, shape_id

def generate_shape_from_input(from_input):
    """
    TODO: The way in this function is written can be improved. Currently takes a PATH as input, turns it into a shape, and then rotates the shape in the right direction.
    :returns: (List) the right shape ids (inshallah)
    """
    # Look at s econd element of the list to know which direction to rotate the shape. We want the second index to be (0,1) , above, because that is the direction the shape is facing in the database
    # define numbre of 90 rotations depending on what the second element of the list is
    number_of_rotations = {
        (0,1): 0,
        (-1,0): 1,
        (0,-1): 2,
        (1,0): 3,
    }

    second_element = from_input[1]
    # Get the shape id of the input shape
    shape_matrix = cartesian_to_matrix(from_input)

    for _ in range(number_of_rotations[second_element]):
        shape_matrix = np.rot90(shape_matrix)
    
    shape_ids = []
    shape_ids.append(matrix_to_shape_id(shape_matrix))
    shape_ids.append(matrix_to_shape_id(np.fliplr(shape_matrix)))
     # TODO : return the matrices as well 
    return shape_ids





if __name__ == "__main__":
    shape = sample_from_json(15)
    

    # input_shape = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [1, 7], [1, 6], [1, 5], [1, 4], [2, 4], [2, 3], [3, 3]]
    # # convert interior to tuples
    # input_shape = [tuple(x) for x in input_shape]
    # (get_shape(from_input=input_shape))


    
    
    





