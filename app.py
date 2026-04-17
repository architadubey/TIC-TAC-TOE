from flask import Flask, render_template, request, jsonify
import math
import random

app = Flask(__name__)

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
            for is_max, player in [(True, self.ai), (False, self.human)]:
                for r, c in empty_cells:
                    board[r][c] = player
                    if self.evaluate(board) == (10 if is_max else -10):
                        board[r][c] = ""
                        return (r, c)
                    board[r][c] = ""
            return random.choice(empty_cells)

        if len(empty_cells) == 9:
            return (1, 1)
            
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/move', methods=['POST'])
def get_move():
    data = request.json
    board = data.get('board')
    difficulty = data.get('difficulty', 'Unbeatable')
    ai_symbol = data.get('ai_symbol', 'O')
    human_symbol = 'X' if ai_symbol == 'O' else 'O'
    
    ai = MinimaxAI(ai_player=ai_symbol, human_player=human_symbol, difficulty=difficulty)
    move = ai.find_best_move(board)
    
    return jsonify({"move": move})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
