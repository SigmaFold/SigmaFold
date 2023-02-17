import numpy as np

# end pull move
def end_pull(rand_num, seq, n, mat):
    if rand_num == 1:
        free_spaces = []
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
        print(f'New Matrix: {mat}')
    elif rand_num == n:
        free_spaces = []
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
        print(f'New Matrix: {mat}')


         
         

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

# choose a random number between 1 to n inclusive
random_number = np.random.randint(1,n+1)
random_number = 8

# call the end_pull function
end_pull(random_number, sequence, n, test_matrix)


