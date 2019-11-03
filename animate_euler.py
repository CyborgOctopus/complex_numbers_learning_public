import sys
import pygame as pg
import math
from Euler import EulerCircle
from shared_functions import *

# Display parameters
width = 800
height = 800
phase_step = 0.007
title = "Animated Euler's formula"


def animate_euler():
    pg.init()
    pg.display.set_caption(title)
    screen = create_screen(width, height)
    euler_circle = EulerCircle(screen)
    euler_circle.display()
    running = True

    while running:
        screen.fill(WHITE)
        euler_circle.display()
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        euler_circle.set_phase((euler_circle.phase + phase_step) % math.tau)
    pg.quit()


if __name__ == "__main__":
    animate_euler()
