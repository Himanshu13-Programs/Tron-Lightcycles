"""
Unit tests for GameEngine: boundary collisions, self/opponent trail
collisions, head-on collisions, and step progression.

Run with: pytest tests/test_game_engine.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from game_engine import GameEngine
from config import GRID_WIDTH, GRID_HEIGHT, RIGHT, LEFT, UP, DOWN, EMPTY, PLAYER_TRAIL, AI_TRAIL


def make_engine(player_pos=(10, 10), player_dir=RIGHT, ai_pos=(60, 10), ai_dir=LEFT):
    return GameEngine(player_pos, player_dir, ai_pos, ai_dir)


def test_initial_grid_marks_spawn_cells():
    engine = make_engine()
    px, py = engine.player.x, engine.player.y
    ax, ay = engine.ai.x, engine.ai.y
    assert engine.grid[py][px] == PLAYER_TRAIL
    assert engine.grid[ay][ax] == AI_TRAIL


def test_step_advances_position():
    engine = make_engine(player_pos=(10, 10), player_dir=RIGHT)
    engine.step()
    assert engine.player.x == 11
    assert engine.player.y == 10
    assert engine.grid[10][11] == PLAYER_TRAIL


def test_border_collision_kills_player():
    engine = make_engine(player_pos=(GRID_WIDTH - 1, 5), player_dir=RIGHT,
                          ai_pos=(5, 5), ai_dir=RIGHT)
    engine.step()
    assert not engine.player.alive
    assert engine.game_over
    assert engine.winner == "ai"


def test_border_collision_top_edge():
    engine = make_engine(player_pos=(5, 0), player_dir=UP,
                          ai_pos=(50, 50), ai_dir=LEFT)
    engine.step()
    assert not engine.player.alive


def test_self_trail_collision():
    # Force the player into a tight loop so it hits its own trail
    engine = make_engine(player_pos=(10, 10), player_dir=RIGHT,
                          ai_pos=(60, 30), ai_dir=LEFT)
    # RIGHT, DOWN, LEFT, UP should bring it back onto its own trail
    engine.step()  # moves right to (11,10)
    engine.player.queue_turn(DOWN)
    engine.step()  # (11,11)
    engine.player.queue_turn(LEFT)
    engine.step()  # (10,11)
    engine.player.queue_turn(UP)
    engine.step()  # would move to (10,10) -- the original spawn trail cell
    assert not engine.player.alive
    assert engine.winner == "ai"


def test_opponent_trail_collision():
    # Place AI directly in the player's path so the player drives into it
    engine = make_engine(player_pos=(10, 10), player_dir=RIGHT,
                          ai_pos=(12, 10), ai_dir=UP)
    engine.step()  # player -> (11,10), ai -> (12,9); no collision yet
    # Now player's next move (12,10) is the AI's old trail cell
    engine.step()
    assert not engine.player.alive


def test_head_on_collision_is_a_draw():
    engine = make_engine(player_pos=(10, 10), player_dir=RIGHT,
                          ai_pos=(12, 10), ai_dir=LEFT)
    engine.step()  # both move into (11, 10) simultaneously
    assert not engine.player.alive
    assert not engine.ai.alive
    assert engine.winner == "draw"


def test_no_further_steps_after_game_over():
    engine = make_engine(player_pos=(GRID_WIDTH - 1, 5), player_dir=RIGHT,
                          ai_pos=(5, 5), ai_dir=RIGHT)
    engine.step()
    assert engine.game_over
    ai_x_before = engine.ai.x
    engine.step()  # should be a no-op
    assert engine.ai.x == ai_x_before


def test_snapshot_grid_is_independent_copy():
    engine = make_engine()
    snapshot = engine.snapshot_grid()
    snapshot[0][0] = 999
    assert engine.grid[0][0] != 999
