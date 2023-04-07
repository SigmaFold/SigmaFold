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
    |   Down  |
    | Up      |
    |  Left   |
    |  Right  |
    +---------+
    """
    def __init__(self, length, render_mode=None) -> None:
        super().__init__()
        

        # Static attributes
        self.length = length
        self.render_mode = render_mode # activates or deativates the UI. Activated if set to "human"
        self.target_shape = np.array((25, 25))

        # Dynamic attributes
        self.starting_pos = np.ndarray(shape=(2,))
        # declare current position as a numpy row vector
        self.current_pos = np.ndarray(shape=(2,))

        self.folding_onehot = np.ndarray(shape=(4, length)) # one-hot encoding of the SAW
        self.folding_matrix = np.ndarray(shape=(25, 25)) # as a visual matrix
        self.curr_length = int()

        # Spaces
        observation_dict = {
            'target': spaces.Box(0, 1, shape=(25,25), dtype=np.uint8),
            'folding_onehot': spaces.Box(0, 1, shape=(4,self.length), dtype=np.uint8)
        }

        action_dict = {
            'select_start': spaces.Box(0, 25, shape=(2,)),
            'move': spaces.Discrete(4)
        } 
        self.action_space = spaces.Discrete(4) # {0, 1, 2, 3}
        self.observation_space = spaces.Dict(observation_dict)
        print(self.observation_space)

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
        _, _, path = path_to_shape_numbered(path, sequence)
        # get the starting point of the path
        starting_point = path[0]
        # convert to ndarray
        starting_point = np.array(starting_point)

        # check if the starting point is valid
        if self.target_shape[starting_point[1], starting_point[0]] == 0:
            raise Exception("The starting point is not valid.")
        
        return starting_point
    
    
    def reset(self, options=None, seed=None):
        self.target_shape, shape_id = get_random_shape(self.length)
        
        
        self.folding_onehot = np.zeros((4, self.length)) # initialise the one-hot encoding to 0 for all actions
        self.folding_matrix = np.zeros((25, 25))

        # start in a posoition that is a 1 in the target shape matrix
        self.starting_pos = self.get_best_starting_point(shape_id)
        self.folding_matrix[self.starting_pos[1], self.starting_pos[0]] += 1
        self.curr_length = 0
        self.current_pos = np.copy(self.starting_pos)

     
        if self.render_mode == "human":
            pygame.init()
            self.screen_size = (500, 500)
            self.screen = pygame.display.set_mode(self.screen_size)
            pygame.display.set_caption('RANDSAW Visualization')
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
        # self.folding_onehot[4, self.curr_length] = 0
        self.curr_length += 1
        obs = self._get_obs()

        action_to_move = {
            0: (0, 1),
            1: (0, -1),
            2: (-1, 0),
            3: (1,0),
        }
        
        self.current_pos = tuple(np.add(self.current_pos, action_to_move[action]))
        self.folding_matrix[self.current_pos[1], self.current_pos[0]] += 1
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
        pygame.draw.rect(self.shape_surface, (0,255,0), (self.current_pos[0]*self.cell_size, self.current_pos[1]*self.cell_size, self.cell_size, self.cell_size))
        self.screen.blit(self.shape_surface, (0,0))      
        time.sleep(3)
        pygame.display.flip()

    def _get_obs(self):
        """
        Get the observation of the environment.
        """
        # IMPORTANT, SET THE DATATYPE TO BE CORRECT HERE !
        obs = {
            'target': self.target_shape.astype(np.uint8),
            'folding_onehot': self.folding_onehot.astype(np.uint8),
            #TODO temporarily removed the starting pos from the observation in case its not relevant. add and compare results
            #TODO: Shoild we add the folding matrix to the observation?
        }
        print("obs", obs)
        return obs

    def compute_reward(self):
        """
        Reward Function.
        If the folding matrix is the same as the target shape, then reward is 1.
        Else, reward is 0.
        """
        reward = 0
        done = False

        diff_matrix  = self.target_shape - self.folding_matrix
        
        # if any element is equal to -1 then something was placed out of bounds 
        if np.any(diff_matrix < 0):
            reward = -1
            done = True
        
        elif np.all(diff_matrix == 0):
            reward = 1
            done = True
        
        elif np.any(self.folding_matrix > 1):
            reward = -1
            done = True

        return reward, done
        


        
        
        