
"""
Mandelbrot Example (Smooth Mandelbrot - Example 2).   Programming with Pybox Demonstration Program.

-----------------------------
Smooth Mandelbrot (Example 2)
-----------------------------
 
Mandelbrot's are a little esoteric in their workings, but implementing them is pretty easy.

At their core, it's as simple as the imaginary function z = z^2 + c, which you can see in the main code below. 

---------------------------------------------------------------
This Example - Secondary Example (Smoorth Mandelbrot Faster -- Bulk operations)
---------------------------------------------------------------

This is the same program as the for-loop-based, pixel-by-pixel Smooth Mandelbrot, but using bulk array operations.

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

# Main color table for each of 16 colors, which wrap around however many max_iter values we choose 

colors = np.array([ ( 0, 0, 0       ), 
                    ( 0, 0, 0       ), (25, 7, 26     ), (9, 1, 47      ), (4, 4, 73      ), 
                    ( 0, 7, 100     ), (12, 44, 138   ), (24, 82, 177   ), (57, 125, 209  ),
                    ( 134, 181, 229 ), (211, 236, 248 ), (241, 233, 191 ), (248, 201, 95  ),
                    ( 255, 170, 0   ), (204, 128, 0   ), (153, 87, 0    ), (106, 52, 3    )])


kColorTableSize = 16384                                                 # size of the output, larger, color table
rgbColorTable = np.zeros(shape=(kColorTableSize,3), dtype='int')        # the main, larger, color table itself.

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

win.write("{75}Python Smooth Mandelbrot\n{y}{20}Bulk-Array Operations Version.\n{w}{35}Working...",
                                                                            just="center",pad_y = -70,update_now=True)

center      = np.array([-.6,0])  # Center of Mandelbrot
l_range     = 3.7                # Range of man elbrot in x/y direction       
max_iter    = 50                 # maximum iterations before bailing out (and drawing black for this point)

frange     = np.array([ l_range, l_range*win_size[1]/win_size[0]])

nx = win_size[0]
ny = win_size[1]

xrange = frange[0]/2
yrange = frange[1]/2

def create_color_table() :
    def new_color(c) :
        return int(colors[i][c]*(1-percent) + colors[i+1][c]*percent)

    for i in range(16) :
        for j in range(int(kColorTableSize/16)) :
            percent = 16*j/kColorTableSize
            rgbColorTable[int(kColorTableSize*i/16) + j] = (new_color(0),new_color(1),new_color(2))
            

#
# Create the Color Table
#
# This function takes the colors int the 16-color 'colors' table and extends them 
# to 16384 colors, with a smooth transition between them, with 1024 color values between each color\
 
create_color_table();

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


xv, yv = np.meshgrid(x,y)     

index = np.zeros(shape=(ny,nx), dtype='int')

mask = np.ones(shape=(ny,nx), dtype='bool')            # main mask so we can stop adding to counter (set to True Initially)

# in this main loop, we calculate the new value of z*z+c, and if it is less than max_iter, we set the mask
# to set the current z (real and imaginary) values. 
#
# note that the mask is persistent, so the new values are not calculated if the x,y space has been marked as 
# out of bounds.  This ends up increasing the performance of this loop significantly. 
#
# note: this version is more streamlined than the previous Mandelbrot example. 
# 1. The mask is assigned immediately
# 2. z_im_new no longer exists, since it's not necessary

for i in range(max_iter):
    mask &= (z_re**2 + z_im**2) < 65536 
    z_re_new[mask] = z_re[mask]**2 - z_im[mask]**2 + xv[mask]

    z_im[mask] = 2 * z_re[mask] * z_im[mask] + yv[mask]
    z_re[mask] = z_re_new[mask]
    counter[mask] += 1
    
# all colors are already 0 (i.e. black).  For those that are in bounds, set the color from the color table,
# rolling over (via the mod()/% function).

# set at all max_iter iteration values to 2, as otherwise we'd perform an ln(0), allowing us to
# avoid using the mask for the log() operations below, and can now do it with the entire array instead.
#
# Since we filter out these 'counter == max_iter' values anyway, we don't use the results calculated in the log() functions

z_re[counter == max_iter] = 2 # avoid ln(0)

# Perform the same log() operation as the for-loop version, but with bulk operations

fLog = np.log2(np.log2(z_re**2 + z_im**2)/2)
fIter_x = (counter -fLog + 1.0) / (max_iter-1.0)
index[:,:] = np.sqrt(fIter_x)*(kColorTableSize-1)

# Get colors from the lager (16384-element) table, avoiding counter values that are at the max_iter 
# value -- these values are already set to 0 (black)

bitmap[counter < max_iter] = rgbColorTable[index[counter < max_iter]]    
win.display_bitmap(0,0,bitmap)


end = timer();                      
win.set_write_indent(20)            # Sets the left-hand X alignment for multiple writes, so it stays a X=20 for the two
                                    # write functions below          

win.write("{c}{50}Python Smooth Mandelbrot\n{20}{w}(bulk-array operations version)\n",pos=(20,20))
win.write(f"{{25}}Mandelbrot Calculation and Display Time\n{{65}}{{g}}{format((int) (1000*(end-start)))} ms\n")

pybox.exit_button() # Signal the user the program is over (otherwise the window would close autoamtically when finished)
