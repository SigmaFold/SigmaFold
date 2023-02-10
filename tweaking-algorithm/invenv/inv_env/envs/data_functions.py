# File with all necessary functions for type conversion, which is quite
# annoying in the envionrment...

import numpy as np

def fold_list2matrix(fold, target):
    """
    Method to convert a fold (list of coordinate) into a np.ndarray.
    It uses the target shape as the template (in terms of size).
    (0, 0) corresponds to the center of the template, so there will be
    an offset with the target. This is to be corrected.
    """

    n, m = np.shape(target)
    # Convert fold to matrix for further analysis
    template = np.zeros((n,m))
    yoffset = round(n/2)-1
    xoffset = round(m/2)-1
    
    for base in fold[1]:
        full_coord = base
        try:
            template[full_coord[0]+yoffset, full_coord[1]+xoffset] = 1
        except IndexError:
            print('Incompatible shape')

    template = template.astype(int)
    print("Hey popilopipi")
    print(template)
    return template

def seq_list2str(list):
    """Method to convert a list of 0 and 1s into a string of H and Ps"""
    new_str = ''.join(
        [str(x) for x in list]).replace('1', 'H').replace('0', 'P')
    return new_str
    