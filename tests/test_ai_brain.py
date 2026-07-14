"""
Unit tests for ai_brain.py: Tier 1 safe-move filtering and Tier 2
flood-fill area scoring. These are pure functions (grid in, value out)
with no Pygame dependency, so they're tested in full isolation.

Run with: pytest tests/test_ai_brain.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ai_brain import flood_fill_score, get_safe_moves, choose_direction
from config import GRID_WIDTH, GRID_HEIGHT, EMPTY, UP, DOWN, LEFT, RIGHT


def empty_grid():
    return [[EMPTY for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]


def test_flood_fill_full_open_grid():
    grid = empty_grid()
    score = flood_fill_score(grid, 0, 0)
    assert score == GRID_WIDTH * GRID_HEIGHT


def test_flood_fill_walled_off_box():
    grid = empty_grid()
    # Wall off a 3x3 box (interior 1x1 open cell at (5,5))
    for x in range(4, 7):
        grid[4][x] = 1
        grid[6][x] = 1
    for y in range(4, 7):
        grid[y][4] = 1
        grid[y][6] = 1
    score = flood_fill_score(grid, 5, 5)
    assert score == 1  # only the center cell is reachable


def test_flood_fill_start_on_wall_returns_zero():
    grid = empty_grid()
    grid[10][10] = 1
    score = flood_fill_score(grid, 10, 10)
    assert score == 0


def test_flood_fill_out_of_bounds_start_returns_zero():
    grid = empty_grid()
    score = flood_fill_score(grid, -1, -1)
    assert score == 0


def test_get_safe_moves_excludes_reversal():
    grid = empty_grid()
    safe = get_safe_moves(grid, 10, 10, RIGHT)
    assert LEFT not in safe
    assert RIGHT in safe
    assert UP in safe
    assert DOWN in safe


def test_get_safe_moves_excludes_walls_and_borders():
    grid = empty_grid()
    grid[10][11] = 1  # blocks RIGHT
    safe = get_safe_moves(grid, 10, 10, UP)  # current dir UP, reversal DOWN excluded
    assert RIGHT not in safe
    assert LEFT in safe
    assert UP in safe


def test_get_safe_moves_at_corner():
    grid = empty_grid()
    # top-left corner: UP and LEFT go out of bounds
    safe = get_safe_moves(grid, 0, 0, RIGHT)
    assert UP not in safe
    assert LEFT not in safe
    assert RIGHT in safe
    assert DOWN in safe


def test_choose_direction_prefers_larger_open_area():
    grid = empty_grid()
    # Fully enclose a 1-cell pocket to the RIGHT of the start (walls on
    # every side of that pocket except the one leading back to start),
    # so taking RIGHT traps the AI in a tiny area, while DOWN leads to
    # the rest of the open grid.
    x, y = 10, 10
    pocket_x, pocket_y = x + 1, y
    grid[y][x] = 1                    # current head cell is itself a trail
                                       # cell in the real game (matches
                                       # game_engine's marking behavior)
    grid[pocket_y - 1][pocket_x] = 1  # wall above pocket
    grid[pocket_y + 1][pocket_x] = 1  # wall below pocket
    grid[pocket_y][pocket_x + 1] = 1  # wall to the right of pocket

    # Also wall off UP into a small 1-cell pocket, so DOWN is the only
    # safe move leading to the large open area of the grid.
    grid[y - 2][x] = 1
    grid[y - 1][x - 1] = 1
    grid[y - 1][x + 1] = 1

    chosen = choose_direction(grid, x, y, RIGHT)
    assert chosen == DOWN


def test_choose_direction_returns_current_when_cornered():
    grid = empty_grid()
    x, y = 5, 5
    # Wall off every neighbor except reversal, forcing an unavoidable crash
    grid[y - 1][x] = 1  # UP blocked
    grid[y + 1][x] = 1  # DOWN blocked
    grid[y][x + 1] = 1  # RIGHT blocked
    # LEFT is open but is the reversal of current_direction=RIGHT, so excluded
    chosen = choose_direction(grid, x, y, RIGHT)
    assert chosen == RIGHT  # no safe moves -> direction unchanged


def test_choose_direction_ties_prefer_straight():
    grid = empty_grid()
    x, y = 40, 30  # center of grid, fully open on all sides
    chosen = choose_direction(grid, x, y, RIGHT)
    assert chosen == RIGHT
