# renderer.py
import pygame
from game import CELL_SIZE, GRID_W, GRID_H

WINDOW_W = CELL_SIZE * GRID_W
WINDOW_H = CELL_SIZE * GRID_H
BG = (30, 30, 30)
GRID_COLOR = (50, 50, 50)
SNAKE_HEAD = (0, 255, 0)
SNAKE_BODY = (0, 180, 0)
FOOD_COLOR = (200, 0, 0)
TEXT_COLOR = (255, 255, 255)
FPS = 10

class SnakeRenderer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.SysFont("Arial", 24, bold=True)

    def draw(self, game):
        self.screen.fill(BG)
        for x in range(0, WINDOW_W, CELL_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, WINDOW_H))
        for y in range(0, WINDOW_H, CELL_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (WINDOW_W, y))
        for i, (x, y) in enumerate(game.snake):
            color = SNAKE_HEAD if i == len(game.snake) - 1 else SNAKE_BODY
            pygame.draw.rect(self.screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, FOOD_COLOR, (game.food[0] * CELL_SIZE, game.food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        score_text = self.font_small.render(f"Score: {game.get_state()['score']}", True, TEXT_COLOR)
        self.screen.blit(score_text, (5, 5))
        pygame.display.flip()
        self.clock.tick(FPS)