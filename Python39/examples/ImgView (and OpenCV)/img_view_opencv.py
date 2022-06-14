"""
---------------------------------------------------------------------------------------
Pybox Image View Window with OpenCV Demonstration (img_view() and img_zoom() functions)
---------------------------------------------------------------------------------------

This module shows the img_view() function used to view two images. 

The image_view() functions can be used to bring up bitmaps in a sized or auto-sized window that then can be zoomed in, resized, 
and can use the Zoom Box for easier navigation.

--------------------------------------------
Using with modules like SciPy, Open CV, etc. 
--------------------------------------------

    Pybox is meant to work as a library so it can work easily with other libraries.  In this example, it is showing reading images via Open CV and then displaying them.
    
    img_view() supports all basic RGB image types, such as float, double, grayscale, RGB, split or interlaced (i.e. RRR,GGG,BBB vs. R,G,B), as well as 4-byte aligned or
    non-aligned bitmaps.  img_view() also supports 16-bit float bitmaps. 
    
    Pybox has its own Bitmap class, but this is not necessary to use most of the bitmap functions in pybox. 

------------
This Example
------------

    This example shows a fairly small usage of img_view().  It loads two images using a different options for img_view().  
    While img_view() can be launched with just the image, options are used to show different things. 

    The code is fairly small, about 15 lines of code, but with a lot of comments showing what the 
    pybox functions are doing. 

    This example does the following:

    1. Loads two images.
    2. If either image isn't found, it writes out an error message in read
       demonstrating using the pybox conio functions for console output
    3. Both images are placed in specific places to show that the images can be ordered on the screen
    4. One image is set to a maximum initial size which can be resized by the user later.
       It uses a "0" for the Y dimension which causes img_view() to look for the best fit in the X dimension given
    5. A function is called to show the instructions.  This is basically for the demo, but can be useful in other cases wher
       users may not know all of the options about the img view window.
    6. wait_for_any() is called to look for either window to close.  You can also call wait_close_all(). 
       You can select "close all Image View Windows" from the upper-left system menu from each window.
    7. One one window is closed, the program continues. 
    8. A pybox event loop is entered (unless "close all windows" was used, then it is skipped because get_event() will
       return false when there are no open windows)
    9. In the event loop, when the other window is closed, the close_event() is triggered (just once for the specific window)
       and a message is printed to the Pybox Debug Window.


-------------------
Simple and Featured
-------------------

    When an image view window comes up, it looks fairly innocuous, just an image in a window.

    The invocation of img_view() is also very easy: 

        img_view(myimage)

    This will bring up an image automatically that can be resized, zoom in, moved around, etc.  

    There are many options you can add to the img_view() call and a large set of features that come with an image view window.
    See the next section for more information


-----------------
img_view features
-----------------

    1. easy to bring up with one small line of code. Simply bring up an image with img_view(myimage) or img_zoom(my_image)

    2. Add easy titling and location options - 
        img_view(myimage,"This is the title") sets the title bar in the window
        img_view(myimage,"This is the title",at(500,200)) puts the window at (500,200) on the screen
        img_view(myimage,"This is the title",size=(700,0)) selects the best fit for a width of 700 for the initial window

    3. Smart intial window size - The initial window sizes itself to a reasonable size on the screen -
       If the image is large, the zoom reduced.  If the image is small, it is displayed at its original size.

    4. Can display bitmap upside-down -  Between packages and systems, bitmaps can be in reverse order vertically -
       The 'reverse' option or using img_view_r() or img_zoom_r() will reverse the direction of the bitmap.

    5. Multiple img_view() Windows -   Multiple img_view windows can be opened at once.
    4. Window Resize.  You can drag the window corners to resize the window.  The image size will automatically change.

    6. Zoom in and out and Move Around - You can Zoom in and out of the image view window with the mouse wheel.
       You can also move the image around with the mouse when it is zoomed in.
       You can then right-click on the window to fit it back into the window or use the upper-left system menu
       for more options

    7. Image Zoom Box -  The Image Zoom Box is a navigator where you can easily zoom in and move around the image. 
       The Zoom Box can be launched by selecting the upper-left system menu.
       The Zoom Box can be automatically launched by using img_zoom() instead of img_view() or setting 'zoom_box' as an option

       When multiple windows are open, clicking on different windows changes the Zoom Box to display the thumbnail and work 
       with the newly-selected image.

    8. Windows Collectively Managed - Pybox can manage all open windows where you can use the following functions

        o wait_for_close()          - wait for the specific window to close (i.e. myimage.wait_for_close())
        o wait_close_all()          - wait for all windows to close
        o wait_close_any()          - wait for any window to close.

    9. Fire and Forget -  When you launch an img_view window, you can save the result of the image_view() call to 
       manage the window as shown above. 

       You can also just call the function in a fire-and-forget fashion.  The window will close on its own
       when the 'X' button is pressed.   You do not need to wait for the image to close to perform other functions.

    10. Close Status and Close Events -  There are a couple functions that can be used to determine the status of the window

        o closed()          - This will return True if the window is closed (i.e. has been closed by the user or otherwise closed)
        o close_event()     - This will return True when a close action has occured.  As an event, it returns True once to let you 
                              know about the event, then false afterward so that it can be used in an event loop without needing to 
                              keep the status. 

    11. Labels - You can use the 'label' option to set a label that will display on the bottom of the image. 
                 If a Title is not specified, the label also appears as the Window's title in the title bar.

                 example: image_view(my_image,label="This is my image")

"""

