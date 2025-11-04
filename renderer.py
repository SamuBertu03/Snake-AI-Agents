import pygame
import time

CELL_SIZE = 30
MARGIN = 2               # spazio vuoto tra un quadrato e l’altro, per creare una griglia visivamente più pulita
FPS = 1                  # esecuzione lenta per vedere bene
THINK_DOT_RADIUS = 3     # raggio dei pallini rossi 

class Renderer:
    def __init__(self, grid_size, think_delay_s=0.08):
        pygame.init()
        self.grid_size = grid_size
        size = grid_size * (CELL_SIZE + MARGIN)
        self.screen = pygame.display.set_mode((size, size + 48))
        pygame.display.set_caption("Snake AI")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 22)
        self.think_delay_s = think_delay_s

    def _cell_rect(self, x, y):
        return pygame.Rect(
            y * (CELL_SIZE + MARGIN),
            x * (CELL_SIZE + MARGIN),
            CELL_SIZE,
            CELL_SIZE,
        )

    def draw(self, game, path=None, visited=None, overlay_info=None):
        self.screen.fill((30, 30, 30))

        # griglia
        for x in range(game.grid_size):
            for y in range(game.grid_size):
                pygame.draw.rect(self.screen, (50, 50, 50), self._cell_rect(x, y))

        # visited (puntini rossi tenui)
        if visited:
            for (vx, vy) in visited:
                cx = vy * (CELL_SIZE + MARGIN) + CELL_SIZE // 2
                cy = vx * (CELL_SIZE + MARGIN) + CELL_SIZE // 2
                pygame.draw.circle(self.screen, (180, 60, 60), (cx, cy), THINK_DOT_RADIUS)

        # serpente: testa di colore diverso
        for i, (x, y) in enumerate(game.snake):
            if i == 0:
                color = (144, 238, 144)  # LightGreen (testa)
            else:
                color = (0, 180, 0)      # corpo verde scuro
            pygame.draw.rect(self.screen, color, self._cell_rect(x, y))

        # cibo
        if game.food:
            fx, fy = game.food
            pygame.draw.rect(self.screen, (200, 0, 0), self._cell_rect(fx, fy))

        # path (linee e frecce rosse per il pensiero della ricerca)
        if path and len(path) >= 2:
            for i in range(len(path) - 1):
                x1, y1 = path[i]
                x2, y2 = path[i + 1]
                start_pos = (
                    y1 * (CELL_SIZE + MARGIN) + CELL_SIZE // 2,
                    x1 * (CELL_SIZE + MARGIN) + CELL_SIZE // 2,
                )
                end_pos = (
                    y2 * (CELL_SIZE + MARGIN) + CELL_SIZE // 2,
                    x2 * (CELL_SIZE + MARGIN) + CELL_SIZE // 2,
                )
                pygame.draw.line(self.screen, (255, 0, 0), start_pos, end_pos, 3)
                pygame.draw.circle(self.screen, (255, 120, 120), end_pos, 4)

        # overlay info riga inferiore
        footer = f"Score: {game.score}"
        if overlay_info:
            footer += "  |  " + overlay_info
        text = self.font.render(footer, True, (255, 255, 255))
        self.screen.blit(text, (10, self.grid_size * (CELL_SIZE + MARGIN)))

        pygame.display.flip()

    # funzione per il disegno delle linee rosse di pensiero
    def show_thought_step(self, game, path, visited, nodes_expanded, frontier_size):
        """Mostra un singolo passo di pianificazione (path parziale + visited)."""
        overlay = f"Thinking… expanded: {nodes_expanded}  frontier: {frontier_size}"
        self.draw(game, path=path, visited=visited, overlay_info=overlay)
        pygame.event.pump()   # mantiene la finestra reattiva
        time.sleep(self.think_delay_s)

    # frame per second, regolano la velocità del serpente una volta calcolato la soluzione
    def tick_execution(self):
        """Frame rate lento durante l'esecuzione del piano."""
        self.clock.tick(FPS)
