import pygame as pg
import math

# Color constants
BLACK = (0, 0, 0)

# Display parameters
radius = 250
circle_thickness = 3
point_radius = 5
revolving_point_color = (255, 0, 255)
x_oscillator_color = (255, 0, 0)
y_oscillator_color = (0, 0, 255)
axis_color = (0, 255, 0)
display_left_top_x = (600, 100)
big_font_size = 25
small_font_size = 20
font_offset = 30
round_num = 1
bigger_round_num = 2


class EulerCircle:

    def __init__(self, screen, phase=0):
        self.screen = screen
        self.phase = phase
        self.center = round(self.screen.get_width() / 2), round(self.screen.get_height() / 2)
        self.x_oscillator_center = 0
        self.y_oscillator_center = 0
        self.revolving_point_center = 0
        self.update_point_centers()

    # Public

    def display(self):
        self.draw_big_circle()
        self.draw_axes()
        self.plot_revolving_point()
        self.plot_x_oscillator()
        self.draw_x_oscillator_line()
        self.plot_y_oscillator()
        self.draw_y_oscillator_line()
        self.display_point_vals()
        self.display_formula()

    def set_phase(self, phase):
        self.phase = phase
        self.update_point_centers()

    # Private

    def draw_big_circle(self):
        pg.draw.circle(self.screen, BLACK, self.center, radius, circle_thickness)

    def draw_axes(self):
        left = self.center[0] - radius, self.center[1]
        right = self.center[0] + radius, self.center[1]
        pg.draw.line(self.screen, axis_color, left, right)
        top = self.center[0], self.center[1] - radius
        bottom = self.center[0], self.center[1] + radius
        pg.draw.line(self.screen, axis_color, top, bottom)

    def plot_revolving_point(self):
        pg.draw.circle(self.screen, revolving_point_color, self.revolving_point_center, point_radius)

    def plot_x_oscillator(self):
        pg.draw.circle(self.screen, x_oscillator_color, self.x_oscillator_center, point_radius)

    def draw_x_oscillator_line(self):
        pg.draw.line(self.screen, y_oscillator_color, self.x_oscillator_center, self.revolving_point_center)

    def plot_y_oscillator(self):
        pg.draw.circle(self.screen, y_oscillator_color, self.y_oscillator_center, point_radius)

    def draw_y_oscillator_line(self):
        pg.draw.line(self.screen, x_oscillator_color, self.y_oscillator_center, self.revolving_point_center)

    def display_formula(self):
        render = pg.font.Font(None, big_font_size).render("e^(i" + str(round(self.phase, round_num)) + ")", True, BLACK)
        self.screen.blit(render, display_left_top_x)

    def display_point_vals(self):
        x_coord = str(round(math.cos(self.phase), bigger_round_num))
        y_coord = str(round(math.sin(self.phase), bigger_round_num))
        h_pt_render = pg.font.Font(None, small_font_size).render(x_coord, True, BLACK)
        self.screen.blit(h_pt_render, (self.x_oscillator_center[0], self.x_oscillator_center[1] + font_offset))
        v_pt_render = pg.font.Font(None, small_font_size).render(y_coord + "i", True, BLACK)
        self.screen.blit(v_pt_render, (self.y_oscillator_center[0], self.y_oscillator_center[1] + font_offset))
        r_pt_render = pg.font.Font(None, small_font_size).render(x_coord + " + " + y_coord + "i", True, BLACK)
        self.screen.blit(r_pt_render, (self.revolving_point_center[0], self.revolving_point_center[1] - font_offset))

    def update_point_centers(self):
        self.x_oscillator_center = round(self.center[0] + radius * math.cos(self.phase)), self.center[1]
        self.y_oscillator_center = self.center[0], round(self.center[1] - radius * math.sin(self.phase))
        self.revolving_point_center = self.x_oscillator_center[0], self.y_oscillator_center[1]
