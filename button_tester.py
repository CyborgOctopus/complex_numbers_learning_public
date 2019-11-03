import pygame as pg
from Button import Button

# Color constants
WHITE = (255, 255, 255)

# Misc.
image_folder_path = 'images/'


def main():
    screen_width, screen_height, x, y, image_1_path, image_2_path = get_user_input()
    screen = create_screen(screen_width, screen_height)
    image_1 = pg.image.load(image_folder_path + image_1_path)
    image_2 = pg.image.load(image_folder_path + image_2_path)
    button = Button(screen, x, y, image_1, image_2)
    animate(button)


def get_user_input():
    screen_width = int(input("Screen width: "))
    screen_height = int(input("Screen height: "))
    x = int(input("Top left button x: "))
    y = int(input("Top left button y: "))
    image_1_path = input("Location of the first image: ")
    image_2_path = input("Location of the second image: ")
    return screen_width, screen_height, x, y, image_1_path, image_2_path


# Executes the animation loop
def animate(button):
    pg.display.flip()
    running = True
    button.display()
    while running:
        for event in pg.event.get():

            if event.type == pg.QUIT:
                running = False

            elif event.type == pg.MOUSEBUTTONDOWN:
                button.update_click_status()
                button.display()


# Opens the pygame window
def create_screen(width, height):
    pg.init()
    screen = pg.display.set_mode((width, height))
    screen.fill(WHITE)
    return screen


main()
