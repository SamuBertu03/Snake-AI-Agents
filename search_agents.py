from collections import deque
import heapq
from heuristics import manhattan

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
    def find_path_with_exploration(self, game, on_expand=None):
        start, goal = game.snake[0], game.food
        if goal is None:
            return SearchResult([], 0, 0, 0, False)

        queue = deque([(game.snake, [], game.food)])
        visited = {tuple(game.snake)}
        nodes_expanded = 0

        while queue:
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

        return SearchResult([], nodes_expanded, 0, 0, False)

    def find_path(self, game):
        return self.find_path_with_exploration(game, on_expand=None)


class DFSAgent(_BaseAgent):
    def find_path_with_exploration(self, game, on_expand=None):
        start, goal = game.snake[0], game.food
        if goal is None:
            return SearchResult([], 0, 0, 0, False)

        stack = [(game.snake, [], game.food)]
        visited = {tuple(game.snake)}
        nodes_expanded = 0

        while stack:
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

        return SearchResult([], nodes_expanded, 0, 0, False)

    def find_path(self, game):
        return self.find_path_with_exploration(game, on_expand=None)


class GreedyAgent(_BaseAgent):
    def find_path_with_exploration(self, game, on_expand=None):
        start, goal = game.snake[0], game.food
        if goal is None:
            return SearchResult([], 0, 0, 0, False)

        open_list = [(manhattan(start, goal), game.snake, [], game.food)]
        visited = {tuple(game.snake)}
        nodes_expanded = 0

        while open_list:
            open_list.sort(key=lambda item: manhattan(item[1][0], goal))
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
                    open_list.append((manhattan(new_head, goal), new_snake, path + [new_head], new_food))

        return SearchResult([], nodes_expanded, 0, 0, False)

    def find_path(self, game):
        return self.find_path_with_exploration(game, on_expand=None)


class AStarAgent(_BaseAgent):
    def find_path_with_exploration(self, game, on_expand=None):
        start, goal = game.snake[0], game.food
        if goal is None:
            return SearchResult([], 0, 0, 0, False)

        open_list = [(manhattan(start, goal), 0, game.snake, [], game.food)]
        visited = {tuple(game.snake)}
        nodes_expanded = 0

        while open_list:
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
                    f = new_g + manhattan(new_head, goal)
                    heapq.heappush(open_list, (f, new_g, new_snake, path + [new_head], new_food))

        return SearchResult([], nodes_expanded, 0, 0, False)

    def find_path(self, game):
        return self.find_path_with_exploration(game, on_expand=None)

