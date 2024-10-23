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

    This example is very simple, only clearing the backdrop and displaying the pendulum.

    This is meant to show a simple version of using some of the pybox drawing functions in 
    a real-time setting.

    see single_pendulum.py for an example that show real-time values.
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

# Open a window. Use the 'realtime' option so pybox will set somet things up for real-time graphics
# size is not required -- when omitted, a default size will be used. 

win        = pybox.new_window("Pybox Pendulum (Simple Version)",size=(500,400),realtime=True)

# Initial pendulum settings

angle      = 45*np.pi/180.0         # starting  angle (i.e. 45 degrees). Try 60,90, 120, etc.
rod_length = 265                    # Length of rod in pixels
angle_vel  = 0
damp       = .999                   # set to 1 for an endless pendulum

center_x   = (win.width()/2, 0 );   # Top-Center of Window

# set the cls for a gradient.
# setting the cls here allows us to just use cls() later, so in the main loop it already knows
# to do the gradient and we don't have to specify it again
#
# Another reason is so we have the right background for the text widget to blend into

win.cls("black,skybluedark")      # skybluedark is similar to pancolor::darkblue

# Set a fire-and-forget persistent widget with a title.
#
# center_x    -- centers the text in the X plane (can also be stated as 'centerx=True'

win.text_widget(0,350,"Real-Time Python Pendulum Example",font=20,center_x=True); 
win.text_widget(0,375,"(simple version)",font=14,center_x=True,textcolor="CornflowerBlue"); 

while win.vsync_wait() :
    win.cls()           # clear the canvas to the gradient we set

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

    win.draw.line_l(center_x,point,"white",pen_size=5);                             # Draw the rod with pen size 5
    win.draw.fill_circle_l(center_x,7,"Beige")                                      # Draw a peg on the top
    win.draw.fill_circle_l(point,40,"MediumVioletRed",pen_color="Beige",pen_size=5) # Draw the circle with outline size 5
   
    win.update()            # Update the window (i.e. send everything we just drew to the window to display)
                            # usually this is handled automatically.  the 'realtime' options means we do it manually.
