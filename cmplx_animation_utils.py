import pygame as pg
import numpy as np
import cmath

# Color constants
WHITE = (255, 255, 255)

# Display and animation parameters
pixel_margin = 20
origin_radius = 10
origin_color = (0, 0, 200)
pt_radius = 5
pt_color = (0, 200, 0)
half_range_multiplier = 1.05
phase_dist_multiplier = 100
upper_range_limit = 1e100
lower_range_limit = 1e-100

# Stores points that should be continually displayed
persistent_pts = []


# Placeholder for functions which should be called during every frame of the animation
funcs = []


# Performs animated multiplication on all currently plotted points
def mul(plane):
    if plane.offset != 0:
        center(plane)
    sorted_pts = sorted(plane.added_coords, key=abs)
    while len(sorted_pts) > 1:
        prev_length = len(sorted_pts)
        pt1, pt2 = sorted_pts[0], sorted_pts[1]
        if pt1 == 0:
            pt1, pt2 = pt2, pt1
        mul_two(plane, pt1, pt2)
        sorted_pts = sorted(plane.added_coords, key=abs)
        if prev_length == len(sorted_pts):
            break
    update_and_wait(plane)


# Graphically multiplies two points on the complex plane
def mul_two(plane, pt1, pt2):
    resize_to_pts(plane, [0, 1, pt1, pt2])
    if pt2 == 0 and plane.half_range * abs(pt1) >= upper_range_limit:
        plane.remove_coords(pt1)
    elif abs(pt1 * pt2) <= upper_range_limit:
        persistent_pts.append(plane.convert_to_pixel_coords(1))
        prod_pixel_loc = plane.convert_to_pixel_coords(pt2)
        persistent_pts.append(prod_pixel_loc)
        plane.remove_coords(pt2)
        if pt1 != 0:
            smooth_phase_transition(plane, plane.phase - cmath.phase(pt1))
            smooth_half_range_transition(plane, plane.half_range * abs(pt1))
            plane.remove_coords(pt1)
            plane.add_coords(pt1 * pt2)
        persistent_pts.clear()


# Performs animated addition on all currently plotted points
def add(plane):
    sorted_pts = sorted(plane.added_coords, key=abs)
    while len(sorted_pts) > 1:
        prev_length = len(sorted_pts)
        current_pt = sorted_pts[0]
        add_two(plane, current_pt, sorted_pts[1])
        sorted_pts = sorted(plane.added_coords, key=abs)
        if prev_length == len(sorted_pts):
            break
    update_and_wait(plane)


# Graphically adds two points on the complex plane
def add_two(plane, pt1, pt2):
    if abs(pt1 + pt2) <= upper_range_limit:
        resize_to_pts(plane, [0, pt1, pt2])
        persistent_pts.append(plane.convert_to_pixel_coords(0))
        sum_pixel_loc = plane.convert_to_pixel_coords(pt2)
        persistent_pts.append(sum_pixel_loc)
        plane.remove_coords(pt2)
        smooth_offset_transition(plane, plane.offset - pt1.real + pt1.imag * 1j) # TODO - fix!
        plane.remove_coords(pt1)
        plane.add_coords(pt1 + pt2)
        persistent_pts.clear()


# Centers the plane on the origin
def center(plane):
    if plane.offset != 0:
        resize_to_pts(plane, [0])
        smooth_offset_transition(plane, 0)


# Resizes the plane so that all points are visible
def resize_to_pts(plane, pts_lst):
    new_half_range = get_farthest_dist_from_center(plane, pts_lst)
    smooth_half_range_transition(plane, new_half_range)


# Returns the absolute value of the distance of the farthest coordinate from the center of the screen
def get_farthest_dist_from_center(plane, pts_lst):
    largest = 0
    for pt in pts_lst:
        if abs(pt - plane.offset) > largest:
            largest = abs(pt - plane.offset)
    return largest


# Causes a smooth transition in the offset of the complex plane animation
def smooth_offset_transition(plane, offset):
    dist = abs(offset - plane.offset)
    vals = list(np.linspace(plane.offset, offset, plane.screen.get_width() / (2 * plane.half_range) * dist)) + [offset]
    for val in vals:
        plane.set_offset(val)
        update_and_wait(plane)


# Causes a smooth transition in the half range of the complex plane animation
def smooth_half_range_transition(plane, half_range):
    quotient = half_range / plane.half_range
    log = abs(round(np.log(quotient) / np.log(half_range_multiplier)))
    vals = list(np.linspace(plane.half_range, half_range, log)) + [half_range]
    for val in vals:
        plane.set_half_range(val)
        update_and_wait(plane)


# Causes a smooth transition in the phase of the complex plane animation
def smooth_phase_transition(plane, phase):
    new_phase = optimal_phase(plane.phase, phase)
    vals = np.linspace(plane.phase, new_phase, abs(phase_dist_multiplier * (new_phase - plane.phase)))
    for val in vals:
        plane.set_phase(val)
        update_and_wait(plane)


# Finds a phase which will result in the shortest travel path from 'starting_phase' to 'target_phase'
def optimal_phase(starting_phase, target_phase):
    phase_dist = target_phase - starting_phase
    if phase_dist % cmath.tau < cmath.pi:
        return starting_phase + phase_dist % cmath.tau
    else:
        return starting_phase + phase_dist % -cmath.tau


# Updates the plane and pauses so the animation doesn't move too fast
def update_and_wait(plane):
    pg.event.pump()  # Make sure pygame doesn't freeze up because the event queue isn't getting called
    plane.screen.fill(WHITE)
    [func() for func in funcs]
    plane.display()
    draw_persistent_pts(plane)
    pg.display.flip()


# Draws points in the persistent points list during every frame of the animation
def draw_persistent_pts(plane):
    for pt in persistent_pts:
        pg.draw.circle(plane.screen, pt_color, pt, pt_radius)
