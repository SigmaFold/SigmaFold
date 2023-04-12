"""Harry Plotter goes to school"""
import json
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

width = 1.2

# GREEN/RED bar plot
# plt.bar(list(uncleared.keys()), uncleared.values(), color=[0.85, 0.13, 0.13], width=width)
# plt.bar(list(cleared.keys()), cleared.values(), bottom=bottom, color=[0.133, 0.612, 0.114], width=width)
# plt.xlabel("Degeneracy")
# plt.ylabel("Number of shapes")
# plt.legend(['Not cleared', 'Cleared'])

# # RATIO bar chart
# ratio = dict()
# for i in range(max_entry+1):
#     try:
#         ratio[i] = uncleared[i]/(uncleared[i] + cleared[i])*100
#     except ZeroDivisionError:
#         ratio[i] = 0
# # [0.8500, 0.3250, 0.0980] # ORANGE
# plt.bar(list(ratio.keys()), ratio.values(), color=[0, 0.4470, 0.7410], width=width)
# plt.xlabel("Degenracy")
# plt.ylabel("Percentage of shapes not cleared")

# Compelxity distribution bar chart
ratio = dict()
for i in range(max_entry+1):
    try:
        ratio[i] = uncleared[i] + cleared[i]
    except ZeroDivisionError:
        ratio[i] = 0
# [0.8500, 0.3250, 0.0980] # ORANGE
plt.bar(list(ratio.keys()), ratio.values(), color=[0, 0.4470, 0.7410], width=width)
plt.xlabel("Minimum Degeneracy")
plt.ylabel("Number of shapes")

plt.show()
