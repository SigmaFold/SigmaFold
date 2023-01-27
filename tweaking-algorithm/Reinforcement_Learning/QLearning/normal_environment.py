import numpy as np
import mmh3
import pandas as pd
import random as rnd
import os

# Personal notes:
# - shape: matrix with 0 representing outside space (ie, cant place amino-acids on 0's) and 1 represents
#   possible locations

class env():
	"""Class implementing the learning environement. Each env object is an environement with a set of methods to render it,
	perform some actions and get the corresponding reward. See each method for further information"""

	def __init__(self, shape):
		self.action_space = 2
		self.state_space = np.sum(shape)
		self.content = shape
		self.state = 0 # State 0 corresponds to initil state: must choose starting index
		self.index = [0, 0] # TODO: implement RL for educated guess when choosing initial index

		self.render('slow')

	def step(self, step):
		"""Method to move 1 step forward. Arguement is the step that should be performed"""

		next_move = step[0]
		next_amino = step[1]
		match next_move:
			case 'U': # Up
				self.index[1] += 1
			case 'D': # Down
				self.index[1] -= 1
			case 'L':
				self.index[0] -=1
			case 'R':
				self.index[0] += 1

		self.content[self.index[0], self.index[1]] = next_amino
		self.state = mmh3.hash64(str(self.content), signed=False)[0] # TODO: Why 0 here? Ask Nico
		done = self._check_done()

		reward = None # TODO: Create the reward function !
		done = False if (self.advancement < self.chain_length) else True
		info = "No error"
		
		return self.state, reward, done, info

	def render(self, render_speed='fast'):
		os.system('cls')
		print(f'State: {self.state}\n')
		if self.index != None:
			self.content[self.index[0], self.index[1]] = '*'
		render_output =  self.content if (render_speed == 'fast') else pd.DataFrame(self.content)
		print(render_output)

	def reset(self):
		self.content = self._init_content(self.chain_length)
		self.state = mmh3.hash64(str(self.content), signed=False)[0] # TODO: Why 0 here? Ask Nico
		return self.state

	def _check_done(self):
		pass

	@staticmethod
	def action_space_sample():
		dir_choice = ['U', 'D', 'L', 'R']
		amino_choice = ['H', 'P']
		choice = rnd.choice(dir_choice) + rnd.choice(amino_choice)
		return choice

	@staticmethod
	def _init_content(n):
		n = n if (n%2 != 0) else n+1
		return np.zeros((n, n), dtype=str)


if __name__ == '__main__':
	my_env  = env(2) 