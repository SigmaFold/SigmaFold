import sys # stoopid
import gym
import numpy as np
import pandas as pd
from gym import spaces
import os, sys
import pygame
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from library.db_query_templates import get_random_shape, get_all_sequences_for_shape
from library.shape_helper import path_to_shape_numbered, deserialize_path

class SAW(gym.Env):
    """
    In this env, we use 1-hot encoding.
    4 rows:
    +---------+
    |  Right      | (because going up in cartesian coordinates is going down in the matrix)
    |  Left   |
    |  Forwa  |
      TBD     |
    +---------+
    """
    def __init__(self, length, render_mode=None, max_attempts=100) -> None:
        super().__init__()
        

        # Static attributes
        self.length = length
        self.render_mode = render_mode # activates or deativates the UI. Activated if set to "human"
        self.target_shape = np.array((25, 25))
        self.max_attempts = max_attempts # the maximum number of times the agent can attempt to place the shape

        # Dynamic attributes
        self.starting_pos = np.ndarray(shape=(2,))
        self.current_pos = np.ndarray(shape=(2,))
        self.attempts = 0 # everyone deserves a second chance - this is the number of times the agent has attempted to place the shape
        
        # length is -1 because the starting position is already defined
        self.folding_onehot = np.ndarray(shape=(4, length-1)) # one-hot encoding of the SAW
        # Initialise fith row to be entirely ones 
        self.folding_onehot[3] = np.ones(shape=(length-1,))
        # Curent direction algo is facing 
        self.current_direction = np.array([0, 1]) # start facing down 


        self.folding_matrix = np.ndarray(shape=(25, 25)) # as a visual matrix
        self.curr_length = 0

        # Spaces
        observation_dict = {
            'target': spaces.Box(0, 1, shape=(25,25), dtype=np.uint8),
            'folding_onehot': spaces.Box(0, 1, shape=(4,self.length - 1), dtype=np.uint8),
            "folding_matrix": spaces.Box(0, 1, shape=(25,25), dtype=np.uint8)
        }

        action_dict = {
            'select_start': spaces.Box(0, 25, shape=(2,)),
            'move': spaces.Discrete(3)
        } 
        self.action_space = spaces.Discrete(3) # {0, 1, 2}
        self.observation_space = spaces.Dict(observation_dict)

    def get_best_starting_point(self, shape_id):
        sequences = get_all_sequences_for_shape(shape_id)
        # sort df by degeneracy
        sequences = sequences.sort_values(by=['degeneracy'], ascending=True)
        # get the first row
        best_sequence = sequences.iloc[0]    
        # get the sequence of the first row 
        sequence = best_sequence['sequence']
        # get the path of the first row 
        path = best_sequence['path']
        # convert path to list of tuples
        path = deserialize_path(path)
        _, shape , path = path_to_shape_numbered(path, sequence)
        # get the starting point of the path
        # convert to ndarray
        # get the position of the first 1 in the shape matrix
        starting_point = np.argwhere(shape == 1)[0]
        # flip to be cartesian coordinates
        starting_point = np.flip(starting_point)

        # check if the starting point is the position of a 1 in the "shape" matrix
        if not shape[starting_point[1], starting_point[0]] == 1:
            raise Exception("The starting point is not a 1 in the shape matrix")
        
        return starting_point
    
    
    def reset(self, options=None, seed=None):
        if self.attempts >= self.max_attempts or self.attempts == 0:
            self.target_shape, shape_id = get_random_shape(self.length)
            self.starting_pos = self.get_best_starting_point(shape_id)
            self.attempts = 0
        else:
            self.attempts += 1
        self.folding_onehot = np.zeros((4, self.length-1)) # initialise the one-hot encoding to 0 for all actions
        self.folding_onehot[3] = np.ones(shape=(self.length-1,)) # initialise the last row to be entirely ones

        self.folding_matrix = np.zeros((25, 25))

        # start in a posoition that is a 1 in the target shape matrix
        
        self.folding_matrix[self.starting_pos[1], self.starting_pos[0]] += 1
        self.curr_length = 0
        self.current_pos = np.copy(self.starting_pos)

     
        if self.render_mode == "human":
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

            
            pygame.draw.rect(self.shape_surface, (255,0,0), (self.starting_pos[0]*self.cell_size, self.starting_pos[1]*self.cell_size, self.cell_size, self.cell_size))
            pygame.display.flip()
            self.screen.blit(self.shape_surface, (0,0))

            
        return self._get_obs()
        

    def step(self, action):
        self.folding_onehot[action, self.curr_length] = 1
        # set the bottom row of the one-hot encoding to 0 (TBD row) This supposedly gives the agent an understanding of how many moves it has left
        self.folding_onehot[3, self.curr_length] = 0
        self.curr_length += 1
        obs = self._get_obs()

        # This implements "real walking" in the environment. Facing right, left, and up, which avoids going back on yourself.
        if action == 0:  # Turn RIGHT
            self.current_direction = (-self.current_direction[1], self.current_direction[0])
        elif action == 1:  # Turn LEFT
            self.current_direction = (self.current_direction[1], -self.current_direction[0])
        # If action == 2, move straight ahead (no need to update the direction)
        
        self.current_pos = tuple(np.add(self.current_pos, self.current_direction))
        self.folding_matrix[self.current_pos[1], self.current_pos[0]] += 1
        if self.render_mode == "human":
            self.render()
        # done = True if (self.curr_lengt == self.length) else False
        reward, done = self.compute_reward()
        return obs, reward, done, {}
                

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
        # IMPORTANT, SET THE DATATYPE TO BE CORRECT HERE !
        obs = {
            'target': self.target_shape.astype(np.uint8),
            'folding_onehot': self.folding_onehot.astype(np.uint8),
            'folding_matrix': self.folding_matrix.astype(np.uint8), # Temporarily added the folding matrix to the observation
        }
        # print("obs", obs)
        return obs

    def compute_reward(self):
        """
        Reward Function.
        If the folding matrix is the same as the target shape, then reward is 1.
        Else, reward is 0.
        """
        reward = 0.1
        done = False
        # TODO : Final path similarity reward
        diff_matrix  = self.target_shape - self.folding_matrix

        if self.curr_length == self.length -1:
            done = True
        
        # if any element is equal to -1 then something was placed out of bounds 
        if np.any(diff_matrix < 0):
            reward = -2
            done = True
        
        elif np.all(diff_matrix == 0):
            reward = 10
            done = True
        
        elif np.any(self.folding_matrix > 1):
            reward = -2
            done = True

        return reward, done
        


        
        
        