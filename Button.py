import pygame as pg


# Defines a button object based on two images. It is flexible enough to act as a normal or radio button.
class Button:

    def __init__(self, screen, top_left_x, top_left_y, rest_image, clicked_image):
        self.screen = screen
        self.x = top_left_x
        self.y = top_left_y
        self.rest_image = rest_image
        self.clicked_image = clicked_image
        self.clicked = False
        self.center_x = 0
        self.center_y = 0
        self.update_center_x()
        self.update_center_y()

    # Displays the appropriate button image on the screen
    def display(self):
        if self.clicked:
            self.screen.blit(self.clicked_image, (self.x, self.y))
        else:
            self.screen.blit(self.rest_image, (self.x, self.y))

    # Updates the x-coordinate of the center location of the button
    def update_center_x(self):
        if self.clicked:
            image = self.clicked_image
        else:
            image = self.rest_image
        self.center_x = self.x + image.get_width() / 2

    # Updates the y-coordinate of the center location of the button
    def update_center_y(self):
        if self.clicked:
            image = self.clicked_image
        else:
            image = self.rest_image
        self.center_y = self.y + image.get_height() / 2

    # Allows the button to be reset
    def unclick(self):
        self.clicked = False
        self.update_center_x()
        self.update_center_y()

    # Checks if the button is currently in the clicked state
    def is_clicked(self):
        return self.clicked

    # Checks if the button has been clicked. If it has been, set accordingly
    def update_click_status(self):
        if self.rest_image.get_rect(center=(self.center_x, self.center_y)).collidepoint(pg.mouse.get_pos()):
            self.clicked = True
            self.update_center_x()
            self.update_center_y()
