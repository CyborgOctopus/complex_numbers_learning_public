import sys
import math
import cmplx_animation_utils
from ComplexPlane import ComplexPlane
from Button import Button
from shared_functions import *

# Color constants
WHITE = (255, 255, 255)

# Display parameters
width = 800
height = 800
vec_color_1 = (0, 200, 0)
vec_color_2 = (0, 0, 200)
initial_spacing = 1
initial_half_range = 5
range_multiplier = 1.1
phase_step = 0.01
button_top_left_y = 50
button_step = 60
real_line_click_tolerance = 3
real_button_pic_addresses = [("home.jpg", "home1.jpg"),  ("plus.jpg", "plus1.jpg"), ("times.jpg", "times1.jpg")]
cmplx_button_pic_addresses = [("rotate_c.jpg", "rotate_c1.jpg"), ("rotate_cc.jpg", "rotate_cc1.jpg")]
real_button_names = ["home", "plus", "times"]
cmplx_button_names = ["rotate_c", "rotate_cc"]
real_title = "Animated real line"
cmplx_title = "Animated complex plane"

# Creates buttons based on the provided data
def get_buttons():
    button_pic_addresses = real_button_pic_addresses[::-1] if plane.real_mode else cmplx_button_pic_addresses[::-1] \
        + real_button_pic_addresses[::-1]
    button_names = real_button_names[::-1] if plane.real_mode else cmplx_button_names[::-1] + real_button_names[::-1]
    button_pics = [[pg.image.load("images/" + button_pic_address[i]) for i in range(2)] for button_pic_address
                   in button_pic_addresses]
    buttons = [Button(screen, width - button_step * (i + 1), button_top_left_y, button_pics[i][0],
                      button_pics[i][1])
               for i in range(len(button_pics))]
    return {button_names[i]: buttons[i] for i in range(len(buttons))}


# Setup
screen = None
plane = None
buttons = None


# Executes the animation loop
def animate(real_mode):

    global screen
    screen = create_screen(width, height)
    global plane
    plane = ComplexPlane(screen, initial_spacing, initial_half_range, real_mode=real_mode)
    global buttons
    buttons = get_buttons()

    pg.init()
    set_title(real_mode)
    plane.display()
    display_buttons()
    pan = False
    time_clicked_down = -100
    zoom_in = False
    zoom_out = False
    cmplx_animation_utils.funcs += [display_buttons, adjust_spacing]
    running = True

    # Main loop
    while running:
        adjust_spacing()
        pg.display.flip()
        prev_mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():

            if event.type == pg.QUIT:
                running = False

            # Sets 'pan' to True and records the click time so a point can be plotted if there's a rapid release
            elif event.type == pg.MOUSEBUTTONDOWN:
                pan = True
                time_clicked_down = pg.time.get_ticks()

            # If 'pan' is True (the mouse button is down) and the mouse is moving, pans the screen
            elif event.type == pg.MOUSEMOTION and pan:
                mouse_pos = event.pos
                x_diff = mouse_pos[0] - prev_mouse_pos[0]
                y_diff = mouse_pos[1] - prev_mouse_pos[1]
                rot_x_diff = x_diff * math.cos(plane.phase) - y_diff * math.sin(plane.phase)
                rot_x_offset = rot_x_diff * 2 * plane.half_range / width
                rot_y_diff = x_diff * math.sin(plane.phase) + y_diff * math.cos(plane.phase)
                rot_y_offset = rot_y_diff * 2 * plane.half_range / width
                plane.set_offset((plane.offset + rot_x_offset + rot_y_offset * 1j))
                wipe_and_redisplay()

            # Sets 'pan' to False if the mouse is released and plots a point if the release happened right after a press
            elif event.type == pg.MOUSEBUTTONUP:
                pan = False
                coord = None
                if real_mode and abs(pg.mouse.get_pos()[1] - screen.get_height() / 2) <= real_line_click_tolerance:
                    coord = plane.snap_to_grid((pg.mouse.get_pos()[0], screen.get_height() / 2))
                elif not real_mode and pg.time.get_ticks() - time_clicked_down <= 100:
                    coord = plane.snap_to_grid(pg.mouse.get_pos())
                if coord is not None:
                    plane.plot_point(coord)
                    plane.add_coords(coord)
                    plane.display_coords()

            # If the up arrow or down arrow is pressed, prepares to zoom in or out, respectively
            elif event.type == pg.KEYDOWN:
                keys = pg.key.get_pressed()
                if keys[pg.K_UP]:
                    zoom_in = True
                if keys[pg.K_DOWN]:
                    zoom_out = True

            # If the up or down arrow keys are released, stops zooming in that direction.
            elif event.type == pg.KEYUP:
                keys = pg.key.get_pressed()
                if not keys[pg.K_UP]:
                    zoom_in = False
                if not keys[pg.K_DOWN]:
                    zoom_out = False

        # Performs a zoom in or zoom out
        if zoom_in or zoom_out:
            pg.time.wait(50)
            if zoom_in and plane.half_range > cmplx_animation_utils.lower_range_limit:
                plane.set_half_range(plane.half_range / range_multiplier)
            if zoom_out and plane.half_range < cmplx_animation_utils.upper_range_limit:
                plane.set_half_range(plane.half_range * range_multiplier)
            wipe_and_redisplay()

        if pg.mouse.get_pressed()[0]:
            for key, button in buttons.items():
                button.update_click_status()

        if buttons["home"].is_clicked():
            cmplx_animation_utils.center(plane)
            cmplx_animation_utils.smooth_half_range_transition(plane, initial_half_range)
            cmplx_animation_utils.smooth_phase_transition(plane, 0)
            plane.set_spacing(initial_spacing)
            wipe_and_redisplay()
            buttons["home"].unclick()
            display_buttons()

        elif buttons["plus"].is_clicked():
            cmplx_animation_utils.add(plane)
            buttons["plus"].unclick()
            display_buttons()

        elif buttons["times"].is_clicked():
            cmplx_animation_utils.mul(plane)
            buttons["times"].unclick()
            display_buttons()

        elif not real_mode and buttons["rotate_c"].is_clicked():
            buttons["rotate_c"].display()
            plane.set_phase((plane.phase - phase_step) % math.tau)
            wipe_and_redisplay()
            buttons["rotate_c"].unclick()
            display_buttons()

        elif not real_mode and buttons["rotate_cc"].is_clicked():
            buttons["rotate_cc"].display()
            plane.set_phase((plane.phase + phase_step) % math.tau)
            wipe_and_redisplay()
            buttons["rotate_cc"].unclick()
            display_buttons()
    pg.quit()


# Displays all buttons to the screen
def display_buttons():
    for key, button in buttons.items():
        button.display()


# Adjusts the spacing of the plane to keep the grid size reasonable
def adjust_spacing():
    if plane.half_range >= initial_half_range ** 2 * plane.spacing or plane.half_range <= plane.spacing:
        plane.set_spacing(plane.half_range / initial_half_range)
        wipe_and_redisplay()


# Wipes the screen and redraws everything to it
def wipe_and_redisplay():
    screen.fill(WHITE)
    plane.display()
    display_buttons()


# Creates a title for the window
def set_title(real_mode):
    if real_mode:
        pg.display.set_caption(real_title)
    else:
        pg.display.set_caption(cmplx_title)


# Convenience functions defining the real and complex animation modes
def animate_real():
    animate(real_mode=True)


def animate_complex():
    animate(real_mode=False)


if __name__ == '__main__':
    animate(bool(input("Real line mode: ")))
