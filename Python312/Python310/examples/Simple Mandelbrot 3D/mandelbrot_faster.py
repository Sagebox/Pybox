
"""
Mandelbrot Example (Simple Mandelbrot - Example 1).   Programming with Pybox Demonstration Program.

-------------------------
3D Mandelbrot (Example 3)
-------------------------
 
Mandelbrot's are a little esoteric in their workings, but implementing them is pretty easy.

At their core, it's as simple as the imaginary function z = z^2 + c, which you can see in the main code below. 

---------------------------------------------------------------
This Example (Simple 3D Faster -- Bulk operations)
---------------------------------------------------------------

This program (mandelbrot_faster.py) is the same program as the pixel-by-pixel, for-loop version, but using bulk array operations.

Using bulk array operations can be many times faster than using for-loops for each value, but also make programming more difficult, as well
as experimenging and programming creatively by changing simple things. 

However, once finished, the result is much faster than this version.  See notes in mandelbrot_faster.py for more information

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

win.write("{75}Python 3D Mandelbrot\n{y}{20}Bulk-Array Operations Version.\n{w}{35}Working...",
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
bitmap      = np.zeros(shape=(ny,nx), dtype='int32')    # Output bitmap (monochrome for this version)

# We have to calculate the z = z^2 + c ourselves, so we track the real and imaginary components
z_re = np.zeros(shape=(ny,nx), dtype='float32')         # real Z
z_im = np.zeros(shape=(ny,nx), dtype='float32')         # imaginary Z

dz_re       = np.zeros(shape=(ny,nx), dtype='float32')  # derivative real 
dz_im       = np.zeros(shape=(ny,nx), dtype='float32')  # derviative imaginary value

# temp arrays

z_re_new    = np.zeros(shape=(ny,nx), dtype='float32')
z_im_new    = np.zeros(shape=(ny,nx), dtype='float32')

dz_re_new   = np.zeros(shape=(ny,nx), dtype='float32')
dz_im_new   = np.zeros(shape=(ny,nx), dtype='float32')

xv, yv      = np.meshgrid(x,y)     
div         = np.zeros(shape=(ny,nx), dtype='float32')

mask        = np.ones(shape=(ny,nx), dtype='bool')      # main mask so we can stop adding to counter (set to True initially) 

# Set the initial values, as in the for-loop version, but with some shortcuts:

z_re[:,:] = xv              # z = c
z_im[:,:] = yv

dz_re[:,:] = - z_im*2       # dz = dz*2*z -- which is really just z*2*(0+1i), since dz is initially (0+1i)   
dz_im[:,:] = + z_re*2 

# in this main loop, we calculate the new value of z*z+c, and if it is less than max_iter, we set the mask
# to set the current z (real and imaginary) values. 
#
# In this version, the derivative is also calculated.
#
# note that the mask is persistent, so the new values are not calculated if the x,y space has been marked as 
# out of bounds.  This ends up increasing the performance of this loop significantly. 

for i in range(max_iter):
    mask[mask] &= (z_re[mask]**2 + z_im[mask]**2) < 65536                   # calculate if we've overflowed max_iter and create mask
                                                                            # (i.e. essentially skip any calculations if we're out-of-bounds
                                                                            #  just now or previously)

    dz_re_new[mask] = dz_re[mask]*z_re[mask]*2 - dz_im[mask]*z_im[mask]*2   # derivative (dz *= z+z)
    dz_im[mask] = dz_re[mask]*z_im[mask]*2 + dz_im[mask]*z_re[mask]*2 
    dz_re[mask] = dz_re_new[mask]
    
    z_re_new[mask] = z_re[mask]**2 - z_im[mask]**2 + xv[mask]               # main z*z + c calculation

    z_im[mask] = 2 * z_re[mask] * z_im[mask] + yv[mask]
    z_re[mask] = z_re_new[mask]
    
    counter[mask] += 1

    
# Calculate the code from the pixel-by-pixel version
#    
#            vec = z/dz
#            vec /= abs(vec) 
#            color = 90*(vec.real + vec.imag) + 128

mask[:,:] = counter != max_iter     # kill out-of-bound values we we don't divide by 0

div[mask] = dz_re[mask]**2 + dz_im[mask]**2                                         # divisor for imaginary div function
dz_re_new[mask] = (z_re[mask]*dz_re[mask] + z_im[mask]*dz_im[mask])/div[mask]       # (z/dz)
dz_im_new[mask] = (z_im[mask]*dz_re[mask] - z_re[mask]*dz_im[mask])/div[mask]

div[mask] = np.sqrt(dz_re_new[mask]**2 + dz_im_new[mask]**2)                        # abs(vec)

bitmap[mask] = 90*(dz_re_new[mask] + dz_im_new[mask])/div[mask] + 128

win.display_bitmap_r(0,0,bitmap)

end = timer();                      
win.set_write_indent(20)            # Sets the left-hand X alignment for multiple writes, so it stays a X=20 for the two
                                    # write functions below          

win.write("{c}{50}Python 3D Mandelbrot\n{20}{w}(bulk-array operations version)\n",pos=(20,20))
win.write(f"{{25}}Mandelbrot Calculation and Display Time\n{{65}}{{g}}{format((int) (1000*(end-start)))} ms\n")

pybox.exit_button() # Signal the user the program is over (otherwise the window would close autoamtically when finished)
