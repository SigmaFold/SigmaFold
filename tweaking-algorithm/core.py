import numpy as np
import gymnasium as gym
from  invenv.inv_env import register
from gymnasium import spaces


import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.optimizers import Adam
import tensorflow.keras.backend as K
from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

from sigma_opt import CustomAdam
from preproc_layer import PrintingLayer
from neural_networks import build_model

Adam._name = 'hey' # Dummy name but else, won't work
    
import tensorflow as tf

def build_agent(model, actions):
    """
    Function to build a DeepRL agent and combines 
    """
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit=50000, window_length=1)
    dqn = DQNAgent(model=model, memory=memory, policy=policy, 
        nb_actions=actions, nb_steps_warmup=10, target_model_update=1e-2)
    return dqn

def deep_rl_main(chain_length=10):

    # Setup
    env = gym.make('inv_fold/PrimWorld-v0')
    states = 2
    actions = 2*chain_length

    model = build_model(states, actions)
    model.summary()

    dqn = build_agent(model, actions)
    dqn.compile(optimizer=CustomAdam(), metrics=['mae'])
    dqn.fit(env, nb_steps=50000, visualize=True, verbose=1)

    dqn.save_weights('dqn_weights.h5f', overwrite=True)

    print("hello")


deep_rl_main()
