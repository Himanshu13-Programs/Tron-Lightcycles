"""
Presentation module for Tron Lightcycles (PRD section 3.1).

Owns the Pygame window, samples human keypresses, drives the master
loop, and paints the board from GameEngine's grid state. Contains no
game-rule or AI logic -- see game_engine.py and ai_brain.py.
"""

import sys
import pygame

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, FPS, MOVE_INTERVAL_MS,
    COLOR_BG, COLOR_GRID_LINE, COLOR_PLAYER, COLOR_PLAYER_TRAIL,
    COLOR_AI, COLOR_AI_TRAIL, COLOR_TEXT,
    PLAYER_TRAIL, AI_TRAIL,
    PLAYER_SPAWN, PLAYER_SPAWN_DIR, AI_SPAWN, AI_SPAWN_DIR,
    UP, DOWN, LEFT, RIGHT,
)
from game_engine import GameEngine
import ai_brain

KEY_TO_DIRECTION = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT,
    pygame.K_w: UP,
    pygame.K_s: DOWN,
    pygame.K_a: LEFT,
    pygame.K_d: RIGHT,
}


def draw_grid_lines(surface):
    for gx in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, COLOR_GRID_LINE, (gx, 0), (gx, SCREEN_HEIGHT))
    for gy in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, COLOR_GRID_LINE, (0, gy), (SCREEN_WIDTH, gy))


def draw_trails(surface, grid):
    for row_idx, row in enumerate(grid):
        for col_idx, value in enumerate(row):
            if value == EMPTY_PLACEHOLDER:
                continue
            color = COLOR_PLAYER_TRAIL if value == PLAYER_TRAIL else COLOR_AI_TRAIL
            rect = pygame.Rect(col_idx * CELL_SIZE, row_idx * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, color, rect)


def draw_cycle_head(surface, cycle, color):
    if not cycle.alive:
        return
    rect = pygame.Rect(cycle.x * CELL_SIZE, cycle.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, color, rect)


def draw_game_over(surface, font, winner):
    text_map = {
        "player": "YOU WIN",
        "ai": "AI WINS",
        "draw": "DRAW",
    }
    label = text_map.get(winner, "GAME OVER")
    text_surf = font.render(f"{label} - press R to restart", True, COLOR_TEXT)
    rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    surface.blit(text_surf, rect)


def new_engine():
    return GameEngine(PLAYER_SPAWN, PLAYER_SPAWN_DIR, AI_SPAWN, AI_SPAWN_DIR)


EMPTY_PLACEHOLDER = 0


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tron Lightcycles")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 24)

    engine = new_engine()
    time_since_last_step = 0

    running = True
    while running:
        dt = clock.tick(FPS)
        time_since_last_step += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in KEY_TO_DIRECTION:
                    engine.player.queue_turn(KEY_TO_DIRECTION[event.key])
                elif event.key == pygame.K_r and engine.game_over:
                    engine = new_engine()
                    time_since_last_step = 0
                elif event.key == pygame.K_ESCAPE:
                    running = False

        if not engine.game_over and time_since_last_step >= MOVE_INTERVAL_MS:
            time_since_last_step = 0

            # AI decision: hand it a snapshot, never the live grid (PRD 3.3)
            grid_snapshot = engine.snapshot_grid()
            new_dir = ai_brain.choose_direction(
                grid_snapshot, engine.ai.x, engine.ai.y, engine.ai.direction
            )
            engine.ai.queue_turn(new_dir)

            engine.step()

        # --- Render ---
        screen.fill(COLOR_BG)
        draw_grid_lines(screen)
        draw_trails(screen, engine.grid)
        draw_cycle_head(screen, engine.player, COLOR_PLAYER)
        draw_cycle_head(screen, engine.ai, COLOR_AI)

        if engine.game_over:
            draw_game_over(screen, font, engine.winner)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
