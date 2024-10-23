
# ---------------------------------------------------------------
# Python Real Time Color Wheel - GDI graphics & Real-Time Example
# ---------------------------------------------------------------
#
# This is a small example of using basic GDI graphics in python.  The program draws a number of squares in
# a circle, slowly rotating them individually as they rotate in a larger circle.
# 
# This program shows using opacity, translation and rotation transforms, as well a simple graphics primitives.
# 
#  ---------------
#  Vertical Resync
#  ---------------
#  
# This program works by waiting for the vertical resync, then drawing the color wheel and updating the window
#
# The opt.real_time() setting enables the high resolution timer, and configuring other details for real-time graphics.
# 
# With the wait_vsync() function used, if the program misses the vertical resync (i.e. it takes longer than 60ms
# or however long the vertical resync takes for the monitor being used), the wait is aborted and returns immediately.
# 
# --------------------
# color_wheel_timer.py
# --------------------
# 
# See this program for a version that shows vertical resync timing. 
# 

import pybox                    # import main pybox module
 
import numpy as np

# Create a pybox window of default size. 
#
# opt.real_time() sets the window as realtime (see notes above)
# opt.bg_color() black sets the background to black instead of the default background color
#
# this uses the symbolic options of pybox.  The line opts='real_time,bg_color=black' or 'RealTime,bgColor=black'
# can also be used.  see color_wheel_timer.py for an example

win             = pybox.new_window("Real-Time Python Color Wheel",realtime=True,bgcolor="black")

# These are essentially constants, but can be changed dynamically by adding pybox Dev Controls (i.e. slider, buttons, etc.)

num_sections    = 20            # number of 
square_size     = 150           # size of each square
radius          = 200           # radius of large circle where squares are placed
spin            = 0.0           # spin factor for both large circle and each square (handled differently)

win.draw.set_opacity(125)        # set the graphics opacity

# Create two text widgets that center themselves for a title.
# These are widgets and are peristent, so they are fire-and-forget here.  
# In other places, the return value can be assign so the text can be changed.
#
# just_top_center   = Center in the upper-top of the window 
# center_x          = Center the text in the X plane
# font              = Sets the font for the text widget
# color             = Sets 'CornflowerBlue' as the color.  This is a pantone color which can also be
#                     stated as "Pancolor:Cornflowerblue" or pybox.PanColor.CornFlowerBlue() for a symbolic version
#
# all of the above can also be stated as symbolic pybox.opt-style options, such as opt.just_top_center(), which 
# allows error-free usage as well as intellisense fill-in and selection/documentation display when "opt." is pressed
#
# try pressing "opt." on a blank line below.  This should display all pybox options available

win.text_widget(5,text="Python Real-Time GDI Graphics Example",centerx=True,font=40)
win.text_widget(0,45,"A More Advanced Example using Rotational and Translate Transformations",          # center_x and centerx are the same.
                                                center_x=True,font=16,textcolor="CornflowerBlue")       # all keywords can be separated with '_' on 
                                                                                                        # natural word boundaries, such as text_color or textcolor

# main loop. (i.e. __main__)
#
# Wait for the vsync.  win.vsync_wait() will return false when the window is closed.

while win.vsync_wait() :
    win.cls()                                           # clear the window to last known background color
    for i in range(0,num_sections) :

        # Some math to rotate the larger wheel and rectangles in relation to each other

        angle = i*(np.pi*2)/num_sections+spin
        color = win.draw.get_hue_color(i*360/num_sections)
        fx = radius*np.cos(angle)       # rotate our larger radius to the current square position
        fy = radius*np.sin(angle)

        # Set a transform so the (fx,fy) position at the end of the larger circle is the new (0,0)

        win.draw.translate_transform(fx+600,fy+420)    

        # draw the rectangle at the transform's (0,0) point and angle specified.
        # With the angle keyword, we set the angle of rotation around the previous outer transform.
        # --> we could have called win.draw.translate_transform() again, but used the angle keyword instead as a shortcut
        # --> We could have used the 'opacity' keyword, but it was set as a global opacity already with win.draw.set_opacity()
        
        win.draw.fill_rectangle(-square_size/2,-square_size/2,square_size,square_size,color,angle = (i+spin*3.5)*60)
        win.draw.reset_transform()      # Transforms are additive, so we need to reset when we're done for the first transform

    win.update()  # send the image we've drawn out to the window
    spin += .005
