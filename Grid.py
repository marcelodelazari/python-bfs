class Grid(object):

    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height
        self.obstacles = set()

    def restart(self):
        self.obstacles.clear()

    def add_obstacle(self, x, y):
        self.obstacles.add((x, y))

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
