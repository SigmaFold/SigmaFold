"""Name explains it all"""

import gym
import gym_registration
import envs
from envs.saw import SAW
from sb3_contrib import RecurrentPPO
from gym import envs

def saw_training(name='auto'):
    params = {
        "learning_rate": 1e-4,
        "n_steps": 128,
        "batch_size": 128,
        "n_epochs": 10,
        "gamma": 0.99,
        "gae_lambda": 0.95,
        "clip_range": 0.2,
        "clip_range_vf": None,
        "normalize_advantage": True,
        "ent_coef": 0.0,
        "vf_coef": 0.5,
        "max_grad_norm": 0.5,
        "use_sde": False,
        "sde_sample_freq": -1,
        "target_kl": None,
        "verbose": 1,
        
        # Add other stuff, idk
    }
    env = gym.make("SAW-v0", length=16, render_mode=None)
    model = RecurrentPPO("MlpLstmPolicy", env, tensorboard_log=f'./logs/{name}', **params)
    model.learn(1000_000_000_000)

saw_training('onehot_encoding') 