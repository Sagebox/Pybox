# ------------------------
# Pybox LCD Widget Example
# ------------------------
#
# This is an example of using an external/standalone Widget that may be written and provided by anyone to use
# with pybox.
#
# This example shows a simple use of an "LCD Widget", which is really just a simple counter that looks like an LCD.
#
# About the LCD Widget
# --------------------
#
# The LCD widget has a few different modes, but, right now, is basically just a counter. 
# The intention is to expand this widget into an LCD emulator, what can have various forms, depending on how much
# you want to emulate, from simple counting, to piecing together numbers and letters, all the way down to 
# communicating with the hardware device and the I/O level.
#
# This example just shows counting to focus on how to install and use a widget easily.
#
# *** Note: This can be a Console Program with a Console Window or a Pure Windows program.  See the Build->Configuration settings.

import pybox
import lcd_widget

win = pybox.new_window("LCD Emulation Widget Example",size=(350,250))
win.cls("skybluelight,skybluedark")       # Set a nice background gradient. 
                            
# Create the lcd widget.  It will place itself in our window
# at the location specified. 
# 
# lcd_widget.popup() will open in its own demonstration window
# (which can be used without declaring the window above)

lcd = lcd_widget.create(win,at=(25,25))

# Set a presistent text-widget title underneath the LCD widget

win.text_widget(0,170,"LCD Emulation Widget Example",font=18,center_x=True)

# Loop for 1,000,000 iterations and display the value
#
# By default, the LCD is upated on every set_value() call. 
#
# Setting fast mode will make this loop complete nearly instantly
# since it will only update as needed (about every 20ms or so)
#
# Note that fast mode requires a call to last_update() after the loop
# to ensure it updated the last value. 

for i in range(0,1000000) :
   lcd.set_value(i)
   if win.closed() : break;     # break out of the loop of the user closed the window

# Put up an exit button.  Not strictly necessary, but it can be nice to get 
# the "program ended" message as an indication the program meant to close.

pybox.exit_button();


