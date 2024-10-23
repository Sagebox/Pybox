
# -----------------------------
# Color Selector Widget Example
# -----------------------------
# 
#  This is an example of using external Widgets that use pybox as a client, where the pybox tools can be used
#  to provide standalone tools. 
# 
#  ---------------------
#  Color Selector Widget
#  ---------------------
# 
#       The Color Selector widget is a quick way to get a color from the user.  The user can enter RGB values or use the mouse to select
#       the color.  This is the first version of the Color Selector, and newer version will support other color models, such as LAB and HSL,
#       and also have an option to use a rectangle rather than a triangle for more accurate color selection.
# 
#       The Color Selector uses the Color Wheel Widget, which is a widget that can be used to obtain more informal colors quickly, 
#       and is easier to embed in the window, rather than using it as a separate window.
# 
#       The Color Selector can be used as a separate window or embedded in the parent window, though most usage is better off as a 
#       separate window.
# 
#       The Color Selector has many options, only some of which are in color_selector.py module (to be expanded soon)
# 
#       CColorSelector is still in progress, and some thing may not be documented.
# 

import pybox
import numpy

# Create a small pybox window where we can draw a rectangle with the currently-selected color
# in the color widget

win = pybox.new_window("Color Selector Widget Example",size=(400,430));     

# Create the color selected as its own popup window.  
# When color_selector.create(win,..) is used, the Color Selected is embedded as a child window
# at the location specified.

c_select = win.color_selector((500,50),popup=True)   # Set it at 500 pixels out, right next to the window just created
                                                     # we can also use a title keyword here, such as title="This is the window title"

c_select.set_rgb_value([0,255,0])           # pre-select a green color (default is red)

# Create a couple persistent fire-and-forget text widget messages, one larger and one a subtitle
#
# the keywords can also be expressed as opts='font=20,centerx'
# centerx can also be center_x and textcolor can also be text_color

win.text_widget(0,370,"Color Selector Widget Example",font=20,centerx=True)
win.text_widget(0,395,"Select Color to Draw Rectangle",font=12,centerx=True,textcolor="CornflowerBlue")

# Enter the main event loop where we can look for things happening

while (pybox.get_event()) :

    # If the value has changed then fill a rectangle in the main window
    # with the color.  Also write out to the debug window the RGB value.
    # 
    #  (this is an event, so it only returns True once per change)

    if c_select.value_changed() : 
        rgbColor = c_select.get_rgb_value()

        # {c} sets the color to cyan. {{c}} is used because of the
        # formatting with .format()

        pybox.debug_write("Value Changed: {{c}}{}\n".format(rgbColor))
        win.draw.fill_rectangle(50,50,300,300,rgbColor)

    if win.mouse_clicked() :
        c_select.show()         # if the mouse was clicked in the main window show the color selector
                                # (pressing OK hides it as an example, and this will bring it back)

    # Show when the window_close() is pressed.  This also issues a cancel event so cancel_pressed() will also return true
    # even though closed by the user, it is really just hidden, so we can re-show it.
    #
    # Also, c_select.disable_close() can be used to prevent the user from closing the window manually.
    
    if (c_select.window_closed()) :
        pybox.debug_write("{p}Window was closed by the user.\n{w}Click window to re-show the Color Selector.\n")
        
    # if the OK button was pressed, hide it (to show we can remove it) and also print 
    # a message to the debug window

    if c_select.ok_pressed()     : 
        pybox.debug_write("{g}Ok Pressed{}\n{w}Click window to re-show the Color Selector\n")
        c_select.hide()

    # If cancel we pressed, print a message in the debug window
    if c_select.cancel_pressed() : 
        pybox.debug_write("{y}Cancel Pressed\n")

# Put an exit button at the end of the program.
# We don't really need to do this, but sometimes its nice to get a solid
# indication that the program knows it has ended and that it actually meant to exit on purpose. 
#
# It can also provide a nice way to wrap things up rather than
# deleting everything suddenly.

pybox.exit_button()

 