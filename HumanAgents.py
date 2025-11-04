import pygame

class HumanAgent:
    def get_action(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            return (-1, 0)
        elif keys[pygame.K_DOWN]:
            return (1, 0)
        elif keys[pygame.K_LEFT]:
            return (0, -1)
        elif keys[pygame.K_RIGHT]:
            return (0, 1)
        return None
