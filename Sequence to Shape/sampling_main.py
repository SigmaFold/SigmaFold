import matplotlib.pyplot as plt

from permutation_generator import perm_gen
from path_generator import handle_sequence

def get_optimal_sequence(length=1, model=2):
    stable_sequence_list = []
    sequences_list = perm_gen(length, model)
    stabilty_list = []
    for sequence in sequences_list:
        [sequence_stability, stable_sequence_paths] = handle_sequence(sequence)
        stabilty_list.append(sequence_stability)
    optimal_stability = min(stabilty_list)
    print(stabilty_list.count(optimal_stability))
    indices = [i for i, x in enumerate(stabilty_list) if x == optimal_stability]

    print(f'Among all sequences of length {length} units, there are {len(indices)}:')
    for index in indices:
        print(sequences_list[index])
    print(f'Each of them has {optimal_stability} stable configurations')
    print(stable_sequence_paths)
    print(len(stable_sequence_paths))
    return stable_sequence_paths


def plot_sequences(stable_sequence_paths):
    sequence_length = len(stable_sequence_paths[0])
    fig, axs = plt.subplots(int(len(stable_sequence_paths) / 4), 4)
    for i in range(0, int(len(stable_sequence_paths) / 4)):
        for j in range(0, 4):
            axs[i, j].plot(*zip(*stable_sequence_paths[(i * 4) + j]), marker='.')
            # axs[i, j].grid()
    plt.setp(axs, xlim=[-sequence_length, sequence_length], ylim=[-sequence_length, sequence_length])
    plt.show()

if __name__=='__main__':
    stable_paths = get_optimal_sequence(4, 2)
    plot_sequences(stable_paths)