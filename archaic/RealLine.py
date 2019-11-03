import numpy as np
import pygame as pg

# Color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Line display parameters
real_line_width = 3
vec_width = 4
tick_mark_width = 1
tick_mark_height = 10
zero_mark_height = 20

# Point and label display parameters
point_color = (200, 0, 0)
point_radius = 5
font_size = 20
font_offset = 30

# Misc.
snap_threshold = 6


# TODO: optimize text overlap prevention, allow unlimited size numbers by switching from float to something else
# This class defines a real number line which supports selection of points and animated arithmetic
class RealLine:

    def __init__(self, screen, spacing, half_range, offset=0):
        self.screen = screen
        self.spacing = spacing
        self.half_range = half_range
        self.pixel_spacing = 0
        self.update_pixel_spacing()
        self.offset = offset
        self.pixel_offset = 0
        self.update_pixel_offset()
        self.added_coords = []
        self.newly_added_coord = None
        self.renders = {}
        self.rects = {}
        self.displayed_coords = []

    # Public

    # Draws a real number line on the screen.
    def display(self):
        self.add_line()
        self.add_tick_marks()
        self.plot_all()
        self.display_coords()

    # Plots all points on the real line
    def plot_all(self):
        for pt in self.added_coords:
            self.plot_point(pt)

    # Plots a point on the real line
    def plot_point(self, x):
        pos = (self.convert_to_pixel_coord(x), self.screen.get_height() // 2)
        pg.draw.circle(self.screen, point_color, pos, point_radius)

    # Allows the spacing of the real line to be altered
    def set_spacing(self, spacing):
        self.spacing = spacing
        self.update_pixel_spacing()

    # Allows the real line to be scaled
    def set_half_range(self, half_range):
        self.half_range = half_range
        self.update_pixel_spacing()
        self.update_pixel_offset()

    # Allows the real line to shift left and right
    def set_offset(self, offset):
        self.offset = offset
        self.update_pixel_offset()

    # Draws a line from 'x' to 'y', where these are interpreted as points on the real line
    def draw_line(self, x, y, color):
        x_pos = (self.convert_to_pixel_coord(x), self.screen.get_height() / 2)
        y_pos = (self.convert_to_pixel_coord(y), self.screen.get_height() / 2)
        pg.draw.line(self.screen, color, x_pos, y_pos, vec_width)

    # Converts from pixel coordinates  to coordinates on the real line
    def convert_to_line_coord(self, pixel_coord):
        return round(((pixel_coord - self.pixel_offset) / self.screen.get_width() - 0.5) * 2 * self.half_range, 5)

    # Converts from real line coordinates to pixel coordinates
    def convert_to_pixel_coord(self, line_coord):
        return int(round((line_coord / (2 * self.half_range) + 0.5) * self.screen.get_width() + self.pixel_offset))

    # Displays text boxes with given coordinates on the real line, making sure there is no overlap.
    def display_coords(self):
        new_displayed_coords = []
        for x in self.added_coords:
            render, render_rect = self.get_display_surf_and_rect(x)
            if self.intersects_displayed_coords(render_rect):
                continue
            elif x not in self.displayed_coords and x != self.newly_added_coord:
                if self.intersects_added_coords(render_rect):
                    continue
            self.screen.blit(render, (render_rect.left, render_rect.top))
            new_displayed_coords.append(x)
        self.displayed_coords = new_displayed_coords
        self.newly_added_coord = None

    # Adds coords to be displayed
    def add_coord(self, x):
        self.added_coords.append(x)
        self.newly_added_coord = x

    # If a pixel value is close enough to a tick mark, converts it to the real line value at the tick mark
    def snap_to_mark(self, pixel_coord):
        center = self.screen.get_width() / 2 + (self.pixel_offset % self.pixel_spacing)
        mark_coord = center + round((pixel_coord - center) / self.pixel_spacing) * self.pixel_spacing
        if abs(mark_coord - pixel_coord) <= snap_threshold:
            return self.convert_to_line_coord(mark_coord)
        return self.convert_to_line_coord(pixel_coord)

    # Private

    # Checks if a given coordinate rect would intersects any displayed coords
    def intersects_displayed_coords(self, rect):
        for x in self.displayed_coords:
            x_rect = self.get_display_surf_and_rect(x)[1]
            if x_rect.colliderect(rect) and x_rect != rect:
                return True
        return False

    # Checks if a given coordinate rect would intersect any other added coords
    def intersects_added_coords(self, rect):
        for x in self.added_coords:
            x_rect = self.get_display_surf_and_rect(x)[1]
            if x_rect.colliderect(rect) and x_rect != rect:
                return True
        return False

    # Returns a surface and rect for a numerical coordinate display
    def get_display_surf_and_rect(self, x):
        font = pg.font.Font(None, font_size)
        pos = (self.convert_to_pixel_coord(x), self.screen.get_height() // 2 - font_offset)
        render = font.render(str(x), True, BLACK)
        return render, render.get_rect(center=(pos[0] + render.get_width() / 2, pos[1] + render.get_height() / 2))

    # Updates the value of 'pixel_spacing' to conform to changes in 'half_range' or 'spacing'
    def update_pixel_spacing(self):
        self.pixel_spacing = self.screen.get_width() / (2 * self.half_range) * self.spacing

    # Updates the value of 'pixel_offset' to conform to changes in 'half_range' or 'offset'
    def update_pixel_offset(self):
        self.pixel_offset = self.screen.get_width() / (2 * self.half_range) * self.offset

    # Adds the main line to the screen
    def add_line(self):
        left = (0, self.screen.get_height() / 2)
        right = (self.screen.get_width(), self.screen.get_height() / 2)
        pg.draw.line(self.screen, BLACK, left, right, real_line_width)

    # Adds tick marks to the real line
    def add_tick_marks(self):
        for pair in self.line_coords():
            pg.draw.line(self.screen, BLACK, pair[0], pair[1], tick_mark_width)
        self.add_origin()

    # Creates the larger tick mark representing the origin
    def add_origin(self):
        origin = self.screen.get_width() / 2 + self.pixel_offset
        top = (origin, self.screen.get_height() / 2 - zero_mark_height)
        bottom = (origin, self.screen.get_height() / 2 + zero_mark_height)
        pg.draw.line(self.screen, BLACK, top, bottom, tick_mark_width)

    # Creates the line coordinates
    def line_coords(self):
        return list(zip(self.top_coords(), self.bottom_coords()))

    # Creates the top coordinates
    def top_coords(self):
        x_coords = self.x_coords()
        tops_y = [self.screen.get_height() / 2 - tick_mark_height] * len(x_coords)
        return list(zip(x_coords, tops_y))

    # Creates the bottom coordinates
    def bottom_coords(self):
        x_coords = self.x_coords()
        bottoms_y = [self.screen.get_height() / 2 + tick_mark_height] * len(x_coords)
        return list(zip(x_coords, bottoms_y))

    # Creates the x-coordinates
    def x_coords(self):
        offset_center = self.screen.get_width() / 2 + (self.pixel_offset % self.pixel_spacing)
        sign = np.sign(self.pixel_spacing)
        neg = np.arange(offset_center, 0, -sign * self.pixel_spacing)
        pos = np.arange(offset_center + self.pixel_spacing, self.screen.get_width(), sign * self.pixel_spacing)
        return np.append(neg, pos)
