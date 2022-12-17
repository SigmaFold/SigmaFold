# from sqlalchemy.sql import Values
from generate_permutations import *
from fold_seq import primitive_fold
import pandas as pd # t pédé ou quoi
import numpy as np
# from supabase import create_client, Client



def cartesian2matrix(path):
    """Function that encodes a cartesian set of coordinates into a matrix"""
    x_array = [node[0] for node in path]
    y_array = [node[1] for node in path]
    n = 2*(max(np.absolute(x_array))+1) - 1 # number of columns
    m = 2*(max(np.absolute(y_array))+1) - 1 # number of rows
    template = np.zeros([m,n]).astype(int)
    i_offset = int((m+1)/2)
    j_offset = int((n+1)/2)
    node_order = 1
    for node in path:
        i = node[1]-i_offset
        j = node[0]-j_offset
        template[i,j] = node_order
        node_order += 1
    template = np.flipud(template) # vertical flip to put it correctly

    # Remove zero-padding
    template = template[~np.all(template == 0, axis=1)]
    idx = np.argwhere(np.all(template[..., :] == 0, axis=0))
    template = np.delete(template, idx, axis=1)
    # print(template)
    return(template)


def exploitLength(length):

    # Initialise the Dataframes
    d = {"sequence_id": [], "shape_id": [], "sequence_string": [], "degeneracy": []}
    shapes_dict = {"shape_id": [], "min_degeneracy": []}

    comb_array = perm_gen(length) # List with all the possible combinations for the given n

    # Iterate over all the possible combinations
    for sequence in comb_array:
        _, folds, degeneracy = primitive_fold(sequence) # Get all the low-energy folds for a given sequence
        if degeneracy > 100: # Skip deg>100 cause that's useless anyway
            continue

        # For each possible folds of the current sequence
        for fold in folds:
            matrix_repr = cartesian2matrix([real_fold[0] for real_fold in fold[1]]) # Generate matrix representation of fold

            # Array hashage
            matrix_repr.flags.writeable = False
            curr_shape_id = hash(str(matrix_repr))

            if curr_shape_id in d["shape_id"]: # Will run if shape has not yet been added to database
                i = d["shape_id"].index(curr_shape_id)
                d["sequence_string"][i].append(sequence)
                d["degeneracy"][i].append(degeneracy)
                d["sequence_id"][i] = d["sequence_id"][-1] + 1
            else: # Will run if shape was alread found
                print("Running except clause")
                d["shape_id"].append(curr_shape_id)
                d["sequence_string"].append([sequence])
                d["degeneracy"].append([degeneracy])
                d["sequence_id"].append(0)

    # Runs after all combinations have been analysed to create the shapes dataframe
    for entry in d["shape_id"]: # for each shape_id in the dictionary
        i = d["shape_id"].index(entry)
        min_deg = min(d["degeneracy"][i])
        shapes_dict["shape_id"].append(entry)
        shapes_dict["min_degeneracy"].append(min_deg)


    sequence_df = pd.DataFrame(data=d)
    print(sequence_df)

    shapes_df = pd.DataFrame(data=shapes_dict)
    print(shapes_df)

if __name__ == '__main__':
    set_limit = 7
    n = 7
    while n <= set_limit:
        exploitLength(n)
        n += 1


