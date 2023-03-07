import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random as rnd

def index_shape(shape):
    '''
    Numbers the elements of an input array from 1, starting horizontally
        Input: shape - numpy array of 0's and 1's representing shape
        Output: shape_out - numpy array with indexed elements for non-zero elements padded with 0 (void)
    '''
    # gets shape dimensions
    row_len = np.shape(shape)[0] # gets row length
    col_len = np.shape(shape)[1] # gets col length
    shape_out = np.asarray(row_len * [col_len * [0]])
    
    index = 1 # path starts from 1
    for row in range(row_len): # goes through each row
        for col in range(col_len): # goes through each column
            if shape[row][col] == 1: # if element present
                shape_out[row][col] = index
                index += 1

    return np.pad(shape_out, 1) # pads with 0 for void

def gen_path(df, shape, origin):
    '''
    Generates all possible paths given a shape
        Input: df - pandas dataframe containing neighbouring environment information of the shape 
               shape - numpy array with indexed elements for non-zero elements padded with 0 (void)
               origin - location (tuple) of point to start from on the shape
        Output: paths - list of all possible paths for a given shape
    '''
    # generate all possible paths and stored in paths
    paths = [] # list of all possible paths
    visited = set()
    length = len(df)
    def saw(start, visited, path=[]):
        # intialising path
        if start not in path:
            path.append(start)
            visited.add(start)

        # growing the path
        if len(path) < length: # if chain not finished
            curr_i = shape[start[0]][start[1]] # name of the current element
            nb_list = df.loc[curr_i].loc["neighbours"] # list of neighbours for the element

            for nb in nb_list: # iteratres through each neighbour
                nb_pos = df.loc[nb].loc["position"]
                if nb_pos not in visited: # if neighbour has not been visted
                    visited.add(nb_pos)
                    saw(nb_pos, visited, path + [nb_pos])
                    visited.remove(nb_pos)
        else:
            paths.append(path)
    saw(origin, visited)

    return paths

def optimal_path(df, shape):
    '''
    Returns the optimal paths given a shape judged by the number of elements in contact with the terminals
        Input: df - pandas dataframe containing neighbouring environment information of the shape 
        Output: optimal paths with the most ends 'buried'
    '''
    # dictionary of how many total terminal neighbours paths have
    terminal_nb = {}
    for i in range(8,1,-1): # min number of connected neighbours for terminals = 4, maximum = 8
        terminal_nb[i] = [] # create empty list for path

    # dictionary of neighbour count and positions
    pos_to_nb = {}
    for i in range(len(df)):
        pos_to_nb[df.iloc[i].loc["position"]] = df.iloc[i].loc["nb count"]

    # generating path from each point in shape
    for i in range(len(df)):
        paths = []
        origin = df.iloc[i].loc["position"]
        paths = gen_path(df, shape, origin) # generate all possible paths starting from given origin
        for path in paths:
            term_nb = pos_to_nb[path[0]] + pos_to_nb[path[-1]] # calculate the total neighbours of the two terminals
            terminal_nb[term_nb].append(path)
    
    # remove repeating paths where start & end are swapped
    for i in range(8,1,-1):
        for path in terminal_nb[i]:
            if list(reversed(path)) in terminal_nb[i]:
                terminal_nb[i].remove(path)

    # for i in range(8,3,-1):
    #     print(f"{len(terminal_nb[i])} paths for terminal neighbours = {i}")

    # return paths with specified terminal neighbours
    return terminal_nb

def plot_path(path):
    '''
    Plots an outputted path given a shape
    '''
    plt.figure(figsize = (6, 6))
    x = []
    y = []
    for i in path:
        x.append(i[0])
        y.append(i[1])

    plt.plot(x, y, 'bo-', ms = 12, linewidth = 1)
    plt.plot(path[0][0], path[0][1], 'go', ms = 14, label = 'Start')
    plt.plot(path[-1][0], path[-1][1], 'ro', ms = 14, label = 'End')
    plt.axis('equal')
    plt.legend(fontsize=15)
    plt.show()

