# Modular Snake Game - Multiple Files Structure

# game.py
import random
from collections import deque

CELL_SIZE = 20
GRID_W = 20
GRID_H = 20

ACTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}
OPPOSITE = {(1, 0): (-1, 0), (-1, 0): (1, 0), (0, 1): (0, -1), (0, -1): (0, 1)}

class SnakeGame:
    def __init__(self, width=GRID_W, height=GRID_H):
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        self.snake = [(5, 5), (6, 5), (7, 5)]
        self.direction = ACTIONS["RIGHT"]
        self.food = self._spawn_food()
        self.game_over = False
        return self.get_state()

    def _spawn_food(self):
        all_cells = {(x, y) for x in range(self.width) for y in range(self.height)}
        free = list(all_cells - set(self.snake))
        return random.choice(free)

    def step(self, action):
        if self.game_over:
            return self.get_state(), 0, True
        if action and action != OPPOSITE[self.direction]:
            self.direction = action
        head = self.snake[-1]
        dx, dy = self.direction
        new_head = (head[0] + dx, head[1] + dy)
        tail = self.snake[0]
        if not (0 <= new_head[0] < self.width and 0 <= new_head[1] < self.height) or \
           (new_head in self.snake and new_head != tail):
            self.game_over = True
            return self.get_state(), -1, True
        self.snake.append(new_head)
        reward = 1 if new_head == self.food else 0
        if reward:
            self.food = self._spawn_food()
        else:
            self.snake.pop(0)
        return self.get_state(), reward, False

    def get_state(self):
        return {
            "snake": self.snake.copy(),
            "direction": self.direction,
            "food": self.food,
            "game_over": self.game_over,
            "score": len(self.snake) - 3
        }




