"""
Unit tests for the Lightcycle entity class: turning rules, movement,
and alive/dead state transitions.

Run with: pytest tests/test_entities.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from entities import Lightcycle
from config import UP, DOWN, LEFT, RIGHT


def test_initial_state():
    cycle = Lightcycle(5, 5, RIGHT, "player")
    assert cycle.x == 5
    assert cycle.y == 5
    assert cycle.direction == RIGHT
    assert cycle.alive
    assert cycle.trail == [(5, 5)]


def test_advance_moves_position_and_appends_trail():
    cycle = Lightcycle(5, 5, RIGHT, "player")
    cycle.advance()
    assert (cycle.x, cycle.y) == (6, 5)
    assert cycle.trail == [(5, 5), (6, 5)]


def test_queue_turn_rejects_180_reversal():
    cycle = Lightcycle(5, 5, RIGHT, "player")
    cycle.queue_turn(LEFT)
    assert cycle.direction == RIGHT  # reversal ignored


def test_queue_turn_accepts_valid_turn():
    cycle = Lightcycle(5, 5, RIGHT, "player")
    cycle.queue_turn(UP)
    assert cycle.direction == UP


def test_peek_next_position_does_not_mutate():
    cycle = Lightcycle(5, 5, DOWN, "ai")
    peeked = cycle.peek_next_position()
    assert peeked == (5, 6)
    assert (cycle.x, cycle.y) == (5, 5)  # unchanged


def test_kill_sets_alive_false():
    cycle = Lightcycle(5, 5, RIGHT, "player")
    cycle.kill()
    assert not cycle.alive


def test_dead_cycle_ignores_turn_and_advance():
    cycle = Lightcycle(5, 5, RIGHT, "player")
    cycle.kill()
    cycle.queue_turn(UP)
    cycle.advance()
    assert cycle.direction == RIGHT
    assert (cycle.x, cycle.y) == (5, 5)
