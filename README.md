# Tron Lightcycles

An intelligent 2D grid-based real-time adversarial pathfinding simulation. A human player faces off against an AI opponent on an 80×60 grid, each leaving a permanent trail wall. Last cycle standing wins.

## Features

- Deterministic 60 FPS game loop, decoupled from grid-step timing
- Clean separation of concerns: rendering / game state / AI logic live in separate modules
- AI opponent using a two-tier heuristic strategy:
  - **Tier 1 — Look-Ahead Safe Step Validation**: filters out immediately fatal moves
  - **Tier 2 — Flood-Fill Area Selection**: among safe moves, picks the one that preserves the most open space, avoiding self-trapping
- Unit-tested core logic (collision rules, AI decision-making, entity behavior)

## Project Structure

```
tron-lightcycles/
├── src/
│   ├── main.py          # Pygame loop, rendering, human input
│   ├── game_engine.py   # Grid state, collision detection, step logic
│   ├── ai_brain.py       # AI decision-making (look-ahead + flood-fill)
│   ├── entities.py       # Lightcycle entity class
│   └── config.py         # Shared constants (grid size, colors, etc.)
├── tests/                 # Unit tests for engine, AI, and entities
├── docs/PRD.md            # Original product requirements document
└── assets/                # Fonts / sounds (optional)
```

## Setup

```bash
git clone <your-repo-url>
cd tron-lightcycles
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the game

```bash
cd src
python main.py
```

**Controls:** Arrow keys or WASD to steer. `R` restarts after a round ends. `Esc` quits.

## Running tests

```bash
pytest tests/
```

## Rules

- Both cycles move continuously in a straight line — you can't stop.
- Turns are 90° only; 180° reversals are ignored.
- You lose if you hit a wall, your own trail, or the opponent's trail.

## Roadmap ideas

- Difficulty levels (tune AI look-ahead depth / area-weighting)
- Local two-player mode
- Power-ups or arena obstacles
- Score/round tracking across multiple rounds

