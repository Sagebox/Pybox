"""
--------------------------------------------------------------------------------------------------------
Pybox Image View Window with OpenCV Demonstration (img_view() and img_zoom() functions) - Simple Version
--------------------------------------------------------------------------------------------------------

See img_view_opencv.py for documentation on img_view()

This example is a simple version of the img_view_opencv.py example to show using img_view in a simpler manner,
as a fire-and-forget one-liner with no options.

------------
This example
------------

This example shows one line being used to bring up the window.

In this case, the "wait_for_close" option is used and img_view() won't return until 
the user has closed the window.

When this option isn't used, the program can continue and other windows can be launched and other GUI
activities in other packages can take place. 

The window is fire-and-forget and manages itself, closing itself down when the user closes the window.

Also see img_zoom_simple for a version that brings up the zoom box.

Also see img_view_simple2.py for a version that does a little more, not using the wait_for_close option and 
doing various things in an event loop.

----------------------
Using the Image Window
----------------------

Once the image appears, you can resize the window, zoom in and out with the mouse wheel
and move the image around (when it is zoomed in) with the mouse. 

You can right-click on the window to reset the image.

Use the upper-left system menu of the window for more options including the zoom box, 
closing all image view windows, etc. 

You can also maximize the window with the maximize button or dragging the top menu bar 
to the top of the screen and releasing it.

When the window is un-maximized, it returns to its previous size.

"""

import pybox
from pybox import conio
import numpy
import cv2

# read the image with cv tools.  If the image doesn't load, cv tools will complain.
# in the previous version, the NoneType status of the image was checked.

# In this version, it just gets passed to img_view() unchecked, which will complain just
# as cv tools did about the image not being valid. 

cvimage1 = cv2.imread("Tiger.jpg")

pybox.show_imgview_instructions()           # Remove this -- this shows instructions and is just for the example. 

# img_view_r() is being used instead of img_view() to display the bitmap in reverse (top to bottom).
# 'reverse' can also be used as an option in img_view() to perform the same function

# use wait_for_close option to pause the program until the user closes the image. 

pybox.img_view_r(cvimage1,waitforclose=True)    # can also use img_view_r(cvimage1,opt.wait_for_close()); 
                                                # opts='waitforclose' also works

