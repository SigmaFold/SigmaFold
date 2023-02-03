import numpy as np
import gym
from  invenv.inv_env import register
from stable_baselines3 import PPO

# Global Parameters
models_dir = "saved_weights"
TIMESTEPS_SAVE = 10000
iters = 0 # change initial value to latest iters to avoid overwriting files

def training_main():
    """
    Main function that trains the learning agent. Weights of the Neural network
    are saved every `TIMESTEPS_SAVE` into a new file. This saved weights can be 
    used to then use the agent in predcting sequences.  
    """

    # Setup
    env = gym.make('inv_fold/PrimWorld-v0')
    env.reset()

    # Instantiate the agent
    model = PPO('MlpPolicy', env, learning_rate=1e-3, verbose=1)

    # Train the agent
    while True:
        iters += 1
        model.learn(total_timesteps=TIMESTEPS_SAVE, reset_num_timesteps=False)
        model.save(f'{models_dir}/{TIMESTEPS_SAVE*iters}')
        
training_main()
