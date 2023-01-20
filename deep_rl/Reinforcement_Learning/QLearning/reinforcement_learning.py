from pandas.core.algorithms import doc
import environment as evrnt
import numpy as np
import random as rnd

# TODO: automatise dict setup
action_lookup_tbl = {
	'UH': 1,
	'UP': 2,
	'DH': 3,
	'DP': 4,
	'LH': 5,
	'LP': 6,
	'RH': 7,
	'RP': 8
}

def learning(
		alpha,
		gamma,
		epsilon,
		chainlength
		):

	rl_env = evrnt.env(chainlength)
	q_table = np.zeros([rl_env.state_space, rl_env.action_space])

	# For plotting metrics
	all_epochs = []
	all_penalties = []

	for i in range(1, 100001):
		state = rl_env.reset()

		epochs, penalties, reward = 0, 0, 0
		done = False
		action = 'None'

		while not done:
			action = None # To prevent 'unbound var' errors
			if rnd.uniform(0, 1) < epsilon: #
				action = rl_env.actactionion_space_sample()
			else:
				action = np.argmax(q_table[state])

		next_state, reward, done, info = rl_env.step(action)

		# TODO: fix action indexing
		action_idx = 1
		old_value = q_table[state, action_idx]
		next_max = np.max(q_table[next_state])

		new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
		q_table[state, action] = new_value

		state = next_state
		epochs += 1

		if i % 100 == 0:
			print(f'Episode {i}')

if __name__ == '__main__':
	learning(
		alpha=0.1,
		gamma=0.6,
		epsilon=1,
		chainlength=3
		)
