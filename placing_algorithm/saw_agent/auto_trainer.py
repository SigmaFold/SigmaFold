"""
Completes all the tests for us on Google  Colab for us.
"""

from saw_training import *
import saw_gym_registration

# Test 1 : done

# # Test 2: gigamodel. 
total_timesteps = 100
save_interval = 100_000
folder = 'gigamodel'
fov = [1, 2, 5, 10]

length = None # train on all lengths

for i in range(4):
    run_name = f'fov_{fov[i]}_test'
    saw_training("SAW-v0", folder=folder, run_name=run_name, save_interval=save_interval, depth_field=fov[i], length=length, total_timesteps=total_timesteps)


# # Test 3: max_attempts test 
# total_timesteps = 1_000_000
# save_interval = 100_000
# folder = 'max_attempts_test'
# max_attempts = [1, 100, 10000]
# fov = 1
# length = None

# for i in range(3):
#     run_name = f'max_attempts_{max_attempts[i]}'
#     saw_training("SAW-v0", folder=folder, run_name=run_name, save_interval=save_interval, depth_field=fov, length=length, total_timesteps=total_timesteps, max_attemps=max_attempts[i])

# Test 4: random baseline
# total_timesteps = 1_000_000
# save_interval = 100_000
# folder = 'random_agent_test'
# fov = 1
# length = None

# run_name = f'random_agent'
# saw_training("RAND-v0", folder=folder, run_name=run_name, save_interval=save_interval, depth_field=fov, length=length, total_timesteps=total_timesteps)


