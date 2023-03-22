"""
File that implements modularity for reward function
"""

import numpy as np
import random as rnd
import scipy as sc
import matplotlib.pyplot as plt
import math
import sys
import os
import gym

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(
    os.path.dirname(
    os.path.dirname(
    os.path.dirname(
    os.path.dirname(
    os.path.dirname(
    os.path.abspath(__file__)))))))

import library.native_fold as nf
from legacy import tweaking_helper as ttk
import library.db_helper as dbtk

from inv_env.envs import tweak_env as twenv
import inv_env.envs.modular_spaces as msp
from inv_env.envs import data_functions as dtf
import inv_env.envs.aux_functions as aux
    
class RankingReward(twenv.TweakingInverse):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        # Modular Gym spaces
        spaces_struct = msp.ranking_space(self.seq_length, self.base_num)
        self.action_space, self.observation_space, self._get_obs = spaces_struct
        self.rank = int()
        self.step_rank = float()
        self.i = 0
        self.previous_sequence = str()

    def reset(self, **kwargs):
        print("===============================================================")
        checked = None
        while checked is None:
            matrix, id = ttk.get_shape(self.seq_length)
            checked = dbtk.check_shape(id)
        self.df = dbtk.db_energy_function(id)
        self.target_shape = matrix

        self.default_rank = max(self.df["ranking"]) + 1
        self.rank = self.default_rank
        self.step_rank = 100/(self.rank - 1)
        print(f'Meilleur rang: {self.default_rank}')
        self.i = 0
        return super().reset(**kwargs)
    
    def step(self, action):
        self.previous_sequence = self.sequence_str
        return super().step(action)
    
    # def compute_reward(self):
    #     self.i += 1        
    #     # check if the shape is in the dataframe if not, set reward to -100
    #     if self.sequence_str in self.df["sequence"].values:
    #         next_rank = self.df[self.df["sequence"] == self.sequence_str]["ranking"].values[0]
    #         delta = self.rank - next_rank
    #         reward = delta * self.step_rank
    #         self.rank = next_rank
    #         done = (self.rank == 1)
    #         print(f'Rank is {self.rank} | Reward is {reward} | Done? {done}')
    #         if done:
    #             print('YOUHOU', self.i)

    #         # print(f'Reward is {reward} | Done? {done} | Rank is {self.rank}')
    #     else:
    #         reward = -100
    #         self.rank = self.default_rank
    #         done = False
        
        
    #     return reward, done, {}
    
    def compute_reward(self):
        """
        n this new approach, every time the agent makes a tweak, we want to find whether the tweak has a similarity with any of the folds above it in the ranking. If it does, we want to reward the agent for that. If it doesn't, we want to penalize the agent for that.
        """
        self.i += 1
        done = False
        # check if the shape is in the dataframe if not, set reward to -100
        if self.sequence_str in self.df["sequence"].values:
            # check if current sequence is identical to one of the best sequences
            if self.sequence_str in self.df[self.df["ranking"] == 1]["sequence"].values:
                reward = 1
                done = True
                print('YOUHOU', self.i)
            else: 
                reward = 0
        else:
            index = [i for i in range(len(self.sequence_str)) if self.sequence_str[i] != self.previous_sequence[i]][0]
            # get the value of the first difference$
            value = self.sequence_str[index]

            # Check if any of the best sequences have that value at that index
            best_sequences = self.df[self.df["ranking"] == 1]["sequence"].values
            best_sequences = [seq for seq in best_sequences if seq[index] == value]
            if len(best_sequences) > 0:
                reward = 100
            else:
                reward = -100
            
        return reward, done, {}




