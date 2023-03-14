import matplotlib.pyplot as plt
import numpy as np
import gym
from inv_env import register

# Need a test for uniformity of initialisation
def initialPdf(sample_num=1_000):
    """
    To test that the initial sequences are indeed sampled from a uniform 
    distribution (no bias) with enough range to cover to full sequence spectrum
    Conclusion: this is now the case
    """
    env = gym.make('inv_fold/TweakWorld-v0')
    initial_seq_array = np.zeros(sample_num)
    for i in range(sample_num):
        obs, *_ = env.reset()
        print(obs)
        initial_seq_array[i] = obs[0]
    
    _ = plt.hist(initial_seq_array, bins='auto', density=True)
    plt.show()

initialPdf()