import sys # stoopid
import gym
import numpy as np
from gym import spaces
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from library.db_query_templates import *
from library.shape_helper import *

class Placing(gym.Env):
    """
    Placing environment for the Folding@AmongUs project.
    """
    def __init__(self, length) -> None:
        super().__init__()

        # Static attributes
        self.length = length
        self.target_shape = np.array((25, 25))

        # Dynamic attributes
        # self.starting_pos = np.ndarray(shape=(2,))
        # self.cuurent_pos = tuple()
        # self.folding_onehot = np.ndarray(shape=(4, length)) # one-hot encoding of the SAW
        # self.folding_matrix = np.ndarray(shape=(25, 25)) # as a visual matrix
        # self.curr_length = int()

        # Spaces
        observation_dict = {
            'target': spaces.Box(0, 1, shape=(25,25), type=np.uint8),
            'path': spaces.Box(0, self.length, shape=(25,25), type=np.uint8),
            'HPassignments': spaces.Box(0, 2, shape=(25,25), type=np.uint8),
        }

        action_dict = {
            'select_position': spaces.Box(0, 0, shape=(25,25)),
            'assign': spaces.Discrete(2),
        } 
        self.action_space = spaces.Dict(action_dict)
        self.observation_space = spaces.Dict(observation_dict)


    def generate_path(self):
        _, shape_id = get_random_shape(self.length)
        sequences = get_all_sequences_for_shape(shape_id)

        # sort sequences by degeneracy in an ascending order and save the first one's sequence and path
        sequences = sequences.sort_values(by=["degeneracy"], ascending=True)
        best_sequence = sequences.iloc[0]
        sequence = best_sequence["sequence"]
        path = best_sequence["path"]

        # separate the path into a list of nodes
        path = path.split(" ")
        path.remove("")

        # convert the strings in path to tuples seperated by commas
        path = [tuple(map(int, node.split(","))) for node in path]

        path_mat = path_to_shape_numbered(path, self.length)
        return path_mat
    
    
    def reset(self, options=None, seed=None):
        self.target_shape = get_random_shape(self.length)
        self.path_shape = self.generate_path()
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
        
        elif np.any(self.folding_matrix > 1):
            reward = -1
            done = True

        return reward, done
        


        
        
        
        

