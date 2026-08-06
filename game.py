import chess
import pyray as rl

import TEXTURES
from container import DoubleScrollableContainer
from engine import engine

class Chess:
    def __init__(self, Player):
        self.w = 1000
        self.h = 600

        self.Player = Player

        self.board_w = self.h
        self.panel_w = self.w - self.board_w

        rl.init_window(self.w, self.h, 'Chess')
        rl.set_target_fps(60)

        self.black_tile_color = (85, 52, 43, 255)
        self.white_tile_color = (209, 175, 132, 255)

        self.board = chess.Board()
        self.engine = engine(self.board)

        self.textures = TEXTURES.load_textures()

        self.font = rl.load_font('assets/fonts/MaidenOrange-Regular.ttf')

        self.objects = []
        self.history = []

        self.guiboard = Chessboard(0,0,self.board_w, self.h, self)
        self.move_list =  DoubleScrollableContainer(self, self.board_w, 0,  self.w - self.board_w, self.h)

        self.handle_events()
        self.render()

        if self.board.turn != self.Player:
            move = self.engine.get_move()
            self.guiboard.push_move(move)

        self.mainloop()

    def mainloop(self):
        while not rl.window_should_close():
            self.handle_events()
            self.render()



    def handle_events(self):
        if rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
            self.guiboard.handle_mouse_click(rl.get_mouse_position())

        self.move_list.event()

    def render(self):
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)
        for o in self.objects:
            o.render()

        rl.end_drawing()


class Display:
    def __init__(self, x, y, w, h, gui_object, bg_color=rl.GRAY):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.bg_color = bg_color
        self.gui_object = gui_object
        self.gui_object.objects.append(self)

        self.objects = []

    def render(self):
        # rl.draw_rectangle(self.x, self.y, self.width, self.height, self.bg_color)
        for o in self.objects:
            o.render()


