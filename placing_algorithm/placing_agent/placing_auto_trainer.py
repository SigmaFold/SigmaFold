
from placing_training import *
import gym_registration

# # Test 1 - neighbour_test 
# total_timesteps = 1_000_000
# save_interval = 100_000
# folder = 'neighbour_test'
# fov = [1, 2, 5] # 0.5 is likely to cuase a crash
# length = None # train on all lengths
# for i in range(3):
#     run_name = f'fov_{fov[i]}_test'
#     placing_training("Placing-v0", folder=folder, run_name=run_name, save_interval=save_interval, depth_field=fov[i], length=length, total_timesteps=total_timesteps)
# # FOV 0.5 
# fov = 1
# length = None
# run_name = f'fov_{fov}_test'
# placing_training("Placing-v0", folder=folder, run_name=run_name, save_interval=save_interval, depth_field=fov, length=length, total_timesteps=total_timesteps, count_diagonal=False)

# test 2 - validation: use neighbour test at fov 1
# Test 3: random baseline
print("Starting random agent test")
total_timesteps = 1_000_000
save_interval = 100_000
folder = 'random_agent_test'
fov = 1
length = None
run_name = f'random_agent'
placing_training("RANDHP-v0", folder=folder, run_name=run_name, save_interval=save_interval, depth_field=fov, length=length, total_timesteps=total_timesteps)


# # test 4, extrapolation test
# total_timesteps = 1_000_000
# save_interval = 100_000
# folder = 'extrapolation_test'
# fov = 1
# length = 14
# run_name = f'extrapolation_fov_{fov}_n_{length}'
# placing_training("Placing-v0", folder=folder, run_name=run_name, save_interval=save_interval, depth_field=fov, length=length, total_timesteps=total_timesteps)
