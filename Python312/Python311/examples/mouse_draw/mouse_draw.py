
# ***************************
# Pybox Mouse Drawing Example
# ***************************
#
#    This program is a very short program to show how useful pybox can be with just a few general pybox functions, such as
#    looking for the mouse click, mouse movement, and drawing lines. 
#
#    The program itself is about 20 lines, and uses common pybox functions.  That is, its not esoteric and is a good way to
#    learn how pybox works.
#
# -----------------
# Using the program
# -----------------
#
#    Just draw on the screen!  The colors change automatically.  Right-Click the mouse to clear the screen, and use the Mouse Wheel to increase the
#    thickness of the lines drawn.

import pybox
import random
  
win = pybox.new_window()            # Create a new window of default size and purposely no      
                                    # pybox.new_window("Mouse Draw Demo") will add a title in the title bar 

pen_size = 4                        # initial pen size
win.draw.set_pen_size(pen_size)     # set the pen size for the window

win.cls("black,darkblue")         # clear the window with a black-to-dark-blue gradient
   
# create a fire-and-forget, persistent text message
#
# pad_y(5) -- moves the Y position of the text widget down 5 pixels so it isn't so
#             abrupt on the top edge. 
#
# opt.style can also be used here, such as opt.center_x(), opt.pad_y(5), etc. for
# intellisense, auto-complete, ensured correct spelling, etc. 

text = win.text_widget(0,0,width=win.width(),centerx=True,font=18,pad_y=5,textcolor="cyan"); 

def show_banner() :
    text.write("Pen Size = {} -- Use Mousewheel to change thickness, right-click to clear screen".format(pen_size))

show_banner()               # Show the initial top-text
cur_color = "yellow"        # not really needed since the first mouse click sets it. 

# Look for events.  get_event() returns false when the window closes. 
#                   The program is asleep until an event occurs

while win.get_event() :

    # If the mouse is clicked, set a new pen color

    if win.mouse_clicked() : 
        cur_color = pybox.get_hue_color(random.randint(0,360))

    # When the right-mouse button is clicked, clear the window

    if win.mouse_r_clicked() : 
        win.cls()

    # If the mouse wheel is moved, set the pen_size up or down

    if win.mouse_wheel_moved() : 
        pen_size += win.get_mouse_wheel_value()     # Set up or down dependig on direction
        pen_size = max(1,pen_size)
        win.draw.set_pen_size(pen_size)             # Negative values default to 1, so we don't 
                                                    # specifically need to check, but its nice to do so
                                                    # so the display won't show negative values
        show_banner()                               # Update the top text

    # If the mouse is moving (or has been clicked) then draw a line from 
    # the previous drag point to the current (last) point.
    #
    # The "True" parameter tells mouse_drag_event to include the initial mouse click.
    # When it is the first click (and the click is included), the previous point (mouse_drag_prev())
    # and current point (mouse_drag_last()) are the same point.

    if win.mouse_drag_event(True) :
        win.draw.line_l(win.mouse_drag_prev(),win.mouse_drag_pos(),cur_color)
