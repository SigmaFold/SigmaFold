import sys
import os
# Set current working directory to be 3 levels above the current file
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # THI

from library.permutations_helper import *
from library.native_fold import *
from library.db_helper import *
from library.shape_helper import *

import pandas as pd
import numpy as np
import mmh3
import tabulate
import json
# from lib.tools import profile
import time




def exploitLength(length):
    # Where we will store the dictionaries of data
    seq_list = []
    shape_list = []
    seen_shapes = set()
    seq_df = pd.DataFrame(columns=["sequence_id", "sequence", "degeneracy", "length", "energy", "shape_mapping", "path"])
    shape_df = pd.DataFrame(columns=["shape_id", "min_degeneracy", "length", "min_energy"])

    # NEW SPEEDUP TO AVOID REPEATED COMPUTATIONS
    if os.path.exists(f"data/folds/fold_{length}.json"):
        with open(f"data/folds/fold_{length}.json", "r") as f:
            paths = json.load(f)
            print("Loaded paths from json file")
    else:       
        paths = fold_n(length)  # Get all the possible paths for a given length 
        # Save the paths to a json file
        with open(f"data/folds/fold_{n}", "w") as f:
            json.dump(paths, f)

    comb_array = perm_gen(length, 2)  # Get all the possible sequences for a given length

    # Iterate over all the possible combinations
    for sequence in comb_array:
        
        energy_heap = compute_energy(paths, sequence)  # Compute the energy of all the possible paths
        folds_heap, degeneracy, energy = native_fold(energy_heap, return_energy=True)  # Get all the low-energy folds for a given sequence

        if degeneracy > 150 :  # Skip deg>200 cause that's useless    anyway
            continue
        # For each possible folds of the current sequence
        for _, fold in folds_heap:

            matrix = path_to_shape(fold) 
            shape_id  = serialize_shape(matrix)  # Get the shape_id of the current fold
            seq_hash = mmh3.hash64(sequence + str(shape_id), signed=True)[0]  # Hash the sequence
            seq_df.loc[len(seq_df)] = [seq_hash, sequence, degeneracy, length, energy, shape_id, serialize_path(fold)]  # Add the sequence to the sequence_df
            
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
  
    # remove all sequences with shape_mapping 0 
    seq_df = seq_df[seq_df["shape_mapping"] != 0]

    # Get datatypes right in the dataframe
    seq_df = seq_df.astype({"sequence_id": int, "degeneracy": int, "length": int})
    shape_df = shape_df.astype({ "min_degeneracy": int, "length": int})

    # Remove all duplicates from each dataframe
    seq_df = seq_df.drop_duplicates()
    shape_df = shape_df.drop_duplicates()

    print(tabulate.tabulate(seq_df, headers="keys", tablefmt="psql"))

    for _, row in shape_df.iterrows():
        shape_list.append(row.to_dict())
    # Package each row of seq_df into a dict and add to list
    for _, row in seq_df.iterrows():
        seq_list.append(row.to_dict())

    return shape_list, seq_list


def save_and_upload(n, shape_list, seq_list):
    """ Adds all the data to the database asynchronously"""

    # Create a client
    with open(f"data/{n}/seq_{n}.json", "w") as f:
        json.dump(seq_list, f)
    with open(f"data/{n}/shape_{n}.json", "w") as f:
        json.dump(shape_list, f)
    try:
        upload_data(n)
    except Exception as e:
        print(e)
        print("Data unsuccesfully uploaded to supabase. Do this manually later.")
        return
    print("Data saved to json files")
    return
    



if __name__ == '__main__':
    set_limit =15
    n = 12
    execution_time = {}
    while n <= set_limit:
        print("Adding data for length: ", n)
        time_start = time.time()
        save_and_upload(n, *exploitLength(n))
        time_end = time.time()
        execution_time[n] = time_end - time_start
        print("Time taken: ", time_end - time_start)
        n += 1 
