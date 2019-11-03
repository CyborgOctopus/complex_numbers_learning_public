import pygame as pg
import tkinter as tk
import tkinter.messagebox as tkmb
import animate_complex
from animate_euler import animate_euler
from PIL import Image, ImageTk

# Display variables
root_width_times_height = "800x800"
title_pad = 100
title_font_size = 18
normal_font_size = 10
font = "cambria"
title = "Welcome to the World of Complex Numbers!"
real_button_title = "Explore the Real Number Line"
cmplx_button_title = "Explore the Complex Plane"
euler_button_title = "Visualize Euler's Formula"
msg = """
Instructions for the real number line and complex plane

To zoom in, press the up arrow key.
To zoom out, press the down arrow key.
To return to the default view, press the Home button.
To add up all of the numbers currently selected, press the + button.
To multiply all of the numbers currently selected, press the x button.
To rotate clockwise in the complex plane, press the button with a curved arrow pointing clockwise.
To rotate counterclockwise in the complex plane, press the button with a curved arrow pointing counterclockwise.
There is a range limit, so you will not be able to zoom in or out past a certain point, and additions or multiplications 
that would result in numbers outside the range limit are not allowed.
TIP: to get rid of all the numbers currently selected on the screen, multiply by zero.


About the Euler’s formula visualization

This shows the standard (real + imaginary) representation of complex numbers on the unit circle along with
 the e^(i * theta) representation, demonstrating Euler's formula. For more explanation, read the accompanying document. 
"""


class Menu:

    def __init__(self):
        self.root = tk.Tk()
        self.setup_root()
        self.top_bar = tk.Frame(self.root)
        self.top_bar.pack(anchor=tk.W)
        self.msg_text = msg
        self.info_button = tk.Button(self.top_bar)
        self.setup_info_button()
        self.title = tk.Label(self.root)
        self.setup_title()
        self.button_region = tk.Frame(self.root)
        self.button_region.pack()
        self.real_animation_button = tk.Button(self.button_region)
        self.setup_real_animation_button()
        self.cmplx_animation_button = tk.Button(self.button_region)
        self.setup_cmplx_animation_button()
        self.euler_animation_button = tk.Button(self.button_region)
        self.setup_euler_animation_button()
        self.logo_label = tk.Label(self.root)
        self.logo_label.pack()
        self.logo = None
        self.setup_logo()

    def display(self):
        self.root.mainloop()

    def setup_root(self):
        self.root.geometry(root_width_times_height)
        self.root.configure(background='white')
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.root.title(title)

    def setup_info_button(self):
        self.info_button.config(font=(font, normal_font_size), text="       ?       ", command=self.display_popup)
        self.info_button.pack(side=tk.LEFT)

    def setup_title(self):
        self.title.pack(pady=title_pad)
        self.title.config(font=(font, title_font_size), text=title)

    def setup_real_animation_button(self):
        self.real_animation_button.config(font=(font, normal_font_size))
        self.real_animation_button.config(text=real_button_title, command=animate_complex.animate_real)
        self.real_animation_button.pack(side=tk.LEFT)

    def setup_cmplx_animation_button(self):
        self.cmplx_animation_button.config(font=(font, normal_font_size))
        self.cmplx_animation_button.config(text=cmplx_button_title, command=animate_complex.animate_complex)
        self.cmplx_animation_button.pack(side=tk.LEFT)

    def setup_euler_animation_button(self):
        self.euler_animation_button.config(font=(font, normal_font_size))
        self.euler_animation_button.config(text=euler_button_title, command=animate_euler)
        self.euler_animation_button.pack(side=tk.LEFT)

    def setup_logo(self):
        self.logo = ImageTk.PhotoImage(Image.open("images/logo.jpg"))
        self.logo_label.config(image=self.logo)

    def display_popup(self):
        tkmb.showinfo("information", self.msg_text)

    def quit(self):
        self.root.destroy()


