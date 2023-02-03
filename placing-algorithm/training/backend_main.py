import sys, os

# Set current working directory to be 3 levels above the current file
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) # THI

from lib.generate_permutations import *
from lib.native_fold import *

import pandas as pd
import numpy as np
import mmh3
import tabulate


# from supabase import create_client, Client


def cartesian2matrix(path):
    """Function that encodes a cartesian set of coordinates into a matrix"""
    x_array = [node[0] for node in path]
    y_array = [node[1] for node in path]
    n = 2 * (max(np.absolute(x_array)) + 1) - 1  # number of columns
    m = 2 * (max(np.absolute(y_array)) + 1) - 1  # number of rows
    template = np.zeros([m, n]).astype(int)
    i_offset = int((m + 1) / 2)
    j_offset = int((n + 1) / 2)
    node_order = 0
    for node in path:
        i = node[1] - i_offset
        j = node[0] - j_offset
        template[i, j] = node_order
        node_order += 1
    template = np.flipud(template)  # vertical flip to put it correctly

    # Remove zero-padding
    template = template[~np.all(template == 0, axis=1)]
    idx = np.argwhere(np.all(template[..., :] == 0, axis=0))
    template = np.delete(template, idx, axis=1)
    # print(template)
    return (template)


def exploitLength(length):
    # Initialise the Dataframes
    seq_list = []  # Where we will store the dictionaries of data
    shape_list = []

    seq_dict = {"shape_id": [], "sequence_string": [], "degeneracy": []}

    seen_shapes = set()
    shape_df = pd.DataFrame(columns=["shape_id", "degeneracies", "min_degeneracy"])

    paths = fold_n(length)
    print(f'Paths: {paths}')  # List of all the possible paths for a given n (2n-1 p
    comb_array = perm_gen(length, 2)
    print(f'Comb Array : {comb_array}')  # List with all the possible combinations for the given n

    # Iterate over all the possible combinations
    for sequence in comb_array:
        energy_heap = compute_energy(paths, sequence)
        print(f'Energy heap: {energy_heap}')
        folds, degeneracy = native_fold(energy_heap) # Get all the low-energy folds for a given sequence
        if degeneracy > 30:  # Skip deg>100 cause that's useless anyway
            continue
        # For each possible folds of the current sequence
        for fold in folds:
            matrix_repr = cartesian2matrix(fold)
            # Array hashage
            matrix_repr.flags.writeable = False
            curr_shape_id = mmh3.hash64(str(matrix_repr), signed=False)[0]  # Hash the matrix representation

            # For each fold create a dictionary with its shape_id, sequence_id and degeneracy

            if curr_shape_id not in seen_shapes:  # Will run if shape has not yet been added to database
                seen_shapes.add(curr_shape_id)
                # add new shape to shape_df
                shape_df = shape_df.append({"shape_id": curr_shape_id, "degeneracies": [degeneracy],
                                            "min_degeneracy": degeneracy}, ignore_index=True)



            else:
                print(f"Seen this shape before!")
            # Append degeneracy to shape_df column with corresponding shape id
            shape_df.loc[shape_df["shape_id"] == curr_shape_id, "degeneracies"].iloc[0].append(degeneracy)
            # Update min_degeneracy if necessary
            if degeneracy < shape_df.loc[shape_df["shape_id"] == curr_shape_id, "min_degeneracy"].iloc[0]:
                shape_df.loc[shape_df["shape_id"] == curr_shape_id, "min_degeneracy"] = degeneracy

            # Add sequence to sequence_df
            seq_dict["sequence_string"] = sequence
            seq_dict["degeneracy"] = degeneracy
            seq_dict["sequence_id"] = mmh3.hash64(str(curr_shape_id) + sequence, signed=False)[0]
            seq_dict["shape_id"] = curr_shape_id
            seq_list.append(seq_dict.copy())  # this is the list of stuff that needs to go into the database
            # commit new sequence to database here
    # Print df without the degeneracies column
    # Drop degeneracies column
    shape_df = shape_df.drop(columns=["degeneracies"])
    # Print df
    print(tabulate.tabulate(shape_df, headers="keys", tablefmt="psql"))

    # Package eqch row of shqpe_df into a dict and add to list
    for _, row in shape_df.iterrows():
        shape_list.append(row.to_dict())

    print(shape_list)
    return seq_list, shape_list


def commit_to_supabase():
    pass
    


if __name__ == '__main__':
    set_limit = 7
    n = 7
    while n <= set_limit:
        exploitLength(n)
        n += 1

# TODO: Optimize by keeping the array of degeneracies as a min heap.
