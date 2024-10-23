
"""
------------------------------------------------------------------------
Pybox MatplotLib Controls Example -- Showing using MatplotLib with Pybox
------------------------------------------------------------------------

Also See: matplotlib_3d.py for a 3D-plot example that uses more controls of the Dev Window

This example shows using simple Dev Window controls with pybox. 

Each control typically uses two lines:  one line to declare the control, and another to use it. 

For example,

    my_button   = pybox.dev_button("Press Me"); 
    if my_button.pressed() : << do something >>

This example uses the Dev Window as a standalone window.  Dev Windows and regular windows can be used separately or together, or in the form 
of the quick_control() which combine the two into two windows embedded in a larger singular window. 

--------------
The Dev Window
--------------

Controls can be placed in regular windows.  

In this example, the Dev Window is used, which is a very easy way to place controls since they are placed automatically and the Dev Window does not
appear until a control is added. 

------------
This Example
------------

There are many types and different uses for the Dev Control Window controls. 
This example shows a relatively small use of pybox, but also shows using a number of controls, mostly sliders with a quit and reset button.

This Example does the following:

    1. Sets up a MatplotLib plot figure for two simultaneous sin() and cos() graphs

    2. Sets the background color of the Dev Window
        a. The default color is dark gray, and this sets it to a gradient to make it look nice.
        b. There can exist any number of Dev Window.   The pybox Dev functions, such as 
           pybox.DevButton() uses the default window. pybox.NewDevWindow() will create more Dev Windows

    3. Sets up two blank text widgets in the Dev Window that will later 
       be used to show data from the current plot.

    4. Creates 5 sliders for various aspects such as phase, frequency, etc.
       for each of the two graphs. 
       a. All sliders but the last slider are floating-point sliders
          --> The default for floating points sliders is 0, with a default
              range of 0-1. 

              The 'range' and 'default' keywords are used to change some of the defaults, but 
              are not required.

        b. The last slider is a regular slider with a default range of 0-100 and a default of 0
           In this case, the range is not change, and the default is set to 10.
    5. The program then enters a loop waiting for events.

        a. If the program is animating, it does not wait for an event.
        b. When not animating, the program is put to sleep until an event occurs, such 
           as a slider movement or button press.

    6. When either occurs (i.e. an event or a passthrough due to an animation setting), the
       follow occurs:
   
       a. The values phase and frequency values are read from the pybox sliders.
       b. The graph is updated via MatplotLib
       c. The widgets created earlier are written out to to show the data for each graph.
       d. If the Reset button has been pressed, the values are reset.
       e. If the Quick button was pressed, the loop is exited and the program ends.

"""

import matplotlib.pyplot as plt
import matplotlib.animation as anim
import pybox
import numpy as np

x = np.linspace(0, 6*np.pi, 400)
y = np.sin(x)


plt.ion()       # tell Matplotlib we don't want an interactive window.  
                # We could use an animation for the interactive window while
                # we use the Dev Window Controls -- see the Matplotlib 3D example.

fig     = plt.figure()
ax      = fig.add_subplot(211)
ax2     = fig.add_subplot(212)

line1, = ax.plot(x, np.sin(x), 'r-',linewidth=3)                # one graph red, the other blue.
line2, = ax2.plot(x, np.cos(x), 'b-',linewidth=3)

pybox.dev_set_bgcolor("forestgreen,blue")           # Set a gradient color for the Dev Window
                                                    # Not necessary, but just to personalize it a little from 
                                                    # the default gray-to-dark gray gradient.

pybox.dev_text("Matplot Lib Controls",font=20)      # Set a title above the graph in the MatplotLib window
                                                    # Note that this is a fire-and-forget usage of a text widget
                                                    # since we didn't save the object.  The object is only needed 
                                                    # if the text widget will be written to again.

# Get a couple of text widgets so we can put out some info later. 

text_sin = pybox.dev_text(font=14)
text_cos = pybox.dev_text(font=14)

# Get some sliders.  Most of that are floating point sliders (dev_slider_f)

