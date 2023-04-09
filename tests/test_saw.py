import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from placing_algorithm.saw_new.envs.saw import SAW
from placing_algorithm.saw_new.envs.one_hot_space import OneHotWrapper
import numpy as np
import matplotlib.pyplot as plt


def test_saw():
    env = SAW(length=16)
    env = OneHotWrapper(env)
    print("Action space:", env.action_space)
    print("Observation space:", env.observation_space)

    

def test_reset():
    env = SAW(length=16)
    obs = env.reset()
    print("shape", obs.shape)
    assert obs.shape == (11,)
    # assert obs["target"].shape == (25, 25)
    # assert obs["folding_onehot"].shape == (4,9) # new shape
    # assert obs["folding_onehot"].sum() == 9 # now max length is 9 not 10 for length 10

def test_step():
    env = SAW(length=16, render_mode="human")
    env.reset()
    actions = [0,1,0,0,0]  # go down, go left, go straight, go straight, go straight
    actions_dict = {
        0: [1, 0, 0],
        1: [0, 1, 0],
        2: [1, 0, 0],

    }
    # display the target shape, overlay the folding matrix
    # uncomment if you want to see the folding matrix at each step
    print("Starting direction", env.starting_dir)

    for action in actions:
        obs, reward, done, info = env.step(actions_dict[action])
        print("Action \n:", action)
        print("Observation \n:", obs)
        print("last_action \n:", env.last_action)
        print("curr_length:", env.curr_length)
        print("Reward:", reward)
        print("Done:", done)
        print("------")
    
    assert env.curr_length == 5
    
if __name__ == "__main__":
    test_reset()
    test_step()
    test_saw()
