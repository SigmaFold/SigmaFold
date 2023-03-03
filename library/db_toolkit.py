"""
Provides a set of functions useful for saving, loading or manipulating data in the database.
"""

from supabase import Client, create_client
import os
import psycopg2
from dotenv import load_dotenv
import numpy as np
from random import randint
import json 

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

# ========================= Useful Queries =========================
def db_energy_function(seq_id):
    """ Energy function using the database
    Ruleset: 
        - If the shape sequence doesn't map into the target shape, return -Infinity
        - If the shape sequence maps into the target shape, return the energy field and the degeneracy
    
        The seq_id encaspulates both the sequence and the shape_id, so if it exists in the database, it means that mapping exists.
    """

    db = SupabaseDB()
    
    # Find sequence match
    seq_match = db.supabase.table("Sequences").select("*").eq("sequence_id", seq_id).execute()
    if seq_match.data == None:
        return float("-inf")
    else:
        # If there are matches, return the energy and degeneracy
        return seq_match.data[0]["energy"], seq_match.data[0]["degeneracy"]
    



if __name__ == "__main__":
    # testing the energy function
    print(db_energy_function(4141209559943024073))

    # Use this section to upload data of a certain size to the database
    for n in range(9, 13):
        print(f"Uploading data for n = {n}")
        upload_data(n)


    