slider_sin_phase = pybox.dev_slider_f("Sin Phase"       , range = (0,3.14*10))              # default is 0, so we don't need to set it.
slider_cos_phase = pybox.dev_slider_f("Cos Phase"       , range = (0,3.14*10))
slider_sin_freq  = pybox.dev_slider_f("Sin Frequency"   , range = (.15,5), default=1)
slider_cos_freq  = pybox.dev_slider_f("Cos Frequency"   , range = (.15,5),default=1)
slider_animate   = pybox.dev_slider("Animation Speed"   , default= 10 )

# Get a couple buttons.  Spaces are added for padding so the buttons aren't too small in width
# the '-' causes the button to stay on the same horizontal line as the previous button.
# Otherwise, the button is placed below the last button to the left.

button_quit      = pybox.dev_button("    Quit    ") 
button_reset     = pybox.dev_button("-  Reset  ")

# Reset everything.  Called in response to the reset button being pressed
# Normally we would have values rather than the canned 0's and 1's, but its
# just a little demo

def reset() :
    slider_sin_phase.set_pos_f(0)
    slider_cos_phase.set_pos_f(0)
    slider_sin_freq.set_pos_f(1) 
    slider_cos_freq.set_pos_f(1) 
    slider_animate.set_pos(0)       # Set animation to stop, even though we defaulted to 10

# Create a fire-and-forget text widget (i.e. we don't save the widget object) for a nice label on time.

ax.title.set_text('Matplot Lib & Pybox Sin and Cos Function Example')

# animation values to adjust phase and add to it for scrolling animation

anim_phase     = 0      
anim_phase_add = 0

# main loop.
#
# This just loops forever.  The program is shut down until an event occures
# (such as a slider movement or button press), or if we're animating. 
# get_event() returns false when the dev window is closed.

while anim_phase_add > 0 or pybox.get_event() :

    if button_reset.pressed() :     # if the reset button is pressed, reset the controls
        reset()

    if button_quit.pressed() :      # if the quit button is pressed, then break out of the loop
        break;                      # so we can put up an exit button.

    # get values from sliders.  
    #
    # each slider can be queried to see if it changed, and a global
    # function called pybox.event_pending() can be called to see if its
    # worth checking events -- usually used for real-time (see the double pendulum example)
    #
    # But, since this is low-duty here, it's just easy to grab them each loop. 
    # (with event pending, the following would be in a "if pybox.event_pending() :" block
    #
    # A call back could be set, but its easier here so we don't change values in the middle of processing,

    anim_phase_add  = slider_animate.get_pos()/50
    sin_phase       = slider_sin_phase.get_pos_f() 
    cos_phase       = slider_cos_phase.get_pos_f() 
    sin_freq        = slider_sin_freq.get_pos_f()
    cos_freq        = slider_cos_freq.get_pos_f()

    # Set up a couple graphics, a cos and sin representing real-time data

    line1.set_ydata(np.sin(x*sin_freq + sin_phase + anim_phase))
    line2.set_ydata(np.cos(x*cos_freq + cos_phase + anim_phase))
    fig.canvas.draw()
    fig.canvas.flush_events()
    anim_phase += anim_phase_add
    
    # Write out the graph value information to the Dev Window text Widgets
    # {g} = green, {c} = cyan, {x=<number>} sets the X position at that value for lining up things.
    #
    # in formatted strings, {{g}}, {{c}}, etc. would be used, hence the "+" values so we can 
    # just use the single "{ and "}"

    text_sin.write("{g}Sin Phase{}{x=80}" + "{0:4f}".format(sin_phase) + 
                      "{g}{x=155}Sin Freq.{}{x=240}" + "{0:4f}".format(sin_freq))

    text_cos.write("{c}Cos Phase{}{x=80}" + "{0:4f}".format(cos_phase) + 
                      "{c}{x=155}Cos Freq.{}{x=240}" + "{0:4f}".format(cos_freq))

# Put up an exit button letting the user know the program has ended.
# These aren't necessary, but since when the program ends and all of the windows go with it,
# sometimes its nice to know the program means to end and gives a chance to review the screen.

pybox.exit_button()

