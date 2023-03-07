"""
Package to implement modularity for observation spaces. Each function is a 
specific implementation of the spaces.
"""


from gym import spaces
import math
import numpy as np

def initial_obs_space(seq_length, base_num):
    "Observation space is a dict"
    temp_bound = 2*int(math.ceil(seq_length/2))+1
    obs_struct = {
        'sequence_str': spaces.Text(max_length=seq_length), # String 
        # 'sequence_folded': spaces.Box(low=0, high=1, dtype=np.uint8), # Image
        'target_folded': spaces.Box(
        low=0, high=1, shape=(temp_bound, temp_bound), dtype=np.uint8),
        'reward_breakdown': spaces.Box(
        low=-10_000, high=10_000, shape=(2,1), dtype=np.int32),
    }

    observation_space = spaces.Dict(obs_struct)
    action_space = spaces.Discrete(base_num*seq_length)
    
    return action_space, observation_space

def debug_text_space(seq_length, base_num):
    "Observation space is a Text"
    observation_space = spaces.Text(max_length=seq_length)
    action_space = spaces.Discrete(base_num*seq_length)

    def _get_obs(self):
        return self.sequence_str
    
    return action_space, observation_space, _get_obs 

def debug_no_text_space(seq_length, base_num):
    "Observation space is a dict without Text"
    temp_bound = 2*int(math.ceil(seq_length/2))+1
    obs_struct = {
        'sequence_int': spaces.Discrete(2**seq_length), 
        'target_folded': spaces.Box(
        low=0, high=1, shape=(temp_bound, temp_bound), dtype=np.uint8),
        'reward_breakdown': spaces.Box(
        low=-10_000, high=10_000, shape=(2,), dtype=np.int32),
    }

    observation_space = spaces.Dict(obs_struct)
    action_space = spaces.Discrete(base_num*seq_length)

    def _get_obs(self):
        obs_struct = {
            'sequence_int': self.sequence_int, 
            'target_folded': self.target_shape,
            'reward_breakdown': np.array([self.current_degeneracy,
                                          self.current_deviation], dtype=np.int32),
        }

        return obs_struct

    
    return action_space, observation_space, _get_obs 

def ranking_space(seq_length, base_num):
    obs_struct = {
        'sequence_int': spaces.Discrete(2**seq_length), 
        'target_folded': spaces.Box(
        low=0, high=1, shape=(25, 25), dtype=np.uint8),
        'reward_breakdown': spaces.Box(
        low=-100, high=100, shape=(1,), dtype=np.int32),
    }

    action_space = spaces.Discrete(base_num*seq_length)
    observation_space = spaces.Dict(obs_struct)
    
    def _get_obs(self):
        obs_struct = {
            'sequence_int': self.sequence_int, 
            'target_folded': self.target_shape,
            'reward_breakdown': np.array([self.rank], dtype=np.int32),
        }
    
        return obs_struct
    
    return action_space, observation_space, _get_obs, 

class ClassicDictSpace:
    """
    Default space, where observations consist of 
        - Sequence: as an integer (not optimal)
        - Target: its shape, as a numpy array
        - Reward breakdown
    """
    def __init__(self, base_num, seq_length):
        obs_struct = {
            'sequence_int': spaces.Discrete(2**seq_length), 
            'target_folded': spaces.Box(
            low=0, high=1, shape=(25, 25), dtype=np.uint8),
            'reward_breakdown': spaces.Box(
            low=-100, high=100, shape=(1,), dtype=np.int32),
        }
        self.action_space = spaces.Discrete(base_num*seq_length)
        self.observation_space = spaces.Dict(obs_struct)

    def get_obs(self):
        obs_struct = {
            'sequence_int': self.sequence_int, 
            'target_folded': self.target_shape,
            'reward_breakdown': np.array([self.rank], dtype=np.int32),
        }
    
        return obs_struct
