# main.py
import pygame, sys
from game import SnakeGame
from renderer import SnakeRenderer
from search_algorithms.humanAgents import HumanAgent

def main():
    game = SnakeGame()
    renderer = SnakeRenderer()
    agent = HumanAgent()
    while True:
        state = game.reset()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
            action = agent.act(state)
            state, _, done = game.step(action)
            renderer.draw(game)

if __name__ == "__main__":
    main()
