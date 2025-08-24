
# Pybox Interactive Pendulum with Dev Controls.  Programming with Pybox Demonstration Program.
#
# Also See: Double Pendulum (Simple Version)           -- Only calculates and renders the double pendulum, with no event handling.
#           Interactive Pendulum                       -- Adds the ability to start and stop the pendulum, move the boobs around,
#                                                         Zoom in and out with the MouseWheel, and set the Peg position with the mouse.
#
# --------------------------------------------
# Pybox Interactive Pendulum with Dev Controls
# --------------------------------------------
# 
# In this version, a QuickForm Window is created to merge a regular window and Dev Controls window into one nice package. 
# With the Dev Controls, many elements of the pendulum can be changed in real-time. 
# 
# Instruction Display
# 
#      An Instruction Text display is added which disappears when the bobs are moved with the mouse.
#      As with the previous interactive version, the Bobs are set at a low angular velocity so they can be moved and then dropped.
#      
#      On average, for each control, there are two lines of code added: 1 line to create the control, and another line of code to 
#      check if the control has
#      changed (via an event) and use its value. 
#      
#      The Dev controls window adds a number of options:
# 
#          1. Mass Input Boxes     - There are now two input boxes where the mass of each bob can be set independently.
#          2. Dampen Slider        - This sets the dampening (friction) on the slider and can be changed while the pendulum, is moving.
#                                    note: lower settings (close to 0) can lead to math overruns, which are detected by the algorithm and shut down.
#          3. Zoom Slider          - Moves the Zoom in and out.  The MouseWheel can also be used for this. 
#          4. Pendulum Size        - Sets the size of the pendulum bobs.   This can be nice for zooming in and out.  Does not affect mass or length 
#                                    of the bobs and only changes the display size.
#          5. Rod Thickness        - Sets the thickness of the rods as displayed.  Does not change the mass or length of the rods and is only used for 
#                                    display. These show a good example of using Radio Buttons in Pybox
#          6. Display Values       - Checkbox to display or disable display of realtime values (angle, mass, etc.)
#          7. Maintain Rod Length  - Checkbox to set static rod length.  When checked, the rod length will not change when moving the pendulum bobs with 
#                                    the mouse
#          8. Show Trail           - Checkbox to show or hide the Trails displayed on the bottom pendulum
#          9. Single Pendulum      - Checkox to set a Single Pendulum.  When checked, only the top pendulum is displayed.  The second Bob and its rod is
#                                    hidden, and the mass of the second bob is set to 0 -- the top pendulum runs as a single pendulum until "Single Pendulum" 
#                                    is unchcked and the mass of second bob returns.
#          10. Show Timing         - Checkbox to show real time information on program execution.  When checked, this shows the milliseconds for each loop
#                                    to calculate and draw the pendulum
#          11. Start,Stop,Drop     - This is a button that changes text depending on the state.   See the set_start_button_text() function calls.
#          12. Quit Button         - This can be pressed to stop the program.  The Window can also simply be closed.
#      
#      Functions Added:
# 
#      set_start_button_text()    - Sets the text of the Start/Stop button to "Start" or "Stop", depending on the mode.
#      handle_events()            - This function is not added, but the code to handle the Dev Controls has been added.
# 
# ---------------------------------------------------------------
# Added with the Pybox Interactive Pendulum (and in this version)
# ---------------------------------------------------------------
# 
#      This version adds to the Pybox Double Pendulum (Simple Version) by adding the following interactive control:
# 
#          1. The pendulum can be stoped and then moved by clicking on the window.
#          2. The bobs can be moved anywhere and the lengths of the rods will changed as you move the bobs.
#          3. After moving the bobs click anywhere on the screen (not on a bob) to drop the pendulum.
#          4. Zoom Control.  You can use the MouseWheel to zoom in and out, enlarging or reducing the zoom of the pendulum 
#                            The size and mass of the pendulum stay the same, as only the zoom changes.
#          5. Moving the Pedulum Up and Down.  Clicking on the Window with the Right Mouse Button will set Y position of the Peg holding up the
#                                      Pendulum.  You can then move the mouse up and down to set the high or low point of the pendulum peg.
# 
#      Functions Added
# 
#          handle_events()          - This handles the events occuring such as mouse clicks, mouse moving, Mouse Wheel, etc.
#          handle_mouse_click()     - This handles the mouse click to stop the pendulum moving and determine if a pendulum bob is being moved.
#          handle_mouse_drag()      - Handles the case where the mouse button is down and moving and a bob is being dragged.
#                                     This sets the new position of the pendulum bobs and their rod lengths.
#          display_instructions()   - Displays instructions on how to use the mouse to move the bobs, etc. Disappears when the Mouse clicks on the window
# 
# --------------------------------
# Pybox Double Pendulum In General
# --------------------------------
# 
#      This double pendulum program shows a double pendulum moving in realtime using Pybox functions. 
#
#      The window is created in the main function and passed to the Double Pendulum module where it calculates and draws the pendulum.
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
#      The program shows a fading trail of where the second bob swings around.  This can be disabled by setting show_trail in 
#      the Double Pendulum Module to False.
#
# --------------
# Timing Display 
# --------------
#
#      When show_timing is set to True, the time for each loop is displayed in the Pybox Process Window, showing the milliseconds
#      taken to calculate and draw the pendulum.
#
# --------------------
# Sagebox C++ Versions
# --------------------
#
# See the Sagebox C++ versions of the double pendulum.
#

