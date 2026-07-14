"""
Core state module for Tron Lightcycles.

Owns the 2D matrix representing the arena, applies collision rules,
and advances both entities one grid-step at a time. Deliberately has
no rendering or input-handling code (see PRD section 3.2 / 3.3
separation of concerns).
"""

from config import GRID_WIDTH, GRID_HEIGHT, EMPTY, PLAYER_TRAIL, AI_TRAIL
from entities import Lightcycle


class GameEngine:
    def __init__(self, player_spawn, player_dir, ai_spawn, ai_dir):
        # Grid[R][C], all zero-initialized per PRD 3.2
        self.grid = [[EMPTY for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

        self.player = Lightcycle(player_spawn[0], player_spawn[1], player_dir, "player")
        self.ai = Lightcycle(ai_spawn[0], ai_spawn[1], ai_dir, "ai")

        self._mark_trail_cell(self.player.x, self.player.y, PLAYER_TRAIL)
        self._mark_trail_cell(self.ai.x, self.ai.y, AI_TRAIL)

        self.game_over = False
        self.winner = None  # "player", "ai", "draw", or None while in progress

    # ------------------------------------------------------------------
    # Grid helpers
    # ------------------------------------------------------------------
    def _mark_trail_cell(self, x, y, value):
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            self.grid[y][x] = value

    def is_in_bounds(self, x, y):
        return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT

    def is_cell_open(self, x, y):
        """True if the cell is in-bounds and unoccupied by any trail."""
        return self.is_in_bounds(x, y) and self.grid[y][x] == EMPTY

    def snapshot_grid(self):
        """
        Returns a shallow copy of the grid matrix for the AI module,
        so the AI never mutates live game state (PRD 3.3).
        """
        return [row[:] for row in self.grid]

    # ------------------------------------------------------------------
    # Collision validation (PRD section 2, Collision Matrix Rules)
    # ------------------------------------------------------------------
    def _check_collision(self, cycle):
        x, y = cycle.peek_next_position()

        if not self.is_in_bounds(x, y):
            return True  # hit outer border

        if self.grid[y][x] != EMPTY:
            return True  # hit own trail or opponent trail

        return False

    # ------------------------------------------------------------------
    # Step update
    # ------------------------------------------------------------------
    def step(self):
        """
        Advances the simulation by one grid-step:
          1. Validate collisions for both entities BEFORE moving either,
             using next-position checks against the current grid state.
          2. Move survivors and stamp new trail cells.
          3. Resolve game-over state (including simultaneous-loss draws).
        """
        if self.game_over:
            return

        player_will_crash = self._check_collision(self.player)
        ai_will_crash = self._check_collision(self.ai)

        # Handle head-on collision: both moving into the same open cell
        if not player_will_crash and not ai_will_crash:
            if self.player.peek_next_position() == self.ai.peek_next_position():
                player_will_crash = True
                ai_will_crash = True

        if player_will_crash:
            self.player.kill()
        else:
            self.player.advance()
            self._mark_trail_cell(self.player.x, self.player.y, PLAYER_TRAIL)

        if ai_will_crash:
            self.ai.kill()
        else:
            self.ai.advance()
            self._mark_trail_cell(self.ai.x, self.ai.y, AI_TRAIL)

        self._resolve_game_over()

    def _resolve_game_over(self):
        if not self.player.alive and not self.ai.alive:
            self.game_over = True
            self.winner = "draw"
        elif not self.player.alive:
            self.game_over = True
            self.winner = "ai"
        elif not self.ai.alive:
            self.game_over = True
            self.winner = "player"
