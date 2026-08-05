import chess
import chess.polyglot
import time
from PST import PST

class TimeoutException(Exception):
    pass


class engine:
    def __init__(self, board):
        self.board = board
        self.depth = 100
        self.tt = {} # zobrist_hash
        self.Exact_tt = 0
        self.Upper_tt = 1
        self.Lower_tt = 2
        self.mate_score = 999999999999999
        self.nodes = 0
        self.qnodes = 0
        self.time_limit = 10.0
        self.time_start = 0

        self.inf = 999999999999999999999999999999


        self.pieces = {chess.QUEEN: 900, chess.ROOK: 500, chess.BISHOP: 300, chess.KNIGHT: 280, chess.PAWN: 100, chess.KING: 0}


    def check_time(self):
        if (self.nodes+self.qnodes) & 2047 == 0:
            if time.time() - self.time_start >= self.time_limit:
                raise TimeoutException()


    def evaluate(self):
        eval = 0
        white_eval = 0
        black_eval = 0

        for piece_type, value in self.pieces.items():
            table = PST[piece_type]

            for sq in self.board.pieces(piece_type, chess.WHITE):
                white_eval += value + table[chess.square_mirror(sq)]

            for sq in self.board.pieces(piece_type, chess.BLACK):
                black_eval += value + table[sq]

        eval = white_eval - black_eval

        if self.board.turn == chess.BLACK:
            return -eval
        return eval


    def negamax(self, depth, alpha, beta, ply=0):
        self.check_time()
        self.nodes += 1

        if depth == 0:
            return self.quiescence(alpha, beta)
            # return self.evaluate()

        # Transpositional Table

        original_alpha = alpha
        key = self.board._transposition_key()
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


        moves = list(self.board.legal_moves)
        if not moves:
            if self.board.is_check():
                return -self.mate_score + ply
            return 0

        moves = self.order_moves(moves, tt_move)

        best = -self.inf
        best_move = None
        for move in moves:
            self.board.push(move)
            score = -self.negamax(depth - 1, -beta, -alpha, ply+1)
            self.board.pop()
            if score > best:
                best = score
                best_move = move
            alpha = max(alpha, score)
            if alpha >= beta:
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
            v = self.board.piece_type_at(move.to_square)
            a = self.board.piece_type_at(move.from_square)
            v_value = self.pieces[v] if v else 100  # in case of en passant
            a_value = self.pieces[a]
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

    def quiescence(self, alpha, beta):
        self.check_time()
        self.qnodes += 1
        original_alpha = alpha
        key = self.board._transposition_key()
        tt_entry = self.tt.get(key)

        if tt_entry is not None and tt_entry[0] == 0:
            tt_depth, tt_score, tt_flag, tt_move = tt_entry
            if tt_flag == self.Exact_tt:
                return tt_score
            elif tt_flag == self.Lower_tt:
                alpha = max(alpha, tt_score)
            elif tt_flag == self.Upper_tt:
                beta = min(beta, tt_score)

            if alpha >= beta:
                return tt_score




        moves = self.order_moves(list(self.board.legal_moves))
        if self.board.is_check():
            if not moves:
                return -self.mate_score

            for move in moves:
                self.board.push(move)
                score = -self.quiescence(-beta, -alpha)
                self.board.pop()

                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score

            return alpha

        cur_eval = self.evaluate()
        if cur_eval >= beta:
            return beta
        if cur_eval > alpha:
            alpha = cur_eval

        moves = [move for move in moves if self.board.is_capture(move) or move.promotion is not None]

        for move in moves:
            if self.board.is_capture(move):
                v = self.board.piece_type_at(move.to_square)
                if v is None:
                    v_value = self.pieces[chess.PAWN]
                else:
                    v_value = self.pieces[v]

                if cur_eval + v_value < alpha:
                    continue

            self.board.push(move)
            score = -self.quiescence(-beta, -alpha)
            self.board.pop()

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score

        flag = self.Exact_tt
        score = alpha
        if score <= original_alpha:
            flag = self.Upper_tt
        elif score >= beta:
            flag = self.Lower_tt

        # avoid mate breaking tt
        if abs(score) < self.mate_score - 1000:
            self.tt[key] = (0, score, flag, None)



        return score


    def get_move(self):
        # best_move = None
        # best_score = -self.inf
        # for move in self.order_moves(self.board.legal_moves):
        #     self.board.push(move)
        #     score = -self.negamax(self.depth - 1, -self.inf, self.inf)
        #     self.board.pop()
        #     if score > best_score:
        #         best_score = score
        #         best_move = move
        # print(self.nodes, self.qnodes)
        # return best_move
        self.time_start = time.time()


        best_overall_move = None
        best_overall_score = -self.inf

        for depth in range(1, self.depth+1):
            self.nodes = 0
            self.qnodes = 0


            depth_best_move = None
            depth_best_score = -self.inf
            root_key = self.board._transposition_key()
            tt_move = self.tt.get(root_key, (None, None, None, None))[3]
            initial_len = len((self.board.move_stack))

            moves = self.order_moves(list(self.board.legal_moves), tt_move)

            try:
                for move in moves:
                    self.board.push(move)
                    score = -self.negamax(depth - 1, -self.inf, self.inf)
                    self.board.pop()

                    if score > depth_best_score:
                        depth_best_score = score
                        depth_best_move = move
                best_overall_move = depth_best_move
                best_overall_score = depth_best_score
                self.tt[root_key] = (depth, depth_best_score, self.Exact_tt, depth_best_move)

                elapsed = time.time() - self.time_start
                print(f'depth {depth} | score {best_overall_score} | nodes {self.nodes} | qnodes {self.qnodes} | time {elapsed:.2}s | move {best_overall_move}')
            except:
                while len(self.board.move_stack) > initial_len:
                    self.board.pop()


        return best_overall_move





