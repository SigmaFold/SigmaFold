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

# Create the environment
