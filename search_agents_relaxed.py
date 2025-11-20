from collections import deque
import heapq
from math import sqrt
from heuristics import manhattan, euclidean_distance, diagonal_distance
# mosse
MOVES = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
}



# def della classe dell'oggetto che ha come attributi il risultato della ricerca
class SearchResult:
    def __init__(self, path, nodes_expanded, depth, cost, found):
        self.path = path
        self.nodes_expanded = nodes_expanded
        self.depth = depth
        self.cost = cost
        self.found = found

# Agente base: restituisce le celle adiacenti alla posizione attuale 
class _BaseAgent:
    def __init__(self,is_relaxed=True):
        self.is_relaxed=is_relaxed
    
    def _neighbors(self, game, pos):
        # Caso rilassato in cui lo stato corrente contiene solo la testa del serpente
        if(self.is_relaxed):
            for dx, dy in MOVES.values():
                nx, ny = pos[0] + dx, pos[1] + dy
                if 0 <= nx < game.grid_size and 0 <= ny < game.grid_size:
                    if (nx, ny) not in game.snake:
                        yield (nx, ny)
        else:
            #applicazione caso completo
            pass
# Agente per BFS 
class Relaxed_BFSAgent(_BaseAgent):
    
    def __init__(self, is_relaxed=True):
        super().__init__(is_relaxed)
        
    def find_path_with_exploration(self, game, on_expand=None,max_expansions=1000000):
        start, goal = game.snake[0], game.food
        if goal is None:
            return SearchResult([], 0, 0, 0, False)

        queue = deque([(start, [start])])
        visited = {start}
        nodes_expanded = 0

        while queue and max_expansions>0:
            pos, path = queue.popleft()
            nodes_expanded += 1

            # far vedere la nuova frontiera espansa durante il reasoning
            if on_expand:
                on_expand(path, set(visited), nodes_expanded, len(queue))

            if pos == goal:
                return SearchResult(path[1:], nodes_expanded, len(path), len(path) - 1, True)

            for nb in self._neighbors(game, pos):
                if nb not in visited:
                    visited.add(nb)
                    queue.append((nb, path + [nb]))
            max_expansions-=1

        return SearchResult([], nodes_expanded, 0, 0, False)

    def find_path(self, game):
        return self.find_path_with_exploration(game, on_expand=None)

# Agente per DFS 
class Relaxed_DFSAgent(_BaseAgent):
    
    def __init__(self, is_relaxed=True):
        super().__init__(is_relaxed)
        
    def find_path_with_exploration(self, game, on_expand=None,max_expansions=1000000):
        start, goal = game.snake[0], game.food
        if goal is None:
            return SearchResult([], 0, 0, 0, False)

        stack = [(start, [start])]
        visited = {start}
        nodes_expanded = 0

        while stack and max_expansions>0:
            pos, path = stack.pop()
            nodes_expanded += 1

            if on_expand:
                on_expand(path, set(visited), nodes_expanded, len(stack))

            if pos == goal:
                return SearchResult(path[1:], nodes_expanded, len(path), len(path) - 1, True)

            for nb in self._neighbors(game, pos):
                if nb not in visited:
                    visited.add(nb)
                    stack.append((nb, path + [nb]))
            max_expansions-=1

        return SearchResult([], nodes_expanded, 0, 0, False)

    def find_path(self, game):
        return self.find_path_with_exploration(game, on_expand=None)

# Agente per Greedy 
class Relaxed_GreedyAgent(_BaseAgent):
    
    def __init__(self, is_relaxed=True):
        super().__init__(is_relaxed)
        
    def find_path_with_exploration(self, game, on_expand=None,heuristic=manhattan,max_expansions=1000000):
        start, goal = game.snake[0], game.food
        if goal is None:
            return SearchResult([], 0, 0, 0, False)

        open_list = [(heuristic(start, goal), [start])]
        visited = {start}
        nodes_expanded = 0

        while open_list and max_expansions>0:
            # scegli il path con h minore
            open_list.sort(key=lambda item: heuristic(item[1][-1], goal))
            _, path = open_list.pop(0)
            pos = path[-1]
            nodes_expanded += 1

            if on_expand:
                on_expand(path, set(visited), nodes_expanded, len(open_list))

            if pos == goal:
                return SearchResult(path[1:], nodes_expanded, len(path), len(path) - 1, True)

            for nb in self._neighbors(game, pos):
                if nb not in visited:
                    visited.add(nb)
                    open_list.append((heuristic(nb, goal), path + [nb]))
            max_expansions-=1

        return SearchResult([], nodes_expanded, 0, 0, False)

    def find_path(self, game):
        return self.find_path_with_exploration(game, on_expand=None,heuristic=manhattan)

# Agente per A star 
class Relaxed_AStarAgent(_BaseAgent):
    
    def __init__(self, is_relaxed=True):
        super().__init__(is_relaxed)
        
    def find_path_with_exploration(self, game, on_expand=None,heuristic=manhattan,max_expansions=1000000):
        start, goal = game.snake[0], game.food
        if goal is None:
            return SearchResult([], 0, 0, 0, False)

        # (priority, g, path)
        open_list = [(heuristic(start, goal), 0, [start])]
        visited = {start}
        nodes_expanded = 0

        while open_list and max_expansions>0:
            priority, g, path = heapq.heappop(open_list)
            pos = path[-1]
            nodes_expanded += 1

            if on_expand:
                on_expand(path, set(visited), nodes_expanded, len(open_list))

            if pos == goal:
                return SearchResult(path[1:], nodes_expanded, len(path), g, True)

            for nb in self._neighbors(game, pos):
                if nb not in visited:
                    visited.add(nb)
                    new_g = g + 1
                    f = new_g + heuristic(nb, goal)
                    heapq.heappush(open_list, (f, new_g, path + [nb]))
            max_expansions-=1

        return SearchResult([], nodes_expanded, 0, 0, False)

    def find_path(self, game):
        return self.find_path_with_exploration(game, on_expand=None)


