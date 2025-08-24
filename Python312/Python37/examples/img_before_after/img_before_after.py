"""
----------------------------------------------------------------------------------------------
Pybox Image Before & After View Window with OpenCV Demonstration (img_before_after() function)
----------------------------------------------------------------------------------------------

This module shows the img_before_after() function used to view a before and after image.

An original image is shown, as well as a edge-detection version created with a sobel filter. 


The img_before_after() functions can be used to bring up before & after bitmaps in a sized or auto-sized window that then can be zoomed in, resized, 
and can use the Zoom Box for easier navigation.

--------------------------------------------
Using with modules like SciPy, Open CV, etc. 
--------------------------------------------

    Pybox is meant to work as a library so it can work easily with other libraries.  In this example, it is showing reading images via Open CV and then displaying them.
    
    img_before_after() supports all basic RGB image types, such as float, double, grayscale, RGB, split or interlaced (i.e. RRR,GGG,BBB vs. R,G,B), as well as 4-byte aligned or
    non-aligned bitmaps.  img_before_after() also supports 16-bit float bitmaps. 
    
    Pybox has its own Bitmap class, but this is not necessary to use most of the bitmap functions in pybox. 

------------
This Example
------------

    This example shows a fairly small usage of img_before_after().  The program simply created an edge-detection version
    of an image loaded with OpenCV, then displays the before & after image using the img_before_after function. 

    See other examples (img_before_after2.py and img_before_after3.py) that use more parameters to set a top label, titles for 
    windows, etc. 

    The code is small, about 5 lines.


    This example does the following:

    1. Loads an image with open cv.
    2. if the image is not found, it writes out an error message in red, demonstrating using the pybox conio functions
       for console output
    3. A new image is then created with the sobel filter function.
    4. Now we have two images in two different formats: the original as a color RGB image, and the output as a monochrome float-point bitmap.
    3. img_before_after() is then called to display the two images that are in different formats.
  
-------------------
Simple and Featured
-------------------

    When an image before & after view window comes up, it looks fairly innocuous, just an two images in a window.
    The invocation of img_before_after() is also very easy: 

        img_before_after(myimage,myimage2)

    This will bring up an image automatically that can be resized, zoom in, moved around, etc.  
    
    The input images must be the same size, but can be any any number of different formats, RGB or monochrome.

    There are many options you can add to the img_before_after() call and a large set of features that come with an image view window.
    See the next section for more information


---------------------------
img_before_after() features
---------------------------

    1. easy to bring up with one small line of code. Simply bring up an img_before_after(myimage,myimage2)

    2. Add easy titling and location options - 
        img_before_after(myimage,myimage2,"This is the title") sets the title bar in the window

        img_before_after(myimage,myimage2,label="This is the title") sets the a label at the top above both windows
            --> this also sets the window title, unless 'title' is used. 

        img_before_after(myimage,myimage2,label="This is the title",labelfont=20) does the same as the above,
            but also sets the font of the label.  See the function for more options.

        img_before_after(myimage,myimage2,before_title = "First Image",after_title="Second Image") 
            --> This will set the titles underneath each image accordingly.

    3. Smart intial window size - The initial window sizes itself to a reasonable size on the screen -
       If the image is large, the zoom reduced.  If the image is small, it is displayed at its original size.

    4. Can display bitmap upside-down -  Between packages and systems, bitmaps can be in reverse order vertically -
       The 'reverse' option or using img_before_after() will reverse the direction of the bitmap.

    5. Normalized images.  For floating-point images that are normalized (i.e. between 0-1), adding the 
        normalize=True keyword will display the bitmap as a standard bitmap.

    6. Window Resize.  You can drag the window corners to resize the window.  The image size will automatically change.

    7. Zoom in and out and Move Around - You can Zoom in and out of the image view window with the mouse wheel.
       You can also move the image around with the mouse when it is zoomed in.
       You can then right-click on the window to fit it back into the window or use the upper-left system menu
       for more options

    8. Image Zoom Box -  The Image Zoom Box is a navigator where you can easily zoom in and move around the image. 

    9. Fire and Forget -  When you launch an img_before_after() window, you can save the result of the img_before_after() call to 
       manage the window as shown above. 

       You can also just call the function in a fire-and-forget fashion.  The window will close on its own
       when the 'X' button is pressed.   You do not need to wait for the image to close to perform other functions.

    10. Close Status and Close Events -  There are a couple functions that can be used to determine the status of the window

        o closed()          - This will return True if the window is closed (i.e. has been closed by the user or otherwise closed)
        o close_event()     - This will return True when a close action has occured.  As an event, it returns True once to let you 
                              know about the event, then false afterward so that it can be used in an event loop without needing to 
                              keep the status. 

"""


import pybox
from pybox import conio
import sobel
import numpy as np
import cv2

cvimage = cv2.imread("dog.jpg")                         # load image with opencv


# if the image doesn't exist print out a message in red
# This uses the pybox conio class. 
#
# {r} = set text color to red. 

if cvimage is None :
    conio.write("{r}Error: Could not load bitmap.\n\n")
    quit()

cvimage = cv2.cvtColor(cvimage,cv2.COLOR_BGR2RGB)   # Convert to RGB
# use the sobel filter to do an edge detection on a grayscaled version of our loaded image

img_result = sobel.filter(cv2.cvtColor(cvimage, cv2.COLOR_BGR2GRAY))

# show the before & after image with a color image before image and grayscaled after image. 
#
# This example is a simple fire-and-forget call that waits until the image is closed by the user.
# There are no parameters execept the images. 
#
# Since "wait_for_close" (or "waitforclose") is used, the function does not return until the user closes the window.
# When "wait_for_close" is not used, program execution continues with no problem -- the Image View window is self-
# managing and will close on its own when the user closes it, the program ends, or it is closed by the program.
#
# See img_before_after2.py and img_before_after3.py for examples using more
# options such as labels, titles, etc.

pybox.img_before_after_r(cvimage,img_result,wait_for_close=True)      # wait_for_close not necessary (window self-manages)

# << more program elements here while the image window is or isn't open >>
#
# In our case, we just end the program.

