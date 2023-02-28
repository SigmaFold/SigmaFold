import numpy as np

# choosing the right VSHD move
def vsdh_move(seq, n, mat):
    # choose a random number between 1 to n inclusive
    random_number = np.random.randint(1,n+1)
    random_number = 5
    print(f'Random number chosen: {random_number}')
    (total_rows, total_cols) = mat.shape

    new_mat = mat.copy()

    # choose a random move
    random_move = np.random.randint(1,5)
    random_move = 4
    if random_move == 1:
        # call the end move function
        print('End move chosen')
        new_mat = end_move(random_number, seq, n, new_mat, total_rows, total_cols)
    elif random_move == 2:
        # call the corner_move function
        print('Corner move chosen')
        new_mat = corner_move(random_number, seq, n, new_mat, total_rows, total_cols)
    elif random_move == 3:
        # call the crankshaft_move function
        print('Crankshaft move chosen')
        new_mat = crankshaft_move(random_number, seq, n, new_mat, total_rows, total_cols)
    else:
        # call the pull_move function
        print('Pull move chosen')
        new_mat = pull_move(random_number, seq, n, new_mat, total_rows, total_cols)        

    # check if the matrix has changed
    if np.array_equal(new_mat, mat):
        print('No change made, returned original path')
        return mat
    else:
        return new_mat
        

# end move
def end_move(rand_num, seq, n, mat, total_rows, total_cols):
    free_spaces = []

    if rand_num == 1:        
        # find index of the 1st and 2nd elements of the sequence in the matrix
        [[row_1], [col_1]] = np.where(mat == 1)
        [[row_2], [col_2]] = np.where(mat == 2)
        
        # find adjacent free spaces to the 2nd element
        if row_2-1 >= 0 and mat[row_2-1, col_2] == 0:
            free_spaces.append([row_2-1, col_2])
        if row_2+1 < total_rows and mat[row_2+1, col_2] == 0:
            free_spaces.append([row_2+1, col_2])
        if col_2-1 >= 0 and mat[row_2, col_2-1] == 0:
            free_spaces.append([row_2, col_2-1])
        if col_2+1 < total_cols and mat[row_2, col_2+1] == 0:
            free_spaces.append([row_2, col_2+1])
        
        # if there are no free spaces, end move has failed
        if len(free_spaces) == 0:
            print('End move failed')
            return mat
        # if there are free spaces, complete end move
        else:
            # choose a random free space
            random_space = np.random.randint(0,len(free_spaces))
            # move 1st position to the random free space
            mat[free_spaces[random_space][0], free_spaces[random_space][1]] = 1
            mat[row_1, col_1] = 0
            return mat
        
    elif rand_num == n:
        # find index of the last and 2nd last elements of the sequence in the matrix
        [[row_end], [col_end]] = np.where(mat == n)
        [[row_2end], [col_2end]] = np.where(mat == n-1)
        
        # find adjacent free spaces to the 2nd last element
        if row_2end-1 >= 0 and mat[row_2end-1, col_2end] == 0:
            free_spaces.append([row_2end-1, col_2end])
        if row_2end+1 < total_rows and mat[row_2end+1, col_2end] == 0:
            free_spaces.append([row_2end+1, col_2end])
        if col_2end-1 >= 0 and mat[row_2end, col_2end-1] == 0:
            free_spaces.append([row_2end, col_2end-1])
        if col_2end+1 < total_cols and mat[row_2end, col_2end+1] == 0:
            free_spaces.append([row_2end, col_2end+1])
        
        # if there are no free spaces, end move has failed
        if len(free_spaces) == 0:
            print('End move failed')
            return mat
        # if there are free spaces, complete end move
        else:
            # choose a random free space
            random_space = np.random.randint(0,len(free_spaces))
            # move last position to the random free space
            mat[free_spaces[random_space][0], free_spaces[random_space][1]] = n
            mat[row_end, col_end] = 0
            return mat
    else:
        print('End move failed')
        return mat
    
