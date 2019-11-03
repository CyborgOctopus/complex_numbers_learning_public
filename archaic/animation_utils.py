import pygame as pg
import numpy as np

# Color constants
WHITE = (255, 255, 255)

# Display and animation parameters
pixel_margin = 20
origin_radius = 10
origin_color = (0, 0, 200)
pt_radius = 5
pt_color = (0, 200, 0)
half_range_multiplier = 1.05
fps = 0
flipping_half_range_multiplier = 50

# Stores points that should be continually displayed
persistent_pts = []


# Stores functions which should be called during every frame of animation
funcs = []


# TODO Multiplication by negatives is messed up
# Performs animated multiplication on all currently plotted points on a real line
def mul(real_line):
    if real_line.offset != 0:
        center(real_line)
    sorted_pts = [x for x in sorted(real_line.added_coords, key=abs) if x != 0]
    while len(sorted_pts) > 1:
        current_pt = sorted_pts[0]
        mul_two(real_line, current_pt, sorted_pts[1])
        sorted_pts = [x for x in sorted(real_line.added_coords, key=abs) if x != 0]
    if 0 in real_line.added_coords:
        mul_two(real_line, sorted_pts[0], 0)
    update_and_wait(real_line)


# Graphically multiplies two points on the real number line
def mul_two(real_line, pt1, pt2):
    real_line.add_coord(1)
    resize_to_pts(real_line)
    real_line.added_coords.remove(1)
    persistent_pts.append((real_line.convert_to_pixel_coord(1), real_line.screen.get_height() // 2))
    prod_pixel_loc = (real_line.convert_to_pixel_coord(pt2), real_line.screen.get_height() // 2)
    persistent_pts.append(prod_pixel_loc)
    real_line.added_coords.remove(pt2)
    if pt1 != 0:
        smooth_half_range_transition(real_line, real_line.half_range * pt1)
        real_line.added_coords.remove(pt1)
        real_line.add_coord(real_line.convert_to_line_coord(prod_pixel_loc[0]))
    persistent_pts.clear()


# Performs animated addition on all currently plotted points on a real line
def add(real_line):
    sorted_pts = sorted(real_line.added_coords)
    while len(sorted_pts) > 1:
        current_pt = sorted_pts[0]
        add_two(real_line, current_pt, sorted_pts[1])
        sorted_pts = sorted(real_line.added_coords)
    update_and_wait(real_line)


# Graphically adds two points on the real number line
def add_two(real_line, pt1, pt2):
    real_line.add_coord(0)
    resize_to_pts(real_line)
    real_line.added_coords.remove(0)
    persistent_pts.append((real_line.convert_to_pixel_coord(0), real_line.screen.get_height() // 2))
    sum_pixel_loc = (real_line.convert_to_pixel_coord(pt2), real_line.screen.get_height() // 2)
    persistent_pts.append(sum_pixel_loc)
    real_line.added_coords.remove(pt2)
    smooth_offset_transition(real_line, real_line.offset - pt1) # TODO - should it be negative?
    real_line.added_coords.remove(pt1)
    real_line.add_coord(real_line.convert_to_line_coord(sum_pixel_loc[0]))
    persistent_pts.clear()


# Centers the real line on 0
def center(real_line):
    real_line.added_coords.append(0)
    resize_to_pts(real_line)
    real_line.added_coords.remove(0)
    smooth_offset_transition(real_line, 0)


# Resizes the real line so that all points are visible
def resize_to_pts(real_line):
    line_margin = real_line.convert_to_line_coord(pixel_margin) - real_line.convert_to_line_coord(0)
    new_half_range = get_farthest_dist_from_center(real_line) + line_margin
    smooth_half_range_transition(real_line, new_half_range)


# Flips the real line, swapping negative and positive
def flip(real_line):
    real_line.set_half_range(-real_line.half_range)


# Returns the absolute value of the distance of the farthest coordinate from the center of the screen
def get_farthest_dist_from_center(real_line):
    largest = 0
    for pt in real_line.added_coords:
        if abs(pt - real_line.offset) > largest:
            largest = abs(pt - real_line.offset)
    return largest


# Causes smooth transition of offset in the real line animation
def smooth_offset_transition(real_line, offset):
    dist = offset - real_line.offset
    vals = np.linspace(real_line.offset, offset, abs(real_line.screen.get_width() / (2 * real_line.half_range) * dist))
    for val in vals:
        real_line.set_offset(val)
        update_and_wait(real_line)


# Causes a smooth transition in half range of the real line animation
def smooth_half_range_transition(real_line, half_range):
    if np.sign(real_line.half_range) != np.sign(half_range):
        smooth_half_range_transition(real_line, flipping_half_range_multiplier * real_line.half_range)
        real_line.set_half_range(-real_line.half_range)
    quotient = half_range / real_line.half_range
    vals = np.linspace(real_line.half_range, half_range, round(abs(np.log(quotient) / np.log(half_range_multiplier))))
    for val in vals:
        real_line.set_half_range(val)
        update_and_wait(real_line)


# Updates the real line and pauses so that the animation doesn't move too fast
def update_and_wait(real_line):
    real_line.screen.fill(WHITE)
    real_line.display()
    [func() for func in funcs]
    draw_persistent_pts(real_line)
    pg.display.flip()


# Draws points in the persistent points list during every frame of animation
def draw_persistent_pts(real_line):
    for pt in persistent_pts:
        pg.draw.circle(real_line.screen, pt_color, pt, pt_radius)
