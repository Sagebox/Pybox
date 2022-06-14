
# DoublePendulum Class using Pybox
#
# Most of this code was copied and adapted from various internet sources.
#
# ------------------------
# Pybox Graphics Functions
# ------------------------
#
# Pybox graphics functions comprise 5-6 lines of code to draw the rods, bobs, and pendulum trail.
#
# Otherwise, the DoublePendulum class simply calculates and maintains the pendulum.
#
# See the Render Function for Pybox code.
#
# ---------------------
# Floating-Point Errors
# ---------------------
#
# With a high mass ratio (i.e. the bottom bob is much heavier than the top bob) and/or low dampening settings (i.e. close to 1.0 -- very little friction), math errors can occur
# where the pendulum speeds up out of control.  This is due to a low sampling rate and some math than needs to be added to modulate the energy being generated in the pendulum when 
# it exceeds is bounds.
#
# These errors can also happen when the top bob is very close to the peg and the second bob is closed to the first one.
# 
# One answer may be to decrease the dt time-slice and call Update() 5-6 times in a row for a better resolution.  
#
# In the meantime, I added some code to compare the Max Potential Energy with the current Kinetic Energy.  If the Ke > Pe then the algorithm starts applying dampening.
# I think the real solution is to determine when the math has caused the pendulum to have more Pe than it should have at any given state. 
#
# But, I just copied this code for a Pybox/Sagebox demo and haven't work with it much, though it is compelling!
#

import pybox
import numpy as np

weight_mul      = .05                       # Basically an observational value, as is line_mul
line_mul        = 4.0
fps             = 60
dt              = 400.0*(1.0/fps)           # 400 is kinda/sorts an observational value.  
gravity         = 9.8
damp            = .998                      # dampening (i.e. friction).  
overflow_mul    = 1.0                       # Overflow correction value dynamically calculated when errors occur
zoom            = 1.0                       # Display zoom
show_trail      = True                      # Show trails yes/no
line_thickness  = 3.0                       # Base Thickness of rod lines
thick_mul       = 1.0                       # Value set by caller when Thickness is set dynamically 
bob_radius      = 23.0                      # Base Bob 
circle_mult     = 1.0                       # Value set by caller to dynamically change Bob size
peg_radius      = 5.0
overflow_count  = 0                         # Number of overflow errors counted. > 2 starts changing overflow_mul
max_trail_size  = 300                       # Number of points in trail.  More point will cost more time, but not too much.
trail_size      = 0                         # Current size of trail (grows from 0 to max_trail_size)
trail_thickness = 4                         # Thickness of trail lines
single_pend     = False                     # When true, only a single pendulum is displayed and the mass of the second bob is set to 0.
win             = 0                         # Init reassigns to pybox Window Type 

# All of the points used to calculate and maintain each pendulum bob

length          = np.array([220 ,185 ],dtype=float)
mass            = np.array([10,10],dtype=float)
angle           = np.array([-15.0*np.pi/180.0,-15.0*np.pi/180.0 ],dtype=float)
angle_vel       = np.array([0 ,0 ],dtype=float)
angle_acc       = np.array([0 ,0 ],dtype=float)
pos1            = np.array([0 ,0 ],dtype=float)
pos2            = np.array([0 ,0 ],dtype=float)
rod             = np.array([[0,0],[0,0],[0,0]],dtype=float)

trails          = np.zeros(shape=(max_trail_size,2),dtype=float)  
trail_colors    = np.zeros(shape=(max_trail_size,3),dtype=float)


# Initialize the pendulum with pybox Window, length, angles, dampening, etc. 
#
# The pybox window is set to win (above) which is reassigned from an Integer into a pybox Window Type 
#
def init(in_win,length1,length2,mass1,mass2,angle1,angle2,in_damp,pegy=.33) : 
    global win,angle,damp,CenterOffset,length,rod,mass

    win             = in_win                                                            # assign pybox Window
    damp            = in_damp
    mass            = np.array([ float(mass1),float(mass2) ])
    length          = np.array([ float(length1),float(length2) ])
    angle           = np.array([ angle1*np.pi/180, angle2*np.pi/180])
    rod[0]          = win.size()/2 * [1, pegy*2 ]                                      # Set Peg center as middle of Screen X and CenterOffset Y
    for i in range(0,max_trail_size) : trail_colors[i] = [ 255*i/max_trail_size,50*i/max_trail_size,0] # assign trail colors from faded (black) to full brightness

# Reset overflow values
#
def reset_overflow() :
    global overflow_count,overflow_mul
    overflow_count = 0
    overflow_mul = 1.0       # Reset to 1 for no dampening

# Reset all moving values
#
def reset()  :
    global angle_vel,angle_acc,trail_size
    angle_vel[0] = 0
    angle_vel[1] = 0
    angle_acc[0] = 0
    angle_acc[1] = 0
    reset_overflow()
    update_pos()

    trail_size = 0   # Restart the trail

# Update rod position 
#
def update_pos() :
    global pos1,pos2
    pos1 = np.array([ np.sin(angle[0]), np.cos(angle[0]) ]) * length[0]
    pos2 = pos1+np.array([ np.sin(angle[1]), np.cos(angle[1]) ]) * length[1]

