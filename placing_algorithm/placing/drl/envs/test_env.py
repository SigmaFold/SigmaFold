from stable_baselines3.common.env_checker import check_env
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
from placing_algorithm.placing.drl.envs.baseline import Placing

env = Placing(length=10, render_mode="human")
check_env(env, warn=True)

# IMPORTANT: If you get an error saying gym has no GoalENv, comment out that line in the satble baselines code by pression control enter on the error.
# This should run perfectly to ensure that your environment is working correctly.