"""
Gets info about the shape being solved and the number of attempts it took to solve it.
Saves info to the log. c'est le caca de l'enfers
"""
import gym
from typing import Tuple, Dict
from collections import defaultdict


class ValidationMonitor(gym.Wrapper):

    def __init__(self, env: gym.Env) -> None:
        super().__init__(env)
        self.required_timesteps_dict = defaultdict(tuple)

    def step(self, action): # Still old step API, no truncation yet
        obs, reward, terminated, info = self.env.step(action)
        # get the attempt number
        if terminated and info["is_cleared"]:
            attempt_number = self.env.attempts
            # get the shape degeneracy
            shape_degeneracy = self.env.min_degen

            self.required_timesteps_dict[shape_degeneracy] = tuple(list(self.required_timesteps_dict[shape_degeneracy]) + [attempt_number])

        return obs, reward, terminated, info
