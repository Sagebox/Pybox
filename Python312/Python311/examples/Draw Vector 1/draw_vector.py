"""
Pybox Draw Vector (Example #1).   Programming with Pybox Demonstration Program.

------------------------
Draw Vector (Example #1)
------------------------
 
The draw_vector() function in pybox draws a vector from point P1 to point P2, with a rounded beginning and an arrow on the end.

draw_vector() is much like a line, but can have 'caps' (i.e. beginning and end 'caps' such as rounded, arrow, etc.), a title, 
varying angles, and can otherwise be controlled in its shape, orientation, and display with various keywords.

Drawing a vector is simple, with only points P1 and P2 needed, as well as a line thickness.  Everything else is automatic
and can be controlled through keywords. 

See draw_vector() documentation (by hovering the mouse over the draw_vector() function in the editor) for information on the various
keywords that can be used to change how the vector displays.

---------------------------------------------------------------------------------------------
Example#1 (this example) - A Vector rounding a circle, using Dev Sliders to control the angle 
---------------------------------------------------------------------------------------------

This example sets up two Dev Sliders to control the angle of a vector rotating around a circle.

The first slider controls where the vector is on the circle.  The vector automatically orients to the circle 'normal'. 

The second slider controls the angle of the slider from its relative placement, allowing the vector to be rotated in place on its 
point in the circle.

-------------
Various Notes
-------------

1. Slider Rollover -- The 'rollover' attribute is set on both sliders.  This means the slider will wrap around when using the mouse wheel.
This allows a smooth motion with the mouse wheel.  Otherwise, with the mouse wheel, the slider would stop at either end without rolling over.

Using the mouse won't rollover/wrap-around.  This only applies to the Mouse Wheel.

2. Dev Slider -- This Draw Vector example also makes a good example of quick and simple usage of Dev Slider, using only 
two lines each: 1) to set up the slider, and 2) to use the slider (getting its value)

3. write_xy() centering and fonts -- note how the write_xy() function is used to center text on multiple lines, as well as 
setting a quick color change and font-size change using {} brackets.

4. Keywords used for draw_vector() - 

The following keywords are used in the draw_vector() call:

        - label_just = "leftcenter" -- This sets the label in the 'left center top' area.  Other options can be left, center, bottom left, etc.
        
        - title = vec_title --  This sets the label on the vector ("label" can also be used).  vec_title is a string already set up for the title. 
                                Otherwise, no title displays on the vector.
                            
        - color="orange" -- This causes the color of the vector to be orange.  The label color defaults to white, but can be changed
                            with the keyword "label_color", e.g. 'label_color="yellow"'
                            
        - set_center=win_center + (x,y) --  "set_center" causes draw_vector() to disregard points P1 and P2, using only the length and angle 
                                            calculated from P1 and P2.  It then sets the center of the line to the point set in set_center, 
                                            then draw the vector at the angle previously calculated for line P1-P2, with any angle setting 
                                            added to this angle (see "angle" keyword")

        - angle=disp_angle+90       --  Since "set_center" is used, and the angle is 0 between P1 and P2, this rotates the vector from it's 
                                        center to this this new angle.  This allows the program to set the circle point as the center and then
                                        set the angle to the angle to the point + 90 degrees to make it normal to the circle. 
 
5. no_auto_update = True -- It basically prevents flickering in real-time graphics loop, by not allowing automatic graphic updates
                            that happen by default for windows.  Try removing it to see what happens.
                            See comments where pybox.new_window() is called. 
                               
6. exit_button() -- This is not necessary, since the program does not end until the user closes the window.  However, it is 
                    always nice to get an indication from the program itself that it has ended.  exit_button() is a quick and 
                    useful function for this purpose.                                                                                                               

-----------
C++ Version
-----------

See the C++ version of the "Draw Vector 1" example in the Sagebox (C++) project. 

"""

import pybox
import numpy as np

