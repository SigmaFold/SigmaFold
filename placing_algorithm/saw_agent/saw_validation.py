import gym
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
import json
import numpy as np
from sb3_contrib import RecurrentPPO
from library.db_query_templates import get_validation_dataset
from utils.validation_wrapper import ValidationMonitor
from stable_baselines3.common.evaluation import evaluate_policy

def validation_testing(path, env):
    validation_set = get_validation_dataset(target_n=16)
    env = gym.make(env,
                   render_mode=None,
                   depth_field=2,
                   shapes=validation_set,
                   max_attempts=10_000_000)
    
    monitored_env = ValidationMonitor(env)
    model = RecurrentPPO.load(path, monitored_env)
    obs = env.reset()
    dones = False
    states = None
    episode_starts = np.ones((env.num_envs,), dtype=bool)
    while not model.get_env().envs[0].cleared_all:
        env.reset()
        while not dones:
            actions, states = model.predict(obs, state=states, episode_start=episode_starts, deterministic=True)
            obs, rewards, dones, infos = env.step(actions)

    with open('data/validation_data.json', 'w') as outfile:
        data = model.get_env().envs[0].required_timesteps_dict
        data = {str(k): str(v) for k, v in data.items()}
        json.dump(data, outfile)

if __name__=='__main__':
    validation_testing('./models/fovTest/fovTest_depth_1', 'SAW-v0')