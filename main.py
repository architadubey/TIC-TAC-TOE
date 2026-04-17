import customtkinter as ctk
import tkinter as tk
import math
import random

# --- SETTINGS ---
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class MinimaxAI:
    def __init__(self, ai_player="O", human_player="X", difficulty="Unbeatable"):
        self.ai = ai_player
        self.human = human_player
        self.difficulty = difficulty

    def evaluate(self, board):
        lines = [
            [board[0][0], board[0][1], board[0][2]],
            [board[1][0], board[1][1], board[1][2]],
            [board[2][0], board[2][1], board[2][2]],
            [board[0][0], board[1][0], board[2][0]],
            [board[0][1], board[1][1], board[2][1]],
            [board[0][2], board[1][2], board[2][2]],
            [board[0][0], board[1][1], board[2][2]],
            [board[2][0], board[1][1], board[0][2]]
        ]
        for line in lines:
            if line[0] == line[1] == line[2] and line[0] != "":
                if line[0] == self.ai: return 10
                elif line[0] == self.human: return -10
        return 0

    def is_moves_left(self, board):
        return any("" in row for row in board)

    def minimax(self, board, depth, is_max, alpha=-math.inf, beta=math.inf):
        score = self.evaluate(board)
        if score == 10: return score - depth
        if score == -10: return score + depth
        if not self.is_moves_left(board): return 0
            
        if is_max:
            best = -math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = self.ai
                        best = max(best, self.minimax(board, depth + 1, not is_max, alpha, beta))
                        board[i][j] = ""
                        alpha = max(alpha, best)
                        if beta <= alpha: break
            return best
        else:
            best = math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = self.human
                        best = min(best, self.minimax(board, depth + 1, not is_max, alpha, beta))
                        board[i][j] = ""
                        beta = min(beta, best)
                        if beta <= alpha: break
            return best

    def get_empty_cells(self, board):
        return [(i, j) for i in range(3) for j in range(3) if board[i][j] == ""]

    def find_best_move(self, board):
        empty_cells = self.get_empty_cells(board)
        if not empty_cells:
            return (-1, -1)

        if self.difficulty == "Easy":
            return random.choice(empty_cells)

        if self.difficulty == "Medium":
            # Medium tries to put random move, but will take immediate win or block immediate loss.
            # We can check 1 step lookahead.
            for is_max, player in [(True, self.ai), (False, self.human)]: # First check win, then block
                for r, c in empty_cells:
                    board[r][c] = player
                    if self.evaluate(board) == (10 if is_max else -10):
                        board[r][c] = ""
                        return (r, c)
                    board[r][c] = ""
            # If no immediate threat/win, pick random
            return random.choice(empty_cells)

        # Unbeatable (Minimax)
        if len(empty_cells) == 9:
            return (1, 1) # Center start optimization
            
        best_val = -math.inf
        best_move = (-1, -1)
        for i, j in empty_cells:
            board[i][j] = self.ai
            move_val = self.minimax(board, 0, False)
            board[i][j] = ""
            if move_val > best_val:
                best_move = (i, j)
                best_val = move_val
        return best_move

