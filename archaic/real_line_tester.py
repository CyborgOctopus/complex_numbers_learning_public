import pygame as pg
from RealLine import RealLine

# Screen display parameters
fill_color = (255, 255, 255)

# Other
offset = 2
vec_color = (0, 200, 0)


def main():
    parameters = get_user_input()
    screen = create_screen(parameters[0], parameters[1])
    rl = RealLine(screen, parameters[2], parameters[3])
    rl.set_offset(offset)
    screen.fill(fill_color)
    rl.display()
    rl.draw_line(0, parameters[4], vec_color)
    rl.plot_point(parameters[4])
    rl.add_coord(parameters[4])
    rl.plot_point(parameters[5])
    rl.add_coord(parameters[5])
    rl.display_coords()
    animate()


# Allows the user to choose values for screen width,  height, number line range, and point displays
def get_user_input():
    width = int(input("Screen width: "))
    height = int(input("Screen height: "))
    spacing = float(input("Number line spacing: "))
    half_range = float(input("Value displayed on far right of real line: "))
    point_1_x = float(input("Point 1 x-coord: "))
    point_2_x = float(input("Point 2 x-coord: "))
    return width,  height, spacing, half_range, point_1_x, point_2_x


# Executes the animation loop
def animate():
    pg.display.flip()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False


# Opens the pygame window
def create_screen(width, height):
    pg.init()
    screen = pg.display.set_mode((width, height))
    screen.fill(fill_color)
    return screen


main()
