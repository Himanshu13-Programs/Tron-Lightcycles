"""
Entity definitions for Tron Lightcycles.

Holds the Lightcycle class shared by both the human-controlled player
and the AI agent, so game_engine.py and ai_brain.py operate on the
same data structure without duplicating state-tracking logic.
"""

from config import OPPOSITE


class Lightcycle:
    """
    Represents a single lightcycle: its position, current direction,
    trail history, and alive/dead state.
    """

    def __init__(self, x, y, direction, label):
        self.x = x
        self.y = y
        self.direction = direction  # (dx, dy) tuple
        self.trail = [(x, y)]
        self.alive = True
        self.label = label  # "player" or "ai", useful for grid marking / debugging

    def queue_turn(self, new_direction):
        """
        Attempts to change direction. Rejects 180-degree reversals
        and no-op moves in the same direction.
        """
        if not self.alive:
            return
        if new_direction == OPPOSITE.get(self.direction):
            return  # illegal reversal, ignored
        self.direction = new_direction

    def peek_next_position(self):
        """Returns the (x, y) the cycle will occupy after the next step, without moving."""
        dx, dy = self.direction
        return (self.x + dx, self.y + dy)

    def advance(self):
        """Moves the cycle forward one grid cell along its current direction."""
        if not self.alive:
            return
        nx, ny = self.peek_next_position()
        self.x, self.y = nx, ny
        self.trail.append((nx, ny))

    def kill(self):
        self.alive = False

    def __repr__(self):
        return f"<Lightcycle {self.label} pos=({self.x},{self.y}) dir={self.direction} alive={self.alive}>"
