"""
Use this file if you want to write a query to do the database and don't know how to do so.

"""

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from library.db_helper import SupabaseDB
from library.shape_helper import *
from library.shape_helper import deserialize_shape
import pandas as pd

# Getting things out of the database

def get_perfect_shapes(target_n=10):
    """ Returns all shapes woith degeneracy 2 in the database
    PREQUESITE: You must have a .env file in the root directory with the following variables:
    URL: the url of the database
    KEY: the secret key for the database

    :params
    :int: target_n: the length of the shape to be returned

    :returns
    :list: perfect_shapes: a list of all the shapes with degeneracy 2 in the database
    """
    db = SupabaseDB()
    # select all the shapes from the database where min_degeneracy = 2
    perfect_shapes = db.supabase.table("Shapes").select("*").eq("min_degeneracy", 2).eq("length", target_n).execute()

    # get all the shape ids and deserialize them
    perfect_shapes = [deserialize_shape(shape["shape_id"]) for shape in perfect_shapes.data]

    return perfect_shapes # return as list of np.arrays


def get_random_shape(target_n=10):
    """ Returns a random shape from the database
    PREQUESITE: You must have a .env file in the root directory with the following variables:
    URL: the url of the database
    KEY: the secret key for the database

    :params
    :int: target_n: the length of the shape to be returned

    :returns
    :np.array: random_shape: a random shape from the database
    """
    db = SupabaseDB()
    # select a random element from the database
    random_shape = db.supabase.table("random_shape").select("*").eq("length", target_n).limit(1).execute()
    shape_id = random_shape.data[0]["shape_id"]

    # deserialize the shape
    random_shape = deserialize_shape(shape_id)

    

    return random_shape, shape_id

def get_random_shape_id(target_n=10):
    """ Returns a random shape id from the database
    PREQUESITE: You must have a .env file in the root directory with the following variables:
    URL: the url of the database
    KEY: the secret key for the database

    :params
    :int: target_n: the length of the shape to be returned

    :returns
    :string: random_shape_id: a random shape from the database
    """
    db = SupabaseDB()
    # select a random element from the database
    random_shape = db.supabase.table("random_shape").select("*").eq("length", target_n).limit(1).execute()

    return random_shape # return as list of strings


def get_all_sequences_for_shape(shape_id):
    """ Returns all sequences for a given shape and their data.
    :params
    :str: shape_id: the shape id of the shape to be returned

    :returns
    :pd.DataFrame: sequences: a list of all the sequences for the given shape.
    """
    db = SupabaseDB()
    # select all the sequences from the database where shape_id = shape_id
    sequences = db.supabase.table("Sequences").select("*").eq("shape_mapping", shape_id).execute()

    # convert to dataframe
    sequences = pd.DataFrame(sequences.data)

    return sequences # return as list of np.arrays

def get_all_shape_data(target_n):
    """ Returns all shape data in the database at a target n

    :params
    :int: target_n: the length of the shape to be returned

    :returns
    :list: shapes: a list of all the shapes in the database
    """
    db = SupabaseDB()
    # select all the shapes from the database where min_degeneracy = 2
    shape_data = db.supabase.table("Shapes").select("*").eq("length", target_n).execute()
    # convert to dataframe
    shape_data = pd.DataFrame(shape_data.data)
    
    return shape_data


def get_all_sequence_data(target_n):
    """ Returns all sequence data in the database at a target n

    :params
    :int: target_n: the length of the shape to be returned

    :returns
    :list: sequences: a list of all the sequences in the database
    """
    db = SupabaseDB()

    # SUPER IMPORTANT FIX TO THE LONG STANDING ISSUE OF DB TIMEOUTS. 
    def count_data(tb_name: str, field_name: str):
        return db.supabase.table(tb_name).select(field_name, count='exact').execute().count

    def get_field_data(tb_name: str, src_field: str, len_record: int, id_field: str = 'id'):
        if len_record <= 1000:
            field_data = db.supabase.table(tb_name).select(id_field, src_field).order(
                column=id_field).execute().data
        else:
            rnk = int(len_record / 1000)
            field_data = []
            for i in range(rnk):
                min_rg = (i * 1000) + 1
                max_rg = (i + 1) * 1000
                field_data = field_data + db.supabase.table(tb_name).select(id_field, src_field).order(
                    column=id_field).range(min_rg - 1, max_rg).execute().data

            field_data = field_data + db.supabase.table(tb_name).select(id_field, src_field).order(
                column=id_field).range(max_rg, len_record).execute().data
        return field_data

    tb_name = "Sequences"
    src_field = "*"
    id_field = "sequence_id"

    len_record = count_data(tb_name, "length")
    sequence_data = get_field_data(tb_name, src_field, len_record, id_field)

    # filter by target_n
    sequence_data = [item for item in sequence_data if item['length'] == target_n]

    # convert to dataframe
    sequence_data = pd.DataFrame(sequence_data)
    return sequence_data

# Checking if things exist 

def check_shape(shape_mappings):
    """
    Checks if a shape is already in the database. If the input is a list, check each mapping sequentially and return the first match. 
    If the input is a single mapping, return the first match.

    :params
    :list: shape_mappings: a list of shape mappings to check
    :bool: matrix: if true, the input is a matrix and not a shape mapping

    :returns
    :str: shape_id: the shape id of the match if it was found, else None
    """
    if type(shape_mappings) == str:
        shape_mappings = [shape_mappings]
    db = SupabaseDB()
    for shape_mapping in shape_mappings:
        shape = db.supabase.table("Shapes").select("*").eq("shape_id", shape_mapping).execute().data
        if shape:
            return shape[0]["shape_id"]
    return None

if __name__ == "__main__":
    sequences = get_all_sequences_for_shape("Ɛ011n041l041l041Ł0")

    # sort sequences by degenracy in an ascending order and save the first one in a variable
    sequences = sequences.sort_values(by=["degeneracy"], ascending=True)
    best_sequence = sequences.iloc[0]
    sequence = best_sequence["sequence"]
    path = best_sequence["path"]
    print(path)
    # separate the path into a list of nodes
    path = path.split(" ")
    path.remove("")
    print(path)
    path = [tuple(map(int, node.split(","))) for node in path]
    print(path)



    # import matplotlib.pyplot as plt


    # seqs = get_perfect_shapes(16)
    # print(len(seqs))
    # plt.matshow(seqs[0])
    # plt.show()