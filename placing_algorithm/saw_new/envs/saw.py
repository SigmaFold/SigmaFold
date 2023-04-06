import sys # stoopid
import gym
import numpy as np
from gym import spaces
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from library.db_query_templates import get_random_shape

class SAW(gym.Env):
    """
    In this env, we use 1-hot encoding.
    4 rows:
    +---------+
    |   Up    |
    | Down    |
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
        self.current_pos = tuple()
        self.folding_onehot = np.ndarray(shape=(4, length)) # one-hot encoding of the SAW
        self.folding_matrix = np.ndarray(shape=(25, 25)) # as a visual matrix
        self.curr_length = int()

        # Spaces
        observation_dict = {
            'target': spaces.Box(0, 1, shape=(25,25), dtype=np.uint8),
            'starting_pos': spaces.Box(0, 25, shape=(2,), dtype=np.uint8),
            'folding_onehot': spaces.Box(0, 1, shape=(4,self.length), dtype=np.uint8),
        }

        action_dict = {
            'select_start': spaces.Box(0, 25, shape=(2,)),
            'move': spaces.Discrete(4)
        } 
        self.action_space = spaces.Discrete(4) # {0, 1, 2}
        self.observation_space = spaces.Dict(observation_dict)


    def reset(self, options=None, seed=None):
        self.target_shape = get_random_shape(self.length)
        self.folding_onehot = np.zeros((4, self.length)) # initialise the one-hot encoding to 0 for all actions
        self.folding_matrix = np.zeros((25, 25))
        self.starting_pos = np.ndarray(shape=(2,)) # Here: put Josh's algo
        self.curr_length = 0
        self.current_pos = tuple(self.starting_pos)
        return self._get_obs()
        

    def step(self, action):
        self.folding_onehot[action, self.curr_length] = 1
        # self.folding_onehot[4, self.curr_length] = 0
        self.curr_length += 1
        obs = self._get_obs()

        
        action_to_move = {
            0: (0, 1),
            1: (0, -1),
            2: (-1, 0),
            3: (1,0 ),
        }
        self.current_pos = tuple(np.add(self.current_pos, action_to_move[action]))
        self.folding_matrix[self.current_pos] = 1

        


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
        """
        If the folding matrix is the same as the target shape, then reward is 1.
        Else, reward is 0.
        """
        reward = 0
        done = False

        diff_matrix  = self.target_shape - self.folding_matrix
        
        # if any element is equal to -1 then something was placed out of bounds 
        if np.any(diff_matrix < 0):
            reward = -1
            done = True
        
        elif np.all(diff_matrix == 0):
            reward = 1
            done = True
        
        elif np.any(self.folding_matrx > 1):
            reward = -1
            done = True

        return reward, done
        


        
        
        
        

