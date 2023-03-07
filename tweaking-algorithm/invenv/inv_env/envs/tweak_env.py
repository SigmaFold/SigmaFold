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
import inv_env.envs.modular_spaces as msp
import inv_env.envs.modular_reward as mrew

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
    """

    DEFAULT_HP_TABLE = {
        'H': 1,
        'P': 0,
    }

    def __init__(self,
        base_num=2,
        seq_length=10,
        amino_code_table=DEFAULT_HP_TABLE) -> None:
        print('Starting creation process')
        super().__init__()

        # Static Attributes
        self.seq_length = seq_length
        self.base_num = base_num
        self.amino_code_table = amino_code_table
        self.upper_encoding_bound = seq_length * base_num

        # Dynamic core attributes
        self.sequence_int = 8
        self.sequence_list = list()
        self.sequence_str = str()
        self.target_shape = np.ndarray(shape=None) # TODO: improve init shape
        self.fold = np.ndarray(shape=None)

        # ??
        self.current_degeneracy = 100
        self.current_deviation = 0
        
        # Modular Gym spaces
        spaces_struct = msp.debug_no_text_space(seq_length, base_num)
        self.action_space, self.observation_space, self._get_obs = spaces_struct

        # Modular Reward code
        self.pre_routine, self.compute_reward = mrew.ranking_reward(self)
        print('creation process is finished')
        
    def reset(self, options=None,seed=None):
        self.target_shape = aux.generate_shape(self.seq_length)
        self.sequence_str = heuristics(self.target_shape)
        self.sequence_int = self._encode(dtf.seq_heur2env(seq=self.sequence_str))
        self.sequence_list = self._decode(self.sequence_int)
        
        heap = nf.compute_energy(
            self.paths,
            self.sequence_str)
        _, degen = nf.native_fold(heap)
        degen /= 2 # Halve degen because of refelections
        self.current_degeneracy = degen
        obs = self.get_obs()
        return obs

    def step(self, action):
        index, amino_code = self._parse_action(action)
        
        # updating everything
        self.sequence_list[index] = amino_code
        self.sequence_int = self._encode(self.sequence_list)
        
        # folding the sequence and getting the degeneracy
        # heap = nf.compute_energy(
        #     self.paths,
        #     dtf.seq_list2str(self.sequence_list))
        # folds, degen = nf.native_fold(heap)
        # folds = [dtf.fold_list2matrix(fold, self.seq_length) for fold in folds]
        
        # the folds + degeneracy are fed to reward function
        # reward, info = mrew.legacy_tweaking_reward(self,
        #     folds, self.target_shape, degen, self.seq_length, 
        #     self.current_degeneracy, self.current_deviation)

        reward, info = self.compute_reward(self)

        self.current_degeneracy = info['degen']
        self.current_deviation = info['corr']
        # done = (deviation == self._min_conv) # TODO: add 5% threshold

        terminated = (self.current_deviation == 0) & (self.current_degeneracy < 6)
        obs = self.get_obs()

        return obs, reward, terminated, {'seq_list': self.sequence_list}
    
    def render(self):
        return None
    
    def get_obs(self):
        """
        Important method that controls the flux of information towards
        the neural network.
        """
        return self._get_obs(self)
    
    def _init_sequence(self):
        """
        Method used when initialising the state of the environment. Returns an
        encoded integer and decoded list
        """
        # TODO: max range is now 2^length... is it correct?
        encoded_sequence = rnd.randint(0, self.base_num**self.seq_length)
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
    
    def _get_info(self):
        info = (self.sequence_list, )

    def _parse_action(self, action):
        index = action // self.base_num
        amino_code = action % self.base_num
        
        return index, amino_code
    