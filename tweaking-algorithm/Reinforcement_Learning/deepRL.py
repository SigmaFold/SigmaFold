import builtins
import numpy as np
import os
import gym
import rl_env

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam

from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

Adam._name = 'hey' # Dummy name but else, won't work
    
os.environ["TF_CPP_MIN_LOG_LEVEL"]="1" # Doesn't work anyway

def build_model(states, actions):
    """
    Function that sets up the Neural Network. 
    Input Layer: state space
    2 densly connected layers
    Output Layer: action space
    """
    model = Sequential()
    model.add(input(shape=(1, states)))
    model.add(Flatten(input_shape=(1,states)))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(actions, activation='linear'))
    return model

def build_agent(model, actions):
    """
    Function to build a DeepRL agent and combines 
    """
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit=50000, window_length=1)
    dqn = DQNAgent(model=model, memory=memory, policy=policy, 
        nb_actions=actions, nb_steps_warmup=10, target_model_update=1e-2)
    return dqn

class TestCallback(tf.keras.callbacks.Callback):
    def on_train_start(self, logs=None):
        print("callback summoned")

def deep_rl_main(chain_length=10):

    # Setup
    env = gym.make('rl_env/InverseFoldingEnv-v0', chain_length=chain_length)
    states = 2**chain_length
    actions = 2*chain_length

    model = build_model(states, actions)
    model.summary()

    dqn = build_agent(model, actions)
    dqn.compile(tf.keras.optimizers.Adam(lr=1e-3), metrics=['mae'])
    dqn.fit(env, nb_steps=50000, visualize=True, verbose=1, callbacks=[])

    dqn.save_weights('dqn_weights.h5f', overwrite=True)

    print("hello")


deep_rl_main()
