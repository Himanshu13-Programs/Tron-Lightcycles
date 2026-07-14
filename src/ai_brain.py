"""
Intelligent agent module for Tron Lightcycles (PRD section 4).

Implements a deterministic Two-Tier Heuristic Matrix Strategy:
  Tier 1 - Look-Ahead Safe Step Validation
  Tier 2 - Connected Component Area Selection (Flood-Fill)

This module is fully decoupled from rendering and Pygame. It operates
on a grid snapshot + position tuples handed to it each frame, and
returns a chosen direction vector. It never mutates the live grid.
"""

from collections import deque
from config import GRID_WIDTH, GRID_HEIGHT, EMPTY, ALL_DIRECTIONS, OPPOSITE


def flood_fill_score(grid, start_x, start_y):
    """
    Breadth-First Search over empty matrix elements starting from
    (start_x, start_y), returning the count of reachable open cells.

    Matches PRD 4/Tier 2 spec. Uses collections.deque for O(1) pops
    instead of list.pop(0), which is O(n) and would slow this down
    considerably on an 80x60 grid searched multiple times per frame.
    """
    queue = deque([(start_x, start_y)])
    visited = set()
    count = 0

    while queue:
        x, y = queue.popleft()
        if (x, y) in visited:
            continue
        if not (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT):
            continue
        if grid[y][x] != EMPTY:
            continue

        visited.add((x, y))
        count += 1

        queue.append((x + 1, y))
        queue.append((x - 1, y))
        queue.append((x, y + 1))
        queue.append((x, y - 1))

    return count


def get_safe_moves(grid, x, y, current_direction):
    """
    Tier 1: Returns the list of direction vectors that are immediately
    safe to take from (x, y) -- in-bounds, unoccupied, and not a
    180-degree reversal of current_direction.
    """
    safe_moves = []
    reverse = OPPOSITE.get(current_direction)

    for d in ALL_DIRECTIONS:
        if d == reverse:
            continue
        nx, ny = x + d[0], y + d[1]
        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and grid[ny][nx] == EMPTY:
            safe_moves.append(d)

    return safe_moves


def choose_direction(grid, x, y, current_direction):
    """
    Top-level AI decision function, called once per grid-step.

    1. Computes the safe move set (Tier 1).
    2. If no safe moves exist, the AI is cornered -- return current
       direction unchanged (a crash is unavoidable; game_engine will
       resolve the loss).
    3. Otherwise, for every safe candidate direction, simulate taking
       that step and score the resulting reachable area via flood-fill
       (Tier 2). Pick the direction with the largest open area,
       preferring the current direction on ties to avoid needless
       zig-zagging.
    """
    safe_moves = get_safe_moves(grid, x, y, current_direction)

    if not safe_moves:
        return current_direction  # no escape; crash is inevitable

    best_direction = None
    best_score = -1

    for d in safe_moves:
        nx, ny = x + d[0], y + d[1]
        score = flood_fill_score(grid, nx, ny)

        # Prefer strictly larger area; on ties, prefer continuing straight
        if score > best_score or (score == best_score and d == current_direction):
            best_score = score
            best_direction = d

    return best_direction
