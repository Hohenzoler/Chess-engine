import chess

class engine:
    def __init__(self, board):
        self.board = board
        self.depth = 4
        self.pieces = {'Q': 900, 'R': 500, 'B': 300, 'N': 280, 'P': 100, 'q': -900, 'r': -500, 'b': -300, 'n': -280, 'p': -100,}

    def evaluate(self):
        eval = 0

        for x in range(8):
            for y in range(8):
                sq = chess.square(x, y)
                p = self.board.piece_at(sq)
                if p != None and p.symbol() != 'K' and p.symbol() != 'k':
                    eval += self.pieces[p.symbol()]

        if self.board.is_checkmate():
            if self.board.turn:
                eval -= 999999999999999
            else:
                eval += 999999999999999
        return eval


    def minmax(self, depth, alpha, beta, maximize):
        if depth == 0 or self.board.is_game_over():
            return self.evaluate()


        if maximize:
            best = -float("inf")
            for move in self.board.legal_moves:
                self.board.push(move)
                score = self.minmax(depth-1, alpha, beta, False)
                self.board.pop()
                best = max(best, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return best

        else:
            best = float("inf")
            for move in self.board.legal_moves:
                self.board.push(move)
                score = self.minmax(depth - 1, alpha, beta,  True)
                self.board.pop()
                best = min(best, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return best


    def get_move(self):
        best_move = None
        if self.board.turn:
            best_score = -float('inf')
            for move in self.board.legal_moves:
                self.board.push(move)
                score = self.minmax(self.depth-1, -float('inf'), float('inf'),  False)
                self.board.pop()

                if score > best_score:
                    best_score = score
                    best_move = move

        else:
            best_score = float('inf')
            for move in self.board.legal_moves:
                self.board.push(move)
                score = self.minmax(self.depth - 1, -float('inf'), float('inf'), True)
                self.board.pop()

                if score < best_score:
                    best_score = score
                    best_move = move


        return best_move





