import pyray as rl



class DoubleScrollableContainer:
    def __init__(self, gui_object, x, y, w, h):
        self.rect = rl.Rectangle(x, y, w, h)

        self.section_width = self.rect.width // 2

        self.content_list = []
        self.font_height = 20
        self.padding = self.font_height//4
        self.content = rl.Rectangle(0, 0, self.rect.width - 20, (int(len(self.content_list)//2 + 1)*self.font_height))

        self.right_x = int(self.rect.x + self.section_width)

        self.scroll = rl.Vector2(0, 0)

        self.font = rl.get_font_default()

        self.view = rl.Rectangle(0, 0, 0, 0)

        if gui_object != None:
            self.gui_object = gui_object
            self.gui_object.objects.append(self)
            self.font = self.gui_object.font
            self.content_list = self.gui_object.history


    def render(self):

        rl.draw_rectangle(int(self.rect.x), int(self.rect.y), int(self.section_width), int(self.rect.height),
                          self.gui_object.black_tile_color)


        rl.draw_rectangle(self.right_x, int(self.rect.y), int(self.section_width), int(self.rect.height),
                          self.gui_object.white_tile_color)

        rl.draw_rectangle_lines_ex((int(self.rect.x), int(self.rect.y), int(self.rect.width), int(self.rect.height)),
                                   5,
                                   rl.GRAY)


        rl.begin_scissor_mode(int(self.view.x), int(self.view.y), int(self.view.width), int(self.view.height))

        base_y = self.view.y + self.scroll.y

        for i, t in enumerate(self.content_list):
            if i % 2 == 0:
                rl.draw_text_ex(self.font, f"{i//2 + 1}. {t}", (int(self.view.x) + self.padding*2, int(base_y + self.font_height * i + self.padding)), self.font_height, self.padding//2, self.gui_object.white_tile_color)
            else:
                rl.draw_text_ex(self.font, t, (self.right_x + self.padding, int(base_y + self.font_height * (i-1) + self.padding)), self.font_height, self.padding//2, self.gui_object.black_tile_color)



        rl.end_scissor_mode()

    def event(self):
        rl.gui_scroll_panel(self.rect, '', self.content, self.scroll, self.view)

    def update_moves(self):
        self.content = rl.Rectangle(0, 0, self.rect.width - 20,
                                    (int((len(self.content_list)-1) // 2 +1) * (self.font_height + self.padding * 4)))


if __name__ == '__main__':
    rl.init_window(800, 600, 'test')
    rl.set_target_fps(60)

    con = DoubleScrollableContainer(None, 0, 0, 200, 500)

    while not rl.window_should_close():
        con.event()
        rl.begin_drawing()
        rl.clear_background(rl.WHITE)

        con.render()

        rl.end_drawing()