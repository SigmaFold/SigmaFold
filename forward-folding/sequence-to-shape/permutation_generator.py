import itertools


def perm_gen(length=1, base=2):
    """"Function that returns a list of all the possible permutations for a given sequence length and a given
    number of possible units. HP lattice by default"""

    if base == 3:
        residues = 'HPA'
    else:
        residues = 'HP'

    perm_list = []
    product_list = list(itertools.product(residues, repeat=length))
    for product in product_list:
        product_str = ''.join(product)
        perm_list.append(product_str)

    return perm_list
