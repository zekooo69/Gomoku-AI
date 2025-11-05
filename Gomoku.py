import tkinter as tk
from tkinter import simpledialog, messagebox
import math

BOARD_SIZE = 15
EMPTY = 0
HUMAN = 1
AI = 2

DIRECTIONS = [(1, 0), (0, 1), (1, 1), (1, -1)]

class Gomoku:
    def __init__(self):
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def is_valid_move(self, x, y):
        return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and self.board[x][y] == EMPTY

    def make_move(self, x, y, player):
        self.board[x][y] = player

    def undo_move(self, x, y):
        self.board[x][y] = EMPTY

    def is_winner(self, player):
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.board[x][y] == player:
                    for dx, dy in DIRECTIONS:
                        if self.check_direction(x, y, dx, dy, player):
                            return True
        return False

    def check_direction(self, x, y, dx, dy, player):
        count = 0
        for i in range(-4, 5):
            nx, ny = x + i * dx, y + i * dy
            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                if self.board[nx][ny] == player:
                    count += 1
                    if count == 5:
                        return True
                else:
                    count = 0
        return False

    def is_board_full(self):
        return all(cell != EMPTY for row in self.board for cell in row)

    def get_empty_cells(self, radius=2):
        positions = set()
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.board[x][y] != EMPTY:
                    for dx in range(-radius, radius + 1):
                        for dy in range(-radius, radius + 1):
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and self.board[nx][ny] == EMPTY:
                                positions.add((nx, ny))
        if not positions:
            return [(BOARD_SIZE // 2, BOARD_SIZE // 2)]
        return list(positions)

    def evaluate(self):
        return self.evaluate_player(AI) - self.evaluate_player(HUMAN)

    def evaluate_player(self, player):
        score = 0
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                for dx, dy in DIRECTIONS:
                    score += self.evaluate_line(x, y, dx, dy, player)
        return score

    def evaluate_line(self, x, y, dx, dy, player):
        count = 0
        for i in range(5):
            nx, ny = x + i * dx, y + i * dy
            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                if self.board[nx][ny] == player:
                    count += 1
                elif self.board[nx][ny] != EMPTY:
                    return 0
            else:
                return 0
        return 10 ** count if count > 0 else 0

    def minimax_basic(self, depth, maximizing):
        if depth == 0 or self.is_winner(HUMAN) or self.is_winner(AI):
            return self.evaluate(), None

        best_move = None
        cells = self.get_empty_cells()

        if maximizing:
            max_eval = -math.inf
            for x, y in cells:
                self.make_move(x, y, AI)
                eval, _ = self.minimax_basic(depth - 1, False)
                self.undo_move(x, y)
                if eval > max_eval:
                    max_eval = eval
                    best_move = (x, y)
            return max_eval, best_move
        else:
            min_eval = math.inf
            for x, y in cells:
                self.make_move(x, y, HUMAN)
                eval, _ = self.minimax_basic(depth - 1, True)
                self.undo_move(x, y)
                if eval < min_eval:
                    min_eval = eval
                    best_move = (x, y)
            return min_eval, best_move

    def minimax_alpha_beta(self, depth, alpha, beta, maximizing):
        if depth == 0 or self.is_winner(HUMAN) or self.is_winner(AI):
            return self.evaluate(), None

        best_move = None
        cells = self.get_empty_cells()

        if maximizing:
            max_eval = -math.inf
            for x, y in cells:
                self.make_move(x, y, AI)
                eval, _ = self.minimax_alpha_beta(depth - 1, alpha, beta, False)
                self.undo_move(x, y)
                if eval > max_eval:
                    max_eval = eval
                    best_move = (x, y)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = math.inf
            for x, y in cells:
                self.make_move(x, y, HUMAN)
                eval, _ = self.minimax_alpha_beta(depth - 1, alpha, beta, True)
                self.undo_move(x, y)
                if eval < min_eval:
                    min_eval = eval
                    best_move = (x, y)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

class GomokuGUI:
    def __init__(self):
        self.game = Gomoku()
        self.window = tk.Tk()
        self.window.title("Gomoku")

        self.cell_size = 40
        self.canvas_size = BOARD_SIZE * self.cell_size
        self.canvas = tk.Canvas(self.window, width=self.canvas_size, height=self.canvas_size, bg="bisque")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_click)

        self.mode = simpledialog.askstring("Mode", "Choose mode:\n1. Human vs AI\n2. AI vs AI", parent=self.window)
        if self.mode not in ("1", "2"):
            messagebox.showerror("Error", "Invalid mode. Exiting.")
            self.window.destroy()
            return

        self.depth = simpledialog.askinteger("Depth", "Enter AI search depth (1-3 recommended):", minvalue=1, maxvalue=4, parent=self.window)
        if not self.depth:
            self.depth = 2

        self.initial_setup()
        self.current_player = HUMAN if self.mode == "1" else AI

        self.draw_board()

        if self.mode == "2":
            self.window.after(1000, self.ai_vs_ai)

        self.window.mainloop()

    def initial_setup(self):
        want_setup = messagebox.askyesno("Initial Setup", "Do you want to enter initial board positions?")
        if not want_setup:
            return

        while True:
            inp = simpledialog.askstring("Initial Move", "Enter move (row col player):\nplayer: 1=Human, 2=AI\nCancel to stop", parent=self.window)
            if inp is None:
                break
            try:
                x, y, player = map(int, inp.split())
                if player not in [HUMAN, AI] or not self.game.is_valid_move(x, y):
                    messagebox.showerror("Invalid Move", "Invalid move or player.")
                    continue
                self.game.make_move(x, y, player)
                self.draw_board()
            except Exception:
                messagebox.showerror("Error", "Invalid input format.")

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                x1 = i * self.cell_size
                y1 = j * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")
                piece = self.game.board[i][j]
                if piece != EMPTY:
                    color = "black" if piece == HUMAN else "red"
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill=color)

    def on_click(self, event):
        if self.mode != "1" or self.current_player != HUMAN:
            return

        x = event.x // self.cell_size
        y = event.y // self.cell_size

        if not self.game.is_valid_move(x, y):
            return

        self.game.make_move(x, y, HUMAN)
        self.draw_board()

        if self.game.is_winner(HUMAN):
            messagebox.showinfo("Game Over", "Human wins!")
            self.window.destroy()
            return

        if self.game.is_board_full():
            messagebox.showinfo("Game Over", "It's a draw!")
            self.window.destroy()
            return

        self.current_player = AI
        self.window.after(500, self.ai_move)

    def ai_move(self):
        _, move = self.game.minimax_alpha_beta(self.depth, -math.inf, math.inf, True)
        if move:
            self.game.make_move(move[0], move[1], AI)
            self.draw_board()

            if self.game.is_winner(AI):
                messagebox.showinfo("Game Over", "AI wins!")
                self.window.destroy()
                return

        if self.game.is_board_full():
            messagebox.showinfo("Game Over", "It's a draw!")
            self.window.destroy()
            return

        self.current_player = HUMAN

    def ai_vs_ai(self):
        if self.current_player == HUMAN:
            _, move = self.game.minimax_basic(self.depth, True)
        else:
            _, move = self.game.minimax_alpha_beta(self.depth, -math.inf, math.inf, True)

        if move:
            self.game.make_move(move[0], move[1], self.current_player)
            self.draw_board()

            if self.game.is_winner(self.current_player):
                label = "Minimax" if self.current_player == HUMAN else "Alpha-Beta"
                messagebox.showinfo("Game Over", f"AI ({label}) wins!")
                self.window.destroy()
                return

        if self.game.is_board_full():
            messagebox.showinfo("Game Over", "It's a draw!")
            self.window.destroy()
            return

        self.current_player = HUMAN if self.current_player == AI else AI
        self.window.after(500, self.ai_vs_ai)

if __name__ == "__main__":
    GomokuGUI()
