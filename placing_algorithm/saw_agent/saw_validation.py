import gym
import sys, os
import saw_gym_registration
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import json
import numpy as np
from sb3_contrib import RecurrentPPO
from library.db_query_templates import get_validation_dataset
from utils.validation_wrapper import ValidationMonitor

def validation_testing(path, env):
    validation_set = get_validation_dataset()
    print("Trying to clear validation set of shape", validation_set.shape)
    env = gym.make(env,
                   render_mode=None,
                   depth_field=1,
                   shapes=validation_set,
                   max_attempts=100)
    
    monitored_env = ValidationMonitor(env)
    model = RecurrentPPO.load(path, monitored_env)
    obs = env.reset()
    done = False
    states = None
    # set episode_starts 
    episode_starts = np.zeros((1,), dtype=np.bool)
    while not model.get_env().envs[0].cleared_all:
        # run the model
        action, states = model.predict(obs, state=states, deterministic=True)
        obs, reward, done, info = env.step(action)
        # set episode_starts
        episode_starts = np.zeros((1,), dtype=np.bool)
        if done:
            obs = env.reset()
            episode_starts = np.ones((1,), dtype=np.bool)
            states = None
        
    
    with open('data/validation_data.json', 'w') as outfile:
        data = model.get_env().envs[0].required_timesteps_dict
        data = {str(k): str(v) for k, v in data.items()}
        json.dump(data, outfile)

if __name__=='__main__':
    validation_testing('./models/fovTest/fovTest_depth_1', 'SAW-v0') # replace with model