# This file is to manually test the environment (not the learning part)

import gymnasium
from  invenv.inv_env import register
import random as rnd 
import os
# from  inv_env import register # Either import statement is fine?

env = gymnasium.make('inv_fold/PrimWorld-v0')

env.reset()

for i in range(15):
	env.step(rnd.randint(0, 19))
