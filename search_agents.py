from collections import deque
import heapq
from heuristics import manhattan, diagonal_distance, euclidean_distance
from collections import deque

def is_state_safe(snake, grid_size):
    
    head = snake[0]
    tail = snake[-1]
    body_without_tail = set(snake[:-1])

    def neighbors(pos):
        for dx, dy in MOVES.values():
            nx, ny = pos[0] + dx, pos[1] + dy
            if not (0 <= nx < grid_size and 0 <= ny < grid_size):
                continue
            new_head = (nx, ny)
            if new_head in body_without_tail:
                continue
            yield new_head

    if not any(True for _ in neighbors(head)):
        return False

    q = deque([head])
    visited = {head}
    while q:
        pos = q.popleft()
        if pos == tail:
            return True
        for nb in neighbors(pos):
            if nb not in visited:
                visited.add(nb)
                q.append(nb)

    return False


MOVES = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
}


class SearchResult:
    def __init__(self, path, nodes_expanded, depth, cost, found):
        self.path = path
        self.nodes_expanded = nodes_expanded
        self.depth = depth
        self.cost = cost
        self.found = found


class _BaseAgent:
    def _next_states(self, snake, food, grid_size):
        head_x, head_y = snake[0]

        for dx, dy in MOVES.values():
            nx, ny = head_x + dx, head_y + dy

            if not (0 <= nx < grid_size and 0 <= ny < grid_size):
                continue

            new_head = (nx, ny)

            if new_head in snake:
                continue

            new_snake = [new_head] + list(snake)

            if new_head == food:
                new_food = None
            else:
                new_snake.pop()
                new_food = food

            yield new_head, new_snake, new_food


class BFSAgent(_BaseAgent):
    def find_path_with_exploration(self, game, on_expand=None,max_expansions=1000000):
        start, goal = game.snake[0], game.food
        if goal is None:
            return SearchResult([], 0, 0, 0, False)

        queue = deque([(game.snake, [], game.food)])
        visited = {tuple(game.snake)}
        nodes_expanded = 0

        while queue and max_expansions>0:
            snake, path, food = queue.popleft()
            head = snake[0]
            nodes_expanded += 1

            if on_expand:
                visited_heads = {state[0] for state in visited}
                on_expand(path, visited_heads, nodes_expanded, len(queue))

            if head == goal:
                return SearchResult(path, nodes_expanded, len(path), len(path), True)

            for new_head, new_snake, new_food in self._next_states(snake, food, game.grid_size):
                state_key = tuple(new_snake)
                if state_key not in visited:
                    visited.add(state_key)
                    queue.append((new_snake, path + [new_head], new_food))
            max_expansions-=1

        return SearchResult([], nodes_expanded, 0, 0, False)

    def find_path(self, game):
        return self.find_path_with_exploration(game, on_expand=None)


class DFSAgent(_BaseAgent):
    def find_path_with_exploration(self, game, on_expand=None,max_expansions=1000000):
        start, goal = game.snake[0], game.food
        if goal is None:
            return SearchResult([], 0, 0, 0, False)

        stack = [(game.snake, [], game.food)]
        visited = {tuple(game.snake)}
        nodes_expanded = 0

        while stack and max_expansions>0:
            snake, path, food = stack.pop()
            head = snake[0]
            nodes_expanded += 1

            if on_expand:
                visited_heads = {state[0] for state in visited}
                on_expand(path, visited_heads, nodes_expanded, len(stack))

            if head == goal:
                return SearchResult(path, nodes_expanded, len(path), len(path), True)

            for new_head, new_snake, new_food in self._next_states(snake, food, game.grid_size):
                state_key = tuple(new_snake)
                if state_key not in visited:
                    visited.add(state_key)
                    stack.append((new_snake, path + [new_head], new_food))
            max_expansions-=1

        return SearchResult([], nodes_expanded, 0, 0, False)

    def find_path(self, game):
        return self.find_path_with_exploration(game, on_expand=None)


