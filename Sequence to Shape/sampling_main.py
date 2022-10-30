from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import numpy as np

from permutation_generator import perm_gen
from path_generator import handle_sequence, remove_duplicates


def get_optimal_sequence(length=1, model=2):
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
    # print(optimal_sequences)
    # print(optimal_sequences_filtered_paths)
    return optimal_sequences, optimal_sequences_filtered_paths


def plot_sequences(sequence_list, stable_sequence_paths):
    """Plots all the optimal sequences and their optimal paths"""
    sequence_length = len(sequence_list[0])
    ticks = np.arange(-sequence_length, sequence_length, 1)  # array to set up xticks and yticks
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
        if len(stable_sequence_paths[0]) != 1:
            for j in range(0, len(stable_sequence_paths[0])):
                axs[j, i].plot(*zip(*stable_sequence_paths[i][j]), c='grey')  # to display the bonds
                axs[j, i].scatter(*zip(*stable_sequence_paths[i][j]), c=sequence_split,
                                  marker='.')  # to display the H and P markers
                axs[j, i].set_xticks(ticks, minor=True)
                axs[j, i].set_yticks(ticks, minor=True)
                axs[j, i].grid(which='both')
                if j == 0:
                    axs[j, i].set_title(sequence_list[i])
        else:
            axs[i].plot(*zip(*stable_sequence_paths[i][0]), c='grey')  # to display the bonds
            axs[i].scatter(*zip(*stable_sequence_paths[i][0]), c=sequence_split,
                           marker='.')  # to display the H and P markers
            axs[i].set_xticks(ticks, minor=True)
            axs[i].set_yticks(ticks, minor=True)
            axs[i].grid(which='both')
            axs[i].set_title(sequence_list[i])

    fig.suptitle(f'Optimal sequences and their paths: Sequence length {sequence_length}')
    fig.legend(handles=legend_elements, loc='upper right')  # Placing the legend
    plt.setp(axs, xlim=[-sequence_length, sequence_length],
             ylim=[-sequence_length, sequence_length])  # Setting x axis and y axis ranges
    plt.show()


if __name__ == '__main__':
    opt_seq, opt_paths = get_optimal_sequence(2, 2)
    plot_sequences(opt_seq, opt_paths)
