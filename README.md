# Gomoku — Minimax & Alpha-Beta AI (Python + Tkinter)

**Gomoku** (Five-in-a-Row) is a board game implemented in Python with a simple Tkinter GUI.  
This project includes two AI implementations (basic Minimax and Minimax with Alpha-Beta pruning), supports Human vs AI and AI vs AI modes, and lets you set an initial board position for testing. The main implementation is in `ffc033da-d405-4611-8916-43ee836c5784.py`. :contentReference[oaicite:1]{index=1}
<img width="315" height="150" alt="image" src="https://github.com/user-attachments/assets/d3a13099-7da3-4bfd-b0bb-a7ce36c3ab51" />
<img width="315" height="150" alt="Screenshot 2025-11-05 192319" src="https://github.com/user-attachments/assets/20970313-e5f4-4e3c-939d-7d6c99c9ef37" />
<img width="500" height="500" alt="Screenshot 2025-11-05 192413" src="https://github.com/user-attachments/assets/ac5334b1-9d31-41da-bf7c-b29c358d7270" />

---

## Features

- 15×15 Gomoku board with GUI (Tkinter).
- Human vs AI (click to place a piece).
- AI vs AI (watch two AIs play: Minimax vs Alpha-Beta).
- Two AI strategies:
  - **Minimax (basic)** — brute-force search with board pruning via neighbourhood selection.
  - **Minimax + Alpha-Beta pruning** — same evaluation but faster search due to pruning.
- Adjustable AI search depth (recommended 1–3 for interactive play).
- Option to pre-fill initial moves through a dialog (useful for testing positions).
- Simple evaluation function and move generation that focuses on nearby empty cells.

---

## Getting started

### Requirements
- Python 3.8+ (should work with 3.8 — 3.12)
- Tkinter (usually included with standard Python installs)

### Run
1. Clone the repo:
   ```bash
   git clone https://github.com/<your-username>/gomoku-ai-tk.git
   cd gomoku-ai-tk
2. Run the game:
```
python gomoku.py
```
---
## How to play / UI notes

When the program starts you will be asked to choose a mode:

1 — Human vs AI (you click to place your stones, human plays black)

2 — AI vs AI (watch two AIs play automatically)

Enter AI search depth when prompted (1–4). Larger depth = stronger but slower AI.

Optional initial board setup: you can add starting moves by entering row col player (player 1 = human/black, 2 = AI/red). Use cancel to stop adding moves.

In Human vs AI, click a board cell to place your piece (if it’s your turn).
---
## Design & implementation notes

Board: 15×15 grid (constants at top of the file).

Move generation: get_empty_cells(radius=2) — returns empty cells within a small radius of existing stones to reduce branching factor.

Evaluation: simple pattern-based scoring — evaluates 5-cell lines and scores exponentially by count of same-player pieces (10^count).

Two search routines:

minimax_basic(depth, maximizing)

minimax_alpha_beta(depth, alpha, beta, maximizing)

GUI class GomokuGUI handles drawing, event binding, dialogs and match loops.

For full code, see gomoku.py
---
## Project structure
/ (repo root)

├─ gomoku.py   # main game + GUI

├─ README.md


