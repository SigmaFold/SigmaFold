"""
Nabeel's code to plot optimal sequences and stable paths and a given n - HOWEVER IT IS CURRENTLY BROKEN AS IT NEEDS REFACTORING TO IMPORT THE NEW LIB/ FOLDER STRUCTURE
"""


from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import numpy as np
import time
import sys, os

# Set current working directory to be 3 levels above the current file
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) # THIS WILL BREAK IF YOU MOVE FILES AROUND
from lib.generate_permutations import perm_gen


def get_optimal_path_sequence(length=1, model=2):
    """Permutes all the sequences of input length and model. Identifies the sequences that have the least number of
    stable configurations and returns the sequences and the stable paths"""


    stable_sequence_path_list = []
    sequences_list = perm_gen(length, model)  # list of all possible sequences with a certain length
    stability_list = []
    optimal_sequences = []
    optimal_sequences_filtered_paths = []

    for sequence in sequences_list:
        [sequence_stability, stable_sequence_paths] = handle_sequence(
            sequence)  # Gets number of stable configurations and the stable paths for each sequence
        stability_list.append(
            sequence_stability)  # adds number of stable configurations of each sequence to stability_list
        stable_sequence_path_list.append(
            stable_sequence_paths)  # adds the paths of stable configuration of each sequence to
        # stable_sequence_path_list

    optimal_stability = min(
        stability_list)  # Finds the lowest number of stable configurations (includes rotations and reflections) in
    # stability_list
    # print(stability_list.count(optimal_stability))

    # Creates a list with the indices of all the sequences with the lowest number of stable configurations
    indices = [i for i, x in enumerate(stability_list) if x == optimal_stability]

    for index in indices:
        optimal_sequences.append(sequences_list[index])
        filtered_stable_path = remove_duplicates(
            stable_sequence_path_list[index])  # rotated and reflected paths are removed
        optimal_sequences_filtered_paths.append(filtered_stable_path)
    print(
        f'Among all sequences of length {length} units, there are {len(indices)} sequences with '
        f'{len(filtered_stable_path)} stable configuration(s):')

    for i in range(len(optimal_sequences)):
        print(i + 1, optimal_sequences[i])
        print(optimal_sequences_filtered_paths[i])
    print(optimal_sequences)
    print(optimal_sequences_filtered_paths)
    return optimal_sequences, optimal_sequences_filtered_paths


def get_optimal_shape_sequence(length=1, model=2):
    stability_list = []
    stable_sequence_path_list = []
    filtered_sequence_path_list = []
    sequences_list = perm_gen(length, model)  # list of all possible sequences with a certain length

    for sequence in sequences_list:
        [sequence_stability, stable_sequence_paths] = handle_sequence(
            sequence)  # Gets number of stable configurations and the stable paths for each sequence
        stability_list.append(
            sequence_stability)  # adds number of stable configurations of each sequence to stability_list
        stable_sequence_path_list.append(
            stable_sequence_paths)  # adds the paths of stable configuration of each sequence to
        # stable_sequence_path_list

    # Removes the rotated and reflected paths
    for sequence_paths in stable_sequence_path_list:
        filtered_sequence_path_list.append(remove_duplicates(sequence_paths))

    # Finding the paths that form the same shape for each sequence
    shape_count = []
    sequence_unique_shape_paths = []
    for unique_paths in filtered_sequence_path_list:
        shape_paths = []
        for path in unique_paths:
            shape_paths.append(sorted(path))  # sorts each path for every sequence
        shape_path_set = set(
            tuple(i) for i in shape_paths)  # puts all the paths for each sequence in a set to remove duplicate shapes
        unique_shape_paths = [list(tup) for tup in
                              shape_path_set]  # creates a list of paths for each sequence with unique shapes
        sequence_unique_shape_paths.append(
            unique_shape_paths)  # adds the unique shape path list to a central list for all permutations
        shape_count.append(
            len(unique_shape_paths))  # adds the minimum number of unique shapes of each sequence to a central list for all permutations
    # print(sequence_unique_shape_paths)
    # print(shape_count)

    min_shape_count = min(shape_count)  # finds the number of minimum shape is for a sequence of length 'length'
    indices = [i for i, x in enumerate(shape_count) if
               x == min_shape_count]  # creates a list of indices for all sequences that have the minimum number of unique shapes

    optimal_sequences = []
    optimal_sequences_shape_paths = []
    for index in indices:
        optimal_sequences.append(sequences_list[index])
        optimal_sequences_shape_paths.append(sequence_unique_shape_paths[index])

    print(min_shape_count)
    print(optimal_sequences)
    print(optimal_sequences_shape_paths)

    return optimal_sequences, optimal_sequences_shape_paths


