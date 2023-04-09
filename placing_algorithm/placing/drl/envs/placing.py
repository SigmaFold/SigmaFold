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

    def __init__(self, length, max_attempts=1, render_mode=None) -> None:
        super().__init__()

        # get the initial shape
        self.shapes = get_all_random_shapes(length)
        sample = self.shapes.sample(1)
        self.shape_id = sample.shape_id.iloc[0]
        self.HP_matrix = deserialize_shape(self.shape_id)    # currently 0s and 1s, but adding H or P will correspond to 2 or 3 respectively
        self.correct_sequence = sample.best_sequence.iloc[0]    # the correct sequence for the target shape as a string
        self.path = deserialize_path(sample.optimal_path.iloc[0])   # path as list of tuples coordinates        
        self.curr_pos = self.path[0]  # position in the target shape matrix as tuple


        self.curr_sequence = [] # where we will be storing hp assingments


        # Static attributes
        self.length = length
        self.max_attempts = max_attempts
        self.render_mode = render_mode  # activates or deativates the UI. Activated if set to "human"
        self.num_actions = 0
        self.attempts = 0

        #TODO: limit position to be following the path
        #TODO: add one hot encoding for observation

        self.action_space = spaces.MultiBinary(2)
        self.observation_space = spaces.MultiBinary(10) # 4 neighbours + 2 HP assignments

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
            sample = self.shapes.sample(1)
            self.shape_id = sample.shape_id.iloc[0]
            self.HP_matrix = deserialize_shape(self.shape_id)    # currently 0s and 1s, but adding H or P will correspond to 2 or 3 respectively
            self.correct_sequence = sample.best_sequence.iloc[0]    # the correct sequence for the target shape as a string
            self.path = deserialize_path(sample.optimal_path.iloc[0])   # path as list of tuples coordinates            
            self.curr_pos = self.path[0]  # position in the target shape matrix as tuple
            self.curr_sequence = []
            self.attempts = 0
        else:
            self.attempts += 1
            self.HP_matrix = deserialize_shape(self.shape_id)    # currently 0s and 1s, but adding H or P will correspond to 2 or 3 respectively
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
        # updating the current sequence with the action
        actions_dict = {0: "H", 1: "P"}
        action = np.argmax(action)
        action = actions_dict[action]
        self.curr_sequence.append(action)

        # updating the HP matrix according to action
        pos_action_col, pos_action_row = self.curr_pos
        assign_action = action
        assign_dict = {"H": 2, "P": 3}
        self.HP_matrix[pos_action_row, pos_action_col] = assign_dict[assign_action]

        # updating the current position
        self.num_actions += 1
        self.curr_pos = self.path[self.num_actions]
        
        # render
        if self.render_mode == "human":
            self.render(pos_action_row, pos_action_col, assign_action)
        
        # check reward
        reward, done = self.compute_reward(pos_action_row, pos_action_col)
        # get observation space
        obs = self._get_obs()
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

    def compute_reward(self):
        """
        If the folding matrix is the same as the target shape, then reward is 1.
        Else, reward is 0.
        """
        reward = 0
        done = False
        # TODO: Compare the last element of the current sequence with the correct sequence
        # # fail immediately if out of bounds
        # if self.target_shape[pos_action_row, pos_action_col] == 0:
        #     reward = -1
        #     done = True

        # # if any element is equal to -1 then something was placed out of bounds
        # if self.num_actions == self.length:
        #     reward_list = []
        #     for correct_mat in self.correctHPassignments:
        #         diff_matrix = correct_mat - self.HPassignments
        #         # sum absolute values of all the elements in diff_matrix and normalise it
        #         sum = np.sum(abs(diff_matrix)) / self.length
        #         reward_list.append(((1-sum)-0.5)*2)
        #     reward = max(reward_list)
        #     done = True

        return reward, done


    def find_neighbours(self):
        """
        Look at neighbours of the current position.
        00 - not connectable (either on the chain or a boundary)
        01 - conenctable and empty
        10 - H
        11  - P
        """
        neighbour_vector = np.zeros((8,1), dtype=int)
   
        # up, right, down and left dirs in matrix [m, n]
        dirs = np.array([[0, -1], [1, 0], [0, 1], [-1, 0]])
            
        curr_pos_list = list(self.curr_pos) # convert it to a list
        
        # fill the neighbour_vector appropriately
        for i, dir in enumerate(dirs):
            # get the neighbour in the given direction
            neighbour_pos = [x + y for x, y in zip(curr_pos_list, dir)]
            # check neighbour characteristic in shape
            neighbour_char = self.HP_matrix[neighbour_pos[1], neighbour_pos[0]]
            if neighbour_char == 0: # if outside boundary, assign 00
                neighbour_vector[2*i] = 0
                neighbour_vector[2*i+1] = 0
            elif neighbour_char == 1: # in boundary but unassigned
                # if in chain, assign 00
                if self.num_actions == 0 and self.path[self.num_actions + 1] == tuple(neighbour_pos):
                    neighbour_vector[2*i] = 0
                    neighbour_vector[2*i+1] = 0
                elif self.num_actions == self.length and self.path[self.num_actions - 1] == tuple(neighbour_pos):
                    neighbour_vector[2*i] = 0
                    neighbour_vector[2*i+1] = 0
                elif self.path[self.num_actions - 1] == tuple(neighbour_pos) or self.path[self.num_actions + 1] == tuple(neighbour_pos):
                    neighbour_vector[2*i] = 0
                    neighbour_vector[2*i+1] = 0
                else:   # if not in chain, assign 01
                    neighbour_vector[2*i] = 0
                    neighbour_vector[2*i+1] = 1
            elif neighbour_char == 2: # H
                # if in chain, assign 00
                if self.num_actions == 0 and self.path[self.num_actions + 1] == tuple(neighbour_pos):
                    neighbour_vector[2*i] = 0
                    neighbour_vector[2*i+1] = 0
                elif self.num_actions == self.length and self.path[self.num_actions - 1] == tuple(neighbour_pos):
                    neighbour_vector[2*i] = 0
                    neighbour_vector[2*i+1] = 0
                elif self.path[self.num_actions - 1] == tuple(neighbour_pos) or self.path[self.num_actions + 1] == tuple(neighbour_pos):
                    neighbour_vector[2*i] = 0
                    neighbour_vector[2*i+1] = 0
                else:   # if not in chain, assign 10
                    neighbour_vector[2*i] = 1
                    neighbour_vector[2*i+1] = 0
            elif neighbour_char == 3: # P
                # if in chain, assign 00
                if self.num_actions == 0 and self.path[self.num_actions + 1] == tuple(neighbour_pos):
                    neighbour_vector[2*i] = 0
                    neighbour_vector[2*i+1] = 0
                elif self.num_actions == self.length and self.path[self.num_actions - 1] == tuple(neighbour_pos):
                    neighbour_vector[2*i] = 0
                    neighbour_vector[2*i+1] = 0
                elif self.path[self.num_actions - 1] == tuple(neighbour_pos) or self.path[self.num_actions + 1] == tuple(neighbour_pos):
                    neighbour_vector[2*i] = 0
                    neighbour_vector[2*i+1] = 0
                else:   # if not in chain, assign 11
                    neighbour_vector[2*i] = 1
                    neighbour_vector[2*i+1] = 1
        
        return neighbour_vector
    

if __name__ == "__main__":
    env  = Placing(16)
    print(env.path)
    print(env.starting_pos)
    print(env.starting_dir)