"""
Pybox Single Pendulum Example.   Programming with Pybox Demonstration Program.

Also See: Pybox Double Pendulum Example

---------------------
Pybox Single Pendulum
---------------------
 
    This version simply displays the pendulum moving until the window is closed, with the pendulum slowly 
    coming to a stop. 
 
    This Single Pendulum is written just to show a pendulum swinging fro 45 degrees back and forth while it 
    slowly comes to a stop. 
 
    For more of a full pendulum display (single and double) see the Double Pendulum example in the Standard C++ examples.
 
    You can change the values such as starting angle, rod length, bob size, window size, etc. 
 
    For larger angles, a smaller length with the rod top (origin) set more in the middle of the window will show the
    pendulum when it is above the center peg.
 
    note: Though the window is small, it can be full-screen.  It is small by design.  See double_pendulum.py for a larger example

------------
This Example
------------

    This example loads a bitmap for a background (if not found, it continues) and displays real-time values as the penulum
    is moving.

    see single_pendulum_simple.py for an example that is even simpler, just drawing the pendulum.
    Also see single_pendulum_timing for a version that displays how many milliseconds it takes to
    render the image.

---------------
Vertical Resync
---------------
 
    This program works by waiting for the vertical resync, then drawing the pendulum and updating the window. 
    The 'realtime' setting enables the high resolution timer and sets other configurations to allow better
    real-time display

--------------
Timing Display 
--------------

    In single_pendulum_timing.py, the time for each loop is displayed in the Pybox Process Window, showing the milliseconds
    taken to calculate and draw the pendulum.

-----------
C++ Version
-----------

See the C++ version of the single pendulum.

"""

import pybox
import numpy as np

#pybox.show_info()          # uncomment this and change name in read_image_file() below
                            # to show how pybox can report information.

# Open a window. Use the 'realtime' option so pybox will set somet things up for real-time graphics
# a symbolic opt.real_time() can be used also

win        = pybox.new_window("Pybox Pendulum",size=(500,400),realtime=True)

# initial pendulum settings

angle      = 45*np.pi/180.0         # starting  angle (i.e. 45 degrees). Try 60,90, 120, etc.
rod_length = 265                    # Length of rod in pixels
angle_vel  = 0
angle_acc  = 0
damp       = .999                   # set to 1 for an endless pendulum

center_x   = (win.width()/2, 0 );   # Top-Center of Window

# set the cls for a gradient in case the read_image_file fails (i.e. file does not exist)
# setting the cls here allows us to just use cls() later, so in the main loop it already knows
# to do the gradient and we don't have to specify it again

win.cls("black,skybluedark")      # skybluedark is similar to pancolor:darkblue

# read in a bitmap and set it to the cls_bitmap, which displays every time cls() is called
# if set_cls_bitmap() fails, it is passive, and refers to the current colors (which was just set
# with the win.cls() call above
#

win.set_cls_bitmap("texture-pendulum.jpg",True)

# Set a fire-and-forget persistent widget with a title.
#
# centerx     -- centers the text in the X plane
# pady = -20  -- This option raises the text Y position -20 pixels 
#                to allow a little nicer spacing. 
#
# text_color = "NearWhite" -- NearWhite is a stock color.  See pybox.SageColor and 
#                              pybox.PanColor for symbolic versions of the colors available.
#
# just_bottom_center = True can also be written as justbottomcenter=True,  The underscores are used
# here for clarity.  just_bottomcenter also works. 

win.text_widget(text="Real-Time Python Pendulum Example",just_bottom_center=True,font=20,pady=-20,textcolor="NearWhite"); 

# using symbolic opt.-style options of the line above: 
#
#       win.text_widget(text="Real-Time Python Pendulum Example",
#               opts=opt.just_bottom_center()+opt.font(20)+opt.pad_y(-20)+opt.text_color("NearWhite"))
#
# while longer, the auto-complete and intellisense spells it correctly for you and this 
# can be a good way see all of the options in a list and choose from them. 

# Show the real-time pendulum values, such as angle, acceleration, etc.

def show_values() :
    win.set_write_indent(10)        # set all newlines to indent 10 pixels (so we don't have to keep
                                    # doing it ourselves # on each new line)

    win.set_write_pos(10,10)        # Set the initial write position

    # {g}  green, {c} = cyan.  {x=130) sets the X write position to that value so things line up
    
    # the formatted value (i.e. 'g' and '.4f') are so that python won't print out
    # 16-digit floating-point values.

    win.write("Rod Length:{x=130}{g}"   + f"{format(rod_length,'g')}\n")
    win.write("Dampening:{x=130}{g}"    + f"{format(1.0-damp,'g')}\n\n")
    
    win.write("Ang Accel:{x=130}{c}"    + f"{format(angle_acc,'.4f')}\n")
    win.write("Ang Velocity:{x=130}{c}" + f"{format(angle_vel,'.4f')}\n")
    win.write("Angle:{x=130}{c}"        + f"{format(180*angle/np.pi,'.4f')}\n")


# Wait for the vertical sync in a loop.  
# vsync_wait() waits for the vertical retrace.  It returns false when the window is closed. 

while win.vsync_wait() :
    win.cls()                                   # clear the canvas (to either the bitmap or gradient we set)
 
    # Calculate the next position of the pendulum 

    angle_acc   = np.sin(angle) / rod_length
    angle_vel   -= angle_acc
    angle       += angle_vel
    angle       *= damp             # apply friction
   
    point = np.array([np.sin(angle), np.cos(angle)]) * rod_length + center_x    # Calculate the point at the end of the rod. 

    # draw the pendulum bob, rod, and top peg
    #
    # line_l() and fill_circle_l() are list/array/tuple versions of line() and fill_circle(),
    # respectively, that take independent x,y values.  Here, a list or array is used for coordinates.

    win.draw.line_l(center_x,point,"white",pen_size=5);                                  # Draw the rod with pen size 5
    win.draw.fill_circle_l(center_x,7,"Beige")                                  # Draw a peg on the top
    win.draw.fill_circle_l(point,40,"MediumVioletRed",pen_color="Beige",pen_size=5)                # Draw the circle with outline size 5
   
    show_values()           # show the values 
    win.update()            # Update the window (i.e. send everything we just drew to the window to display)
                            # usually this is handled automatically.  the 'realtime' options means we do it manually.