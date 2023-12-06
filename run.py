import pgzrun
from game import Game
from Mainpage import Mainpage
from settings import Settings
from util import *

import json
import os

WIDTH = 400
HEIGHT = 600
TITLE = 'Game'

STATUS_metadata = ['mainpage', 'game', 'setting']
status = 0

speed, init_person_num, win_person_num, music0, sound = load_params()

mainpage = Mainpage()
game = Game(WIDTH, HEIGHT, speed,
            init_person_num, win_person_num)
setting = Settings()

if music0:
    sounds.game_music.play(-1)

def draw():
    if status == 0:
        mainpage.draw(screen)
    if status == 1:
        game.draw(screen)
    if status == 2:
        setting.draw(screen)

def on_mouse_move(pos, rel):
    if status == 0:
        mainpage.on_mouse_move(pos, rel)
    if status == 1:
        game.on_mouse_move(pos, rel)
    if status == 2:
        setting.on_mouse_move(pos, rel)

def on_mouse_down(pos, button):
    """
    这里实现各个页面之间的相互跳转。
    """
    global status, game, speed, init_person_num, win_person_num, music0, sound
    if status == 0:
        event = mainpage.on_mouse_down(pos, button)
        if event == 'start':
            status = 1
        if event == 'setting':
            status = 2
    if status == 1:
        event = game.on_mouse_down(pos, button)
        if event == 'main':
            status = 0
            game = Game(WIDTH, HEIGHT, speed, init_person_num, win_person_num)  # reset game
    if status == 2:
        event = setting.on_mouse_down(pos, button)
        if event == 'main':
            status = 0
        if event == 'music_off' or event == 'music_on':
            process_music_switch(event, sounds)
        if event == 'sound_off' or event == 'sound_on':
            pass
        if event == 'speed_add' or event == 'speed_sub':
            speed, init_person_num, win_person_num, music0, sound = load_params()
            game = Game(WIDTH, HEIGHT, speed, init_person_num, win_person_num)

def update():
    speed, init_person_num, win_person_num, music0, sound = load_params()
    if status == 1:
        game.update(music, should_play_sound=sound)
    if status == 2:
        setting.update()

pgzrun.go()