# corner move
def corner_move(rand_num, seq, n, mat, total_rows, total_cols):
    free_spaces_bef = []
    free_spaces_aft = []
    
    # ensure it is not the first or last element of the sequence
    if rand_num == 1 or rand_num == n:
        print('Corner move failed')
        return mat

    # find the index of the element, the element before and the alement after it in the sequence in the matrix
    [[row_num], [col_num]] = np.where(mat == rand_num)
    [[row_bef], [col_bef]] = np.where(mat == rand_num-1)
    [[row_aft], [col_aft]] = np.where(mat == rand_num+1)
    
    # find adjacent free spaces to the element before
    # TODO: make it more efficient by checking corners of element 
    if row_bef-1>=0 and mat[row_bef-1, col_bef] == 0:
        free_spaces_bef.append([row_bef-1, col_bef])
    if row_bef+1<total_rows and mat[row_bef+1, col_bef] == 0:
        free_spaces_bef.append([row_bef+1, col_bef])
    if col_bef-1>=0 and mat[row_bef, col_bef-1] == 0:
        free_spaces_bef.append([row_bef, col_bef-1])
    if col_bef+1<total_cols and mat[row_bef, col_bef+1] == 0:
        free_spaces_bef.append([row_bef, col_bef+1])
    # find adjacent free spaces to the element after
    if row_aft-1>=0 and mat[row_aft-1, col_aft] == 0:
        free_spaces_aft.append([row_aft-1, col_aft])
    if row_aft+1<total_rows and mat[row_aft+1, col_aft] == 0:
        free_spaces_aft.append([row_aft+1, col_aft])
    if col_aft-1>=0 and mat[row_aft, col_aft-1] == 0:
        free_spaces_aft.append([row_aft, col_aft-1])
    if col_aft+1<total_cols and mat[row_aft, col_aft+1] == 0:
        free_spaces_aft.append([row_aft, col_aft+1])  
    
    # find the common free space between the two lists
    common_space = list(set(tuple(x) for x in free_spaces_bef) & set(tuple(x) for x in free_spaces_aft))
    
    if len(common_space) == 0:
        print('Corner move failed')
        return mat
    else:
        # choose a random common free space
        random_space = np.random.randint(0,len(common_space))
        # move the element to the random common free space
        mat[common_space[random_space][0], common_space[random_space][1]] = rand_num
        mat[row_num, col_num] = 0
    return mat

# crankshaft move
def crankshaft_move(rand_num, seq, n, mat, total_rows, total_cols):
    # ensure it is not the first or last element of the sequence
    if rand_num == 1 or rand_num == n:
        print('Crankshaft move failed')
        return mat

    # find the index of the element, the element before and the element after
    [[row_num], [col_num]] = np.where(mat == rand_num)
    [[row_bef], [col_bef]] = np.where(mat == rand_num-1)
    [[row_aft], [col_aft]] = np.where(mat == rand_num+1)
    
    # see direction of next element relative to the current element
    row_dir = row_num - row_bef
    col_dir = col_num - col_bef

    #fail if the next element is in the same direction
    if row_dir == row_aft - row_num and col_dir == col_aft - col_num:
        print('Crankshaft move failed')
        return mat

    # find the next non zero element in the matrix in the direction of the current element
    row_u = row_num + row_dir
    col_u = col_num + col_dir
    while mat[row_u, col_u] == 0:
        row_u += row_dir
        col_u += col_dir
        # check if row or column index is out of bounds
        if row_u < 0 or row_u > total_rows-1 or col_u < 0 or col_u > total_cols-1:
            print('Crankshaft move failed')
            return mat
    u_num = mat[row_u, col_u]

    # do the crankshaft move
    num = rand_num+1
    # find the non zero elements between rand_num and u_num reflect them along the axis created by mat[row_num, col_num] and mat[row_u, col_u]
    while num != u_num:
        # find the index of the element in the matrix
        [[row], [col]] = np.where(mat == num)
        # reflect the mat[row, col] along the axis created by mat[row_num, col_num] and mat[row_u, col_u]
        num_dir_row = row - row_num # positive in increase in row number
        num_dir_col = col - col_num # positive is increase in column number
        
        if col_dir == 0:
            new_pos = [row_num + num_dir_row, col_num - num_dir_col]
        else:
            new_pos = [row_num - num_dir_row, col_num + num_dir_col]
        
        # check if new position is out of bounds or if it is already occupied
        if mat[new_pos[0], new_pos[1]] != 0 or new_pos[0] < 0 or new_pos[0] > total_rows-1 or new_pos[1] < 0 or new_pos[1] > total_cols-1:
                print('Crankshaft move failed')
                return mat
        else:
            mat[new_pos[0], new_pos[1]] = num
            mat[row, col] = 0
        num += 1
    return mat

