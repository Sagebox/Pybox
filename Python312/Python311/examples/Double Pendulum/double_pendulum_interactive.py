
# Pybox Interactive Pendulum.  Programming with Pybox Demonstration Program. 
#
# Also See: Double Pendulum (Simple Version)           -- Only calculates and renders the double pendulum, with no event handling.
#           Interactive Pendulum with Dev Controls     -- Adds sliders, buttons and checkboxes to change various aspects
#                                                          of the double pendulum in real-time while running.
#
# --------------------------
# Pybox Interactive Pendulum
# --------------------------
# 
#      This version adds to the Pybox Double Pendulum (Simple Version) by adding the following interactive control:
# 
#          1. The pendulum can be stoped and then moved by clicking on the window.
#          2. The bobs can be moved anywhere and the lengths of the rods will changed as you move the bobs.
#          3. After moving the bobs click anywhere on the screen (not on a bob) to drop the pendulum.
#          4. Zoom Control.  You can use the MouseWheel to zoom in and out, enlarging or reducing the zoom of the pendulum 
#                            The size and mass of the pendulum stay the same, as only the zoom changes.
#          5. Moving the Pedulum Up and Down.  Clicking on the Window with the Right Mouse Button will set Y position of the Peg holding up the
#                                          Pendulum.  You can then move the mouse up and down to set the high or low point of the pendulum peg.
# 
#      Functions Added
# 
#          handle_events()          - This handles the events occuring such as mouse clicks, mouse moving, Mouse Wheel, etc.
#          handle_mouse_click()     - This handles the mouse click to stop the pendulum moving and determine if a pendulum bob is being moved.
#          handle_mouse_drag()      - Handles the case where the mouse button is down and moving and a bob is being dragged.
#                                     This sets the new position of the pendulum bobs and their rod lengths.
#          show_instructions()      - Displays instructions on how to use the mouse to move the bobs, etc. Disappears when the Mouse clicks on the window
# 
#      The initial angular velocity is set purposely low so that the pendulums can be moved with the mouse and then dropped (by clicking the window once moved)
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
from timeit import default_timer as timer   # time it so we can time how many ms we're using to calculate and display the pendulum

import pend_module as pend                  # Bring in the pendulum module

# Create main pybox window
#
# realtime (or real_time) -  Sets the window for real-time graphics, which sets a number of configuration
#                            items for better real-time graphics. 

win     = pybox.new_window("Pybox Double Pendulum",size=(1200,700),realtime=True,bgcolor="black")

# Set up pendulum with pybox Window, and Length1, Length2, Angle1, Angle2, Dampening and
# where to place the peg in relation to the window height.

pend.init(win,220,185,10,10,-15,-15,.9985,.33)

# Handle when we have a mouse click.
#
# If the mouse is clicked on a pendulum bob then set a dragging status
# if the mouse is not clicked on a bob, then either continue or pause the rendering
# (pausing the rendering makes it easier to grab a bob, then click the window to continue)

def handle_mouse_click() :
    global paused,dragging,opt_show_instructions

    opt_show_instructions = False                           # remove instructions after first mouse click

    force_pause = not paused   
    pos = win.get_mouse_pos()                               # get current mouse position in the window

    radius = pend.bob_radius*pend.zoom*pend.circle_mult     # calculate display radius            
    dragging = 0
    
    # if the mouse is within one of the bobs, set the dragging status so we know
    # we're dragging a bob around

    if (pos[0] >= pend.rod[1][0]-radius and pos[0] < pend.rod[1][0]+radius and 
        pos[1] >= pend.rod[1][1]-radius and pos[1] < pend.rod[1][1]+radius) : dragging = 1

    if (pos[0] >= pend.rod[2][0]-radius and pos[0] < pend.rod[2][0]+radius and 
        pos[1] >= pend.rod[2][1]-radius and pos[1] < pend.rod[2][1]+radius) : dragging = 2

    if not dragging : paused = force_pause      # if a bob wasn't clicked, then pause or unpause
    else : 
        paused = True                           # otherwise, pause or sure so the user can move the bob


# Handle when a mouse drag event occurs -- when the mouse is moving and it is also pressed.
#
# This moves the pendulum bobs (whichever is being dragged) as well as the line length (if keep_rod_length is not True)

