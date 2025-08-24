"""
------------------------------------------------------------------------
Pybox MatplotLib Controls Example -- Showing using MatplotLib with Pybox
------------------------------------------------------------------------

Also See: matplotlib_2d.py for a 3D-plot example that uses more controls of the Dev Window

This example shows using Dev Window controls with pybox.  In addition to the sliders and buttons used with the 
matplotlib_2d.py code, this example adds checkboxes and a combobox.

Each control typically uses two lines:  one line to declare the control, and another to use it. 

For example,

    my_button   = pybox.dev_button("Press Me"); 
    if my_button.pressed() : << do something >>

This example uses the Dev Window as a standalone window.  Dev Windows and regular windows can be used separately or together, or in the form 
of the quick_control() which combine the two into two windows embedded in a larger singular window. 


----------------------------------
Adding Checkboxes and the Combobox
----------------------------------

In matplotlib_2d.py, slider and buttons were used in the Dev Window. 

In this version, checkboxes and a combobox are used.

Checkboxes are like buttons but also have a checked or not-checked status.  Checkboxes default as unchecked, and can be 
set when created or after. 

As with the buttons, the checkboxes return a "pressed()" event status, but also contained a "checked()" function to determine whether they
are checked.  In many cases the checked() function does not need to be called, because the pressed() returning True means the value is now just the
opposite of what is was before (so the function can just invert the setting without calling checked()). 

This example also shows the combobox where 3 function names are added, and 3 functions are put into a tuple, where 
the return of (0-2) from the checkbox can index diretly into the array.

The return from the checkbox is guaranteed to be 0-2.

--------------
The Dev Window
--------------

Controls can be placed in regular windows.  

In this example, the Dev Window is used, which is a very easy way to place controls since they are placed automatically and the Dev Window does not
appear until a control is added. 

------------
This Example
------------

This example sets up some pybox Dev Window controls so the graph may be changed dynamically and in real-time as it is being animated.

The graph can be resized, rotated, and changed to a new function.  The background can be changed, and the animation started or stopped. 

The panel resolution can be changed to allow for faster animation -- the highest setting may slow the program down.  

--> Animation

    An animation function is used in Matplot lib.  Rather than an event-loop using pybox, pybox is used inside 
    of the Matplotlib loop, where the values of the sliders, combobox, checkboxes, etc. are checked. 

    If the Quit button is pressed, quit() is called, as I really have no idea how to tell the MatplotLib to exit
    the plt() call when it is animating.

    note: Animation may be faster if "Show Axes" is unchecked.  Also lowering the panel resolution helps.

 --> Zoom Slider

    You can zoom into a MatplotLib graph with the right mouse button.  However, this does not work when animating and changing the
    graph.  The Zoom Slider can be used to zoom in and out when animating. 

--> The MatplotLib code for this example

    The Matplot Lib part of the code for this example was copied nearly verbatim from an example on the Internet.
    Some hard-coded values were changed to slider values.

--> There are many types and different uses for the Dev Control Window controls. 
    This example shows a relatively small use of pybox, but also shows using a number of controls, mostly sliders with a quit and reset button.

    This Example does the following:
    
        1. Sets up the Dev Window and initial top label. 
           Neither are required, but provide nice additives.
        2. Sets up the combobox, sliders, and buttons in the Dev Window
           a. All sliders are floating-point sliders
              --> The default for floating points sliders is 0, with a default
                  range of 0-1.  The 'range' and 'default' keywords are used to change some of the 
                  defaults, but are not required.
           b. The combobox items are set inline, but can also be set later, after the declaration.
           c. The eheckboxes used some embedded features to control the outlay of the checkboxes.
              see comments where they are created.
        3. A matplot lib figure is established for a 3D-Graph
        4. Three functions are put into a list so we can select them later in the combobox
        5. The animation loop is then entered where the program does the following:
            a. Gets the values from the pybox controls
            b. Reponds to any changes, such as the quit button being pressed.
            c. displays the current 3D-Graph through Matplot Lib.
"""

import pybox

import numpy as np

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import matplotlib.animation as anim

import matplotlib.pyplot as plt
import numpy as np

pybox.dev_set_bgcolor("palebluedark")

# Set a text widget on the top for a nice label to our controls.
# The font is set to 18 (default is around 12) with a textcolor of "lightyellow"
# textcolor can also be used as "text_color"

pybox.dev_text("Matplot Lib Controls",font=18, textcolor="lightyellow")

# Create a combobox with three items for the functions.
# The items are specified as "item 1\nitem2\nitem 3", etc.
# Items are not necessary here -- items can be added later with combobox.add_item(), which can
# take a single element or multiple elements as shown below.
#
# "title=" sets the title to the right (or on top).  When not defined, no title appears.

combobox_func       = pybox.dev_combobox("sin(z)\nexp(-z^2)\n(1-z^2)^2*.01\n", title="Select Function")

# Create a number of sliders.  All sliders below are floating-point sliders.
# Default/Typical sliders that return integer position values are created with dev_slider() vs. dev_slider_f()

slider_scale_xy     = pybox.dev_slider_f("x-y axis scale"       ,range=(.05,20), default = 1)
slider_amp          = pybox.dev_slider_f("Amplitude"            ,range=(-10,10), default = 1)
slider_res          = pybox.dev_slider_f("Panel Resolution"     ,range=(10,.1) , default = 1)
slider_rotate_y     = pybox.dev_slider_f("Rotate on Y axis"     ,range=(0,6.24))
slider_offset_z     = pybox.dev_slider_f("Z offset"             ,range=(-20,20))
slider_zoom         = pybox.dev_slider_f("Zoom"                 ,range=(.1,10),default=1)  

