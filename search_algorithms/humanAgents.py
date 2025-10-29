# agents.py
import pygame
from game import ACTIONS

class HumanAgent:
    def act(self, state):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]: return ACTIONS["UP"]
        if keys[pygame.K_DOWN]: return ACTIONS["DOWN"]
        if keys[pygame.K_LEFT]: return ACTIONS["LEFT"]
        if keys[pygame.K_RIGHT]: return ACTIONS["RIGHT"]
        return None