def plot_sequences(sequence_list, stable_sequence_paths):
    """Plots all the optimal sequences and their optimal paths"""
    sequence_length = len(sequence_list[0])
    ticks = np.arange(-sequence_length, sequence_length, 1)  # array to set up x-ticks and y-ticks
    # Building the legend
    legend_elements = [Line2D([0], [0], marker='.', color='grey', markerfacecolor='red', label='H'),
                       Line2D([0], [0], marker='.', color='grey', markerfacecolor='blue', label='P')]

    # Creating a figure which produces a column of stable configurations for every optimal sequence
    fig, axs = plt.subplots(len(stable_sequence_paths[0]), len(sequence_list))
    for i in range(0, len(sequence_list)):

        # Creating a list to color 'H' markers red and 'P' markers blue
        sequence_split = list(sequence_list[i])
        for index in range(len(sequence_split)):
            if sequence_split[index] == 'H':
                sequence_split[index] = 'red'
            elif sequence_split[index] == 'P':
                sequence_split[index] = 'blue'

        # Generating the plot
        if (len(stable_sequence_paths[0]) != 1) and (len(sequence_list) != 1):
            for j in range(0, len(stable_sequence_paths[0])):
                # axs[j, i].plot(*zip(*stable_sequence_paths[i][j]), c='grey')  # to display the bonds
                axs[j, i].scatter(*zip(*stable_sequence_paths[i][j]), c=sequence_split,
                                  marker='.')  # to display the H and P markers
                axs[j, i].set_xticks(ticks, minor=True)
                axs[j, i].set_yticks(ticks, minor=True)
                axs[j, i].grid(which='both')
                if j == 0:
                    axs[j, i].set_title(sequence_list[i])

        elif (len(stable_sequence_paths[0]) == 1) and (len(sequence_list) != 1):
            axs[i].plot(*zip(*stable_sequence_paths[i][0]), c='grey')  # to display the bonds
            axs[i].scatter(*zip(*stable_sequence_paths[i][0]), c=sequence_split,
                           marker='.')  # to display the H and P markers
            axs[i].set_xticks(ticks, minor=True)
            axs[i].set_yticks(ticks, minor=True)
            axs[i].grid(which='both')
            axs[i].set_title(sequence_list[i])

        elif (len(stable_sequence_paths[0]) != 1) and (len(sequence_list) == 1):
            for j in range(0, len(stable_sequence_paths[0])):
                axs[j].plot(*zip(*stable_sequence_paths[0][j]), c='grey')  # to display the bonds
                axs[j].scatter(*zip(*stable_sequence_paths[0][j]), c=sequence_split,
                               marker='.')  # to display the H and P markers
                axs[j].set_xticks(ticks, minor=True)
                axs[j].set_yticks(ticks, minor=True)
                axs[j].grid(which='both')
                axs[j].set_title(sequence_list[0])

        elif (len(stable_sequence_paths[0]) == 1) and (len(sequence_list) == 1):
            axs[0].plot(*zip(*stable_sequence_paths[0][0]), c='grey')  # to display the bonds
            axs[0].scatter(*zip(*stable_sequence_paths[0][0]), c=sequence_split,
                           marker='.')  # to display the H and P markers
            axs[0].set_xticks(ticks, minor=True)
            axs[0].set_yticks(ticks, minor=True)
            axs[0].grid(which='both')
            axs[0].set_title(sequence_list[0])

    fig.suptitle(f'Optimal sequences and their paths: Sequence length {sequence_length}')
    fig.legend(handles=legend_elements, loc='upper right')  # Placing the legend
    plt.setp(axs, xlim=[-sequence_length, sequence_length],
             ylim=[-sequence_length, sequence_length])  # Setting x-axis and y-axis ranges
    plt.show()


if __name__ == '__main__':
    # Getting optimal sequences with least unique shapes
    start = time.time()
    opt_seq, opt_paths = get_optimal_shape_sequence(10, 2)
    plot_sequences(opt_seq, opt_paths)
    end = time.time()
    print(f'The time taken was: {end - start}')

    # # Getting optimal sequences with the least unique paths
    # start = time.time()
    # opt_seq, opt_paths = get_optimal_sequence(9, 2)
    # plot_sequences(opt_seq, opt_paths)
    # end = time.time()
    # print(f'The time taken was: {end - start}')

    # stability, stable_paths = handle_sequence('HHHHHHHHH')
    # print(stability)
    # print(stable_paths)
    # print(len(stable_paths))
    # filtered_paths = remove_duplicates(stable_paths)
    # print(filtered_paths)
    # print(len(filtered_paths))
    # plot_sequences(['HHHHHHHHH'], [filtered_paths])
