import pygame as pg


# Color constants
WHITE = (255, 255, 255)


# Creates the pygame window
def create_screen(width, height):
    global screen
    screen = pg.display.set_mode((width, height))
    screen.fill(WHITE)
    return screen

