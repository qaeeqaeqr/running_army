from pgzero.builtins import Actor, animate, keyboard
import random


class TrapBase(object):
    """
    一个Trap类的示例代表地图上出现的一个陷阱。
    """
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.rect = 0

    def draw(self, *args):
        raise NotImplementedError('class "Trap" must have method "draw"!')

    def update(self, *args):
        raise NotImplementedError('class "Trap" must have method "draw"!')


class Trap1(TrapBase):
    def __init__(self, x, y, speed):
        super(Trap1, self).__init__(x, y, speed)
        self.bomb0 = Actor('game_scene/traps/trap1_bomb0')
        self.bomb1 = Actor('game_scene/traps/trap1_bomb1')
        self.blowup = Actor('game_scene/traps/trap1_blowup')
        self.bomb0.x = self.bomb1.x = self.blowup.x = self.x
        self.bomb0.y = self.bomb1.y = self.blowup.y = self.y
        self.STATUS_BOMB_metadata = ['black', 'red', 'blowup', 'blowed']
        self.status = 0

    def draw(self):
        if self.status == 0:
            self.bomb0.draw()
        if self.status == 1:
            self.bomb1.draw()
        if self.status == 2:
            self.blowup.draw()
        if self.status == 3:
            pass

    def update(self):
        self.y += self.speed
        self.bomb0.y = self.bomb1.y = self.blowup.y = self.y


class Trap2(TrapBase):
    def __init__(self, x, y, speed):
        super(Trap2, self).__init__(x, y, speed)
        self.fire0 = Actor('game_scene/traps/trap2_fire0')
        self.fire1 = Actor('game_scene/traps/trap2_fire1')
        self.fire2 = Actor('game_scene/traps/trap2_fire2')
        self.fire0.x = self.fire1.x = self.fire2.x = x
        self.fire0.y = self.fire1.y = self.fire2.y = y
        self.current_frame = 0
        self.delay_times = 6
        self.firex = 0

    def draw(self):
        if self.firex == 0:
            self.fire0.draw()
        if self.firex == 1:
            self.fire1.draw()
        if self.firex == 2:
            self.fire2.draw()

    def update(self):
        self.current_frame = (self.current_frame + 1) % (self.delay_times * 3)
        self.firex = self.current_frame // self.delay_times
        self.y += self.speed
        self.fire0.y = self.fire1.y = self.fire2.y = self.y

