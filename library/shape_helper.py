"""
Provides helper functions to help handdling shapes for various purposes (database storage, training etc.)
"""
import numpy as np


# Saving shapes based on their center of mass 
def path2shape(path):
    grid = np.asarray([[0]*25]*25, dtype=int) # actual grid for mapping
    temp_grid = np.asarray([[0]*25]*25, dtype=int) # temp grid to hold the array before alignment
    for coord in test_path:
        temp_grid[coord[0]+13][coord[1]+13] = 1 # path transferred onto grid but uncentered
    temp_grid = np.pad(temp_grid, 1) # zero padding to avoid multiplying by 0 when calculating moments

    # find centroid of temp_grid
    m_00 = len(path) # non-zero residues
    m_01 = 0
    for row_n, row in enumerate(temp_grid):
        if np.any(row!=0):
            m_01 += row_n * np.count_nonzero(row)
    m_10 = 0
    for col_n in range(np.shape(temp_grid)[1]):
        if np.any(temp_grid[:, col_n]!=0):
            m_10 += col_n *  np.count_nonzero(temp_grid[:, col_n])

    # coordinates of centroid
    n_centroid = math.floor((m_10/m_00))
    m_centroid = math.floor((m_01/m_00))
    centroid = (m_centroid, n_centroid)

    # align temp_grid onto grid
    dev_m = 13-centroid[0]
    dev_n = 13-centroid[1]
    coord_list = np.nonzero(temp_grid)
    for i in range(len(coord_list[0])):
        grid[coord_list[0][i]+dev_m][coord_list[1][i]+dev_n] = 1

    return grid