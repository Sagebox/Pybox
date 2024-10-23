
# ******************
# Happy Face Example
# ******************
#
# This is just a simple program to draw a happy face in the window.
#
# This example shows some of the drawing functions in Pybox and some general usage, such as creating the intial window
# and using exit_button() to put up a message for the user that the program has ended.
#
# Some notes:
#
# - The write() and write_xy() functions can use embedded nomenclature, such as setting the font or color.
#   In this example, "{65}" is used to set the font in the second write_xy() example, setting the font to
#   an "arial,65" font.  "font=65" could also be used as a keyword.  With a keyword, you can set a more 
#   specific font, such as 'font="Times New Roman,65,bold,italic"
#
#   Although not shown here, colors can be embedded, too, such as "{green}" (or "{g}" for short)
#   using "{}" to end the color, such as "this is {g}text is in green{}, and this is now back to the original color"
#
# - pen_color="blue,green" causes the border (with pen_size=10) to draw as a gradient from blue to green.
#   the pen gradient angle can be changed, as with 'pen_gradient_angle=45', etc.
# 
#   To draw a gradient in the circle, just specify two colors, such as "yellow,green" instead of the "yellow"
#   used in the program below.
#
# - arc() is just a simple arc function.  The "-150,120" represents the "start angle" and "sweep angle" of the arc
#   line_caps-"round anchor" puts 'caps' on the beginning and end of the arc.   Different caps can be used such 
#   as "round" (default), "square", "arrow", "arrow anchor", etc. "flat" will remove the caps.
#
#   Put the mouse over the arc() function below for more information
#
# - exit_button().  Since the program does not loop, the program would end and the window would close as soon 
#   as the program ended.  exit_button() puts up a message in a box for the user explaining that the program is finished,
#   and also prevents the program from ending, keeping the window open util the user pressed "ok"
#
#   There are a few other ways to keep the window from closing, such as window.wait_for_close(), etc.

import pybox
 
window = pybox.new_window(bgcolor="black,midblue")
window.write_xy(0,50,"Remember when programming with Graphics\n{40}was easy and fun?",font=40,center_x=True) 

window.draw.fill_circle(590  ,405,180,"yellow",pen_size=10, pen_color="blue,green")
window.draw.fill_circle(510  ,360,30,"black",pen_size=5) 
window.draw.fill_circle(670  ,360,30,"black",pen_size=5)
window.draw.arc        (590  ,410,100,100,150,-120,"black",pen_size=10, line_caps="round anchor")
  
# {65} sets an "arial,65" font.  The keyword font=65 can be added as a keyword instead.

window.write_xy(0,650,"Sagebox does.",font=65,center_x=True)

pybox.exit_button() # Since we're not in a loop waiting for something, this shows the user the program is over.
                    # Otherwise, the program would and and the window close immediately.