# Create some checkboxes.
#
# Note the embedded controls such as '+', '-', and {x=<position} below. 
# These are not necessary but help make the display more formatted and intentional.

checkbox_color      = pybox.dev_checkbox("Solid Color")
checkbox_alias      = pybox.dev_checkbox("-Anti-Alias",xoffset=120)     # The '-' keeps it on the same line/Y position as the last checkbox
                                                                        # Set checkbox at 120 pixels in.  It is otherwise auto-placed,
                                                                        # and the xoffset=120 lets it align with the one below it

checkbox_axes       = pybox.dev_checkbox("-Show Axes",default=True)     # default as checked (also the '+' keeps it on the same line)
checkbox_dark       = pybox.dev_checkbox("+Dark Theme")                 # '+' moves it to the next line, but only a little so it stays as part of a
                                                                        # natural group.  Otheriwse more vertical space is added to separate groupings.

checkbox_anim       = pybox.dev_checkbox("-{x=120}Animate")             # {x=120} is another way of saying set it at 120 pixels, as in the keyword "xoffset=120"

fig         = plt.figure(figsize=(12,8),dpi=80)
ax          = fig.gca(projection='3d')
solid       = False
anti_alias  = False
ang_rotate  = 0
add_rotate  = .05

# Quick functions we can select with the combobox

def func1(R) : return np.sin(R)*5
def func2(R) : return 5.0*np.exp(-R*R*.25)*1.5
def func3(R) : return .75*(1-R*R)*(1-R*R)*.01-7

funclist = [func1,func2,func3]

def set_theme(dark) :
    colorface = (0,0,0) if dark else (1,1,1)
    colortext = (1,1,1) if dark else (0,0,0)

    ax.set_facecolor(colorface)

    ax.tick_params(axis='x', colors=colortext)
    ax.tick_params(axis='y', colors=colortext)
    ax.tick_params(axis='z', colors=colortext)
    ax.w_xaxis.set_pane_color(colorface)
    ax.w_yaxis.set_pane_color(colorface)
    ax.w_zaxis.set_pane_color(colorface)
    fig.patch.set_facecolor(colorface)


def update(i) :
    global solid,anti_alias,animate,ang_rotate
    up_graph = pybox.event_pending() or animate

    # Get current values from the sliders we set up.
    # Since they are all float-based sliders, get_pos_f() is used,
    # where regular get_pos() would return the rounded integer value.

    scale_xy    = slider_scale_xy.get_pos_f()
    amplitude   = slider_amp.get_pos_f()
    resolution  = slider_res.get_pos_f()
    rotate_y    = slider_rotate_y.get_pos_f()
    zoom        = 1.0/slider_zoom.get_pos_f()
    offset_z    = slider_offset_z.get_pos_f()

    if pybox.dev_closed(True) : quit()          # True adds a close button.

    scale_xy    = np.sqrt(scale_xy)
    
    # Get boolean checkbox items

    solid       = checkbox_color.checked()
    anti_alias  = checkbox_alias.checked()

    show_axes   = 'on' if checkbox_axes.checked() else 'off'
    animate     = checkbox_anim.checked()

    # Update graph via MatplotLib
    #
    # The graph is only updated as needed: when slider was moved or button pressed,
    # or if we're animating.
    #
    # The code below was copied pretty much as-is from internet sources, except for
    # the addition of a function list (func_list) 

    if up_graph: 
        ax.clear()
        ax.title.set_text('Matplot 3D-Graph with Controls')
        X = np.arange(-5*scale_xy, 5*scale_xy, 0.25*resolution*scale_xy)
        Y = np.arange(-5*scale_xy, 5*scale_xy, 0.25*resolution*scale_xy)
        xlen = len(X)
        ylen = len(Y)

        X, Y = np.meshgrid(X, Y)

        if animate :
            X2 = X * np.cos(ang_rotate) - Y*np.sin(ang_rotate)
            Y = X * np.sin(ang_rotate) + Y*np.cos(ang_rotate)
            X = X2
            ang_rotate += add_rotate

        R = np.sqrt(X**2 + Y**2)
        
        Z = funclist[combobox_func.get_selection()](R)

        Z *= amplitude 
        Z += offset_z
        
        X2 = Z *np.sin(rotate_y) + X*np.cos(rotate_y); 
        Z = Z *np.cos(rotate_y) - X*np.sin(rotate_y); 
        X = X2; 
        color2 = 'r' if solid else 'w'
        colortuple = ('r', color2)
        colors = np.empty(X.shape, dtype=str)
        
        for y in range(ylen):
            for x in range(xlen):
                colors[x, y] = colortuple[(x + y) % len(colortuple)]

        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, facecolors=colors,
                linewidth=0, antialiased=anti_alias)

        ax.set_zlim3d(-5*zoom, 5*zoom)
        ax.set_xlim3d(-5*scale_xy*zoom, 5*scale_xy*zoom)
        ax.set_ylim3d(-5*scale_xy*zoom, 5*scale_xy*zoom)
        ax.w_zaxis.set_major_locator(LinearLocator(6))

        if checkbox_dark.pressed() :
            set_theme(checkbox_dark.checked())

        plt.axis(show_axes)

# ----------------------------------
# Main Program Start (i.e. __main__)
# ----------------------------------

a = anim.FuncAnimation(fig, update, frames=1000, interval = 16,repeat=True)

plt.show()

# Add an exit button, though we don't really get here.
# I don't know how to exit the animation loop and just call quit()
# when the close button is prssed. So we never get here
# (until someone tells me how to exit the animation loop)

pybox.exit_button()
