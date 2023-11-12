from pgzero.builtins import Actor, animate, keyboard
import random


class Door(object):
    def __init__(self, x, y, speed):
        """

        :param speed:
        :param x: should be one of (150, 250)
        :param y:
        """
        self.speed = speed
        self.x = x
        self.y = y
        self.door = Actor('game_scene/door')
        # op和num构成门的功能：加减乘除及相应系数
        self.op = ''
        self.num = 0
        self.random_function()

        self.player_through = False

    def random_function(self):
        """
        x: 人数
        关键代码，门随机生成加减乘除及数字。要控制比例，不能减或除太多。
        """
        r = random.random()
        if 0 <= r <= 0.25:
            self.op = '×'
            r_mult = random.random()
            if 0 <= r_mult <= 0.3:
                self.num = 2
            elif 0.3 < r_mult <= 0.6:
                self.num = 3
            elif 0.6 < r_mult <= 0.85:
                self.num = 4
            elif 0.85 < r_mult <= 1:
                self.num = 5

        elif 0.25 < r <= 0.7:
            self.op = '+'
            r_add = random.random()
            for i in range(20):
                if 0.05 * i <= r_add <= 0.05 * (i + 1):
                    self.num = i + 1

        elif 0.7 < r <= 0.85:
            self.op = '-'
            r_sub = random.random()
            for i in range(10):
                if 0.1 * i <= r_sub <= 0.1 * (i + 1):
                    self.num = i + 1

        elif 0.85 < r <= 1:
            self.op = '÷'
            r_div = random.random()
            if 0 <= r_div <= 0.5:
                self.num = 2
            elif 0.5 < r_div <= 0.8:
                self.num = 3
            elif 0.8 < r_div <= 1:
                self.num = 4

    def calculate(self, x):
        if self.op == '+':
            return x + self.num
        elif self.op == '-':
            return max(x - self.num, 0)
        elif self.op == '×':
            return x * self.num
        elif self.op == '÷':
            return x // self.num

    def draw(self, screen):
        self.door.draw()
        if self.num < 10:
            screen.draw.text(self.op + str(self.num), (self.x - 16, self.y - 15), fontsize=50)
        else:
            screen.draw.text(self.op + str(self.num), (self.x - 28, self.y - 15), fontsize=50)

    def update(self):
        self.y += self.speed
        self.door.x = self.x
        self.door.y = self.y