import pybox                                    # import main pybox
import numpy as np                              # numpy, of course!
from timeit import default_timer as timer       # time it so we can time how many ms we're using to calculate and display the pendulum

import pend_module as pend                      # Bring in the pendulum module

# Create main pybox Quick Form Window, which gives a Window and a Dev Controls Window put together
# (These can be below in the main section. These lines are just here to point them out)
#
# realtime (or real_time) -  Sets the window for real-time graphics, which sets a number of configuration
#                            items for better real-time graphics. 

qf = pybox.quick_form(label=" Pybox Double Pendulum with QuickForm Window ",realtime=True,sageicon=True)

win     = qf.win     # Assign window for easier use
dev     = qf.dev     # Assign Dev Window for easuer use

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

    # if a bob wasn't clicked, then pause or unpause as well as the button text.

    if not dragging : set_start_button_text(force_pause,True)       
    else : 
        paused = True                           # otherwise, pause or sure so the user can move the bob
        button_start.set_text("   Drop!   ")    # .. and set the button text


# Handle when a mouse drag event occurs -- when the mouse is moving and it is also pressed.
#
# This moves the pendulum bobs (whichever is being dragged) as well as the line length (if keep_rod_length is not True)

def handle_mouse_drag() :
    delta = win.get_mouse_pos()-pend.rod[dragging-1]            # get difference between current mouse position and original bob position
    pend.angle[dragging-1] = np.arctan2(delta[0],delta[1])

    if not keep_rod_length : pend.length[dragging - 1] = np.sqrt(delta[0]*delta[0] + delta[1]*delta[1])/pend.zoom

    pend.reset()    # since we're dragging, reset the pendulum trails, velocity, acceleration, etc.


# Set the start/stop button text accordingly.

def set_start_button_text(pause : bool,set_pause) :
    global paused

    if pause     : button_start.set_text("   Start   ")     # Add spaces to make the button wider.
    else         : button_start.set_text("   Stop   ")
    if set_pause : paused = pause


# Handle an event when we know we have one.
#
# This handles the mouse movements, clicks, right-click, as well as all of the Dev Window controls

def handle_events() : 
    global keep_rod_length,opt_show_values,opt_show_timing,quit_program

    if win.mouse_clicked() : handle_mouse_click()
    if win.mouse_drag_event() and dragging > 0 : handle_mouse_drag()

    # If the mouse wheel was moved, zoom in or out, depending on mousewheel direction

    if win.mouse_wheel_moved() :
        if (win.get_mouse_wheel_value() < 0) : pend.zoom *= .95 
        else : pend.zoom *= 1/.95

    # if the right mouse-button was clicked, then set the display position accordingly. 
 
    if win.mouse_r_button_down()   : pend.rod[0][1] = win.get_mouse_pos()[1]

    if slider_dampen.moved()        :
        if pend.damp == 0 : pend.reset_overflow()
        pend.damp = 1.0-float(slider_dampen.get_pos())/10000.0

    # Handle Dev Window Controls. This probably could/should be a separate function

    if slider_pend_size.moved() : pend.circle_mult  = float(slider_pend_size.get_pos())/100*5 + .25
    if slider_zoom.moved()      : pend.zoom         = float(slider_zoom.get_pos())/100.0 

    if radio_thick_lines.pressed() : pend.thick_mul = line_thickness[radio_thick_lines.get_checked_button()]

    # check checkboxes -- basically just inverts the current setting

    if checkbox_single_pend.pressed()      : pend.single_pend    = not pend.single_pend 
    if checkbox_show_trail.pressed()       : pend.show_trail     = not pend.show_trail  
    if checkbox_static_length.pressed()    : keep_rod_length     = not keep_rod_length
    if checkbox_show_values.pressed()      : opt_show_values     = not opt_show_values 

    # If the show_timing is changed, then we want to also show or hide the debug window.

    if checkbox_show_timing.pressed()      : 
        opt_show_timing    = not opt_show_timing 
        pybox.debug_show(opt_show_timing)

    if button_quit.pressed()      : quit_program   = True
    if button_start.pressed()     : set_start_button_text(not paused,True)

    # If the weights were changed (by pressed CR in the input box), then change them in the program

    if inputbox_weight1.return_pressed() : pend.mass[0] = inputbox_weight1.get_float()
    if inputbox_weight2.return_pressed() : pend.mass[1] = inputbox_weight2.get_float()


