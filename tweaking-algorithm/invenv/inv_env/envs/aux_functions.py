import numpy as np
import random as rnd
import scipy as sc
import matplotlib.pyplot as plt
import math

def generate_shape(seq_len=int(10)):

    # maximum dimension
    half_len = int(round(seq_len/2))

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
    return shape

def tweaking_reward(folds: list, degen: int, seq_length: int):
    displayCols = 9
    displayRows = 5
    half_bound = int(math.ceil(seq_length/2))
    bound = 2*half_bound+1

    # align all folds into one stack
    fold_stack = np.zeros((degen, bound, bound))
    print(np.shape(fold_stack))
    for i, fold in enumerate(folds):
        # find centroid
        m_c, n_c = find_centroids(fold)

        # rotate image
        orient_image(fold, m_c, n_c)
        
        # add image to stack
        fold_stack[i,:,:] = fold[m_c-half_bound:m_c+half_bound+1, 
                                 n_c-half_bound:n_c+half_bound+1]

    _, axs = plt.subplots(5, 9)
    fold_no = 0
    print(f'The degen is fuck you {degen}')
    for r in range(displayRows):
        for c in range(displayCols):
            try:
                axs[r, c].imshow(fold_stack[fold_no,:,:])
            except IndexError:
                print('C\'est la fin... du MONDE!')
                break
            fold_no += 1

    average_fold = np.average(fold_stack, axis=0)/degen
    # print(average_fold)
    plt.show()
    return 1, average_fold

def find_centroids(image):
    zeroth_neutral = np.sum(image)
    zeroth_moments = [np.sum(x) for x in np.nonzero(image)]
    m_centroid, n_centroid = np.round(np.array(zeroth_moments)/zeroth_neutral)
    return m_centroid, n_centroid

def orient_image(image, m_c, n_c):
    µ_20 = np.sum((np.nonzero(image)[0] - m_c)^2)
    µ_02 = np.sum((np.nonzero(image)[1] - n_c)^2)
    µ_11 = np.sum(
        (np.nonzero(image)[0] - m_c)*(np.nonzero(image)[1] - n_c))
    µ_matrix = np.array([[µ_20, µ_11], [µ_11, µ_02]])
    eig_val, eig_vect = np.linalg.eig(µ_matrix)
    print(eig_val, eig_vect)

    return eig_val, eig_vect

if __name__ == '__main__':
    print(generate_shape())

