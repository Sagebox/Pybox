import pybox
from timeit import default_timer as timer
 
# ----------------------------
# TurtleShell Graphics Example
# ----------------------------
#
# This example uses the TurtleShell prototype library.
#
# The TurtleShell library is based on Turtle Graphics, using the same commands with some added commands.
# This is just in a prototype stage, with planned additions for: 
#
#     - More graphics functions, such as curves, other interesting shapes.
#     - GPU usage
#     - 3D Turtle Graphics
#     - Planar and 3D shapes
#
# The TurtleShell class features real-time-based turtle graphics for smooth animations.
# 
# TurtleShell is not part of the Sagebox package, per se, but is an example of an external library written using Sagebox functions,
# which is why "TurtleShell.h" is included -- the library is currently compiled into Sagebox mostly for convenience. 
#
# ------------------------
# This TurtleShell Example
# ------------------------
#
# This example started off simply, as a set of 36 triangles rotated in a circle about a larger circle.  The triangles were filled with a transparent color
# that range through all hues.  The main image was than redrawn continuously in real-time at an incresing angle to rotate the image.
#
# ** Playing With Turtle Graphics
#
# Playing with some code and expanding the angle of the triangle sides changed the image into something interesting, especially with it's real-time application.
# This example is a good example of how just playing around and experimenting with slight changes can be fun and create interesting images.
# 
# ** Real-Time Turtle Graphics Example
#
# This example also shows how nice real-time display is with turtle graphics.  By not showing the items being drawn, and only showing the result at the end,
# the resultant image is slowly changed into a nice real-time, moving and growing display.
#
# This example shows using the sleep(0) function that shuts off any intermediate display (allowing the program to use update() to show the result only),
# as well as kw::Realtime() to set a real-time status for the window that is initially created.
#
# ** Showing timing
# 
# Uncomment the lines regarding timing to show how many milliseconds it takes to draw each frame.
# ------
# Future
# ------
#
# The TurtleShell class is experimental, but shows some great results.  This example is a small example, and there will be more examples and additons over time.
# I'm basically waiting for feedback, suggestions, and requests to let help direct its future path.
#
# 3-D, Planar, and other drawing aspects, as well as GPU functionality are planned for future updates.
#


window = pybox.new_window(real_time = True) 

## turtle graphics test
t = window.new_turtle_graphics()    

iRotAngle = 0
t.set_speed(0)  # Sets speed to 0, to not display items as they are drawn (> 0 numbers are milliseconds to wait between draw items)

#window.set_realtime()  # -- we can use this function if we didn't use "real_time = True" when the window was created.

# In the main loop, wait for the vertical resync so we can have smooth motion at the sync-rate of the monitor (usually 60fps)
#
while window.vsync_wait() :
    
    # The code below uses multiples of the angle, so we rotate by basically 1440 degrees (or 360*4)
 
    if iRotAngle > 360*4 : iRotAngle -= 360*4
 
    # Put some text on top of the window

    window.cls("black")
    window.write("{40}Sagebox Python Turtle Shell Graphics\n{17}{lb}Some Random Turtle Graphics Example",center_x = True); 
  
    t.color("white(150)")   # Set main color (for the lines drawn) at white with 150 (out of 255) opacity (i.e. a little transparent)
 
#   start = timer()         # --Start a timer -- ** uncomment to show timing information

# Draw 36 triangles (or semi-triangles, since we manipulate the angles of the triangles based on current iteration value)

    for i in range(36) :
        color = pybox.get_hue_color(i*10)   # Get a color that represents a changing hue 
        
        # Turtle Graphics Code

        t.pen_up()             
        t.set_pos(0,0)                      # Go back to center
        t.set_heading(-i*10+iRotAngle/2)    # Set angle of triangle placment and triangle itself (/2 is just to slow down the rotation m the vsync) 
        t.forward(50)                       # Move out to the first vertex 
        t.pen_down() 

        t.begin_fill(color,92)              # Start a fill for the triangle with our chosen hue color and transparency of 92
        
        t.forward(200)                      # Draw first semi-triangle side
        t.left(-iRotAngle/4.0-120.0)        # Rotate 60 degrees to the last line for our triangle         
        t.forward(200)                      # Draw second triangle side
        t.left(-iRotAngle/4.0-120.0)        # Rotate another 60 degrees to the triangle interior
        t.forward(200)                      # Draw third triangle side
        t.end_fill()                        # Fill the triangle
    
    window.update()     # For real-time windows, using VsynvWait(), we must update the window ourselves
    end = timer()       # Set a new angle and prepare to draw the entire triangle-wheel again at a rotated angle.
    
#    pybox.debug_write(f"Time = {{p}}{format(1000*(end-start),'.4f')} ms\n")   # ** uncomment to show timing information
 
    iRotAngle = iRotAngle + 2   # Set a new angle and prepare to draw the entire triangle-wheel again at a rotated angle.

pybox.exit_button()     # We don't really need this since the user closes the window, but it's nice to have the program put up
                        # a "program is finished" message with a button to press to close it all down.
exit(0)