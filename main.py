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
    pos = get_grid_pos(mouse_x, mouse_y)
    grid.add_obstacle(pos)


# returns true if rectangle group is created
def add_rectangle_group(rectangle_controller, group_id, mouse_x, mouse_y):
    pos = get_grid_pos(mouse_x, mouse_y)
    return rectangle_controller.add_rectangle_group(group_id, pos, grid.target)


def create_target(pos):
    grid_pos = get_grid_pos(pos[0], pos[1])
    grid.add_target(grid_pos)


def create_random_obstacles(percentage):
    grid.random_obstacles(percentage)


def animate():
    rectangle_controller.grow_groups()


def restart():
    global user_input_allowed
    global next_rectangle_group_id
    global created_first_rectangle

    grid.restart()
    rectangle_controller.restart()
    created_first_rectangle = False
    next_rectangle_group_id = 0
    user_input_allowed = True
    next_rectangle_group_id = 0


# Setup the screen
WIDTH = 600  # optional value
HEIGHT = 300  # optional value
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shortest path finder")

# Setup sizes
width_rectangle_amount = 60  # optional value, WIDTH divisor preferred
height_rectangle_amount = 30  # optional value, HEIGHT divisor preferred
rectangle_width = WIDTH // width_rectangle_amount
rectangle_height = HEIGHT // height_rectangle_amount
vertical_line_width = rectangle_width // 10
horizontal_line_width = rectangle_height // 10

# Instantiate classes
grid = Grid(width_rectangle_amount, height_rectangle_amount)
rectangle_controller = RectangleController(grid)
grid.rectangle_controller = rectangle_controller
drawer = Drawer(WIDTH, HEIGHT, screen, grid, rectangle_controller, rectangle_width, rectangle_height,
                vertical_line_width, horizontal_line_width)

# Other variables
created_first_rectangle = False
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
            if pressed[pygame.K_z]:
                create_random_obstacles(25)  # obstacle percentage in grid

    drawer.draw()
    pygame.display.update()

    if user_input_allowed:
        clock.tick(120)
    else:
        animate()
        clock.tick(30)

pygame.quit()
