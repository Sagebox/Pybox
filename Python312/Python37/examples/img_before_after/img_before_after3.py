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

This example shows how the image_before_after() function can manage itself or the program can manage it.

The window manages itself, so the program can continue and do other things while the window is open.

In this case, we want to know when the window is closed, so we can look for a widow close event. Or, 
as in this program, we may want to close it in response to an event.

This program does the following:

    1. loads an image with open CV
    2. Create a sobel edge-detected image 
    3. Displays the before & after images with img_before_after()
       --> In this case, wait_for_close is not used, so the img_before_after() function
           returns immediately with the before & after window still open
    4. Two buttons are created: a Close Window Button and a Quit Program Button
    5. The program then looks for events.
       a. When the Close Window button is pressed, the image view window is closed, and the
          program stays open.
       b. If the Quit Program is closed, the event loop exits.
       c. If the image_before_after() window is closed by the user, the 
          program prints a message to the pybox Process/Debug window.
          --> The program is still running. 

    6. When the program is done, an Exit Button is displayed
       a. If the image_before_after() window is still open, it can still be
          used until the button is pressed.

"""

import pybox
from pybox import conio
import sobel
import numpy as np
import cv2

cvimage = cv2.imread("dog.jpg")     # load image with opencv

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
# This example uses an after_title and label to personalize the window.
#
# img_before_after_r() is called to reverse the image, as Open CV returns a 'right-side-up'
# bitmap and pybox defaults to the standard 'upside-down' format. 
#
# Also save the return image object so we can use it to look for events and status

image = pybox.img_before_after_r(cvimage,img_result,after_title="Sobel Image",label="Sobel Before & After Image")

pybox.dev_set_bgcolor("palebluedark")               # Set a different color for the dev window, so it doesn't
                                                    # blend too much with the gray background of the image view window

pybox.dev_text("Dev Window Controls",font=18)     # Print a top message, well, just so it is less plain looking since we 
                                                    # only have two buttons. 
close_button = pybox.dev_button("Close Window")     # Create a close window button
quit_button = pybox.dev_button("-Quit Program")     # Create a Quit Program button
                                                    # the '-' tells the Dev Window to place the button on the same line as the previous

# Wait for some events to occur.
#
# The program is asleep until something happens
# get_event() will return false when all primary windows are closed
# (in this case, the Image View window and Dev Window are both primary windows)

while pybox.get_event() :

    # If the close button was pressed close the Image View window, but keep the program going.

    if close_button.pressed() : image.close_window()

    # If the quit button was pressed, break out of the loop but don't close the image.
    # The image will be closed when the program ends or the user closes it beforehand.

    if quit_button.pressed() : break

    # Check for a close event. This only happens on time so we only react to it once.
    # as an event, it resets itself after we check it.
    #
    # We can also use image.closed() as a permanent status (i.e. always returns True of opem
    # or False if closed)
    #
    # {g} = green, {i} = italic, {c} = cyan  (these can be spelled out, too, i.e. {green},{italic}, etc.

    if image.close_event() : 
        pybox.debug_write("{g}image was closed\n")
        pybox.debug_write("Program is still running.\n--> {i}{c}Press 'Quit Program' to exit.\n")

# Continue with program execution

# << more program elements here while the image window is or isn't open >>

# Put up an exit button as a nice way to say the program has ended.
# this prevents the program from ending and closing all windows abruptly.
#
# For this example, it shows how to can keep the window open as we continue program execution.
# When the "quit" button is pressed, the image is still visible and can be used until
# the "Ok" button is pressed in the new window created by exit_button()

pybox.exit_button()