class Chessboard(Display):
    def __init__(self, x, y, w, h, gui_object, bg_color=rl.GRAY):
        Display.__init__(self, x, y, w, h, gui_object, bg_color)

        self.black_tile_color = self.gui_object.black_tile_color
        self.white_tile_color = self.gui_object.white_tile_color
        self.move_color = (144, 238, 144, 255)
        self.promotion_background = (26,26,26,230)

        self.legal_moves_highlighted = []
        self.selected_piece = (None, None)

        self.board = self.gui_object.board
        self.textures = self.gui_object.textures


        self.highlighted_sq_1 = (None, None)
        self.highlighted_sq_2 = (None, None)
        self.played_color = (57,255,50,255)


        self.promotion = False

        self.tile_w = self.width // 8
        self.tile_h = self.height // 8

        self.scale = self.tile_w/self.textures['P'].width

        self.font = self.gui_object.font
        self.font_size = self.tile_h // 4
    def render(self):
        for y in range(8):
            for x in range(8):

                if x == self.highlighted_sq_1[0] and y == self.highlighted_sq_1[1]:
                    print('sq1')
                    rl.draw_rectangle(self.x + x * self.tile_w, self.y + y * self.tile_h, self.tile_w, self.tile_h,
                                      self.played_color)


                elif x == self.highlighted_sq_2[0] and y == self.highlighted_sq_2[1]:
                    print('sq2')
                    rl.draw_rectangle(self.x + x * self.tile_w, self.y + y * self.tile_h, self.tile_w, self.tile_h,
                                      self.played_color)


                elif (x + y) % 2 == 0:
                    rl.draw_rectangle(self.x + x * self.tile_w, self.y + y * self.tile_h, self.tile_w, self.tile_h,
                                      self.white_tile_color)
                else:
                    rl.draw_rectangle(self.x + x * self.tile_w, self.y + y * self.tile_h, self.tile_w, self.tile_h,
                                      self.black_tile_color)




                if x == 0:
                    if y % 2 == 1:
                        color = self.white_tile_color
                    else:
                        color = self.black_tile_color

                    rl.draw_text_ex(self.font, f'{8-y}', (self.x + x * self.tile_w + self.tile_w//16, self.y + y * self.tile_h + self.tile_h//16), self.font_size,0, color)

                if y == 7:
                    if x % 2 == 0:
                        color = self.white_tile_color
                    else:
                        color = self.black_tile_color

                    rl.draw_text_ex(self.font, f'{chr(x + 97)}', (self.x + x * self.tile_w + self.tile_w * (15/16) - self.font_size//2, self.y + y * self.tile_h + self.tile_h//16 + self.tile_h * (15/16) - self.font_size//1.2), self.font_size,0, color)




                square = chess.square(x, 7 - y)
                piece = self.board.piece_at(square)
                if piece != None:
                    # print(piece.symbol())
                    rl.draw_texture_ex(self.textures[piece.symbol()],
                                       (self.x + x * self.tile_w, self.y + y * self.tile_h), 0, self.scale, rl.WHITE)

                if (x, y) in self.legal_moves_highlighted:
                    rl.draw_circle(self.x + x * self.tile_w + self.tile_w//2, self.y + y * self.tile_h + self.tile_h//2, self.tile_w//5, self.move_color)










        if self.promotion:
            rl.draw_rectangle(self.x + 3*self.tile_w, self.y + 3 * self.tile_h, self.tile_w * 2, self.tile_h * 2, self.promotion_background)
            pos = rl.get_mouse_position()
            mx, my = pos.x, pos.y

            if (int(mx//self.tile_w), int(my//self.tile_h)) in ((3,3), (3,4), (4,3), (4,4)):
                rl.draw_rectangle_lines(self.x + int(mx//self.tile_w) * self.tile_w, self.y + int(my//self.tile_h) * self.tile_h, self.tile_w, self.tile_h, self.move_color)


            if self.board.turn:
                rl.draw_texture_ex(self.textures["Q"],
                                   (self.x + 3 * self.tile_w, self.y + 3 * self.tile_h), 0, self.scale, rl.WHITE)
                rl.draw_texture_ex(self.textures["N"],
                                   (self.x + 4 * self.tile_w, self.y + 3 * self.tile_h), 0, self.scale, rl.WHITE)
                rl.draw_texture_ex(self.textures["B"],
                                   (self.x + 3 * self.tile_w, self.y + 4 * self.tile_h), 0, self.scale, rl.WHITE)
                rl.draw_texture_ex(self.textures["R"],
                                   (self.x + 4 * self.tile_w, self.y + 4 * self.tile_h), 0, self.scale, rl.WHITE)
            else:
                rl.draw_texture_ex(self.textures["q"],
                                   (self.x + 3 * self.tile_w, self.y + 3 * self.tile_h), 0, self.scale, rl.WHITE)
                rl.draw_texture_ex(self.textures["n"],
                                   (self.x + 4 * self.tile_w, self.y + 3 * self.tile_h), 0, self.scale, rl.WHITE)
                rl.draw_texture_ex(self.textures["b"],
                                   (self.x + 3 * self.tile_w, self.y + 4 * self.tile_h), 0, self.scale, rl.WHITE)
                rl.draw_texture_ex(self.textures["r"],
                                   (self.x + 4 * self.tile_w, self.y + 4 * self.tile_h), 0, self.scale, rl.WHITE)




        super().render()
    def handle_mouse_click(self, pos):
        x = pos.x
        y = pos.y

        if x >= 0 and x <= self.width and y >= 0 and y <= self.height:
            if not self.promotion:
                square_to_check = chess.square(int(x//self.tile_w), 7 - int(y//self.tile_h))

                if (int(x // self.tile_w), int(y // self.tile_h)) in self.legal_moves_highlighted:

                    square_to_move_from = chess.square(int(self.selected_piece[0]), int(self.selected_piece[1]))
                    if ((int(y // self.tile_h)) == 0 or int(y // self.tile_h) == 7) and self.board.piece_type_at(square_to_move_from) == chess.PAWN:

                        self.promotion = True
                        self.promotion_to_square = chess.square(int(x // self.tile_w), 7 - int(y // self.tile_h))

                    else:
                        legal_moves_finder = list(self.board.generate_legal_moves(from_mask=chess.BB_SQUARES[square_to_move_from]))
                        for m in legal_moves_finder:
                            if 7 - chess.square_rank(m.to_square) == int(y // self.tile_h) and chess.square_file(
                                    m.to_square) == int(x // self.tile_w):
                                self.push_move(m)
                                break

                else:
                    if (int(x // self.tile_w), 7 - int(y // self.tile_h)) == self.selected_piece:

                        self.selected_piece = (None, None)
                        self.legal_moves_highlighted = []

                    else:
                        legal_moves_check = [move for move in self.board.legal_moves if move.from_square == square_to_check]
                        if len(legal_moves_check) > 0:
                            self.selected_piece = (x//self.tile_w, 7 - y//self.tile_h)
                            self.legal_moves_highlighted = []
                            for m in legal_moves_check:
                                y = chess.square_rank(m.to_square)

                                x = chess.square_file(m.to_square)

                                self.legal_moves_highlighted.append((x, 7 - y))

            else:
                x1, y1 = int(x // self.tile_w), int(y // self.tile_h)
                move = 0
                if x1 == 3 and y1 == 3:
                    move = chess.Move(chess.square(int(self.selected_piece[0]), int(self.selected_piece[1])), self.promotion_to_square, promotion=chess.QUEEN)

                elif x1 == 4 and y1 == 3:
                    move = chess.Move(chess.square(int(self.selected_piece[0]), int(self.selected_piece[1])), self.promotion_to_square, promotion=chess.KNIGHT)

                elif x1 == 3 and y1 == 4:
                    move = chess.Move(chess.square(int(self.selected_piece[0]), int(self.selected_piece[1])), self.promotion_to_square, promotion=chess.BISHOP)

                elif x1 == 4 and y1 == 4:
                    move = chess.Move(chess.square(int(self.selected_piece[0]), int(self.selected_piece[1])), self.promotion_to_square, promotion=chess.ROOK)

                if move != 0:
                    self.push_move(move)


    def push_move(self, move):
        san = self.board.san(move)

        self.highlighted_sq_1 = (move.to_square%8, 7 - move.to_square//8)
        self.highlighted_sq_2 = (move.from_square%8, 7 - move.from_square//8)


        self.board.push(move)
        if self.promotion:
            self.promotion = False
        self.selected_piece = (None, None)
        self.legal_moves_highlighted = []
        self.gui_object.history.append(san)
        self.gui_object.move_list.update_moves()

        if self.board.turn != self.gui_object.Player:
            move = self.gui_object.engine.get_move()
            self.push_move(move)




class Text:
    def __init__(self, x, y, font_size, color, text, gui_object):
        self.x = x
        self.y = y
        self.font_size = font_size
        self.color = color
        self.text = text
        self.width = rl.measure_text(self.text, self.font_size)
        self.gui_object = gui_object
        self.gui_object.objects.append(self)

    def render(self):
        rl.draw_text(self.text, self.x - self.width//2, self.y - self.font_size//2, self.font_size, self.color)

    def change_text(self, text, font_size=None):
        self.text = text

        if font_size != None:
            self.font_size = font_size
        self.width = rl.measure_text(self.text, self.font_size)






if __name__ == '__main__':
    c = Chess(0)




