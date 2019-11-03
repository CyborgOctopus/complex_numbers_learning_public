import pygame as pg
import math
from ComplexPlane import ComplexPlane

# Screen display parameters
fill_color = (255, 255, 255)

# Other
vec_color = (0, 200, 0)


def main():
    side_length, spacing, half_range, phase, offset, point_1, point_2 = get_user_input()
    screen = create_screen(side_length, side_length)
    cp = ComplexPlane(screen, spacing, half_range, phase, offset)
    cp.add_coords(point_1)
    cp.add_coords(point_2)
    cp.draw_line(point_1, point_2, vec_color)
    cp.display()
    cp.display_coords()
    animate()


# Allows the user to choose values for screen size, complex plane range, and point displays
def get_user_input():
    side_length = int(input("Screen side length: "))
    spacing = float(input("Grid spacing: "))
    half_range = float(input("Half range: "))
    phase = float(input("Phase as a multiple of pi: ")) * math.pi
    offset = complex(input("offset: "))
    point_1 = complex(input("Point 1 coord: "))
    point_2 = complex(input("Point 2 x-coord: "))
    return side_length, spacing, half_range, phase, offset, point_1, point_2


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
