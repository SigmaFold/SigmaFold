"""
Collection of functions used by 
"""

# TODO: do not check deviation if degen > 5000000

import numpy as np
import random as rnd
import scipy as sc
import matplotlib.pyplot as plt
import math

def generate_shape(seq_len=int(10)):

    # maximum dimension
    half_len = int(round(seq_len/2))

    # from another piece of code
    half_bound = int(math.ceil(seq_len/2))
    bound = 2*half_bound+1

    # compute triangle constraint
    bounds = np.tril(np.ones([half_len, half_len], dtype=int), 0) # boundary for reference
    shape = np.zeros([half_len, half_len], dtype=int) # shape for output
    bounds = np.pad(bounds, 1) # padding to account for void
    shape = np.pad(shape, 1)
    
    # possible moves
    dirs = ((0,1), (0, -1), (1, 0), (-1, 0))

    # initialising
    shape[-2, 1] = 1 # bottom left of triangle
    shape[-2, 2] = 1 # first move is definitely right
    i, j = half_len, 2 # i = row, j = col
    path_len = np.count_nonzero(shape)# initial path length
    monke_stupid_index = 0 # how stupid monke is

    while (path_len) < seq_len:
        cur_dir = rnd.choice(dirs) # chooses a random move (monke thinks)
        i, j = i + cur_dir[0], j + cur_dir[1] # update coordinates (monke's proposed move)

        # check if move viable (monke checks)
        dirs2 = [(0,1), (0, -1), (1, 0), (-1, 0)] # temporary list for remaking decisions
        while (bounds[i, j] == 0) or (shape[i, j] == 1): # if steps into void or path already taken, monke stupid
            i, j = i-cur_dir[0], j-cur_dir[1] # monke forgets
            dirs2.remove(cur_dir) # monke learns

            if len(dirs2) == 0: # moves have run out
                monke_stupid_index += 1
                i,j = half_len, 2 # resetting coordinate to beginning
                shape = np.pad(np.zeros([half_len, half_len], dtype=int), 1) # resetting shape & path length
                shape[-2, 1] = 1
                shape[-2, 2] = 1
                path_len = np.count_nonzero(shape)
                break

            else: # still have available moves
                cur_dir = rnd.choice(dirs2)# pick another move
                i, j = i + cur_dir[0], j + cur_dir[1]

        # move viable
        shape[i, j] = 1 # monke moves
        path_len = np.count_nonzero(shape)

    # print(f"monke got stuck {monke_stupid_index} times")
    aligned_target = align_target(shape, bound, half_bound)
    return aligned_target

def legacy_tweaking_reward(folds: list, target, degen: int, seq_length: int, curr_degen, curr_corr):
    """
    Old function that uses 
    """
    half_bound = int(math.ceil(seq_length/2))
    bound = 2*half_bound+1
    
    # Short-circuit the func is too much degen anyway
    if degen > 5_000:
        degen /= 4 # quick removal of inflation due to rotation
        diff_degen = curr_degen - degen
        reward_degen = (diff_degen)**2 * np.sign(diff_degen)
        return reward_degen, {'trunc': True}
    
    # align all folds into one stack
    fold_stack = np.zeros((degen, bound, bound))
    for i, fold in enumerate(folds):
        # find centroid
        m_c, n_c = find_centroids(fold) # need to round centroids here
        fold[m_c, n_c] = 2

        # add image to stack
        fold_stack[i,:,:] = fold[m_c-half_bound:m_c+half_bound+1, 
                                 n_c-half_bound:n_c+half_bound+1]
    
    # orientation invariant screening
    shape_set = set()
    result_dict = {}
    for fold in fold_stack:
        m_c, n_c = find_centroids(fold)
        eig_val, eig_vect = orient_image(fold, m_c, n_c)
        temp_list = []
        for val in eig_val:
            temp_list.append(np.abs(val))
        for vect in eig_vect:
            for val in vect:
                temp_list.append(np.abs(val))
        test_fset = frozenset(temp_list)
            
        # weight matrix
        weight_matrix = np.zeros(shape=(bound, bound))
        centroid = (half_bound, half_bound)
        for index in np.ndindex(np.shape(weight_matrix)):
            distance = np.linalg.norm(np.subtract(centroid,index))
            weight_matrix[index] = distance+1

        if test_fset not in shape_set:
            shape_set.add(test_fset)
            res_list = []
            for i in range(4):    
                fold = np.rot90(fold, 1)
                # plt.figure()
                # plt.imshow(fold)
                target = align_matrix(target, fold)
                result = np.abs(np.subtract(fold, target)) * weight_matrix
                result = np.sum(result)
                res_list.append(result)
            result = min(res_list)
            result_dict[test_fset.__hash__()] = result
    
    # calculating the reward
    min_corr = min(result_dict.values())
    degen = len(result_dict.keys())

    info = {
        'degen': degen,
        'corr': min_corr - 1, # to remove the "2" error cause by displaying yellow pixel for center
    }
    print(info)
    weight_degen = 1 if (curr_degen > 50) else curr_degen/50
    diff_dev = curr_corr - min_corr # positive (good) if deviation has decreased
    diff_degen = curr_degen - degen  # positive (good) if degeneracy has decreased
    reward_dev = (1-weight_degen) * (diff_dev)**2 * np.sign(diff_dev)
    reward_degen = weight_degen * (diff_degen)**2 * np.sign(diff_degen)
    reward = reward_dev + reward_degen
    print(f'Reward is {reward} !')
    return reward, info

def align_matrix(og_shape, template):
    template_c = find_centroids(template) # centroids of template
    # print(f"centroids of template is {template_c}")
    og_c = find_centroids(og_shape) # centroids of og shape
    new_shape = np.zeros(np.shape(template)) # new shape same dimension as template
    diff = np.subtract(template_c, og_c) # difference to align centers

    # iterate through each element in original shape
    for index in np.ndindex(np.shape(og_shape)):
        if og_shape[index[0]][index[1]] == 1:
            new_coord = index + diff
            new_shape[new_coord[0]][new_coord[1]] = 1

    return new_shape

def align_target(target, bound, half_bound):
    template = np.zeros(shape=(bound, bound), dtype=np.uint8)
    target_centroids = find_centroids(target)
    diff = np.subtract([half_bound,half_bound], list(target_centroids))
    for index in np.ndindex(np.shape(target)):
        new_coord = index + diff
        template[new_coord[0], new_coord[1]] = target[index] # transformed matrix for comparison
    return template

def find_centroids(image):
    """Returns centroids of int"""
    zeroth_neutral = np.sum(image)
    zeroth_moments = [np.sum(x) for x in np.nonzero(image)]
    m_centroid, n_centroid = (np.array(zeroth_moments)/zeroth_neutral)
    m_centroid = math.floor(m_centroid)
    n_centroid = math.floor(n_centroid)
    return m_centroid, n_centroid

def orient_image(image, m_c, n_c):
    µ_20 = np.sum((np.nonzero(image)[0] - m_c)**2)
    µ_02 = np.sum((np.nonzero(image)[1] - n_c)**2)
    µ_11 = np.sum(
        (np.nonzero(image)[0] - m_c)*(np.nonzero(image)[1] - n_c))
    µ_matrix = np.array([[µ_20, µ_11], [µ_11, µ_02]])
    eig_val, eig_vect = np.linalg.eig(µ_matrix)

    return eig_val, eig_vect

def concurrent_reward():
    """
    Implements another possible reward function, based on the idea of 
    equilibrium. Will write more after discussion with group
    """
    pass

