import sys # stoopid
import gym
import numpy as np
import pandas as pd
from gym import spaces
import os, sys
import pygame
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from library.db_query_templates import get_training_dataset
from library.shape_helper import path_to_shape_numbered, deserialize_path, deserialize_shape, deserialize_point, serialize_point
from tabulate import tabulate

class SAWValidation(gym.Env):
    """
    In this env, we use 1-hot encoding.
    Forward 0
    Right 1
    Left 2 
    +---------+
    """
    def __init__(self, length=None, render_mode=None, max_attempts=1, depth_field=1, shapes=None) -> None:            
        super().__init__()
        if shapes is None:
            self.shapes = get_training_dataset(length) # if length is None, the dataset will be of variable lengths
        else:
            self.shapes = shapes
        # duplicate every row in the dataframe, replace the starting_point field with the last element in the optimal_path field
        # and replace the starting_dir field with the last element in the optimal_path field for the DUPLICATES
        # this way we have a starting point and direction for every shape
        # self.shapes = pd.concat([self.shapes, self.shapes], ignore_index=True)
        for _, row in self.shapes.iterrows():
            # duplicate the row inside the dataframe
            # get the last element of the optimal_path field
            row = row.to_dict()
            path = deserialize_path(row["optimal_path"])
            # substract with second to last point to get the direction
            starting_dir = np.array(path[-2]) - np.array(path[-1])
            starting_pos = np.array(path[-1])

            # create a  duplicate row with the new starting point and direction
            new_row = row.copy()
            new_row["starting_point"] = serialize_point(starting_pos)
            new_row["starting_dir"] = serialize_point(starting_dir)
            # add using concat
            self.shapes = pd.concat([self.shapes, pd.DataFrame([new_row])], ignore_index=True)
        
        # shuffle the dataframe
        self.shapes = self.shapes.sample(frac=1).reset_index(drop=True)  
        # Static attributes
        
        self.render_mode = render_mode # activates or deativates the UI. Activated if set to "human"
        self.target_shape = np.array((25, 25))
        self.max_attempts = max_attempts # the maximum number of times the agent can attempt to place the shape

        # Dynamic attributes
        self.starting_pos = np.ndarray(shape=(2,))
        self.starting_dir = np.ndarray(shape=(2,))
        self.current_pos = np.ndarray(shape=(2,))
        self.length = 20 # arbitrary length for now, dynamically set later
        self.current_direction = np.ndarray(shape=(2,))
        self.folding_matrix = np.ndarray(shape=(25, 25)) # as a visual matrix
        self.last_action = np.ndarray(shape=(3,))
        self.cleared = False
        self.attempts = self.max_attempts + 1
        self.cleared_all = False # True if all shapes have been cleared
        self.fov_area = (2*depth_field+1)**2
        self.dirs = self.generate_fov_vector(depth=depth_field, fov_area=self.fov_area)
        
        self.sample_shape()

        # One hot encoded observation space
        self.action_space = spaces.MultiBinary(3)
        self.observation_space = spaces.MultiBinary(self.fov_area+3)

    def reset(self, options=None, seed=None):  
        if self.cleared: # shape was cleared entirely correctly, remove it frol the training dataset.
            # drop and reset indexing
            print(f"Shape cleared, shapes remaining: {len(self.shapes)}")
            self.shapes = self.shapes.drop(self.shape_index)
            self.shapes = self.shapes.reset_index(drop=True)  
            if self.shapes.empty:
                # let it run on the previous shape to avoid errors but set the flag to true so that the training can stop after this episode
                self.cleared_all = True
                self.attempts = 0
            else:
                # resample a new shape
                self.sample_shape()
                self.attempts = 0
                
        elif self.attempts >= self.max_attempts:
            print(f"Shape not cleared, deleting, shapes remaining: {len(self.shapes)}")
            self.shapes = self.shapes.drop(self.shape_index)
            self.shapes = self.shapes.reset_index(drop=True)  
            # get a new shape, unsuccessful clear
            self.sample_shape()
            self.attempts = 0
        
        else:
            # keep trying on current shape
            self.attempts += 1

        # reset the environment
        self.reset_properties()
        
        if self.render_mode == "human":
            self.render_init()
            
        return self._get_obs()    
    

    def step(self, action):        
        action = np.argmax(action)
        self.last_action = np.zeros((3, 1), dtype=np.int)
        self.last_action[action] = 1
        
       # This implements "real walking" in the environment. Facing right, left, and up, which avoids going back on yourself.
        if action == 1:  # Turn LEFT
            self.current_direction = (-self.current_direction[1], self.current_direction[0])
        elif action == 2:  # Turn RIGHT
            self.current_direction = (self.current_direction[1], -self.current_direction[0])
        # If action == 0, move straight ahead (no need to update the direction)x
        # Move the agent
        self.current_pos = (self.current_pos[0] + self.current_direction[0], self.current_pos[1] + self.current_direction[1])
        self.folding_matrix[self.current_pos[1], self.current_pos[0]] += 1
        self.curr_length += 1

        if self.render_mode == "human":
            self.render()
        # done = True if (self.curr_lengt == self.length) else False
        reward, done, info = self.compute_reward()
        
        obs = self._get_obs()
        return obs, reward, done, info
                

    def render(self):
        """
        Render the environment to the screen.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # render the current pos as a green square overwriting the target shape
        if self.render_mode == "human":
            pygame.draw.rect(self.shape_surface, (0,255,0), (self.current_pos[0]*self.cell_size, self.current_pos[1]*self.cell_size, self.cell_size, self.cell_size))
            self.screen.blit(self.shape_surface, (0,0))      
            time.sleep(0.5)
            pygame.display.flip()


    def _get_obs(self):
        """
        Get the observation of the environment.
        """
        boundary_vector = self.find_boundaries()

        obs = np.vstack([self.last_action, boundary_vector])
            
        return obs.flatten()
    

    def compute_reward(self):
        """
        Reward Function.
        If the folding matrix is the same as the target shape, then reward is 1.
        Else, reward is 0.
        """
        reward = 1/self.length
        done = False
        diff_matrix  = self.target_shape - self.folding_matrix

        info = {}
        info["remaining_shapes"] = len(self.shapes)
        
        if np.any(diff_matrix < 0): # out of bounds
            reward = -20*reward
            done = True
            info["termination_info"] =  "out_of_bound"
            info["is_cleared"] = False
        
        elif np.all(diff_matrix == 0): # correct final shape
            reward = 100*reward
            done = True
            self.cleared = True
            info["termination_info"] = self.min_degen # degen of shape cleared
            info["is_cleared"] = True
        
        elif np.any(self.folding_matrix > 1): # self-crossing
            reward = -20*reward
            done = True
            info["termination_info"] = "self_crossing"
            info["is_cleared"] = False

        return reward, done, info
    
# ======= Helper methods for the environment =======   
    def find_boundaries(self):
        """
        Look at neighbours of the current position. If top left is 1, then the current position is a boundary.
        """

        boundary_vector = np.zeros((self.fov_area,1), dtype=int)
         # top left to bottom right dirs in cartesian coordinates
        # dirs = np.array([[1,-1], [0,1], [1,1], [1,0], [0,-1], [-1,-1], [-1,0], [-1,1]])

        # Rotate dirs array based on the agent's current direction
        current_dir_idx = np.where((self.dirs == self.current_direction).all(axis=1))[0][0]
        dirs = np.roll(self.dirs, -current_dir_idx, axis=0)
            
        for i, direction in enumerate(dirs):
            # get the neighbour in the given direction
            neighbour = self.current_pos + direction

            # check if the neighbour is in the shape
            x, y = neighbour
            boundary_vector[i] = (self.target_shape[y, x] == 0) or (self.folding_matrix[y, x] > 0)
            boundary_vector[i] = int(boundary_vector[i])
          
        return boundary_vector
    

    @staticmethod
    def generate_fov_vector(depth, fov_area):
        """Method that generates the vector with all the relevant vision 
        directions depending on the depth_field attribute"""
        size = fov_area
        dirs = np.zeros((size, 2), dtype=int)
        counter = 0
        dirs_list = []

        for i in range(-depth, depth+1):
            for j in range(-depth, depth+1):
                dirs_list.append((i,j))
        
        dirs_list.remove((0,0))
        dirs = np.array(dirs_list)
        return dirs
    
    def sample_shape(self):
        sample = self.shapes.sample(1)
        self.shape_id = sample.shape_id.iloc[0]
        self.starting_pos = np.array(deserialize_point(sample.starting_point.iloc[0]))
        self.starting_dir = np.array(deserialize_point(sample.starting_dir.iloc[0]))
        self.target_shape = deserialize_shape(self.shape_id)
        self.shape_index  = sample.index[0]
        self.min_degen = sample.min_degeneracy.iloc[0]
        self.length = sample.length.iloc[0]

    def reset_properties(self):
        # reset attempts and cleared to start over on new shape
        
        self.cleared = False

        # reset shape properties
        self.folding_matrix = np.zeros((25, 25))
        self.last_action = np.zeros((3, 1))
        self.folding_matrix[self.starting_pos[1], self.starting_pos[0]] += 1
        self.curr_length = 0
        self.current_pos = tuple(np.copy(self.starting_pos))
        self.current_direction = tuple(np.copy(self.starting_dir))

    def render_init(self):
        pygame.init()
        self.screen_size = (500, 500)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption('SAW Visualization')
        self.cell_size = 20
        # Draw the target shape
        self.shape_surface = pygame.Surface(self.screen_size)
        self.shape_surface.fill((0,0,0))
        for i in range(25):
            for j in range(25):
                if self.target_shape[i, j] == 1:
                    pygame.draw.rect(self.shape_surface, (255,0,0), (j*self.cell_size, i*self.cell_size, self.cell_size, self.cell_size))

        # draw starting position
        pygame.draw.rect(self.shape_surface, (0,255,0), (self.starting_pos[0]*self.cell_size, self.starting_pos[1]*self.cell_size, self.cell_size, self.cell_size))
        pygame.display.flip()
        self.screen.blit(self.shape_surface, (0,0))
    

if __name__ == "__main__":
    env = SAW(16, render_mode="human")
    env.reset()
  


    
    