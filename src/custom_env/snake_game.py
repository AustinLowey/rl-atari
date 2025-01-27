import random
import sys
import time

import pygame
from pygame.surfarray import array3d


BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)


class SnakeEnv():
    
    def __init__(self, frame_size_x=600, frame_size_y=600):
        """Defines the initial game window size"""

        self.frame_size_x = frame_size_x
        self.frame_size_y = frame_size_y
        self.game_window = pygame.display.set_mode((frame_size_x, frame_size_y))
        self.reset()
    

    def reset(self, starting_direction=2):
        """Resets the game, along with the default snake size and spawning food."""

        self.game_window.fill(BLACK)
        self.snake_pos = [200, 300]
        node_size = 10
        self.snake_body = [[200, 300], [200 - node_size, 300], [200 - (2 * node_size), 300]]
        self.food_pos = self.spawn_food()
        self.food_spawn = True

        self.direction = starting_direction # 0, 1, 2, 3 = left, down, right, up
        self.action = self.direction
        self.score = 0
        self.steps = 0
        print('Game Reset.')
    

    def change_direction(self, action, direction):
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
    

    def move(self, direction, snake_pos):
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


    def human_step(self, event):
        """Returns an environment action based on human keyboard event."""
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                return 0           
            elif event.key == pygame.K_DOWN:
                return 1
            elif event.key == pygame.K_RIGHT:
                return 2
            elif event.key == pygame.K_UP:
                return 3
            
            # Escape key quits game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                
        return None
    

    def display_score(self, color, font, size):
        """Updates the shown score."""
        
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render(f'Score : {self.score}', True, color)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (self.frame_size_x / 10, 15)
        self.game_window.blit(score_surface, score_rect)


    def check_game_over(self):
        """Checks game over conditions (if the snake has touched either itself or the window edge)."""
        
        # If snake touches game/window edge
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.frame_size_x - 10:
            self.end_game()
        elif self.snake_pos[1] < 0 or self.snake_pos[1] > self.frame_size_y - 10:
            self.end_game()

        # If snake touches its own body
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                self.end_game()


    def end_game(self):
        """Ends the game."""

        # Game over screen display
        message = pygame.font.SysFont('arial', 45)
        message_surface = message.render('Game Over.', True, RED)
        message_rect = message_surface.get_rect()
        message_rect.midtop = (self.frame_size_x / 2, self.frame_size_y / 4)
        self.game_window.fill(BLACK)
        self.game_window.blit(message_surface, message_rect)
        self.display_score(RED, 'times', 20)
        pygame.display.flip()

        # Quit game
        time.sleep(3)
        pygame.quit()
        sys.exit()


    def play_game(self, refresh_rate=10):
        """
        Main logic loop for playing the Atari Snake game. Higher makes snake "move faster" and
        thus harder for human to play.
        """

        # Create FPS controller, check for any pygame errors, and init game window
        fps_controller = pygame.time.Clock()
        check_errors = pygame.init()
        pygame.display.set_caption('Atari Snake')

        # Game loop
        while True:
            
            # Check for and convert keyboard input
            for event in pygame.event.get():
                snake_env.action = snake_env.human_step(event)
        
            # Check for and update position and direction
            snake_env.direction = snake_env.change_direction(snake_env.action, snake_env.direction)
            snake_env.snake_pos = snake_env.move(snake_env.direction, snake_env.snake_pos)

            # Check if ate  food and spawn food if needed
            snake_env.snake_body.insert(0, list(snake_env.snake_pos))
            if snake_env.eat():
                snake_env.score += 1
                snake_env.food_spawn = False
            else:
                snake_env.snake_body.pop()

            if not snake_env.food_spawn:
                snake_env.food_pos = snake_env.spawn_food()
            snake_env.food_spawn = True

            # Game display
            snake_env.game_window.fill(BLACK)
            for pos in snake_env.snake_body:
                pygame.draw.rect(snake_env.game_window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))
            pygame.draw.rect(snake_env.game_window, WHITE, pygame.Rect(snake_env.food_pos[0], snake_env.food_pos[1], 10, 10))

            snake_env.check_game_over()
            
            # Refresh game
            snake_env.display_score(WHITE, 'consolas', 20)
            pygame.display.update()
            fps_controller.tick(refresh_rate)
            img = array3d(snake_env.game_window)


if __name__ == '__main__':
    snake_env = SnakeEnv()
    snake_env.play_game()