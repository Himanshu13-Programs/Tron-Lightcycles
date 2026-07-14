# Product Requirement Document (PRD)

## Project Title
**Tron Lightcycles: An Intelligent 2D Grid-Based Real-Time Adversarial Pathfinding Simulation**

---

## 1. Introduction & Project Objectives
Tron Lightcycles is a top-down, 2D arcade-style strategy game developed using Python (Pygame) or Java (Swing/AWT). The project pits a human player against an automated, highly calculative AI agent within a closed grid space. Both entities control a "Lightcycle" moving continuously in fixed cardinal directions, leaving behind an absolute, solid trail wall.

### 1.1 Target Objectives
* **Deterministic Game Loop:** Build a reliable 60 FPS update cycle down-sampled to a strict spatial grid.
* **Separation of Concerns:** Keep game state management, UI rendering, and AI calculation tasks completely modular.
* **Algorithmic Showcase:** Demonstrate real-time grid search efficiency using look-ahead collision handling and multi-node Flood-Fill area calculation to give the AI an intellectual advantage over human prediction limits.

---

## 2. Game Mechanics & Core Rules
* **Grid Space Constraints:** The arena operates on an 80x60 coordinate system. Each coordinate maps to a distinct 10x10 pixel square on a standard 800x600 display.
* **Linear Trajectory:** Both lightcycles spawn at opposite sides of the arena and move forward continuously. They cannot stop or remain idle.
* **90-Degree Steer Restrictions:** Turning inputs are strictly orthogonal (Up, Down, Left, Right). 180-degree immediate reversals are barred.
* **Collision Matrix Rules:** A solid trail wall is appended to the game matrix at the cycle's tail coordinate every single step. A player instantly loses if their front bumper contacts the outer map borders, their own trail, or the opponent's trail.

(See repository source for full architecture, module breakdown, and AI algorithmic specification -- this file mirrors the original PRD supplied for the project.)
