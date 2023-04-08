"""
Samples all shapes with min_degen less than 10 and returns the best starting point for each shape.
"""
import numpy as np
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # THI
from library.db_query_templates import get_all_sequences_for_shape, get_all_random_shapes, get_all_shape_data
from library.shape_helper import path_to_shape_numbered, deserialize_path, deserialize_shape, serialize_path
from library.db_helper import SupabaseDB

def get_best_starting_point(shape_id):
        sequences = get_all_sequences_for_shape(shape_id)
        # sort df by degeneracy
        sequences = sequences.sort_values(by=['degeneracy'], ascending=True)
        # get the first row
        best_sequence = sequences.iloc[0]    
        # get the sequence of the first row 
        sequence = best_sequence['sequence']
        # get the path of the first row 
        path = best_sequence['path']
        # convert path to list of tuples
        path = deserialize_path(path)
        shape, _ , path = path_to_shape_numbered(path, sequence)
        # get the starting point of the path
        # convert to ndarray
        # get the position of the first 1 in the shape matrix
        starting_point = np.argwhere(shape == 1)[0]
        # flip to be cartesian coordinates
        starting_point = np.flip(starting_point)

        # check if the starting point is the position of a 1 in the "shape" matrix
        if not shape[starting_point[1], starting_point[0]] == 1:
            raise Exception("The starting point is not a 1 in the shape matrix")
        
        # find location of the first 2 
        next_point = np.argwhere(shape == 2)[0]
        # flip to be cartesian coordinates
        next_point = np.flip(next_point)
        # get the direction of the path
        direction = next_point - starting_point
        return starting_point, direction, path, sequence

def upload_best_starting_points(n=16):
    """
    Uploads the best starting points for all shapes with min_degen less than 10.
    """
    # get all shapes with min_degen less than 10
    shapes = get_all_shape_data(n)
    print(shapes)
    db = SupabaseDB()
    # iterate over all shapes
    for row in shapes.iterrows():
        shape_id = row[1]['shape_id']
        # get the best starting point for the shape
        starting_point, direction, path, sequence = get_best_starting_point(shape_id)
        path = serialize_path(path)

        # convert to string to upload to db
        starting_point = ",".join(str(x) for x in starting_point)
        direction = ",".join(str(x) for x in direction)
        #print("Starting point", starting_point, "Direction", direction)
        data = {"starting_point": starting_point, "starting_dir": direction, "shape_id": shape_id, "optimal_path": path, "best_sequence": sequence}
        # upload the best starting point for the shape
        db.supabase.table("Shapes").insert(data, upsert=True).execute()

if __name__ == "__main__":
    for n in range(14, 17):
        upload_best_starting_points(n)
