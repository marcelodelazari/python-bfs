import pygame
from Drawer import Drawer
from Grid import Grid
from RectangleController import RectangleController

pygame.init()

# Keyboard control guide:
# O = New obstacle, A = New rectangle group, R = Restart, T = Set target, G = Start animation
def get_grid_pos(mouse_x, mouse_y):
    return mouse_x // (WIDTH // width_rectangle_amount), mouse_y // (HEIGHT // height_rectangle_amount)

#  return True if obstacle is created
def add_obstacle(grid, mouse_x, mouse_y):
    global target

    grid_x, grid_y = get_grid_pos(mouse_x, mouse_y)
    if target == (grid_x, grid_y):
        return False
    grid.add_obstacle(grid_x, grid_y)
    return True

# returns true if rectangle group is created
def add_rectangle_group(rectangle_controller, group_id, mouse_x, mouse_y):
    center = get_grid_pos(mouse_x, mouse_y)
    if not pos_occupied(center):
        rectangle_controller.add_rectangle_group(group_id, center)
        return True
    return False


def pos_occupied(pos):
    global target

    return rectangle_controller.pos_occupied(pos) or grid.is_obstacle(pos) or pos == target


def create_target(pos):
    global target

    grid_pos = get_grid_pos(pos[0], pos[1])
    if not pos_occupied(grid_pos):
        target = grid_pos
        rectangle_controller.add_target(grid_pos)


def animate():
    rectangle_controller.grow_groups()


def restart():
    global user_input_allowed
    global next_rectangle_group_id
    global target
    global first_rectangle

    grid.restart()
    rectangle_controller.restart()
    target = None
    first_rectangle = False
    next_rectangle_group_id = 0
    user_input_allowed = True
    next_rectangle_group_id = 0


# Setup the screen
WIDTH = 800  # optional value
HEIGHT = 600  # optional value
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shortest path finder")

# Setup sizes
width_rectangle_amount = 40  # optional value, WIDTH divisor preferred
height_rectangle_amount = 30  # optional value, HEIGHT divisor preferred
rectangle_width = WIDTH // width_rectangle_amount
rectangle_height = HEIGHT // height_rectangle_amount
vertical_line_width = rectangle_width // 10
horizontal_line_width = rectangle_height // 10

# Instantiate classes
grid = Grid(width_rectangle_amount, height_rectangle_amount)
rectangle_controller = RectangleController(grid)
drawer = Drawer(WIDTH, HEIGHT, screen, grid, rectangle_controller, rectangle_width, rectangle_height, vertical_line_width, horizontal_line_width)

# Other variables
target = None
first_rectangle = False
next_rectangle_group_id = 0

# Program loop
running = True
user_input_allowed = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        pressed = pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g and next_rectangle_group_id > 0:
                user_input_allowed = False
            if event.key == pygame.K_a and user_input_allowed:
                if add_rectangle_group(rectangle_controller, next_rectangle_group_id, mouse_x, mouse_y):
                    next_rectangle_group_id += 1

        if pressed[pygame.K_r]:
            restart()
        if user_input_allowed:
            if pressed[pygame.K_o]:
                add_obstacle(grid, mouse_x, mouse_y)
            if pressed[pygame.K_t]:
                create_target((mouse_x, mouse_y))
    drawer.draw(target)
    pygame.display.update()

    if user_input_allowed:
        clock.tick(120)
    else:
        animate()
        clock.tick(30)
