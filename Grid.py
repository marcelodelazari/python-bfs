import random


class Grid(object):

    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height
        self.obstacles = set()
        self.target = None
        self.rectangle_controller = None

    def restart(self):
        self.add_target(None)
        self.obstacles.clear()

    def add_target(self, pos):
        if not self.is_occupied(pos):
            self.target = pos
        self.rectangle_controller.set_target(self.target)

    def add_obstacle(self, pos):
        if not self.is_occupied(pos):
            self.obstacles.add(pos)

    def is_inside(self, pos):
        x = pos[0]
        y = pos[1]
        if x < 0 or x >= self.WIDTH:
            return False
        if y < 0 or y >= self.HEIGHT:
            return False
        return True

    def is_obstacle(self, pos):
        return pos in self.obstacles

    def is_target(self, pos):
        return pos == self.target

    def is_occupied(self, pos):
        return pos == self.target or pos in self.obstacles

    def random_obstacles(self, percentage):
        self.obstacles.clear()

        for w in range(self.WIDTH):
            for h in range(self.HEIGHT):
                pos = (w, h)
                if random.randrange(1, 101) <= percentage:
                    if not self.is_occupied(pos) and not self.rectangle_controller.is_occupied(pos):
                        self.add_obstacle(pos)