# pull move
def pull_move(rand_num, seq, n, mat, total_rows, total_cols):
    # ensure it is not the first or last element of the sequence
    if rand_num == 1 or rand_num == n:
        print('Pull move failed')
        return mat
    
    # find the index of the element, the next element, and the element before in the sequence in the matrix
    [[row_num], [col_num]] = np.where(mat == rand_num)
    [[row_aft], [col_aft]] = np.where(mat == rand_num+1)
    [[row_bef], [col_bef]] = np.where(mat == rand_num-1)

    # find the non diagonal adjacent free spaces to the element before in the sequence while making sure they are not out of bounds
    free_spaces = []
    if row_bef-1>=0 and mat[row_bef-1, col_bef] == 0:
        free_spaces.append([row_bef-1, col_bef])
    if row_bef+1<total_rows and mat[row_bef+1, col_bef] == 0:
        free_spaces.append([row_bef+1, col_bef])
    if col_bef-1>=0 and mat[row_bef, col_bef-1] == 0:
        free_spaces.append([row_bef, col_bef-1])
    if col_bef+1<total_cols and mat[row_bef, col_bef+1] == 0:
        free_spaces.append([row_bef, col_bef+1])

    # If these free spaces are diagonal to mat[row_num, col_num] then add them to a list
    row_dir = row_num - row_bef
    col_dir = col_num - col_bef
    if [row_bef-row_dir, col_bef-col_dir] in free_spaces:
        free_spaces.remove([row_bef-row_dir, col_bef-col_dir])
    
    # choose a random free space
    if len(free_spaces) == 0:
        print('Pull move failed')
        return mat
    else:
        random_space = np.random.randint(0,len(free_spaces))
    
    old_mat = mat.copy()
    
    # move the element to the random free space
    mat[free_spaces[random_space][0], free_spaces[random_space][1]] = rand_num
    mat[row_num, col_num] = 0
    
    # direction of movement
    row_dir = free_spaces[random_space][0] - row_num
    col_dir = free_spaces[random_space][1] - col_num


    # move all subsequent elements similarly until the pull move is complete
    coord_dict = {}
    for i in range(rand_num+1, n+1):
        indices = np.where(mat == i)
        if indices[0].size > 0:
            [[row_num], [col_num]] = indices
        else:
            [row_num, col_num] = coord_dict[i]

        if row_num+row_dir>= 0 and row_num+row_dir<total_rows and col_num+col_dir>= 0 and col_num+col_dir<total_cols:
            if mat[row_num+row_dir, col_num+col_dir] != 0 and i == rand_num+1:
                print('Pull move failed')
                return old_mat
            elif mat[row_num+row_dir, col_num+col_dir] != 0:
                coord_dict[mat[row_num+row_dir, col_num+col_dir]]= [row_num+row_dir, col_num+col_dir]
            else:
                pass
            mat[row_num+row_dir, col_num+col_dir] = i
            mat[row_num, col_num] = 0
        else:
            print('Pull move failed')
            return old_mat
    return mat


if __name__ == "__main__":

    # initialize the sequence
    sequence = "HPPHHPHHHH"
    n = len(sequence)

    #create a test matrix of size 11X11 where the origin is at the center [5,5]
    test_matrix = np.zeros((15,15))

    # fill the matrix with numbers indicating a SAW
    test_matrix[5,5] = 1
    test_matrix[5,6] = 2
    test_matrix[5,7] = 3
    test_matrix[5,8] = 4
    test_matrix[6,8] = 5
    test_matrix[6,9] = 6
    test_matrix[6,10] = 7
    test_matrix[7,10] = 8
    test_matrix[7,9] = 9
    test_matrix[7,8] = 10
    print(f'Test Matrix: {test_matrix}')

    # do the move
    new_matrix = vsdh_move(sequence, n, test_matrix)
    print(f'New Matrix: {new_matrix}')

