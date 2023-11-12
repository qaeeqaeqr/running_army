import json
import os

def load_params():
    file_path = './config/settings.json'
    if not os.path.exists(file_path):
        raise FileNotFoundError('Fetal error! No config file for game.')

    with open(file_path, 'r') as f:
        res = json.load(f)

    return res['speed'], res['init_person_num'], res['win_person_num'], res['music'], res['sound']

def process_music_switch(event, sounds):
    if event == 'music_off':
        sounds.game_music.stop()
    if event == 'music_on':
        sounds.game_music.play(-1)


