from pgzero.builtins import Actor, animate, keyboard, mouse


class Mainpage(object):
    def __init__(self):
        self.background = Actor('mainpage_background')

        self.button_start_untouched = Actor('button_untouched')
        self.button_start_touched = Actor('button_touched')
        self.button_start_untouched.x = self.button_start_touched.x = 200
        self.button_start_untouched.y = self.button_start_touched.y = 320
        self.is_button_start_touch = False

        self.button_setting_untouched = Actor('button_untouched')
        self.button_setting_touched = Actor('button_touched')
        self.button_setting_untouched.x = self.button_setting_touched.x = 200
        self.button_setting_untouched.y = self.button_setting_touched.y = 420
        self.is_button_setting_touch = False

    def draw(self, screen):
        self.background.draw()

        if self.is_button_start_touch:
            self.button_start_touched.draw()
        else:
            self.button_start_untouched.draw()
        screen.draw.text('Start', (self.button_start_touched.x - 42, self.button_start_touched.y - 16),
                         fontsize=50, color=(20, 220, 20))

        if self.is_button_setting_touch:
            self.button_setting_touched.draw()
        else:
            self.button_setting_untouched.draw()
        screen.draw.text('Setting', (self.button_setting_touched.x - 63, self.button_setting_touched.y - 16),
                         fontsize=50, color=(20, 220, 20))

    def on_mouse_move(self, pos, rel):
        if self.button_start_untouched.collidepoint(pos[0], pos[1]):
            self.is_button_start_touch = True
        else:
            self.is_button_start_touch = False

        if self.button_setting_untouched.collidepoint(pos[0], pos[1]):
            self.is_button_setting_touch = True
        else:
            self.is_button_setting_touch = False

    def on_mouse_down(self, pos, button):
        if self.button_start_untouched.collidepoint(pos[0], pos[1]) and button == mouse.LEFT:
            return 'start'
        if self.button_setting_untouched.collidepoint(pos[0], pos[1]) and button == mouse.LEFT:
            return 'setting'

        return None
