def perm_gen(length=1, base=2):
    """"Function that returns a list of all the possible permuations for a given sequence length and a given
    number of possible units. HP lattice by default"""

    initial_chain = [conv_base(n, base, length) for n in range(base**length)]
    formatted_chain = conv_to_lattice(initial_chain)
    # print(formatted_chain)
    formatted_chain = list(dict.fromkeys(formatted_chain))
    return formatted_chain

def conv_base(n,b, l):
    """Function that converts a base10 number into any other base"""

    # Initialising the final list
    digits = list()

    while n:
        digits.insert(0, n % b)
        n = n // b

    # This it to convert to 8bit but should be changed later
    while len(digits) < l:
        digits.insert(0, 0)

    return magic(digits)

def magic(numList):
    """"Function that converts a list of digits into a string"""

    s = ''.join(map(str, numList))
    return s

def conv_to_lattice(int_chain):
    """Function that replaces the numerical bases with the alphabetical names"""
    formatted_chain = []
    for sequence in int_chain:
        sequence = sequence.replace('0', 'P')
        sequence = sequence.replace('1', 'H')
        formatted_chain.append(sequence)
    return formatted_chain


if __name__ == "__main__":
    perm_gen(2,2)