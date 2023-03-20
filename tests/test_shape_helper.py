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