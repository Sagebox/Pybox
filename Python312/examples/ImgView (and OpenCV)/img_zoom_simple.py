"""
-----------------------------------------------------------------------------------------------------------------
Pybox Image View Window with OpenCV Demonstration (img_view() and img_zoom() functions) - Simple Zoom Box Version
-----------------------------------------------------------------------------------------------------------------

See img_view_opencv.py for documentation on img_view()

This example is a simple version of the img_view_opencv.py example to show using img_view in a simpler manner,
as a fire-and-forget one-liner with no options.

In this case, the zoom box is brought up with img_zoom() instead of image_view().

img_view() can be used with the "zoom_box" option, where img_zoom() is a convenient way to do the same thing.

------------
This example
------------

This example shows one line being used to bring up the window.

In this case, the "wait_for_close" option is used and img_zoom() won't return until 
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

------------------
Using the Zoom Box
------------------

The Zoom Box is fairly self-explanatory, but some notes:

    1. Use the mousehweel when the mouse is over the thumbnail or slider to quickly zoom in and out
       (you can also zoom in and out when the mouse is in the main image view window)

    2. grab the square in the thumbnail to move the window.
    3. You can also grab the image in the main image view window and the zoom box will track the changes.
    4. Hover over the slider handle to show the tool-tip.
    5. double-click on the handle to set 100% zoom
    6. Press the control-key when using the mousehweel on the slider for fine increments on the zoom
       (1 at a time instead of 30 or so)
    7. You can close the zoom box and it will not close the image.
    8. You can re-open the zoom box by clicking in the upper-left system menu of the image view window.
    9. If the Zoom Box was never launched, you can open it by using the above step
       (clicking in the upper-left system menu of the image view window)

    
"""

import pybox
import numpy
import cv2

cvimage1 = cv2.imread("Tiger.jpg")

cvimage1 = cv2.cvtColor(cvimage1,cv2.COLOR_BGR2RGB)   # Convert to RGB

pybox.show_imgview_instructions()           # Remove this -- this shows instructions and is just for the example. 
 
# img_zoom_r() is being used instead of img_zoom() to display the bitmap in reverse (top to bottom).
# 'reversed=True' can also be used as an option in img_zoom() to perform the same function
#

pybox.img_zoom_r(cvimage1,waitforclose=True)     # pybox.img_zoom_r("Tiger.jpg",waitforclose=True) works, too, when its
                                                 # just a read from an image file, eliminating the line above.
                                                


