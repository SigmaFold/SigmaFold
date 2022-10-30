import matplotlib.pyplot as plt

from permutation_generator import perm_gen
from path_generator import handle_sequence, remove_duplicates


def get_optimal_sequence(length=1, model=2):
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

    optimal_stability = min(stability_list)  # Finds the lowest number of stable configurations in stability_list
    print(stability_list.count(optimal_stability))

    # Creates a list with the indices of all the sequences with the lowest number of stable configurations
    indices = [i for i, x in enumerate(stability_list) if x == optimal_stability]
    print(f'Among all sequences of length {length} units, there are {len(indices)}:')

    for index in indices:
        optimal_sequences.append(sequences_list[index])
        filtered_stable_path = remove_duplicates(stable_sequence_path_list[index])
        optimal_sequences_filtered_paths.append(filtered_stable_path)
        # print(sequences_list[index])  # Sequences with lowest number of stable configurations
        # print(stable_sequence_path_list[
        #           index])  # Stable paths of the sequences with the lowest number of stable configurations
        print(f'The sequence of "{sequences_list[index]}" has {len(filtered_stable_path)} stable paths')
    print(f'Each of them has {optimal_stability} stable configurations')

    for i in range(len(optimal_sequences)):
        print(optimal_sequences[i])
        print(optimal_sequences_filtered_paths[i])
    # print(stable_sequence_paths)
    # print(len(stable_sequence_paths))
    return optimal_sequences, optimal_sequences_filtered_paths


# def plot_sequences(stable_sequence_paths):
#     sequence_length = len(stable_sequence_paths[0])
#     fig, axs = plt.subplots(int(len(stable_sequence_paths) / 4), 4)
#     for i in range(0, int(len(stable_sequence_paths) / 4)):
#         for j in range(0, 4):
#             axs[i, j].plot(*zip(*stable_sequence_paths[(i * 4) + j]), marker='.')
#             # axs[i, j].grid()
#     plt.setp(axs, xlim=[-sequence_length, sequence_length], ylim=[-sequence_length, sequence_length])
#     plt.show()


if __name__ == '__main__':
    stable_paths = get_optimal_sequence(4, 2)
    plot_sequences(stable_paths)
