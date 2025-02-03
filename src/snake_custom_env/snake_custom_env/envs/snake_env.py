import random
import sys
import time

import gymnasium as gym
from gymnasium import error, spaces, utils
from gymnasium.utils import seeding
import numpy as np
import pygame
from pygame import display
from pygame.surfarray import array3d


BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)


class SnakeEnv(gym.Env):
    
    metadata = {'render.modes': ['human']}

    def __init__(self):
        """Defines the initial game window size"""

        self.action_space = spaces.Discrete(4)
        # self.step_limit = 10000 # Can optionally limit max length in each episode
        self.sleep = 0 # Used for rendering

        self.frame_size_x = 200
        self.frame_size_y = 200
        self.game_window = pygame.display.set_mode((self.frame_size_x, self.frame_size_y))

        self.reset()


    def step(self, action):
        """Returns an environment action based on human keyboard event."""

        # Static method calls
        self.direction = SnakeEnv.change_direction(action, self.direction)
        self.snake_pos = SnakeEnv.move(self.direction, self.snake_pos)
        
        self.snake_body.insert(0, list(self.snake_pos))

        reward = self.determine_reward() # Determine and return the reward
        self.update_game_state() # Update the env after the action
        reward, done = self.check_game_over(reward) # Determine if game over conditions met
        img = self.get_image_array_from_game() # Get observations (in this case, the game image)

        info = {'score': self.score}
        self.steps += 1
        time.sleep(self.sleep)

        return img, reward, done, info # img as the observation
    

    def reset(self, starting_direction=2):
        """Resets the game, along with the default snake size and spawning food."""

        self.game_window.fill(BLACK)
        self.snake_pos = [100, 100] # Center of self.game_window
        node_size = 10
        self.snake_body = [[100, 100], [100 - node_size, 100], [100 - (2 * node_size), 100]]
        self.food_pos = self.spawn_food()
        self.food_spawn = True

        self.direction = starting_direction # 0, 1, 2, 3 = left, down, right, up
        self.action = self.direction
        self.score = 0
        self.steps = 0
        
        # Gets and returns pygame window image to use as observation
        img = array3d(display.get_surface())
        img = np.swapaxes(img, 0, 1) # Note to self: Is swapping axes technically even necessary since feeding into CNN?

        return img # Note: .reset() NEEDS to return ONLY the observation
    
    @staticmethod
    def change_direction(action, direction):
        """
        Changes direction based on action input. Checks to make sure snake can't move directly
        opposite its current direction.
        """
        
        if action == 3 and direction != 1:
            direction = 3
        elif action == 1 and direction != 3:
            direction = 1
        elif action == 0 and direction != 2:
            direction = 0
        elif action == 2 and direction != 0:
            direction = 2
            
        return direction
    
    @staticmethod
    def move(direction, snake_pos):
        """Updates snake_pos list to reflect direction change."""
        
        if direction == 0: # Left
            snake_pos[0] -= 10
        elif direction == 1: # Down
            snake_pos[1] += 10
        elif direction == 2: # Right
            snake_pos[0] += 10
        elif direction == 3: # Up
            snake_pos[1] -= 10
            
        return snake_pos
    

    def eat(self):
        """Returns Boolean indicating if Snake has "eaten" the white food square."""

        return self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]
    

    def spawn_food(self):
        """Spawns food in a random location in the window."""

        return [random.randrange(1, (self.frame_size_x // 10)) * 10, random.randrange(1, (self.frame_size_y // 10)) * 10]


    def determine_reward(self):
        """Determine reward based on if snake ate food during current step."""

        if self.eat():
            self.score += 1
            reward = 1
            self.food_spawn = False
        else:
            self.snake_body.pop()
            reward = 0

        if not self.food_spawn:
            self.food_pos = self.spawn_food()

        self.food_spawn = True

        return reward


    def get_image_array_from_game(self):
        """Get observations, i.e. the game image."""

        img = array3d(display.get_surface())
        img = np.swapaxes(img, 0, 1)

        return img


    def update_game_state(self):
        """Update the env after the agent's action."""

        self.game_window.fill(BLACK)
        for pos in self.snake_body:
            pygame.draw.rect(self.game_window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.draw.rect(self.game_window, WHITE, pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10))
    

    def check_game_over(self):
        """Checks game over conditions (if the snake has touched either itself or the window edge)."""
        
        # If snake touches game/window edge
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.frame_size_x - 10:
            return -1, True
        elif self.snake_pos[1] < 0 or self.snake_pos[1] > self.frame_size_y - 10:
            return -1, True

        # If snake touches its own body
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                return -1, True


    def render(self, mode='human'):
        """Define display rendering capability."""

        if mode == 'human':
            display.update()

    
    def close(self):
        """Close early."""

        pass