"""
File that implements modularity for reward function
"""

import numpy as np
import random as rnd
import scipy as sc
import matplotlib.pyplot as plt
import math
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(
    os.path.dirname(
    os.path.dirname(
    os.path.dirname(
    os.path.dirname(
    os.path.dirname(
    os.path.abspath(__file__)))))))

import inv_env.envs.aux_functions as aux
import library.native_fold as nf
def ranking_reward():
    pass

def legacy_tweaking_reward(env, folds: list, target, degen: int, seq_length: int, curr_degen, curr_corr):
    """
    Old function that uses 
    """
    
    def initial_data():
        env.paths = nf.fold_n(env.seq_length)

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
        m_c, n_c = aux.find_centroids(fold) # need to round centroids here
        fold[m_c, n_c] = 2

        # add image to stack
        fold_stack[i,:,:] = fold[m_c-half_bound:m_c+half_bound+1, 
                                 n_c-half_bound:n_c+half_bound+1]
    
    # orientation invariant screening
    shape_set = set()
    result_dict = {}
    for fold in fold_stack:
        m_c, n_c = aux.find_centroids(fold)
        eig_val, eig_vect = aux.orient_image(fold, m_c, n_c)
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
                target = aux.align_matrix(target, fold)
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