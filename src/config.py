"""
Central configuration constants for Tron Lightcycles.
Single source of truth for grid dimensions, display size, colors, and timing.
"""

# --- Grid & Display ---
GRID_WIDTH = 80          # columns (C)
GRID_HEIGHT = 60         # rows (R)
CELL_SIZE = 10           # pixels per grid cell
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE    # 800
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE  # 600

# --- Timing ---
FPS = 60
MOVE_INTERVAL_MS = 50    # how often (ms) the grid actually advances one step
                          # (decouples 60fps rendering from grid-step logic)

# --- Directions (dx, dy) ---
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

OPPOSITE = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT,
}

ALL_DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

# --- Grid cell states ---
EMPTY = 0
PLAYER_TRAIL = 1
AI_TRAIL = 2

# --- Colors (RGB) ---
COLOR_BG = (10, 10, 20)
COLOR_GRID_LINE = (25, 25, 40)
COLOR_PLAYER = (0, 200, 255)
COLOR_PLAYER_TRAIL = (0, 90, 120)
COLOR_AI = (255, 80, 40)
COLOR_AI_TRAIL = (120, 30, 15)
COLOR_TEXT = (230, 230, 230)

# --- Spawn positions ---
PLAYER_SPAWN = (10, GRID_HEIGHT // 2)
AI_SPAWN = (GRID_WIDTH - 11, GRID_HEIGHT // 2)
PLAYER_SPAWN_DIR = RIGHT
AI_SPAWN_DIR = LEFT
