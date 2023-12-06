from pgzero.builtins import Actor, animate, keyboard, mouse, Rect

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

        self.button_sound_untouched = Actor('setting_scene/button_untouched')
        self.button_sound_touched = Actor('setting_scene/button_touched')
        self.button_sound_touched.x = self.button_sound_untouched.x = 300
        self.button_sound_touched.y = self.button_sound_untouched.y = 260
        self.is_button_sound_touched = False

        self.button_speed_add_untouched = Actor('setting_scene/button_adjust_untouched')
        self.button_speed_add_touched = Actor('setting_scene/button_adjust_touched')
        self.button_speed_add_touched.x = self.button_speed_add_untouched.x = 330
        self.button_speed_add_touched.y = self.button_speed_add_untouched.y = 320
        self.is_button_speed_add_touched = False
        self.button_speed_sub_untouched = Actor('setting_scene/button_adjust_untouched')
        self.button_speed_sub_touched = Actor('setting_scene/button_adjust_touched')
        self.button_speed_sub_touched.x = self.button_speed_sub_untouched.x = 330
        self.button_speed_sub_touched.y = self.button_speed_sub_untouched.y = 350
        self.is_button_speed_sub_touched = False
        self.speed_max = 5
        self.speed_min = 3
        self.speed_change = 0.2

        self.button_initperson_add_untouched = Actor('setting_scene/button_adjust_untouched')
        self.button_initperson_add_touched = Actor('setting_scene/button_adjust_touched')
        self.button_initperson_add_touched.x = self.button_initperson_add_untouched.x = 330
        self.button_initperson_add_touched.y = self.button_initperson_add_untouched.y = 410
        self.is_button_initperson_add_touched = False
        self.button_initperson_sub_untouched = Actor('setting_scene/button_adjust_untouched')
        self.button_initperson_sub_touched = Actor('setting_scene/button_adjust_touched')
        self.button_initperson_sub_touched.x = self.button_initperson_sub_untouched.x = 330
        self.button_initperson_sub_touched.y = self.button_initperson_sub_untouched.y = 440
        self.is_button_initperson_sub_touched = False
        self.initperson_max = 10
        self.initperson_min = 1
        self.initperson_change = 1

        self.speed, self.init_person_num, self.win_person_num, self.music, self.sound = load_params()

    def _internal_update(self):
        self.speed, self.init_person_num, self.win_person_num, self.music, self.sound = load_params()

    def draw(self, screen):
        self.background.draw()
        self.homeicon.draw()

        screen.draw.text('music:', (self.button_music_touched.x - 120, self.button_music_touched.y - 12),
                         fontsize=30, color=(0, 0, 127))
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

        screen.draw.text('sound:', (self.button_sound_touched.x - 120, self.button_sound_touched.y - 12),
                         fontsize=30, color=(0, 0, 127))
        if self.is_button_sound_touched:
            self.button_sound_touched.draw()
        else:
            self.button_sound_untouched.draw()
        if self.sound:
            screen.draw.text('on', (self.button_sound_touched.x - 13, self.button_sound_touched.y - 10),
                             fontsize=30, color=(0, 0, 100))
        else:
            screen.draw.text('off', (self.button_sound_touched.x - 16, self.button_sound_touched.y - 10),
                             fontsize=30, color=(0, 0, 100))

        screen.draw.text('speed:   ' + str(self.speed),
                         (self.button_speed_add_touched.x - 150, self.button_speed_add_touched.y + 8),
                         fontsize=30, color=(0, 0, 127))
        if not self.speed >= self.speed_max:
            if self.is_button_speed_add_touched:
                self.button_speed_add_touched.draw()
            else:
                self.button_speed_add_untouched.draw()
            screen.draw.text('+',
                             (self.button_speed_add_touched.x - 8, self.button_speed_add_touched.y - 15),
                             fontsize=40, color=(0, 0, 0))
        if not self.speed <= self.speed_min:
            if self.is_button_speed_sub_touched:
                self.button_speed_sub_touched.draw()
            else:
                self.button_speed_sub_untouched.draw()
            screen.draw.text('-',
                             (self.button_speed_sub_touched.x - 5, self.button_speed_sub_touched.y - 14),
                             fontsize=40, color=(0, 0, 0))

        screen.draw.text('initial:     ' + str(self.init_person_num),
                         (self.button_initperson_add_touched.x - 150, self.button_initperson_add_touched.y + 8),
                         fontsize=30, color=(0, 0, 127))
        if not self.init_person_num >= self.initperson_max:
            if self.is_button_initperson_add_touched:
                self.button_initperson_add_touched.draw()
            else:
                self.button_initperson_add_untouched.draw()
            screen.draw.text('+',
                             (self.button_initperson_add_touched.x - 8, self.button_initperson_add_touched.y - 15),
                             fontsize=40, color=(0, 0, 0))
        if not self.init_person_num <= self.initperson_min:
            if self.is_button_initperson_sub_touched:
                self.button_initperson_sub_touched.draw()
            else:
                self.button_initperson_sub_untouched.draw()
            screen.draw.text('-',
                             (self.button_initperson_sub_touched.x - 5, self.button_initperson_sub_touched.y - 14),
                             fontsize=40, color=(0, 0, 0))

    def on_mouse_move(self, pos, rel):
        if self.button_music_untouched.collidepoint(pos[0], pos[1]):
            self.is_button_music_touched = True
        else:
            self.is_button_music_touched = False
        
        if self.button_sound_untouched.collidepoint(pos[0], pos[1]):
            self.is_button_sound_touched = True
        else:
            self.is_button_sound_touched = False
        
        if self.button_speed_add_untouched.collidepoint(pos[0], pos[1]):
            self.is_button_speed_add_touched = True
        else:
            self.is_button_speed_add_touched = False
        
        if self.button_speed_sub_untouched.collidepoint(pos[0], pos[1]):
            self.is_button_speed_sub_touched = True
        else:
            self.is_button_speed_sub_touched = False

        if self.button_initperson_add_untouched.collidepoint(pos[0], pos[1]):
            self.is_button_initperson_add_touched = True
        else:
            self.is_button_initperson_add_touched = False

        if self.button_initperson_sub_untouched.collidepoint(pos[0], pos[1]):
            self.is_button_initperson_sub_touched = True
        else:
            self.is_button_initperson_sub_touched = False

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
        
        if self.button_sound_untouched.collidepoint(pos[0], pos[1]):
            with open(self.file_path, 'w') as f:
                sound = 0 if self.sound else 1
                new_dict = {"speed": self.speed,
                            "init_person_num": self.init_person_num,
                            "win_person_num": self.win_person_num,
                            "music": self.music,
                            "sound": sound}
                json.dump(new_dict, f)
            self._internal_update()
            return 'sound_off' if not sound else 'sound_on'

        if self.button_speed_add_untouched.collidepoint(pos[0], pos[1]):
            with open(self.file_path, 'w') as f:
                speed = round(self.speed + self.speed_change, 1) if self.speed < self.speed_max else self.speed
                new_dict = {"speed": speed,
                            "init_person_num": self.init_person_num,
                            "win_person_num": self.win_person_num,
                            "music": self.music,
                            "sound": self.sound}
                json.dump(new_dict, f)
            self._internal_update()
            return 'speed_add'

        if self.button_speed_sub_untouched.collidepoint(pos[0], pos[1]):
            with open(self.file_path, 'w') as f:
                speed = round(self.speed - self.speed_change, 1) if self.speed > self.speed_min else self.speed
                new_dict = {"speed": speed,
                            "init_person_num": self.init_person_num,
                            "win_person_num": self.win_person_num,
                            "music": self.music,
                            "sound": self.sound}
                json.dump(new_dict, f)
            self._internal_update()
            return 'speed_sub'

        if self.button_initperson_add_untouched.collidepoint(pos[0], pos[1]):
            with open(self.file_path, 'w') as f:
                init = self.init_person_num + self.initperson_change if self.init_person_num < self.initperson_max else self.init_person_num
                new_dict = {"speed": self.speed,
                            "init_person_num": init,
                            "win_person_num": self.win_person_num,
                            "music": self.music,
                            "sound": self.sound}
                json.dump(new_dict, f)
            self._internal_update()
            return 'speed_add'

        if self.button_initperson_sub_untouched.collidepoint(pos[0], pos[1]):
            with open(self.file_path, 'w') as f:
                init = self.init_person_num - self.initperson_change if self.init_person_num > self.initperson_min else self.init_person_num
                new_dict = {"speed": self.speed,
                            "init_person_num": init,
                            "win_person_num": self.win_person_num,
                            "music": self.music,
                            "sound": self.sound}
                json.dump(new_dict, f)
            self._internal_update()
            return 'speed_sub'

    def update(self):
        pass

