import sys
sys.path.append('c:\\users\\ec_pe\\onedrive - imperial college london\\dapp 3\\sigmafold')

import gym
import numpy as np
from gym import spaces
import library

class SAW(gym.Env):
    """
    In this env, we use 1-hot encoding.
    4 rows:
    +---------+
    |   TBD   |
    | Forward |
    |  Left   |
    |  Right  |
    +---------+
    """
    def __init__(self, length) -> None:
        super().__init__()

        # Static attributes
        self.length = length
        self.target_shape = np.array((25, 25))

        # Dynamic attributes
        self.starting_pos = np.ndarray(shape=(2,))
        self.folding_onehot = np.ndarray(shape=(4, length)) # one-hot encoding of the SAW
        self.folding_matrix = np.ndarray(shape=(25, 25)) # as a visual matrix
        self.curr_length = int()

        # Spaces
        observation_dict = {
            'target': spaces.Box(0, 1, shape=(25,25), type=np.uint8),
            'starting_pos': spaces.Box(0, 25, shape=(2,), type=np.uint8),
            'folding_onehot': spaces.Box(0, 1, shape=(4,self.length), type=np.uint8),
        } 
        self.action_space = spaces.Discrete(3) # {0, 1, 2}
        self.observation_space = spaces.Dict(observation_dict)


    def reset(self, options=None, seed=None):
        self.target_shape = 0 # Here: generate a random shape
        self.folding_onehot = np.tile(np.array([[0,0,0,1]]).transpose(), (1, self.length))
        self.folding_matrix = np.zeros((25, 25))
        self.starting_pos = np.ndarray(shape=(2,)) # Here: put Josh's algo
        self.curr_length = 0
        return self._get_obs()
        

    def step(self, action):
        self.folding_onehot[action, self.curr_length] = 1
        self.folding_onehot[4, self.curr_length] = 0
        self.curr_length += 1
        obs = self._get_obs()
        # done = True if (self.curr_lengt == self.length) else False
        reward, done = self.compute_reward()
        return obs, reward, done, {}
                

    def render(self):
        return None

    def _get_obs(self):
        obs = {
            'target': self.target_shape,
            'folding_onehot': self.folding_onehot,
            'starting_pos': self.starting_pos,
        }
        return obs

    def compute_reward(self):
        pass