# -----------------------
# Create the main window.  
# -----------------------
# 
#   Set "no_auto_update" to turn off automatic window updates. Since the program basically works in a realtime loop
#   re-displaying on each slider movement, the window would otherwise update automatically every 10ms or so which can cause
#   a flicker if the automatic redraw occurs when drawing the main window image on each loop.

window = pybox.new_window(bgcolor="black",no_auto_update=True);

pybox.dev_set_bgcolor("Blue48,SkyBlue");                                                # Set the Dev Window colors, just to look nice. 
pybox.dev_text("Sagebox C++ DrawVector() Function Test",font=18,text_color="cyan");     # Set a basic title on the Dev Window

# Create the sliders.  The "allow_rollover" option allows the slider to rollover when the mousewheel is used, so it 
#                      won't stick to the edges (i.e. minimum and maximum values), allowing a smooth rotation when using the mousewheel
#                      ("default=-90" on the first slider sets the vector on the top of the circle vertically.)

slider_vec_pos      = pybox.dev_slider("Vector Position",range=(-180,180),allow_rollover=True,default=-90);
slider_vec_angle    = pybox.dev_slider("Vector Angle",range=(-180,180),allow_rollover=True);

radius = 200;   # Basic radius for our circle and where the vector should go.


# Loop until the user closes the window, redrawing the image each time.
#
# note: The event loop stops the entire program execution until some event happens, such as a mouse click, slider movement, etc.
#       The first event always falls through to allow one complete display loop before stopping for events.

while pybox.get_event():
    window.cls();               # Clear the window to get a fresh start
    window.draw_grid();         # Draw a graph-like grid
    
    # Write the main titling, which is a large title with a smaller sub-title in a different color
    # "centerx" centers it in the X-dimension on both lines.

    window.write_xy(0,70,"{50}Sagebox C++ DrawVector() Function Test\n"
                    "{18}{lightgreen}Also Keyword Functionality Tests - Classic Keywords and Functional Keywords",
                    textjust = "centerx");
 
    # Move around the circle, drawing a vector at each point
    
    vec_pos     = slider_vec_pos.get_pos();     # slider positions
    vec_angle   = slider_vec_angle.get_pos();

    disp_angle  = vec_pos+vec_angle;    # The display angle is both slider angle values added together

    if disp_angle >= 360 : disp_angle -= 360;
        
    x = np.cos(vec_pos*3.14159/180)*(radius+7.5 + 5.0)  # move center of line out so it is on the circle edge:
    y = np.sin(vec_pos*3.14159/180)*(radius+7.5 + 5.0)  #   7.5 for 15-pixel border width and 5.0 for 10-pixel line width

    win_center = np.array(window.size())/2 + (0,35)     # bring the center down some pixels (e.g. 0,35) so it is a little off-center (looks nicer)
    
    window.draw.circle_l(win_center,radius,"lightblue",pen_size=15)     # draw the main circle with a border size of 15 pixels
    window.draw.fill_circle_l(win_center,15,"lightblue")                # draw a small filled circle int the center of the main circle

    vec_title = "Rotation Angle = {} deg.".format(vec_pos)              # title of the vector as it rotates.
    
    # draw the vector with various options, setting the label justiciation, vector color
    #    notably, the vector is set at (0,0),(350,0) to set a straight vector so we later readjust it by setting the center
    #    with "set_center" and then change the angle with "angle", so the (0,0),(350,0) just really specified a horizontal length.

    window.draw_vector((0,0),(350,0),10,"orange",label_just = "leftcenter",
                           title = vec_title, set_center=win_center + (x,y),angle=disp_angle+90)
    

    # note that there is no window.update() call at the end of this loop.  
    #    The pybox.get_event() call automatically updates the window as necessary.
    #    Since the first event falls through we're guaranteed at least one update on the loop back to pybox.get_event() on top.


pybox.exit_button();    # put up a little windowed button to let the user know the program is over.
                        # not necessary, but it's nice to get the message.