import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from utils.validation_data_processor import process_inbound_validation_data, process_outbound_validation_data, process_cumulative_count

# font = {'family' : 'normal',
#         'weight' : 'bold',
#         'size'   : 10}

# matplotlib.rc('font', **font)

fig, axs = plt.subplots(2, 2)

extrapolation = process_inbound_validation_data("./data_saw/validation_data_extrapolation.json")
interpolation = process_inbound_validation_data("./data_saw/validation_data_gigamodel.json")

axs[0, 0].plot(list(interpolation.keys()), interpolation.values(), color=[0, 0.4470, 0.7410])
axs[0, 0].set_title('Interpolation')
axs[0, 0].set(xlabel="Minimum Degeneracy", ylabel="Average number of trials")


axs[0, 1].plot(list(extrapolation.keys()), extrapolation.values(), color=[0, 0.4470, 0.7410])
axs[0, 1].set_title('Extrapolation')
axs[0, 1].set(xlabel="Minimum Degeneracy", ylabel="Average number of trials")

extrapolation = process_cumulative_count("./data_saw/validation_data_extrapolation.json")
interpolation = process_cumulative_count("./data_saw/validation_data_gigamodel.json")

axs[1, 0].bar(list(interpolation.keys()), interpolation.values(), color=[0, 0.4470, 0.7410], width=2)
# axs[1, 0].set_title('Interpolation')
axs[1, 0].set(xlabel="Minimum Degeneracy", ylabel="Ratio of solved shapes (%)")


axs[1, 1].bar(list(extrapolation.keys()), extrapolation.values(), color=[0, 0.4470, 0.7410], width=2)
# axs[1, 1].set_title('Extrapolation')
axs[1, 1].set(xlabel="Minimum Degeneracy", ylabel="Ratio of solved shapes (%)")
plt.show()