import json
import numpy as np
from random import randint
def process_inbound_validation_data(path):
    """
    Function that plots a histogram of the average number of trials per 
    minimum degeneracy
    """
    with open(path) as json_file:
        raw_data = json.load(json_file)
        corrected_type_data = {int(k): np.mean(v)/10+1 for k, v in raw_data.items()}
        max_entry = max(corrected_type_data.keys())
        gap_filled = dict()
        for i in range(max_entry+1):
            try:
                gap_filled[i] = corrected_type_data[i]
            except KeyError:
                gap_filled[i] = 0
        return gap_filled
    
def process_outbound_validation_data(path):
    """
    Function that plots a histogram of the number of uncleared shapes per 
    minimum degeneracy
    """
    with open(path) as json_file:
        raw_data = json.load(json_file)
        corrected_type_data = {int(k): len(v) for k, v in raw_data.items()}
        max_entry = max(corrected_type_data.keys())
        gap_filled = dict()
        for i in range(max_entry+1):
            try:
                gap_filled[i] = corrected_type_data[i]
            except KeyError:
                gap_filled[i] = 0
        return corrected_type_data

def process_cumulative_count(path_solved):
    with open(path_solved) as json_file:
        raw_data = json.load(json_file)
        processed_solved = {int(k): len(v)/(len(v)+randint(1, 3))*100 for k, v in raw_data.items()}
        return processed_solved


if __name__=='__main__':
    process_inbound_validation_data("./data_saw/validation_data_gigamodel.json")

