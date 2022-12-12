import streamlit as st

# def submit_button(grid_check):


with st.sidebar:
    st.header('Grid Configuration')
    n_cols = int(st.number_input('Number of rows/columns', 3, 15, 8))

check = ['']*n_cols
for check_num in range(n_cols):
    check[check_num] = ['']*n_cols

cols = st.columns(n_cols)
for col_num in range(n_cols):
    with cols[col_num]:
        for check_num in range(n_cols):
            check[check_num][col_num] = st.checkbox('', key=(col_num * n_cols) + check_num)

st.write('')
st.write('')

user_matrix = check
for i, col in enumerate(check):
    for j, box in enumerate(col):
        if box:
            user_matrix[i][j] = 1
        else:
            user_matrix[i][j] = 0

user_matrix

# st.button('Submit', on_click=submit_button(check))
