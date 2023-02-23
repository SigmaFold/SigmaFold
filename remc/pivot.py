import numpy as np

# choosing the right VSHD move
def vsdh_move(seq, n, mat):
    # choose a random number between 1 to n inclusive
    random_number = np.random.randint(1,n+1)
    # random_number = 4
    print(f'Random number chosen: {random_number}')

    if random_number == 0 or random_number == n:
        # call the end_pull function
        new_mat = end_move(random_number, seq, n, mat)
    else:
        # call the corner_pull function
        new_mat = corner_move(random_number, seq, n, mat)

    # check if the matrix has changed
    if new_mat.all() == mat.all():
        print('No change made, returned original path')
        return mat
    else:
        return new_mat
        

# end move
def end_move(rand_num, seq, n, mat):
    free_spaces = []

    if rand_num == 1:        
        # find index of the 1st and 2nd elements of the sequence in the matrix
        [[row_1], [col_1]] = np.where(mat == 1)
        [[row_2], [col_2]] = np.where(mat == 2)
        
        # find adjacent free spaces to the 2nd element
        if mat[row_2-1, col_2] == 0:
            free_spaces.append([row_2-1, col_2])
        if mat[row_2+1, col_2] == 0:
            free_spaces.append([row_2+1, col_2])
        if mat[row_2, col_2-1] == 0:
            free_spaces.append([row_2, col_2-1])
        if mat[row_2, col_2+1] == 0:
            free_spaces.append([row_2, col_2+1])
        print(f'Free Spaces: {free_spaces}')
        
        # choose a random free space
        random_space = np.random.randint(0,len(free_spaces))
        # move 1st position to the random free space
        mat[free_spaces[random_space][0], free_spaces[random_space][1]] = 1
        mat[row_1, col_1] = 0
        return mat
    else:
        # find index of the last and 2nd last elements of the sequence in the matrix
        [[row_end], [col_end]] = np.where(mat == n)
        [[row_2end], [col_2end]] = np.where(mat == n-1)
        
        # find adjacent free spaces to the 2nd last element
        if mat[row_2end-1, col_2end] == 0:
            free_spaces.append([row_2end-1, col_2end])
        if mat[row_2end+1, col_2end] == 0:
            free_spaces.append([row_2end+1, col_2end])
        if mat[row_2end, col_2end-1] == 0:
            free_spaces.append([row_2end, col_2end-1])
        if mat[row_2end, col_2end+1] == 0:
            free_spaces.append([row_2end, col_2end+1])
        print(f'Free Spaces: {free_spaces}')
        
        # choose a random free space
        random_space = np.random.randint(0,len(free_spaces))
        # move last position to the random free space
        mat[free_spaces[random_space][0], free_spaces[random_space][1]] = n
        mat[row_end, col_end] = 0
        return mat
    
# corner move
def corner_move(rand_num, seq, n, mat):
    free_spaces_bef = []
    free_spaces_aft = []
    
    # find the index of the element, the element before and the alement after it in the sequence in the matrix
    [[row_num], [col_num]] = np.where(mat == rand_num)
    [[row_bef], [col_bef]] = np.where(mat == rand_num-1)
    [[row_aft], [col_aft]] = np.where(mat == rand_num+1)
    
    # find adjacent free spaces to the element before
    # TODO: make it more efficient by checking corners of element 
    if mat[row_bef-1, col_bef] == 0:
        free_spaces_bef.append([row_bef-1, col_bef])
    if mat[row_bef+1, col_bef] == 0:
        free_spaces_bef.append([row_bef+1, col_bef])
    if mat[row_bef, col_bef-1] == 0:
        free_spaces_bef.append([row_bef, col_bef-1])
    if mat[row_bef, col_bef+1] == 0:
        free_spaces_bef.append([row_bef, col_bef+1])
    # find adjacent free spaces to the element before
    if mat[row_aft-1, col_aft] == 0:
        free_spaces_aft.append([row_aft-1, col_aft])
    if mat[row_aft+1, col_aft] == 0:
        free_spaces_aft.append([row_aft+1, col_aft])
    if mat[row_aft, col_aft-1] == 0:
        free_spaces_aft.append([row_aft, col_aft-1])
    if mat[row_aft, col_aft+1] == 0:
        free_spaces_aft.append([row_aft, col_aft+1])    
    
    # find the common free space between the two lists
    common_space = list(set(tuple(x) for x in free_spaces_bef) & set(tuple(x) for x in free_spaces_aft))
    print(f'Common Space: {common_space}')
    
    if len(common_space) == 0:
        pass
    else:
        # choose a random common free space
        random_space = np.random.randint(0,len(common_space))
        # move the element to the random common free space
        mat[common_space[random_space][0], common_space[random_space][1]] = rand_num
        mat[row_num, col_num] = 0
    return mat

# crankshaft move
def crankshaft_move(rand_num, seq, n, mat):
    # find the index of the element, the element before, the element after and the element 2 after it in the sequence in the matrix
    [[row_num], [col_num]] = np.where(mat == rand_num)
    [[row_bef], [col_bef]] = np.where(mat == rand_num-1)
    [[row_aft], [col_aft]] = np.where(mat == rand_num+1)
    [[row_2aft], [col_2aft]] = np.where(mat == rand_num+2)
    
    # see direction of next element relative to the current element
    row_dir = row_num - row_aft
    col_dir = col_aft - col_num

    # TODO: incomplete


if __name__ == "__main__":
    # initialize the sequence
    sequence = "HPPHHPHH"
    n = len(sequence)

    #create a test matrix of size 11X11 where the origin is at the center [5,5]
    test_matrix = np.zeros((11,11))

    # fill the matrix with numbers indicating a SAW
    test_matrix[5,5] = 1
    test_matrix[5,6] = 2
    test_matrix[5,7] = 3
    test_matrix[5,8] = 4
    test_matrix[6,8] = 5
    test_matrix[6,9] = 6
    test_matrix[7,9] = 7
    test_matrix[7,8] = 8
    print(f'Test Matrix: {test_matrix}')

    # do the move
    new_matrix = vsdh_move(sequence, n, test_matrix)
    print(f'New Matrix: {new_matrix}')

