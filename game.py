import random

class SnakeGame:
    def __init__(self, grid_size=10, seed=42):
        self.grid_size = grid_size
        self.reset(seed)

    # inizializzazione dell'envinroment
    def reset(self, seed=42):
        random.seed(seed)
        self.snake = [(self.grid_size // 2, self.grid_size // 2)]
        self.direction = (0, 1)  # in che verso inizia a guardare, default: verso destra
        self.food = self._spawn_food()
        self.score = 0
        self.game_over = False
        self.moves = 0
        self.seed = seed

    # funzione per far spawnare il cibo 
    def _spawn_food(self):
        empty_cells = [(x, y) for x in range(self.grid_size)
                       for y in range(self.grid_size)
                       if (x, y) not in self.snake]
        if not empty_cells:
            return None
        return random.choice(empty_cells)

    # funzione per effettuare un passo nel gioco
    def step(self, action):
        """action: (dx, dy)"""
        if self.game_over:
            return

        head_x, head_y = self.snake[0]
        dx, dy = action

        # aggiorno la testa del serpente a seconda della direzione da intraprendere
        new_head = (head_x + dx, head_y + dy)

        # controlla collisioni (con la griglia e contro se stesso)
        if (new_head in self.snake) or not (0 <= new_head[0] < self.grid_size) or not (0 <= new_head[1] < self.grid_size):
            self.game_over = True
            return

        # muove il serpente
        self.snake.insert(0, new_head)

        # controlla se ha mangiato
        if new_head == self.food:
            self.score += 1
            self.food = self._spawn_food()
        else:
            # rimuovo la coda del serpente, dunque il penultimo elemento del corpo diventa la nuova coda
            # le posizioni intermedie del corpo non vengono modificate, si aggiunge un nuovo elemento in testa e si rimuove in coda (FIFO)
            self.snake.pop()
        
        # numero di azioni intraprese dal serpente  
        self.moves += 1

    # restituisce lo stato corrente 
    def get_state(self):
        return {
            "snake": list(self.snake),
            "direction": self.direction,
            "food": self.food,
            "game_over": self.game_over,
            "score": self.score,
            "grid_size": self.grid_size,
        }

    def clone(self):
        """Ritorna una copia dello stato attuale (per la ricerca)."""
        clone = SnakeGame(self.grid_size)
        clone.snake = list(self.snake)
        clone.direction = self.direction
        clone.food = self.food
        clone.score = self.score
        clone.game_over = self.game_over
        clone.moves = self.moves
        return clone
