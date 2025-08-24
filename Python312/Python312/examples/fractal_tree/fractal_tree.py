
# ----------------------------
# Fractal Tree (color version)
# ----------------------------
#
# This program is about 20 lines of code, just as the Basic Fractal Tree, showing using Sagebox in more-or-less
# minimal way -- most of the code is about the Fractal Tree, and Sagebox usage is mostly to create the main window 
# and put out the graphics. 
# 
# The main difference in this version is that it uses a color table to put out some nice color for the tree, and 
# converts DrawTree() into a recursive function to make it easier to use (this part has nothing to do with pybox, 
# but python programming)
#
# This program shows how expansive pybox functions can be.  For example, draw.line() in the basic version
# did not provide a color, relying on the current Pen Color.  In this example, the same line is used, provided
# from the color table -- this tells draw.line() to use this color instead, and does not change the current pen color. 
#
# This is an example of using pybox to adapt other source easily with basic graphics functions and controls.
#
# The original source code for this program was found at Rosetta Stone at http://rosettacode.org/wiki/Category:C%2B%2B

import pybox
import numpy as np;

# Main fractal_tree() function
#
# This was (more or less) copied from http://rosettacode.org/wiki/Category:C%2B%2B, so
# it is largely undocumented here. 
#
# The main functions added (or changed) are the draw.line() functions to draw the lines, as 
# well as the color selection, which calls get_hue_color() (the original was in monochrome)

def fractal_tree(win_size,angle,line_length) :

    def draw_tree(sp,line_len,a,rg,depth) :
        r = np.array(([0,-line_len]),dtype = float)
        a += rg * angle
        temp = r[0]*np.cos(a) - r[1]*np.sin(a) 
        r[1] = r[0]*np.sin(a) + r[1]*np.cos(a) 
        r[0] = temp
        r += sp

        # draw a line in the window.
        # use pybox.get_hue_color to get a bright color based on a 0-360 angle.

        win.draw.line_l(sp,r,pybox.get_hue_color(360*(depth/12)))

        if (depth < 12) :
            draw_tree(r,line_len*.75,a,-1,depth+1)
            draw_tree(r,line_len*.75,a, 1,depth+1)

    # main function start 

    sp = np.array(([win_size[0]/2,win_size[1]-1-line_length]),dtype = float)
    win.draw.line_l(sp,sp+(0,line_length),"red")    # draw initial line

    # start recursion for different sides of the tree

    draw_tree(sp, line_length, 0, -1 ,0);
    draw_tree(sp, line_length, 0,  1 ,0);

# -------------------------------------
# Start of main program (i.e. __main__)
# -------------------------------------

# Create a pybox window.  In this case, we want a size of 1300,900.
# This also sets the title and the background color
#
# bgcolor = "black,darkblue"  - this sets a gradient for the background color. 
#                               If one color is used, (i.e. "black" or "darkblue"), a slod
#                               color is used.
#
#  bgcolor can also accept a color array (i.e.RGB).  For graident colors using non-strings,
#  use the function win.set_bg_color()
#

win = pybox.new_window(size=(1300,900),title="Pybox - Fractal Tree")   

win.cls_radial("darkblue,black")       # Clear the window with a nice radial darkblue (or we can use cls() for plain/vertical gradient)

fractal_tree(win.get_window_size(),24*3.14159/180,130.0*1.45)

# Write a title at the bottom in a large font
#
# justbottomcenter  - (also just_bottom_center) sets the text at the bottom-center of the window
# yoffset           - (also y_offset) brings the text up 10 pixels so its not exactly at the bottom.

win.write("Python Color Fractal Tree",font=40,just_bottom_center=True,y_offset=-40)

# Let the user know the program has ended.
# exit_button() is not required, but the program must pause before exiting. Since this program
# doesn't look for events or take any time, the program would othewriwse exit, closing down all
# windows.
#
# pybox.wait_pending() can be used to wait for the user to close the window without displaying a button.
# (displaying a button is just a nice way to let the user know the program has actually ended)
#
# Use pybox.exit_button() for an exit button that comes up in a separate window with a text message area.

win.exit_button()
