
"""
Mandelbrot Example (Simple Mandelbrot - Example 1).   Programming with Pybox Demonstration Program.

-----------------------------
Simple Mandelbrot (Example 1)
-----------------------------
 
Mandelbrot's are a little esoteric in their workings, but implementing them is pretty easy.

At their core, it's as simple as the imaginary function z = z^2 + c, which you can see in the main code below. 


---------------------------------------------------------------------------------------------
This Example (Simple Mandelbrot - Bulk-Operations Version)
---------------------------------------------------------------------------------------------

This Mandelbrot example is the simplest example, calculating the mandelbrot luminance value, with 16 colors, that simply
wrap around (via a mod function), showing the mandelbrot with visible boundaries for each different luminance value.

-----------------------------
Bulk-Array Operations Version
-----------------------------

This version uses bulk-array operations and is 4-5 times faster than the for-loop version.

It is much more difficult to use bulk-operations, and they don't translate so easily to creative changes and general experimentation.

Though not all types of programs can be converted to using bulk-array operations, those that do are typically much faster than their one-by-one
(i.e. for-loop) counterparts. 

The code below is comment to help identify the changes from the for-loop version and bulk-array code.

-------------------
Mandelbrot Examples
-------------------

There are 3 Mandelbrot Example projects that generate simple mandelbrots. 

These three mandelbrot programs are the same calculation, with the same center and range. 
The only difference is how the colors are place, as well as how the colors are interpreted, in the case of the 3-D mandelbrot.

    -----------------------------------
    1. Simple Mandelbrot - this example
    -----------------------------------
    
    Generates a simple mandelbrot with simple colors. 
    
    --------------------
    2. Smooth Mandelbrot
    --------------------

    Generates a simple mandelbrot with smooth color gradient
    
    -----------------
    3. 3-D Mandelbrot
    -----------------
    
    Generates a mandelbrot with 3-D edges (that is, not a 3-D mandelbrot, per se), by calculating the gradient of the mandelbrot
    in the main loop.

"""

import pybox
import numpy as np
from timeit import default_timer as timer

# Main color table for each of 16 colors, which wrap around however many max_iter values we choose 

colors = np.array([( 0, 0, 0       ), 
                    ( 0, 0, 0       ), (25, 7, 26     ), (9, 1, 47      ), (4, 4, 73      ), 
                    ( 0, 7, 100     ), (12, 44, 138   ), (24, 82, 177   ), (57, 125, 209  ),
                    ( 134, 181, 229 ), (211, 236, 248 ), (241, 233, 191 ), (248, 201, 95  ),
                    ( 255, 170, 0   ), (204, 128, 0   ), (153, 87, 0    ), (106, 52, 3    )])



win_size = np.array([1400,900])     # Initial Wi ndow Size

# Create a window of size win_size (the default is 1200x800), and a gradient background color

win = pybox.new_window(size=win_size,bg_color="black,midblue");  # Look at issues for C#, adding size, etc.

# Construct a basic "operating" window, since it can take a few seconds to complete.
# update_now  -- Tells the window to update immediately.  Since we're going right into calculating, the window
#                won't update until there is an input or status function called.  
#
#                This basically saves having to do a "win.update()" to ensure it gets updated prior to entering the main loop
#
# See "mandelbrot.py" for comments on the write() code line below

win.write("{75}Python Simple Mandelbrot\n{y}{20}Bulk-Array Operations Version.\n{w}{35}Working...",
                                                                            just="center",pad_y = -70,update_now=True)

center      = np.array([-.6,0])  # Center of Mandelbrot
l_range     = 3.7                # Range of man elbrot in x/y direction       
max_iter    = 50                 # maximum iterations before bailing out (and drawing black for this point)

frange     = np.array([ l_range, l_range*win_size[1]/win_size[0]])

nx = win_size[0]
ny = win_size[1]

xrange = frange[0]/2
yrange = frange[1]/2

start = timer();   # start timing from here

# get matrix values for X and Y dimensions (i.e. x,y values if we were to use a for-loop)
x = np.linspace(-xrange+center[0],xrange+center[0], nx)
y = np.linspace(-yrange+center[1],yrange+center[1], ny)

# Get matrices (zeroed-out and otherwise) for the bulk operations that replace 
# variables in a double x,y for-loop (i.e. mandelbrot.py, non-bulk version)

counter     = np.zeros(shape=(ny,nx), dtype='int')      # iteration count for each x,y place - value "iter" in the for-loop version
colors_a    = np.zeros(shape=(ny,nx), dtype='int')      # iteration % 16, essentially, to wrap around in the color
bitmap      = np.zeros(shape=(ny,nx,3), dtype='int')    # output bitmap

# We have to calculate the z = z^2 + c ourselves, so we track the real and imaginary components
z_re = np.zeros(shape=(ny,nx), dtype='float32')         # real Z
z_im = np.zeros(shape=(ny,nx), dtype='float32')         # imaginary Z

z_re_new = np.zeros(shape=(ny,nx), dtype='float32')     # preliminary value for real Z to check inclusion
z_im_new = np.zeros(shape=(ny,nx), dtype='float32')     # preliminary value for imag Z to check inclusion

xv, yv = np.meshgrid(x,y)     

mask = np.ones(shape=(ny,nx), dtype='bool')            # main mask so we can stop adding to counter (set to True Initially)

# in this main loop, we calculate the new value of z*z+c, and if it is less than max_iter, we set the mask
# to set the current z (real and imaginary) values. 
#
# note that the mask is persistent, so the new values are not calculated if the x,y space has been marked as 
# out of bounds.  This ends up increasing the performance of this loop significantly. 

for i in range(max_iter):
    z_re_new[mask] = z_re[mask]**2 - z_im[mask]**2 + xv[mask]   # calculate z*z+c to check if it is out of bounds
    z_im_new[mask] = 2 * z_re[mask] * z_im[mask] + yv[mask]

    mask[mask] &= (z_re[mask]**2 + z_im[mask]**2) < 4           # if we're out of bounds, mark the mask as OOB permanently,
                                                                # so we don't do any more calculations at all

    # for those x,y values that have passed the test and are still in bounds, set the Z value so we can calculate again
    
    z_re[mask] = z_re_new[mask]
    z_im[mask] = z_im_new[mask]
    counter[mask] += 1          # increase the iteration value for those x,y points that are still not out of bounds
    
# all colors are already 0 (i.e. black).  For those that are in bounds, set the color from the color table,
# rolling over (via the mod()/% function).

colors_a[counter < max_iter] = (counter[counter < max_iter] % 16) + 1 

bitmap[:,:] = colors[colors_a]      # Create the output bitmap by translating each color_a value from the color table

 
win.display_bitmap(0,0,bitmap)      # Display the result bitmap

end = timer();                      
win.set_write_indent(20)            # Sets the left-hand X alignment for multiple writes, so it stays a X=20 for the two
                                    # write functions below          

win.write("{c}{50}Python Simple Mandelbrot\n{20}{w}(bulk-array operations version)\n",pos=(20,20))
win.write(f"{{25}}Mandelbrot Calculation and Display Time\n{{65}}{{g}}{format((int) (1000*(end-start)))} ms\n")

pybox.exit_button() # Signal the user the program is over (otherwise the window would close autoamtically when finished)
