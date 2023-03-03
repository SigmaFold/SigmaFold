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
# from lib.tools import profile
import time

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
    seq_df = pd.DataFrame(columns=["sequence_id", "sequence", "degeneracy", "length", "energy", "shape_mapping"])
    shape_df = pd.DataFrame(columns=["shape_id", "min_degeneracy", "length", "min_energy"])
    map_df = pd.DataFrame(columns=["map_id", "sequence_id", "shape_id"])

    paths = fold_n(length)  # Get all the possible paths for a given length
    comb_array = perm_gen(length, 2)  # Get all the possible sequences for a given length

    # Iterate over all the possible combinations
    for sequence in comb_array:
        
        energy_heap = compute_energy(paths, sequence)  # Compute the energy of all the possible paths
        folds_heap, degeneracy, energy = native_fold(energy_heap, return_energy=True)  # Get all the low-energy folds for a given sequence
        # print(tabulate.tabulate(seq_df, headers="keys", tablefmt="psql"))

        if degeneracy > 100:  # Skip deg>100 cause that's useless    anyway
            continue
        # For each possible folds of the current sequence
        for _, fold in folds_heap:

            shape_id = cartesian2matrix(fold)
            seq_hash = mmh3.hash64(sequence + str(shape_id), signed=True)[0]  # Hash the sequence

            seq_df.loc[len(seq_df)] = [seq_hash, sequence, degeneracy, length, energy, shape_id]  # Add the sequence to the sequence_df
            
            # For each fold update the shape_df
            if shape_id not in seen_shapes:  # Will run if shape has not yet been added to database
                seen_shapes.add(shape_id)
                # add new shape to shape_df without using append
                shape_df.loc[len(shape_df)] = [shape_id, degeneracy, length, energy]
            else:
                # Update min_degeneracy if necessary
                if degeneracy < shape_df.loc[shape_df["shape_id"] == shape_id, "min_degeneracy"].iloc[0]:
                    shape_df.loc[shape_df["shape_id"] == shape_id, "min_degeneracy"] = degeneracy

                # Update min_energy if necessary
                if energy < shape_df.loc[shape_df["shape_id"] == shape_id, "min_energy"].iloc[0]:
                    shape_df.loc[shape_df["shape_id"] == shape_id, "min_energy"] = energy
            
            # convert to int 
  
    # remove all sequences with shape_mapping 0 
    seq_df = seq_df[seq_df["shape_mapping"] != 0]
    # convert to int
    seq_df = seq_df.astype({"sequence_id": int, "degeneracy": int, "length": int, "shape_mapping": int})
    # Set the dataframes for each column in a dict, umbers should be np.uint64
    #     # print all duplicates of map_id in map_df
    #print(tabulate.tabulate(map_df[map_df.duplicated(subset=["map_id"])], headers="keys", tablefmt="psql"))
    seq_df = seq_df.astype({"sequence_id": int, "degeneracy": int, "length": int})
    shape_df = shape_df.astype({"shape_id": int, "min_degeneracy": int, "length": int})
    print(tabulate.tabulate(shape_df, headers="keys", tablefmt="psql"))
    for _, row in map_df.iterrows():
        map_list.append(row.to_dict())
    for _, row in shape_df.iterrows():
        shape_list.append(row.to_dict())
    # Package each row of seq_df into a dict and add to list
    for _, row in seq_df.iterrows():
        seq_list.append(row.to_dict())
    # Package each row of map_df into a dict and add to list
    

    return shape_list, seq_list


def commit_to_supabase(n, shape_list, seq_list):
    """ Adds all the data to the database asynchronously"""
    # Create a client
    
    with open(f"data/{n}/seq_{n}.json", "w") as f:
        json.dump(seq_list, f)
    with open(f"data/{n}/shape_{n}.json", "w") as f:
        json.dump(shape_list, f)
    
    print("Data saved to json files")
    return
    



if __name__ == '__main__':
    set_limit = 10
    n = 1
    execution_time = {}
    while n <= set_limit:
        print("Adding data for length: ", n)
        time_start = time.time()
        commit_to_supabase(n, *exploitLength(n))
        time_end = time.time()
        execution_time[n] = time_end - time_start
        print("Time taken: ", time_end - time_start)
        n += 1 
