"""
Mandelbrot Example (Simple Mandelbrot - Example 1).   Programming with Pybox Demonstration Program.

-------------------------
3D Mandelbrot (Example 3)
-------------------------
 
Mandelbrot's are a little esoteric in their workings, but implementing them is pretty easy.

At their core, it's as simple as the imaginary function z = z^2 + c, which you can see in the main code below. 


---------------------------------------------------------------------------------------------
This Example (3D - Pixel-by-Pixel, For-Loop Version)
---------------------------------------------------------------------------------------------

This Mandelbrot calculates 3D edges by calculating the derivative of the Mandelbrot as the Mandelbrot itself is calculated.
This tells us what angle to use for the luminance. 

---------------------------------------------------------------
Secondary Example (Simple 3D Faster -- Bulk operations)
---------------------------------------------------------------

The other .py file in this project (mandelbrot_faster.py) is the same program as this one, but using bulk array operations.

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

win_size = np.array([1400,900])     # Initial Window Size

# Create a window of size win_size (the default is 1200x800), and a gradient background color

win = pybox.new_window(size=win_size,bg_color="black,midblue");  # Look at issues for C#, adding size, etc.

# Construct a basic "operating" window, since it can take a few seconds to complete.
# {75} sets the font to 75 points -- any {<number>} in text sets the font to that size, e.g. the {20} and {35} values below
# {y} sets the foreground/text color to yellow -- yellow can also be spelled out
# {w} sets the foreground color to white -- "white" can also be spelled out
# just="center" - this centers the text in the window
# pad_y = -70 -- this moves the text up by 70 pixels, just for aesthetic placement.

win.write("{75}Python 3D Mandelbrot\n{y}{20}Pixel-by-Pixel, for-loop version.\n{w}{35}Working...",
                                                                            just="center",pad_y = -70)

# Normally, the window does not update until a function such as get_event(), exit_button() (shown below) or any other
# input-type function is used, unless we set the auto update type to various types (see documentaton for "set_auto_update")

# In this case, since the result can take a while, we set it to "timer", which means the image will update as it is being drawn
# every 20+ milliseconds or so.  This does not typically interefer with timing, and saves us from having to worry about when to update
# as the image is drawing. 
#
# note: This also has the effect is immediately updating the window with the write() function we used in the previous line.
#       pybox.set_win_timer_update_ms() can be used to set the ms to a higher rate, e.g. pybox.set_win_timer_update_ms(100) 

win.set_auto_update("timer")
start = timer();    # Measure the time from here

center      = np.array([-.6,0])  # Center of Mandelbrot
l_range     = 3.7                # Range of man elbrot in x/y direction       
max_iter    = 50                 # maximum iterations before bailing out (and drawing black for this point)

fD          = [ l_range, -l_range]/win_size[0]      # Get Normalize Range                    
fStart      = center  - fD*win_size/2               # upper-left edge (center is in the middle of our range)             
   
for i in range(win_size[1]) :
    y =  i*fD[1] + fStart[1]
    for j in range(win_size[0]) :
        x = j*fD[0] + fStart[0];
        iter = 0;
         
        c = complex(x,-y)       # Making 'y' negative simple flips the Mandelbrot updside down, to put the white area on top vs. bottom
        dz = complex(0,1)       # derivative for tangent angle calculation
        
        z = c
        dz *= z+z     
    
        while abs(z) < 256 and iter < max_iter :
            dz *= z+z
            z = z*z + c
            iter += 1
        
        # if we are at max_iter, then set 0.  Otherwise calculate the luminance base on the derivative
        
        if iter == max_iter : color = 0
        else :
            vec = z/dz
            vec /= abs(vec) 
            color = 90*(vec.real + vec.imag) + 128
            
        win.draw.set_pixel(j,i,(color,color,color))   
           
end = timer();

win.set_write_indent(20)            # Sets the left-hand X alignment for multiple writes, so it stays a X=20 for the two
                                    # write functions below          

# put out timing informaton

win.write("{c}{50}Python 3D Mandelbrot\n{20}{w}(pixel-by-pixel, for-loop version)\n",pos=(20,20))
win.write(f"{{25}}Mandelbrot Calculation and Display Time\n{{65}}{{g}}{format((int) (1000*(end-start)))} ms\n")

pybox.exit_button() # Signal the user the program is over (otherwise the window would close autoamtically when finished)
