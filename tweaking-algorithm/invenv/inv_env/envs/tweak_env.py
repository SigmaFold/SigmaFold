import gym
import numpy as np
import random as rnd
from gym import spaces

class TweakingInverse(gym.Env):
    """
    Final class for the implementation of the learning environment for the 
    tweaking algorthm

    ### Action space

    ### Observation space

    | Num | Observation           | Min                 | Max               |
    |-----|-----------------------|---------------------|-------------------|
    | 0   | Sequence (int)        | 0                   | Inf               |
    | 1   | Target (ndarray)      | 0                   | Inf               |
    | 2   | Deviation (int)       | 0                   | Inf               |
    | 3   | Degen (int)           | 0                   | Inf               |
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
        self.target_matrix = np.array()

        # Environment Attributes


