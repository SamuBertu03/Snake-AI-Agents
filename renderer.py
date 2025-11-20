import pygame
import time

CELL_SIZE = 30
MARGIN = 2
THINK_DOT_RADIUS = 3


class Renderer:
    def __init__(self, grid_size, agent_name, fps,
                 think_delay_s=0.08, windowed=False):

        pygame.init()
        self.grid_size = grid_size
        self.agent_name = agent_name
        self.fps = fps
        self.think_delay_s = think_delay_s
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 22)

        self.windowed = windowed

        if windowed:
            # ------------------------------------------------------------
            # MODE 1 — WINDOWED: usa la versione semplice classica
            # ------------------------------------------------------------
            size = grid_size * (CELL_SIZE + MARGIN)
            window_width = size
            window_height = size + 48

            self.screen = pygame.display.set_mode(
                (window_width, window_height),
                pygame.RESIZABLE
            )

            self.scaled_cell = CELL_SIZE
            self.scaled_margin = MARGIN
            self.offset_x = 0
            self.offset_y = 0  # niente centratura

        else:
            # ------------------------------------------------------------
            # MODE 2 — BORDERLESS FULLSCREEN: versione moderna centrata
            # ------------------------------------------------------------
            info = pygame.display.Info()
            screen_w, screen_h = info.current_w, info.current_h

            self.screen = pygame.display.set_mode(
                (screen_w, screen_h),
                pygame.NOFRAME
            )

            # spazio disponibile (testo sopra + testo sotto)
            header_footer = 60
            available_h = screen_h - header_footer
            available_w = screen_w

            # pixel/cella
            spacing_x = available_w / grid_size
            spacing_y = available_h / grid_size
            spacing = int(min(spacing_x, spacing_y))

            self.scaled_margin = max(1, spacing // 20)
            self.scaled_cell = spacing - self.scaled_margin

            if self.scaled_cell < 1:
                self.scaled_cell = 1

            grid_pix = grid_size * spacing

            # centratura
            self.offset_x = (screen_w - grid_pix) // 2
            self.offset_y = (screen_h - grid_pix) // 2

        pygame.display.set_caption("Snake AI")

    # ESC quit
    def handle_escape(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True
        return False

    # Rect cella con offset (solo fullscreen)
    def _cell_rect(self, x, y):
        return pygame.Rect(
            self.offset_x + y * (self.scaled_cell + self.scaled_margin),
            self.offset_y + x * (self.scaled_cell + self.scaled_margin),
            self.scaled_cell,
            self.scaled_cell,
        )

    def draw(self, game, path=None, visited=None, overlay_info=None):
        if self.handle_escape():
            pygame.quit()
            exit()

        self.screen.fill((30, 30, 30))
        screen_w = self.screen.get_width()

        # ---------------- GRID ----------------
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                pygame.draw.rect(
                    self.screen,
                    (50, 50, 50),
                    self._cell_rect(x, y)
                )

        # ---------------- VISITED (puntini rossi) ----------------
        if visited:
            for (vx, vy) in visited:
                cx = self.offset_x + vy * (self.scaled_cell + self.scaled_margin) + self.scaled_cell // 2
                cy = self.offset_y + vx * (self.scaled_cell + self.scaled_margin) + self.scaled_cell // 2
                pygame.draw.circle(self.screen, (180, 60, 60), (cx, cy), THINK_DOT_RADIUS)

        # ---------------- SNAKE ----------------
        for i, (x, y) in enumerate(game.snake):
            color = (144, 238, 144) if i == 0 else (0, 180, 0)
            pygame.draw.rect(self.screen, color, self._cell_rect(x, y))

        # ---------------- FOOD ----------------
        if game.food:
            fx, fy = game.food
            pygame.draw.rect(self.screen, (200, 0, 0), self._cell_rect(fx, fy))

        # ---------------- PATH ----------------
        if path and len(path) >= 2:
            for i in range(len(path) - 1):
                x1, y1 = path[i]
                x2, y2 = path[i + 1]

                start_pos = (
                    self.offset_x + y1 * (self.scaled_cell + self.scaled_margin) + self.scaled_cell // 2,
                    self.offset_y + x1 * (self.scaled_cell + self.scaled_margin) + self.scaled_cell // 2,
                )
                end_pos = (
                    self.offset_x + y2 * (self.scaled_cell + self.scaled_margin) + self.scaled_cell // 2,
                    self.offset_y + x2 * (self.scaled_cell + self.scaled_margin) + self.scaled_cell // 2,
                )

                pygame.draw.line(self.screen, (255, 0, 0), start_pos, end_pos, 3)
                pygame.draw.circle(self.screen, (255, 120, 120), end_pos, 4)

        # ---------------- HEADER ----------------
        header = f"Search Algorithm: {self.agent_name}"
        header_text = self.font.render(header, True, (255, 255, 255))
        header_x = (screen_w - header_text.get_width()) // 2

        if self.windowed:
            # modalità semplice → testo in alto a sinistra
            self.screen.blit(header_text, (10, 10))
        else:
            # fullscreen → centrato
            self.screen.blit(header_text, (header_x, self.offset_y - 20))

        # ---------------- FOOTER ----------------
        footer = f"Score: {game.score}"
        if overlay_info:
            footer += "  |  " + overlay_info

        footer_text = self.font.render(footer, True, (255, 255, 255))
        footer_x = (screen_w - footer_text.get_width()) // 2

        if self.windowed:
            # modalità semplice
            self.screen.blit(
                footer_text,
                (10, self.grid_size * (CELL_SIZE + MARGIN))
            )
        else:
            # fullscreen centrato
            bottom_y = self.offset_y + self.grid_size * (self.scaled_cell + self.scaled_margin) - 25
            self.screen.blit(footer_text, (footer_x, bottom_y))

        pygame.display.flip()

    # ---------------- THINKING STEP ----------------
    def show_thought_step(self, game, path, visited, nodes_expanded, frontier_size):
        if self.handle_escape():
            pygame.quit()
            exit()

        overlay = f"Thinking… expanded: {nodes_expanded}  frontier: {frontier_size}"
        self.draw(game, path=path, visited=visited, overlay_info=overlay)
        pygame.event.pump()
        time.sleep(self.think_delay_s)

    # ---------------- EXECUTION TICK ----------------
    def tick_execution(self):
        if self.handle_escape():
            pygame.quit()
            exit()

        self.clock.tick(self.fps)
