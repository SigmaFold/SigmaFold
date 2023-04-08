import numpy as np
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from library.db_query_templates import get_random_shape, find_HP_assignments
from library.shape_helper import path_to_shape, path_to_shape_numbered

def test_get_random_shape():
    shape = get_random_shape()
    assert shape.shape == (25, 25)

def test_find_HP_assignments():
    seq = 'HHHPH'
    path = [(0,0), (0,1), (0,2), (-1,2), (-1,1)]
    
    length = len(seq)
    target_grid, _ = path_to_shape(path)
    path_grid, HP_grid, _ = path_to_shape_numbered(path, seq)
    sequence_list, correctHPassignments_list = find_HP_assignments(length, target_grid, path_grid)
    
    passed = False
    if seq in sequence_list:
        for a in correctHPassignments_list:
            if np.array_equal(a, HP_grid):
                passed = True
    print(passed)

if __name__ == "__main__":
    test_find_HP_assignments()
    
