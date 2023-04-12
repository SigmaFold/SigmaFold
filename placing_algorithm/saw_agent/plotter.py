"""Harry Plotter goes to school"""
import json # et la toison d'or
import numpy as np
import matplotlib.pyplot as plt

with open("./logs/gigamodel/fov_1_test/degen_histo.json") as json_file:
    raw_data = json.load(json_file)
    corrected_type_data = {int(k): int(v) for k, v in raw_data.items()}
    max_entry = max(corrected_type_data.keys())
    gap_filled = dict()
    for i in range(max_entry+1):
        try:
            gap_filled[i] = corrected_type_data[i]
        except KeyError:
            gap_filled[i] = 0
    cleared = gap_filled

with open("./logs/gigamodel/fov_1_test/nb_not_cleared.json") as json_file:
    raw_data = json.load(json_file)
    corrected_type_data = {int(k): int(v) for k, v in raw_data.items()}
    max_entry = max(corrected_type_data.keys())
    gap_filled = dict()
    for i in range(max_entry+1):
        try:
            gap_filled[i] = corrected_type_data[i]
        except KeyError:
            gap_filled[i] = 0
    uncleared = gap_filled

bottom = np.zeros((max_entry+1,))
for i in range(max_entry):
    bottom[i] = uncleared[i] # here select which one is below

width = 1.3
plt.bar(list(uncleared.keys()), uncleared.values(), color=[0.85, 0.13, 0.13], width=width)
plt.bar(list(cleared.keys()), cleared.values(), bottom=bottom, color=[0.133, 0.612, 0.114], width=width)
plt.xlabel("Degeneracy")
plt.ylabel("Number of shapes")
plt.legend(['Not cleared', 'Cleared'])
plt.show()