def plot_HP(sequence, path):
    '''
    Plots the lattice with H & P assigned
    '''
    plt.figure(figsize = (6, 6))

    # Gets positions of elements
    x_P = [] # position of P elements
    y_P = []
    for i in range(len(path)):
        if sequence[i] == "P":
            x_P.append(path[i][0])
            y_P.append(path[i][1])
    x = [] # position of all elements
    y = []
    for i in path:
        x.append(i[0])
        y.append(i[1])

    # Plots H & P with path
    plt.plot(x, y, 'ro-', ms = 12, linewidth = 1, label='H')
    plt.plot(x_P, y_P, 'bo', ms = 12, label='P')
    plt.legend(fontsize=15)
    
    plt.axis('equal')
    plt.show()

def get_env(shape):
    '''
    Gets the environment of each element before assigning path
        Input: shape - numpy array with indexed elements for non-zero elements padded with 0 (void)
        Output: dataframe including position, neighbours & neighbour count for each element
    '''
    # record position data
    pos = {} # dict of position
    for row in shape:
        for i in row:
            if i != 0: # if i is an element
                pos[i] = (np.where(shape==i)[0][0], np.where(shape==i)[1][0]) # coordinate of element as tuple

    # record neighbour data
    nb = {} # dict of neighbours
    for i in range(1, len(pos)+1):
        nb[i] = [] # generates empty dictionary for each indexed element
    coord_sum = {} # list of coordinate sums for finding neighbours
    for i in range(1, len(pos)+1):
        coord_sum[i] = sum(pos[i])
    
    # find neighbours of each element according to coordinate sum
    for i1 in coord_sum: # for each element
        sum1 = coord_sum[i1] # coordinate sum
        if (sum1 % 2) == 0: # get elements with even coord sum
            for sum2 in [sum1-1, sum1+1]: # get elements with coord sum +-1 of sum1
                for i2 in coord_sum: # iterate through dictionary to find matching coord sum
                    if coord_sum[i2] == sum2: # if the sum matches
                        i1_pos = pos[i1]
                        i2_pos = pos[i2]
                        distance = (i1_pos[0] - i2_pos[0])**2 + (i1_pos[1] - i2_pos[1])**2 # calculates distance
                        if distance == 1: # neighbour
                            nb[i1].append(i2)
                            nb[i2].append(i1)      
    
    nb_count = {} # dict of neighbour numbers
    for i in range(1, len(pos)+1):
        nb_count[i] = len(nb[i])
    
    return pd.DataFrame({"position":pd.Series(pos), "neighbours":pd.Series(nb), "nb count":pd.Series(nb_count)})
    
def path_info(path, shape):
    '''
    Checks the surrounding environment of each connected element given a path
        Input: path - list of coordinates in order of the path
        Output: df - dataframe with environment information
    '''
    # get the element label for each path coordinate
    path_order = [] # list of element name in order for a given path
    for i in path:
        path_order.append(shape[i[0]][i[1]])#
    
    # record position data
    pos = {} # dict of position
    for row in shape:
        for i in row:
            if i != 0: # if i is an element
                pos[i] = (np.where(shape==i)[0][0], np.where(shape==i)[1][0]) # coordinate of element as tuple

    # record neighbour data
    nb = {} # dict of neighbours
    for i in range(1, len(path_order)+1): # i = element name
        nb[i] = [] # generates empty dictionary for each indexed element

    # find non-connected neighbours of each element using odd-even contact rule
    for idx_i in range(1,len(path_order),2): # even index
        i = path_order[idx_i] # element label
        i_pos = pos[i]
        for idx_j in range(0,len(path_order),2): # odd index
            j = path_order[idx_j] # element label

            if idx_j != (idx_i-1) and  idx_j != (idx_i+1):
                j_pos = pos[j]
                distance = (i_pos[0] - j_pos[0])**2 + (i_pos[1] - j_pos[1])**2 # calculates distance
                if distance == 1: # neighbour
                    nb[i].append(j)
                    nb[j].append(i)
    
    # counts how many non-connected neighbours an element has
    nb_count = {}
    for i in nb:
        nb_count[i] = len(nb[i])

    df = pd.DataFrame({"position":pd.Series(pos), "contact":pd.Series(nb), "contact number":pd.Series(nb_count)})

    return df

