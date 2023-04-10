import gym
from typing import Union
from stable_baselines3.common import type_aliases
from stable_baselines3.common.vec_env import VecEnv

def evaluate_efficiency(
    model: "type_aliases.PolicyPredictor",
    env: "str",
    shapes, 
):
    """Runs policy for on a set shapes and for each shape returns the number of
    timesteps required to solve it.
    """
    ep_count = [] # TODO: initialise size?
    shaped_env = gym.make(env, shapes=shapes, max_attempts=float('inf'))
    while not shapes.empty:
        pass