def handle_mouse_drag() :
    delta = win.get_mouse_pos()-pend.rod[dragging-1]        # get difference between current mouse position and original bob position

    pend.angle[dragging-1] = np.arctan2(delta[0],delta[1])

    pend.length[dragging - 1] = np.sqrt(delta[0]*delta[0] + delta[1]*delta[1])/pend.zoom

    pend.reset() # since we're dragging, reset the pendulum trails, velocity, acceleration, etc.


# Handle an event when we know we have one.
#
# This handles the mouse movements, clicks, right-click, etc.

def handle_events() : 
    if win.mouse_clicked() : handle_mouse_click()
    if win.mouse_drag_event() and dragging > 0 : handle_mouse_drag()

    # If the mouse wheel was moved, zoom in or out, depending on mousewheel direction

    if win.mouse_wheel_moved() :
        if (win.get_mouse_wheel_value() < 0) : pend.zoom *= .95 
        else : pend.zoom *= 1/.95

    # if the right mouse-button was clicked, then set the display position accordingly. 

    if win.mouse_r_button_down()   : pend.rod[0][1] = win.get_mouse_pos()[1]


# Show instructions.  This shows until the mouse clicks on the window.

def show_instructions() :
    win.set_text_color("Gray192")         # Set the text color

    # {y} = yellow, {g} = green. {30} = set font to size 30pt

    win.set_write_indent(300)   # Set the newline position for each line 
    win.set_write_pos(300,100) 
    win.write("{30}{y}Double Pendulum\n")
    win.write("\nClick on either or both pendulums to set position.\n") 
    win.write("Click on the screen (or press {g}\"Drop\"{/}) to drop the pendulum.\n\n")
    win.write("Click on {g}\"Maintain Rod Length\"{/} to change pendulum angles without changing the rod length.\n\n")
    win.write("Use the controls to the left to change states while pendulum is in motion or before dropping the pendulum.\n\n")
    win.write("{p}While the pendulum is moving\n\n") 
    win.write("Right-click on the screen to move the display area up and down\n") 
    win.write("Use the Mouse Wheel to zoom in and out\n") 
    win.write("Click on the display area to stop the pendulums so you can move them.")            
    win.set_write_indent(0)     # Set newline indent back to 0


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
    # Here, I use a "+" between strings so I can use just the {r},{g}, etc. for readability.

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
  
    win.write("Zoom:{x=130}{g}"             + f"{format(pend.zoom*100,'.2f')}%")

    # If there has been an overflow, then display it in red.  This means the math/float-point had
    # some sort of resolution problem, usually when the bob starts wobbling severely.

    # Only display it if we've have more than two, since they can happen at end points here and there. 

    if pend.overflow_count > 2 :
        win.write("\n\n\n\n{r}Math Overflow "+ f"({pend.overflow_count-2})\n")
        win.write("{12}Try increasing dampening (also lowering weight values and weight ratios).")

    win.set_write_padding(0)    # Reset Padding (since we may be displaying instructions)

# -----------------------------
# Main Program Start (__main__)
# -----------------------------

dragging                = 0             # Active when dragging a bob around
paused                  = False         # Click on screen to pause/unpaus.  Click on bob to move bob
opt_show_instructions   = True          # Shows instructions initially.  First mouse clicked removes them
opt_show_values         = True          # When False, realtime values are not shown
opt_show_timing         = False         # Set to True to show timing. 

# Wait for the vertical sync in a loop.  Exits when the window is closed

while win.vsync_wait() :
    win.cls()
    start = timer()

    # event_pending() is not strictly necessary, but can be used in loops that require speed and 
    # don't pause the program (such as get_event() does). 
    #
    # We can handle events any time, but using event_padding() in a real-time loop allows just 
    # one check for an event, so that handle_events() only needs to check events when we know one
    # is there to get, eliminating unnecessary processing time in a tight loop when it is
    #
    # By contrast, using the typical get_event() only returns when there is an event pending, so
    # event_pending() is not needed.  

    if pybox.event_pending() : handle_events()

    if (not paused) : pend.update()        
    pend.render()                       # always render

    # Print title in upper center of window. 
    #
    # {w} sets color to white (overriding current gray color for output)

    win.write_xy(0,10,"{w}Python Interactive Double Pendulum",centerx=True,font=30)

    if opt_show_instructions  : show_instructions()
    if opt_show_values        : show_values()

    end = timer()

    # {p} = purple.  Wrapped in "{{p}}" because of the formatted string.

    if opt_show_timing : pybox.debug_write(f"Time = {{p}}{format(1000*(end-start),'.4f')} ms\n")

    win.update()    # Send the image we've created to the window



