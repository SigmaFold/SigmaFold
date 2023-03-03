import json
from db.supabase_setup import SupabaseDB


def import_data_from_json(n):
    """ Imports data from json files and returns lists of dicts"""
    with open(f"data/{n}/seq_{n}.json", "r") as f:
        seq_list = json.load(f)
        print("Parsed seq_list")
    with open(f"data/{n}/shape_{n}.json", "r") as f:
        shape_list = json.load(f)
        print("Parsed shape_list")
    
    try:
        commit_to_supabase(shape_list, seq_list)
    except Exception as e:
        print("Error: ", e)
        print("Data not added to database")
        return
    return shape_list, seq_list


    # Add all the data to the database
def commit_to_supabase(shape_list, seq_list):
    """ Adds all the data to the database asynchronously"""
    # Create a client
    db = SupabaseDB()
    # Add all the data to the database
    try:
        # insert if it doesn't exist
        # db.supabase.table("Shapes").insert(shape_list, upsert=True).execute()

        db.supabase.table("Sequences").insert(seq_list, upsert=True).execute()
    except Exception as e:
        # try again halving the data
        print("Error: ", e)
        print("Data not added to database")
        commit_to_supabase(shape_list[:len(shape_list)//2], seq_list[:len(seq_list)//2])
        commit_to_supabase(shape_list[len(shape_list)//2:], seq_list[len(seq_list)//2:])

        
        return
    print("Data added to database")


# Run a query to a sql database



if __name__ == '__main__':
    for n in range(1,10):
        print("Adding data for length: ", n)
        import_data_from_json(n)
