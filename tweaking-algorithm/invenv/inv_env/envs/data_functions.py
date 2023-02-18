# File with all necessary functions for type conversion, which is quite
# annoying in the envionrment...

import numpy as np

def fold_list2matrix(fold, length):
    """
    Method to convert a fold (list of coordinate) into a np.ndarray.
    The size is twice the length of the sequence to avoid clipping/warping.
    """

    n = length*2+1 # always odd number
    m = length*2+1
    # Convert fold to matrix for further analysis

    template = np.zeros((n,m))

    yoffset = (n+1)/2
    xoffset = (m+1)/2
    for base in fold[1]:
        full_coord = base
        m = int(full_coord[0]+yoffset)
        n = int(full_coord[1]+xoffset)
        try:
            template[m, n] = 1
        except IndexError:
            print(f"SHOULD NOT HAPPEN with ({m}; {n})")
            print(f"Full coordinates: {full_coord}")

    template = template.astype(int)

    return template

def seq_list2str(list):
    """Method to convert a list of 0 and 1s into a string of H and Ps"""
    new_str = ''.join(
        [str(x) for x in list]).replace('1', 'H').replace('0', 'P')
    return new_str

def seq_heur2env(seq):
    return list(seq.replace('H', '1').replace('P', '0'))
    
    