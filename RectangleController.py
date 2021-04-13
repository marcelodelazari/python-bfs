from RectangleGroup import RectangleGroup


class RectangleController(object):

    def __init__(self, grid):
        self.center_rectangle_groups = set()
        self.rectangle_groups = []
        self.grid = grid
        self.target = None
        self.drawer = None

    def add_target(self, pos):
        self.target = pos
        for group in self.rectangle_groups:
            group.target = pos

    def restart(self):
        self.target = None
        self.center_rectangle_groups.clear()
        for group in self.rectangle_groups:
            group.restart()
        self.rectangle_groups.clear()

    def add_rectangle_group(self, group_id, center):
        self.center_rectangle_groups.add(center)
        self.rectangle_groups.append(RectangleGroup(self.grid, group_id, center, self.target))

    def grow_groups(self):
        for group in self.rectangle_groups:
            group.grow_rectangles()

    def pos_occupied(self, pos):
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
