import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from library.db_query_templates import get_random_shape

def test_get_random_shape():
    shape = get_random_shape()
    assert shape.shape == (25, 25)
    
