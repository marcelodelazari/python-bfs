class Rectangle(object):

    def __init__(self, father, x, y, group_id, color, is_first):
        self.father = father
        self.x = x
        self.y = y
        self.group_id = group_id
        self.color = color
        self.is_first = is_first

    def get_pos(self):
        return self.x, self.y
