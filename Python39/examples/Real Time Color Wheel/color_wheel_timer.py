# ------------------------------------------
# Python Real Time Color Wheel Timer Version
# ------------------------------------------
#
# See notes in color_wheel.py for general information on the Color Wheel
#
# This timer version is used as a method to determine the performance of a system using Python with real-time
# graphics and to determine the reliability of the vsync.
#
# --------------
# Timers 1 and 2
# --------------
# 
# Two timers are used. 
# 
# Timer 1 measures the time it takes to draw the image.  Usually this should be in the range of 1-4 milliseconds at most. 
# On older systems this may take longer.  On my fairly-decent laptop, it takes about 2.2 ms
# 
# Timer 2 measures the time waited for the vsync.  This is used specifically to look for hesitations or jitter in the update.
# If Timer 1 is within the vysnc time (usually 16 ms), this number should never be greater than 15 or so ms. 
# 
# If a jitter occurs, this number will absorb the next vsync wait and the number will show as larger than the vsync time.
# (i.e. it will display something like "29", "30"m etc. instead of "12" or "14" or whatever it usually displayed
#
# This shouldn't happan, and as of this writing, no thia has not been seen in testing.
#
# --------------
# color_wheel.py
# --------------
# 
# For the general color wheel program, see color_wheel.py
# It has more notes about using pybox and what the functions used do in the program
# 
# As noted in color_wheel.py, the opts (i.e. pybox.opt vs. 'opts') are reversed in this module to show
# the two different option styles (text vs. symbolic)
# 

import pybox
from pybox import opt
from timeit import default_timer as timer 
import numpy as np

win             = pybox.new_window("Real-Time Python Color Wheel",realtime=True,bgcolor='black')

num_sections    = 20      # number of 
square_size     = 150     # size of each square
radius          = 200     # radius of large circle where squares are placed
spin            = 0.0     # spin factor for both large circle and each square (handled differently)

win.draw.set_opacity(50)

# Note the opt. usage.  Its a little more text, but the intellisense shows you the documentation and 
# will also fill it in for you, so no mistakes are made.  In fact, I accidentally typed "real+time" above 
# before I noted it and changed it where "opt.real_time" would have been filled in an underlined in red if not found.
#
# note: as of this writing pybox has just been released, so not all options in pybox.opt have been documented yet.

win.text_widget(0,5,text="Python Real-Time GDI Graphics Example",centerx=True,font=40)
win.text_widget(0,50,"A More Advanced Example using Rotational and Translate Transformations",
                                                centerx=True,font=16,textcolor="CornflowerBlue")

start2 = timer()         # just to get the timer variable placed. Not used until the end of the loop

while win.vsync_wait() :
    start = timer()      # Get the start time (which is also the end time for the outer loop)

    win.cls()

    for i in range(0,num_sections) :
        angle = i*(np.pi*2)/num_sections+spin
        color = win.draw.get_hue_color(i*360/num_sections)
        fx = radius*np.cos(angle)
        fy = radius*np.sin(angle)
        win.draw.translate_transform(fx+600,fy+420)
        win.draw.rotate_transform((i+spin*3.5)*60)
        win.draw.fill_rectangle(-square_size/2,-square_size/2,square_size,square_size,color)
        win.draw.reset_transform()

    end = timer()       # get the end time for the draw time

    # {p} = purple, {g} = green.  Wrapped in "{{p}}" & "{{g}}" because of the formatted string.
    # {} ends the previous color black ("{{}}"" in formatted strings). {} isn't necessary to
    # close the green segment as it is reset a the end of line (EOL)

    # t1 = time it took to draw.  t2 = time waited for the vsync after we were done drawing.

    pybox.debug_write(f"t1: {{p}}{format(1000*(end-start),'.4f')} ms{{}}, "
                      f"t2: {{g}}{format(1000*(start-start2),'.4f')} ms\n")
     
    win.update()            # send the image we created out to the window
    
    start2 = timer()        # set the timer for the vsync wait time
    spin += .005