def assign_HP(path, shape):
    '''
    Assigns H or P to each element, according to rule set 1, H = 1, P = -1
    Rule set 1:
        Assign H's to all interior residues
        Assign H's to all exterior residues in contact with interior residues
    '''
    # creates array copy with the same dimension
    row_n = np.shape(shape)[0] # gets row number
    col_n = np.shape(shape)[1] # gets col number
    shape1 = np.asarray(row_n*[col_n*[0]])

    # get neighbour information
    df_path = path_info(path, shape)

    # list of interior & exterior H's
    interior_H = []
    exterior_H = []

    # find interior H & assign H
    for i in range(1,len(df_path)+1):
        if df_path.loc[i].loc["contact number"] >= 2: # interior
            interior_H.append(i)

    # choose exterior residue to assign H
    for i in interior_H: # each interior H
        for j in df_path.loc[i].loc["contact"]: # contact of each interior H
            if j not in interior_H: # finds only exterior contact
                exterior_H.append(j)
    if len(interior_H) == 0: # if no interior
        for i in range(1,len(df_path)+1):
            if df_path.loc[i].loc["contact number"] >= 1:
                exterior_H.append(i)

    # assign H & P
    residue = {}
    sequence = []
    for i in range(len(df_path)): # index
        j = df_path.iloc[i].name # element name
        if len(interior_H) != 0:
            if (j in interior_H) or (j in exterior_H): # check if assigned H
                shape1[df_path.iloc[i].loc["position"][0]][df_path.iloc[i].loc["position"][1]] = 1 # H
                residue[j] = 'H'
            else:
                shape1[df_path.iloc[i].loc["position"][0]][df_path.iloc[i].loc["position"][1]] = -1 # P
                residue[j] = 'P'
        else:
            if j in exterior_H:
                shape1[df_path.iloc[i].loc["position"][0]][df_path.iloc[i].loc["position"][1]] = 1 # H
                residue[j] = 'H'
            else:
                shape1[df_path.iloc[i].loc["position"][0]][df_path.iloc[i].loc["position"][1]] = -1 # P
                residue[j] = 'P'

    df_path["residue"] = pd.Series(residue)

    for pos in path:
        i = shape[pos[0]][pos[1]]
        sequence.append(residue[i])

    return shape1, df_path, "".join(sequence)

def calc_energy(df):
    '''
    Calculates energy of the outputted array with H & P
    '''
    energy = 0
    for i in range(len(df)):
        if df.iloc[i].loc["residue"] == "H":
            for j in df.iloc[i].loc["contact"]:
                if df.loc[j].loc["residue"] == "H":
                    energy += -1

    return energy/2

def heuristics(target):
    '''
    Input: target - matrix of 1's and 0's
    Output: sequence - string of H and P
    '''
    print(target)
    target = np.asarray(target) # test
    target1 = index_shape(target) # index the input shape
    seq_df = get_env(target1) # get required information
    paths_dict = optimal_path(seq_df, target1) # generates optimal paths
    
    # chooses the most optimal neighbours
    opt_nb = 0
    for i in range(max(paths_dict.keys()),min(paths_dict.keys())-1,-1):
        if len(paths_dict[i]) != 0:
            opt_nb = i
            break
    __, __, sequence = assign_HP(rnd.choice(paths_dict[opt_nb]), target1) # randomly selects from pool of candidates
    
    print(f"The input sequence from heuristics is {sequence}")
    return sequence

