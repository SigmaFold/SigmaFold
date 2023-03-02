import numpy as np
import gym
from  invenv.inv_env import register
from stable_baselines3 import DQN, PPO
from gym.wrappers import TimeLimit

# Global Parameters
models_dir = "saved_weights"
TIMESTEPS_SAVE = 50
iters = 0 # change initial value to latest iters to avoid overwriting files

def training_main(limit=False):
    """
    Main function that trains the learning agent. Weights of the Neural network
    are saved every `TIMESTEPS_SAVE` into a new file. This saved weights can be 
    used to then use the agent in predcting sequences.  
    """

    # Setup
    timed_env = gym.make('inv_fold/TweakWorld-v0', 
                         max_episode_steps=5_000, 
                         apply_api_compatibility=True,
                         disable_env_checker=False)
    
    # timed_env = TimeLimit(env=base_env, max_episode_steps=5)
    timed_env.reset()

    # Instantiate the agent
    model = PPO('MultiInputPolicy', timed_env, learning_rate=1e-3, verbose=1)
    iters = 1 
    is_learning = True
    print('going into learning')
    
    # Train the agent
    while is_learning:
        iters += 1
        model.learn(total_timesteps=TIMESTEPS_SAVE, reset_num_timesteps=False)
        model.save(f'{models_dir}/{TIMESTEPS_SAVE*iters}')
        is_learning = (iters < limit) if limit is not False else True
        
training_main(50)
