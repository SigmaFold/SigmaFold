import numpy as np

def q_table_setup(state_space_dim, action_space_dim):
	q_table = np.zeros([state_space_dim, action_space_dim+1])

	# TODO: setup database to quickly fill the table
	q_table[:,0] = [783*state_space_dim]

	return q_table

