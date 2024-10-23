"""
Python Sierpinski Triangle Example .   Programming with Pybox Demonstration Program.

---------------------------
Sierpinski Triangle Example
---------------------------
 
From Wikipedia: 

    "The Sierpiński triangle, also called the Sierpiński gasket or Sierpiński sieve, is a fractal with the overall shape of
    an equilateral triangle, subdivided recursively into smaller equilateral triangles."

In programming practice, this is a pretty simple implementation and small program to write. 

However, it also turns out to be a good (and also simple) example of recursive programming. 

---------------------
Notes on this Example
---------------------

This is a good example of using graphics and doing something mathematically interesting at the same time, showing many Pybox function
mixed in with the main algorithm. 

Input box       -- This example shows using an input box in the Dev Window to get the level of the Sierpinski Triangle

Range Validation    -- Using the range keyword (from 0 to 11) will validate these values in the input box, with a 
                       'ok'-based dialog box that lets the user know the value is out of range, then returning to the input
                       
                       This allows setting range values without having to validate them, since Pybox does it already.
                       
                       using the keyword 'cancel_ok=True' will allow the input box to be canceled with any value showing
                       (e.g. by pressing the escape key or cancel button (when present), in which case the function
                       input_box.was_canceled() can be called to determine if the input box was canceled or has a valid number
                       within the range specified)
                       
cls_radial()    -- this shows using cls_radial() instead of the typical cls() to form a radial clear window effect. It's 
                   basically for aesthetic reasons, and, in this case, directs the eye to the Sierpinski triangle much more effectively
                   than a single-color cls() or vertical-gradient cls(). 
                   
win.get_window_center()   -- this gets the window center to use to calculate the center of the triangle. 
                             it is converted to an array so that it can be used with math functions later on. 
                                                
Various {}-based write formatting -- As with Python, in general, Pybox uses '{}' directives for text, such as 
                                     "{75}", which will set the text size to 75, or "{yellow}", will set the text color
                                     to yellow.
                                     
                                     These are used in the program below.
                                     
                                     Note that when a formatted string is used in Python (which also uses {} directives, then the 
                                     Pybox directives use double {{}}, such as {{75}} for a 75-point font, rather than the "{75}", which
                                     can be used when there is no string formatting within python.
"""

import pybox            # import pybox module
import numpy as np      # and numpy module

win = pybox.new_window();           # create main Pybox window

win.cls_radial("darkblue,black")    # clear window with a radial gradient. We could also use win.cls() for plain color or vertical gradient.

# create an input box to get a number from 0-11
# --> numbers_only   -- allows only numbers to be entered
# --> range(0,11)    -- a 'Ok' dialog box will come up if numbers outside of this range are entered. 
#
#                       note: Though not used here, the keyword "allow_cancel=True" allows canceling the dialog box, 
#                       and input_box.was_canceled() can be called to determine if it was canceled.
#
#                       In this case, there is no ok-to-cancel, so we don't worry about it being exited with a bad number

input_box = pybox.dev_inputbox("Enter level 0-11",numbers_only=True,range=(0,11))

center = np.array(win.get_window_center()); # Get the window center (as a list), but convert to an array so we can do some math on it

# Write a large (60-point) message about entering the initial level.
# just=center -- this centers the text in the window
win.write("{60}Enter level to draw Sierpinski Triangle.", just="center");

colors = ("green","yellow","purple")        # define come colors for the three main sections of the triangle display

# ----------------------------
# Main Siperinski Drawing Loop
# ---------------------------- 
# 
# Calculate the triangles in a recursive loop from 0 to our maximum depth

def calc_triangle(win : pybox.Window,level,top_point,left_point,right_point,depth) :
    if not level :              # if we're done (at the end of the recursion), draw the triangle
        win.draw.fill_triangle(top_point,left_point,right_point,calc_triangle.use_color)
    else :
        left_mid = (top_point + left_point) / 2
        right_mid =(top_point + right_point) / 2
        bottom_mid = (left_point + right_point) / 2
        
        if not depth : calc_triangle.use_color = colors[0]      # set colors for largest sections (when we are at depth 0)
        calc_triangle(win, level - 1, top_point, left_mid, right_mid,depth + 1);
        
        if not depth : calc_triangle.use_color = colors[1]
        calc_triangle(win, level - 1, left_mid, left_point, bottom_mid,depth + 1);
        
        if not depth : calc_triangle.use_color = colors[2]
        calc_triangle(win, level - 1, right_mid, bottom_mid, right_point, depth + 1);

calc_triangle.use_color = colors[0]     # Set initial color value for calc_triangle function (otherwise we get an error)

# ---------------------
# Main Event Input Loop
# ---------------------
#
# This loop will continue until the window is closed (pybox.get_event() returns False)
#
# In this loop, we can look for events that have occurred, or just get their status or values directly.
# 
# input_box.return_pressed() -- tells us someone entered the return or otherwise selected a number in the input box

while pybox.get_event() :
    if input_box.return_pressed() :         # we could call a function here, but the code is inlined below for easy reading
        level = input_box.get_integer()     # get the value of the input box
        
        win.cls()                           # clear the window display (it will keep with the last radial cls values) --
                                            # win.cls() (when empty) remembers the last cls() and just repeats it. 
                                            
        # Write some information the opt of the window:
        # {40},{15}, etc    -- these set the font
        # {cyan}            -- sets the text color to cyan
        # just="top center" -- Tells the write function to center the text on the top of the window's display
        # pady=20           -- Brings down the text 20 pixels so it isn't so pressed against the top of the window
        
        win.write("{{40}}Python Sierpinski Triangle\n{{15}}{{cyan}}Level {}".format(level), just="top_center", pady=20)
    
        # Set the initial triangle.  We know the windows is 1200x800 by default, but we could also make these numbers calculated
        # based on win.get_window_size().
        #
        # In this case, we just establish (0,0) at the center and come back some values that make it look good in the window, 
        # using the window's center ('center') we got from win.get_window_center() to make (0,0) the center of the window by adding
        # it's value to the points below. 
        
        p = [(0,-300), (500,350), (-500,350)]       # Set our main center-based points (i.e. (0,0) is the center of the main triangle) 
        
        # Start the recursive ball rolling.
        
        calc_triangle(win, level,p[0] + center,p[1] + center,p[2] + center,0);
 
        input_box.clear_text()      # clear the input box text window  

pybox.exit_button();        # Puts up a "program finished" window.  We don't need this here since the program waits until the 
                            # window is closed, but it's always nice to get an affirmation that the program exited on purpose.