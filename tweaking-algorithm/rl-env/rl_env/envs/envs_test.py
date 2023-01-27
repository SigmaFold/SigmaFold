from sequence_cls import *
import gym
import rl_env

env = gym.make('rl_env/InverseFoldingEnv-v0', chain_length=5)