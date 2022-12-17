import streamlit as st
import logic


def submit_button(user_mat):
    """Runs the functions in genpathlist.py to output a hamiltonian path"""
    path_mat, grid_size = logic.create_pathmat(user_mat)
    output_mat = logic.graphicchain(path_mat, grid_size)
    st.write(output_mat)


# Creating a sidebar that allows you to modify the shape of the grid by controlling number of columns and rows
with st.sidebar:
    st.header('Grid Configuration')
    n_cols = int(st.number_input('Number of rows/columns', 3, 15, 8))

# Initializing variable check to the size of the grid
check = ['']*n_cols
for check_num in range(n_cols):
    check[check_num] = ['']*n_cols

# Creating a grid of checkboxes based on the number of columns inputted in sidebar and modifying check to reflect if the checkboxes are ticked or not
cols = st.columns(n_cols)
for col_num in range(n_cols):
    with cols[col_num]:
        for check_num in range(n_cols):
            check[check_num][col_num] = st.checkbox('', key=(col_num * n_cols) + check_num)

# Whitespace
st.write('')
st.write('')

# Creating variable user_matrix which replaces the boolean values in check to 1s and 0s
user_matrix = check
for i, col in enumerate(check):
    for j, box in enumerate(col):
        if box:
            user_matrix[i][j] = 1
        else:
            user_matrix[i][j] = 0

submit_button(user_matrix)
