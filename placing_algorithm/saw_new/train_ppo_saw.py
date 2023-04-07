"""
Where the training takes place. We will use the PPO algorithm to train the agent.
I am going to try to use Long-Short Term Memory (LSTM) to train the agent to remember the previous actions and see if that helps.
In The next few days, I will be researching to figure out the real differences between all these things.
"""
import os, sys
from gym import spaces
from stable_baselines3 import PPO # the policy 
from stable_baselines3.common.vec_env import DummyVecEnv
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from placing_algorithm.saw_new.envs.saw import SAW
from stable_baselines3 import PPO
from stable_baselines3.common.policies import MultiInputPolicy

from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor

import torch as th
from torch import nn

class CustomCombinedExtractor(BaseFeaturesExtractor):
    def __init__(self, observation_space: spaces.Dict, features_dim: int = 256):
        super().__init__(observation_space, features_dim=features_dim)

        extractors = {}
        total_concat_size = 0

        for key, subspace in observation_space.spaces.items():
            if key == "target":
                extractors[key] = nn.Sequential(
                    nn.Flatten(),
                    nn.Linear(25 * 25, 64),
                    nn.ReLU(),
                    nn.Linear(64, 32)
                )
                total_concat_size += 32
            elif key == "folding_onehot":
                extractors[key] = nn.Sequential(
                    nn.Flatten(),
                    nn.Linear(4 * 10, 32),
                    nn.ReLU(),
                    nn.Linear(32, 16)
                )
                total_concat_size += 16

        self.extractors = nn.ModuleDict(extractors)
        self._features_dim = total_concat_size

    def forward(self, observations) -> th.Tensor:
        encoded_tensor_list = []

        for key, extractor in self.extractors.items():
            encoded_tensor_list.append(extractor(observations[key]))

        return th.cat(encoded_tensor_list, dim=1)

def make_env(length, render_mode=None):
    def _init():
        return SAW(length, render_mode)
    return _init

class CustomMultiInputPolicy(MultiInputPolicy):
    def __init__(self, *args, **kwargs):
        super(CustomMultiInputPolicy, self).__init__(*args, **kwargs)
        self.mlp_extractor = CustomCombinedExtractor(self.observation_space)

# Set the desired length of the self-avoiding walks

length = 10

env = DummyVecEnv([make_env(length, render_mode="human")])

policy_kwargs = dict(
    net_arch=[64, 64]
)


# Create the PPO agent with the custom multi-input policy
model = PPO(CustomMultiInputPolicy, env, verbose=1, tensorboard_log="./ppo_tensorboard/", policy_kwargs=policy_kwargs)


# Train the agent
model.learn(total_timesteps=100000)

# Save the trained model
model.save("placing_algorithm/models/saw_ppo_mlp_model")