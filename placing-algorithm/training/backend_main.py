import sys
import os

# Set current working directory to be 3 levels above the current file
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # THI

from lib.generate_permutations import *
from lib.native_fold import *

import pandas as pd
import numpy as np
import mmh3
import tabulate
from db.supabase_setup import SupabaseDB
import json
def cartesian2matrix(path):
    """Function that encodes a cartesian set of coordinates into a matrix"""
    # generate a 25 by 25 matrix in numpy
    matrix = np.zeros((25, 25))
    for x, y in path:
        matrix[y + 13, x + 13] = 1
    # Array hashing
    matrix.flags.writeable = False
    curr_shape_id = mmh3.hash64(str(matrix), signed=True)[0]
    return curr_shape_id


def exploitLength(length):
    # Where we will store the dictionaries of data
    seq_list = []
    shape_list = []
    map_list = []

    seen_shapes = set()
    seen_map_ids = set()
    # Initialise the Dataframes
    # set the datatypes for each column
    seq_df = pd.DataFrame(columns=["sequence_id", "sequence", "degeneracy", "length"])
    shape_df = pd.DataFrame(columns=["shape_id", "min_degeneracy", "length"])
    map_df = pd.DataFrame(columns=["map_id", "sequence_id", "shape_id"])

    paths = fold_n(length)  # Get all the possible paths for a given length
    comb_array = perm_gen(length, 2)  # Get all the possible sequences for a given length

    # Iterate over all the possible combinations
    for sequence in comb_array:
        seq_hash = mmh3.hash64(sequence, signed=True)[0]  # Hash the sequence
        
        energy_heap = compute_energy(paths, sequence)  # Compute the energy of all the possible paths
        folds_heap, degeneracy = native_fold(energy_heap)  # Get all the low-energy folds for a given sequence
        seq_df.loc[len(seq_df)] = [seq_hash, sequence, degeneracy, length]
        if degeneracy > 30:  # Skip deg>100 cause that's useless anyway
            continue
        # For each possible folds of the current sequence
        for _, fold in folds_heap:
            shape_id = cartesian2matrix(fold)

            # For each fold update the shape_df
            if shape_id not in seen_shapes:  # Will run if shape has not yet been added to database
                seen_shapes.add(shape_id)
                # add new shape to shape_df without using append
                shape_df.loc[len(shape_df)] = [shape_id, degeneracy, length]
            else:
                # Update min_degeneracy if necessary
                if degeneracy < shape_df.loc[shape_df["shape_id"] == shape_id, "min_degeneracy"].iloc[0]:
                    shape_df.loc[shape_df["shape_id"] == shape_id, "min_degeneracy"] = degeneracy
            

            # Add mapping to map_df
            # Check if previous index is equal to mapping
        
            map_id = mmh3.hash64(str(seq_hash) + str(shape_id), signed=True)[0]
            if map_id not in seen_map_ids:
                seen_map_ids.add(map_id)
                map_df.loc[len(map_df)] = [map_id, seq_hash, shape_id]
            # convert to int 
  

    # Set the dataframes for each column in a dict, umbers should be np.uint64
    map_df = map_df.astype({"map_id": int, "sequence_id": int, "shape_id": int})
    # print all duplicates of map_id in map_df
    #print(tabulate.tabulate(map_df[map_df.duplicated(subset=["map_id"])], headers="keys", tablefmt="psql"))
    seq_df = seq_df.astype({"sequence_id": int, "degeneracy": int, "length": int})
    shape_df = shape_df.astype({"shape_id": int, "min_degeneracy": int, "length": int})
    print(tabulate.tabulate(shape_df, headers="keys", tablefmt="psql"))
    #print(tabulate.tabulate(shape_df, headers="keys", tablefmt="psql"))
    # print(tabulate.tabulate(seq_df, headers="keys", tablefmt="psql"))
    #print(tabulate.tabulate(map_df, headers="keys", tablefmt="psql"))
    #print(shape_df.dtypes)
    # Convert all columns to int
    # Package each row of shape_df into a dict and add to list
    for _, row in map_df.iterrows():
        map_list.append(row.to_dict())
    for _, row in shape_df.iterrows():
        shape_list.append(row.to_dict())
    # Package each row of seq_df into a dict and add to list
    for _, row in seq_df.iterrows():
        seq_list.append(row.to_dict())
    # Package each row of map_df into a dict and add to list
    

    return shape_list, seq_list, map_list


def commit_to_supabase(n, shape_list, seq_list, mapping_list):
    """ Adds all the data to the database asynchronously"""
    # Create a client

    with open(f"data/seq_{n}.json", "w") as f:
        json.dump(seq_list, f)
    with open(f"data/shape_{n}.json", "w") as f:
        json.dump(shape_list, f)
    with open(f"data/map_{n}.json", "w") as f:
        json.dump(mapping_list, f)
    
    print("Error: ", e)
    print("Data saved to json files")
    return
    print("Data added to database")
    



if __name__ == '__main__':
    set_limit = 12
    n = 12
    while n <= set_limit:
        print("Adding data for length: ", n)
        commit_to_supabase(n, *exploitLength(n))
        n += 1 