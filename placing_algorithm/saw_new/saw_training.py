"""Name explains it all"""

import gym
import envs

from envs.saw import SAW
from sb3_contrib import RecurrentPPO
from gym import envs
print(envs)

def saw_training():
    params = {
        "learning_rate": 1e-5,
        "verbose": 1,
        # Add other stuff, idk
    }
    env = SAW(length=10, render_mode="human")
    model = RecurrentPPO("MultiInputLstmPolicy", env, **params)
    model.learn(10_000)

 
saw_training()