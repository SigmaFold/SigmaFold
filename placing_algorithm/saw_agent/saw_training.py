"""Name explains it all"""

import gym
import saw_gym_registration
import envs
from envs.saw import SAW
from sb3_contrib import RecurrentPPO
from gym import envs
import os 
from stable_baselines3.common.callbacks import BaseCallback
import json
from utils.info_collector_wrapper import InfoCollectorWrapper
from collections import defaultdict

class CustomCallback(BaseCallback):
    def __init__(self, save_interval, save_path, folder, run_name,  verbose=0):
        super(CustomCallback, self).__init__(verbose)
        self.save_interval = save_interval
        self.save_path = save_path
        self.timesteps_since_save = 0
        self.folder = folder
        self.run_name = run_name

    def _on_step(self) -> bool:
        self.timesteps_since_save += 1

        # Save the model
        if self.timesteps_since_save >= self.save_interval:
            self.model.save(self.save_path)
            self.timesteps_since_save = 0

        # Stop training if shapes list is empty
        if self.model.get_env().envs[0].cleared_all:
            print("Cleared all shapes")
            print("Number of timesteps:", self.num_timesteps)
            # save nulber of timestep to file
            with open(f'./logs/{self.folder}/{self.run_name}/timesteps.txt', 'w') as f:
                f.write(str(self.num_timesteps))
            return False
        return True

    def _on_training_end(self) -> None:
        with open(f'./logs/{self.folder}/{self.run_name}/degen_histo.json', 'w') as outfile: # made it save to the same folder as the tensorboard for that run
            # make all keys strings
            degen = self.model.get_env().envs[0].degen_counter
            degen = {str(k): v for k, v in degen.items()}
            # make value string
            degen = {k: str(v) for k, v in degen.items()}
            json.dump(degen, outfile)

        with open(f'./logs/{self.folder}/{self.run_name}/failure_modes.json', 'w') as outfile:
            # make all keys strings
            failure_modes = self.model.get_env().envs[0].failure_modes
            failure_modes = {str(k): str(v) for k, v in failure_modes.items()}
            json.dump(failure_modes, outfile)

        with open(f'./logs/{self.folder}/{self.run_name}/nb_not_cleared.json', 'w') as outfile:
            remaining_df = self.model.get_env().envs[0].shapes # TODO: size?
            uncleared_shapes = defaultdict(int)
            # extract min_degeneracy for each row, store in dict
            for i, row in remaining_df.iterrows():
                uncleared_shapes[row['min_degeneracy']] += 1
                # make all keys strings
            uncleared_shapes = {str(k): str(v) for k, v in uncleared_shapes.items()}    
            json.dump(uncleared_shapes, outfile)
            # save dataframe
            remaining_df.to_csv(f'./logs/{self.folder}/{self.run_name}/remaining_shapes.csv')

        print("Successfully saved additional info")
        return super()._on_training_end()

def saw_training(env, folder='auto', run_name='default', save_interval=100_000, depth_field=1, length=14, render_mode=None, total_timesteps=1_000_000, max_attempts=1, **kwargs):
    params = {
        "learning_rate": 1e-3,
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
    
    model_save_path = f'./models/{folder}/{run_name}'
    env = gym.make(env, render_mode=render_mode, depth_field=depth_field, length=length, max_attempts=max_attempts)
    env  = InfoCollectorWrapper(env)
    model = RecurrentPPO("MlpLstmPolicy", env, tensorboard_log=f'./logs/{folder}/{run_name}', **params)
    custom_callback = CustomCallback(save_interval=save_interval, save_path=model_save_path, folder=folder, run_name=run_name)
    model.learn(
        total_timesteps=total_timesteps,
        callback=custom_callback,
    )
    
    model.save(model_save_path)  

if __name__=='__main__':
    #folder = str(input("What is the type of the test? "))
    #run_name = str(input("What is the name of the run? "))
    #saw_training('SAW-v0', folder, run_name)

    folder = "test"
    run_name = "test"
    saw_training('SAW-v0', folder, run_name)

     