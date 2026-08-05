import chess
import chess.polyglot

class engine:
    def __init__(self, board):
        self.board = board
        self.depth = 6
        self.tt = {} # zobrist_hash
        self.Exact_tt = 0
        self.Upper_tt = 1
        self.Lower_tt = 2
        self.mate_score = 999999999999999


        self.pieces = {chess.QUEEN: 900, chess.ROOK: 500, chess.BISHOP: 300, chess.KNIGHT: 280, chess.PAWN: 100, chess.KING: 0}

    def evaluate(self):
        eval = 0

        for piece_type, value in self.pieces.items():
            white_count = chess.popcount(self.board.pieces_mask(piece_type, chess.WHITE))
            black_count = chess.popcount(self.board.pieces_mask(piece_type, chess.BLACK))

            eval += value * (white_count - black_count)


        return eval


    def minmax(self, depth, alpha, beta, maximize):

        if depth == 0 or self.board.is_checkmate() or self.board.is_stalemate():
            return self.evaluate()

        # Transpositional Table

        original_alpha = alpha
        key = chess.polyglot.zobrist_hash(self.board)
        tt_entry = self.tt.get(key)
        tt_move = None

        if tt_entry is not None and tt_entry[0] >= depth:
            tt_depth, tt_score, tt_flag, tt_move = tt_entry
            if tt_flag == self.Exact_tt:
                return tt_score
            elif tt_flag == self.Lower_tt:
                alpha = max(alpha, tt_score)
            elif tt_flag == self.Upper_tt:
                beta = min(beta, tt_score)

            if alpha >= beta:
                return tt_score
        elif tt_entry is not None:
            tt_move = tt_entry[3]


        moves = self.order_moves(self.board.legal_moves, tt_move)


        if maximize:
            best = -float("inf")
            for move in moves:
                self.board.push(move)
                score = self.minmax(depth-1, alpha, beta, False)
                self.board.pop()
                if score > best:
                    best = score
                    best_move = move
                alpha = max(alpha, score)
                if beta <= alpha:
                    break


        else:
            best = float("inf")
            for move in moves:
                self.board.push(move)
                score = self.minmax(depth - 1, alpha, beta,  True)
                self.board.pop()
                if score < best:
                    best = score
                    best_move = move
                beta = min(beta, score)
                if beta <= alpha:
                    break


        # add to tt
        flag = self.Exact_tt
        if best <= original_alpha:
            flag = self.Upper_tt
        elif best >= beta:
            flag = self.Lower_tt


        #avoid mate breaking tt
        if abs(best) < self.mate_score -1000:
            self.tt[key] = (depth, best, flag, best_move)

        return best


    def order_moves(self, moves, tt_move=None):
        def score(move):
            v = self.board.piece_at(move.to_square)
            a = self.board.piece_at(move.from_square)
            v_value = self.pieces[v.piece_type] if v else 100  # in case of en passant
            a_value = self.pieces[a.piece_type]
            return 100_000 + v_value * 10 - a_value

        captures = []
        inactive = []

        for move in moves:
            if move == tt_move:
                continue
            if self.board.is_capture(move):
                captures.append(move)

            else:
                inactive.append(move)
        captures.sort(key=score, reverse=True)
        if tt_move == None:
            return  captures + inactive

        return [tt_move] + captures + inactive





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