# Show instructions.  This shows until the mouse clicks on the window.

def show_instructions() :
    win.set_text_color("Gray192")         # Set the text color

    # {y} = yellow, {g} = green. {30} = set font to size 30pt

    win.set_write_indent(300)   # Set the newline position for each line 
    win.set_write_pos(300,30) 
    win.write("{30}{y}Python Double Pendulum\n")
    win.write("\nClick on either or both pendulums to set position.\n") 
    win.write("Click on the screen (or press {g}\"Drop\"{/}) to drop the pendulum.\n\n")
    win.write("Click on {g}\"Maintain Rod Length\"{/} to change pendulum angles without changing the rod length.\n\n")
    win.write("Use the controls to the left to change states while pendulum is in motion or before dropping the pendulum.\n\n")
    win.write("{p}While the pendulum is moving\n\n") 
    win.write("Right-click on the screen to move the display area up and down\n") 
    win.write("Use the Mouse Wheel to zoom in and out\n") 
    win.write("Click on the display area to stop the pendulums so you can move them.")            
    win.set_write_indent(0)               # Set newline indent back to 0


# Show real-time pendulum values

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

dragging                = 0                 # Active when dragging a bob around
paused                  = False             # Click on screen to pause/unpaus.  Click on bob to move bob
opt_show_instructions   = True              # Shows instructions initially.  First mouse clicked removes them
opt_show_values         = True              # When False, realtime values are not shown
keep_rod_length         = False             # When true, the rod lengths won't change when moving the bobs around
quit_program            = False             # Set when quit button is pressed to exit the program (The window can also just be closed)
opt_show_timing         = False             # When True, the realtime data is displayed for each render
line_thickness           = (1.0,2.0,3.0)    # Line thickness multiplier values for the Rod Thickness radio buttons

# Add dev window controls.
#
# The dev window here is part of the quick_form window that was returned (qf.dev) assigned as dev

dev.new_text("Pendulum Controls",font=17,textcolor="Cyan") 

inputbox_weight1        = dev.new_inputbox("Weight 1",          default = pend.mass[0])
inputbox_weight2        = dev.new_inputbox("Weight 2",          default = pend.mass[1]) 

slider_dampen           = dev.new_slider("Dampen Multiplier",   default = 15)
slider_zoom             = dev.new_slider("Zoom",                default = 100,range=(25,150))
slider_pend_size        = dev.new_slider("Pendulum Size",       default = 15)

radio_thick_lines       = dev.new_radiobuttons("Rod Thickness","Normal\nThick\nThicker",horz=True) 

checkbox_show_values    = dev.new_checkbox("Display Values",        default = opt_show_values)      
checkbox_show_trail     = dev.new_checkbox("-Show Trail",           default = pend.show_trail)      # "+" to add checkbox on same line as last
checkbox_show_timing    = dev.new_checkbox("+Show Timing",          default = opt_show_timing)                
checkbox_single_pend    = dev.new_checkbox("+Single Pendulum",      default = pend.single_pend)

checkbox_static_length  = dev.new_checkbox("+Maintain Rod Length")       # "-" puts it on next line but closer to last checkbox to
                                                                         # keep it visually part of the same grouping

button_start            = dev.new_button("   Stop   ")                   # Use spaces to pad the display so it is wider. 
button_quit             = dev.new_button("-   Quit   ")                  # "+" to add checkbox on same line as last

# Wait for the vertical sync in a loop.  Exits when the window is closed

while win.vsync_wait() and not quit_program :
    start = timer()
    win.cls()

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

    if opt_show_instructions  : show_instructions()
    if opt_show_values        : show_values()

    end = timer()

    # {p} = purple.  Wrapped in "{{p}}" because of the formatted string.

    if opt_show_timing : pybox.debug_write(f"Time = {{p}}{format(1000*(end-start),'.4f')} ms\n")

    win.update()    # Send the image we've created to the window



