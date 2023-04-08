import gym
import numpy as np
from gym import spaces
import os
import sys
import pygame
import time
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
from library.shape_helper import path_to_shape_numbered, deserialize_path, deserialize_point, deserialize_shape
from library.db_query_templates import get_random_shape, get_all_sequences_for_shape, find_HP_assignments, get_all_random_shapes

class Placing(gym.Env):
    """
    Placing environment for the Folding@AmongUs project.
    """

    def __init__(self, length, using_prev_agent = False, max_attempts=1, target_shape=None, path_shape=None, render_mode=None) -> None:
        super().__init__()

        # get the initial shape
        self.shapes = get_all_random_shapes(length)
        sample = self.shapes.sample(1)
        shape_id = sample.shape_id.iloc[0]
        self.starting_pos = np.array(deserialize_point(sample.starting_point.iloc[0]))
        self.starting_dir = np.array(deserialize_point(sample.starting_dir.iloc[0]))
        self.target_shape = deserialize_shape(shape_id)
        self.correct_sequence = sample.best_sequence.iloc[0]
        self.path = sample.optimal_path.iloc[0]
        self.curr_sequence = []


        # Static attributes
        self.length = length
        self.using_prev_agent = using_prev_agent
        self.max_attempts = max_attempts
        self.render_mode = render_mode  # activates or deativates the UI. Activated if set to "human"
        self.num_actions = 0
        self.attempts = 0

        #TODO: limit position to be following the path
        #TODO: add one hot encoding for observation

        self.action_space = spaces.MultiBinary(2)
        self.observation_space = spaces.MultiBinary(6) # 4 neighbours + 2 HP assignments

    # def generate_path(self, shape_id):
    #     #TODO: make it so this doesnt call db at every reset
    #     # get all sequences for the target shape
    #     sequences = get_all_sequences_for_shape(shape_id)
    #     # sort sequences by degeneracy in an ascending order and save the first one's sequence and path
    #     sequences = sequences.sort_values(by=["degeneracy"], ascending=True)
    #     best_sequence = sequences.iloc[0]
    #     sequence = best_sequence["sequence"]
    #     path = best_sequence["path"]
    #     # convert path string into list of tuples
    #     path = deserialize_path(path)
    #     path_mat, HP_mat, _ = path_to_shape_numbered(
    #         path, sequence)    # convert path into a numbered matrix
    #     return path_mat, HP_mat, sequence

    def reset(self, options=None, seed=None):
        # get the initial shape
        if self.attempts >= self.max_attempts:
            self.shapes = get_all_random_shapes(self.length)
            sample = self.shapes.sample(1)
            shape_id = sample.shape_id.iloc[0]
            self.starting_pos = np.array(deserialize_point(sample.starting_point.iloc[0]))
            self.starting_dir = np.array(deserialize_point(sample.starting_dir.iloc[0]))
            self.target_shape = deserialize_shape(shape_id)
            self.correct_sequence = sample.best_sequence.iloc[0]
            self.path = sample.optimal_path.iloc[0]
            self.curr_sequence = []
            self.attempts = 0
        else:
            self.attempts += 1
        
        self.correct_sequences, self.correctHPassignments = find_HP_assignments(self.length, self.target_shape, self.path_shape)
        self.curr_sequence = []

        if self.render_mode == "human":
            pygame.init()
            self.screen_size = (500, 500)
            self.screen = pygame.display.set_mode(self.screen_size)
            pygame.display.set_caption('HP Visualization')
            self.cell_size = 20
            # Draw the target shape
            self.shape_surface = pygame.Surface(self.screen_size)
            self.shape_surface.fill((0, 0, 0))
            for i in range(25):
                for j in range(25):
                    if self.target_shape[i, j] == 1:
                        pygame.draw.rect(self.shape_surface, (255, 0, 0), (
                            j*self.cell_size, i*self.cell_size, self.cell_size, self.cell_size))

            pygame.display.flip()
            self.screen.blit(self.shape_surface, (0, 0))
        return self._get_obs()

    def step(self, action):
        #TODO: Make it so that it iterates through the path instead of the whole grid
        actions_dict = {0: "H", 1: "P"}
        action = np.argmax(action)
        action = actions_dict[action]
        self.curr_sequence.append(action)
        idx  = len(self.curr_sequence) - 1
        
        pos_action_row = self.path[idx][1]
        pos_action_col = self.path[idx][0]
        assign_action = self.curr_sequence[idx]
        
        obs = self._get_obs()
        if self.render_mode == "human":
            self.render(pos_action_row, pos_action_col, assign_action)
        reward, done = self.compute_reward(pos_action_row, pos_action_col)
        return obs, reward, done, {}

    def render(self, pos_action_row, pos_action_col, assign_action):
        """
        Render the environment to the screen.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # render the current pos as a green square overwriting the target shape
        if assign_action == "H":
            pygame.draw.circle(self.shape_surface, (0, 255, 0), (
                pos_action_col*self.cell_size, pos_action_row*self.cell_size), radius=self.cell_size/3)
        else:
            pygame.draw.circle(self.shape_surface, (0, 0, 255), (
                pos_action_col*self.cell_size, pos_action_row*self.cell_size), radius=self.cell_size/3)

        self.screen.blit(self.shape_surface, (0, 0))
        pygame.display.flip()

    def _get_obs(self):
        """
        Get the observation of the environment.
        """
        # IMPORTANT, SET THE DATATYPE TO BE CORRECT HERE
        obs = np.zeros(6, dtype=np.int8)
        # get the neighbours of the current position

        return obs

    def compute_reward(self, pos_action_row, pos_action_col):
        """
        If the folding matrix is the same as the target shape, then reward is 1.
        Else, reward is 0.
        """
        reward = 0
        done = False

        # fail immediately if out of bounds
        if self.target_shape[pos_action_row, pos_action_col] == 0:
            reward = -1
            done = True

        # if any element is equal to -1 then something was placed out of bounds
        if self.num_actions == self.length:
            reward_list = []
            for correct_mat in self.correctHPassignments:
                diff_matrix = correct_mat - self.HPassignments
                # sum absolute values of all the elements in diff_matrix and normalise it
                sum = np.sum(abs(diff_matrix)) / self.length
                reward_list.append(((1-sum)-0.5)*2)
            reward = max(reward_list)
            done = True

        return reward, done


    def find_neighbours(self):
        """
        Look at neighbours of the current position.
        00 - not connectable (either on the chain or a boundary)
        01 - conenctable and empty
        10 - H
        11  - P
        """
        neighbour_vector = np.zeros((16,1), dtype=int)
   
         # top left to bottom right dirs in cartesian coordinates
        dirs = np.array([[1,-1], [0,1], [1,1], [1,0], [0,-1], [-1,-1], [-1,0], [-1,1]])
            
        for i, direction in enumerate(dirs):
            # get the neighbour in the given direction
            neighbour = self.current_pos + direction
            # check if the neighbour is in the shape
            x, y = neighbour
            
            #TODO: make neighbour vector of length 16 depending on what each position is
        
        return neighbour_vector
    

if __name__ == "__main__":
    env  = Placing(16)