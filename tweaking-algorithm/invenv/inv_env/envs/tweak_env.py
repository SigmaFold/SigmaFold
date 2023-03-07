import gym
import numpy as np
import random as rnd
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(
    os.path.dirname(
    os.path.dirname(
    os.path.dirname(
    os.path.dirname(
    os.path.dirname(
    os.path.abspath(__file__)))))))

# Custom libraries
import library.native_fold as nf
import inv_env.envs.aux_functions as aux
import inv_env.envs.data_functions as dtf
from heursitics_algorithm.heuristics import heuristics

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
    2) sequence_list: representing the sequence as a list of bases (0,1...), so
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
    
    The information space only contains redundant information, and its main
    purpose is to interact with the GUI to display clean information.

    ### Notes and Todos:

    1) Lower and upper bounds of reward_breakdown (line 120) are temp solutions,
    need more refined numbers there.

    2) Warning from package: unconventional shape (is it a big deal?)

    3) Must switch to new step API to account for truncation vs termination
        -> DONE
    """

    DEFAULT_HP_TABLE = {
        'H': 1,
        'P': 0,
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

        # Dynamic core attributes
        self.sequence_int = 8
        self.sequence_list = list()
        self.sequence_str = str()
        self.target_shape = np.ndarray(shape=None) # TODO: improve init shape
        
    def reset(self, options=None,seed=None):
        # Stuff must happen here

        self.sequence_str = heuristics(self.target_shape)
        self.sequence_int = self._encode(dtf.seq_heur2env(seq=self.sequence_str))
        self.sequence_list = self._decode(self.sequence_int)
        obs = self._get_obs(self)
        return obs

    def step(self, action):
        index, amino_code = self._parse_action(action)
        
        # updating everything
        self.sequence_list[index] = amino_code
        self.sequence_int = self._encode(self.sequence_list)
        
        reward, done, info = self.compute_reward(self)
        obs = self.get_obs(self)
        info['seq_list': self.sequence_list]

        return obs, reward, done, info
    
    def render(self):
        return None
    
    def get_obs(self):
        """
        Important method that controls the flux of information towards
        the neural network.
        """
        return self._get_obs(self)

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

    def _encode(self, number: list[int]) -> int:
        """
        Method to convert a baseX number into a base10 number (ie, encoding)
        Ex:
               010011010 --> 154
        HP model (base2) --> Neural Network compatible value
        """

        split_num = number
        b = self.base_num
        i = len(split_num) - 1 # TODO: is there really a -1 ?

        result = sum([int(digit)*(b**(i-index)) for index, digit in 
            enumerate(split_num)])

        return result

    def _parse_action(self, action):
        index = action // self.base_num
        amino_code = action % self.base_num
        
        return index, amino_code
    