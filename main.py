import argparse
from game import SnakeGame
from renderer import Renderer
from human_agent import HumanAgent
from search_agents import BFSAgent, DFSAgent, GreedyAgent, AStarAgent
from search_agents_relaxed import Relaxed_BFSAgent, Relaxed_DFSAgent, Relaxed_AStarAgent, Relaxed_GreedyAgent
from heuristics import manhattan, euclidean_distance, diagonal_distance
import pygame
import time

AGENTS = {
    "human": HumanAgent,
    "bfs": BFSAgent,
    "dfs": DFSAgent,
    "greedy": GreedyAgent,
    "astar": AStarAgent,
    "relaxed_bfs": Relaxed_BFSAgent,
    "relaxed_dfs": Relaxed_DFSAgent,
    "relaxed_astar": Relaxed_AStarAgent,
    "relaxed_greedy": Relaxed_GreedyAgent,
}

HEURISTICS = {
    "manhattan": manhattan,
    "euclidean": euclidean_distance,
    "diagonal": diagonal_distance,
}


def run_game(agent_name="bfs", heuristic_name="manhattan", n=101, grid_size=10,
             seed=42, fps=1, think_speed=0.001, max_expansions=1000000,
             windowed=True):

    game = SnakeGame(grid_size, seed)
    agent = AGENTS[agent_name]()
    renderer = Renderer(grid_size, agent_name=agent_name, fps=fps,
                        think_delay_s=think_speed, windowed=windowed) 
    human = HumanAgent() if agent_name == "human" else None

    stage = 1

    while not game.game_over and game.score < n:

        # --- Input umano ---
        if agent_name == "human":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            action = human.get_action()
            if action:
                game.step(action)
                renderer.draw(game)
                renderer.tick_execution()
            continue

        # --- Callback per la visualizzazione della ricerca ---
        def on_expand(path, visited, nodes_expanded, frontier_size):
            renderer.show_thought_step(
                game, path, visited, nodes_expanded, frontier_size
            )

        # --- Se l’agente usa una euristica ---
        if agent_name in ["relaxed_astar", "relaxed_greedy", "greedy", "astar"]:
            heuristic = HEURISTICS[heuristic_name]
            result = agent.find_path_with_exploration(
                game,
                on_expand=on_expand,
                heuristic=heuristic,
                max_expansions=max_expansions
            )
        else:
            result = agent.find_path_with_exploration(
                game,
                on_expand=on_expand,
                max_expansions=max_expansions
            )

        if not result.found:
            print(f" Nessun percorso trovato (sottoproblema {stage})")
            break

        renderer.draw(
            game,
            path=result.path,
            visited=None,
            overlay_info=f"Plan found — cost {result.cost} | expanded {result.nodes_expanded}"
        )
        pygame.event.pump()
        time.sleep(0.5)

        # --- Esecuzione del piano ---
        for next_pos in result.path:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            if game.game_over:
                break
            head = game.snake[0]
            action = (next_pos[0] - head[0], next_pos[1] - head[1])
            game.step(action)
            renderer.draw(game)
            renderer.tick_execution()

        print(f" Mela {stage} mangiata! (expanded: {result.nodes_expanded}, cost: {result.cost})")
        stage += 1

    print(f"Gioco terminato. Score: {game.score}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", type=str, default="bfs", choices=AGENTS.keys())
    parser.add_argument("--heuristic", type=str, default="manhattan",
                        choices=["manhattan", "euclidean", "diagonal"])
    parser.add_argument("--n", type=int, default=50)
    parser.add_argument("--grid", type=int, default=10)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--fps", type=int, default=10)
    parser.add_argument("--think-speed", type=float, default=0.08)
    parser.add_argument("--max_expansions", type=int, default=1000000)

    # --- Flag per finestra o borderless fullscreen ---
    parser.add_argument("--windowed", action="store_true",
                        help="Apri la finestra normale invece che borderless fullscreen")

    args = parser.parse_args()

    run_game(
        agent_name=args.agent,
        heuristic_name=args.heuristic,
        n=args.n,
        grid_size=args.grid,
        seed=args.seed,
        fps=args.fps,
        think_speed=args.think_speed,
        max_expansions=args.max_expansions,
        windowed=args.windowed
    )
