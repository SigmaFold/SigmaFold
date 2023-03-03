import sys 
import os

# Set current working directory to be 3 levels above the current file
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # THI

from lib.native_fold import *
import json

def execute_and_save_native_fold(n):
    fold = fold_n(n)

    # save the fold as a json file
    with open(f"data/folds/fold_{n}.json", "w") as f:
        json.dump(fold, f)
    
def read_fold_from_json(n):
    with open(f"data/folds/fold_{n}.json", "r") as f:
        fold = json.load(f)
    
    # convert every coordinate in the nest to tuples
    for i, path in enumerate(fold):
        fold[i] = [tuple(coord) for coord in path]

    return fold

if __name__ == "__main__":
    n = 27
    execute_and_save_native_fold(n)
    print(f"Done saving fold_{n}.json")