from pgzero.builtins import Actor, animate, keyboard
import random


class Enemy_single(object):
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

        self.img_names = ['enemy/0', 'enemy/1', 'enemy/2', 'enemy/3']
        self.current_img = 0
        self.delay_times = 6
        self.enemy = Actor(self.img_names[self.current_img])

    def draw(self):
        self.enemy.draw()

    def update(self, x, y):
        self.current_img = (self.current_img + 1) % (len(self.img_names) * self.delay_times)
        self.enemy = Actor(self.img_names[self.current_img // self.delay_times])

        x_dist = x - self.x
        y_dist = y - self.y
        x_dist = 1 if x_dist == 0 else x_dist
        y_dist = 1 if y_dist == 0 else y_dist
        x_speed = self.speed * x_dist / (x_dist + y_dist)
        y_speed = self.speed * y_dist / (x_dist + y_dist) / 2
        self.x = self.x + x_speed
        self.y = self.y + y_speed

        self.enemy.x = self.x
        self.enemy.y = self.y



class Enemy(object):
    def __init__(self, x, y, speed, num_enemy):
        self.x = x
        self.y = y
        self.speed = speed
        self.num_enemy = num_enemy
        self.enemies = []
        self.enemies_pos = []
        self.left = 0  # 最左侧人物到中心人物（x，y）之间的距离
        self.right = 0

        self.distance_between_enemies = 12
        self.arrangement = arrangement = [[121, 120, 119, 118, 117, 116, 115, 114, 113, 112, 111],
                                          [82, 81, 80, 79, 78, 77, 76, 75, 74, 73, 110],
                                          [83, 50, 49, 48, 47, 46, 45, 44, 43, 72, 109],
                                          [84, 51, 26, 25, 24, 23, 22, 21, 42, 71, 108],
                                          [85, 52, 27, 10, 9, 8, 7, 20, 41, 70, 107],
                                          [86, 53, 28, 11, 2, 1, 6, 19, 40, 69, 106],
                                          [87, 54, 29, 12, 3, 4, 5, 18, 39, 68, 105],
                                          [88, 55, 30, 13, 14, 15, 16, 17, 38, 67, 104],
                                          [89, 56, 31, 32, 33, 34, 35, 36, 37, 66, 103],
                                          [90, 57, 58, 59, 60, 61, 62, 63, 64, 65, 102],
                                          [91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101]]
        self.init_enemies()

    def init_enemies(self):
        # initialize enemies position (randomly)
        for i in range(self.num_enemy):
            pos = random.randint(1, 121)
            while pos in self.enemies_pos:
                pos = random.randint(1, 121)
            self.enemies_pos.append(pos)

        for i in range(self.num_enemy):
            for row in range(11):
                for col in range(11):
                    if self.arrangement[row][col] == self.enemies_pos[i]:
                        dist_from_center_x = col - 5
                        dist_from_center_y = row - 5
                        break
            self.enemies.append(Enemy_single(self.x + dist_from_center_x * self.distance_between_enemies,
                                             self.y + dist_from_center_y * self.distance_between_enemies,
                                             speed=self.speed))

    def draw(self):
        for enemy in self.enemies:
            enemy.draw()

    def update(self, x, y):
        """
        敌人的目标应该是朝着玩家移动。
        :param x:  玩家x
        :param y:  玩家y
        :return:
        """
        for i in range(len(self.enemies)):
            self.enemies[i].update(x, y)





