import gym
import numpy as np
import random as rnd
from gym import spaces

class TweakingInverse(gym.Env):
    """
    Final class for the implementation of the learning environment for the 
    tweaking algorthm

    ### Action space
    For each unit, X actions possible. Again use Euclidien encoding

    ### Observation space

    | Num | Observation           | Min                 | Max               |
    |-----|-----------------------|---------------------|-------------------|
    | 0   | Sequence (int)        | 0                   | Inf               |
    | 1   | Target (ndarray)      | 0                   | Inf               |
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

        # Dynamic attributes
        self.sequence_int = int()
        self._sequence_list = list()
        self.target_path = np.array()

        # Environment Attributes
        # idk

    def resest(self, options=None,seed=None):
        self.sequence, self._sequence_list = self._init_sequence()
        self.target_path = self._init_path()

    def step(self, action):
        pass

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
