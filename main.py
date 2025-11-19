import argparse
from game import SnakeGame
from renderer import Renderer
from human_agent import HumanAgent
from search_agents import BFSAgent, DFSAgent, GreedyAgent, AStarAgent
from search_agents_relaxed import Relaxed_BFSAgent, Relaxed_DFSAgent, Relaxed_AStarAgent, Relaxed_GreedyAgent
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

def run_game(agent_name="bfs", n=101, grid_size=10, seed=42, render=True, fps=1, think_speed=0.001):
    game = SnakeGame(grid_size, seed)
    agent = AGENTS[agent_name]()
    renderer = Renderer(grid_size, agent_name=agent_name, fps=fps, think_delay_s=think_speed) if render else None
    human = HumanAgent() if agent_name == "human" else None

    stage = 1

    while not game.game_over and game.score < n:
        if agent_name == "human":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            action = human.get_action()
            if action:
                game.step(action)
            if render:
                renderer.draw(game)
                renderer.tick_execution()
            continue

        def on_expand(path, visited, nodes_expanded, frontier_size):
            if render:
                renderer.show_thought_step(game, path, visited, nodes_expanded, frontier_size)

        result = agent.find_path_with_exploration(game, on_expand=on_expand)

        if not result.found:
            print(f" Nessun percorso trovato (sottoproblema {stage})")
            break

        if render:
            renderer.draw(
                game,
                path=result.path,
                visited=None,
                overlay_info=f"Plan found — cost {result.cost} | expanded {result.nodes_expanded}",
            )
            pygame.event.pump()
            time.sleep(0.5)

        for next_pos in result.path:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            if game.game_over:
                break
            head = game.snake[0]
            action = (next_pos[0] - head[0], next_pos[1] - head[1])
            game.step(action)
            if render:
                renderer.draw(game)
                renderer.tick_execution()

        print(f" Mela {stage} mangiata! (expanded: {result.nodes_expanded}, cost: {result.cost})")
        stage += 1

    print(f"Gioco terminato. Score: {game.score}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", type=str, default="bfs", choices=AGENTS.keys())
    parser.add_argument("--n", type=int, default=50)
    parser.add_argument("--grid", type=int, default=10)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--no-render", action="store_true")
    parser.add_argument("--fps", type=int, default=10)
    parser.add_argument("--think-speed", type=float, default=0.08)
    args = parser.parse_args()

    run_game(
        agent_name=args.agent,
        n=args.n,
        grid_size=args.grid,
        seed=args.seed,
        render=not args.no_render,
        fps=args.fps,
        think_speed=args.think_speed,
    )

