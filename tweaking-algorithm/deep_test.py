import builtins
import numpy as np
import gymnasium as gym
from  invenv.inv_env import register
from gymnasium import spaces

from preproc_layer import PrintingLayer

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.optimizers import Adam
import tensorflow.keras.backend as K
from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

Adam._name = 'hey' # Dummy name but else, won't work
    
import tensorflow as tf

class MyAdam(tf.keras.optimizers.Optimizer):
    """Custom Adam optimizer that is compatible with the Keras RL DQNAgent."""
    def __init__(self, learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-7, name="mytest", **kwargs):
        self.learning_rate = learning_rate
        super(MyAdam, self).__init__(name, **kwargs)
        with tf.keras.backend.name_scope(self.__class__.__name__):

            self.iterations = tf.keras.backend.variable(0, dtype='int64', name='iterations')
            self.learning_rate = tf.keras.backend.variable(learning_rate, name='learning_rate')
            self.beta_1 = tf.keras.backend.variable(beta_1, name='beta_1')
            self.beta_2 = tf.keras.backend.variable(beta_2, name='beta_2')
            self.epsilon = tf.keras.backend.variable(epsilon, name='epsilon')

    def get_updates(self, loss, params):
        grads = tf.gradients(loss, params)
        self.updates = [tf.keras.backend.update_add(self.iterations, 1)]

        lr = self.learning_rate * (tf.keras.backend.sqrt(1. - tf.keras.backend.pow(self.beta_2, self.iterations)) /
                                   (1. - tf.keras.backend.pow(self.beta_1, self.iterations)))

        t = tf.cast(self.iterations, tf.float32) + 1
        lr_t = lr * (tf.keras.backend.sqrt(1. - tf.keras.backend.pow(self.beta_2, t)) /
                     (1. - tf.keras.backend.pow(self.beta_1, t)))

        for p, g in zip(params, grads):
            m = tf.keras.backend.zeros(shape=tf.keras.backend.int_shape(p), dtype=tf.dtypes.float32)
            v = tf.keras.backend.zeros(shape=tf.keras.backend.int_shape(p), dtype=tf.dtypes.float32)

            m_t = (self.beta_1 * m) + (1. - self.beta_1)

class CustomAdam(tf.keras.optimizers.Optimizer):

    def __init__(self, lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-7, name='dcdc', **kwargs):
        self._learning_rate = lr
        self._name = name
        super(CustomAdam, self).__init__(name, **kwargs)
        self.lr = tf.keras.backend.variable(lr, name='lr')
        self.beta_1 = tf.keras.backend.variable(beta_1, name='beta_1')
        self.beta_2 = tf.keras.backend.variable(beta_2, name='beta_2')
        self.epsilon = epsilon

    def get_updates(self, loss, params):
        grads = self.get_gradients(loss, params)
        self.updates = [K.update_add(self.iterations, 1)]

        t = K.cast(self.iterations, K.floatx()) + 1
        lr_t = self.lr * (K.sqrt(1. - K.pow(self.beta_2, t)) /
                         (1. - K.pow(self.beta_1, t)))

        for p, g in zip(params, grads):
            m = K.zeros(K.int_shape(p), dtype=K.floatx())
            v = K.zeros(K.int_shape(p), dtype=K.floatx())

            m_t = (self.beta_1 * m) + (1. - self.beta_1) * g
            v_t = (self.beta_2 * v) + (1. - self.beta_2) * K.square(g)
            p_t = p - lr_t * m_t / (K.sqrt(v_t) + self.epsilon)

            self.updates.append(K.update(m, m_t))
            self.updates.append(K.update(v, v_t))
            self.updates.append(K.update(p, p_t))
        return self.updates

    def get_gradients(self, loss, params):
        return K.gradients(loss, params)

def build_model(states, actions):
    """
    Function that sets up the Neural Network. 
    Input Layer: state space
    2 densly connected layers
    Output Layer: action space
    """


    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(3,)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(20, activation='softmax')
    ])

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