import pybox
from pybox import conio
import numpy
import cv2

# read in a couple sample images with OpenCV. 
# pybox also has some read functions. Here, we're showing pybox working with other tools. 

cvimage1 = cv2.imread("Tiger.jpg")
cvimage2 = cv2.imread("dog.jpg")

# make sure the images exist.  Not strictly necessary but might as well. 

if cvimage1 is None or cvimage2 is None :
    conio.write("{r}Img View Test: Could not open bitmaps\n")   # put out the message in red so it is more easily seen.
    quit()

# img_view_r() is being used instead of img_view() to display the bitmap in reverse (top to bottom).
# OpenCV brings in the bitmaps right-side up, and the pybox default is the standard
# upside-down bitmap. 
#
# img_view() with a 'reverse' or opt.reverse() can also be used to flip the bitmap.

# Show the first image.  "Image 1" is the title, and at(520,0) is where to put it.
# These are optional parameters: img_view_r(cvimage1) can also be used for automatic placement and sizing

my_image1 = pybox.img_view_r(cvimage1,"Image 1",at=(520,0))                 # can also use just img_view_r(cvimage1)

# Show the second bitmap, but with a size. 
# the size will make the image smaller in the window.
# size option is best fit.  When one value is 0 (i.e. (500,0)) the best fit is used for the 
# used value (width or height)
## If the bitmap is not as large as the requested size, the bitmap is not enlarged.

my_image2 = pybox.img_view_r(cvimage2,"Image 2",at=(0,0),size=(500,0))

# Show the instructions on how to use the image view window. 

my_image1.show_instructions()

# Wait for any of the window to close.  wait_close_all() can be used to wait for all window.  
# my_image1.wait_close() can be used to specifically wait for this window to close. 

my_image1.wait_close_any()

pybox.debug_write("closed a window\n")      # write to the debug window that we closed a window

# We can just quit here, but instead we'll wait for events. 
# get_event() will return false when no primary windows are open
# (image view windows are primary windows, where the instruction window is not)

while pybox.get_event() :

    # look for close events on either window an show it in the debug window when it is closed (i.e. an event)
    # as an event function, close_event() will only return true once for the event and then false after so that it
    # can be used in a loop and does not need to be reset (since it resets itself)

    # this is different than the image.closed() function will returns true every time if the window is closed and
    # false if it isn't.
    
    if my_image1.close_event() : pybox.debug_write("{y}Window 1 closed.\n")
    if my_image2.close_event() : pybox.debug_write("{g}Window 2 closed.\n")

# Now that we're done display an exit_button().  We could just leave, but the exit button will keep the
# debug window open until OK is pressed -- otherwise the program would end and all windows would close. 

pybox.exit_button()

