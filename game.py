import math

from pgzero.builtins import Actor, animate, keyboard, mouse
import random
from src.door import Door
from src.player import Player
from src.enemy import Enemy
from src.trap import Trap1, Trap2, Trap3
from src.progress import ProgressBar
import time


class Game(object):
    def __init__(self, width, height, speed,
                 num_person, max_num_person):
        self.width = width
        self.height = height
        self.speed = speed
        self.bk_num = 0
        self.bk = Actor('game_scene/backgrounds/bg' + str(self.bk_num))
        self.road_num = 0
        self.road1 = Actor('game_scene/roads/r' + str(self.road_num))
        self.road2 = Actor('game_scene/roads/r' + str(self.road_num))
        self.progressbar = ProgressBar(350, 200, 20, 200)
        self.win = Actor('game_scene/win')
        self.lose = Actor('game_scene/lose')
        self.win.x = self.lose.x = 200
        self.win.y = self.lose.y = 300
        self.intogame = True  # 解决点击start进入游戏后自动发射一发子弹的bug
        self.is_win = 0
        self.is_lose = 0
        self.timer = 1  # 这里timer的单位1是pgzero执行一次update函数的时间
        self.level = 1
        self.homeicon = Actor('home_icon')
        self.doors = []
        self.traps = []
        self.score = 0  # 消灭boss获得的score
        self.bullets = []
        self.bullet_speed = self.speed * 2
        self.player = Player(200, 400, speed,
                             num_person=num_person, max_num_person=max_num_person)
        self.enemies = Enemy(200, 200, 3, 0)
        self.enemy_pass = False
        self.num_enemy_kill_player = 2
        self.create_enemy_this_level = False
        self.enemy_nums = [3, 6, 8, 10, 10]

        self.init_road()
        self.init_door()
        self.init_trap()


    def init_road(self):
        self.road1.x = self.width // 2
        self.road1.y = self.road1.height // 2
        self.road2.x = self.width // 2
        self.road2.y = -self.road2.height // 2

    def init_door(self):
        self.doors.append(Door(150, 0, self.speed))
        self.doors.append(Door(250, 0, self.speed))

    def init_trap(self):
        r = random.random()
        if 0 <= r <= 0.5:
            x = random.choice(list(range(110, 160)) + list(range(240, 290)))
            y = random.randint(-300, -100)
            self.traps.append(Trap1(x, y, self.speed))
        elif 0.5 < r <= 0.8:
            x = random.choice(list(range(140, 160)) + list(range(240, 260)))
            y = random.randint(-300, -100)
            self.traps.append(Trap2(x, y, self.speed))
        elif 0.8 < r <= 1:
            x = random.choice(list(range(140, 160)) + list(range(240, 260)))
            y = random.randint(-300, -100)
            self.traps.append(Trap3(x, y, self.speed))

    def road_update(self):
        # 实现背景移动
        if self.road1.y > self.road1.height / 2 + self.road1.height:
            self.road1.y = -self.road1.height / 2 + 25
        if self.road2.y > self.road2.height / 2 + self.road2.height:
            self.road2.y = -self.road2.height / 2 + 25
        self.road1.y += self.speed
        self.road2.y += self.speed

    def door_update(self):
        # 随机在地图上方产生门，并更新门位置，并删除已经从地图中消失的门
        dist = random.randint(200, 900)
        if len(self.doors) <= 2:
            self.doors.append(Door(150, self.doors[-1].y - dist, self.speed))
            self.doors.append(Door(250, self.doors[-2].y - dist, self.speed))
        for i in range(len(self.doors)):
            self.doors[i].update()
        self.doors = [door for door in self.doors if door.y < self.height]

    def trap_update(self):
        if len(self.traps) <= 2:
            r = random.random()
            if 0 <= r <= 0.4:
                x = random.choice(list(range(110, 160)) + list(range(240, 290)))
                y_dist = random.randint(600, 1200)
                # 炸弹不能生成在门里
                while abs((self.traps[-1].y - y_dist) - self.doors[-1].y) < 200:
                    y_dist += 10
                self.traps.append(Trap1(x, self.traps[-1].y - y_dist, self.speed))
            elif 0.4 < r <= 0.6:
                x = random.choice(list(range(140, 160)) + list(range(240, 260)))
                y_dist = random.randint(600, 1200)
                # 火不能生成在门里，由于火很宽，需要和门保持一定距离
                while abs((self.traps[-1].y - y_dist) - self.doors[-1].y) < 300:
                    y_dist += 10
                self.traps.append(Trap2(x, self.traps[-1].y - y_dist, self.speed))
            elif 0.6 <= r <= 1:
                x = random.choice(list(range(140, 160)) + list(range(240, 260)))
                y_dist = random.randint(600, 1200)
                self.traps.append(Trap3(x, self.traps[-1].y - y_dist, self.speed))

        for i in range(len(self.traps)):
            self.traps[i].update()
        self.traps = [trap for trap in self.traps if trap.y < self.height]

    def bullet_update(self):
        for bullet in self.bullets:
            bullet.y -= self.bullet_speed
            if bullet.y <= 0:
                self.bullets.remove(bullet)

    def enemies_update(self):
        if self.progressbar.value == self.progressbar.max_value and not self.create_enemy_this_level:
            self.enemies = Enemy(200, 100, 6, self.enemy_nums[self.level-1])
            self.create_enemy_this_level = True

        self.enemies.update(self.player.x, self.player.y)


    def level_update(self, is_level_update):
        def no_enemy_in_screen():
            for enemy in self.enemies.enemies:
                if 0 < enemy.x < 450:
                    return False
            return True
        if self.create_enemy_this_level and (len(self.enemies.enemies) == 0 or no_enemy_in_screen()):
            self.enemy_pass = True
        if not is_level_update:
            return

        self.level += 1
        self.create_enemy_this_level = False
        self.enemy_pass = False
        if self.level > 5:
            self.is_win = True
            return

        self.player.update_skin()
        self.bk_num = (self.bk_num + 1) % 5
        self.bk = Actor('game_scene/backgrounds/bg' + str(self.bk_num))
        self.road_num = (self.road_num + 1) % 5
        self.road1 = Actor('game_scene/roads/r' + str(self.road_num))
        self.road2 = Actor('game_scene/roads/r' + str(self.road_num))
        self.init_road()

        self.speed += math.log(self.level + 1, 2) / 1.5
        for door in self.doors:
            door.speed = self.speed
        for trap in self.traps:
            trap.speed = self.speed


    def win_lose_update(self):
        # if self.player.num_person >= 100:
        #     self.is_win = 1
        if self.player.num_person <= 0:
            self.is_lose = 1

    def detect_door_player(self, music, should_play_sound):
        # 判断门和人物是否碰撞。若碰撞，改变人数，设置并排的两个门不能再碰撞。
        for i in range(len(self.doors)):
            if self.doors[i].door.collidepoint(self.player.x, self.player.y) and not self.doors[i].player_through:
                self.doors[i].player_through = True
                if i % 2 == 0:
                    self.doors[i + 1].player_through = True
                else:
                    self.doors[i - 1].player_through = True
                change = self.doors[i].calculate(self.player.num_person) - self.player.num_person
                self.player.on_person_change(change)
                if should_play_sound:
                    music.play_once('door_sound')
                break

    def detect_trap_player(self, music, should_play_sound):
        for i in range(len(self.traps)):
            if self.traps[i].__class__.__name__ == 'Trap1':
                # 更新炸弹状态
                if 50 < (self.player.y - self.player.up) - self.traps[i].bomb0.y < 90:
                    self.traps[i].status = 1
                    if should_play_sound:
                        music.play_once('boom_sound')
                if 0 < (self.player.y - self.player.up) - self.traps[i].bomb0.y <= 50:
                    self.traps[i].status = 2
                if (self.player.y - self.player.up) - self.traps[i].bomb0.y < 0:
                    self.traps[i].status = 3

                # 判断玩家人数变化
                if self.traps[i].status == 0 or self.traps[i].status == 3:  # 防止炸弹爆炸后仍然能伤害玩家
                    continue
                decrease = 0
                for person in self.player.persons:
                    if person.person.colliderect(self.traps[i].bomb0):
                        decrease += 1
                self.player.on_person_change(-decrease)

            if self.traps[i].__class__.__name__ == 'Trap2':
                decrease = 0
                for person in self.player.persons:
                    if person.person.colliderect(self.traps[i].fire0):
                        decrease += 1
                if decrease and should_play_sound:
                    music.play_once('fire_sound')
                self.player.on_person_change(-decrease)

            if self.traps[i].__class__.__name__ == 'Trap3':
                decrease = 0
                for person in self.player.persons:
                    if person.person.colliderect(self.traps[i].boss):
                        decrease += 1
                if decrease and should_play_sound:
                    music.play_once('fire_sound')
                self.player.on_person_change(-decrease)

    def detect_enemy_player(self, music, should_play_sound):
        person_decrease = 0
        for enemy in self.enemies.enemies:
            for person in self.player.persons:
                if person.person.colliderect(enemy.enemy):
                    person_decrease += self.num_enemy_kill_player
                    self.enemies.enemies.remove(enemy)
                    break
        if person_decrease and should_play_sound:
            music.play_once('enemy_kill_sound')
        self.player.on_person_change(-person_decrease)

    def detect_boss_bullet(self, music, should_play_sound):
        for trap in self.traps:
            if not trap.__class__.__name__ == 'Trap3':
                continue

            for bullet in self.bullets:
                if bullet.colliderect(trap.boss):
                    self.bullets.remove(bullet)
                    trap.life -= 1
            if trap.life <= 0:
                self.traps.remove(trap)
                self.score += 1
                if should_play_sound:
                    music.play_once('boss_blow_sound')

    def shoot(self):
        if not self.intogame:
            bullet = Actor('game_scene/bullet')
            bullet.x = self.player.x
            bullet.y = self.player.y
            self.bullets.append(bullet)

    def show_info(self, screen):
        screen.draw.text('level: ' + str(self.level), (10, 100), fontsize=30, color=(255, 0, 0))
        screen.draw.text('score: ' + str(self.score), (10, 140), fontsize=30, color=(0, 255, 0))
        screen.draw.text('hero: ', (10, 200), fontsize=30, color=(0, 0, 255))
        if len(self.player.persons) > 0:
            self.player.persons[0].front_person.x = 30
            self.player.persons[0].front_person.y = 250
            self.player.persons[0].front_person.draw()
        else:
            loss_face = Actor('game_scene/loss_front_person')
            loss_face.x = 30
            loss_face.y = 250
            loss_face.draw()

    def draw(self, screen):
        self.bk.draw()
        self.road1.draw()
        self.road2.draw()
        self.homeicon.draw()
        self.progressbar.draw(screen)
        for door in self.doors:
            door.draw(screen)
        for trap in self.traps:
            trap.draw()
        for bullet in self.bullets:
            bullet.draw()
        self.player.draw(screen)
        self.enemies.draw()

        self.show_info(screen)

        if self.is_win:
            self.win.draw()
            screen.draw.text('Click left button to return to homepage.', (10, 380), fontsize=30)
        if self.is_lose:
            self.lose.draw()
            screen.draw.text('Click left button to return to homepage.', (10, 380), fontsize=30)

    def on_mouse_move(self, pos, rel):
        # 先确定人物可以移动的范围（最左侧、右侧人物不到道路外面）
        road_left, road_right = self.width // 2 - self.road1.width // 2, self.width // 2 + self.road1.width // 2
        left_bound, right_bound = road_left + self.player.left, road_right - self.player.right
        if not self.is_lose and not self.is_win:
            self.player.on_mouse_move(pos, rel, left_bound, right_bound)

    def on_mouse_down(self, pos, button):
        self.progressbar.on_mouse_down(pos, button)
        if self.homeicon.collidepoint(pos[0], pos[1]) and button == mouse.LEFT:
            return 'main'
        if (self.is_win or self.is_lose) and button == mouse.LEFT:
            return 'main'
        if not self.homeicon.collidepoint(pos[0], pos[1]) and button == mouse.LEFT:
            self.shoot()

    def update(self, music, should_play_sound):
        self.win_lose_update()
        self.road_update()
        self.door_update()
        self.trap_update()
        if self.is_win or self.is_lose:
            return
        self.level_update(self.progressbar.is_level_update)
        self.progressbar.update(self.timer, self.level, self.enemy_pass)
        self.bullet_update()
        self.player.update()
        self.enemies_update()
        self.intogame = False
        self.detect_boss_bullet(music, should_play_sound)
        self.detect_door_player(music, should_play_sound)
        self.detect_trap_player(music, should_play_sound)
        self.detect_enemy_player(music, should_play_sound)
        self.timer += 1