class GreedyAgent(_BaseAgent):
    def find_path_with_exploration(self, game, on_expand=None,heuristic=manhattan,max_expansions=1000000):
        start, goal = game.snake[0], game.food
        if goal is None:
            return SearchResult([], 0, 0, 0, False)

        open_list = [(heuristic(start, goal), game.snake, [], game.food)]
        visited = {tuple(game.snake)}
        nodes_expanded = 0

        while open_list and max_expansions>0:
            open_list.sort(key=lambda item: heuristic(item[1][0], goal))
            _, snake, path, food = open_list.pop(0)
            head = snake[0]
            nodes_expanded += 1

            if on_expand:
                visited_heads = {state[0] for state in visited}
                on_expand(path, visited_heads, nodes_expanded, len(open_list))

            if head == goal:
                return SearchResult(path, nodes_expanded, len(path), len(path), True)

            for new_head, new_snake, new_food in self._next_states(snake, food, game.grid_size):
                state_key = tuple(new_snake)
                if state_key not in visited:
                    visited.add(state_key)
                    open_list.append((heuristic(new_head, goal), new_snake, path + [new_head], new_food))
            max_expansions-=1
        return SearchResult([], nodes_expanded, 0, 0, False)

    def find_path(self, game):
        return self.find_path_with_exploration(game, on_expand=None)


class AStarAgent(_BaseAgent):
    def find_path_with_exploration(self, game, on_expand=None,heuristic=manhattan,max_expansions=1000000):
        start, goal = game.snake[0], game.food
        if goal is None:
            return SearchResult([], 0, 0, 0, False)

        open_list = [(heuristic(start, goal), 0, game.snake, [], game.food)]
        visited = {tuple(game.snake)}
        nodes_expanded = 0

        while open_list and max_expansions>0:
            f, g, snake, path, food = heapq.heappop(open_list)
            head = snake[0]
            nodes_expanded += 1

            if on_expand:
                visited_heads = {state[0] for state in visited}
                on_expand(path, visited_heads, nodes_expanded, len(open_list))

            if head == goal:
                return SearchResult(path, nodes_expanded, len(path), g, True)

            for new_head, new_snake, new_food in self._next_states(snake, food, game.grid_size):
                state_key = tuple(new_snake)
                if state_key not in visited:
                    visited.add(state_key)
                    new_g = g + 1
                    f = new_g + heuristic(new_head, goal)
                    heapq.heappush(open_list, (f, new_g, new_snake, path + [new_head], new_food))
            max_expansions-=1
        return SearchResult([], nodes_expanded, 0, 0, False)

    def find_path(self, game):
        return self.find_path_with_exploration(game, on_expand=None)


class SafeAStarAgent(_BaseAgent):

    def find_path_with_exploration(self, game, on_expand=None,
                                   heuristic=manhattan, max_expansions=1000000):
        start, goal = game.snake[0], game.food
        if goal is None:
            return SearchResult([], 0, 0, 0, False)

        open_list = [(heuristic(start, goal), 0, game.snake, [], game.food)]
        visited = {tuple(game.snake)}
        nodes_expanded = 0

        while open_list and max_expansions > 0:
            f, g, snake, path, food = heapq.heappop(open_list)
            head = snake[0]
            nodes_expanded += 1

            if on_expand:
                visited_heads = {state[0] for state in visited}
                on_expand(path, visited_heads, nodes_expanded, len(open_list))

            if head == goal:
                if is_state_safe(snake, game.grid_size):
                    return SearchResult(path, nodes_expanded, len(path), g, True)
                max_expansions -= 1
                continue

            for new_head, new_snake, new_food in self._next_states(snake, food, game.grid_size):
                state_key = tuple(new_snake)
                if state_key not in visited:
                    visited.add(state_key)
                    new_g = g + 1
                    f = new_g + heuristic(new_head, goal)
                    heapq.heappush(open_list, (f, new_g, new_snake, path + [new_head], new_food))

            max_expansions -= 1

        return SearchResult([], nodes_expanded, 0, 0, False)

    def find_path(self, game):
        return self.find_path_with_exploration(game, on_expand=None)
    

