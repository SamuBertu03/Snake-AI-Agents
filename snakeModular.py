import pygame, sys, random

CELL_SIZE = 20
GRID_W = 20
GRID_H = 20
WINDOW_W = CELL_SIZE * GRID_W
WINDOW_H = CELL_SIZE * GRID_H
FPS = 10

# colori
BG = (30, 30, 30)
GRID_COLOR = (50, 50, 50)
SNAKE_HEAD = (0, 255, 0)
SNAKE_BODY = (0, 180, 0)
FOOD_COLOR = (200, 0, 0)
TEXT_COLOR = (255, 255, 255)

# azioni possibili
ACTIONS = {
    "UP": (0,-1),
    "DOWN": (0,1),
    "LEFT": (-1,0),
    "RIGHT": (1,0)
}
OPPOSITE = { (1,0):(-1,0), (-1,0):(1,0), (0,1):(0,-1), (0,-1):(0,1) }

# ------------------ GAME LOGIC ------------------
class SnakeGame:
    def __init__(self, width=GRID_W, height=GRID_H):
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        self.snake = [(5,5),(6,5),(7,5)]
        self.direction = (1,0)  # right
        self.food = self._spawn_food()
        self.game_over = False
        return self.get_state()

    def _spawn_food(self):
        all_cells = {(x,y) for x in range(self.width) for y in range(self.height)}
        free = list(all_cells - set(self.snake))
        if not free: return None
        return random.choice(free)

    def step(self, action):
        if self.game_over:
            return self.get_state(), 0, True

        if action and action != OPPOSITE[self.direction]:
            self.direction = action                         # si evita l'inversione di direzione 

        # si calcola la nuova posizione della testa
        head = self.snake[-1]
        dx,dy = self.direction
        new_head = (head[0]+dx, head[1]+dy)

        tail = self.snake[0]
        # collisioni
        if not (0 <= new_head[0] < self.width and 0 <= new_head[1] < self.height):
            self.game_over = True
        elif new_head in self.snake and new_head != tail:
            self.game_over = True

        if self.game_over:
            return self.get_state(), -1, True

        
        self.snake.append(new_head)
        reward = 0
        if new_head == self.food:
            reward = 1
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
            "score": len(self.snake)-3
        }

    def is_game_over(self):
        return self.game_over

# ------------------ RENDERER ------------------
class SnakeRenderer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.SysFont("Arial", 24, bold=True)
        self.font_big = pygame.font.SysFont("Arial", 48, bold=True)

    def draw(self, game: SnakeGame):
        self.screen.fill(BG)
        # griglia
        for x in range(0, WINDOW_W, CELL_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x,0), (x,WINDOW_H))
        for y in range(0, WINDOW_H, CELL_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0,y), (WINDOW_W,y))
        # snake
        for i,(x,y) in enumerate(game.snake):
            color = SNAKE_HEAD if i==len(game.snake)-1 else SNAKE_BODY
            pygame.draw.rect(self.screen, color, (x*CELL_SIZE,y*CELL_SIZE,CELL_SIZE,CELL_SIZE))
            pygame.draw.rect(self.screen, BG, (x*CELL_SIZE,y*CELL_SIZE,CELL_SIZE,CELL_SIZE), 1)
        # food
        if game.food:
            pygame.draw.rect(self.screen, FOOD_COLOR, (game.food[0]*CELL_SIZE,game.food[1]*CELL_SIZE,CELL_SIZE,CELL_SIZE))
        # score
        txt = self.font_small.render(f"Score: {game.get_state()['score']}", True, TEXT_COLOR)
        self.screen.blit(txt,(5,5))

        pygame.display.flip()
        self.clock.tick(FPS)

    def game_over_menu(self, score):
        self.screen.fill(BG)
        msg = self.font_big.render("Game Over!", True, TEXT_COLOR)
        msg_rect = msg.get_rect(center=(WINDOW_W//2, WINDOW_H//3))
        self.screen.blit(msg, msg_rect)

        score_text = self.font_small.render(f"Score: {score}", True, TEXT_COLOR)
        score_rect = score_text.get_rect(center=(WINDOW_W//2, WINDOW_H//2))
        self.screen.blit(score_text, score_rect)

        opt_text = self.font_small.render("Press R to Restart or Q to Quit", True, TEXT_COLOR)
        opt_rect = opt_text.get_rect(center=(WINDOW_W//2, WINDOW_H//2 + 40))
        self.screen.blit(opt_text, opt_rect)

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return "restart"
                    elif event.key == pygame.K_q:
                        pygame.quit(); sys.exit()

# ------------------ AGENT BASE ------------------
class HumanAgent:
    def act(self, state):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]: return ACTIONS["UP"]
        if keys[pygame.K_DOWN]: return ACTIONS["DOWN"]
        if keys[pygame.K_LEFT]: return ACTIONS["LEFT"]
        if keys[pygame.K_RIGHT]: return ACTIONS["RIGHT"]
        return None

class RandomAgent:
    def act(self, state):
        return random.choice(list(ACTIONS.values()))
    


# ------------------ MAIN LOOP ------------------
def main():
    game = SnakeGame()
    renderer = SnakeRenderer()
    agent = HumanAgent()   # sostituibile con RandomAgent()

    while True:  
        state = game.reset()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

            action = agent.act(state)
            state, reward, done = game.step(action)
            renderer.draw(game)

        
        choice = renderer.game_over_menu(state["score"])
        if choice == "restart":
            continue

if __name__=="__main__":
    main()
