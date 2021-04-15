from RectangleGroup import RectangleGroup


class RectangleController(object):

    def __init__(self, grid):
        self.pos_rectangle_groups = set()
        self.rectangle_groups = []
        self.grid = grid
        self.drawer = None

    def restart(self):
        self.target = None
        self.pos_rectangle_groups.clear()
        for group in self.rectangle_groups:
            group.restart()
        self.rectangle_groups.clear()

    def add_rectangle_group(self, group_id, pos, target):
        if not self.is_occupied(pos) and not self.grid.is_occupied(pos):
            self.pos_rectangle_groups.add(pos)
            self.rectangle_groups.append(RectangleGroup(self.grid, group_id, pos, target))
            return True
        return False

    def set_target(self, target):
        for group in self.rectangle_groups:
            group.target = target

    def grow_groups(self):
        for group in self.rectangle_groups:
            group.grow_rectangles()

    def is_occupied(self, pos):
        for group in self.rectangle_groups:
            if group.pos_occupied(pos):
                return True
        return False

    def get_pos_color(self, pos):
        amount = 0
        r, g, b = 0, 0, 0
        for group in self.rectangle_groups:
            if group.pos_occupied(pos):
                r += group.COLOR[0]
                g += group.COLOR[1]
                b += group.COLOR[2]
                amount += 1

        if amount > 0:
            r //= amount
            g //= amount
            b //= amount

            return r, g, b
        return False