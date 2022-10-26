from permutation_generator import perm_gen
from path_generator import handle_sequence

def get_optimal_sequence(length=1, model=2):
    sequences_list = perm_gen(length, model)
    stabilty_list = []
    for sequence in sequences_list:
        sequence_stability = handle_sequence(sequence)
        stabilty_list.append(sequence_stability)
    optimal_stability = min(stabilty_list)
    print(stabilty_list.count(optimal_stability))
    indices = [i for i, x in enumerate(stabilty_list) if x == optimal_stability]

    print(f'Among all sequences of length {length} units, there are {len(indices)}:')
    for index in indices:
        print(sequences_list[index])
    print(f'Each of them has {optimal_stability} stable configurations')

if __name__=='__main__':
    get_optimal_sequence(12, 2)