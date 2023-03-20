import sys 
import os
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from library.shape_helper import *



def test_serialize_shape():
    matrix = np.random.randint(2, size=(25, 25))
    matrix = np.array([0,0,0,0,0,0,0,0,0,0])
    assert len(serialize_shape(matrix)) == 2
    assert serialize_shape(matrix) == "a0"


def test_deserialize_shape():
    matrix = np.random.randint(2, size=(25, 25))
    assert np.array_equal(deserialize_shape(serialize_shape(matrix)), matrix)


def test_path_to_shape():
    # will generate two path that fold into the same shape and check whether they generate the same matrix
    path = [(0,0), (-1,0), (-1,-1), (-2,-1), (-2,0), (-2, 1), (-1, 1)]
    path2 = [(0,0), (-1,0), (-1,-1), (-1, -2), (0, -2), (0, -1), (1, -1)]

    matrix1= path_to_shape(path)
    matrix2 = path_to_shape(path2)
    assert np.array_equal(matrix1, matrix2)

if __name__ == "__main__":
    test_path_to_shape()