class TicTacToeAppV2(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Tic Tac Toe AI - V2")
        self.geometry("500x700")
        self.resizable(False, False)
        
        # Colors
        self.X_COLOR = "#BB86FC"
        self.O_COLOR = "#03DAC6"
        self.GRID_COLOR = "#333333"
        self.HOVER_X = "#332244"
        self.HOVER_O = "#113333"
        self.CANVAS_BG = "#1A1A1A"
        
        # Game State
        self.scores = {"P1": 0, "P2": 0, "Draws": 0}
        self.mode = "PVC"
        self.difficulty = "Unbeatable"
        self.first_turn = "Player" # "Player" or "Computer" or "P1" or "P2"
        self.current_player = "X" # X always goes first logically
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.game_over = False
        
        # Player Mapping
        self.human_symbol = "X"
        self.ai_symbol = "O"
        self.ai = MinimaxAI(self.ai_symbol, self.human_symbol, self.difficulty)
        
        self.show_menu()

    def show_menu(self):
        for widget in self.winfo_children():
            widget.destroy()
            
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=40, pady=40)
        
        # Title
        title_lbl = ctk.CTkLabel(container, text="TIC TAC TOE", font=("Helvetica", 36, "bold"))
        title_lbl.pack(pady=(20, 40))

        # Settings
        settings_frame = ctk.CTkFrame(container)
        settings_frame.pack(fill="x", pady=20, ipadx=10, ipady=10)
        
        # Mode Section
        ctk.CTkLabel(settings_frame, text="Game Mode:", font=("Helvetica", 16, "bold")).pack(pady=(10, 0))
        self.mode_var = ctk.StringVar(value="PVC")
        mode_seg = ctk.CTkSegmentedButton(settings_frame, values=["Play vs Computer", "Play vs Friend"], 
                                          command=self.on_mode_change)
        mode_seg.set("Play vs Computer")
        mode_seg.pack(pady=10)

        # Difficulty Section
        self.diff_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        self.diff_frame.pack(fill="x")
        ctk.CTkLabel(self.diff_frame, text="AI Difficulty:", font=("Helvetica", 14)).pack()
        self.diff_seg = ctk.CTkSegmentedButton(self.diff_frame, values=["Easy", "Medium", "Unbeatable"])
        self.diff_seg.set("Unbeatable")
        self.diff_seg.pack(pady=5)
        
        # First Turn Section
        ctk.CTkLabel(settings_frame, text="Who goes first? ('X')", font=("Helvetica", 14)).pack(pady=(10, 0))
        self.turn_seg = ctk.CTkSegmentedButton(settings_frame, values=["Player", "Computer"])
        self.turn_seg.set("Player")
        self.turn_seg.pack(pady=5)
        
        # Start button
        start_btn = ctk.CTkButton(container, text="Start Game", height=50, font=("Helvetica", 18, "bold"), 
                                  command=self.start_game)
        start_btn.pack(pady=30, fill="x")
        
    def on_mode_change(self, value):
        if value == "Play vs Friend":
            self.mode = "PVP"
            self.diff_frame.pack_forget()
            self.turn_seg.configure(values=["Player 1", "Player 2"])
            self.turn_seg.set("Player 1")
        else:
            self.mode = "PVC"
            # Quick hack to preserve correct ordering: repack everything in frame
            for child in self.turn_seg.master.winfo_children():
                child.pack_forget()
            
            ctk.CTkLabel(self.turn_seg.master, text="Game Mode:", font=("Helvetica", 16, "bold")).pack(pady=(10, 0))
            self.turn_seg.master.winfo_children()[1].pack(pady=10) # Mode segment
            
            self.diff_frame.pack(fill="x")
            
            ctk.CTkLabel(self.turn_seg.master, text="Who goes first? ('X')", font=("Helvetica", 14)).pack(pady=(10, 0))
            self.turn_seg.configure(values=["Player", "Computer"])
            self.turn_seg.set("Player")
            self.turn_seg.pack(pady=5)
            

    def start_game(self):
        if self.mode == "PVC":
            self.difficulty = self.diff_seg.get()
            self.first_turn = self.turn_seg.get()
        else:
            self.first_turn = self.turn_seg.get()

        self.setup_game_variables()
        self.build_game_ui()
        
        if self.mode == "PVC" and self.first_turn == "Computer":
            self.status_lbl.configure(text="Computer is thinking...")
            self.after(500, self.computer_move)

    def setup_game_variables(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_over = False
        
        if self.mode == "PVC":
            if self.first_turn == "Computer":
                self.ai_symbol = "X"
                self.human_symbol = "O"
            else:
                self.ai_symbol = "O"
                self.human_symbol = "X"
            self.ai = MinimaxAI(self.ai_symbol, self.human_symbol, self.difficulty)

    def build_game_ui(self):
        for widget in self.winfo_children():
            widget.destroy()
            
        top_bar = ctk.CTkFrame(self)
        top_bar.pack(fill="x", padx=20, pady=20)
        
        p1_name = "Player" if self.mode == "PVC" else "Player 1"
        p2_name = "Computer" if self.mode == "PVC" else "Player 2"
        
        ctk.CTkLabel(top_bar, text=f"{p1_name}: {self.scores['P1']}", font=("Helvetica", 16, "bold"), text_color=self.X_COLOR if self.human_symbol=="X" or self.mode=="PVP" else self.O_COLOR).pack(side="left", padx=20, pady=10)
        ctk.CTkLabel(top_bar, text=f"Draws: {self.scores['Draws']}", font=("Helvetica", 16, "bold")).pack(side="left", expand=True, pady=10)
        ctk.CTkLabel(top_bar, text=f"{p2_name}: {self.scores['P2']}", font=("Helvetica", 16, "bold"), text_color=self.O_COLOR if self.human_symbol=="X" or self.mode=="PVP" else self.X_COLOR).pack(side="right", padx=20, pady=10)

        self.status_lbl = ctk.CTkLabel(self, text=f"{self.current_player}'s Turn", font=("Helvetica", 24, "bold"))
        self.status_lbl.pack(pady=10)

        self.canvas = tk.Canvas(self, width=360, height=360, bg=self.CANVAS_BG, highlightthickness=0)
        self.canvas.pack(pady=20)
        
        self.redraw_grid()
            
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Motion>", self.on_hover)
        self.canvas.bind("<Leave>", self.on_leave)

        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=40, pady=10)
        
        menu_btn = ctk.CTkButton(bottom_frame, text="Settings Menu", command=self.reset_and_show_menu, fg_color="transparent", border_width=1)
        menu_btn.pack(side="left")
        
        self.play_again_btn = ctk.CTkButton(bottom_frame, text="Play Again", command=self.reset_board, state="disabled")
        self.play_again_btn.pack(side="right")

    def reset_and_show_menu(self):
        self.scores = {"P1": 0, "P2": 0, "Draws": 0}
        self.show_menu()

    def reset_board(self):
        self.setup_game_variables()
        self.build_game_ui()
        if self.mode == "PVC" and self.first_turn == "Computer":
            self.status_lbl.configure(text="Computer is thinking...")
            self.after(500, self.computer_move)

    def on_hover(self, event):
        if self.game_over: return
        if self.mode == "PVC" and self.current_player == self.ai_symbol: return
        
        col = event.x // 120
        row = event.y // 120
        
        self.canvas.delete("hover")
        
        if 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == "":
            x1, y1 = col * 120, row * 120
            color = self.HOVER_X if self.current_player == "X" else self.HOVER_O
            self.canvas.create_rectangle(x1, y1, x1+120, y1+120, fill=color, outline="", tags="hover")
            # Redraw grid lines as they might be covered by hover
            self.canvas.tag_lower("hover")
            self.canvas.tag_raise("grid")

    def redraw_grid(self):
        self.canvas.delete("grid")
        for i in range(1, 3):
            self.canvas.create_line(120 * i, 0, 120 * i, 360, fill=self.GRID_COLOR, width=4, tags="grid")
            self.canvas.create_line(0, 120 * i, 360, 120 * i, fill=self.GRID_COLOR, width=4, tags="grid")

    def on_leave(self, event):
        self.canvas.delete("hover")

    def on_click(self, event):
        if self.game_over: return
        if self.mode == "PVC" and self.current_player == self.ai_symbol: return
            
        col = event.x // 120
        row = event.y // 120
        
        if 0 <= row < 3 and 0 <= col < 3:
            if self.board[row][col] == "":
                self.canvas.delete("hover")
                self.make_move(row, col)

    def draw_x(self, row, col):
        x1, y1 = col * 120 + 30, row * 120 + 30
        x2, y2 = col * 120 + 90, row * 120 + 90
        self.canvas.create_line(x1, y1, x2, y2, fill=self.X_COLOR, width=8, capstyle=tk.ROUND)
        self.canvas.create_line(x2, y1, x1, y2, fill=self.X_COLOR, width=8, capstyle=tk.ROUND)

    def draw_o(self, row, col):
        x, y = col * 120 + 60, row * 120 + 60
        self.canvas.create_oval(x - 35, y - 35, x + 35, y + 35, outline=self.O_COLOR, width=8)

    def make_move(self, row, col):
        self.board[row][col] = self.current_player
        
        if self.current_player == "X":
            self.draw_x(row, col)
            self.current_player = "O"
        else:
            self.draw_o(row, col)
            self.current_player = "X"
            
        winner = self.check_winner()
        
        if winner:
            self.end_game(winner)
            return
            
        if self.ai.is_moves_left(self.board) is False:
            self.end_game("Draw")
            return
            
        p_name = "Computer" if (self.mode == "PVC" and self.current_player == self.ai_symbol) else f"Player ({self.current_player})"
        if self.mode == "PVP": p_name = f"Player 1" if self.current_player == "X" else f"Player 2"
        self.status_lbl.configure(text=f"{p_name}'s Turn")
        
        if self.mode == "PVC" and self.current_player == self.ai_symbol:
            self.after(500, self.computer_move)

    def computer_move(self):
        if self.game_over: return
        move = self.ai.find_best_move(self.board)
        if move != (-1, -1):
            self.make_move(move[0], move[1])

    def check_winner(self):
        b = self.board
        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] and b[i][0] != "":
                self.draw_win_line(i, 0, i, 2)
                return b[i][0]
            if b[0][i] == b[1][i] == b[2][i] and b[0][i] != "":
                self.draw_win_line(0, i, 2, i)
                return b[0][i]
        if b[0][0] == b[1][1] == b[2][2] and b[0][0] != "":
            self.draw_win_line(0, 0, 2, 2)
            return b[0][0]
        if b[0][2] == b[1][1] == b[2][0] and b[0][2] != "":
            self.draw_win_line(0, 2, 2, 0)
            return b[0][2]
        return None

    def draw_win_line(self, r1, c1, r2, c2):
        x1 = c1 * 120 + 60
        y1 = r1 * 120 + 60
        x2 = c2 * 120 + 60
        y2 = r2 * 120 + 60
        margin = 35
        if c1 == c2: y1 -= margin; y2 += margin
        elif r1 == r2: x1 -= margin; x2 += margin
        else:
            if x1 < x2: x1 -= margin; y1 -= margin; x2 += margin; y2 += margin
            else: x1 += margin; y1 -= margin; x2 -= margin; y2 += margin
        self.canvas.create_line(x1, y1, x2, y2, fill="#FF5252", width=12, capstyle=tk.ROUND)

    def end_game(self, result):
        self.game_over = True
        self.play_again_btn.configure(state="normal")
        
        if result == "Draw":
            self.status_lbl.configure(text="It's a Draw!", text_color="#FFEB3B")
            self.scores["Draws"] += 1
        else:
            if self.mode == "PVC":
                if result == self.human_symbol:
                    self.scores["P1"] += 1
                    winner_name = "Player"
                else:
                    self.scores["P2"] += 1
                    winner_name = "Computer"
            else:
                if result == "X":
                    self.scores["P1"] += 1
                    winner_name = "Player 1"
                else:
                    self.scores["P2"] += 1
                    winner_name = "Player 2"
                    
            self.status_lbl.configure(text=f"{winner_name} Wins!", text_color="#4CAF50")
            
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and len(widget.winfo_children()) == 3:
                labels = widget.winfo_children()
                if isinstance(labels[0], ctk.CTkLabel) and ("Player" in labels[0].cget("text")):
                    p1_name = "Player" if self.mode == "PVC" else "Player 1"
                    p2_name = "Computer" if self.mode == "PVC" else "Player 2"
                    labels[0].configure(text=f"{p1_name}: {self.scores['P1']}")
                    labels[1].configure(text=f"Draws: {self.scores['Draws']}")
                    labels[2].configure(text=f"{p2_name}: {self.scores['P2']}")

if __name__ == "__main__":
    app = TicTacToeAppV2()
    app.mainloop()
