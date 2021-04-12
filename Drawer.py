import pygame


class Drawer(object):

    WHITE = (255, 255, 255)
    GREY = (210, 210, 210)
    BLACK = (10, 10, 10)
    RED = (255, 0, 0)
    YELLOW = (220, 220, 0)

    def __init__(self, width, height, screen, grid, rectangle_controller, rectangle_width, rectangle_height, vertical_line_width, horizontal_line_width):
        self.WIDTH = width
        self.HEIGHT = height
        self.screen = screen
        self.grid = grid
        self.rectangle_controller = rectangle_controller
        self.rectangle_width = rectangle_width
        self.rectangle_height = rectangle_height
        self.vertical_line_width = vertical_line_width
        self.horizontal_line_width = horizontal_line_width
        self.font = pygame.font.SysFont('bahnschrift', int(self.rectangle_width / 1.2))


    def draw(self, target):
        self.screen.fill(self.GREY)

        self.draw_obstacles()


        self.draw_rectangles()

        if target != None:
            x = target[0]
            y = target[1]
            pygame.draw.rect(self.screen, self.RED, (
            x * self.rectangle_width, y * self.rectangle_height, self.rectangle_width, self.rectangle_height))

        self.draw_all_groups_score()
        self.draw_lines()

    def draw_lines(self):
        for x in range(0, self.WIDTH, self.rectangle_width):
            pygame.draw.line(self.screen, self.BLACK, (x, 0), (x, self.HEIGHT), max(1, self.vertical_line_width))
        for y in range(0, self.HEIGHT, self.rectangle_height):
            pygame.draw.line(self.screen, self.BLACK, (0, y), (self.WIDTH, y), max(1, self.horizontal_line_width))

    def draw_obstacles(self):
        for obstacle in self.grid.obstacles:
            x = obstacle[0]
            y = obstacle[1]
            pygame.draw.rect(self.screen, self.BLACK, (x * self.rectangle_width, y * self.rectangle_height, self.rectangle_width, self.rectangle_height))

    def draw_rectangle(self, rectangle, distance):
        x = rectangle.x
        y = rectangle.y
        pos = (x, y)
        color = rectangle.color

        mixed_color = self.rectangle_controller.get_pos_color(pos)

        if mixed_color:
            color = mixed_color

        screen_x = x * self.rectangle_width
        screen_y = y * self.rectangle_height
        pygame.draw.rect(self.screen, color, (screen_x, screen_y, self.rectangle_width, self.rectangle_height))

    def draw_all_groups_score(self):
        for group in self.rectangle_controller.rectangle_groups:
            self.draw_group_score(group)

    def draw_group_score(self, rectangle_group):
        growing = rectangle_group.growing
        if growing:
            return False

        score = rectangle_group.get_score()
        first_rectangle = rectangle_group.first_rectangle

        screen_x = first_rectangle.x * self.rectangle_width
        screen_y = first_rectangle.y * self.rectangle_height

        score_render = self.font.render(str(score), True, self.BLACK)
        score_x = screen_x + self.rectangle_width // 10
        score_y = screen_y + self.rectangle_height // 10
        if score < 10:
            score_x += self.rectangle_width // 10

        self.screen.blit(score_render, (score_x, score_y))



    def draw_rectangles(self):
        for rectangle_group in self.rectangle_controller.rectangle_groups:
            show_distance = not rectangle_group.growing
            distance = False
            if show_distance:
                distance = len(rectangle_group.rectangles) - 1
            for rectangle in rectangle_group.rectangles:
                self.draw_rectangle(rectangle, distance)
