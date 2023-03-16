"""
Provides a set of functions useful for saving, loading or manipulating data in the database.
"""

from supabase import Client, create_client
import os
from dotenv import load_dotenv
import numpy as np
from random import randint
import json 
import pandas as pd
from tabulate import tabulate
import sys 

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from library.tweaking_helper import get_shape, sample_from_json
# COMMENT LINE BELOW OUT - FOR TESTING PURPOSES ONLY


load_dotenv()

# ========================= Supabase Database Connection Toolkit =========================
class Config:
    """
    Root level configuration for project
    """

    URL = os.getenv("URL")
    KEY = os.getenv("KEY")


class SupabaseDB:
    """
    class instance for database connection to supabase
    :str: url: configuration for database url for data inside supafast project
    :str: key: configuration for database secret key for authentication
    :object: supabase: Supabase instance for connection to database environment
    """

    url: str = Config.URL
    key: str = Config.KEY
    supabase: Client = create_client(url, key)

# ========================= JSON Data Saving Toolkit =========================
def upload_data(n):
    """ Imports data from json files and returns lists of dicts"""
    with open(f"data/{n}/seq_{n}.json", "r") as f:
        seq_list = json.load(f)
        print("Parsed seq_list")
    with open(f"data/{n}/shape_{n}.json", "r") as f:
        shape_list = json.load(f)
        print("Parsed shape_list")
    # Drop all duplicates from the lists
    seq_list = list({v['sequence_id']: v for v in seq_list}.values())
    shape_list = list({v['shape_id']: v for v in shape_list}.values())
    try:
        commit_to_supabase(shape_list, seq_list)
    except Exception as e:
        print("Error: ", e)
        print("Data not added to database")
        return
    
def commit_to_supabase(shape_list, seq_list, retries = 0):
    """ Adds all the data to the database asynchronously"""
    # Create a client
    db = SupabaseDB()
    # Add all the data to the database
    if retries > 10:
        print("Too many retries, aborting")
        return
    
    try:
        # insert if it doesn't exist
        db.supabase.table("Shapes").insert(shape_list, upsert=True).execute()
        db.supabase.table("Sequences").insert(seq_list, upsert=True).execute()
    except Exception as e:
        # try again halving the data if it timed out
        print("Error: ", e)
        print("Data not added to database")
        commit_to_supabase(shape_list[:len(shape_list)//2], seq_list[:len(seq_list)//2], retries=retries+1)
        commit_to_supabase(shape_list[len(shape_list)//2:], seq_list[len(seq_list)//2:], retries=retries+1)
        return
    print("Data added to database")

# ========================= Tweaking Algorithm Queries =========================

def check_shape(shape_mappings, matrix=False):
    """
    Checks if a shape is already in the database. If the input is a list, check each mapping sequentially and return the first match. If the input is a single mapping, return the first match
    """
    if type(shape_mappings) == int:
        shape_mappings = [shape_mappings]
    db = SupabaseDB()
    for shape_mapping in shape_mappings:
        shape = db.supabase.table("Sequences").select("*").eq("shape_mapping", shape_mapping).execute().data
        if shape and matrix:
            return shape_mapping
    return None

def get_random_shape_in_db(n):
    shape_id = False
    print("Getting random shape from database...")
    while not shape_id:
        matrix, shape_id = sample_from_json(n)
        shape_id = check_shape(shape_id)
    print("Shape found!")
    return matrix





        
    
def db_energy_function(shape_mapping):
    """
    Called when all info is needed on a shape in the database. Returns a dataframe with the sequences that fold into the given shape and their rankig   
    """
    db = SupabaseDB()
    # Get the sequences that fold into the given shape
    seq_list = db.supabase.table("Sequences").select("*").eq("shape_mapping", shape_mapping).execute().data
    if not seq_list:
        print("No sequences found for this shape")
        return
    
    # Sort the sequences by degeneracy
    seq_list.sort(key=lambda x: x["degeneracy"], reverse=True)
    df = pd.DataFrame(seq_list)
    # Add a ranking column
    df["ranking"] =df["degeneracy"].rank(ascending=True, method="dense")
    return df

# ========================= Adding a new column to the DB (disregard this) =========================

# This section is for adding the new "path"column to the database. 

    



if __name__ == "__main__":
    # testing the energy function
    # print(db_energy_function(-5985573905669293688))
    import time
    import matplotlib.pyplot as plt
    import numpy as np
    # Get the sequences that fold into the given shape

    
    
    