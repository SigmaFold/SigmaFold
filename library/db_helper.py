"""
Provides a set of functions useful for saving, loading or manipulating data in the database.
"""

from supabase import Client, create_client
from supabase.lib.client_options import ClientOptions
import os
from dotenv import load_dotenv
import numpy as np
from random import randint
import json 
import pandas as pd
from tabulate import tabulate
import sys 
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
    client_options = ClientOptions(postgrest_client_timeout=600.0)

    supabase: Client = create_client(url, key, options=client_options)

# ========================= JSON Data Saving Toolkit =========================
def upload_data(n):
    """ Imports data from json files and returns lists of dicts
    PREQUESITE: You must have ran native_fold for your n of choice and have the json files in the data folder.
    
    :params
    :int: n: the length of the sequences to be returned.
    """
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
    if retries > 20:
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

# ========================= Adding a new column to the DB (disregard this) =========================

# This section is for adding the new "path"column to the database. 

    



if __name__ == "__main__":
    # testing the energy function
    # print(db_energy_function(-5985573905669293688))
    import time
    import matplotlib.pyplot as plt
    import numpy as np
    # Get the sequences that fold into the given shape

    
    
    