# """https://stackoverflow.com/questions/54022606/openai-gym-how-to-create-one-hot-observation-space"""

from gym import Wrapper, spaces
import numpy as np


class OneHotWrapper(Wrapper):
    def __init__(self, env):
        super().__init__(env)
        num_actions = env.action_space.n
        self.action_space = spaces.MultiBinary(num_actions)

    def step(self, action):
        # Find the index with the maximum value and set all other elements to 0
        one_hot_action = np.zeros_like(action)
        one_hot_action[np.argmax(action)] = 1
        return self.env.step(np.argmax(one_hot_action))

    def reset(self, **kwargs):
        return self.env.reset(**kwargs)