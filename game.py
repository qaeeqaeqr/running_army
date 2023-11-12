from pgzero.builtins import Actor, animate, keyboard, mouse
import random
from src.door import Door
from src.player import Player
from src.trap import Trap1, Trap2
import time


class Game(object):
    def __init__(self, width, height, speed,
                 num_person, max_num_person):
        self.width = width
        self.height = height
        self.speed = speed
        self.bk = Actor('game_scene/game_background')
        self.road1 = Actor('game_scene/game_road')
        self.road2 = Actor('game_scene/game_road')
        self.win = Actor('game_scene/win')
        self.lose = Actor('game_scene/lose')
        self.win.x = self.lose.x = 200
        self.win.y = self.lose.y = 300
        self.is_win = 0
        self.is_lose = 0
        self.homeicon = Actor('home_icon')
        self.doors = []
        self.traps = []
        self.player = Player(200, 400, speed,
                             num_person=num_person, max_num_person=max_num_person)
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
        if 0 <= r <= 0.3:
            x = random.choice(list(range(110, 160)) + list(range(240, 290)))
            y = random.randint(-300, -100)
            self.traps.append(Trap1(x, y, self.speed))
        elif 0.3 < r <= 1:
            x = random.choice(list(range(140, 160)) + list(range(240, 260)))
            y = random.randint(-300, -100)
            self.traps.append(Trap2(x, y, self.speed))

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
        dist = random.randint(300, 800)
        if len(self.doors) <= 2:
            self.doors.append(Door(150, self.doors[-1].y - dist, self.speed))
            self.doors.append(Door(250, self.doors[-2].y - dist, self.speed))
        for i in range(len(self.doors)):
            self.doors[i].update()
        self.doors = [door for door in self.doors if door.y < self.height]

    def trap_update(self):
        if len(self.traps) <= 2:
            r = random.random()
            if 0 <= r <= 0.3:
                x = random.choice(list(range(110, 160)) + list(range(240, 290)))
                y_dist = random.randint(600, 1200)
                # 炸弹不能生成在门里
                while abs((self.traps[-1].y - y_dist) - self.doors[-1].y) < 200:
                    y_dist += 10
                self.traps.append(Trap1(x, self.traps[-1].y - y_dist, self.speed))
            elif 0.3 < r <= 1:
                x = random.choice(list(range(140, 160)) + list(range(240, 260)))
                y_dist = random.randint(600, 1200)
                # 火不能生成在门里，由于火很宽，需要和门保持一定距离
                while abs((self.traps[-1].y - y_dist) - self.doors[-1].y) < 300:
                    y_dist += 10
                self.traps.append(Trap2(x, self.traps[-1].y - y_dist, self.speed))

        for i in range(len(self.traps)):
            self.traps[i].update()
        self.traps = [trap for trap in self.traps if trap.y < self.height]

    def win_lose_update(self):
        if self.player.num_person >= 100:
            self.is_win = 1
        if self.player.num_person <= 0:
            self.is_lose = 1

    def detect_door_player(self):
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
                break

    def detect_trap_player(self):
        for i in range(len(self.traps)):
            if self.traps[i].__class__.__name__ == 'Trap1':
                # 更新炸弹状态
                if 50 < (self.player.y - self.player.up) - self.traps[i].bomb0.y < 90:
                    self.traps[i].status = 1
                if 0 < (self.player.y - self.player.up) - self.traps[i].bomb0.y <= 50:
                    self.traps[i].status = 2
                if (self.player.y - self.player.up) - self.traps[i].bomb0.y < 0:
                    self.traps[i].status = 3
                # 判断玩家人数变化
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
                self.player.on_person_change(-decrease)


    def draw(self, screen):
        self.bk.draw()
        self.road1.draw()
        self.road2.draw()
        self.homeicon.draw()
        for door in self.doors:
            door.draw(screen)
        for trap in self.traps:
            trap.draw()
        self.player.draw(screen)

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
        if self.homeicon.collidepoint(pos[0], pos[1]) and button == mouse.LEFT:
            return 'main'
        if (self.is_win or self.is_lose) and button == mouse.LEFT:
            return 'main'

    def update(self):
        self.win_lose_update()
        if self.is_win or self.is_lose:
            return
        self.road_update()
        self.door_update()
        self.trap_update()
        self.player.update()
        self.detect_door_player()
        self.detect_trap_player()

