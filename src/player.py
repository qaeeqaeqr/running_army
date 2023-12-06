from pgzero.builtins import Actor, animate, keyboard


class Person(object):
    def __init__(self, x, y, speed, playeri):
        self.x = x
        self.y = y
        self.speed = speed
        self.playeri = playeri
        self.image_folder = 'player' + str(self.playeri)
        self.images = [self.image_folder + '/0',
                       self.image_folder + '/1',
                       self.image_folder + '/2',
                       self.image_folder + '/3']
        self.front_person = Actor(self.image_folder + '/person')
        self.current_running_image = 0
        self.delay_times = 6
        self.person = Actor(self.images[self.current_running_image])

    def draw(self):
        if self.person.x < 100:
            return
        self.person.draw()

    def update_skin(self):
        self.image_folder = 'player' + str(self.playeri)
        self.images = [self.image_folder + '/0',
                       self.image_folder + '/1',
                       self.image_folder + '/2',
                       self.image_folder + '/3']
        self.front_person = Actor(self.image_folder + '/person')

    def update(self):
        self.current_running_image = (self.current_running_image + 1) % (len(self.images) * self.delay_times)
        self.person.image = self.images[self.current_running_image // self.delay_times]
        self.person.x = self.x
        self.person.y = self.y


class Player(object):
    def __init__(self, x, y, speed, num_person, max_num_person=100):
        self.x = x
        self.y = y
        self.speed = speed
        self.num_person = num_person
        self.persons = []
        self.max_num_person = max_num_person
        self.left = 0  # 最左侧人物到中心人物（x，y）之间的距离
        self.right = 0
        self.up = 0  # 最上面人物到中心人物之间的距离
        self.down = 0
        self.playeri = 0

        self.distance_between_persons = 10 + 3 / self.num_person
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

        self.init_persons()

    def query_i(self, x, lst):
        for i in range(11):
            for j in range(11):
                if lst[i][j] == x:
                    return i, j

    def sort_persons(self):
        """
        在人数变化的时候按照人物的xy排序，使得显示效果更好。
        """
        return sorted(self.persons, key=lambda person: (person.y, person.x))

    def update_bounds(self):
        min_x = 1000
        max_x = 0
        up_y = 800
        for person in self.persons:
            if person.x < min_x:
                min_x = person.x
            if person.x > max_x:
                max_x = person.x
            if person.y < up_y:
                up_y = person.y
        self.left = self.x - min_x
        self.right = max_x - self.x
        self.up = self.y - up_y

    def init_persons(self):
        """
        根据一开始的num_person确定每个人的位置。
        :return:
        """
        for i in range(self.num_person):
            res = self.query_i(i + 1, self.arrangement)
            x_offset, y_offset = res[1] - 5, res[0] - 5
            self.persons.append(Person(self.x + x_offset * self.distance_between_persons,
                                       self.y + y_offset * self.distance_between_persons,
                                       self.speed,
                                       self.playeri))

    def syn_person_movement(self):
        """
        当人数增加时，可能会导致不同的人处于行走的不同帧，使得整个军队看起来不整齐。故需要状态同步。
        """
        frame = self.persons[0].current_running_image
        for i in range(len(self.persons)):
            self.persons[i].current_running_image = frame

    def on_person_change(self, num):
        """
        改变人数，并重新排列。
        """
        if num > 0:
            terminate = min(self.num_person + num + 1, self.max_num_person + 1)
            for i in range(self.num_person + 1, terminate):
                res = self.query_i(i + 1, self.arrangement)
                x_offset, y_offset = res[1] - 5, res[0] - 5
                self.persons.append(Person(self.x + x_offset * self.distance_between_persons,
                                           self.y + y_offset * self.distance_between_persons,
                                           self.speed,
                                           self.playeri))
            self.num_person = min(self.num_person + num, self.max_num_person)
        else:
            if abs(num) >= self.num_person:
                self.persons.clear()
                self.num_person = 0
                return
            for i in range(self.num_person - 1, self.num_person + num - 1, -1):
                self.persons.pop(i)
            self.num_person += num
        self.syn_person_movement()

    def draw(self, screen):
        # NOTE: 这里显示很重要。应该从上到下从左到右显示。
        sorted_person = self.sort_persons()
        for i in range(self.num_person):
            sorted_person[i].draw()
        screen.draw.text(str(self.num_person), (self.x - 20, self.y - 60),
                         fontsize=40, color=(200, 66, 66))

    def on_mouse_move(self, pos, rel, left_bound, right_bound):
        mouse_pos0 = pos[0]
        if pos[0] > right_bound:
            mouse_pos0 = right_bound
        if pos[0] < left_bound:
            mouse_pos0 = left_bound
        for i in range(self.num_person):
            self.persons[i].x = mouse_pos0 - self.x + self.persons[i].x
        self.x = mouse_pos0

    def update_skin(self):
        self.playeri = (self.playeri + 1) % 5
        for i in range(self.num_person):
            self.persons[i].playeri = self.playeri
            self.persons[i].update_skin()

    def update(self):
        for i in range(self.num_person):
            self.persons[i].update()
        self.update_bounds()