# Create the pendulum in the window
#
def render() :
    global rod,pos1,pos2,trail_size,trails,trail_colors

    rod[1] = pos1*zoom + rod[0]
    rod[2] = pos2*zoom + rod[0]

    # Show trails

    if trail_size < max_trail_size : trail_size += 1
    else : trails      = np.roll(trails,-2)
        
    trails[trail_size-1]     = pos2      # assign newest trail position to end of trails

    # Show all trails with one call 

    if show_trail and not single_pend : win.draw.line_segments(trails*zoom+rod[0],trail_colors,trail_thickness,trail_size)

    # Draw the rod lines

    win.draw.line_l(rod[0],rod[1],"White",line_thickness*thick_mul*zoom)
    if not single_pend : win.draw.line_l(rod[1],rod[2],"Cyan",line_thickness*thick_mul*zoom)

    # Draw the peg and Pendulum bobs

    win.draw.fill_circle_l(rod[0],thick_mul*peg_radius*zoom,"White")
    win.draw.fill_circle_l(rod[1],bob_radius*zoom*circle_mult,"Red","White",2.5)
    if not single_pend : win.draw.fill_circle_l(rod[2],bob_radius*zoom*circle_mult,"Green","White",2.5)

# Update the pendulum position
#
# This routine looks for errors and tries to correct them, as the small sampling rate
# can cause too much angular velocity when there is little or no dampening and a big weight difference
# between pendulum bobs. 
#
# A fix might be to call Update() 5-10 times in a row with smaller time segment (dt)
#
def update() :
    global angle,angle_vel,angle_acc,overflow_count,overflow_mul,length

    rod_length = length/(weight_mul*line_mul)
    bob_mass   = mass/10.0                       # Making the mass smaller helps the floating-point precision out

    # Basically code I copied from multiple Internet sources (exept the Pe and Ke calculations below)

    if single_pend : bob_mass[1] = 0
    ldt = dt*dt*weight_mul

    n11 = -gravity*(2.0*bob_mass[0]+bob_mass[1])*np.sin(angle[0])
    n12 = -bob_mass[1]*gravity*np.sin(angle[0]-2.0*angle[1])
    n13 = -2.0*np.sin(angle[0]-angle[1]) * bob_mass[1]
    n14 = (angle_vel[1]*angle_vel[1]*rod_length[1] + angle_vel[0]*angle_vel[0]*rod_length[0]*np.cos(angle[0]-angle[1]))
    den = 2.0*bob_mass[0]+bob_mass[1]-bob_mass[1]*np.cos(2.0*angle[0]-2.0*angle[1])
    n21 = 2.0*np.sin(angle[0]-angle[1])
    n22 = angle_vel[0]*angle_vel[0]*rod_length[0]*(bob_mass[0]+bob_mass[1])
    n23 = gravity*(bob_mass[0]+bob_mass[1])*np.cos(angle[0])
    n24 = angle_vel[1]*angle_vel[1]*rod_length[1]*bob_mass[1]*np.cos(angle[0]-angle[1])
     
    angle_acc[0] = (n11+n12+n13*n14)/(rod_length[0]*den*ldt)
    angle_acc[1] = (n21*(n22+n23+n24))/(rod_length[1]*den*ldt)

    angle_vel += angle_acc
    angle += angle_vel 
    
    if angle[0] > np.pi*2   : angle[0] -= np.pi*2
    if angle[0] < -np.pi*2  : angle[0] += np.pi*2
    if angle[1] > np.pi*2   : angle[1] -= np.pi*2
    if angle[1] < -np.pi*2  : angle[1] += np.pi*2
 
    update_pos()

    angle_vel *= damp*overflow_mul      

    # Check Max Potential Energy vs. Kinetic energy.  Look for overflows when Ke > Pe
    # 
    # Overflows occur because of inaccurate calculations due to time-slice resolution which can 
    # cause the pendulum to move too fast when there is little or no dampening. 
    # This routine works for a 60fps reference with 1 sample per-frame, which is a pretty big dt. 
    # The proper method is to probably call Update() 5-10 times in succession and then render it, rather than
    # just the one time.
     
    v1 = angle_vel[0] #/ldt
    v2 = angle_vel[1] #/ldt

    Pe2 = -(bob_mass[0]+bob_mass[1])*gravity*length[0]-bob_mass[1]*gravity*length[1] 
    Ke2 = .5*bob_mass[0]*v1*v1*length[0]*length[0] + .5*bob_mass[1]*(v1*v1*length[0]*length[0] + 
                            v2*v2*length[1]*length[1] + 2*v1*length[0]*v2*length[1]*np.cos(angle[0]-angle[1])) 

    # If the Kinetic energy went over the max potential energy then slow the pendulum down.
    # If we have seen more than two overflows in this session than add some dampening to 
    # keep slowing it down. 

    if np.fabs(Ke2) > np.fabs(Pe2) :
        ratio = np.fabs(Pe2/Ke2) 
        overflow_count += 1
        angle_vel[0] *= ratio*.65 
        angle_vel[1] *= ratio*.65 

        # Start slowing it down if we've seen more than 2 hits.

        if overflow_count > 2 :
            overflow_mul *= overflow_mul 
            if overflow_mul == 1 : overflow_mul = .9999  # Set static value on first error

if __name__ == "__main__" :
    print("Error: This is a Double Pendulum module and is not meant to be run as a main program.")
    quit()
