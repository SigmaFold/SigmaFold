from typing import List
import gym
from gym import spaces
import numpy as np 

default_hp_table = {
	0: 'H',
	1: 'P',
}
class InverseFoldingEnv(gym.Env):
	metadata = {'render_modes':['human']}

	def __init__(
			self, 
			chain_length,
			base_num=2,
			amino_table=default_hp_table,
			render_mode=None,
			) -> None:

		super(InverseFoldingEnv, self).__init__()

		# Static properties of the environment
		self.chain_length = chain_length
		self.base_num = base_num
		self.amino_table = amino_table

		self.sequence = self._initialise_sequence()
		self.target = self._initialise_target()

		# Action space: <base_num> action possible for each units, ie:
		self.action_space = spaces.Discrete(base_num*chain_length)

		# Observation space gives structural info on the observation
		self.observation_space = spaces.Dict(
			{
				"sequence": spaces.Box(10, 10, (10, 10)),
				"target": spaces.Box(10, 10, (10, 10)),
			})

		# State space
		self.state_space = 2**self.chain_length
		
		# Memory-based reward function
		self.degen = int()
		self.seq_target_corr = int()

		# Rendering options
		self.render_mode = render_mode
		self.window = None
		self.clock = None
		

	def reset(self, seed=None):
		"""
		Method to reset the content of the environement. All the amino-acids 
		are deleted along with the spacial constraints. Then new random 
		constraints are generated
		"""
		super().reset(seed=seed)

		self.sequence = self._initialise_sequence()
		self.target = self._initialise_target()

		if self.render_mode == 'human':
			self._render_frame()

		observation = self._get_obs()
		info = self._get_info()

		return observation, info

	# TODO: finish reward function
	def step(self, action):
		"""
		Method that accepts an action (int 0 -> (2*chain length - 1) and 
		computes the resulting state along with the reward
		"""
		index, amino_int = self._action_parser(action)

		self.sequence = self.sequence.set_amino(index, str(amino_int))

		observation = self._get_obs()
		info = self._get_info()

		done = True if ((info["degen"] < 10) & info["corr"] < 5) else False

		reward = self._get_reward(info)

		return observation, reward, done, False, info

	# TODO: better rendering method
	def render(self):
		return np.zeros((2,2))
	
	@staticmethod
	def test_import():
		print("Module correctly imported!")

	# TODO: upgrade this method to initialise with educated guess, not random
	def _initialise_sequence(self): # -> Sequence type
		"""
		Method that initialise a random state. A random number is generated
		and converted to the corresponding base to fit the model
		"""
		init_sequence = list()

		b = self.base_num
		n = b^self.chain_length
		
		while n:
			init_sequence.append(n % b)
			n = n // b

		while len(init_sequence) < self.chain_length:
			init_sequence.insert(0, 0)

		sequence = Sequence(init_sequence)
		
		return sequence


	# TODO: finish this method. Use integrated Gym RNG for better seed handling
	def _initialise_target(self):
		# create np.zeros array
		# fill with <chain_length> 1's
		# (make sure shape is filled)
		# trim the zero-padding
		# return the array
		temp_target = np.zeros((self.chain_length, self.chain_length))

		return temp_target

	# TODO: is there anything to add here?
	def _get_obs(self):
		print(self.sequence)
		return {"sequence": self.sequence, "target": None}

	# TODO: add correct functions and links to lookup tables
	def _get_info(self):
		"""
		Crucial method were most of the reward function parameters are 
		computed
		"""
		folded_seq = self._get_fold()
		fold_degen = int() # TODO: should be normalized degen. here!
		matrix_correlation = int()

		return {"degen": fold_degen, "corr": matrix_correlation}

	def _get_fold(self):
		pass

	def _action_parser(self, action):
		index = action % self.base_num
		amino_code = action // self.base_num

		return index, amino_code

	def _get_reward(self, info, degen_weight=2, corr_weight=1):
		"""
		Private method that generates a integer reward based on new 
		degeneracy and new correlation with target shape.

		Reward is computed using a linearly-weighted difference system. By
		default lowering degeneracy is twice more rewarding because it is the
		main physical problem. Default weights can be modifed if needed.
		"""
		degen = info["degen"]
		corr = info["corr"]

		# low degen = better
		# high core = better
		delta_degen = self.degen - degen
		delta_corr = corr - self.seq_target_corr

		# Magic happens here
		reward = degen_weight*delta_degen + corr_weight*delta_corr


	# TODO: Deprecated methods. Need to remove?
	def _render_frame(self):
		pass

	def _generate_shape(self):
		pass

	def _next_observation(self):
		pass

	def _take_action(self):
		pass

class Sequence():
	"""
	Class that implements the sequence datastructure (add more info!)
	"""

	default_hp = {
		'0': 'H',
		'1': 'P'
	}

	def __init__(self, sequence: list, transfer_dict: dict=default_hp) -> None:
		self.list_seq = [str(x) for x in sequence] 
		# list of str(int), each corresponding to a A.A.
		self.transfer_dict = transfer_dict

	def __str__(self) -> str:
		return self.get_fold_format()

	def set_amino(self, index: int, code: str) -> list:
		self.list_seq[index] = code # Code is str(int) so '1' for example
		return self.list_seq

	def get_fold_format(self) -> str:
		print(self.list_seq)
		temp_seq = ''.join(self.list_seq)
		print(temp_seq)
		for key in self.transfer_dict.keys():
			temp_seq = temp_seq.replace(key, self.transfer_dict[key])
		return ''.join(temp_seq)

# v0.2: adding custom Sequence class features