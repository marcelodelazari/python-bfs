import random

from Rectangle import Rectangle


class RectangleGroup(object):

    def __init__(self, grid, group_id, center, target):
        self.rectangles_positions = set()
        self.rectangles = []

        self.grid = grid
        self.group_id = group_id
        self.center = center
        self.COLOR = (random.randrange(10, 230), random.randrange(50, 200), random.randrange(50, 200))

        self.first_rectangle = Rectangle(None, center[0], center[1], self.group_id, self.COLOR, True)
        self.rectangles.append(self.first_rectangle)
        self.rectangles_positions.add((center[0], center[1]))

        self.target = target
        self.growing = True
        self.found_path = False

    def restart(self):
        self.rectangles_positions.clear()
        self.rectangles.clear()

    def add_target(self, pos):
        self.target = pos

    def grow_rectangle(self, rectangle):
        growth = False
        if self.growing:
            x = rectangle.x
            y = rectangle.y

            up = (x, y - 1)
            down = (x, y + 1)
            right = (x + 1, y)
            left = (x - 1, y)

            for pos in [up, down, right, left]:
                if self.grid.is_inside(pos) and not self.grid.is_obstacle(pos) and pos not in self.rectangles_positions:
                    new_rectangle = Rectangle(rectangle, pos[0], pos[1], self.group_id, self.COLOR, False)
                    self.rectangles_positions.add(pos)
                    self.rectangles.append(new_rectangle)
                    growth = True

                    if pos == self.target:
                        self.growing = False
                        possible_path = self.path(new_rectangle)
                        self.found_path = True
                        return self.found_path, possible_path, growth

        return self.found_path, False, growth

    #  deletes all rectangles that doesnt belong to the right path
    def path(self, rectangle):
        path_rectangles = []

        while rectangle is not None:
            path_rectangles.append(rectangle)
            rectangle = rectangle.father

        self.rectangles_positions.clear()
        self.rectangles.clear()

        for rectangle in path_rectangles:
            self.rectangles_positions.add(rectangle.get_pos())
            self.rectangles.append(rectangle)

        return path_rectangles

    def grow_rectangles(self):
        if self.growing:
            growth_at_least_once = False
            if self.growing:
                for i in range(len(self.rectangles)):
                    found_path, possible_path, growth = self.grow_rectangle(self.rectangles[i])
                    if growth:
                        growth_at_least_once = True
                    if found_path:
                        return False  # stops

            if not growth_at_least_once:
                self.growing = False
                self.only_first()
        return False

    # deletes all except the first
    def only_first(self):
        self.rectangles_positions.clear()
        self.rectangles.clear()
        self.rectangles.append(self.first_rectangle)
        self.rectangles_positions.add(self.first_rectangle.get_pos())

    def pos_occupied(self, pos):
        return pos in self.rectangles_positions

    def get_score(self):
        if len(self.rectangles) <= 1:
            return "N"
        return len(self.rectangles) - 1
