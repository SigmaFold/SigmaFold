import json
import numpy as np
import matplotlib.pyplot as plt

with open("./data_saw/validation_data.json") as json_file:
    raw_data = json.load(json_file)
    corrected_type_data = {int(k): np.mean(v) for k, v in raw_data.items()}
    max_entry = max(corrected_type_data.keys())
    gap_filled = dict()
    for i in range(max_entry+1):
        try:
            gap_filled[i] = corrected_type_data[i]
        except KeyError:
            gap_filled[i] = 0
    cleared = gap_filled