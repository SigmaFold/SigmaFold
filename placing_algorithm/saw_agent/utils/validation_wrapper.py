"""
Gets info about the shape being solved and the number of attempts it took to solve it.
Saves info to the log. c'est le caca de l'enfers
"""
import gym
from typing import Tuple, Dict
class ValidationMonitor(gym.Wrapper):

    def __init__(self, env: gym.Env) -> None:
        super().__init__(env)
        self.required_timesteps_dict = dict()
        self.temp_counter = 0
    
    def step(self, action): # Still old step API, no truncation yet
        obs, reward, terminated, info = self.env.step(action)
        if terminated:
            if info["is_cleared"]:
                if self.env.min_degen not in self.required_timesteps_dict:
                    self.required_timesteps_dict[self.env.min_degen] = tuple([self.temp_counter])
                else:
                    # get current tuple
                    current_tuple = self.required_timesteps_dict[self.env.min_degen]
                    # add new value to tuple
                    new_tuple = tuple(list(current_tuple) + [self.temp_counter])
                    # update dict
                    self.required_timesteps_dict[self.env.min_degen] = new_tuple
                    
                print("Nb of tires to clear shapes:", self.temp_counter)
                self.temp_counter = 0
                
            else:
                self.temp_counter +=1
            

        return obs, reward, terminated, info
