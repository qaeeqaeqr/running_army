from pgzero.builtins import Actor, animate, keyboard, mouse

from util import load_params
import json
import os

class Settings(object):
    def __init__(self):
        self.background = Actor('setting_scene/setting_background')
        self.homeicon = Actor('home_icon')
        self.file_path = './config/settings.json'

        self.button_music_untouched = Actor('setting_scene/button_untouched')
        self.button_music_touched = Actor('setting_scene/button_touched')
        self.button_music_touched.x = self.button_music_untouched.x = 300
        self.button_music_touched.y = self.button_music_untouched.y = 200
        self.is_button_music_touched = False

        self.speed, self.init_person_num, self.win_person_num, self.music, self.sound = load_params()

    def _internal_update(self):
        self.speed, self.init_person_num, self.win_person_num, self.music, self.sound = load_params()

    def draw(self, screen):
        self.background.draw()
        self.homeicon.draw()

        screen.draw.text('music:', (self.button_music_touched.x - 120, self.button_music_touched.y - 12),
                         fontsize=30)
        if self.is_button_music_touched:
            self.button_music_touched.draw()
        else:
            self.button_music_untouched.draw()

        if self.music:
            screen.draw.text('on', (self.button_music_touched.x - 13, self.button_music_touched.y - 10),
                             fontsize=30, color=(0, 0, 100))
        else:
            screen.draw.text('off', (self.button_music_touched.x - 16, self.button_music_touched.y - 10),
                             fontsize=30, color=(0, 0, 100))


    def on_mouse_move(self, pos, rel):
        if self.button_music_untouched.collidepoint(pos[0], pos[1]):
            self.is_button_music_touched = True
        else:
            self.is_button_music_touched = False

    def on_mouse_down(self, pos, button):
        if self.homeicon.collidepoint(pos[0], pos[1]) and button == mouse.LEFT:
            return 'main'

        if self.button_music_untouched.collidepoint(pos[0], pos[1]):
            with open(self.file_path, 'w') as f:
                music = 0 if self.music else 1
                new_dict = {"speed": self.speed,
                            "init_person_num": self.init_person_num,
                            "win_person_num": self.win_person_num,
                            "music": music,
                            "sound": self.sound}
                json.dump(new_dict, f)
            self._internal_update()
            return 'music_off' if not music else 'music_on'

    def update(self):
        pass

