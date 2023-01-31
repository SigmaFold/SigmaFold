import gym
import numpy as np
import random as rnd
from gym import spaces

# List of random TODOs:
# - Too much type casting
# - remember that dqn.py was highly modded as well as the rendering functions

class PrimitiveInverseEnv(gym.Env):
	"""
	Very primitive implementation of the inverse folding training environment,
	mainly for debugging purpose and getting familiar with Neural Networks.

	### Action Space

	Action in a ndarray with shape `(1,)` (meaning?) which can take values 
	`{0 -> 2*length}`. The number can be decoded through Euclidian 
	division with the number of bases (given as an input):
		- the quotient is the index of the unit that must be changed
		- the remainder is the target base that will replace the previous one

	### Observation Space

	The observation is a `ndarray` with shape `(3,)` with the value 
	corresponding to the following:

	| Num | Observation           | Min                 | Max               |
    |-----|-----------------------|---------------------|-------------------|
    | 0   | Sequence (int)        | 0                   | Inf               |
    | 1   | Target (int)          | 0                   | Inf               |
    | 2   | Deviation (int)       | 0                   | Inf               |

    where sequences are encoded into integers (encoding is described in method
    _____).

    ### Reward

    In this primitive environment, the sequence is simply rewareded by 1 when 
    making a change that makes it closer to the target, and -1 otherwise.

    ## Encoding Techniques


	"""
	default_hp = {
		'H': 0
	}

	def __init__(self, base_num=2, seq_length=10, amino_table=default_hp) -> None:
		super().__init__()

		# Static attributes
		self.seq_length = seq_length
		self.base_num = base_num
		self.upper_encoding_bound = self.base_num**seq_length
		self.amino_table = amino_table

		# Dynamic attributes
		self.sequence = int() # sequence stored as encoded base10 integer
		self.target = int() # target stored as encoded base10 integer

		self._shadow_sequence = list() # sequence stored as decoded LIST of int(AA)
		self._shadow_target = list() # target stored as decoded LIST of int(AA)

		# Environment attributes
		low = np.array([0, 0, 0], dtype=np.float64)
		high = np.array([10000, 10000, 100], dtype=np.float64)

		self.action_space = spaces.Discrete(self.base_num*self.seq_length)
		self.observation_space = spaces.Box(low=low, high=high, dtype=np.float64)

		# Reward related attributes
		self.divergence = 10 # number of different bases

	def reset(self, options=None, seed=None):
		self.sequence, self._shadow_sequence = self._randomise_sequence()
		self.target, self._shadow_target = self._randomise_sequence()
		# print(self._shadow_sequence)
		# print(self._shadow_target)
		observation = self._get_obs()
		return observation, {}

	def step(self, action):
		# print('\n New action starting')
		index, amino_code = self._parse_action(action)

		# Decoding sequence in list of digits
		decoded_seq_list = self._decode(self.sequence)

		# Performing the action
		#print(decoded_seq_list)
		decoded_seq_list[index] = amino_code
		#print(decoded_seq_list)
		# Encoding the new sequence and storing it in the environment attributes
		decoded_seq_int = int("".join(map(str, decoded_seq_list)))
		self.sequence = self._encode(decoded_seq_int)
		self._shadow_sequence = decoded_seq_list

		# Computing the reward
		new_divergence = 0
		for i, _ in enumerate(self._shadow_sequence):
			new_divergence += self._shadow_sequence[i] != self._shadow_target[i]
		reward = 1 if new_divergence < self.divergence else -1
		self.divergence = new_divergence
		terminated = True if new_divergence == 0 else False
		print(reward)
		observation = self._get_obs()
		# print('End step')
		return observation, reward, terminated, {}

	def render(self, mode=None):
		print("MAJHKDHCBNHJBFDNHJK")
		return "hehehe"

	def _get_obs(self):
		state = (self.sequence, self.target, self.divergence)
		return np.array(state, dtype=np.float64)

	def _randomise_sequence(self):
		"""
		Method used when initialising the state of the environment. Returns an
		encoded integer and decoded list
		"""
		encoded_sequence = rnd.randint(0, self.upper_encoding_bound)
		decoded_list = self._decode(encoded_sequence)


		return encoded_sequence, decoded_list

	def _parse_action(self, action):
		index = action // self.base_num
		amino_code = action % self.base_num
		self._render_action(index, amino_code)
		return index, amino_code

	def _encode(self, number) -> int:
		"""
		Method to convert a baseX number into a base10 number (ie, encoding)
		Ex:
			   010011010 --> 154
		HP model (base2) --> Neural Network compatible value
		"""
		split_num = list(str(number))
		b = self.base_num
		i = len(split_num) - 1 # TODO: is there really a -1 ?

		result = sum([int(digit)*(b**(i-index)) for index, digit in 
			enumerate(split_num)])

		return result

	def _decode(self, number) -> list:
		"""
		Method to convert a base10 number into a baseX number (ie, decoding)
		Ex:
			154 --> 010011010
		"""
		digit_list = list()

		b = self.base_num
		
		while number:
			digit_list.append(number % b)
			number = number // b

		while len(digit_list) < self.seq_length:
			digit_list.insert(0, 0)
		return digit_list

	@staticmethod
	def _render_action(i, ac):
		print(f'Changing {i}th unit with a {ac}')

### Debugging Tests
def test_encoder():
	pass

if __name__ == '__main__':
	pass