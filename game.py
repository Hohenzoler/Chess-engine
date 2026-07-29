import chess
import pyray as rl
import TEXTURES

class Chess:
    def __init__(self):
        self.w = 800
        self.h = 600

        self.board_w = 600
        self.panel_w = self.w - self.board_w

        rl.init_window(self.w, self.h, 'Chess')
        rl.set_target_fps(60)


        self.board = chess.Board()

        self.textures = TEXTURES.load_textures()

        self.objects = []

        self.guiboard = Chessboard(0,0,self.board_w, self.h, self)

        self.mainloop()

    def mainloop(self):
        while not rl.window_should_close():
            self.render()
            self.handle_events()


    def handle_events(self):
        pass

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

        self.black_tile_color = (85, 52, 43, 255)
        self.white_tile_color = (209, 175, 132, 255)

        self.board = self.gui_object.board
        self.textures = self.gui_object.textures


        self.tile_w = self.width // 8
        self.tile_h = self.height // 8

        self.scale = self.tile_w/self.textures['P'].width

        self.font = rl.load_font('assets/fonts/MaidenOrange-Regular.ttf')
        self.font_size = self.tile_h // 4
    def render(self):
        for y in range(8):
            for x in range(8):
                y = 7-y
                if (x+y) % 2 == 0:
                    rl.draw_rectangle(self.x + x * self.tile_w, self.y + y * self.tile_h, self.tile_w, self.tile_h, self.white_tile_color)
                else:
                    rl.draw_rectangle(self.x + x * self.tile_w, self.y + y * self.tile_h, self.tile_w, self.tile_h, self.black_tile_color)


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

                square = chess.square(x, y)
                piece = self.board.piece_at(square)
                if piece != None:
                    rl.draw_texture_ex(self.textures[piece.symbol()],
                                       (self.x + x * self.tile_w, self.y + y * self.tile_h), 0, self.scale, rl.WHITE)



        super().render()
    def events(self):
        pass




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
    c = Chess()




