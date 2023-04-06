import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from placing_algorithm.saw_new.envs.saw import SAW
import matplotlib.pyplot as plt


def test_saw():
    env = SAW(length=5)
    print("Action space:", env.action_space)
    print("Observation space:", env.observation_space)
    assert env.action_space.n == 4
    assert env.observation_space["target"].shape == (25, 25)
    assert env.observation_space["starting_pos"].shape == (2,)
    assert env.observation_space["folding_onehot"].shape == (4, 5)
    test_reset()

def test_reset():
    env = SAW(length=5)
    obs = env.reset()
    print("Observation:", obs)
    assert obs["target"].shape == (25, 25)
    assert obs["starting_pos"].shape == (2,)
    assert obs["folding_onehot"].shape == (4, 5)
    assert obs["folding_onehot"].sum() == 0

def test_step():
    env = SAW(length=5)
    env.reset()
    actions = [0, 1, 0, 2] # should fail at 3rd step
    # display the target shape, overlay the folding matrix
    # uncomment if you want to see the folding matrix at each step
    # plt.imshow(env.target_shape, cmap="gray")
    # plt.imshow(env.folding_matrix, cmap="jet", alpha=0.3)
    # plt.show()
    for action in actions:
        obs, reward, done, info = env.step(action)
        print("Action:", action)
        print("folding_onehot:", env.folding_onehot)
        print("folding_matrix:", env.folding_matrix)
        print("curr_length:", env.curr_length)
        print("Reward:", reward)
        print("Done:", done)
        print("------")
        # uncomment if you want to see the folding matrix at each step
        # plt.imshow(env.target_shape, cmap="gray")
        # plt.imshow(env.folding_matrix, cmap="jet", alpha=0.5)
        # plt.show()
    assert env.curr_length == 4
    assert done == True
    

    

    



if __name__ == "__main__":
    test_step()