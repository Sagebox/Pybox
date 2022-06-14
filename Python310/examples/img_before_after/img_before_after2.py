"""
----------------------------------------------------------------------------------------------
Pybox Image Before & After View Window with OpenCV Demonstration (img_before_after() function)
----------------------------------------------------------------------------------------------

See img_before_after.py for documentation on img_before_after()


This module shows the img_before_after() function used to view a before and after image.

An original image is shown, as well as a edge-detection version created with a sobel filter. 

------------
This example
------------

This example adds a top label and  Before and After Title to the img_before_after() window.

see img_before_after3.py for a more extensive use of parameters and other uses of
img_before_after();

"""

import pybox
from pybox import conio
import sobel
import numpy as np
import cv2

cvimage         = cv2.imread("dog.jpg")     # load image with opencv

# if the image doesn't exist print out a message in red
# This uses the pybox conio class. 
#
# {r} = set text color to red. 

if cvimage is None :
    conio.write("{r}Error: Could not load bitmap.\n\n")
    quit()

# use the sobel filter to do an edge detection on a grayscaled version of our loaded image

img_result = sobel.filter(cv2.cvtColor(cvimage, cv2.COLOR_BGR2GRAY))

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

