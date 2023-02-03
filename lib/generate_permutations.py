"""
Defines toolset to generate sequence permutations - for now it is a naive implementation that is in need of optimisation.
"""

import time
from itertools import permutations
import sys, os

# Set current working directory to be 3 levels above the current file
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # THIS WILL BREAK IF YOU MOVE FILES AROUND

from lib.tools import profile


@profile
def perm_gen(length=1, base=2):
    """Function that returns a list of all the possible permutations for a given sequence length and a given
    number of possible units. HP lattice by default"""

    # Generate a list of all binary sequences of length n
    initial_chain = []
    for i in range(base ** length):
        initial_chain.append(bin(i)[2:].zfill(length))
    # formatted_chain = conv_to_lattice(initial_chain)
    formatted_chain = conv_to_lattice_degen(initial_chain)
    return formatted_chain


def conv_to_lattice(int_chain):
    """Function that replaces the numerical bases with the alphabetical names"""
    formatted_chain = []
    for sequence in int_chain:
        sequence = sequence.replace('0', 'P')
        sequence = sequence.replace('1', 'H')
        formatted_chain.append(sequence)
    return formatted_chain


def conv_to_lattice_degen(int_chain):
    """Function that replaces the numerical bases with the alphabetical names while removing clearly degenerate sequences"""
    formatted_chain = []
    n = len(int_chain[0])

    for sequence in int_chain:
        # Ensuring that sequences that have Hs only in even or odd positions are not added to the list because it is degenerate
        formatted_seq = []
        # print(n)
        H_indices_odd = []
        H_indices_even = []
        for i in range(n):
            if sequence[i] == '0':
                formatted_seq.append('P')
            else:
                formatted_seq.append('H')
                if i % 2 == 0:
                    H_indices_even.append(i)
                else:
                    H_indices_odd.append(i)

        threshold = 0.9
        even_length = len(H_indices_even)
        odd_length = len(H_indices_odd)
        if (1 - threshold) * n < (even_length + odd_length) < threshold * n:
            if even_length > 0 and odd_length > 0:
                if (even_length + odd_length == 2) and (abs(H_indices_even[0] - H_indices_odd[0]) > 1):
                    formatted_chain.append(''.join(formatted_seq))
                elif even_length + odd_length == 3:
                    if even_length > odd_length:
                        if abs(H_indices_even[0] - H_indices_odd[0]) > 1 or abs(
                                H_indices_even[1] - H_indices_odd[0]) > 1:
                            formatted_chain.append(''.join(formatted_seq))
                    else:
                        if abs(H_indices_even[0] - H_indices_odd[0]) > 1 or abs(
                                H_indices_even[0] - H_indices_odd[1]) > 1:
                            formatted_chain.append(''.join(formatted_seq))
                else:
                    formatted_chain.append(''.join(formatted_seq))

    return formatted_chain


if __name__ == "__main__":
    start = time.time()
    print(perm_gen(20, 2))

    end = time.time()
    print(f'Time taken: {end - start}')
