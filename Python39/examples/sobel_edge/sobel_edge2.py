"""
------------------------------------------------------------------------
Pybox Sobel Image -- showing using Open CV with pybox.img_before_after()
------------------------------------------------------------------------

This is a simple program showing preforming a sobel filter with an image read with
Open CV and displayed using img_before_after() with pybox.

The input (before image) and output (after image) are two different types.

img_before_after() supports many times of images. 

See img_before_after.py and img_view.py examples for more information on using these functions.

------------
This Example
------------

This example uses a some options of the img_before_after() function to show adding labels to the
before & after images, as well as a label above the two images. 

See the img_before_after.py examples for even more varied usage of img_before_after()

Also see img_view() examples. 

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
import numpy as np
import scipy,cv2
import scipy.ndimage as ndimage

def sobel_filter(img) :
  Kx = np.array([[-1, 0, 1], 
                 [-2, 0, 2], 
                 [-1, 0, 1]])

  Ky = np.array([[1, 2, 1], 
                 [0, 0, 0], 
                 [-1, -2, -1]])

  Ix = ndimage.convolve(img, Kx,output = float) # Get X plane
  Iy = ndimage.convolve(img, Ky,output = float) # Get Y Plane

  G = np.sqrt(np.square(Ix) + np.square(Iy))    # Get gradient

  G = G/(G.max()*.5)        # brighten it a little

  # The value below is multiplued by 255 to make standard RGB bitmap (floating-point)
  # with values from 0-255.
  #
  # Without this, the values would range from 0-1. 
  # This works with img_view() and img_before_after() when the 'normalize=True'
  # keyword is used (i.e. when the *255 is omitted).

  G = np.clip(G,0,1)*255        # clip is since values can go over 1.0

  return G  # return the new image (floating-point RGB image)

# Main Code (__main__)

cvimage         = cv2.imread("dog.jpg")

# if the image doesn't exist print out a message in red
# This uses the pybox conio class. 
#
# {r} = set text color to red. 

if cvimage is None :
    conio.write("{r}Error: Could not load bitmap.\n\n")
    quit()

cvimage = cv2.cvtColor(cvimage,cv2.COLOR_BGR2RGB)   # Convert to RGB

# use the sobel filter to do an edge detection on a grayscaled version of our loaded image

img_result = sobel_filter(cv2.cvtColor(cvimage, cv2.COLOR_BGR2GRAY))

# show the before & after image with a color image before image and grayscaled after image. 
# This example uses an after_title and label to personalize the window.
#
# img_before_after_r() is called to reverse the image, as Open CV returns a 'right-side-up'
# bitmap and pybox defaults to the standard 'upside-down' format. 
#
# Since "wait_for_close" (or "waitforclose") is used, the function does not return until the user closes the window.
# When "wait_for_close" is not used, program execution continues with no problem -- the Image View window is self-
# managing and will close on its own when the user closes it, the program ends, or it is closed by the program.
#
# Without "wait_for_close" the program execution would continue with no problem. 

pybox.img_before_after_r(cvimage,img_result,after_title="Sobel Image",label="Sobel Before & After Image",waitforclose=True)

# << more program elements here while the image window is or isn't open >>
#
# In our case, we just end the program.


