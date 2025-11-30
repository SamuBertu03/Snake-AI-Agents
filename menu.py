import pygame
import random
from main import run_game

pygame.init()
FONT = pygame.font.SysFont("Arial", 32)
SMALL = pygame.font.SysFont("Arial", 26)

OPTIONS = [
    "Manual",
    "Relaxed BFS",
    "Relaxed DFS",
    "Relaxed Greedy",
    "Relaxed A*",
    "BFS",
    "DFS",
    "Greedy",
    "A*"
]

MENU_TO_AGENT = {
    "Manual": "human",
    "Relaxed BFS": "relaxed_bfs",
    "Relaxed DFS": "relaxed_dfs",
    "Relaxed Greedy": "relaxed_greedy",
    "Relaxed A*": "relaxed_astar",
    "BFS": "bfs",
    "DFS": "dfs",
    "Greedy": "greedy",
    "A*": "astar",
}

HEURISTICS = ["manhattan", "euclidean", "diagonal"]


def draw_main_menu(screen, agent_selected, fullscreen_enabled):
    screen.fill((30, 30, 30))

    title = FONT.render("SnAIke Launcher", True, (255, 255, 255))
    screen.blit(title, (40, 20))

    y = 90
    subtitle = SMALL.render("Select Agent:", True, (255, 255, 255))
    screen.blit(subtitle, (40, y))
    y += 40

    # Draw agent list
    for i, opt in enumerate(OPTIONS):
        color = (255, 255, 0) if i == agent_selected else (200, 200, 200)
        surf = SMALL.render(opt, True, color)
        screen.blit(surf, (60, y))
        y += 40

    y += 20

    # Checkbox for fullscreen
    checkbox = "[X]" if fullscreen_enabled else "[ ]"
    fs_text = SMALL.render(f"Fullscreen: {checkbox}", True, (200, 200, 200))
    screen.blit(fs_text, (40, y))

    y += 60
    info = SMALL.render("Press ENTER to apply fullscreen", True, (180, 180, 180))
    screen.blit(info, (40, y))

    pygame.display.flip()


def main_menu():
    screen = pygame.display.set_mode((700, 700))
    agent_selected = 0
    fullscreen_enabled = False

    while True:
        draw_main_menu(screen, agent_selected, fullscreen_enabled)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    agent_selected = (agent_selected - 1) % len(OPTIONS)

                elif event.key == pygame.K_DOWN:
                    agent_selected = (agent_selected + 1) % len(OPTIONS)

                elif event.key in (pygame.K_SPACE, pygame.K_LEFT, pygame.K_RIGHT):
                    fullscreen_enabled = not fullscreen_enabled

                elif event.key == pygame.K_RETURN:
                    agent_label = OPTIONS[agent_selected]
                    agent_key = MENU_TO_AGENT[agent_label]

                    needs_heuristic = agent_key in [
                        "relaxed_greedy", "relaxed_astar",
                        "greedy", "astar"
                    ]

                    heuristic = "manhattan"
                    if needs_heuristic:
                        heuristic = choose_option("Select Heuristic", HEURISTICS)

                    launch_game(agent_key, heuristic, fullscreen_enabled)
                    return


def draw_menu(screen, title, options, selected):
    screen.fill((30, 30, 30))
    title_surf = FONT.render(title, True, (255, 255, 255))
    screen.blit(title_surf, (40, 20))

    y = 100
    for i, opt in enumerate(options):
        color = (255, 255, 0) if i == selected else (200, 200, 200)
        surf = SMALL.render(opt, True, color)
        screen.blit(surf, (60, y))
        y += 50

    pygame.display.flip()


def choose_option(title, options):
    screen = pygame.display.set_mode((600, 600))
    selected = 0

    while True:
        draw_menu(screen, title, options, selected)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected]


def launch_game(agent_key, heuristic, fullscreen):
    windowed = not fullscreen  # fullscreen ON → windowed=False

    print(f"Launching game → agent={agent_key}, heuristic={heuristic}, fullscreen={fullscreen}")

    # IMPORTANT: re-init pygame before launching the real game
    pygame.quit()
    pygame.init()

    run_game(
        agent_name=agent_key,
        heuristic_name=heuristic,
        seed=random.randint(0, 999999),
        n=50,
        grid_size=10,
        fps=10,
        think_speed=0.08,
        max_expansions=700000,
        windowed=windowed
    )


if __name__ == "__main__":
    main_menu()
