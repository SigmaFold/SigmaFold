import json
from db.supabase_setup import SupabaseDB
import sys 
import os 




def import_data_from_json(n):
    """ Imports data from json files and returns lists of dicts"""

    with open(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + f"/data/{n}/seq_{n}.json", "r") as f:
        seq_list = json.load(f)
        print("Parsed seq_list")
    with open(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + f"/data/{n}/shape_{n}.json", "r") as f:
        shape_list = json.load(f)
        print("Parsed shape_list")

    with open(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + f"/data/{n}/map_{n}.json", "r") as f:
        mapping_list = json.load(f)
        print("Parsed mapping_list")
    
    try:
        commit_to_supabase(shape_list, seq_list, mapping_list)
    except Exception as e:
        print("Error: ", e)
        print("Data not added to database")
        return
    return shape_list, seq_list, mapping_list

        



    # Add all the data to the database
def commit_to_supabase(shape_list, seq_list, mapping_list):
    """ Adds all the data to the database asynchronously"""
    # Create a client
    db = SupabaseDB()
    # Add all the data to the database
    try:
        # insert if it doesn't exist
        db.supabase.table("Sequences").insert(seq_list, upsert=True).execute()
        db.supabase.table("Shapes").insert(shape_list, upsert=True).execute()
        db.supabase.table("Mappings").insert(mapping_list, upsert=True).execute()
    except Exception as e:
        # try again halving the data
        print("Error: ", e)
        print("Data not added to database")
        commit_to_supabase(shape_list[:len(shape_list)//2], seq_list[:len(seq_list)//2], mapping_list[:len(mapping_list)//2])
        commit_to_supabase(shape_list[len(shape_list)//2:], seq_list[len(seq_list)//2:], mapping_list[len(mapping_list)//2:])

        
        return
    print("Data added to database")



if __name__ == '__main__':
    n = 15
    print("Adding data for length: ", n)
    import_data_from_json(n)
