import pygame as pg
import animation_utils
from RealLine import RealLine
from Button import Button

# Color constants
WHITE = (255, 255, 255)

# Display parameters
width = 800
height = 800
vec_color_1 = (0, 200, 0)
vec_color_2 = (0, 0, 200)
spacing = 1
initial_half_range = 10
line_click_tolerance = 3
range_multiplier = 1.1
button_top_left_y = 50
home_top_left_x = 600
plus_top_left_x = 660
times_top_left_x = 720


# Creates the pygame window.
def create_screen(width, height):
    screen = pg.display.set_mode((width, height))
    screen.fill(WHITE)
    return screen


# Gets buttons for returning to home view, addition, and multiplication
def get_buttons():
    home_rest = pg.image.load("images/home.jpg")
    home_clicked = pg.image.load("images/home1.jpg")
    plus_rest = pg.image.load("images/plus.jpg")
    plus_clicked = pg.image.load("images/plus1.jpg")
    times_rest = pg.image.load("images/times.jpg")
    times_clicked = pg.image.load("images/times1.jpg")
    home = Button(screen, home_top_left_x, button_top_left_y, home_rest, home_clicked)
    plus = Button(screen, plus_top_left_x, button_top_left_y, plus_rest, plus_clicked)
    times = Button(screen, times_top_left_x, button_top_left_y, times_rest, times_clicked)
    return {"home": home, "plus": plus, "times": times}


# Setup
pg.init()
screen = create_screen(width, height)
rl = RealLine(screen, spacing, initial_half_range)
buttons = get_buttons()


# Executes the animation loop.
def animate():

    rl.set_half_range(initial_half_range)
    rl.display()
    display_buttons()
    running = True
    pan = False
    zoom_in = False
    zoom_out = False
    pts_lst = []
    animation_utils.funcs += [display_buttons, adjust_spacing]

    # Main loop
    while running:
        adjust_spacing()
        pg.display.flip()
        prev_mouse_x = pg.mouse.get_pos()[0]
        for event in pg.event.get():

            if event.type == pg.QUIT:
                running = False

            # Sets 'pan' to True and plots a point if the line has been clicked. Also handles button clicks
            elif event.type == pg.MOUSEBUTTONDOWN:
                pan = True
                mouse_x, mouse_y = pg.mouse.get_pos()
                if abs(mouse_y - screen.get_height() / 2) <= line_click_tolerance:
                    line_coord = rl.snap_to_mark(mouse_x)
                    pts_lst.append(line_coord)
                    rl.plot_point(line_coord)
                    rl.add_coord(line_coord)
                    rl.display_coords()
                for key, button in buttons.items():
                    button.update_click_status()

            # Sets 'pan' to False if the mouse is released.
            elif event.type == pg.MOUSEBUTTONUP:
                pan = False

            # If 'pan' is True (the mouse button is down) and the mouse is moving, pans the screen.
            elif event.type == pg.MOUSEMOTION and pan:
                mouse_x = event.pos[0]
                rl.set_offset(rl.offset + (mouse_x - prev_mouse_x) * 2 * rl.half_range / width)
                wipe_and_redisplay()

            # If the up arrow or down arrow keys are depressed, prepares to zoom in or out, respectively.
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

        # Performs a zoom in or zoom out.
        if zoom_in or zoom_out:
            pg.time.wait(50)
            if zoom_in:
                rl.set_half_range(rl.half_range / range_multiplier)
            if zoom_out:
                rl.set_half_range(rl.half_range * range_multiplier)
            wipe_and_redisplay()

        if buttons["home"].is_clicked():
            animation_utils.center(rl)
            animation_utils.smooth_half_range_transition(rl, initial_half_range)
            buttons["home"].unclick()
            display_buttons()

        elif buttons["plus"].is_clicked():
            animation_utils.add(rl)
            buttons["plus"].unclick()
            display_buttons()

        elif buttons["times"].is_clicked():
            animation_utils.mul(rl)
            buttons["times"].unclick()
            display_buttons()


# Wipes the screen and redraws everything to it
def wipe_and_redisplay():
    screen.fill(WHITE)
    rl.display()
    display_buttons()


# Displays all buttons to the screen
def display_buttons():
    for key, button in buttons.items():
        button.display()


# Adjusts the spacing of the line to keep the distance between tick marks reasonable
def adjust_spacing():
    if rl.half_range >= initial_half_range ** 2 * rl.spacing:
        rl.set_spacing(initial_half_range * rl.spacing)
        wipe_and_redisplay()

    elif rl.half_range <= rl.spacing:
        rl.set_spacing(rl.spacing / initial_half_range)
        wipe_and_redisplay()


animate()
