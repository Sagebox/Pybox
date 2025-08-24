
# Pybox Double Pendulum (Simple Version).   Programming with Pybox Demonstration Program.
#
# Also See: Interactive Pendulum                       -- Allows stopping and moving bobs/chaging length of bobs.
#           Interactive Pendulum with Dev Controls     -- Adds sliders, buttons and checkboxes to change various aspects
#                                                          of the double pendulum in real-time while running.
# --------------------------------------
# Pybox Double Pendulum (Simple Version)
# --------------------------------------
# 
#      This version simply displays the pendulum moving until the window is closed, with the pendulum slowly 
#      coming to a stop. 
# 
#      Change the values in the pend.init() call to set Mass and Length for each bob, dampening, starting angles (i.e. how high), etc.
# 
#      The bobs are initially set at 150 degrees so when the drop they will swing for quite a while.
#      The Interactive and Interactive with Dev Controls version sets them much lower so that they can be moved with the mouse and then dropped
#      by the user. 
# 
# --------------------------------
# Pybox Double Pendulum In General
# --------------------------------
# 
#      This double pendulum program shows a double pendulum moving in realtime using Pybox functions. 
#
#      The window is created in the main function and passed to the Double Pendulum class where it calculates and draws the pendulum.
#
#      In this version, the pendulum runs until it stops. 
#
#      The init() function can be changed to change the bob masses, lengths, dampening and other aspects. 
#
#      The code itself is very short, using just a few GUI calls through Pybox (at least if you don't count the show_values() function
#      that prints real-time information to the window.
#
# ---------------
# Vertical Resync
# ---------------
# 
#      This program works by waiting for the vertical resync, then drawing the pendulum and updating the window. 
#      The real_time setting enables the high resolution timer, so the update can be increased by using a simple sleep()
#      call rather than using the vertical resync. 
# 
# --------------
# Pendulum Trail
# --------------
#
#      The program shows a fading trail of where the second bob swings around.  This can be disabled by setting opt_show_trail in 
#      DPendulum to false.
#
# --------------
# Timing Display 
# --------------
#
#      When bShowTiming is set to True, the time for each loop is displayed in the Pybox Process Window, showing the milliseconds
#      taken to calculate and draw the pendulum.
#
# --------------------
# Sagebox C++ Versions
# --------------------
#
# See the Sagebox C++ versions of the double pendulum.
#

import pybox                                # import main pybox
import numpy as np

import pend_module as pend                  # Bring in the pendulum module

# Create main pybox window
#
# realtime (or real_time) -  Sets the window for real-time graphics, which sets a number of configuration
#                            items for better real-time graphics. 

win = pybox.new_window("Pybox Double Pendulum",size=(1200,700),realtime=True,bgcolor="black")

# Set up pendulum with pybox Window, and Length1, Length2, Angle1, Angle2, Dampening and
# where to place the peg in relation to the window height.

pend.init(win,240,225,10,10,-150,-150,.9985,.25)        

# Show real-time values while the pendulum is moving

def show_values() :
    win.set_write_indent(10)        # Set an indent of 10 so the text is not right on the left edge.
                                    # set_write_indent() does this for every newline so we can move the 
                                    # text out and don't have to keep resetting it. 

    win.set_write_padding(5)        # Add some space between lines when writing to the window (for nicer display)
    win.set_write_pos(10,10)
    win.set_text_color("Gray172")   # Set the text color.  Gray172 is a stock color. See SageColor::Gray172()

    # {g}  green, {c} = cyan.  {x=130) sets the X write position to that value so things line up
    
    # Double "{{" and "}}" can used so we can pass them to pybox in formatted strings (i.e. "{red}" becomes "{{red}}" 
    # Here, a "+" is used between strings just the {r},{g}, etc. can be used (for readability).

    win.write("Mass 1:{x=130}{g}"           + f"{format(pend.mass[0],'.2f')}\n")
    
    win.write("Mass 2:{x=130}{g}"           + f"{format(pend.mass[1],'.2f')}\n")
    win.write("Length 1:{x=130}{g}"         + f"{format(pend.length[0],'g')}\n")
    win.write("Length 2:{x=130}{g}"         + f"{format(pend.length[1],'g')}\n")
    win.write("Dampening:{x=130}{g}"        + f"{format(1.0-pend.damp*pend.overflow_mul,'g')}\n\n")

    win.write("Ang Accel 1:{x=130}{c}"      + f"{format(pend.angle_acc[0],'.4f')}\n")
    win.write("Ang Accel 2:{x=130}{c}"      + f"{format(pend.angle_acc[1],'.4f')}\n")
    win.write("Ang Velocity 1:{x=130}{c}"   + f"{format(pend.angle_vel[0],'.4f')}\n")
    win.write("Ang Velocity 2:{x=130}{c}"   + f"{format(pend.angle_vel[1],'.4f')}\n")
    win.write("Angle 1:{x=130}{c}"          + f"{format(180*pend.angle[0]/np.pi,'.4f')}\n")
    win.write("Angle 2:{x=130}{c}"          + f"{format(180*pend.angle[1]/np.pi,'.4f')}\n\n")
    
    # If there has been an overflow, then display it in red.  This means the math/floating-point had
    # some sort of resolution problem, usually when the bob starts wobbling severely.

    # Only display it if we've have more than two, since they can happen at end points here and there. 

    if pend.overflow_count > 2 :
        win.write("\n\n\n\n{r}Math Overflow "+ f"({pend.overflow_count-2})\n")
        win.write("{12}Try increasing dampening (also lowering weight values and weight ratios).")

# -----------------------------
# Main Program Start (__main__)
# -----------------------------

# Wait for the vertical sync in a loop.  Exits when the window is closed

while win.vsync_wait() :
    win.cls()

    pend.update()    
    pend.render()

    # Print title in upper center of window. 
    # (10 pixels down. 'centerx' centers it horizontally int he window)
    #
    # {w} sets color to white (overriding current gray color we previously set for output)

    win.write_xy(0,10,"{w}Python Double Pendulum",centerx=True,font=30)
    
    show_values()
    win.update()        # Send the image we've created to the window




