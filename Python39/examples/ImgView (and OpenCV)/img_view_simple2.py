"""
-----------------------------------------------------------------------------------------------------------
Pybox Image View Window with OpenCV Demonstration (img_view() and img_zoom() functions) - Simple Version #2
-----------------------------------------------------------------------------------------------------------

See img_view_opencv.py for documentation on img_view()

------------
This example
------------

This example is a simple version of the img_view_opencv.py example showing bringing up the image_view window
and then looking at it in various ways.

This example shows one line being used to bring up the window, using the img_view() with the 'reverse' option to 
reverse the bitmap vertically, instead of img_view_r() which does this automatically.

In this example, the return class object is saved so we can look for an event in the window
and also close it ourselves.

Instead of waiting for the window to close before returning (by using the "wait_for_close" option), the program continues. 
More windows can be opened and GUI items from other packages used, as the window is self-managing.

It does not need to be monitored, but can be if you want to control it yourself or know when someone closed the window.

See the comments in the code below. 

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
import numpy
import cv2

cvimage1 = cv2.imread("Tiger.jpg")

cvimage1 = cvimage1 / 255           # divide the image so it is a floating-point image from 0-1
                                    # the 'normalized' keyword tells img_view that it is a normalized image (0-1)

# 'reverse' is used to reverse the image vertically.  Open CV returns 
# "right-side-up" bitmaps, where pybox defaults to standard "reversed" bitmaps.

image = pybox.img_view(cvimage1,reversed=True,normalized=True)    # can also call img_view_r(cvimage1) to reverse the image
                                                                  # 'normalized=True' tells img_view the image is 0.0-1.0 and convert it to 
                                                                  # a displayable RGB bitmap.

# Create a close button so we can close the window by pressing it. 

close_button = pybox.dev_button("close window")

# Enter the event loop where the program is shut down until an event occurs in the system
# The loop will exit when both the image view window and the dev window is closed.
#
# note: 
#
#   we could just break out of the loop or quit() when the close button is pressed
#   or we see that the window is closed, which would close down the windows
#   and exit the program cleanly and safely.
#
#   The event-checking here is for an example of using events.

while pybox.get_event() :

    # Look for a close event on the window, telling it the user closed it. 

    if image.close_event() : 
        pybox.debug_write("{y}Window was closed by user.\n")

    # Check if the close button was pressed
    # if the image is already closed, print a message stating we know that

    if close_button.pressed() :
        if image.closed() :
            pybox.debug_write("image already closed\n")
   
        pybox.debug_write("{g}Press 'x' button in Dev Window to exit.\n")

        # Close the window.  If it is already closed, this has no effect, so it is
        # safe to call it either way.

        image.close_window()
