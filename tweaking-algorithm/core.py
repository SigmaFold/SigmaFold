import numpy as np
import gym
from  invenv.inv_env import register
from gym import spaces
from stable_baselines3 import PPO

def deep_rl_main(chain_length=10):

    # Setup
    env = gym.make('inv_fold/PrimWorld-v0')
    states = env.observation_space
    actions = env.action_space
    print(type(actions))

    # Instantiate the agent
    model = PPO('MlpPolicy', env, learning_rate=1e-3, verbose=1)
    # Train the agent
    model.learn(total_timesteps=int(2e5))

deep_rl_main()
