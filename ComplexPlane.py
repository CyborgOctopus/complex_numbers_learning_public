import numpy as np
import pygame as pg
import math

# Color constants
BLACK = (0, 0, 0)

# Plane display parameters
line_width = 1
axis_width = 3
vec_width = 4

point_color = (200, 0, 0)
point_radius = 5
font_size = 20
font_offset = 30

# Real line display parameters
tick_mark_height = 10
zero_mark_height = 20

# Misc.
# Point and label display parameters
snap_threshold = 6


# TODO Known bugs: 1. clicking anywhere selects one number when zoomed in far
#   TODO 2. zooming in far causes problems in general (shaky screen, etc.)
#   TODO 3. quitting the application occurs incorrectly when a pygame window is open
# TODO Nice-to-add features: Allow for unlimited range zooming and arithmetic
# This class defines a complex number plane which supports selection of points and animated arithmetic
class ComplexPlane:

    def __init__(self, screen, spacing, half_range, phase=0, offset=0+0j, real_mode=False):
        self.screen = screen
        self.spacing = spacing
        self.half_range = half_range
        self.phase = phase
        self.pixel_spacing = 0
        self.update_pixel_spacing()
        self.offset = offset.real - offset.imag * 1j
        self.pixel_offset = (0, 0)
        self.update_pixel_offset()
        self.added_coords = []
        self.newly_added_coords = None
        self.renders = {}
        self.rects = {}
        self.displayed_coords = []
        self.padding = 0
        self.set_padding()
        self.real_mode = real_mode

    # Public

    # Draws a complex plane on the screen
    def display(self):
        self.add_grid()
        self.add_bold_axes()
        self.plot_all()
        self.display_coords()

    # Plots a point on the complex plane
    def plot_point(self, coords):
        pg.draw.circle(self.screen, point_color, self.convert_to_pixel_coords(coords), point_radius)

    # Allows the spacing of the plane to be altered
    def set_spacing(self, spacing):
        self.spacing = spacing
        self.update_pixel_spacing()

    # Allows the complex plane to be scaled
    def set_half_range(self, half_range):
        self.half_range = half_range
        self.update_pixel_spacing()
        self.update_pixel_offset()

    # Allows the plane to shift left, right, up, and down
    def set_offset(self, offset):
        self.offset = offset.real if self.real_mode else offset
        self.update_pixel_offset()

    # Allows the plane to be rotated
    def set_phase(self, phase):
        self.phase = phase

    # Draws a line from 'point_1' to 'point_2', where these are interpreted as points on the complex plane
    def draw_line(self, point_1, point_2, color):
        pixel_point_1 = self.convert_to_pixel_coords(point_1)
        pixel_point_2 = self.convert_to_pixel_coords(point_2)
        pg.draw.line(self.screen, color, pixel_point_1, pixel_point_2, vec_width)

    # Converts from pixel coordinates to coordinates on the complex plane
    def convert_to_plane_coords(self, pixel_coords):
        pixel_coords = self.rotate(pixel_coords, -self.phase)
        plane_x = ((pixel_coords[0] - self.pixel_offset[0]) / self.screen.get_width() - 0.5) * 2 * self.half_range
        plane_y = ((pixel_coords[1] - self.pixel_offset[1]) / self.screen.get_height() - 0.5) * 2 * self.half_range
        if self.real_mode:
            plane_y = 0
        return round(plane_x, 5) - round(plane_y, 5) * 1j

    # Converts from complex plane coordinates to pixel coordinates
    def convert_to_pixel_coords(self, plane_coords):
        pixel_x = (plane_coords.real / (2 * self.half_range) + 0.5) * self.screen.get_width() + self.pixel_offset[0]
        pixel_y = (-plane_coords.imag / (2 * self.half_range) + 0.5) * self.screen.get_height() + self.pixel_offset[1]
        pixel = self.rotate((pixel_x, pixel_y), self.phase)
        return int(round(pixel[0])), int(round(pixel[1]))

    # Displays text boxes with given coordinates on the complex plane, making sure there is no overlap.
    def display_coords(self):
        new_displayed_coords = []
        self.update_rects()
        for coords in self.rects:
            rect = self.rects[coords]
            if self.intersects_displayed_coords(rect):
                continue
            elif coords not in self.displayed_coords and coords != self.newly_added_coords:
                if self.intersects_rect_coords(rect):
                    continue
            self.screen.blit(self.renders[coords], (rect.left, rect.top))
            new_displayed_coords.append(coords)
        self.displayed_coords = new_displayed_coords
        self.newly_added_coords = None

    # Adds coords to be displayed
    def add_coords(self, coords):
        self.added_coords.append(coords)
        self.renders[coords] = self.get_display_surf(coords)
        self.newly_added_coords = coords

    # removes coords so they are no longer plotted and displayed
    def remove_coords(self, coords):
        if coords in self.added_coords:
            self.added_coords.remove(coords)
            if coords not in self.added_coords:
                del self.renders[coords]
        if coords in self.displayed_coords:
            self.displayed_coords.remove(coords)

    # If the pixel coordinates are close enough to a grid point, converts them to the values at the grid point
    def snap_to_grid(self, pixel_coords):
        pixel_coords = self.rotate(pixel_coords, -self.phase)
        center_x = self.screen.get_width() / 2 + (self.pixel_offset[0] % self.pixel_spacing)
        center_y = self.screen.get_height() / 2 + (self.pixel_offset[1] % self.pixel_spacing)
        closest_horiz_coord = center_x + round((pixel_coords[0] - center_x) / self.pixel_spacing) * self.pixel_spacing
        closest_vert_coord = center_y + round((pixel_coords[1] - center_y) / self.pixel_spacing) * self.pixel_spacing
        if abs(closest_horiz_coord - pixel_coords[0]) <= snap_threshold \
                and abs(closest_vert_coord - pixel_coords[1]) <= snap_threshold:
            return self.convert_to_plane_coords(self.rotate((closest_horiz_coord, closest_vert_coord), self.phase))
        return self.convert_to_plane_coords(self.rotate(pixel_coords, self.phase))

    # Private

    # Plots all current points on the complex plane
    def plot_all(self):
        for pt in self.added_coords:
            if self.in_screen(self.convert_to_pixel_coords(pt)):
                self.plot_point(pt)

    # Checks if a given coordinate rect would intersect any displayed coords
    def intersects_displayed_coords(self, rect):
        for coords in self.displayed_coords:
            if coords in self.rects and self.rects[coords].colliderect(rect) and self.rects[coords] != rect:
                return True
        return False

    # Checks if a given coordinate rect would intersect any other added coords
    def intersects_rect_coords(self, rect):
        for coords in self.rects:
            if self.rects[coords].colliderect(rect) and self.rects[coords] != rect:
                return True
        return False

    # Returns a surface for a numerical coordinate display.
    def get_display_surf(self, coords):
        font = pg.font.Font(None, font_size)
        imag_part = "" if self.real_mode else " + " + str(coords.imag) + "i"
        render = font.render(str(coords.real) + imag_part, True, BLACK)
        return render

    # Returns a rect for a numerical coordinate display
    def get_display_rect(self, coords):
        pos = (self.convert_to_pixel_coords(coords)[0], self.convert_to_pixel_coords(coords)[1] - font_offset)
        render = self.renders[coords]
        return render.get_rect(center=(pos[0] + render.get_width() / 2, pos[1] + render.get_height() / 2))

    # Generates all currrent coordinate display rects which will not cause an overflow
    def update_rects(self):
        self.rects.clear()
        for coords in self.added_coords:
            try:
                rect = self.get_display_rect(coords)
                if self.rect_in_screen(rect):
                    self.rects[coords] = rect
            except TypeError:
                continue

    # Updates the value of 'pixel_spacing' to conform to changes in 'half_range' or 'spacing'
    def update_pixel_spacing(self):
        self.pixel_spacing = self.screen.get_width() / (2 * self.half_range) * self.spacing

    # Updates the value of 'pixel_offset' to conform to changes in 'half_range' or 'offset'
    def update_pixel_offset(self):
        x_offset = self.screen.get_width() / (2 * self.half_range) * self.offset.real
        y_offset = self.screen.get_height() / (2 * self.half_range) * self.offset.imag
        self.pixel_offset = x_offset, y_offset

    # Adds the main grid to the screen, or the main line with tick marks in real mode
    def add_grid(self):
        self.add_imag_lines()
        if not self.real_mode:
            self.add_real_lines()

    # Adds imaginary lines to the screen
    def add_imag_lines(self):
        for pair in self.imag_line_coords():
            pg.draw.line(self.screen, BLACK, pair[0], pair[1], line_width)

    # Adds real lines to the screen
    def add_real_lines(self):
        for pair in self.real_line_coords():
            pg.draw.line(self.screen, BLACK, pair[0], pair[1], line_width)

    # Adds bold real and imaginary axes to the screen
    def add_bold_axes(self):
        self.add_real_axis()
        self.add_imag_axis()

    # Adds a bold imaginary axis to the screen
    def add_imag_axis(self):
        imag_width = self.screen.get_width() / 2 + self.pixel_offset[0]
        top = (imag_width, self.zero_ys()[0] if self.real_mode else -self.padding)
        bottom = (imag_width, self.zero_ys()[1] if self.real_mode else self.screen.get_height() + self.padding)
        try:
            pg.draw.line(self.screen, BLACK, self.rotate(top, self.phase), self.rotate(bottom, self.phase), axis_width)
        except TypeError:
            return

    # Adds a bold real axis to the screen
    def add_real_axis(self):
        real_height = self.screen.get_height() / 2 + self.pixel_offset[1]
        left = (-self.padding, real_height)
        right = (self.screen.get_width() + self.padding, real_height)
        try:
            pg.draw.line(self.screen, BLACK, self.rotate(left, self.phase), self.rotate(right, self.phase), axis_width)
        except TypeError:
            return

    # Gets coords for imaginary lines which will be added to the screen
    def imag_line_coords(self):
        x_coords = self.x_coords()
        tops_y = [self.tick_ys()[0] if self.real_mode else -self.padding] * len(x_coords)
        tops = list(zip(x_coords, tops_y))
        bottoms_y = [self.tick_ys()[1] if self.real_mode else self.screen.get_height() + self.padding] * len(x_coords)
        bottoms = list(zip(x_coords, bottoms_y))
        return [(self.rotate(pair[0], self.phase), self.rotate(pair[1], self.phase)) for pair in zip(tops, bottoms)]

    # Gets coords for real lines which will be added to the screen
    def real_line_coords(self):
        y_coords = self.y_coords()
        lefts_x = [-self.padding] * len(y_coords)
        lefts = list(zip(lefts_x, y_coords))
        rights_x = [self.screen.get_width() + self.padding] * len(y_coords)
        rights = list(zip(rights_x, y_coords))
        return [(self.rotate(pair[0], self.phase), self.rotate(pair[1], self.phase)) for pair in zip(lefts, rights)]

    # Creates the x coords for vertical lines
    def x_coords(self):
        offset_center = self.screen.get_width() / 2 + (self.pixel_offset[0] % self.pixel_spacing)
        neg = np.arange(offset_center, -self.padding, -self.pixel_spacing)
        pos = np.arange(offset_center + self.pixel_spacing, self.screen.get_width() + self.padding, self.pixel_spacing)
        return np.append(neg, pos)

    # Creates the y coords for horizontal lines
    def y_coords(self):
        offset_center = self.screen.get_height() / 2 + (self.pixel_offset[1] % self.pixel_spacing)
        pos = np.arange(offset_center, -self.padding, -self.pixel_spacing)
        neg = np.arange(offset_center + self.pixel_spacing, self.screen.get_height() + self.padding, self.pixel_spacing)
        return np.append(pos, neg)

    # Performs a rotation of a point about the center of the screen
    def rotate(self, pt, angle):
        pt_minus_center = pt[0] - self.screen.get_width() / 2, pt[1] - self.screen.get_height() / 2
        rot_matrix = np.array([[np.cos(angle), np.sin(angle)], [-np.sin(angle), np.cos(angle)]])
        result = np.matmul(rot_matrix, np.array(pt_minus_center))
        return result[0] + self.screen.get_width() / 2, result[1] + self.screen.get_height() / 2

    # Sets the amount of padding to apply in case of rotation
    def set_padding(self):
        if self.screen.get_height() < self.screen.get_width():
            to_subtract = self.screen.get_height()
        else:
            to_subtract = self.screen.get_width()
        self.padding = (np.sqrt(self.screen.get_width() ** 2 + self.screen.get_height() ** 2) - to_subtract) / 2

    # Determines whether a rect for given coords is in the screen
    def rect_in_screen(self, rect):
        return self.in_screen(rect.topleft) or self.in_screen(rect.topright) or self.in_screen(rect.bottomleft) or \
            self.in_screen(rect.bottomright)

    # Determines whether a given coordinate is within the display or not
    def in_screen(self, pt):
        return 0 <= pt[0] <= self.screen.get_width() and 0 <= pt[1] <= self.screen.get_height()

    # Returns the upper and lower y-coordinates of the tick marks in real mode
    def tick_ys(self):
        return self.screen.get_height() / 2 - tick_mark_height, self.screen.get_height() / 2 + tick_mark_height
    
    # Returns the upper and lower y-coordinates of the zero mark in real mode
    def zero_ys(self):
        return self.screen.get_height() / 2 - zero_mark_height, self.screen.get_height() / 2 + zero_mark_height
