import numpy as np
import random as rnd

def generate_path(seq_len=int(10)):
    half_len = int(round(seq_len/2))
    print(half_len)
    # compute triangle
    bounds = np.tril(np.ones([half_len, half_len]), 0)

    shape = np.zeros([half_len, half_len], dtype=int)
    
    dirs = ((0,1), (0, -1), (1, 0), (-1, 0))
    bounds = np.pad(bounds, 1)
    shape = np.pad(shape, 1)
    

    path_len = 2
    shape[-2, 1] = 1
    shape[-2, 2] = 1

    i,j=(half_len-1), 2

    while (path_len) < seq_len:
        print("hey")
        cur_dir = rnd.choice(dirs)
        i, j = i+cur_dir[0], j+cur_dir[1]
        dirs2 = [(0,1), (0, -1), (1, 0), (-1, 0)]

        while (bounds[i, j] == 0) or (shape[i, j] == 1): # if steps into void or path already taken, monke stupid
            i, j = i-cur_dir[0], j-cur_dir[1]
            dirs2.remove(cur_dir) # monke learns
            if len(dirs2) == 0: # check if action has run out
                # help_im_stuck += 1
                print('im stuck')
                i,j=(half_len-1), 2 # back to beginning

                shape = np.zeros([half_len, half_len], dtype=int)
                shape[-2, 1] = 1
                shape[-2, 2] = 1
                path_len = 2
                break
            else:
                cur_dir = rnd.choice(dirs2)# regenerate step
                i, j = i+cur_dir[0], j+cur_dir[1] # monke rethinks
        shape[i, j] = 1
        path_len += 1
    print(shape)

if __name__=='__main__':
    generate_path()