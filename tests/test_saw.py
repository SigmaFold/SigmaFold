import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from placing_algorithm.saw_new.envs.saw import SAW


def test_saw():
    env = SAW(length=5)
    print("Action space:", env.action_space)
    print("Observation space:", env.observation_space)





if __name__ == "__main__":
    test_saw()

