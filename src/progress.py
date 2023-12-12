from pygame import Rect
from pgzero.builtins import Actor, animate, keyboard, mouse


class ProgressBar:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_value = 100
        self.value = 0

        self.delay = 8
        self.able_level_update = False
        self.is_level_update = False

        self.draw_text_timer = 0
        self.current_level = 1

    def update(self, timer, cur_level, enemy_pass):
        self.current_level = cur_level
        if timer % self.delay == 0:
            self.value = self.value + 1 if self.value < self.max_value else self.max_value
        if self.value == self.max_value and enemy_pass:
            self.able_level_update = True

        if self.is_level_update:
            self.is_level_update = False
            self.able_level_update = False
            self.value = 0
            self.delay -= 1

        self.draw_text_timer = (self.draw_text_timer + 1) % 25

    def on_mouse_down(self, pos, button):
        if self.able_level_update and button == mouse.RIGHT:
            self.is_level_update = True

    def draw(self, screen):
        progress_height = int(self.height * (self.value / self.max_value))
        progress_rect = Rect(self.x, self.y, self.width, self.height)
        progress_surface = Rect(self.x, self.y + self.height - progress_height, self.width, progress_height)
        screen.draw.filled_rect(progress_surface, (200, 100, 0))
        screen.draw.rect(progress_rect, (0, 0, 0))

        if self.able_level_update and self.draw_text_timer < 15:
            if self.current_level <= 5:
                screen.draw.text('press right button to enter next level!',
                                 (30, 50), fontsize=30)
            else:
                screen.draw.text('press right button to VECTORY!',
                                 (30, 50), fontsize=30)


