import gym
import numpy as np
import random as rnd
from gym import spaces
import scipy as sc
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import inv_env.envs.aux_functions as aux 

class TweakingInverse(gym.Env):
    """
    Final class for the implementation of the learning environment for the 
    tweaking algorthm

    ### Overview

    The environment consists of two items:
    1) The sequence, that can be acted upon by the agent at each step
    2) The target shape, that cannot be changed by the agent

    And the reward function.

    ### The Sequence

    The sequence has two forms:
    1) sequence_int: representing the sequence as a base10 number. This makes
        this integer non-readable by humans but it is a better input data for
        neural networks
    2) _sequence_list: representing the sequence as a list of bases (0,1...), so
        that it can be understand by humans. It is useful because actions can
        only be performed on this reprentation (the int version compacts 
        everything in one single number)
    To go from one form to the other, the environent relies on the encode() and
    decode() methods.
    
    ### The target 

    The target shape is represented as a ndarray with 0 (void) and 1 (actual
    shape). This is the only representation of the shape.

    ### Reward function

    Has not yet been finished so will write something later.

    ### Action space
    
    Action can only be integers ranging fro 0 to an upper bound we set. Hence we
    have map this set of integers (so 0, 1, ... N) to the action space (assign a
    H to the n-th unit). To do so we use Euclidian division mapping, which works
    as follows:
    1) Take the action integer and do an Euclidian division by the number of 
        different bases (2 for HP, 4 for HPNX...)
    2) The quotient is the index of the modified amino-acid
    3) The rest is the new amino-acid (0 -> H, 1 -> P)

    ### Observation space

    Array of 4 values:

    | Num | Observation           | Min                 | Max               |
    |-----|-----------------------|---------------------|-------------------|
    | 0   | Sequence (int)        | 0                   | Inf               |
    | 1   | Target shape(ndarray) | 0                   | Inf               |
    | 2   | Deviation (int)       | 0                   | Inf               |
    | 3   | Degeneracy (int)      | 0                   | Inf               |
    """

    DEFAULT_HP_TABLE = {
        'H': 0,
        'P': 1,
    }

    def __init__(self,
        base_num=2,
        seq_length=10,
        amino_code_table=DEFAULT_HP_TABLE) -> None:
        super().__init__()

        # Static Attributes
        self.seq_length = seq_length
        self.base_num = base_num
        self.amino_code_table = amino_code_table
        self.upper_encoding_bound = seq_length * base_num

        # Dynamic attributes
        self.sequence_int = int()
        self._sequence_list = list()
        self.target_shape = np.ndarray(shape=None)

        self.current_degeneracy = int()
        self.current_deviation = int()

        self._min_conv = np.mean(sc.signal.convolve(self.target_shape, self.target_shape))
        
        print("Environment initialised!")
        
        # Environment Attributes
        # idk

    def reset(self, options=None,seed=None):
        self.target_shape = aux.generate_shape(self.seq_length)
        self.sequence, self._sequence_list = self._init_sequence()
        obs = self._get_obs()
        info = self._get_info()

        return obs, {}

    def step(self, action):
        index, amino_code = self._parse_action(action)
        
        # updating everything
        self._sequence_list[index] = amino_code
        self.sequence_int = self._encode(self._sequence_list)
    
        sequence_str = ''.join(self._sequence_list).replace('1', 'H').replace('0', 'P')
        reward, dev, deg = aux.get_reward(sequence_str)
        
        obs = self._get_obs()

        done = (dev == self._min_conv) # TODO: add 5% threshold
        
        return obs, reward, done, {}

    def render(self):
        pass

    def _init_sequence(self):
        """
        Method used when initialising the state of the environment. Returns an
        encoded integer and decoded list
        """
        encoded_sequence = rnd.randint(0, self.upper_encoding_bound)
        decoded_list = self._decode(encoded_sequence)

        return encoded_sequence, decoded_list

    def _decode(self, number) -> list:
        """
        Method to convert a base10 number into a baseX number (ie, decoding)
        Ex:
            154 --> 010011010
        There is 0-padding on the left.
        """
        digit_list = list()

        b = self.base_num
        
        while number:
            digit_list.append(number % b)
            number = number // b

        while len(digit_list) < self.seq_length:
            digit_list.insert(0, 0)

        return digit_list

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
    
    def _get_obs(self):
        state = (self.sequence_int, self.target_shape, self.current_degeneracy,
            self.current_deviation)
        return state

    def _get_info(self):
        info = (self._sequence_list, )

    def _parse_action(self, action):
        index = action // self.base_num
        amino_code = action % self.base_num
        self._render_action(index, amino_code)
        return index, amino_code