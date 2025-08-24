# ----------------------------
# Pybox  Dial Widget Example
# ----------------------------
#
# This example shows using a Widget that is not included in the main library.
# Widgets can be written by anyone and can be distributed and use the same pybox module.
#
# Widgets can be anything that a window can use, such as as a Text Widget, Color Selector, Curves Window, Graphing, etc. 
# In this case, a simple dial similar to a dial on a wall.
#
# In this case, the "Dial Widget" is used.  The Dial Widget is an example widget to show widgets in their
# various forms.
#
# ---------------------
# About the Dial Widget 
# ---------------------
#
# This dial widget was written specifically as an example of how Widgets work in pybox.  Also see the LCD Widget example
#
# The Dial Widget is a simple dial with a range, which can be set.  It has a dial to change the value, as well as a
# couple arrow buttons to change the value one step at a time.
#
# The source code for the Dial Widget will be released as an upcoming example of creating widgets. 
#
# notes:
#
#      1. right-click on the dial widget.  This will bring up some selections: 
#         The "Debug Output" shows some debug information in the window
#         The "Debug Window" option shows a primitive graph determining how to higlight the ring.
#      2. Note that the dial widget is attached to the window created below.  It is its own window set inside
#         of your window as a "child window". Some widgets will pop up as an individual window, while others
#         (such as the Color Selector) give a choice as an option.
#      3. This example shows how to use the Event Loop with GetEvent().  You can also 
#         use the Windows event structure/methodology via events from the Dial Widget.
#
# *** Note: This can be a Console Program with a Console Window or a Pure Windows program.  See the Build->Configuration settings.

import pybox
import dial_widget

window = pybox.new_window("Dial Widget Example",size=(320,325));

# Create the dial widget at the location specified and 
# range of 200-300.  Sets the default at 227. 
#
# None of these options are required, and there are functions
# to set the range, location, and value.

widget = dial_widget.create(window,(50,30),range=(200,300),default=227)

# Set a couple things with the dev window.
#
# 1. Set the location at 425,50 to the right of the window we just created
# 2. Set autoclose to true, which will close the Dev Window when the main window is closed.
#    otherwise, when the main window is closed, the Dev Window will remain open and an 'x'
#    will appear in the upper-right of the window to the user can close it.
#
#    try removing the autoclose keyword (or setting it to False) then closing the Main Window.
#
# note:  Two functions can be used independently instead (dev_set_config is a shortcut):
#
#   pybox.dev_set_auto_close()
#   pybox.dev_set_location(425,50)

pybox.dev_set_config(loc=(425,50), autoclose=True)

# Create a sub-window in the Dev Window so we can write out some data
#
#   label_font  -- Sets the font of the top label
#   label_color -- Sets the color of the top label
#   font        -- Sets the font of the window itself
#
# The above options are not required and are used to personalize the window

dev_win = pybox.dev_window("Dial Widget Output",font=15,labelfont=14,labelcolor="cyan")

dev_win.write("Turn the dial on the dial widget.\n\n")

# Create a persistent fire-and-forget widget with the title, set below the dial widget.
# note: just_bottom_cente=true (or justbottomcenter) can be used to automatically
# place the text at the bottom

window.text_widget(0,270,"Dial Widget Example",centerx=True,font=20)

# A simple event loop that only looks for value change events in the dial widget

while pybox.get_event() :

    # value_changed() is an event call and only returns true once per change.
    # the program is asleep until we get an event, where we can check the value.
    #
    # This writes the value to the debug window as the value is changed in the widget. 

    # {y} sets the color to yellow.  {{y}} is used here because of the .format()
    # after the text. 

    if widget.value_changed() : dev_win.write("Value = {{y}}{}\n".format(widget.get_value()))
