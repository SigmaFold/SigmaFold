"""Name explains it all"""

import sys
sys.path.append('c:/Users/ec_pe/OneDrive - Imperial College London/DAPP3/SigmaFold/')

import gym
from sb3_contrib import RecurrentPPO
from gym import envs
print(envs)

def saw_training():
    params = {
        "learning_rate": 1e-5,
        # Add other stuff, idk
    }
    env = gym.make("sigma_env/SAW-v0")
    model = RecurrentPPO("MultiInputLstmPolicy", env, **params)

saw_training()