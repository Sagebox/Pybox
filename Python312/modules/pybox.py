"""
Commentary

"""

import numpy
import _pybox
from enum import IntEnum
from typing import Callable

class RgbColor :
    "rgbcolor"
    def __init__(self,red,green,blue) : 
        self.red     = int(red)
        self.green   = int(green)
        self.blue    = int(blue)
    def __repr__(self):
        return "pybox.RgbColor"
    def __str__(self):
        return "[{0: >3}{1: >4}{2: >4}]".format(self.red,self.green,self.blue)

class Bitmap :
    "Sagebit Bitmap Class - this is the same as CBitmap in the C++ version of pybox (Sagebox)"
    def __init__(self,id=0) :
        self.__id = id
    def __repr__(self):
        return "pybox.Bitmap"
    def size(self) ->  numpy.ndarray :
        """
        Returns the size of the Bitmap as a list (width,height). Will return (0,0) for invalid bitmaps.
        """
#        return numpy.array(_pybox.BitmapGetSize(self.__id)) 
        return _pybox.BitmapGetSize(self.__id) 
    def get_array(self) -> numpy.ndarray:
        """
        Returns the Bitmap as a Python array compatible with SciPy and other libraries that
        use bitmaps as a Python array.

        The array returned is 24-bit bitmap numpy unsigned char array in the dimensions [height][width][3], where the [3] elements
        are Blue, Green, Red 

        The array is initially returned as an aligned bitmap array, but any operations vis Python will probably convert it to an unaligned
        bitmap.
        """
        return _pybox.BitmapGetMemory(self.__id)

    def is_valid(self) -> bool:
        """
        Returns True if the bitmap exists and has memory data (i.e a width and a height).
        Returns False if the bitmap does not exist or holds no actual bitmap memory.
        """
        if (self.__id <= 0) : return False
        return _pybox.isValid(self.__id)
        
class __typePeekEvent : 
    """
    This type is used as a special type to 'peek' at events.  
    When events are polled they are typically reset so that subsequent polling returns False until
    a new event occurs. 

    Using a 'peek' will look at the event and not reset it so other code can look at the same event.
    """
    def __init(self) :
        self.peek = True

peek = __typePeekEvent()


class conio :
    """
    Console Class

    This class contains functions to output and input to/from the console mode window.

    Functions allow you to write out in color to the console window and to also input qualified 
    input.
    """
    def write(*args) : 
        """
        Write out to the console window.  This is the same as print() except that colors and formatting may be used: 

        - Use {color} to start a color and {} to end the color. Example: pybox.console.Write("This is {red}in the color red{}")
        - You can use the first lett of the color, and do not need the closing {} if its at the end of the line:
            Example: pybox.console.Write("This is {r}in the color red")
        - Multiple colors can be used. Example: pybox.console.Write("This {c}is in cyan{} and this {r}is in the color red")
        - Use "{x=<number>}" to set a column (does not use closing {}):
            Example: pybox.console.Write("This {x=40}is at column 40")
        - Use "{bg=<color>"} to set the background color: Example: pybox.console.Write("This {bg=r}background{} is in red") 
        - Use "{lbg=<color>} at the begining of the line to make the entire line the background color:
            Example: pybox.console.Write("{lbg=blue}This entire line is in a blue background")

        Other commands:

        - {u} -> Underline
        - {r} -> Reverse (reverses color and background)
        - {vl}, {vr}, {ht}, {hb} : Vertical left line, vertical left line, horizontal top line, horizontal bottom line
                -> These can be used to make a box
        Available Colors: Black, White, Gray, red, green, yellow, blue, cyan, purple/magenta,
                          darkred, darkgreen, darkyellow, darkblue, darkcyan, darkpurple/darkmagenta

        Abbreviation for Colors: blk (black), w, gry (gray), r, g (green), y, b, c, p, m (magenta), db, dr, dy, db, dc, dp, dm (dark magenta)

        Examples: 
                \t -pybox.conio.Write("This {r}Text is in red{} and {b}this text is in blue")      \t - - the first {} ends the red. The last {} is not needed
                \t -pybox.conio.Write("This text {w}{bg=b}is in a blue background with bright white text.") 

        - Important Note:  When using background color, underlines, boxes, etc., Windows can change the rest of the line to the background color if the window size is changed.
            \t - you can end the line with {_} to end the block. "{bg=b}This is in blue{_}" vs. "{bg=b}This is in blue{}".  This will prevent this issue with Windows. 
        """
        _pybox.ConsoleWrite(*args)

#    def Box(text : str,fg : str = None,bg : str = None) -> bool :
#        return _pybox.ConsoleBox(text,fg,bg)

    def get_integer(text = None,*args,**kwargs) -> int :
        """
        Get an Integer from the keyboard.  This can be qualified with a range with a default.

        Example: MyInteger = pybox.console.get_integer("Enter a number: ")

        Options and Keywords 

        - use Range option to set a range:
            pybox.console.get_integer("Enter a value from 1-10",range=(1,10))
            pybox.console.get_integer("Enter a value from 1-10,opt.range(1,10)) also works.

            When the value is out of range, the user will be asked again to enter the value.
            If the user presses return, the minimum value is returned if there is no Default value

        - use Default option to set a default (for an empty return)
            pybox.console.get_integer("Enter a value from 1-10",opt.range(1,10),opt.default(5))

            note: You can set a default out of the range (when not using "NoCancel" option) to determine the user entered a blank line
                Example: pybox.console.get_integer("Enter a value from 1-10",opt.range(1,10),opt.default(-1))
                    --> Check -1 as a return value to determine user pressed return and did not enter a number.

        - use NoCancel option to disallow blank lines.  The user will be repeatedly asked for the number until a valid number is entered.
            pybox.console.get_integer("Enter a number from 1-10",range=(1,10),nocancel)

        - Colors may also be used to differentiate the question from the number:
            Example: pybox.console.get_integer("{y}Enter a number from 1-10")
                This will print the question in yellow (note that the closing "{} was not needed).
        """
        return _pybox.ConsoleGetNumber(text,*args,**kwargs)

    def get_float(text = None,*args,**kwargs) -> float :
        """
        Get a floating-point value from the keyboard.  This can be qualified with a range with a default.

        Example: MyFloat = pybox.console.get_float("Enter a number: ")

        Options and Keywords

        - use Range option to set a range:
            pybox.console.get_float("Enter a value from 1.5-10",range=(1.5,10.5))
            pybox.console.get_float("Enter a value from 1.5-10,iopt.range(1.5,10.5)') also works.

            When the value is out of range, the user will be asked again to enter the value.
            If the user presses return, the minimum value is returned if there is no Default value

        - use Default option to set a default (for an empty return)
            pybox.console.get_float("Enter a value from 1.5-10.5",opt.range(1.5,10.5),opt.default(5.7))

            note: You can set a default out of the range (when not using "NoCancel" option) to determine the user entered a blank line
                Example: pybox.console.get_float("Enter a value from 1.5-10.5",range=(1.5,10.5),default = -1)
                    --> Check -1 as a return value to determine user pressed return and did not enter a number.

        - use NoCancel() option to disallow blank lines.  The user will be repeatedly asked for the number until a valid number is entered.
            pybox.console.get_float("Enter a number from 1-10",range=(1.5,10.5),nocancel)

        - Colors may also be used to differentiate the question from the number:
            Example: pybox.console.get_float("{y}Enter a number from 1.5-10.5")
                This will print the question in yellow (note that the closing "{} was not needed).
        """        
        return _pybox.ConsoleGetFloat(text,*args,**kwargs)

class debug :
    """
    Pybox/Sagebug debug functions provide a number of functions via the Sagebox Process Window.

    To show the process window, move the mouse to the upper-right-hand part of the screen and hold it there for 
    .25 seconds.

    The Sagebox Process Window will appear, where you can write debug information.

    You can also terminate the program by pressing the "Terminate program" button, in case the program is unresponsive or hidden.
    In Python, this is really never an issue, but it still provides a nice way to terminate the program quickly.
    """
    def write(*args) :
        """
        Write a message out to the sagebox debug window. The SageboxDebug window is in the Sagebox Process Window.

        When writing to the debug window, the debug window will come up automatically the first time it is written to.
        The debug window can be manually hidden (it will not come up automatically after that)

        The Sagebox debug window is a good place to put debug information so it won't clutter up the console window.
        Each line has a line number and you can scroll through the debug output. 

        --> To hide and show the debug/Sagebox process window, move the mouse to the upper-right of the monitor and hold for
            1/4 of a second.

        As with the console output functions, you can use colors to set the color of the output:

            - Use {color} to start a color and {} to end the color. 
                Example: pybox.debug.Write("This is {red}in the color red{}")
            - You can use the first lett of the color, and do not need the closing {} if its at the end of the line:
                Example: pybox.debug.Write("This is {r}in the color red")
            - Multiple colors can be used.
                \t -Example: pybox.debug.Write("This {c}is in cyan{} and this {r}is in the color red")
            - "{x=<number>}" to set a column (does not use closing {}): Example: pybox.debug.Write("This {x=40}is at column 40")
            - "{bg=<color>"} to set the background color: Example: pybox.debug.Write("This {bg=r}background{} is in red") 
            - "{lbg=<color>} at the begining of the line to make the entire line the background color: 
                \t -Example: pybox.debug.Write("{lbg=blue}This entire line is in a blue background")
            - {bold} or {bld} for bold
            - {italic} or {i} for italic
            - {bolditalic} or {bi} for bold and italic
            - {div} for dividing line (i.e. DebugWrite("{div}\n") 

            Available Colors: Black, White, Gray, red, green, yellow, blue, cyan, purple/magenta,

            Abbreviation for Colors: w (white), r, g, y, b, c, p, m (magenta)
        """
        _pybox.DebugWrite(*args)
    def show(show : bool) -> bool :
        """
        """
        _pybox.DebugShow(show)
    def hide(hide : bool) -> bool :
        """
        """
        _pybox.DebugShow(not hide)

class MouseRegion :
    def __init__(self,_id)  : 
        self.id = _id
        self.win = _pybox.GetMouseRegionWindowControlID(self.id,1)
       

    def set_pos(self,index : int,x,y) :
        """
        Sets the current positon of the mouse region/point.

        - This does not change the size or shape of the region or point, and only sets it's position.
        - This does not change the display order of the region/point.
        - For point-type mouse regions, this sets the center point.  For region-type mouse regions, this sets the upper-left corner of the region.
        - See set_pos_l() to set position with a list/array/tuple element instead of individual values.
        
        Parameters:
        
        index  \t - index of mouse region/point
        x,y    \t - new x,y position
        """
        return _pybox.MouseRegionSetPos(self.id,index,x,y)
    
    def set_pos_l(self,index : int,pos : list) :
        """
        Sets the current positon of the mouse region/point.

        - This does not change the size or shape of the region or point, and only sets it's position.
        - This does not change the display order of the region/point.
        - For point-type mouse regions, this sets the center point.  For region-type mouse regions, this sets the upper-left corner of the region.
        - See set_pos() to set position with individual (x,y) values instead of list/array/tuple.
        
        Parameters:
        
        index  \t - index of mouse region/point
        x,y    \t - new x,y position
        """
        return _pybox.MouseRegionSetPos(self.id,index,pos[0],pos[1])
    
    def set_point(self,index : int,x,y,width,height) :
        """
        Sets the point-type region location and size.  See set_region() to change a region-type mouse region.

        - This does not change the display order of the region/point.
        - The location sets the center point, with width/height the radius in each direction.  See set_region() to set a region-type mouse region.  
        - See set_point_l() to use list/tuple/array for (x,y) and (width,height)
        - See set_point_r() to use list/tuple/array for (x,y,width,height) together

        ** note:  set_region() and set_point() can be used with any type of mouse point or region. The 'point'- or 'region'-type status will be adjusted accordingly.  

        Parameters
        
        - index         \t-- Index of mouse region/point to change.
        - x,y           \t-- New location of mouse region/point
        - width,height  \t-- New Size of mouse region/point.
        """
        return _pybox.MouseRegionSetPoint(self.id,index,x,y,width,height,True)
    
    def set_point_l(self,index : int,pos : list, size : list) :
        """
        Sets the point-type region location and size.  See set_region_l() to change a region-type mouse region.

        - This does not change the display order of the region/point.
        - The location sets the center point, with width/height the radius in each direction.  See set_region() to set a region-type mouse region.  
        - See set_point() to use individual values for x,y,width and height rather than list/tuple/array.
        - See set_point_r() to use list/tuple/array for (x,y,width,height) together

        ** note:  set_region() and set_point() can be used with any type of mouse point or region. The 'point'- or 'region'-type status will be adjusted accordingly.  

        Parameters
        
        - index         \t-- Index of mouse region/point to change.
        - pos           \t-- New location of mouse region/point
        - size          \t-- New Size of mouse region/point.
        """
        return _pybox.MouseRegionSetPoint(self.id,index,pos[0],pos[1],size[0],size[1],True)
    
    def set_point_r(self,index : int,size_rect : list) :
        """
        Sets the point-type region location and size.  See set_region_r() to change a region-type mouse region.

        - This does not change the display order of the region/point.
        - The location sets the center point, with width/height the radius in each direction.  See set_region() to set a region-type mouse region.  
        - See set_point() to use individual values for x,y,width and height rather than list/tuple/array.
        - See set_point_l() to use list/tuple/array for (x,y) and (width,height)

        ** note:  set_region() and set_point() can be used with any type of mouse point or region. The 'point'- or 'region'-type status will be adjusted accordingly.  

        Parameters
        
        - index         \t-- Index of mouse region/point to change.
        - size_rect     \t-- New location and size of mouse region/point (i.e. (x,y,width,height))
        """
        return _pybox.MouseRegionSetPoint(self.id,index,size_rect[0],size_rect[1],size_rect[2],size_rect[3],True)
    
    
    def set_region(self,index : int,x,y,width,height) :
        """
        Sets the region-type region location and size.  See set_point() to change a point-type mouse region.

        - This does not change the display order of the region/point.
        - The location given sets the upper-left of the region (see set_point() to set a point-type center location) 
        - See set_region_l() to use list/tuple/array for (x,y) and (width,height)
        - See set_region_r() to use list/tuple/array for (x,y,width,height) together

        ** note:  set_region() and set_point() can be used with any type of mouse point or region. The 'point'- or 'region'-type status will be adjusted accordingly.  

        Parameters
        
        - index         \t-- Index of mouse region/point to change.
        - x,y           \t-- New location of mouse region/point
        - width,height  \t-- New Size of mouse region/point.
        """
        return _pybox.MouseRegionSetPoint(self.id,index,x,y,width,height,False)
    
    def set_region_l(self,index : int,pos : list,size : list) :
        """
        Sets the region-type region location and size.  See set_point() to change a point-type mouse region.

        - This does not change the display order of the region/point.
        - The location given sets the upper-left of the region (see set_point() to set a point-type center location) 
        - See set_region() to use individual values for x,y,width and height rather than list/tuple/array.
        - See set_region_r() to use list/tuple/array for (x,y,width,height) together

        ** note:  set_region() and set_point() can be used with any type of mouse point or region. The 'point'- or 'region'-type status will be adjusted accordingly.  

        Parameters
        
        - index         \t-- Index of mouse region/point to change.
        - pos           \t-- New location of mouse region/point
        - size          \t-- New Size of mouse region/point.
        """
        return _pybox.MouseRegionSetPoint(self.id,index,pos[0],pos[1],size[0],size[1],False)

    def set_region_r(self,index : int,size_rect : list) :
        """
        Sets the region-type region location and size.  See set_point() to change a point-type mouse region.

        - This does not change the display order of the region/point.
        - The location given sets the upper-left of the region (see set_point() to set a point-type center location) 
        - See set_region() to use individual values for x,y,width and height rather than list/tuple/array.
        - See set_region_l() to use list/tuple/array for (x,y) and (width,height)

        ** note:  set_region() and set_point() can be used with any type of mouse point or region. The 'point'- or 'region'-type status will be adjusted accordingly.  

        Parameters
        
        - index         \t-- Index of mouse region/point to change.
        - size_rect     \t-- New location and size of mouse region/point (i.e. (x,y,width,height))
        """
        return _pybox.MouseRegionSetPoint(self.id,index,size_rect[0],size_rect[1],size_rect[2],size_rect[3],False)
    
    
    def add_point(self,x,y,width,height,**kwargs) : 
        """
        Adds a singular point-type Mouse Region point to the Mouse Region.  
        
        A Point-Type Mouse Region uses a center point (x,y) with width and height used as the radius in the X and Y directions, respectively.
        
        - See add_region() for a Region-Type Mouse Region where a specific rectangular region is described.
        - See add_point_l() to use list/array/tuple values for (x,y) and (width,height)
        - See add_point_r() to use a single list/array/tuple value for (x,y,width,height) together.
        - Index values are in the order added, with the first index starting at 0. 

        Example: add_point(x,y,5,5) 
        
        This sets a point at (x,y) with a mouse-region/point area extending 5 pixels in both directions in the X and Y axes, respectively, for a total
        size of (10,10) with (x,y) in the center.
        
        Parameters
        
        - x,y               \t -- location of new point
        - width,height      \t -- size of mouse point area in X and Y dimensions, respectively x2 (i.e. width and height are radius values)

        Optional Keywords
        
        - auto_draw         \t -- Sets the "auto draw" characteristics of the auto_draw() function output for specific to this point.
                            \t For example, auto_draw="red,circle" sets a red circle for display when auto_draw() is called. 
        - id                \t -- Sets a numeric 'user id' for the element that can be used to get its index as points are added and removed.
                            \t Indexes are in order of additions, with deleted points changing indexes of the point below, accordingly.
                            \t 'id' (e.g. id=123) can be used with get_id_index() to retrieve the Mouse Region index based on the user ID. 
        """
        return _pybox.MouseRegionAddPoint(self.id,x,y,width,height,True,**kwargs)
    
    def add_point_l(self,pos : list,size : list,**kwargs) : 
        """
        Adds a singular point-type Mouse Region point to the Mouse Region.  
        
        A Point-Type Mouse Region uses a center point (x,y) with width and height used as the radius in the X and Y directions, respectively.
        
        Example: add_point(x,y,5,5) 
        
        This sets a point at (x,y) with a mouse-region/point area extending 5 pixels in both directions in the X and Y axes, respectively, for a total
        size of (10,10) with (x,y) in the center.
        
        - See add_region() for a Region-Type Mouse Region where a specific rectangular region is described.
        - See add_point() to use individual values for x,y,width,height
        - See add_point_r() to use a single list/array/tuple value for (x,y,width,height) together.
        - If a point or region is removed, the index values are adjusted accordingly
        
        Parameters
        
        - pos       \t -- location of new point
        - size      \t -- size of mouse point area in X and Y dimensions, respectively x2 (i.e. width and height are radius values)

        Optional Keywords
        
        - auto_draw         \t -- Sets the "auto draw" characteristics of the auto_draw() function output for specific to this point.
                            \t For example, auto_draw="red,circle" sets a red circle for display when auto_draw() is called. 
        - id                \t -- Sets a numeric 'user id' for the element that can be used to get its index as points are added and removed.
                            \t Indexes are in order of additions, with deleted points changing indexes of the point below, accordingly.
                            \t 'id' (e.g. id=123) can be used with get_id_index() to retrieve the Mouse Region index based on the user ID. 
        """
        return _pybox.MouseRegionAddPoint(self.id,pos[0],pos[1],size[0],size[1],True,**kwargs)
    
    def add_point_r(self,size_rect : list,**kwargs) : 
        """
        Adds a singular point-type Mouse Region point to the Mouse Region.  
        
        A Point-Type Mouse Region uses a center point (x,y) with width and height used as the radius in the X and Y directions, respectively.
        
        Example: add_point(x,y,5,5) 
        
        This sets a point at (x,y) with a mouse-region/point area extending 5 pixels in both directions in the X and Y axes, respectively, for a total
        size of (10,10) with (x,y) in the center.
        
        - See add_region() for a Region-Type Mouse Region where a specific rectangular region is described.
        - See add_point() to use individual values for x,y,width,height
        - See add_point_l() to use list/array/tuple values for (x,y) and (width,height)
        - If a point or region is removed, the index values are adjusted accordingly
        
        Parameters
        
        - size_rect      \t -- x,y,width,height of new point (e.g. (x,y,width,height))

        Optional Keywords
        
        - auto_draw         \t -- Sets the "auto draw" characteristics of the auto_draw() function output for specific to this point.
                            \t For example, auto_draw="red,circle" sets a red circle for display when auto_draw() is called. 
        - id                \t -- Sets a numeric 'user id' for the element that can be used to get its index as points are added and removed.
                            \t Indexes are in order of additions, with deleted points changing indexes of the point below, accordingly.
                            \t 'id' (e.g. id=123) can be used with get_id_index() to retrieve the Mouse Region index based on the user ID. 
        """
        return _pybox.MouseRegionAddPoint(self.id,size_rect[0],size_rect[1],size_rect[2],size_rect[3],True,**kwargs)
    
    def add_region(self,x,y,width,height,**kwargs) : 
        """
        Adds a singular region-type Mouse Region point to the Mouse Region.  
        
        A Region-Type Mouse Region specifies a rectangular region with (x,y) as the upper-left corner of the rectangle, with width and height specifying
        the size of the rectangle in each X-Y axes, respectively.
        
        - See add_point() for a Point-Type Mouse Region where a specific point with a radius in each X-Y axes is specified.
        - See add_region_l() to use list/array/tuple values for (x,y) and (width,height)
        - See add_region_r() to use a single list/array/tuple value for (x,y,width,height) together.
        - Index values are in the order added, with the first index starting at 0. 

        Parameters
        
        - x,y               \t -- upper-left location of new region
        - width,height      \t -- width and height of the rectangular region.

        Optional Keywords
        
        - auto_draw         \t -- Sets the "auto draw" characteristics of the auto_draw() function output for specific to this point.
                            \t For example, auto_draw="red,circle" sets a red circle for display when auto_draw() is called. 
        - id                \t -- Sets a numeric 'user id' for the element that can be used to get its index as points are added and removed.
                            \t Indexes are in order of additions, with deleted points changing indexes of the point below, accordingly.
                            \t 'id' (e.g. id=123) can be used with get_id_index() to retrieve the Mouse Region index based on the user ID. 
        """
        return _pybox.MouseRegionAddPoint(self.id,x,y,width,height,False,**kwargs)
    
    def add_region_l(self,pos : list,size : list,**kwargs) : 
        """
        Adds a singular region-type Mouse Region point to the Mouse Region.  
        
        A Region-Type Mouse Region specifies a rectangular region with (x,y) as the upper-left corner of the rectangle, with width and height specifying
        the size of the rectangle in each X-Y axes, respectively.
        
        - See add_point() for a Point-Type Mouse Region where a specific point with a radius in each X-Y axes is specified.
        - See add_region() to use individual values for x,y,width,height
        - See add_region_r() to use a single list/array/tuple value for (x,y,width,height) together.
        - Index values are in the order added, with the first index starting at 0. 

        Parameters
        
        - pos       \t -- upper-left location of new region
        - size      \t -- width and height of the rectangular region.

        Optional Keywords
        
        - auto_draw         \t -- Sets the "auto draw" characteristics of the auto_draw() function output for specific to this point.
                            \t For example, auto_draw="red,circle" sets a red circle for display when auto_draw() is called. 
        - id                \t -- Sets a numeric 'user id' for the element that can be used to get its index as points are added and removed.
                            \t Indexes are in order of additions, with deleted points changing indexes of the point below, accordingly.
                            \t 'id' (e.g. id=123) can be used with get_id_index() to retrieve the Mouse Region index based on the user ID. 
        """
        return _pybox.MouseRegionAddPoint(self.id,pos[0],pos[1],size[0],size[1],False,**kwargs)
    
    def add_region_r(self,size_rect,**kwargs) : 
        """
        Adds a singular region-type Mouse Region point to the Mouse Region.  
        
        A Region-Type Mouse Region specifies a rectangular region with (x,y) as the upper-left corner of the rectangle, with width and height specifying
        the size of the rectangle in each X-Y axes, respectively.
        
        - See add_point() for a Point-Type Mouse Region where a specific point with a radius in each X-Y axes is specified.
        - See add_region() to use individual values for x,y,width,height
        - See add_region_l() to use list/array/tuple values for (x,y) and (width,height)
        - Index values are in the order added, with the first index starting at 0. 

        Parameters
        
        - size_rect     \t -- (x,y) upper-left location of new region and size (w,h) of rectangle (i.e. (x,y,w,h))

        Optional Keywords
        
        - auto_draw         \t -- Sets the "auto draw" characteristics of the auto_draw() function output for specific to this point.
                            \t For example, auto_draw="red,circle" sets a red circle for display when auto_draw() is called. 
        - id                \t -- Sets a numeric 'user id' for the element that can be used to get its index as points are added and removed.
                            \t Indexes are in order of additions, with deleted points changing indexes of the point below, accordingly.
                            \t 'id' (e.g. id=123) can be used with get_id_index() to retrieve the Mouse Region index based on the user ID. 
        """
        return _pybox.MouseRegionAddPoint(self.id,size_rect[0],size_rect[1],size_rect[2],size_rect[3],False,**kwargs)
    
    
    def set_bound_box(self,index : int,x,y,width,height,**kwargs) : 
        """
        Sets the bounding box for the mouse region or point.

        - When a bounding box is used, the mouse point or region cannot exceed the boundaries set inside the box.
        - With a Point-type index (i.e. add_point() was used), the center x,y value is restricted to the bounding box, allowing the radiusX and radiusY
          width/height to exceed the bounding box by width/2 and height/2, respectively.  
          Reduce the Bounding Box as needed to include these values with Point-type indexes. 

        - See: set_boundbox_l() to use list/array/tuple values for (x,y) and (width,height)
        - See: set_boundbox_r() to use list/array/tuple values for (x,y,width,height) together.
          
        Parameters
        
        - index         \t -- index of mouse point/region.
        - x,y           \t -- (x,y) location of region/point (for region-type, upper-left.  For point-type, center x,y)
        - width,height  \t -- width and height of region/point (for point-type, these act as radius values from the center x,y point)
        """
        return _pybox.MouseRegionSetBoundBox(self.id,index,x,y,width,height,**kwargs)

    def set_bound_box_l(self,index : int,pos : list,size : list,**kwargs) : 
        """
        Sets the bounding box for the mouse region or point.

        - When a bounding box is used, the mouse point or region cannot exceed the boundaries set inside the box.
        - With a Point-type index (i.e. add_point() was used), the center x,y value is restricted to the bounding box, allowing the radiusX and radiusY
          width/height to exceed the bounding box by width/2 and height/2, respectively.  
          Reduce the Bounding Box as needed to include these values with Point-type indexes. 

        - See: set_boundbox() to use individul values for x,y,width and height
        - See: set_boundbox_r() to use list/array/tuple values for (x,y,width,height) together.
          
        Parameters
        
        - index         \t -- index of mouse point/region.
        - pos           \t -- (x,y) location of region/point (for region-type, upper-left.  For point-type, center x,y)
        - size          \t -- width and height of region/point (for point-type, these act as radius values from the center x,y point)
        """
        return _pybox.MouseRegionSetBoundBox(self.id,index,pos[0],pos[1],size[0],size[1],**kwargs)
    
    def set_bound_box_r(self,index : int,size_rect : list,**kwargs) : 
        """
        Sets the bounding box for the mouse region or point.

        - When a bounding box is used, the mouse point or region cannot exceed the boundaries set inside the box.
        - With a Point-type index (i.e. add_point() was used), the center x,y value is restricted to the bounding box, allowing the radiusX and radiusY
          width/height to exceed the bounding box by width/2 and height/2, respectively.  
          Reduce the Bounding Box as needed to include these values with Point-type indexes. 

        - See: set_boundbox_l() to use list/array/tuple values for (x,y) and (width,height)
        - See: set_boundbox_r() to use list/array/tuple values for (x,y,width,height) together.
          
        Parameters
        
        - index         \t -- index of mouse point/region.
        - size_rect     \t -- (x,y) location of region/point (for region-type, upper-left) and (w,h) of region, i.e. (x,y,w,h) as one array/tuple/list.
        """
        return _pybox.MouseRegionSetBoundBox(self.id,index,size_rect[0],size_rect[1],size_rect[2],size_rect[3],**kwargs)

    def auto_draw(self,index = None) :
        """
        Draws all points or regions to the window. The program may handle the display of points itself by processing events, which can be much more flexible.

        auto_draw() is provided as a way to quickly display the mouse points/regions as they are used, moved, highlighted, etc.
        
        - auto_draw() can be used for most programs. However, as programs grow and require more extensive display, auto_draw() can be omitted. 
        
        Also, individual points/regions can be set to off, allowing some to use auto_draw() and others to be bypassed so that the program can draw the point itself.
        example: set_auto_draw(index,"off");
        
        ** note ** - Documentation for this feature is still in development.  See various example for usage information.
        """
        return _pybox.MouseRegionAutoDraw(self.id,index)
    
    def auto_draw_index(self,index : int) :
        """
        Calls the auto_draw() function for only the index provided.
        
        Where auto_draw() updates all Mouse Region elements in the Auto-Draw display, auto_draw() updates only the indexed element provided.
        
        This allows some control over the output, allowing for text and other additives to the auto-draw display before moving to the next
        element.
        
        See auto_draw() documentation for more information.
        
        Parameters:
        
        - index         \t - Index of element to auto-draw.
        """
        return _pybox.MouseRegionAutoDraw(self.id,index)
    
    def update_points(self) :
        """
        *** Note: This function is currently unnecessary and is provided for future use. 
        *** This function is not used when using a mouse region obtained with window.get_mouse_region()
        *** with Mouse Regions obtained from window.get_mouse_region() this function is called automatically.

        This looks at the current mouse status to update the current Mouse Region status for all points / regions.

        This is used to update the movement, highlight, selection of points/regions based on what has happened to the mouse since the last time it was called.
        
        - update_points() must be called for every get_event() to update the mouse points, and should be called in the main event loop
        before looking for updated events or values from the Mouse Region.
        
        - This function is best called directly after a get_event() call.
        """
        return _pybox.MouseRegionUpdatePoints(self.id,1)
        
    def event_ready(self) :
        """
        Returns True if an event is ready to be processed, such as a Mouse Drag event, etc. 
        
        - This is an Event-type function, which will return False once a 'true' is returned for the same event, and until another event is ready
        
        The event status is only for the event_ready() call itself and not any of the Mouse Region events that have occurred.
        
        Looking for specific events (e.g. Mouse Drag Event) will return true or false for their respective event, even if event_ready() has been called.
        
        event_ready() can be useful to only process Mouse Regions if there is a reason to do so (i.e. a Mouse Region event has occurred). 
        This can be useful in separating mouse events from Mouse Region events, to allow using the mouse in areas not within mouse region points/regions.
        """
        return _pybox.MouseRegionEventReady(self.id,1)
        
    def reset_points(self) :
        """
        Clears all points/regions from the Mouse Region object, leaving 0 points/regions.
        Once cleared, new additions start at index 0 and forward.
        """
        return _pybox.MouseRegionResetPoints(self.id,1)
        
    def mouse_drag_event(self) -> bool :
        """
        Returns True if there is a mouse point or region that is being moved by the mouse, or the mouse has otherwise clicked on the region/point
        while not yet releasing the mouse button (i.e. the mouse buttin is pressed on the object).
        
        When mouse_drag_event() returns true, get_last_selected() can be used to retrieve the index of the Mouse Region element that has changed.
        
        - This is an Event-type function, which will return False once a 'true' is returned for the same event, and until another event is ready
        """
        return _pybox.MouseRegionMouseDragEvent(self.id,1)
    
    def mouse_drag_ended(self) -> bool :
        """
        Returns True if a mouse/region being dragged by the mouse (or was clicked upon) has been released. 

        A Drag Event ends when the mouse is released from a selected region/point.
        
        When mouse_drag_ended() returns true, get_last_selected() can be used to retrieve the index of the Mouse Region element that has changed.
        
        - This is an Event-type function, which will return False once a 'true' is returned for the same event, and until another event is ready
        """
        return _pybox.MouseRegionMouseDragEnded(self.id,1)
        
    def remove_bound_box(self,index : int) :
        """
        Removes a bounding box constraint from a mouse region or point.

        See: set_bound_box() to set a bounding box for a mouse region or point. Or use bound_box as a keyword when adding a point to add a bound box to a point/region.
        
        Parameters
        
        - index         \t -- index of mouse point/region.
        """
        return _pybox.MouseRegionRemoveBoundBox(self.id,index)
 
    def reset_selected(self) :
        """
        Resets the last selected point value to -1.
        The 'last selected point' can be used to keep a static value for selected point, even after it has been released from being moved or selected with the mouse.

        - The 'selected point' (i.e. get_current_selection()) is the point that is being moved or otherwise the mouse has clicked on without yet unclicking the button.
        - This resets last selected point (i.e. get_last_selected())
        - reset_selected() also resets the last highlighted index (i.e. get_last_highlighted())
        
        ** Note: Once the mouse is released from a selection, this value is stored as the 'last selected point' for later reference.  
        This 'last selected' value remains the same until a new region or point is selected, or reset_selected() is called to reset it to -1 (no selection)

        See: get_last_selected() to get the last selected item (vs. get_current_selection())
        """
        return _pybox.MouseRegionResetSelected(self.id,1)
    
    def get_current_selection(self) -> int :
        """
        Returns the index of the currently selected item. 

        - Note: The currently selected item is active only if the mouse is currently moving a point or region, or has clicked on a point or region and
        the mouse button has not yet been unclicked.  Once the mouse is unclicked, the item is no longer selected and -1 is returned.

        - See get_last_selected() to return the value of the most recently selected item even after the mouse has been released.

        - Note: When there is no selected item or the mouse is no in contact with the mouse region/point, a -1 is returned to indicate there is no currently selected item.

        Returns:
        
        If the mouse is currently moving or otherwise has clicked on an object (without having unclicked the mous yet, whether it is moving the region/point or not),
        the index of the point/region is returned. Otherwise -1 is returned to indicate there is no selected item.
        """
        return _pybox.MouseRegionGetCurrentSelection(self.id,1)

    def get_last_selected(self) -> int :
        """
        Returns the index of the last selected item (or the currently selected item of the mouse is moving or otherwise pressed on a region/point).

        - Note: get_last_selected() returns the last selected item, which also includes an item that is currently selected (i.e. currently being moved by the mouse)
        
        get_last_selected() returns the last item that was selected (or -1 if there is no previous selection).  This differs from get_current_selection() which only
        returns an index value if the mouse is currently pressed on a selected item (which then returns to -1 when the mouse button is released).

        - get_last_selected() will return the value of the last selection, unless reset_selected() is called or there has not yet been a selected item. 
        This is also useful when using auto_draw().
        """
        return _pybox.MouseRegionGetLastSelected(self.id,1)
    
    def get_current_highlight(self) -> int :
        """
        Returns the index of the currently highlighted item. 

        The currently highlighted item is the item that the mouse is currently over or has selected. 

        - Note: When there is no highlighted item or the mouse is no longer over the previous item, a -1 is returned to indicate there is no current highlight.
        - See: get_last_highlighted() to get the last and/or current highlighted item. 
        
        Returns:
        
        If the mouse is currently within a region (whether it is moving the region/point or not), the index of the mouse region/point is returned.
        Otherwise -1 is returned to indicate there is no highlighted item.
        """
        return _pybox.MouseRegionGetCurrentHighlight(self.id,1)
    
    def get_last_highlighted(self) -> int :
        """
        Returns the index of the last highlighted item (or the currently highlighted item of the mouse is currently over a region/point).

        - Note: get_last_highlighted() returns the last highlighted item, which also includes an item that is currently highlighted (i.e. mouse is currently over).
        
        get_last_highlighted() returns the last index that was highlighted (or -1 if there is no previously highlighted item).  
        This differs from get_current_highlight() which only returns an index value if the mouse is currently over a mouse point/region 
        (which then returns to -1 when the mouse is no longer over the item).

        - get_last_highlighted() will return the value of the last highlighted item, unless reset_selected() is called or there has not yet been a highlighted item. 
        This is also useful when using auto_draw().
        """
        return _pybox.MouseRegionGetLastHighlight(self.id,1)
    
    def selection_changed(self) -> bool :
        """
        Returns true of the selection changed since the last call to selection_changed(), or a new selection has occurred.

        - The selection occurs when the mouse clicked on region or point.  The selection value remains active while the point/region is being moved. 
        See get_last_selected() to get the last selected item even after it is no longer being moved.

        - Use get_last_selected() to obtain the index of the mouse point/region that is referenced by this event.
        - note: -1 as an index value may be returned if the selection changed to no selection.
        
        - This is an Event-type function, which will return False once a 'true' is returned for the same event, and until another selection_changed() event is ready
        """
        return _pybox.MouseRegionSelectionChanged(self.id,1)
    
    def highlight_changed(self) -> bool :
        """
        Returns true of the highlight index changed since the last call to highlight_changed(), or a new highlight index has occurred.

        - The highlight occurs when the mouse is over a region or point.  The highlight value remains active while the mouse is over the point/region. 
        See get_last_highlighted() to get the last highlighted item even after it is no longer being moved.

        - Use get_last_highlighted() to obtain the index of the mouse point/region that is referenced by this event.
        - note: -1 as an index value may be returned if the selection changed to no selection.
        
        - This is an Event-type function, which will return False once a 'true' is returned for the same event, and until another highlight_changed() event is ready
        """
        return _pybox.MouseRegionHighlightChanged(self.id,1)
    
    def add_points(self, size_rect : list,**kwargs) :
        """
        Adds an array, list, or tuple set of point-type Mouse Region point to the Mouse Region.  
        
        A Point-Type Mouse Region uses a center point (x,y) with width and height used as the radius in the X and Y directions, respectively.
        
        - See add_regions() for a Region-Type Mouse Region where a specific rectangular region is described vs. (x,y) point with surrounding radius values.
        - Index values are in the order added, with the first index starting at 0. 

        
        Example: 
        
        my_points = [(200,500,50,50),(300,500,50,50),(400,500,50,50),(500,500,50,50),(600,500,50,50)], 
        mr.add_points(my_list) 
        
        This sets 5 points at (x,y) with a mouse-region/point area extending 50 pixels in both directions in the X and Y axes, respectively, for a total
        size of (100,100) with (x,y) in the center.
        
        Parameters
        
        - size_rect         \t -- list of points in (x,y,w,h) list, tuple, or array

        Optional Keywords
        
        - auto_draw         \t -- Sets the "auto draw" characteristics of the auto_draw() function output for specific to this point.
                            \t For example, auto_draw="red,circle" sets a red circle for display when auto_draw() is called. 
        - id                \t -- Sets a numeric 'user id' for the element that can be used to get its index as points are added and removed.
                            \t Indexes are in order of additions, with deleted points changing indexes of the point below, accordingly.
                            \t 'id' (e.g. id=123) can be used with get_id_index() to retrieve the Mouse Region index based on the user ID. 
        """
        return _pybox.MouseRegionAddPoints(self.id,size_rect,True,**kwargs)
   
    def add_regions(self, Loc : list,**kwargs) :
        """
        Adds an array, list, or tuple set of region-type Mouse Region point to the Mouse Region.  
        
        A Region-Type Mouse Region specifies a rectangular region with (x,y) as the upper-left corner of the rectangle, with width and height specifying
        the size of the rectangle in each X-Y axes, respectively.
        
        - See add_points() for a Point-Type Mouse Region where a specific point with a radius in each X-Y axes is specified.
        - Index values are in the order added, with the first index starting at 0. 

        
        Example: 
        
        my_points = [(200,500,50,50),(300,500,50,50),(400,500,50,50),(500,500,50,50),(600,500,50,50)], 
        mr.add_regions(my_list) 
        
        This sets 5 rectangle regions at with upper-left (x,y) and width/height of 50 in each direction.
        
        Parameters
        
        - size_rect         \t -- list of regions in (x,y,w,h) list, tuple, or array

        Optional Keywords
        
        - auto_draw         \t -- Sets the "auto draw" characteristics of the auto_draw() function output for specific to this point.
                            \t For example, auto_draw="red,circle" sets a red circle for display when auto_draw() is called. 
        - id                \t -- Sets a numeric 'user id' for the element that can be used to get its index as points are added and removed.
                            \t Indexes are in order of additions, with deleted points changing indexes of the point below, accordingly.
                            \t 'id' (e.g. id=123) can be used with get_id_index() to retrieve the Mouse Region index based on the user ID. 
        """
        return _pybox.MouseRegionAddPoints(self.id,Loc,False,**kwargs)
   
    def set_options(self,**kwargs) :
        """
        Sets keyword-based options for the Mouse Region object. This can be useful to change options when using different or new sets of points. 
        This function can be useful when re-using the Mouse Region obtained from the window (e.g. win.GetMouseRegion()), when using mouse points for different
        types of processes in the same window.  (you can also create a new and separate MouseRegion by declaring a MouseRegion object).

        Keywords:
        
        - auto_draw         \t -- Sets the "auto draw" characteristics of the auto_draw() function output for all current and new mouse regions/points.
                            \t For example, auto_draw="red,circle" sets a red circle for all elements for display when auto_draw() is called. 
        """
        return _pybox.MouseRegionSetOptions(self.id,1,**kwargs)
   
    def set_auto_draw_index(self,index : int,auto_draw_string : str) :
        """
        Sets the auto_draw() characteristics of the given index.

        Use auto_draw() with no index to set the characteristics of all points or regions simultaneously.  
        When using the index value, the changes only affect the current index's auto_draw() characteristics.

        ** Note ** -- Documentation for this feature is still in development.  See various example for usage information. ---
        """
        return _pybox.MouseRegionSetAutoDraw(self.id,index,auto_draw_string)
   
    def set_auto_draw(self,auto_draw_string : str) :
        """
        Sets the auto_draw() characteristics of all points/regions simultaneously.  This also sets the default AutoDraw characteristics of new point/regions added 
        after this function call.

        Use auto_draw() with an index to set the AutoDraw characteristics of a single point or region.
        
        ** Note ** -- Documentation for this feature is still in development.  See various example for usage information. ---
        """
        return _pybox.MouseRegionSetAutoDraw(self.id,-20000,auto_draw_string)
   
    def get_display_index(self,index : int) -> int :
        """
        Gets the display index iteratively, in the display order.
        
        - When Mouse Region items are selected, they are moved to the top of the display order (unless the keyword dont_promote is used to prevent it).
          Thus, the index order vs. the display order may not be the same. 

        To iterate through the display order, GetDisplayIndex() can be called until a -1 is returned to signal there are no more display items:
        
        Example:
        
        index = -1
        while (index := GetDisplayIndex(index)) >= 0) : perform_display_operation_on_index()
        
        Parameters:
        
        - index     \t -- index of current iterative display item (** this must start with -1)
        
        Returns"
        
        Index Value of display item.  A return of -1 means there are no more items to display.
        """
        return _pybox.MouseRegionGetDisplayIndex(self.id,index)
    
    def get_num_indexes(self) -> int :
        """
        Returns the number of points and regions in the Mouse Region object.
        """
        return _pybox.MouseRegionGetNumIndexes(self.id,1)
    
    def get_kill_passed_events(self, kill_events : bool = True) :
        """
        By default, mouse movements, clicks, unclicks, are not passed as general events when the Mouse Region has determined a Mouse Region event has 
        occured.

        For example, if the main event loop looks for mouse movements or clicks, these will not be reported if the mouse is over or is currently
        moving a mouse point or region.
        
        This helps to react only to mouse events not within mouse regions.
        
        Sometimes it may be useful to get the mouse events as regions are being moved or highlighted. 
        
        Using get_kill_passed_events(False) will pass these events through, so the same mouse events that Mouse Region used will also be available to the main
        event loop. 
        
        Parameters:
        
        - kill_events       \t - True to not pass Mouse Region mouse events to the main event loop (default behavior).  
                            \t   False to pass the events for use with the main event loop.
        """
        return _pybox.MouseRegionKillPassedEvents(self.id,kill_events)
    
    def get_userid_index(self, userid : int) :
        """
        Returns the mouse region/point index corresponding to the user ID as set with the "id" keyword when the point/region was added.
       (e.g. add_point(my_point,id=123)

        -1 is returned if no valid index was found
        
        Parameters:

        - user_id       \t - User ID as given with "id" keyword on point creation
        
        Returns:
        
        Index of point that has this user ID.  
        -1 is returned if no point was found.
        """
        return _pybox.MouseRegionGetUserIDIndex(self.id,userid,True)
    
    def get_index_userid(self, index : int) :
        """
        Returns userID corresponding to the mouse region/point index given as input.
        
        If the point/region was not specified the "id" keyword when the point/region was added, the user ID is 0 for that point/region.
        
        -1 is returned if the index was not a valid mouse region/point index.

        Parameters :
        
        - index     \t - index of the mouse region/point from which to obtain its user ID
        
        Returns
        
        
        User ID of the mouse point/region if ID was established with the 'id' keyword when the point/region was created.
        If no user id was established via the 'id' keyword, 0 is returned
        
        -1 is returned if the index given was invalid.
        """
        return _pybox.MouseRegionGetUserIDIndex(self.id,index,False)

    class Point :
        def __init__(self) :
            index = 0
            cur = ( 0,0 )
            cur_oob = ( 0, 0 )
            valid = False 
            
    class Region :
        def __init__(self) :
            index = 0
            region = ( 0,0,0,0 )
            region_oob = ( 0, 0, 0, 0 )
            valid = False 
            
    def get_point(self,index : int) -> Point :
        """
        """
        l = _pybox.MouseRegionGetPoint(self.id,index)
        p = MouseRegion.Point()
        p.index = l[0]
        p.cur = (l[1],l[2])
        p.cur_oob = (l[3],l[4])
        p.valid = bool(l[5])
        return p
        
    def get_region(self,index : int) -> Region :
        """
        """
        l = _pybox.MouseRegionGetRegion(self.id,index)
        p = MouseRegion.Region()
        p.index = l[0]
        p.region = (l[1],l[2],l[3],l[4])
        p.region_oob = (l[5],l[6],l[3],l[4])
        p.valid = bool(l[7])
        
        return p
   


class Slider :
    """
    Pybox Slider Class.  See functions such as NewSlider and DevSlider.
    """
    def __init__(self,_id)  : self.id = _id
    def moved(self)         -> bool :
        """
        Returns a True value if the slider has been moved, False if it has not or in subsequent calls until the next event. 
        Use GetPos() to retreive the current value of the slider.

        --> This function an EVENT function: This function will only return a True value ONE TIME PER EVENT 
        --> and will return False after the first call until the event occurs again. 

            In most events, you can specify "peek=true" as a parameter so that the event will not be reset.
        """
        return _pybox.SliderMoved(self.id)       

    def get_pos(self)        -> int  :
        """
        Returns the current position of the slider based on its range.
        Use get_pos() for default sliders, and get_pos_f() for floating-pointer sliders
        (floating-point sliders are created with new_slider_f() and dev_slider_f() forms).

        The default range is (0-100), but this can be set through the Range() option when creating the slider.
        """ 
        return _pybox.SliderGetPos(self.id)      

    def get_pos_f(self)        -> int  :
        """
        Returns the current position of the floating-pointer slider based on its range.
        Use get_pos() for default sliders, and get_pos_f() for floating-pointer sliders
        (floating-point sliders are created with new_slider_f() and dev_slider_f() forms).

        The default range is (0-100), but this can be set through the Range() option when creating the slider.
        """ 
        return _pybox.SliderGetPosf(self.id)     
    
    def set_pos(self,pos)    -> bool : 
        """
        Sets the position of the slider within the slider's range.
        Use set_pos() for default sliders, and set_pos_f() for floating-pointer sliders
        (floating-point sliders are created with new_slider_f() and dev_slider_f() forms).

        The default range is (0-100), but this can be set through the Range() option when creating the slider.
        """
        return _pybox.SliderSetPos(self.id,pos)  

    def set_pos_f(self,pos)    -> bool : 
        """
        Sets the position of the floating-point slider within the slider's range.
        Use set_pos() for default sliders, and set_pos_f() for floating-pointer sliders
        (floating-point sliders are created with new_slider_f() and dev_slider_f() forms).


        The default range is (0-100), but this can be set through the Range() option when creating the slider.
        """
        return _pybox.SliderSetPosf(self.id,pos)  

class Listbox :
    "Pybox Listbox class.  See function such as NewListbox() or DevListbox()"
    def __init__(self,_id)   : self.__id = _id
    def add_item(self,item : str) -> bool :
        "Adds the text to the listbox as a new item."
        return _pybox.ListboxAddItem(self.__id,item)

    def item_selected(self,*args) -> bool :
        """
        returns True is an item has been selected in the listbox, False if not or in subsequent calls until the next event.

        --> This function an EVENT function: This function will only return a True value ONE TIME PER EVENT 
        --> and will return False after the first call until the event occurs again. 

            In most events, you can specify "peek=true" as a parameter so that the event will not be reset.
        """
        return _pybox.ListboxItemSelected(self.__id,*args)

    def get_selection(self) -> int :
        "Returns the positional value of the currently selected item."
        return _pybox.ListboxGetSelection(self.__id)

    def set_selection(self,selection : int) -> bool :
        "Sets and highlights the current selection in the listbox"
        return _pybox.ListboxSetSelection(self.__id,int(selection))

    def get_num_items(self) -> int :
        "Returns the number of items in the listbox."
        return _pybox.ListboxGetNumItems(self.__id)

    def clear_list(self) -> bool :
        "Clears the current listbox."
        return _pybox.ListboxClearList(self.__id)

    def set_location(self,x, y = None) -> bool :
        """
        Sets the window location of the listbox.

        Setlocation(width,height) may be used, as well as a list or tuple: 
        SetLocation(Location), where location = (width,height)

        """
        if (isinstance(x,list) or isinstance(x,tuple)) :
            y = x[1]
            x = x[0]
        if y is None: y = 0
        return _pybox.ListboxSetLocation(self.__id,int(x),int(y))

class Combobox :
    "Pybox ComboBox functions.  See functions such as NewCombobox or DevCombobox()"
    def __init__(self,_id)   : self.__id = _id

    def add_item(self,item : str) -> bool :
        "Adds the text to the combobox as a new item."
        return _pybox.ComboboxAddItem(self.__id,item)
    
    def item_selected(self,*args) -> bool :
        """
        returns True is an item has been selected in the combobox, False if not or in subsequent calls until the next event.

        --> This function an EVENT function: This function will only return a True value ONE TIME PER EVENT 
        --> and will return False after the first call until the event occurs again. 

            In most events, you can specify "peek=true" as a parameter so that the event will not be reset.
        """        
        return _pybox.ComboboxItemSelected(self.__id,*args)

    def get_selection(self) -> int :
        "Returns the positional value of the currently selected item."
        return _pybox.ComboboxGetSelection(self.__id)

    def set_selection(self,selection : int) -> bool :
        "Sets and highlights the current selection in the listbox"
        return _pybox.ComboboxSetSelection(self.__id,int(selection))

    def get_num_items(self) -> int :
        "Returns the number of items in the combobox."
        return _pybox.ComboboxGetNumItems(self.__id)

    def clear_list(self) -> bool :
        "Clears the current combobox."
        return _pybox.ComboboxClearList(self.__id)

    def set_location(self,x, y = None) -> bool :
        """
        Sets the window location of the combobox.

        Setlocation(width,height) may be used, as well as a list or tuple: 
        SetLocation(Location), where location = (width,height)

        """
        if (isinstance(x,list) or isinstance(x,tuple)) :
            y = x[1]
            x = x[0]
        if y is None: y = 0
        return _pybox.ComboboxSetLocation(self.__id,int(x),int(y))

class InputBox:
    "Pybox InputBox class.  See functions such as NewInputBox() or DevInputBox()"
    def __init__(self,_id)   : self.__id = _id
    def return_pressed(self,peek = None,*args) -> bool :
        """
        Returns True if the user pressed Return in the input box False if not or subsequently until the next event.

        Using ReturnPressed() is the best way to determine if a user has signaled end of input to an input box.

        --> This function an EVENT function: This function will only return a True value ONE TIME PER EVENT 
        --> and will return False after the first call until the event occurs again. 

            In most events, you can specify "peek=true" as a parameter so that the event will not be reset.
        """
        return _pybox.InputBoxReturnPressed(self.__id,peek,*args)

    def get_text(self) -> str :
        "Returns the text of the current Input box.  Returns an empty string if there is no input."
        return _pybox.InputBoxGetText(self.__id)

    def get_float(self) -> float : 
        """
        Returns the number in the input box as a floating-point value.

        If there is no value in the input box (or it is not a number) 0 is returned. 
        You can use set_range() or set_range_f() to ensure only numbers are allowed in the input box.
        """
        return _pybox.InputBoxGetFloat(self.__id)
    def get_integer(self) -> int : 
        """
        Returns the number in the input box as an integer value.

        If there is no value in the input box (or it is not a number) 0 is returned. 
        You can use SetRange() or SetRangef() to ensure only numbers are allowed in the input box.
        """        
        return _pybox.InputBoxGetInteger(self.__id)

    def set_text(self, text : str) -> bool :
        """
        Sets the text in the input box, replacing any current text.

        The input value can be text, a number, or anything that can be converted to text.

        --> Note SetValue() and SetText() are the same function
        """
        if not isinstance(text,str) : text = "{}".format(text)
        return _pybox.InputBoxSetText(self.__id,text)
    def set_value(self, text : str) -> bool :
        """
        Sets the text in the input box, replacing any current text.

        The input value can be text, a number, or anything that can be converted to text.

        --> Note SetValue() and SetText() are the same function
        """        
        if not isinstance(text,str) : text = "{}".format(text)
        return _pybox.InputBoxSetText(self.__id,text)
    def show(self,show : bool = True) -> bool :
        "Shows (or Hides) the input box (i.e. makes it appear or disappear entirely)."
        return _pybox.InputBoxShow(self.__id,show)
    def hide(self,hide : bool = True) -> bool :
        "Hides (or Shows) the input box (i.e. makes it appear or disappear entirely)."
        return _pybox.InputBoxHide(self.__id,hide)
    def enable(self,enable : bool = True) -> bool :
        "Enables (or disables) the input box.  When disabled, no input will be allowed into the input box."
        return _pybox.InputBoxEnable(self.__id,enable)
    def disable(self,disable : bool = True) -> bool :
        "Disables (or enables) the input box.  When disabled, no input will be allowed into the input box."
        return _pybox.InputBoxDisable(self.__id,disable)

    def clear_text(self) -> bool :
        "Clears all text from the input box."
        return _pybox.InputBoxClearText(self.__id)

    def mouse_wheel_moved(self,peek = None,*args) -> bool :
        """
        returns True of the MouseWheel was moved in the input box, False if not or until the next event.

        The MouseWheel can be used to increase or decrease values in the input box. 
        See SetMouseWheel() to do this automatically.

        See GetMouseWheelValue() to get the value, which is a positive integer (ususally -1 or 1) to determine the direction.
        If the mousewheel is moved quickly, 2 or 3 (or -2,-3) may be returned to reflect the speed of mousewheel movement.

        --> This function an EVENT function: This function will only return a True value ONE TIME PER EVENT 
        --> and will return False after the first call until the event occurs again. 

            In most events, you can specify "peek=true" as a parameter so that the event will not be reset.
        """
        return _pybox.InputBoxMouseWheelMoved(self.__id,peek,*args)

    def get_mouse_wheel_value(self) -> int :
        """
        Returns the value of the last mouse wheel movement (-1 or 1 usually).  See mouse_wheel_moved() to check when the event occurs.

        This returns the results of the last event and will return the same value until a new event occurs. 

        Usually the value is -1 or 1 to indicate direction, and can be higher (such as -2 or 2) to reflect a mousewheel that has moved very quickly.

        This value can be used to multiply against an increase or decrease in value, such as:

        if MyInputBox.MouseWheelMoved() : MyValue += Increment*GetMouseWheelValue() 
        """
        return _pybox.InputBoxGetMouseWheelValue(self.__id)

    def set_mouse_wheel(self,add,sub = None,min = None,max = None) -> bool :
        """
        Sets the mousewheel to automatically increase & decrease the value entered in the input box. 

        --> This also sets the values for an arrowbox() when placed to the right of the input box.  See add_arrow_box() for more information

        add = number to add when the mousewhwwl is moved in the positive direction.
        sub = number to add when the mousewheel is moved in the negative direction (note: this must be a NEGATIVE value, as it is the value subtracted)
        min,max = minimum and maximum values 

        Example: InputBox.set_mouse_wheel(1,-1,-10,10)
            This sets the mousewheel to subtract 1 (i.e. add -1) and add 1 on mousewheel movement with a minimum value of -10 and maximum value of 10

        Integer and Float values can be used. To ensure floating point, you can cast to a float() value, such as:
            InputBox.SetMouseWheel(float(1),-1,-10,10)
            note: only one float value is required - any float value converts the input box to a floating-point input box.

        floating-point example: InputBox.set_mouse_wheel(1.5,-1.5,10,10) 

        See: set_mouse_wheel_f() to specifically set floating-point values
        """
        _pybox.InputBoxSetMouseWheel(self.__id,add,sub,min,max)

    def set_mouse_wheel_f(self,add,sub = None,min = None,max = None) -> bool :
        """
        Sets the mousewheel to automatically increase & decrease the value entered in the input box, setting the input box to a floating-point box, even
        when integer values are used in the function call. 

        --> This also sets the values for an arrowbox() when placed to the right of the input box.  See add_arrow_box() for more information

        add = number to add when the mousewhwwl is moved in the positive direction.
        sub = number to add when the mousewheel is moved in the negative direction (note: this must be a NEGATIVE value, as it is the value subtracted)
        min,max = minimum and maximum values 

        Example: InputBox.set_mouse_wheel_f(1,-1,-10,10)
            This sets the mousewheel to subtract 1 (i.e. add -1) and add 1 on mousewheel movement with a minimum value of -10 and maximum value of 10, but 
            also allows floating-point values to be entered manually.

        Example: InputBox.set_mouse_wheel_f(1.5,-1.5,10,10) 

        See: set_mouse_wheel() to use integer or floating point values.
        """        
        _pybox.InputBoxSetMouseWheel(self.__id,float(add),sub,min,max)

    def set_range(self,min = None,max = None) -> bool :
        """
        Sets the range of the input box

        If any floating-point valued are used, this sets the status of the input box to an integer input box.
        Otherwise, it allows floating-point values. 

        See: set_range_f() to explicitly set floating-point values, even if integer values are used in the function call. 

        Example: InputBox.SetRange(-100,100)

        To specify floating-point, only one floating-point value needs to be used.

        Example: InputBox.set_range(float(-100),100)
        Example: InputBox.set_range(-100.0,100)
        Example: InputBox.set_range(-50.5,50.5)
        """
        _pybox.InputBoxSetRange(self.__id,min,max)

    def set_range_f(self,min = None,max = None) -> bool :
        """
        Sets the range of the input box, setting the input box as a floating-point box so that floating-point values
        can be also typed in manually.


        See: set_range() to set either integer or float, depending on the type of input values used for the function.

        Example: InputBox.set_range_f(-100,100)
        Example: InputBox.set_range_f(float(-100),100)
        Example: InputBox.set_range_f(-100.0,100)
        Example: InputBox.set_range_f(-50.5,50.5)

        All of the above functions set the input box as a floating-point input box.
        """
        _pybox.InputBoxSetRange(self.__id,float(min),float(max))

    def set_min(self,_min) -> bool :
        """
        Sets the minimum value of the input box.  

        When a minimum is set, there can be no maximum.

        If a floating-point value is used, the input box is set to a floating-point box, otherwise it is set to an Integer box.

        Use set_minf() to explicitly set a floating-point value regardless of input type to the function:

        See: SetRange() to set the minimum and maximum values together.

        Examples:
            set_min(-10) -> Set minimum to -10
            set_min(float(-10) -> set minimum to -10, but as floating-point
            set_min(-10.0)   -> Set minimum to -10 as floating-point
            set_min(-10.5)   -> Set minimum to -10.5 as floating-point

        """
        _pybox.InputBoxSetMin(self.__id,_min)

    def set_max(self,_max) -> bool :
        """
        Sets the maximum value of the input box.  

        When a maximum is set, there can be no minimum.

        See: SetRange() to set the minimum and maximum values together.

        If a floating-point value is used, the input box is set to a floating-point box, otherwise it is set to an Integer box.

        Use set_maxf() to explicitly set a floating-point value regardless of input type to the function:

        Examples:
            set_max(10) -> Set maximum to 10
            set_max(float(10) -> set maximum to 10, but as floating-point
            set_max(10.0)   -> Set maximum to 10 as floating-point
            set_max(10.5)   -> Set maximum to 10.5 as floating-point

        """        
        _pybox.InputBoxSetMax(self.__id,_max)

    def set_min_f(self,min) -> bool :
        """
        Sets the minimum value of the input box, setting the box as a floating-point box regardless of the min value type..  

        When a minimum is set, there can be no maximum.

        If a floating-point value is used, the input box is set to a floating-point box, otherwise it is set to an Integer box.

        Use set_min() to set an integer or float minimum, depending on the type of the min value.

        See: set_range() to set the minimum and maximum values together.

        Examples:
            set_min_f(-10) -> Set minimum to -10
            set_min_f(-10.0)   -> Set minimum to -10 
            set_min_f(-10.5)   -> Set minimum to -10.5

        """ 
        _pybox.InputBoxSetMin(self.__id,float(min))

    def set_max_f(self,max) -> bool :
        """
        Sets the maximum value of the input box.  

        When a maximum is set, there can be no minimum.

        See: set_range() to set the minimum and maximum values together.

        If a floating-point value is used, the input box is set to a floating-point box, otherwise it is set to an Integer box.

        Use set_max() to set an integer or float maximum, depending on the type of the min value.

        Examples:
            set_max_f(10) -> Set maximum to 10
            set_max_f(float(10) -> set maximum to 10, but as floating-point
            set_max_f(10.0)   -> Set maximum to 10 as floating-point
            set_max_f(10.5)   -> Set maximum to 10.5 as floating-point

        """                
        _pybox.InputBoxSetMax(self.__id,float(max))
    
    def add_arrowbox(self) -> bool :
        """
        Adds an arrow box to the right of the input box with an UP and DOWN arrow button.

        When these buttons are pressed, the value in the input box is moved up and down depending on the add & subtraction value set for the input box.

        The default values are 1 and -1. 

        Use set_mouse_wheel() to change the up/down values, as they pair with the MouseWheel values.
        """
        return _pybox.InputBoxAddArrowBox(self.__id)

class Button:
    """
    Pybox Button Class.  See functions such as NewButton(), NewCheckbox(), DevButton(), and DevCheckbox()

    Pybox Button Class covers a range of button types: Buttons, Checkboxes, and Radiobuttons

    Typically RadioButtons are accessed through a ButtonGroup() since there are always more than Radio Buttons at a time. 
    Buttons and Checkboxes can also be in a Button Group for easier access, but are usually access by their individual object names.
    """
    def __init__(self,_id)   : self.__id = _id
    def pressed(self,peek = None) -> bool : 
        """
        Returns true of the button has been pressed.  Returns false afterwards until pressed again (i.e. this is an event)

        --> This function an EVENT function: This function will only return a True value ONE TIME PER EVENT 
        --> and will return False after the first call until the event occurs again. 

            In most events, you can specify "peek=true" as a parameter so that the event will not be reset.
        """
        return _pybox.ButtonPressed(self.__id)

    def unpressed(self,peek = None) -> bool : 
        """
        Returns true of the button has been unpressed.  Returns false afterwards until unpressed again (i.e. this is an event)

        --> This function an EVENT function: This function will only return a True value ONE TIME PER EVENT 
        --> and will return False after the first call until the event occurs again. 

            In most events, you can specify "peek=true" as a parameter so that the event will not be reset.
        """
        return _pybox.ButtonUnpressed(self.__id)

    def checked(self) -> bool : 
        """
        Returns true of the checkbox is currently checked.  False if it is not checked or until next event occurs.

        --> This function an EVENT function: This function will only return a True value ONE TIME PER EVENT 
        --> and will return False after the first call until the event occurs again. 

            In most events, you can specify "peek=true" as a parameter so that the event will not be reset.
        """
        return _pybox.ButtonChecked(self.__id)

    def show(self,show : bool = True) -> bool :
        "Shows (or hides) the button (i.e. appears or disappears from view altogether)"
        return _pybox.ButtonShow(self.__id,show)

    def hide(self,hide : bool = True) -> bool :
        "Hides (or dhows) the button (i.e. appears or disappears from view altogether)"
        return _pybox.ButtonShow(self.__id,not hide)

    def set_text(self,text : str) -> bool :
        "Sets the text of the button.  The size of the button will change in relation to the next text unless the Width was explicitly set on button creation."
        return _pybox.ButtonSetText(self.__id,text)

    def set_location(self,x, y = None) -> bool :
        """
        Sets the window location of the button.

        set_location(width,height) may be used, as well as a list or tuple: 
        set_location(Location), where location = (width,height)
        """
        if (isinstance(x,list) or isinstance(x,tuple)) :
            y = x[1]
            x = x[0]
        if y is None: y = 0
        return _pybox.ButtonSetLocation(self.__id,int(x),int(y))

    def set_location_l(self,pos : list) -> bool :
        """
        Sets the window location of the button from a list, tuple, or array. i.e. SetLocationL((x,y)) 
        """
        return _pybox.ButtonSetLocation(self.__id,int(pos[0]),int(pos[1]))

class RadioButtonGroup:
    """ 
    Pybox Radio Button Group Class.  See functions such as NewRadioButtons() or DevRadioButtons()

    A Radio Button Group contains multiple Radiop Buttons so that they do not need to be tracked, created or 
    stored independently.

    With a Radio Button Group you can specify the radio button by position (i.e. order created) and manage them all in one group.

    Example:    if (radiobotton.pressed) : buttonpressed = radiobutton.GetCheckedButton()
    
    checks if any of the radio buttons were pressed. If so, then button pressed is assigned to the button that was pressed.
    """
    def __init__(self,_id)   : self.id = _id

    def pressed(self,peek = None) -> bool : 
        """
        Returns true of a button in the button group was pressed.  Returns false afterwards until pressed again (i.e. this is an event)
        
        Use GetCheckedButton() to get the index of the button pressed
            example: PressedButton = MyRadioButtons.GetCheckedButton())

        --> This function an EVENT function: This function will only return a True value ONE TIME PER EVENT 
        --> and will return False after the first call until the event occurs again. 

            In most events, you can specify "peek=true" as a parameter so that the event will not be reset.
        """
        return _pybox._ButtonGroupPressed(self.id,peek)

    def get_checked_button(self) -> int :
        "Returns the zero-based index of the currently checked (i.e. highlighted) radio button."
        return _pybox._ButtonGroupGetChecked(self.id)

    def get_checked_button_text(self) -> str :
        "Returns the ascii-text name of the currently highlighted radio button."
        return _pybox._ButtonGroupGetCheckedText(self.id)

    def get_button_text(self,id) -> str:
        "Returns the ascii-text name of the currently highlighted radio button. The ID is the zero-based index of the radio button."
        return _pybox._ButtonGroupGetText(self.id,id)

class UpdateType(IntEnum):
    """
    Window Auto Update Types.  This is used to set different auto update types for a Window:

    The default for pybox is "Immediate".  The default for C++ Sagebox is "On"

    On -    The window will auto passively update every 10-20ms.  This means when any pybox display or GetEvent function is called and a window needs
            Updating, pybox will do it, but it is not guaranteed for code that lingers/loops after the last display function.  
            
            For most applications, pybox will update the window when necessary, since any waiting (i.e. ExitButton() or GetEvent()) function or
            display function (i.e. Write()) will update the window if the window needs it. 

            In loops that can take time, or without a pybox call of some sort, sometimes a pybox.Update() may
            be necessary to ensure the window is updated.

    Off -   The window will not be updated, and it is the program's responsibility to do so.
            This can be useful when redrawing the screen in a real-time setting, to avoid flashing.

    Immediate - Updates the screen after every single display operation.  This can be slow when a lot of data is put out to the screen, but it is
                guaranteed and the update status never needs to be managed.  This can be useful for putting out data from equipment, etc. 
                Also see 'OnTime'

    OnTime - The update is mixed with 'On' (which updates when a Pybox function see the window needs it) and a timer in the 25ms range.
             If Pybox has not updated the window on its own within 25ms, the timer set will instruct Pybox to do it immediately behind the scenes.
             This can be a good mode because it is fast and guaranteed, because the window is only updated every 10-20ms, with a follow-up if
            no Pybox functon was called in that time. 

            This mode can interfere with real-time displays, so setting the Update to either On or Off can be more streamlined in this type of application.
    """
    on           = 1      
    off          = 2
    immediate    = 3
    on_time      = 4

class CTextWidget :
    """
    Sagebox Widget Class. Provides a Text Widget for a window. See functions such as NewTextWidget() or DevText()

    Sagebox widgets are peristent text boxes on the screen.  They are usually transparent (i.e. only the text displays, but not
    the background) and blend in with the window.  

    As opposed to using the Window.Write() function, When output is put to the window or the window changes, the text widget remains.

    For a single-text item, you can use Text Widgets in a fire-and-forget fashion (i.e. you don't need to keep the returned object).

    For text that can change or to hide/show the widget, you can keep the object and use the Write() function. 

    """
    def __init__(self,_id) : self.__id = _id

    def write(self,text : str,*args,**kwargs) : 
        """
        Writes text to the widget.

        Text text is written to the widget based on the widget settings, such as centered or right-justified text. 
        The text is written in the color, background color, and font specified when the widget was created, unless options
        are added to the write function call.

        As with window.write, different fonts and colors may be used and mixed with the text. 

        Example:    widget.write("This is the widget text)
                    widget.write("This is the {r}widget{} text")    -> Writes the word "widget" in read
                    widget.write(f"This is count #{count})          -> Writes the variable <count> with the string
                    widget.write(f"This is count #{{g}}{count}")    -> Writes the variable count in green
                    widget.write(f"{{10}}This is count #{{}}{{g}}{count}")
                        --> this writes the text "This is count" in a smaller font sized 10, with Count in the text widgets default font to look bigger.

            Note: In formatted strings an extra "{" and "}" must be used to specify controls, i.e. {r} becomes {{r}} and {} becomes {{}}.  This allows
            the passing of control items through Python formatted strings.

           Available Embedded controls in the text:

           - {<color>}      -> Sets a text color, i.e. {r} or {red}, {blue} or {b}, {forestgreen}, <defined color with MakeColor())>
                                Example: "this {r}string{} is in the color red"
            - {fontsize}    -> Sets a font size
                                Example: "this {20}string{} is written in size 20 font"
                                note:  The text widget must be created with the largest fonts size needed.
            - {x=<value>}   -> Sets the write position.
                                Example: "Value: {x=50}is at location 50"

            A limited set of pybox options and/or keywords can also be used, such as opt.bgcolor,opt.font, etc. 
            See Window.write() for more information about options.  Typically, fgColor(), bgColor(), font() can be used rather then using the {} formatting.          
        """
        return _pybox.TextWidgetWrite(self.__id,text,*args,**kwargs)

class _ColorSelector :
    """    
    Color Selector widget, either in the current window or as a popup window. 
        
    With the color selector, you can select an RGB color using the wheel or input boxes next to the wheel itself. 
    A color rectangle is shown with the currently selected color.
        
    color_selector returns a _ColorSelector object which can be used to look at changes in the color wheel in the window's main event loop. 
        
    See the _ColorSelector object functions for more information.
        
    Parameters:
        
    - at          \t - Where to put the Color Selector (in the window or as a popup).  If this is not used, the Color Selector is placed automatically.

    Keywords usable when creating the Color Selector:

    - Popup         \t - When true (i.e. Popup=True), the window pops up as a separate window.  Otherwise, it is placed in the current window at the location specified
    - Title         \t - Sets a title displayed in the window's top bar area, such as title="This is the window title".  Otherwise a default title is used.
    - x,y           \t - 'x' and 'y' keywords can be used in place of using the 'at' parameter, i.e. x=500, y=200 instead of (500,200) or at=(500,200)
  
    examples:\t - color_sel = mywin.color_selector(at=(500,200),popup=True)     --> Opens a Color Selector window as an individual window on the screen at x=500 and y=200
    - color_sel = mywin.color_selector(at=(500,200))     --> Opens a Color Selector window inside the window 'mywin, at window location x=500 and y=200
    - color_sel = pybox.color_selector(at=500,200)  --> Opens the same type of window, but as a pybox function without a parent window.
        
    - while mywin.GetEvent() : if (color_sel.value_changed()) print("Color value = ",color_sel.get_rgb_value()) --> prints values as the wheel is moved.
    """
    def __init__(self,_id) : self.__id = _id
    
    def value_changed(self,**kwargs) -> bool :
        """
        Returns true of the value has changed since the last time called (i.e. the Mouse Wheel was moved, or a value entered in the input boxes)
      
        Useful Keywords:
        
        - Peek         \t - When true (i.e. Peek=True), the 'value changed' status is not reset and will always read 'true' (when a change has occurred) until a call occurs without the 'Peek' keyword set to True
        
        example: if color_sel.value_changed() : new_color = color_sel.get_rgb_value();
        """
        return _pybox.ColorSelector_ValueChanged(self.__id,**kwargs)
    
    def get_rgb_value(self) -> RgbColor :
        """
        Returns the current selected color in the Color Selector as an RgbColor value. 
        
        This can be used after checking for a value change, such as: 
        
        \t -if color_sel.value_changed() : new_color = color_sel.get_rgb_value();
        
        - See: get_array_value() to return the value as a numpy integer array rather than an RgbColor value. 
        """
        value = _pybox.ColorSelector_GetRGBValue(self.__id);
        return RgbColor(value[0],value[1],value[2]);   

    def get_array_value(self) -> numpy.ndarray :
        """
        Returns the currently selected color in the Color Selector as an numpy integer array. 
        
        This can be used after checking for a value change, such as: 
        
        \t -if color_sel.value_changed() : new_color = color_sel.get_array_value();
        
        - See: get_rgb_value() to return the value as an RgbColor value rather than a numpy integer array. 
        """
        value = _pybox.ColorSelector_GetRGBValue(self.__id);
        return numpy.array(value);

    def set_rgb_value(self,RgbValue) -> bool :
        """
        Sets the RGB value of the currently color selection in the Color Selector.
        
        When set_rgb_value() sets an RGB value, the color wheel, input boxes, and color rectangle in the Color Selector Window will change accordingly.
        
        - Color values may be RgbColor values, lists, tuples, or numpy arrays with 3 values representing red, green and blue (from 0-255)
        
        Examples:\t - color_sel.set_rgb_value((0,255,0)) --> Set Green
        - color_sel.set_rgb_value(PanColor.ForestGreen()) --> Set forestgreen  (example used with previous "from pybox import PanColor")
        """
        return _pybox.ColorSelector_SetRGBValue(self.__id,RgbValue);

    def set_location(self,at = None,**kwargs) -> bool :
        """
        Set the physical location of the Color Selector. 
        
        When the Color Selector window is a popup, this sets the popup window to the coordinates given.
        When the Color Selector window is embedded in the window, the location will be set within the window.
        
        Examples:\t - color_sel.SetLocation((500,200))
        - color_sel.SetLocation(x=500,y=200)
        """
        return _pybox.ColorSelector_SetLocation(self.__id,opt.at(at),**kwargs);

    def show(self,show : bool = True) -> bool :
        """
        Shows (or Hides) the Color Selector. 
        
        If the Color Selector is hidden from view, Show() will re-show the window. 
        
        If the Color Selector is a popup window, the entire window disappears.
        If the Color Selected is not a popup window, the color selector disappears from the window until shown again.
        
        - The 'show' parameter may be set to 'False' (i.e. color_sel.show(False) to reverse the command and hide the window instead)
        """
        return _pybox.ColorSelector_Show(self.__id,show);

    def hide(self,hide : bool = True) -> bool :
        """
        Hides (or Shows) the Color Selector. 
        
        If the Color Selector is visible, Hide() will hide it from view.
        
        If the Color Selector is a popup window, the entire window reappear.
        If the Color Selected is not a popup window, the color selector resappears embedded in the window in its current/previous location
        
        - The 'hide' parameter may be set to 'True' (i.e. color_sel.show(True) to reverse the command and show the window instead)
        """
        return _pybox.ColorSelector_Hide(self.__id,hide);

    def ok_pressed(self,**kwargs) -> bool :
        """
        Returns True if the OK button was pressed (popup-window mode only). 
        
        This can be used in an event-loop to determine when the OK button is pressed vs. the Cancel button or a general window closure.
        
        - Also see: cancel_pressed() and window_closed() 
        
        Useful Keywords:
        
        - Peek         \t - When true (i.e. Peek=True), the 'ok_pressed' status is not reset and will always read 'True' (when a change has occurred) until a call occurs without the 'Peek' keyword set to True
        
        Example: if color_sel.ok_pressed() : print("Ok button was pressed")
        
        """
        return _pybox.ColorSelector_OkPressed(self.__id,**kwargs);

    def cancel_pressed(self,**kwargs) -> bool :
        """
        Returns True if the Cancel button was pressed (popup-window mode only). 
        
        This can be used in an event-loop to determine when the Cancel button is pressed or the Window was closed (by presing the upper-right 'x' button, or ALT-F4).
        
        - Also see: ok_pressed() and window_closed()
        - note: cancel_pressed() can be used to check when the window is closed by pressing Alt-F4 or by using the 'X' button (in the upper-right).\
 In this case, a cancel is issued to the window, resulting in cancel_pressed() returning true as the window is closed.
        
        Useful Keywords:
        
        - Peek         \t - When true (i.e. Peek=True), the 'ok_pressed' status is not reset and will always read 'True' (when a change has occurred) until a call occurs without the 'Peek' keyword set to True
        
        Example: if color_sel.cancel_pressed() : print("Cancel button was pressed or Window was closed.")
        
        """
        return _pybox.ColorSelector_CancelPressed(self.__id,**kwargs);

    def window_closed(self,**kwargs) -> bool :
        """
        Returns True if the Window was closed (popup-window mode only). 
        
        This can be used in an event-loop to determine if the window was closed by the user.  When window_closed() returns True, this means the window was closed \
without pressing any of the buttons, representing a cancel button press at the same time.
        
        - Also see: ok_pressed() and cancel_pressed()
        - note: cancel_pressed() can be used to check when the window is closed by pressing Alt-F4 or by using the 'X' button (in the upper-right).\
 In this case, a cancel is issued to the window, resulting in cancel_pressed() returning true as the window is closed.
        
        Useful Keywords:
        
        - Peek         \t - When true (i.e. Peek=True), the 'ok_pressed' status is not reset and will always read 'True' (when a change has occurred) until a call occurs without the 'Peek' keyword set to True
        
        Example: if color_sel.window_closed() : print("Window was closed by the user.")
        
        """
        return _pybox.ColorSelector_WindowClosed(self.__id,**kwargs);

    def disable_close(self,disable : bool = True) -> bool :
        """
        This disables the ability to close the Color Selector Window (popup-window mode only) by pressing ALT-F4 or pressing the 'X' close button in the upper-right of the window.
        
        By default, the user can close the window by pressing the ALT-F4 or upper-right 'X' button.
        
        - The window can be restored by using the Show() function if it is closed by the user.
        - When closed by the user without pressing the Ok or Cancel button, a window_closed() and cancel_pressed() will both return True
        - When close is disabled, no actions are taken when the user attempts to close the window and the window remains open
        - use diable_close(False) to re-enable the ability for the user to close the window manually.
        """
        return _pybox.ColorSelector_DisableClose(self.__id,disable);

class _ColorWheel :
    """    
    Color Wheel widget, put into the existing window as a single color wheel with no other controls but the wheel itself. 
        
    With the color selector, you can select an RGB color using the wheel or input boxes next to the wheel itself. 
    A color rectangle is shown with the currently selected color.
        
    color_wheel returns a _ColorWheel object which can be used to look at changes in the color wheel in the window's main event loop. 
        
    See the _ColorWheel object functions for more information.
        
    Parameters:
        
    - at          \t - Where to put the Color Selector (in the window or as a popup).  If this is not used, the Color Selector is placed automatically.

    Keywords usable when creating the Color Selector:

    - x,y           \t - 'x' and 'y' keywords can be used in place of using the 'at' parameter, i.e. x=500, y=200 instead of (500,200) or at=(500,200)
  
    example:\t - color_wheel = mywin.color_wheel((500,200))     --> Opens a Color Wheel window in the window at (500,200)
        
    - while mywin.GetEvent() : if (color_wheel.value_changed()) print("Color value = ",color_wheel.get_rgb_value()) --> prints values as the wheel is moved.
    """
    def __init__(self,_id) : self.__id = _id
    
    def value_changed(self,**kwargs) -> bool :
        """
        Returns true of the value has changed since the last time called (i.e. the Mouse Wheel was moved, or a value entered in the input boxes)
      
        Useful Keywords:
        
        - Peek         \t - When true (i.e. Peek=True), the 'value changed' status is not reset and will always read 'true' (when a change has occurred) until a call occurs without the 'Peek' keyword set to True
        
        example: if color_wheel.value_changed() : new_color = color_wheel.get_rgb_value();
        """
        return _pybox.ColorWheel_ValueChanged(self.__id,**kwargs)
    
    def get_rgb_value(self) -> RgbColor :
        """
        Returns the currently selected color in the Color Wheel as an RgbColor value. 
        
        This can be used after checking for a value change, such as: 
        
        \t -if color_wheel.value_changed() : new_color = color_wheel.get_rgb_value();
        
        - See: get_array_value() to return the value as a numpy integer array rather than an RgbColor value. 
        """
        value = _pybox.ColorWheel_GetRGBValue(self.__id);
        return RgbColor(value[0],value[1],value[2]);   

    def get_array_value(self) -> numpy.ndarray :
        """
        Returns the currently selected color in the Color Wheel as an numpy integer array. 
        
        This can be used after checking for a value change, such as: 
        
        \t -if color_wheel.value_changed() : new_color = color_wheel.get_array_value();
        
        - See: get_rgb_value() to return the value as an RgbColor value rather than a numpy integer array. 
        """
        value = _pybox.ColorWheel_GetRGBValue(self.__id);
        return numpy.array(value);

    def set_rgb_value(self,RgbValue) -> bool :
        """
        Sets the RGB value of the current color selection in the Color Wheel.
                
        - Color values may be RgbColor values, lists, tuples, or numpy arrays with 3 values representing red, green and blue (from 0-255)
        
        Examples:\t - color_wheel.set_rgb_value((0,255,0)) --> Set Green
        - color_wheel.set_rgb_value(PanColor.ForestGreen()) --> Set forestgreen  (example used with previous "from pybox import PanColor")
        """
        return _pybox.ColorWheel_SetRGBValue(self.__id,RgbValue);

    def set_location(self,at = None,**kwargs) -> bool :
        """
        Set the physical location of the Color Wheel. 
        
        Examples:\t - color_wheel.SetLocation((500,200))
        - color_wheel.SetLocation(x=500,y=200)
        """
        return _pybox.ColorWheel_SetLocation(self.__id,opt.at(at),**kwargs);

    def show(self,show : bool = True) -> bool :
        """
        Shows (or Hides) the Color Wheel. 
        
        If the Color Wheel is hidden from view, Show() will re-show the Color Selector. 
        
        - The 'show' parameter may be set to 'False' (i.e. color_sel.show(False) to reverse the command and hide the Color Wheel instead)
        """
        return _pybox.ColorWheel_Show(self.__id,show);

    def hide(self,hide : bool = True) -> bool :
        """
        Hides (or Shows) the Color Wheel. 
        
        If the Color Wheel is visible, Hide() will hide it from view.
        
        - The 'hide' parameter may be set to 'True' (i.e. color_sel.show(True) to reverse the command and show the Color Wheel instead)
        """
        return _pybox.ColorWheel_Hide(self.__id,hide);

class Window :
    """
    Pybox Window Class

    With a Pybox window you can do many things.  A Pybox window is basically a simple window that acts as a canvas where you
    can draw items, place text in different colors and fonts.  You can also place and use controls. 

    You can open as many Windows as you want, as well as create child windows inside of the window itself.
    """
    def __init__(self,_id : int) : 
        self.__id           = _id
        #self.__pointer      = _pybox.WindowGetWindowPointer(_id)
        self.draw           = self.__WinDraw(self)
        self.console        = self.__WinConsole(self)

    class __WinConsole :
        """
        """
        def __init__(self, outer): self.__id = outer._Window__id

        def get_integer(self,text = None,*args,**kwargs) -> int :
            """
            """
            return _pybox.WinConsoleGetNumber(self.__id,text,*args,**kwargs)
        def get_float(self,text = None,*args,**kwargs) -> float :
            """
            """
            return _pybox.WinConsoleGetFloat(self.__id,text,*args,**kwargs)

    class __WinDraw :
        """
        The WinDraw class contains drawing functions that can be used in pybox.  Many functions can be found in the regular window class. 
        
        Drawing functions are collected here for easier access and so that typing "draw." after your window name will list all functions, i.e. "MyWindow.draw"

        Drawing functions are split between 'fast' functions and regular drawing functions (i.e. "CircleFast" vs "Circle"). 

        The 'fast' functions are about 10x faster to draw and can be useful in drawing various graphics where quality is not the largest issue.

        Other functions use the GDI functions and are more compatible with the upcoming GPU-based functions.  Most of these functions support opacity levels
        as well as transformations.

        See the individual function descriptions for more information
        """
        def __init__(self, outer) : 
            self.__id = outer._Window__id
            #self.pointer = outer._Window__pointer

        #
        # Window WinDraw class functions Class Functions
        # 
        
        def get_hue_color(self,deg : int) -> RgbColor :
            """
            Returns a bright, primary color based on the input value. 

            get_hue_color() is a quick way to grab a bright color as specific value or in a random manner. 

            For example, get_hue_color(0) returns a bright red, where get_hue_color(60) returns a bright magenta, and 
            get_hue_color(120) returns a bright Blue, and so-forth.

            Parameters

            - deg      \t -- Input degrees, from 0-360. 

            Notable Values:

            - 0     \t --Red.  Same as GetHueColor(360)
            - 60    \t --Purple / Magenta
            - 120   \t --Blue
            - 180   \t --Cyan
            - 240   \t --Green
            - 300   \t --Yellow

            Returns: A pybox RgbColor object consisting of a Red, Green, and Blue value
            """
            color = _pybox.FromHSL(deg)
            return RgbColor(color[0],color[1],color[2])

        def set_opacity(self,opacity) -> bool :
            """
            Sets the opacity of the drawing functions such as Circle, Ellipse, Polygon, Line, etc. 

            A 100% opacity is fully opaque, where a 0% opacity is fully transparent (i.e. not visible). 

            Opacity works only with regular drawing functions and not the 'fast' functions.  When set to a value, this will persist
            for all drawing functions.

            Parameters:

            - opacity         \t -- Opacity from 0-100 (or 0-255 if 'byValue' is True)
                            
            """
            return _pybox.DrawSetDrawOpacity(self.__id,opacity)

        def get_opacity(self) -> int :
            """
            Returns the opacity value set for drawing functions such as Circle, Ellipse, Polygon, Line, etc.

            The value is returned as a 0-255 value, where 0 is completely transparent and 255 is fully opaque (default).

            See SetOpacity() to set the opacity of drawing functions.
            """
            return _pybox.DrawGetDrawOpacity(self.__id)

        def rotate_transform(self,angle) -> bool :
            """
            Sets a rotational transform for drawing operations such as Circle, Ellipse, Polygon, Line, etc.

            After set, any object drawn (i.e. circle, rectangles, etc.) will be drawn rotated to the angle specified. 

            Transforms only work with regular drawing functions and not the 'fast' functions.  

            Note: Transforms are additive.  You must use ResetTransform() to repeat transform blocks.  Otherwise they will 
            add on to each other with odd results. 

            Parameters

            - Angle         \t -- Angle to rotate drawn objects, in degrees (0-360)

            Example:
                MyWindow.Draw.rotate_transform(60)
                MyWindow.Draw.rectangle(x,y,width,height,color)
                ... other drawing functions

                MyWindow.Draw.reset_transform()      # remove transforms. 

            """
            return _pybox.DrawRotateTransform(self.__id,angle)

        def reset_transform(self) -> bool : 
            """
            Resets all transforms associated with the current graphics set. 

            See RotateTransform() and ResetTransform() for more information.
            """
            return _pybox.DrawResetTransform(self.__id)

        def translate_transform(self,x,y) -> bool : 
            """
            Sets a translation transform for drawn objects such as a Circle, Ellipse, Polygon, Line, etc.
            See translate_transform_l() to use a list, tuple, or array to specify the location.

            This causes the point (0,0) to be translated as (x,y) value. 

            This is useful when drawing multiple objects with the same relative center without the need to specify
            different coordinates for each object.

            Parameters:

            - x,y         \t -- x,y coordinates of new center. 

            Transforms only work with regular drawing functions and not the 'fast' functions.  

            Note: Transforms are additive.  You must use ResetTransform() to repeat transform blocks.  Otherwise they will 
            add on to each other with odd results. 

            Example:

            Example:
                MyWindow.draw.translate_transform(400,200)
                MyWindow.draw.circle(0,0,200,"red")     # draws circle at 400,200 even though 0,0 is specified.

                ... other drawing functions

                MyWindow.Draw.reset_transform()      # remove transforms. 

            """
            return _pybox.DrawTranslateTransform(self.__id,x,y)

        def translate_transform_l(self,at : list) -> bool : 
            """
            Sets a translation transform for drawn objects such as a Circle, Ellipse, Polygon, Line, etc.
            See translate_transform() specify individual values for x,y

            This causes the point (0,0) to be translated as (x,y) value. 

            This is useful when drawing multiple objects with the same relative center without the need to specify
            different coordinates for each object.

            Parameters:

            - at         \t -- x,y coordinates of new center. 

            Transforms only work with regular drawing functions and not the 'fast' functions.  

            Note: Transforms are additive.  You must use ResetTransform() to repeat transform blocks.  Otherwise they will 
            add on to each other with odd results. 

            Example:

            Example:
                MyWindow.Draw.TranslateTransformL(400,200)
                MyWindow.Draw.Circle(0,0,200,"red")     # draws circle at 400,200 even though 0,0 is specified.

                ... other drawing functions

                MyWindow.Draw.ResetTransform()      # remove transforms. 

            """            
            return _pybox.DrawTranslateTransform(self.__id,at[0],at[1])

        def set_pen_size(self,pen_size : int) :
            """
            Sets the size of the drawing pen, which is the size of lines and shape borders (i.e. circles, squares, etc.)

            Parameters:

            \t -- pen_size               \t -- Size of the pen.  Currently an integer value, but will accept floating-point in a future version.

            Example:

                    MyWin.set_pen_size(10)
                    MyWin.draw.Ellipse(500,500,200,400,"yellow")

                    where: if set_pen_size() is not called prior to DrawEllipse(), the current pen size is used.

            The default pen_size is 1.

            Note: You can specify the pen size in all functions that use it, such as: 

            \t -- MyWin.draw.ellipse(500,500,200,400,"yellow",10). 

            set_pen_size() will set the pen size globally and will use that pen size for all functions when the pen size is omitted.

            When the Pen Size is included in a function, the pen size is used only for that function.

            """
            return _pybox.WindowSetPenSize(self.__id,pen_size)

        #
        # Quadrangle Functions
        #

        def fill_quadrangle_fast(self,p1 : list, p2 : list, p3 : list,p4 : list,inside_color,border_color = 0,pen_size : int = 0) :
            """
            Draws a 'fast' filled Quadrangle on the screen with axis points at p1, p2, p3, and p4. 

            See quadrangle_fast() to draw an open/wireframe Quadrangle vs. a filled Quadrangle. 

            This drawing function is a 'fast' function that does not use anti-aliasing and is about 10x faster than
            non-fast drawing functions.  These functions are useful for general drawing and do not respond to opacity or transformations.

            Parameters

            \t -- p1,p2,p3,p4     \t -- Location of the 3 axes of the quadrangle
            \t -- inside_color     \t -- Color of the interior of the quadrangle
            \t -- border_color     \t -- [optional] Color if the outside edge of the quadrangle (based on the current Pen Size).  When omitted, the entire quadrangle is drawn the color
                                    \t -of the inside_color.  See: set_pen_size() to set the thickness of the border when using border_color.
            \t -- pen_size         \t -- [optional] Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 

            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:

                \t -p1 = (300,300)
                \t -p2 = (200,500)
                \t -p3 = (400,500)
                \t -p4 = (500,600)

                window.draw.fill_quadrangle_fast(p1,p2,p3,p4,"yellow","red")
                window.draw.fill_quadrangle_fast(p1,p2,p3,p4,"yellow",6)

            """
            return _pybox.WindowDrawQuadrangleFast(self.__id,p1,p2,p3,p4,inside_color,border_color,pen_size,False)

        def quadrangle_fast(self,p1 : list, p2 : list, p3 : list,p4 : list,color,pen_size : int = 0) :
            """
            Draws a 'fast' open/wireframe Quadrangle on the screen with axis points at p1, p2, p3, and p4. 

            See fill_quadrangle_fast() to draw an filled Quandrangle vs. an open/wireframe Quadrangle.

            This drawing function is a 'fast' function that does not use anti-aliasing and is about 10x faster than
            non-fast drawing functions.  These functions are useful for general drawing and do not respond to opacity or transformations.

            Parameters

            \t -- p1,p2,p3,p4     \t -- Location of the 3 axes of the quadrangle
            \t -- inside_color     \t -- Color of the interior of the quadrangle
            \t -- border_color     \t -- [optional] Color if the outside edge of the quadrangle (based on the current Pen Size).  When omitted, the entire quadrangle is drawn the color
                                    \t -of the inside_color.  See: set_pen_size() to set the thickness of the border when using border_color.
            \t -- pen_size         \t -- [optional] Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 

            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

                \t -p1 = (300,300)
                \t -p2 = (200,500)
                \t -p3 = (400,500)
                \t -p4 = (500,600)

                window.draw.quadrangle_fast(p1,p2,p3,p4,"red")
                window.draw.quadrangle_fast(p1,p2,p3,p4,"yellow",6)

            """
            return _pybox.WindowDrawQuadrangleFast(self.__id,p1,p2,p3,p4,color,color,pen_size,True)

        # HR Quadrangle Functions

        def fill_quadrangle(self,p1 : list, p2 : list, p3 : list,p4 : list,inside_color,**kwargs) :
            """
            Draws a filled Quadrangle on the screen with axis points at p1, p2, p3, and p4. 

            See quadrangle() to draw an open/wireframe Quadrangle vs. a filled Quadrangle. 

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            Hint: use an odd-size pen_size for sharper edges.

            Parameters

            \t -- p1,p2,p3,p4     \t -- Location of the 3 axes of the quadrangle
            \t -- inside_color     \t -- Color of the interior of the quadrangle

            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_color   \t -- Color if the outside edge of the quadrangle (based on the current Pen Size).  When omitted, the entire quadrangle is drawn the color
                                    \t -of the inside_color.  See: set_pen_size() to set the thickness of the border when using border_color.
            - pen_size         \t -- Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:

                \t -p1 = (300,300)
                \t -p2 = (200,500)
                \t -p3 = (400,500)
                \t -p4 = (500,600)

                window.draw.fill_quadrangle(p1,p2,p3,p4,"yellow",pen_color="red")
                window.draw.fill_quadrangle(p1,p2,p3,p4,"yellow",pen_size=6)

            """
            return _pybox.WindowDrawQuadrangle(self.__id,p1,p2,p3,p4,inside_color,False,**kwargs)

        def quadrangle(self,p1 : list, p2 : list, p3 : list,p4 : list,color,**kwargs) :
            """
            Draws a an open/wireframe Quadrangle on the screen with axis points at p1, p2, p3, and p4. 

            See fill_quadrangle() to draw a filled Quadrangle vs an open/wireframe Quadrangle.

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            Hint: use an odd-size pen_size for sharper edges.

            Parameters

            \t -- p1,p2,p3,p4     \t -- Location of the 3 axes of the quadrangle
            \t -- inside_color     \t -- Color of the interior of the quadrangle
            \t -- pen_color     \t -- [optional] Color if the outside edge of the quadrangle (based on the current Pen Size).  When omitted, the entire quadrangle is drawn the color
                                    \t -of the inside_color.  See: set_pen_size() to set the thickness of the border when using pen_color.

            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_size         \t -- Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
                                    
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:

                \t -p1 = (300,300)
                \t -p2 = (200,500)
                \t -p3 = (400,500)
                \t -p4 = (500,600)

                window.draw.quadrangle(p1,p2,p3,p4,"red")
                window.draw.quadrangle(p1,p2,p3,p4,"yellow",pen_size=6)

            """
            return _pybox.WindowDrawQuadrangle(self.__id,p1,p2,p3,p4,color,True,**kwargs)
        
        #
        # Triangle Functions
        #

        def fill_triangle_fast(self,p1 : list, p2 : list, p3 : list,inside_color,border_color = 0,pen_size : int = 0) :
            """
            Draws a 'fast' filled Triangle on the screen with axis points at p1, p2, and p3. 

            See triangle_fast() to draw an open/wireframe Triangle vs. a filled Triangle. 

            This drawing function is a 'fast' function that does not use anti-aliasing and is about 10x faster than
            non-fast drawing functions.  These functions are useful for general drawing and do not respond to opacity or transformations.

            Parameters

            \t -- p1,p2,p3        \t -- Location of the 3 axes of the triangle
            \t -- inside_color     \t -- Color of the interior of the triangle
            \t -- border_color     \t -- [optional] Color if the outside edge of the triangle (based on the current Pen Size).  When omitted, the entire triangle is drawn the color
                                    \t -of the inside_color.  See: set_pen_size() to set the thickness of the border when using border_color.
            \t -- pen_size         \t -- [optional] Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 

            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:

                \t -p1 = (300,300)
                \t -p2 = (200,500)
                \t -p3 = (400,500)

                window.draw.fill_triangle_fast(p1,p2,p3,"yellow","red")
                window.draw.fill_triangle_fast(p1,p2,p3,"yellow",6)

            """
            return _pybox.WindowDrawFilledTriangleFast(self.__id,p1,p2,p3,inside_color,border_color,pen_size)

        def triangle_fast(self,p1 : list, p2 : list, p3 : list,color,pen_size : int = 0) :
            """
            Draws a 'fast' open/wireframe Triangle on the screen with axis points at p1, p2, and p3.

            See fill_triangle_fast() to draw an filled Triangle vs. an open/wireframe Triangle.

            This drawing function is a 'fast' function that does not use anti-aliasing and is about 10x faster than
            non-fast drawing functions.  These functions are useful for general drawing and do not respond to opacity or transformations.

            Parameters

            \t -- p1,p2,p3        \t -- Location of the 3 axes of the triangle
            \t -- color           \t -- Color of the interior of the triangle
            \t -- pen_size         \t -- [optional] Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 

            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:

                \t -p1 = (300,300)
                \t -p2 = (200,500)
                \t -p3 = (400,500)

                window.draw.TriangleFast(p1,p2,p3,"red")
                window.draw.TriangleFast(p1,p2,p3,"yellow",6)

            """
            return _pybox.WindowDrawTriangleFast(self.__id,p1,p2,p3,color,color,pen_size)

        # HR Triangles

        def fill_triangle(self,p1 : list, p2 : list, p3 : list,inside_color,**kwargs) :
            """
            Draws a filled Triangle on the screen with axis points at p1, p2, and p3 

            See triangle() to draw an open/wireframe Triangle vs. a filled Triangle. 

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            Hint: use an odd-size pen_size for sharper edges.

            Parameters

            \t -- p1,p2,p3        \t -- Location of the 3 axes of the triangle
            \t -- inside_color     \t -- Color of the interior of the triangle

            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_color   \t -- Color if the outside edge of the triangle (based on the current Pen Size).  When omitted, the entire triangle is drawn the color
                                    \t -of the inside_color.  See: set_pen_size() to set the thickness of the border when using pen_color.
            - pen_size         \t -- Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:

                \t -p1 = (300,300)
                \t -p2 = (200,500)
                \t -p3 = (400,500)

                window.draw.fill_triangle(p1,p2,p3,"yellow",pen_color="red")
                window.draw.fill_triangle(p1,p2,p3,"yellow",pen_size=6)

            """
            return _pybox.WindowDrawTriangle(self.__id,p1,p2,p3,inside_color,False,**kwargs)
        def fill_triangle_test(self,p1 : list, p2 : list, p3 : list,inside_color,**kwargs) :
            return _pybox.WindowDrawTriangle_Test(self.pointer[0],self.pointer[1],p1,p2,p3,inside_color,False,**kwargs)

        def triangle(self,p1 : list, p2 : list, p3 : list,color,**kwargs) :
            """
            Draws a an open/wireframe Triangle on the screen with axis points at p1, p2, p3. 

            See fill_triangle() to draw a filled Triangle vs an open/wireframe Triangle.

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            Hint: use an odd-size pen_size for sharper edges.

            Parameters

            \t -- p1,p2,p3        \t -- Location of the 3 axes of the triangle
            \t -- color           \t -- Color of the interior of the triangle

            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_size         \t -- Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:

                \t -p1 = (300,300)
                \t -p2 = (200,500)
                \t -p3 = (400,500)

                window.draw.triangle(p1,p2,p3,"red")
                window.draw.triangle(p1,p2,p3,"yellow",pen_size=6)

            """
            return _pybox.WindowDrawTriangle(self.__id,p1,p2,p3,color,True,**kwargs)
        
        #
        # Rectangle Functions
        #

        def fill_rectangle_fast(self,x : int,y : int,width : int,height : int,inside_color,border_color = 0,pen_size : int = 0) : 
            """
            Draws a 'fast' filled Rectangle on the screen at starting point (x,y) with a width and height of (width,height)

            See rectangle_fast() to draw an open/wireframe Rectangle vs. a filled Rectangle. 
            See fill_rectangle_fast_l() to set the Rectangle location, width, and height using a tuple, list, or array

            This drawing function is a 'fast' function that does not use anti-aliasing and is about 10x faster than
            non-fast drawing functions.  These functions are useful for general drawing and do not respond to opacity or transformations.

            Parameters

            - x,y                   \t -- Location of the center of the rectangle in the window
            - width                \t -- Width (in pixels) of the rectangle
            - height               \t -- Width (in pixels) of the rectangle
            - inside_color   \t -- Color of the interior of the rectangle
            - border_color   \t -- [optional] Color if the outside edge of the rectangle (based on the current Pen Size).  When omitted, the entire rectangle is drawn the color
                                    \t -of the inside_color.  See: set_pen_size() to set the thickness of the border when using border_color.
            - pen_size         \t -- [optional] Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:
                            window.draw.fill_rectangle_fast(400,200,300,100,"red") 
                            window.draw.fill_rectangle_fast(400,200,300,100,"red","Green")       - Draws a Red rectangle with a green outer border (thickness of current pen size)
                            window.draw.fill_rectangle_fast(400,200,300,100,PanColor.ForestGreen())
                            window.draw.fill_rectangle_fast(400,200,300,100,MyColor,6)            - Sets a pen size of 6
                            window.draw.fill_rectangle_fast(400,200,300,100,pybox.RgbColor(0,255,0))         
            """
            return _pybox.WindowDrawFilledRectangleFast(self.__id,int(x),int(y),int(width),int(height),inside_color,border_color,pen_size)

        def fill_rectangle_fast_l(self,at : list,size : list,inside_color,border_color = 0,pen_size : int = 0) :
            """
            Draws a 'fast' filled Rectangle on the screen at starting point (x,y) with a width and height of (width,height)

            See rectangle_fast_l() to draw an open/wireframe Rectangle vs. a filled Rectangle. 
            See fill_rectangle_fast() to set the Rectangle location, width, and height using a separate values.

            This drawing function is a 'fast' function that does not use anti-aliasing and is about 10x faster than
            non-fast drawing functions.  These functions are useful for general drawing and do not respond to opacity or transformations.

            Parameters

            - at                \t -- (x,y) Location of the center of the rectangle in the window
            - size              \t -- (Width, Height), in pixels, of the rectangle
            - inside_color   \t -- Color of the interior of the rectangle
            - border_color   \t -- [optional] Color if the outside edge of the rectangle (based on the current Pen Size).  When omitted, the entire rectangle is drawn the color
                                    \t -of the inside_color.  See: set_pen_size() to set the thickness of the border when using border_color.
            - pen_size         \t -- [optional] Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:
                            window.draw.fill_rectangle_fast_l((400,200),(300,100),"red") 
                            window.draw.fill_rectangle_fast_l(Location,Size,"red","Green")            - Draws a Red rectangle with a green outer border (thickness of current pen size)
                            window.draw.fill_rectangle_fast_l((400,200),(300,100),PanColor.ForestGreen())
                            window.draw.fill_rectangle_fast_l((400,200),(300,100),MyColor,6)            - Sets a pen size of 6
                            window.draw.fill_rectangle_fast_l((400,200),(300,100),pybox.RgbColor(0,255,0))         
            """
            return _pybox.WindowDrawFilledRectangleFast(self.__id,int(at[0]),int(at[1]),int(size[0]),int(size[1]),inside_color,border_color,pen_size)

        def rectangle_fast(self,x : int,y : int,width : int,height : int,color,pen_size : int = 0) : 
            """
            Draws a 'fast' open/wireframe Rectangle on the screen at starting point (x,y) with a width and height of (width,height)

            See fill_rectangle_fast() to draw a filled Rectangle vs. an open/wireframe Rectangle.
            See rectangle_fast_l() to set the Rectangle location, width, and height using a tuple, list, or array

            This drawing function is a 'fast' function that does not use anti-aliasing and is about 10x faster than
            non-fast drawing functions.  These functions are useful for general drawing and do not respond to opacity or transformations.

            Parameters

            - x,y                   \t -- Location of the center of the rectangle in the window
            - width                \t -- Width (in pixels) of the rectangle
            - height               \t -- Width (in pixels) of the rectangle
            - color             \t -- Color of the interior of the rectangle
            - pen_size         \t -- [optional] Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:
                            window.draw.rectangle_fast(400,200,300,100,"red") 
                            window.draw.rectangle_fast(400,200,300,100,PanColor.ForestGreen())
                            window.draw.rectangle_fast(400,200,300,100,MyColor,6)            - Sets a pen size of 6
                            window.draw.rectangle_fast(400,200,300,100,pybox.RgbColor(0,255,0))         
            """
            return _pybox.WindowDrawRectangleFast(self.__id,int(x),int(y),width,height,color,color,pen_size)

        def rectangle_fast_l(self,at : list,size : list,color,pen_size : int = 0) :
            """
            Draws a 'fast' open/wireframe Rectangle on the screen at starting point (x,y) with a width and height of (width,height)

            See fill_rectangle_fast_l() to draw a filled Rectangle vs. an open/wireframe Rectangle.
            See rectangle_fast() to set the Rectangle location, width, and height using independent values.

            This drawing function is a 'fast' function that does not use anti-aliasing and is about 10x faster than
            non-fast drawing functions.  These functions are useful for general drawing and do not respond to opacity or transformations.

            Parameters

            - at                   \t -- (x,y) Location of the center of the rectangle in the window
            - size                \t -- (Width, Height), in pixels, of the rectangle
            - color             \t -- Color of the interior of the rectangle
            - pen_size         \t -- [optional] Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:
                            window.draw.rectangle_fast_l(400,200,300,100,"red") 
                            window.draw.rectangle_fast_l(location,size,300,100,PanColor.ForestGreen())
                            window.draw.rectangle_fast_l(400,200,300,100,MyColor,6)            - Sets a pen size of 6
                            window.draw.rectangle_fast_l(400,200,300,100,pybox.RgbColor(0,255,0))         
            """
            return _pybox.WindowDrawRectangleFast(self.__id,int(at[0]),int(at[1]),int(size[0]),int(size[1]),color,color,pen_size)

        # HR Rectangle Functions

        def fill_rectangle(self,x : int,y : int,width : int,height : int,inside_color,**kwargs) : 
            """
            Draws a filled Rectangle on the screen at starting point (x,y) with a width and height of (width,height)

            See rectangle() to draw an open/wireframe Rectangle vs. a filled Rectangle. 
            See fill_rectangle_l() to set the Rectangle location, width, and height using a separate values.

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            Hint: use an odd-size pen_size for sharper edges.

            Parameters

            - x,y                   \t -- Location of the center of the rectangle in the window
            - width                \t -- Width (in pixels) of the rectangle
            - height               \t -- Width (in pixels) of the rectangle
            - inside_color   \t -- Color of the interior of the rectangle

            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_color   \t -- Color if the outside edge of the rectangle (based on the current Pen Size).  When omitted, the entire rectangle is drawn the color
                                    \t -of the inside_color.  See: set_pen_size() to set the thickness of the border when using pen_color.
            - pen_size         \t -- Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:
                            window.draw.fill_rectangle(400,200,300,100,"red") 
                            window.draw.fill_rectangle(400,200,300,100,"red",pen_color="Green")       - Draws a Red rectangle with a green outer border (thickness of current pen size)
                            window.draw.fill_rectangle(400,200,300,100,PanColor.ForestGreen())
                            window.draw.fill_rectangle(400,200,300,100,MyColor,pen_size=6)            - Sets a pen size of 6   
                            window.draw.fill_rectangle(400,200,300,100,pybox.RgbColor(0,255,0))         
            """
            return _pybox.WindowDrawRectangle(self.__id,x,y,width,height,inside_color,False,**kwargs)

        def fill_rectangle_l(self,at : list,size : list,inside_color,**kwargs) :
            """
            Draws a filled Rectangle on the screen at starting point (x,y) with a width and height of (width,height)

            See rectangle() to draw an open/wireframe Rectangle vs. a filled Rectangle. 
            See fill_rectang() to set the Rectangle location, width, and height using independent values.

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            Hint: use an odd-size pen_size for sharper edges.

            Parameters

            - at                   \t -- (x,y) Location of the center of the rectangle in the window
            - size                \t -- (Width, Height), in pixels, of the rectangle
            - inside_color   \t -- Color of the interior of the rectangle

            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_color   \t -- Color if the outside edge of the rectangle (based on the current Pen Size).  When omitted, the entire rectangle is drawn the color
                                    \t -of the inside_color.  See: set_pen_size() to set the thickness of the border when using pen_color.
            - pen_size         \t -- Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:
                            window.draw.fill_rectangle_l((400,200),(300,100),"red") 
                            window.draw.fill_rectangle_l((400,200),(300,100),"red",pen_color="Green")      - Draws a Red rectangle with a green outer border (thickness of current pen size)
                            window.draw.fill_rectangle_l(Location,Size,PanColor.ForestGreen())
                            window.draw.fill_rectangle_l((400,200),(300,100),MyColor,pen_size=6)           - Sets a pen size of 6   
                            window.draw.fill_rectangle_l((400,200),(300,100),pybox.RgbColor(0,255,0))         
            """
            return _pybox.WindowDrawRectangle(self.__id,at[0],at[1],size[0],size[1],inside_color,False,**kwargs)

        def fill_rectangle_r(self,size_rect : list,inside_color,**kwargs) :
            """
            Draws a filled Rectangle on the screen at starting point (x,y) with a width and height of (width,height)

            See rectangle() to draw an open/wireframe Rectangle vs. a filled Rectangle. 
            See fill_rectangle() to set the Rectangle location, width, and height using independent values.

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            Hint: use an odd-size pen_size for sharper edges.

            Parameters

            - size_rect             \t -- (x,y,width,height) list or array specifying (x,y) and (width,height) of rectangle
            - inside_color      \t -- Color of the interior of the rectangle

            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_color   \t -- Color if the outside edge of the rectangle (based on the current Pen Size).  When omitted, the entire rectangle is drawn the color
                                    \t -of the inside_color.  See: set_pen_size() to set the thickness of the border when using pen_color.
            - pen_size         \t -- Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:
                            window.draw.fill_rectangle_r((400,200,300,100),"red") 
                            window.draw.fill_rectangle_r((400,200,300,100),"red",pen_color="Green")      - Draws a Red rectangle with a green outer border (thickness of current pen size)
                            window.draw.fill_rectangle_r(my_rect,PanColor.ForestGreen())
                            window.draw.fill_rectangle_r((400,200,300,100),MyColor,pen_size=6)           - Sets a pen size of 6   
                            window.draw.fill_rectangle_r((400,200,300,100),pybox.RgbColor(0,255,0))         
            """
            return _pybox.WindowDrawRectangle(self.__id,size_rect[0],size_rect[1],size_rect[2],size_rect[3],inside_color,False,**kwargs)
        
        def rectangle(self,x : int,y : int,width : int,height : int,color,**kwargs) : 
            """
            Draws an open/wireframe Rectangle on the screen at starting point (x,y) with a width and height of (width,height)

            See fill_rectangle() to draw a filled Rectangle va. an open/wireframe Rectangle.
            See rectangle_l() to set the Rectangle location, width, and height using a separate values.

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            Hint: use an odd-size pen_size for sharper edges.

            Parameters

            - x,y                   \t -- Location of the center of the rectangle in the window
            - width                \t -- Width (in pixels) of the rectangle
            - height               \t -- Width (in pixels) of the rectangle
            - color             \t -- Color of the interior of the rectangle

            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_size         \t -- Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:
                            window.draw.rectangle(400,200,300,100,"red") 
                            window.draw.rectangle(400,200,300,100,PanColor.ForestGreen())
                            window.draw.rectangle(400,200,300,100,MyColor,pen_size=6)        - Sets a pen size of 6   
                            window.draw.rectangle(400,200,300,100,pybox.RgbColor(0,255,0))         
            """
            return _pybox.WindowDrawRectangle(self.__id,x,y,width,height,color,True,**kwargs)

        def rectangle_l(self,at : list,size : list,color,**kwargs) :
            """
            Draws an open/wireframe Rectangle on the screen at starting point (x,y) with a width and height of (width,height)

            See fill_rectangle_l() to draw a filled Rectangle va. an open/wireframe Rectangle.
            See rectangle() to set the Rectangle location, width, and height using a independent values.

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            Hint: use an odd-size pen_size for sharper edges.

            Parameters

            - at                   \t -- (x,y) Location of the center of the rectangle in the window
            - size                \t -- (Width, Height), in pixels, of the rectangle
            - color             \t -- Color of the interior of the rectangle

            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_size         \t -- Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:
                            window.draw.rectangle_l((400,200),(300,100),"red") 
                            window.draw.rectangle_l((400,200),(300,100),PanColor.ForestGreen())
                            window.draw.rectangle_l(Location,Size,MyColor,pen_size=6)        - Sets a pen size of 6   
                            window.draw.rectangle_l((400,200),(300,100),pybox.RgbColor(0,255,0))         
            """
            return _pybox.WindowDrawRectangle(self.__id,at[0],at[1],size[0],size[1],color,True,**kwargs)
        
        def rectangle_r(self,size_rect : list,color,**kwargs) :
            """
            Draws an open/wireframe Rectangle on the screen at starting point (x,y) with a width and height of (width,height)

            See fill_rectangle_r() to draw a filled Rectangle va. an open/wireframe Rectangle.
            See rectangle() to set the Rectangle location, width, and height using a independent values.

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            Hint: use an odd-size pen_size for sharper edges.

            Parameters

            - size_rect             \t -- (x,y,width,height) list or array specifying (x,y) and (width,height) of rectangle
            - color             \t -- Color of the interior of the rectangle

            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_size         \t -- Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:
                            window.draw.rectangle_r((400,200,300,100),"red") 
                            window.draw.rectangle_r((400,200,300,100),PanColor.ForestGreen())
                            window.draw.rectangle_r(my_rect,MyColor,pen_size=6)        - Sets a pen size of 6   
                            window.draw.rectangle_r((400,200,300,100),pybox.RgbColor(0,255,0))         
            """
            return _pybox.WindowDrawRectangle(self.__id,size_rect[0],size_rect[1],size_rect[2],size_rect[3],color,True,**kwargs)

        #
        # Draw Ellipse Functions
        #

        def fill_ellipse_fast(self,x : int, y : int, radius_x : int, radius_y, inside_color, border_color = 0,pen_size : int = 0) :
            """
            Draws a 'fast' filled Ellipse on the screen at starting point (x,y) with a width and height of (radius_x, radius_y)

            See ellipse_fast() to draw an open/wireframe Ellipse vs. a filled Ellipse. 
            See fill_ellipse_fast_l() to set the Ellipse location, width, and height using a tuple, list, or array

            This drawing function is a 'fast' function that does not use anti-aliasing and is about 10x faster than
            non-fast drawing functions.  These functions are useful for general drawing and do not respond to opacity or transformations.

            Parameters

            - x,y                   \t -- Location of the center of the ellipse in the window
            - radius_x                \t -- Width/Radius (in pixels) of the ellipse in the X direction
            - radius_y               \t -- Height/Radius (in pixels) of the ellipse in the Y direction
            - inside_color   \t -- Color of the interior of the ellipse
            - border_color   \t -- [optional] Color if the outside edge of the ellipse (based on the current Pen Size).  When omitted, the entire ellipse is drawn the color
                                    \t -of the inside_color.  See: set_pen_size() to set the thickness of the border when using border_color.
            - pen_size         \t -- [optional] Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:
                            window.draw.fill_ellipse_fast(400,200,300,100,"red") 
                            window.draw.fill_ellipse_fast(400,200,300,100,"red","Green")       - Draws a Red ellipse with a green outer border (thickness of current pen size)
                            window.draw.fill_ellipse_fast(400,200,300,100,PanColor.ForestGreen())
                            window.draw.fill_ellipse_fast(400,200,300,100,MyColor,6)            - Sets a pen size of 6
                            window.draw.fill_ellipse_fast(400,200,300,100,pybox.RgbColor(0,255,0))         
            """          
            return _pybox.WindowDrawEllipseFast(self.__id,int(x),int(y),int(radius_x),int(radius_y),inside_color,border_color,pen_size,False)

        def fill_ellipse_fast_l(self,at : list, size : list, inside_color, border_color = 0,pen_size : int = 0) :
            """
            Draws a 'fast' filled Ellipse on the screen at starting point (x,y) with a width and height of (radius_x, radius_y)

            See ellipse_fast() to draw an open/wireframe Ellipse vs. a filled Ellipse. 
            See fill_ellipse_fast() to set the Ellipse location, width, and height using independent values.

            This drawing function is a 'fast' function that does not use anti-aliasing and is about 10x faster than
            non-fast drawing functions.  These functions are useful for general drawing and do not respond to opacity or transformations.

            Parameters

            - at                   \t -- (x,y) Location of the center of the rectangle in the window
            - size                \t -- (Width, Height), in pixels, of the rectangle
            - inside_color   \t -- Color of the interior of the ellipse
            - border_color   \t -- [optional] Color if the outside edge of the ellipse (based on the current Pen Size).  When omitted, the entire ellipse is drawn the color
                                    \t -of the inside_color.  See: set_pen_size() to set the thickness of the border when using border_color.
            - pen_size         \t -- [optional] Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:
                            window.draw.fill_ellipse_fast_l((400,200),(300,100),"red") 
                            window.draw.fill_ellipse_fast_l((400,200),(300,100),"red","Green")       - Draws a Red ellipse with a green outer border (thickness of current pen size)
                            window.draw.fill_ellipse_fast_l(Location,Size,PanColor.ForestGreen())
                            window.draw.fill_ellipse_fast_l((400,200),(300,100),MyColor,6)            - Sets a pen size of 6
                            window.draw.fill_ellipse_fast_l((400,200),(300,100),pybox.RgbColor(0,255,0))         
            """          
            return _pybox.WindowDrawEllipseFast(self.__id,int(at[0]),int(at[1]),int(size[0]),int(size[1]),inside_color,border_color,pen_size,False)

        def ellipse_fast(self,x : int, y : int, radius_x : int, radius_y, color,pen_size : int = 0) :
            """
            Draws a 'fast' open/wireframe Ellipse on the screen at starting point (x,y) with a width and height of (radius_x, radius_y)

            See fill_ellipse_fast() to draw a filled Ellipse vs. an open/wireframe Ellipse
            See ellipse_fast_l() to set the Ellipse location, width, and height using a tuple, list, or array

            This drawing function is a 'fast' function that does not use anti-aliasing and is about 10x faster than
            non-fast drawing functions.  These functions are useful for general drawing and do not respond to opacity or transformations.

            Parameters

            - x,y                   \t -- Location of the center of the ellipse in the window
            - radius_x                \t -- Width/Radius (in pixels) of the ellipse in the X direction
            - radius_y               \t -- Height/Radius (in pixels) of the ellipse in the Y direction
            - color                 \t -- Color of the ellipse
            - pen_size         \t -- [optional] Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:
                            window.draw.ellipse_fast(400,200,300,100,"red") 
                            window.draw.ellipse_fast(400,200,300,100,PanColor.ForestGreen())
                            window.draw.ellipse_fast(400,200,300,100,MyColor,6)            - Sets a pen size of 6
                            window.draw.ellipse_fast(400,200,300,100,pybox.RgbColor(0,255,0))         
            """               
            return _pybox.WindowDrawEllipseFast(self.__id,int(x),int(y),int(radius_x),int(radius_y),color,0,pen_size,True)

        def ellipse_fast_l(self,at : list, size : list, color,pen_size : int = 0) :
            """
            Draws a 'fast' open/wireframe Ellipse on the screen at starting point (x,y) with a width and height of (radius_x, radius_y)

            See fill_ellipse_fast_l() to draw a filled Ellipse vs. an open/wireframe Ellipse
            See ellipse_fast() to set the Ellipse location, width, and height using independent values.

            This drawing function is a 'fast' function that does not use anti-aliasing and is about 10x faster than
            non-fast drawing functions.  These functions are useful for general drawing and do not respond to opacity or transformations.

            Parameters

            - at                   \t -- (x,y) Location of the center of the rectangle in the window
            - size                \t -- (Width, Height), in pixels, of the rectangle
            - color                 \t -- Color of ellipse
            - pen_size         \t -- [optional] Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:
                            window.draw.ellipse_fast_l((400,200),(300,100),"red") 
                            window.draw.ellipse_fast_l((400,200),(300,100),PanColor.ForestGreen())
                            window.draw.ellipse_fast_l(Location,Size,MyColor,6)            - Sets a pen size of 6
                            window.draw.ellipse_fast_l((400,200),(300,100),pybox.RgbColor(0,255,0))         
            """                  
            return _pybox.WindowDrawEllipseFast(self.__id,int(at[0]),int(at[1]),int(size[0]),int(size[1]),color,0,pen_size,True)

        # HR Ellipse Functions

        def fill_ellipse(self,x, y, radius_x, radius_y, inside_color, **kwargs) :
            """
            Draws a filled Ellipse on the screen at starting point (x,y) with a width and height of (radius_x, radius_y)

            See ellipse() to draw an open/wireframe Ellipse vs. a filled Ellipse. 
            See fill_ellipse_l() to set the Ellipse location, width, and height using a tuple, list, or array

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            Hint: use an odd-size pen_size for sharper edges.

            Parameters

            - x,y                   \t -- Location of the center of the ellipse in the window
            - radius_x                \t -- Width/Radius (in pixels) of the ellipse in the X direction
            - radius_y               \t -- Height/Radius (in pixels) of the ellipse in the Y direction
            - inside_color   \t -- Color of the interior of the ellipse
            - pen_color   \t -- [optional] Color if the outside edge of the ellipse (based on the current Pen Size).  When omitted, the entire ellipse is drawn the color
                                    \t -of the inside_color.  See: set_pen_size() to set the thickness of the border when using pen_color.
            
            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_color   \t -- Color if the outside edge of the ellipse (based on the current Pen Size).  When omitted, the entire ellipse is drawn the color
                                    \t -of the inside_color.  See: set_pen_size() to set the thickness of the border when using pen_color.
            - pen_size         \t -- Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:
                            window.draw.fill_ellipse(400,200,300,100,"red") 
                            window.draw.fill_ellipse(400,200,300,100,"red",pen_color="Green")       - Draws a Red ellipse with a green outer border (thickness of current pen size)
                            window.draw.fill_ellipse(400,200,300,100,pen_color=PanColor.ForestGreen())
                            window.draw.fill_ellipse(400,200,300,100,MyColor,pen_size=6)            - Sets a pen size of 6
                            window.draw.fill_ellipse(400,200,300,100,pybox.RgbColor(0,255,0))         
            """               
            return _pybox.WindowDrawEllipse(self.__id,x,y,radius_x,radius_y,inside_color,False,**kwargs)

        def fill_ellipse_l(self,at : list, size : list, inside_color, **kwargs) :
            """
            Draws a filled Ellipse on the screen at starting point (x,y) with a width and height of (radius_x, radius_y)

            See ellipse_l() to draw an open/wireframe Ellipse vs. a filled Ellipse. 
            See fill_ellipse() to set the Ellipse location, width, and height using independent values.

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            Hint: use an odd-size pen_size for sharper edges.

            Parameters

            - at                   \t -- (x,y) Location of the center of the ellipse in the window
            - size                \t -- (Width, Height), in pixels, of the ellipse
            - inside_color   \t -- Color of the interior of the ellipse

            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_color   \t -- Color if the outside edge of the ellipse (based on the current Pen Size).  When omitted, the entire ellipse is drawn the color
                                    \t -of the inside_color.  See: set_pen_size() to set the thickness of the border when using pen_color.
            - pen_size         \t -- Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:
                            window.draw.fill_ellipse_l((400,200),(300,100),"red") 
                            window.draw.fill_ellipse_l((400,200),(300,100),PanColor.ForestGreen())
                            window.draw.fill_ellipse_l(Location,Size,MyColor,pen_size=6)            - Sets a pen size of 6
                            window.draw.fill_ellipse_l((400,200),(300,100),pybox.RgbColor(0,255,0))         
            """               
            return _pybox.WindowDrawEllipse(self.__id,at[0],at[1],size[0],size[1],inside_color,False,**kwargs)

        def fill_ellipse_r(self,size_rect : list, inside_color, **kwargs) :
            """
            Draws a filled Ellipse on the screen at starting point (x,y) with a width and height of (radius_x, radius_y)

            See ellipse_r() to draw an open/wireframe Ellipse vs. a filled Ellipse. 
            See fill_ellipse() to set the Ellipse location, width, and height using independent values.

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            Hint: use an odd-size pen_size for sharper edges.

            Parameters

            - size_rect             \t -- (x,y,width,height) list or array specifying (x,y) and (radius X ,radius Y) of ellipse
            - inside_color   \t -- Color of the interior of the ellipse

            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_color   \t -- Color if the outside edge of the ellipse (based on the current Pen Size).  When omitted, the entire ellipse is drawn the color
                                    \t -of the inside_color.  See: set_pen_size() to set the thickness of the border when using pen_color.
            - pen_size         \t -- Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:
                            window.draw.fill_ellipse_r(400,200,300,100),"red") 
                            window.draw.fill_ellipse_r(400,200,300,100),PanColor.ForestGreen())
                            window.draw.fill_ellipse_r(my_sizerect,Size,MyColor,pen_size=6)            - Sets a pen size of 6
                            window.draw.fill_ellipse_r(400,200,300,100),pybox.RgbColor(0,255,0))         
            """               
            return _pybox.WindowDrawEllipse(self.__id,size_rect[0],size_rect[1],size_rect[2],size_rect[3],inside_color,False,**kwargs)

        def ellipse(self,x, y, radius_x, radius_y, color,**kwargs) :
            """
            Draws an open/wireframe Ellipse on the screen at starting point (x,y) with a width and height of (radius_x, radius_y)

            See fill_ellipse() to draw a filled Ellipse vs. an open/wireframe Ellipse
            See ellipse_l() to set the Ellipse location, width, and height using a tuple, list, or array

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            Hint: use an odd-size pen_size for sharper edges.

            Parameters

            - x,y                   \t -- Location of the center of the ellipse in the window
            - radius_x                \t -- Width/Radius (in pixels) of the ellipse in the X direction
            - radius_y               \t -- Height/Radius (in pixels) of the ellipse in the Y direction
            - color             \t -- Color of the ellipse
            
            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_size         \t -- Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:
                            window.draw.ellipse(400,200,300,100,"red") 
                            window.draw.ellipse(400,200,300,100,PanColor.ForestGreen())
                            window.draw.ellipse(400,200,300,100,MyColor,pen_size=6)            - Sets a pen size of 6
                            window.draw.ellipse(400,200,300,100,pybox.RgbColor(0,255,0))         
            """             
            return _pybox.WindowDrawEllipse(self.__id,x,y,radius_x,radius_y,color,True,**kwargs)

        def ellipse_l(self,at : list, size : list, color,**kwargs) :
            """
            Draws an open/wireframe Ellipse on the screen at starting point (x,y) with a width and height of (radius_x, radius_y)

            See fill_ellipse_l() to draw a filled Ellipse vs. an open/wireframe Ellipse
            See ellipse() to set the Ellipse location, width, and height using independent values

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            Hint: use an odd-size pen_size for sharper edges.

            Parameters

            - at                   \t -- (x,y) Location of the center of the ellipse in the window
            - size                \t -- (Width, Height), in pixels, of the ellipse
            - color             \t -- Color of the ellipse
            
            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_size         \t -- Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:
                            window.draw.ellipse_l((400,200),(300,100),"red") 
                            window.draw.ellipse_l((400,200),(300,100),PanColor.ForestGreen())
                            window.draw.ellipse_l((Location,Size,MyColor,pen_size=6)            - Sets a pen size of 6
                            window.draw.ellipse_l((400,200),(300,100),pybox.RgbColor(0,255,0))         
            """                    
            return _pybox.WindowDrawEllipse(self.__id,at[0],at[1],size[0],size[1],color,True,**kwargs)     

        def ellipse_r(self,size_rect : list, color,**kwargs) :
            """
            Draws an open/wireframe Ellipse on the screen at starting point (x,y) with a width and height of (radius_x, radius_y)

            See fill_ellipse_r() to draw a filled Ellipse vs. an open/wireframe Ellipse
            See ellipse() to set the Ellipse location, width, and height using independent values

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            Hint: use an odd-size pen_size for sharper edges.

            Parameters

            - size_rect             \t -- (x,y,width,height) list or array specifying (x,y) and (radius X ,radius Y) of ellipse
            - color             \t -- Color of the ellipse
            
            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_size         \t -- Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:
                            window.draw.ellipse_r(400,200,300,100),"red") 
                            window.draw.ellipse_r(400,200,300,100),PanColor.ForestGreen())
                            window.draw.ellipse_r(my_size_rect,Size,MyColor,pen_size=6)            - Sets a pen size of 6
                            window.draw.ellipse_r(400,200,300,100),pybox.RgbColor(0,255,0))         
            """                    
            return _pybox.WindowDrawEllipse(self.__id,size_rect[0],size_rect[1],size_rect[2],size_rect[3],color,True,**kwargs)     

        #
        # Draw Circle Functions
        #

        def fill_circle_fast(self,x : int, y : int, radius : int, inside_color, border_color = 0,pen_size : int = 0) :
            """
            Draws a 'fast' filled Circle on the screen at starting point (x,y) with a width and height of (radius_x, radius_y)

            See circle_fast_l() to draw an open/wireframe Circle vs. a filled Circle. 
            See fill_circle_fast_l() to set the Circle location, width, and height using a tuple, list, or array

            This drawing function is a 'fast' function that does not use anti-aliasing and is about 10x faster than
            non-fast drawing functions.  These functions are useful for general drawing and do not respond to opacity or transformations.

            Parameters

            - x,y                   \t -- Location of the center of the circle in the window
            - radius                \t -- Radius (in pixels) of the circle.
            - inside_color   \t -- Color of the interior of the circle
            - border_color   \t -- [optional] Color if the outside edge of the circle (based on the current Pen Size).  When omitted, the entire circle is drawn the color
                                    \t -of the inside_color.  See: set_pen_size() to set the thickness of the border when using border_color.
            - pen_size         \t -- [optional] Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:
                            window.draw.fill_circle_fast(400,200,100,"red") 
                            window.draw.fill_circle_fast(400,200,100,"red","Green")       - Draws a Red circle with a green outer border (thickness of current pen size)
                            window.draw.fill_circle_fast(400,200,100,PanColor.ForestGreen())
                            window.draw.fill_circle_fast(400,200,100,MyColor,6)            - Sets a pen size of 6
                            window.draw.fill_circle_fast(400,200,100,pybox.RgbColor(0,255,0))         
            """          
            return _pybox.WindowDrawFilledCircleFast(self.__id,int(x),int(y),int(radius),inside_color,border_color,pen_size)

        def fill_circle_fast_l(self,at : list, radius : int, inside_color, border_color = 0,pen_size : int = 0) :
            """
            Draws a 'fast' filled Circle on the screen at starting point (x,y) with a width and height of (radius_x, radius_y)

            See circle_fast_l() to draw an open/wireframe Circle vs. a filled Circle. 
            See fill_circle_fast() to set the Circle location, width, and height using independent values.

            This drawing function is a 'fast' function that does not use anti-aliasing and is about 10x faster than
            non-fast drawing functions.  These functions are useful for general drawing and do not respond to opacity or transformations.

            Parameters

            - at                   \t -- (x,y) Location of the center of the circle in the window
            - radius                \t -- Radius (in pixels) of the circle.
            - inside_color   \t -- Color of the interior of the circle
            - border_color   \t -- [optional] Color if the outside edge of the circle (based on the current Pen Size).  When omitted, the entire circle is drawn the color
                                    \t -of the inside_color.  See: set_pen_size() to set the thickness of the border when using border_color.
            - pen_size         \t -- [optional] Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:
                            window.draw.fill_circle_fast_l((400,200),100,"red") 
                            window.draw.fill_circle_fast_l((400,200),100,"red","Green")       - Draws a Red circle with a green outer border (thickness of current pen size)
                            window.draw.fill_circle_fast_l(Location,Size,PanColor.ForestGreen())
                            window.draw.fill_circle_fast_l((400,200),100,MyColor,6)            - Sets a pen size of 6
                            window.draw.fill_circle_fast_l((400,200),100,pybox.RgbColor(0,255,0))         
            """          
            return _pybox.WindowDrawFilledCircleFast(self.__id,int(at[0]),int(at[1]),int(radius),inside_color,border_color,pen_size)

        def circle_fast(self,x : int, y : int, radius : int, color,pen_size : int = 0) :
            """
            Draws a 'fast' open/wireframe Circle on the screen at starting point (x,y) with a width and height of (radius_x, radius_y)

            See fill_circle_fast() to draw a filled Circle vs. an open/wireframe Circle
            See circle_fast_l() to set the Circle location, width, and height using a tuple, list, or array

            This drawing function is a 'fast' function that does not use anti-aliasing and is about 10x faster than
            non-fast drawing functions.  These functions are useful for general drawing and do not respond to opacity or transformations.

            Parameters

            - x,y                   \t -- Location of the center of the circle in the window
            - radius                \t -- Radius (in pixels) of the circle.
            - color                 \t -- Color of the circle
            - pen_size         \t -- [optional] Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:
                            window.draw.circle_fast(400,200,100,"red") 
                            window.draw.circle_fast(400,200,100,PanColor.ForestGreen())
                            window.draw.circle_fast(400,200,100,MyColor,6)            - Sets a pen size of 6
                            window.draw.circle_fast(400,200,100,pybox.RgbColor(0,255,0))         
            """               
            return _pybox.WindowDrawCircleFast(self.__id,int(x),int(y),radius,color,color,pen_size)

        def circle_fast_l(self,at : list, radius : int, color,pen_size : int = 0) :
            """
            Draws a 'fast' open/wireframe Circle on the screen at starting point (x,y) with a width and height of (radius_x, radius_y)

            See fill_circle_fast_l() to draw a filled Circle vs. an open/wireframe Circle
            See circle_fast() to set the Circle location, width, and height using independent values.

            This drawing function is a 'fast' function that does not use anti-aliasing and is about 10x faster than
            non-fast drawing functions.  These functions are useful for general drawing and do not respond to opacity or transformations.

            Parameters

            - at                   \t -- (x,y) Location of the center of the circle in the window
            - radius                \t -- Radius (in pixels) of the circle.
            - color                 \t -- Color of circle
            - pen_size         \t -- [optional] Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:
                            window.draw.circle_fast_l((400,200),100,"red") 
                            window.draw.circle_fast_l((400,200),100,PanColor.ForestGreen())
                            window.draw.circle_fast_l(Location,Size,MyColor,6)            - Sets a pen size of 6
                            window.draw.circle_fast_l((400,200),100,pybox.RgbColor(0,255,0))         
            """                  
            return _pybox.WindowDrawCircleFast(self.__id,int(at[0]),int(at[1]),radius,color,color,pen_size)

        # HR Draw Circle Functions

        def circle(self,x, y, radius, color,**kwargs) :
            """
            Draws an open/wireframe Circle on the screen at starting point (x,y) with a width and height of (radius_x, radius_y)

            See fill_circle() to draw a filled Circle vs. an open/wireframe Circle
            See circle_l() to set the Circle location, width, and height using a tuple, list, or array

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            Hint: use an odd-size pen_size for sharper edges.

            Parameters

            - x,y                   \t -- Location of the center of the circle in the window
            - radius                \t -- Radius (in pixels) of the circle.
            - color             \t -- Color of the circle
             
            Keywords and/or Pybox options can be included.  Some various options are as follows:

           - pen_size         \t -- Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:
                            window.draw.circle(400,200,100,"red") 
                            window.draw.circle(400,200,100,PanColor.ForestGreen())
                            window.draw.circle(400,200,100,MyColor,pen_size=6)            - Sets a pen size of 6
                            window.draw.circle(400,200,100,pybox.RgbColor(0,255,0))         
            """             
            return _pybox.WindowDrawCircle(self.__id,x,y,radius,color,True,**kwargs)

        def circle_l(self,at, radius, color,**kwargs) :
            """
            Draws an open/wireframe Circle on the screen at starting point (x,y) with a width and height of (radius_x, radius_y)

            See fill_circle_l() to draw a filled Circle vs. an open/wireframe Circle
            See circle() to set the Circle location, width, and height using independent values

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            Hint: use an odd-size pen_size for sharper edges.

            Parameters

            - at                   \t -- (x,y) Location of the center of the circle in the window
            - radius                \t -- Radius (in pixels) of the circle.
            - color             \t -- Color of the circle
            
            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_size         \t -- Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:
                            window.draw.circle_l((400,200),100,"red") 
                            window.draw.circle_l((400,200),100,PanColor.ForestGreen())
                            window.draw.circle_l((Location,Size,MyColor,pen_size=6)            - Sets a pen size of 6
                            window.draw.circle_l((400,200),100,pybox.RgbColor(0,255,0))         
            """                    
            return _pybox.WindowDrawCircle(self.__id,at[0],at[1],radius,color,True,**kwargs)

        def fill_circle(self,x , y , radius, inside_color, **kwargs) :
            """
            Draws a filled Circle on the screen at starting point (x,y) with a width and height of (radius_x, radius_y)

            See circle() to draw an open/wireframe Circle vs. a filled Circle. 
            See fill_circle_l() to set the Circle location, width, and height using a tuple, list, or array

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            Hint: use an odd-size pen_size for sharper edges.

            Parameters

            - x,y                   \t -- Location of the center of the circle in the window
            - radius                \t -- Radius (in pixels) of the circle.
            - inside_color   \t -- Color of the interior of the circle
            
            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_color   \t -- Color if the outside edge of the circle (based on the current Pen Size).  When omitted, the entire circle is drawn the color
                                    \t -of the inside_color.  See: set_pen_size() to set the thickness of the border when using pen_color.
            - pen_size         \t -- Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

            Examples:
                            window.draw.fill_circle(400,200,100,"red") 
                            window.draw.fill_circle(400,200,100,"red","Green")       - Draws a Red circle with a green outer border (thickness of current pen size)
                            window.draw.fill_circle(400,200,100,PanColor.ForestGreen())
                            window.draw.fill_circle(400,200,100,MyColor,pen_size=6)            - Sets a pen size of 6
                            window.draw.fill_circle(400,200,100,pybox.RgbColor(0,255,0))         
            """               
            return _pybox.WindowDrawCircle(self.__id,x,y,radius,inside_color,False,**kwargs)

        def fill_circle_l(self,at, radius, inside_color, **kwargs) :
            """
            Draws a filled Circle on the screen at starting point (x,y) with a width and height of (radius_x, radius_y)

            See circle_l() to draw an open/wireframe Circle vs. a filled Circle. 
            See fill_circle() to set the Circle location, width, and height using independent values.

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            Hint: use an odd-size pen_size for sharper edges.

            Parameters

            - at                   \t -- (x,y) Location of the center of the circle in the window
            - radius                \t -- Radius (in pixels) of the circle.
            - inside_color   \t -- Color of the interior of the circle
            
            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_color   \t -- Color if the outside edge of the circle (based on the current Pen Size).  When omitted, the entire circle is drawn the color
                                    \t -of the inside_color.  See: set_pen_size() to set the thickness of the border when using pen_color.
            - pen_size         \t -- Pen size for the border color if specified.  If the pen_size is not specified, the current default pen size is used.
                                    \t -See set_pen_size() to set the default pen size (the default is 1) 
            Examples:
                            window.draw.fill_circle_l((400,200),100,"red") 
                            window.draw.fill_circle_l((400,200),100,PanColor.ForestGreen())
                            window.draw.fill_circle_l(Location,Size,MyColor,pen_size=6)            - Sets a pen size of 6
                            window.draw.fill_circle_l((400,200),100,pybox.RgbColor(0,255,0))         

            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()
            """               
            return _pybox.WindowDrawCircle(self.__id,at[0],at[1],radius,inside_color,False,**kwargs)

        #
        # Draw Polygon (and lines()) Functions
        #

        def polygon(self, pos : list,color,**kwargs) :
            """
            Draws an open/wireframe polygon on the screen using clockwise points in the list.
            
            Example: 
            
            my_list = [(400,400),(500,500),(500,600),(300,600),(300,500)]
            window.draw.polygon(my_list,"green",pen_size=5) # draws a green polygon with a pen size of 5 that looks like a house. 

            See fill_polygon() to draw a filled polygon vs. an open/wireframe polygon. 

            This drawing function responds to current opacity and transformations and will anti-alias output results.

            At least 3 points must be given to draw a polygon.  
            
            Parameters

            - pos           \t -- List or array of clockwise polygon points.
            - color         \t -- Color of the polygon

            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_size         \t -- Pen size for the color if specified.  If the pen_size is not specified, the current default pen size is used.
                                \t -See set_pen_size() to set the default pen size (the default is 1) 
   
            Other useful keywords: angle, join_type, gradient_angle, set_gradient, set_center, opacity
            
            Examples:

                window.draw.polygon(my_list,"yellow")
                window.draw.polygon(my_list,"yellow(128)",pen_size=6)        # Sets an opacity of 128 for the yellow
                window.draw.polygon(my_list,"{255,255,0}",pen_size=6)        # Another way to express yellow.
                window.draw.polygon(my_list,"{255,255,0,128}",pen_size=6)    # Another way to express yellow with opacity = 128
                window.draw.polygon(my_list,"red,blue",pen_size=6)           # Specifies gradient color

            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen", or 3-4 element arrays such as [0,255,255]. 

            Opacity values may also be used on most functions, which can be specified in text by adding (opacity), e.g. "cyan(170)" for an opacity of 170
            (opacity ranges from 0-255)
            
            """
            _pybox.WindowDrawPolygon(self.__id,pos,color,0,**kwargs)

        def fill_polygon(self, Loc : list,color,**kwargs) :
            """
            Draws an filled Polygon on the screen using clockwise points in the list.
            
            Example: 
            
            my_list = [(400,400),(500,500),(500,600),(300,600),(300,500)]
            window.draw.fill_polygon(my_list,"green") # draws a filled green polygon with a pen size of 5 that looks like a house. 

            See polygon() to draw an open/wireframe polygon vs. a filled polygon. 

            This drawing function responds to current opacity and transformations and will anti-alias output results.

            At least 3 points must be given to draw a polygon. 
            
            Parameters

            - pos           \t -- List or array of clockwise polygon points.
            - color         \t -- Color of the interior of the polygon

            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_size         \t -- Pen size for the color if specified, which will draw a border around the polygon.  
                                \t If the pen_size is not specified, the current default pen size is used.
                                \t - See set_pen_size() to set the default pen size (the default is 1) 
            - pen_color         \t -- Sets the  color of the border pen.  If no pen size is specified, the default/current pen size is used.
            
            
            Other useful keywords: angle, join_type, gradient_angle, set_gradient, set_center, opacity
            
            Examples:

                window.draw.fill_polygon(my_list,"yellow")
                window.draw.fill_polygon(my_list,"yellow(128)",pen_size=6,,pen_color="red")        # Sets an opacity of 128 for the yellow
                window.draw.fill_polygon(my_list,"{255,255,0}",pen_size=6)        # Another way to express yellow.
                window.draw.fill_polygon(my_list,"{255,255,0,128}",pen_size=6)    # Another way to express yellow with opacity = 128
                window.draw.fill_polygon(my_list,"red,blue",pen_size=6)           # Specifies gradient color

            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen", or 3-4 element arrays such as [0,255,255]. 

            Opacity values may also be used on most functions, which can be specified in text by adding (opacity), e.g. "cyan(170)" for an opacity of 170
            (opacity ranges from 0-255)
            
            """
            _pybox.WindowDrawPolygon(self.__id,Loc,color,1,**kwargs)

        def lines(self, pos : list,color,**kwargs) :
            """
            Draws an open/wireframe set of lines on the screen using points in the list.
            ** note: This function is essentially the same as "draw.polygon".  The only difference is that the last point is not connected to the
            first point (i.e. it is an open set of lines vs. a polygon)
            
            Example: 
            
            my_list = [(400,400),(500,500),(500,600),(300,600),(300,500)]
            window.draw.lines(my_list,"green",pen_size=5) # draws a green set of lines with a pen size of 5. 

            See fill_lines() to draw a filled set of lines vs. an open/wireframe set of lines. 

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            
            Parameters

            - pos           \t -- List or array of line points.
            - color         \t -- Color of the set of lines

            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_size      \t -- Pen size for the color if specified.  If the pen_size is not specified, the current default pen size is used.
                            \t -See set_pen_size() to set the default pen size (the default is 1) 
            - linecaps      \t - Sets the 'cap' type for the bezier curve.  By default these are round and the size of the line itself.
                            
                            \t Possible linecap values are "flat" (no caps),"round","diamond","square" and "arrow".  use "default" to set default cap type.
                            \t Add "anchor" to make caps larger, e.g. "round anchor","arrow anchor", etc.  ("flat" has no "anchor")
                            
                            \t This sets both cap types unless a ',' is used, such as "round,square anchor".  
                            \t using a blank for the cap type sets the default, such as ",arrow anchor" or "arrow anchor,", which sets only the
                            \t end cap and beginning cap to "anchor arrow", respectively, leaving the other cap type as the default. 
   
            Other useful keywords: angle, join_type, gradient_angle, set_gradient, set_center, opacity
            
            Examples:

                window.draw.lines(my_list,"yellow")
                window.draw.lines(my_list,"yellow(128)",pen_size=6)        # Sets an opacity of 128 for the yellow
                window.draw.lines(my_list,"{255,255,0}",pen_size=6)        # Another way to express yellow.
                window.draw.lines(my_list,"{255,255,0,128}",pen_size=6)    # Another way to express yellow with opacity = 128
                window.draw.lines(my_list,"yellow",line_caps="round anchor,arrow anchor")       # Adds a round circle and arrow to beginning & end

            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen", or 3-4 element arrays such as [0,255,255]. 

            Opacity values may also be used on most functions, which can be specified in text by adding (opacity), e.g. "cyan(170)" for an opacity of 170
            (opacity ranges from 0-255)
            
            """
            _pybox.WindowDrawPolygon(self.__id,pos,color,10,**kwargs)

        def fill_lines(self, pos : list,color,**kwargs) :
            """
            Draws a filled set of lines on the screen using points in the list.
            ** note: This function is essentially the same as "draw.fill_polygon".  The only difference is that the last point is not connected to the
            first point when a pen (i.e. border) is used. (i.e. it is an open set of lines vs. a polygon)
            
            Without using a pen, fill_lines() is functionally equivalent to fill_polygon()
            Example: 
            
            my_list = [(400,400),(500,500),(500,600),(300,600),(300,500)]
            window.draw.fill_lines(my_list,"green",pen_size=5,pen_color="yellow") # draws a green set of lines with a pen size of 5. 

            See lines() to draw an open/wireframe set of lines vs. a filled set of lines. 

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            
            Parameters

            - pos           \t -- List or array of line points.
            - color         \t -- Color of the set of lines

            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_size      \t -- Pen size for the color if specified.  If the pen_size is not specified, the current default pen size is used.
                            \t -See set_pen_size() to set the default pen size (the default is 1) 
            - pen_color     \t -- Sets the  color of the border pen.  If no pen size is specified, the default/current pen size is used.
            - line_caps     \t - Line caps may be used when a pen is used as a border.  See lines() for more information.
   
            Other useful keywords: angle, join_type, gradient_angle, set_gradient, set_center, opacity
            
            Examples:

                window.draw.fill_lines(my_list,"yellow")
                window.draw.fill_lines(my_list,"yellow(128)",pen_size=6)        # Sets an opacity of 128 for the yellow
                window.draw.fill_lines(my_list,"{255,255,0}",pen_size=6)        # Another way to express yellow.
                window.draw.fill_lines(my_list,"{255,255,0,128}",pen_size=6)    # Another way to express yellow with opacity = 128
                window.draw.fill_lines(my_list,"yellow",pen_color="cyan")       # sets border color to cyan (default is white)

            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen", or 3-4 element arrays such as [0,255,255]. 

            Opacity values may also be used on most functions, which can be specified in text by adding (opacity), e.g. "cyan(170)" for an opacity of 170
            (opacity ranges from 0-255)
            
            """
            _pybox.WindowDrawPolygon(self.__id,pos,color,11,**kwargs)  
 

        #
        # Bezier and Spline Curve Functions
        #

        def beziers(self, pos : list,color,**kwargs) :
            """
            Draws an open/wireframe sequence of connected Cubic Bezier splines. There are two control points between each two points, such as 
            <p1,c1,c2,p2,c3,c4,p3>, in this case, using 4 control points, 2 each between the three points. 

            - This function draws a 'Cubic Bezier Spline', requiring two control points between every two points.
            See QuadBeziers() (i.e. Quadratic Bezier vs. cubic) for the Bezier Spline format that requires only one control point between each set of points.

            - See fill_beziers() function to draw filled beziers. vs. open/wireframe beziers.
            
            Example (draws a sine-wave like bezier with 3 points and 4 control points between points 1 and 3): 
            
            my_list = [(50,400),(110,200),(170,600),(230,400),(290,200),(350,600),(410,400)]
            window.draw.beziers(my_list,"green",pen_size=5)

            See fill_beziers() to draw filled beziers vs. open/wireframe beziers. 

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            
            Parameters

            - pos           \t -- List or array of bezier points and control points.
            - color         \t -- Color of the beziers curve

            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_size         \t -- Pen size for the color if specified.  If the pen_size is not specified, the current default pen size is used.
                                \t -See set_pen_size() to set the default pen size (the default is 1) 
            - pen_size      \t - Sets the thickness of the bezier curve.  Otherwise defaults to current Pen Size (which is usually 1)
            - linecaps      \t - Sets the 'cap' type for the bezier curve.  By default these are round and the size of the bezier line itself.
                            
                            \t Possible linecap values are "flat" (no caps),"round","diamond","square" and "arrow".  use "default" to set default cap type.
                            \t Add "anchor" to make caps larger, e.g. "round anchor","arrow anchor", etc.  ("flat" has no "anchor")
                            
                            \t This sets both cap types unless a ',' is used, such as "round,square anchor".  
                            \t using a blank for the cap type sets the default, such as ",arrow anchor" or "arrow anchor,", which sets only the
                            \t end cap and beginning cap to "anchor arrow", respectively, leaving the other cap type as the default. 
  
                                
            Other useful keywords: angle, join_type, gradient_angle, set_gradient, set_center, opacity
            
            Examples:

                window.draw.beziers(my_list,"yellow")
                window.draw.beziers(my_list,"yellow(128)",pen_size=6)        # Sets an opacity of 128 for the yellow
                window.draw.beziers(my_list,"{255,255,0}",pen_size=6)        # Another way to express yellow.
                window.draw.beziers(my_list,"{255,255,0,128}",pen_size=6)    # Another way to express yellow with opacity = 128
                window.draw.beziers(my_list,"yellow",line_caps="anchor round, anchor arrow")   # Adds a round circle and arrow to beginning & end

            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen", or 3-4 element arrays such as [0,255,255]. 

            Opacity values may also be used on most functions, which can be specified in text by adding (opacity), e.g. "cyan(170)" for an opacity of 170
            (opacity ranges from 0-255)
            
            """            
            _pybox.WindowDrawPolygon(self.__id,pos,color,2,**kwargs)

        def fill_beziers(self, pos : list,color,**kwargs) :
            """
            Draws a filled sequence of connected Cubic Bezier splines. There are two control points between each two points, such as 
            <p1,c1,c2,p2,c3,c4,p3>, in this case, using 4 control points, 2 each between the three points. The filled area is generally 
            along the axis line between the first and last points.

            - This function draws a 'Cubic Bezier Spline', requiring two control points between every two points.
            See QuadBeziers() (i.e. Quadratic Bezier vs. cubic) for the Bezier Spline format that requires only one control point between each set of points.

            - See beziers() function to draw open/wireframe beziers vs. filled
            
            Example (draws a sine-wave like bezier with 3 points and 4 control points between points 1 and 3): 
            
            my_list = [(50,400),(110,200),(170,600),(230,400),(290,200),(350,600),(410,400)]
            window.draw.beziers(my_list,"green",pen_size=5,pen_color="yellow")  # draws green interior with yellow border of 5 pixels.

            See fill_beziers() to draw filled beziers vs. open/wireframe beziers. 

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            
            Parameters

            - pos           \t -- List or array of bezier points and control points.
            - color         \t -- Interior color of the beziers curve

            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_size      \t - Sets the thickness of the bezier x=curve.  Otherwise defaults to current Pen Size (which is usually 1)
            - pen_color     \t -- Sets the  color of the border pen.  If no pen size is specified, the default/current pen size is used.
            - line_caps     \t - Sets the 'cap' type for the bezier curve.  By default these are round and the size of the bezier line itself.
                            
                            \t Possible linecap values are "flat" (no caps),"round","diamond","square" and "arrow".  use "default" to set default cap type.
                            \t Add "anchor" to make caps larger, e.g. "round anchor","arrow anchor", etc.  ("flat" has no "anchor")
                            
                            \t This sets both cap types unless a ',' is used, such as "round,square anchor".  
                            \t using a blank for the cap type sets the default, such as ",arrow anchor" or "arrow anchor,", which sets only the
                            \t end cap and beginning cap to "anchor arrow", respectively, leaving the other cap type as the default. 
  
                                
            Other useful keywords: angle, join_type, gradient_angle, set_gradient, set_center, opacity
            
            Examples:

                window.draw.beziers(my_list,"yellow")
                window.draw.beziers(my_list,"yellow(128)",pen_size=6)        # Sets an opacity of 128 for the yellow
                window.draw.beziers(my_list,"{255,255,0}",pen_size=6)        # Another way to express yellow.
                window.draw.beziers(my_list,"{255,255,0,128}",pen_size=6)    # Another way to express yellow with opacity = 128
                window.draw.beziers(my_list,"yellow",line_caps="anchor round, anchor arrow")   # Adds a round circle and arrow to beginning & end

            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen", or 3-4 element arrays such as [0,255,255]. 

            Opacity values may also be used on most functions, which can be specified in text by adding (opacity), e.g. "cyan(170)" for an opacity of 170
            (opacity ranges from 0-255)           
            """
            _pybox.WindowDrawPolygon(self.__id,pos,color,3,**kwargs)
 
        def quad_beziers(self, pos : list,color,**kwargs) :
            """
            Draws a sequence of connected Quadratic Bezier splines. There is one control point between each two points, such as 
            <p1,c1,p2,c2,p3>, in this case, using 2 control points, 1 each between the three points. 

            - This function draws a 'Quadratic Bezier Spline', requiring one control point between every two points.
            - See beziers() (i.e. Cubic Bezier vs. quadratic) for the Bezier Spline format that requiress two control points between each set of points, for more control.
            - See fill_quad_beziers() function to draw filled quadratic beziers. vs. open/wireframe quadratic beziers.
            
            Example (draws a S-Curve Quadratic Bezier with 3 points and 2 control points between points 1 and 2): 
            
            my_list = [(590,277),(347,310),(556,374),(726,433),(453,480)]
            window.draw.quad_beziers(my_list,"green",pen_size=5) # draws a green, S-shaped Quadratic Bezier Curve size of 5. 

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            
            Parameters

            - pos           \t -- List or array of bezier points and control points.
            - color         \t -- Color of the beziers curve

            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_size      \t - Sets the thickness of the bezier curve.  Otherwise defaults to current Pen Size (which is usually 1)
            - linecaps      \t - Sets the 'cap' type for the bezier curve.  By default these are round and the size of the bezier line itself.
                            
                            \t Possible linecap values are "flat" (no caps),"round","diamond","square" and "arrow".  use "default" to set default cap type.
                            \t Add "anchor" to make caps larger, e.g. "round anchor","arrow anchor", etc.  ("flat" has no "anchor")
                            
                            \t This sets both cap types unless a ',' is used, such as "round,square anchor".  
                            \t using a blank for the cap type sets the default, such as ",arrow anchor" or "arrow anchor,", which sets only the
                            \t end cap and beginning cap to "anchor arrow", respectively, leaving the other cap type as the default. 
  
                                
            Other useful keywords: angle, join_type, gradient_angle, set_gradient, set_center, opacity
            
            Examples:

                window.draw.quad_beziers(my_list,"yellow")
                window.draw.quad_beziers(my_list,"yellow(128)",pen_size=6)        # Sets an opacity of 128 for the yellow
                window.draw.quad_beziers(my_list,"{255,255,0}",pen_size=6)        # Another way to express yellow.
                window.draw.quad_beziers(my_list,"{255,255,0,128}",pen_size=6)    # Another way to express yellow with opacity = 128
                window.draw.quad_beziers(my_list,"yellow",line_caps="anchor round, anchor arrow")   # Adds a round circle and arrow to beginning & end

            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen", or 3-4 element arrays such as [0,255,255]. 

            Opacity values may also be used on most functions, which can be specified in text by adding (opacity), e.g. "cyan(170)" for an opacity of 170
            (opacity ranges from 0-255)
            
            """
            _pybox.WindowDrawPolygon(self.__id,pos,color,4,**kwargs)   

        def fill_quad_beziers(self, pos : list,color,**kwargs) :
            """
            Draws a sequence of connected Quadratic Bezier splines. There is one control point between each two points, such as 
            <p1,c1,p2,c2,p3>, in this case, using 2 control points, 1 each between the three points. 

            - The filled area is generally along the axis line between the first and last points.
            - This function draws a 'Quadratic Bezier Spline', requiring one control point between every two points.
            - See fill_beziers() (i.e. Cubic Bezier vs. quadratic) for the Bezier Spline format that requiress two control points between each set of points, for more control.
            - See quad_beziers() function to draw open/wireframe quadratic beziers vs. filled quadratic beziers.
            
            Example (draws a filled S-Curve Quadratic Bezier with 3 points and 2 control points between points 1 and 2): 
            
            my_list = [(590,277),(347,310),(556,374),(726,433),(453,480)]
            window.draw.quad_beziers(my_list,"green",pen_size=5,pen_color=yellow) # draws a green Quadratic Bezier Curve, with yellow border of size of 5. 
            
            This drawing function responds to current opacity and transformations and will anti-alias output results.
            
            Parameters

            - pos           \t -- List or array of bezier points and control points.
            - color         \t -- Interior color of the beziers curve

            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_size      \t - Sets the thickness of the bezier x=curve.  Otherwise defaults to current Pen Size (which is usually 1)
            - pen_color     \t -- Sets the  color of the border pen.  If no pen size is specified, the default/current pen size is used.
            - line_caps     \t - Line caps may be used when a pen is used as a border.  See quad_beziers() for more information.
                                
            Other useful keywords: angle, join_type, gradient_angle, set_gradient, set_center, opacity
            
            Examples:

                window.draw.fill_quad_beziers(my_list,"yellow")
                window.draw.fill_quad_beziers(my_list,"yellow(128)",pen_size=6)        # Sets an opacity of 128 for the yellow
                window.draw.fill_quad_beziers(my_list,"{255,255,0}",pen_size=6)        # Another way to express yellow.
                window.draw.fill_quad_beziers(my_list,"{255,255,0,128}",pen_size=6)    # Another way to express yellow with opacity = 128

            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen", or 3-4 element arrays such as [0,255,255]. 

            Opacity values may also be used on most functions, which can be specified in text by adding (opacity), e.g. "cyan(170)" for an opacity of 170
            (opacity ranges from 0-255)           
            """
            _pybox.WindowDrawPolygon(self.__id,pos,color,5,**kwargs)   

        def curve(self, Loc : list,color,**kwargs) :
            """
            Draws an open/wireframe Spline Curve of connected points. 
            
            A cardinal spline is a sequence of individual curves joined to form a larger curve. The spline is specified 
            by an array of points and a tension parameter. A cardinal spline passes smoothly through each point in the array; 
            there are no sharp corners and no abrupt changes in the tightness of the curve.
        
            - See beziers() and quad_beziers() for bezier-type curves.
            - See fill_curve() function to draw a filled spline curve. vs. open/wireframe spline curve.
            - See closed_curve() function to draw a closed spline curve (last point connects to first point)
            
            Example (Draws a sine-wave-like curve with 4 curve points):
            
            my_list = [(200,500),(278,333),(386,640),(465,486)]
            window.draw.curve(my_list,"green",pen_size=5) # draws a green curve with a pen size of 5. 
           
            This drawing function responds to current opacity and transformations and will anti-alias output results.
            
            Parameters

            - pos           \t -- List or array of spline curve points.
            - color         \t -- Color of the spline curve

            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - tension       \t - Sets the tension. By default the tension is .5.  
                            \t - Using smaller numbers (e.g. .1) makes the curves appear more and more like bent straight lines.
                            \t - Using numbers > .5, e.g. 1.5, 2.0, etc. make the 'tension' on the curve higher, causing the curves to take longer to bend around to fit the curve.
            - pen_size      \t - Sets the thickness of the spline curve.  Otherwise defaults to current Pen Size (which is usually 1)
            - linecaps      \t - Sets the 'cap' type for the spline curve.  By default these are round and the size of the spline curve line itself.
                            
                            \t Possible linecap values are "flat" (no caps),"round","diamond","square" and "arrow".  use "default" to set default cap type.
                            \t Add "anchor" to make caps larger, e.g. "round anchor","arrow anchor", etc.  ("flat" has no "anchor")
                            
                            \t This sets both cap types unless a ',' is used, such as "round,square anchor".  
                            \t using a blank for the cap type sets the default, such as ",arrow anchor" or "arrow anchor,", which sets only the
                            \t end cap and beginning cap to "anchor arrow", respectively, leaving the other cap type as the default. 
  
                                
            Other useful keywords: angle, join_type, gradient_angle, set_gradient, set_center, opacity
            
            Examples:

                window.draw.curve(my_list,"yellow")
                window.draw.curve(my_list,"yellow(128)",pen_size=6)        # Sets an opacity of 128 for the yellow
                window.draw.curve(my_list,"{255,255,0}",pen_size=6)        # Another way to express yellow.
                window.draw.curve(my_list,"{255,255,0,128}",pen_size=6)    # Another way to express yellow with opacity = 128
                window.draw.curve(my_list,"yellow",line_caps="anchor round, anchor arrow")   # Adds a round circle and arrow to beginning & end

            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen", or 3-4 element arrays such as [0,255,255]. 

            Opacity values may also be used on most functions, which can be specified in text by adding (opacity), e.g. "cyan(170)" for an opacity of 170
            (opacity ranges from 0-255)                       
            """
            _pybox.WindowDrawPolygon(self.__id,Loc,color,6,**kwargs)   

        def fill_curve(self, Loc : list,color,**kwargs) :
            """
            Draws a filled Spline Curve of connected points. 
            
            A cardinal spline is a sequence of individual curves joined to form a larger curve. The spline is specified 
            by an array of points and a tension parameter. A cardinal spline passes smoothly through each point in the array; 
            there are no sharp corners and no abrupt changes in the tightness of the curve.
        
            - The filled area is generally along the axis line between the first and last points.
            - See fill_beziers() and fill_quad_beziers() for bezier-type curves.
            - See curve() function to draw an open/wireframe spline curve. vs. a filled spline curve.
            - See fill_closed_curve() function to draw a closed spline curve (last point connects to first point)
            
            Example (Draws a sine-wave-like curve with 4 curve points):
            
            my_list = [(200,500),(278,333),(386,640),(465,486)]
            window.draw.fill_curve(my_list,"green",pen_size=5,pen_color="yellow") # draws a filled green curve with a yellow border of size of 5. 
           
            This drawing function responds to current opacity and transformations and will anti-alias output results.
            
            Parameters

            - pos           \t -- List or array of spline curve points.
            - color         \t -- Color of the spline curve

            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - tension       \t - Sets the tension. By default the tension is .5.  
                            \t - Using smaller numbers (e.g. .1) makes the curves appear more and more like bent straight lines.
                            \t - Using numbers > .5, e.g. 1.5, 2.0, etc. make the 'tension' on the curve higher, causing the curves to take longer to bend around to fit the curve.
            - pen_size      \t - Sets the thickness of the spline curve.  Otherwise defaults to current Pen Size (which is usually 1)
            - pen_color     \t -- Sets the  color of the border pen.  If no pen size is specified, the default/current pen size is used.
            - line_caps     \t - Line caps may be used when a pen is used as a border.  See curve() for more information.
                                
            Other useful keywords: angle, join_type, gradient_angle, set_gradient, set_center, opacity
            
            Examples:

                window.draw.fill_curve(my_list,"yellow")
                window.draw.fill_curve(my_list,"yellow(128)",pen_size=6)        # Sets an opacity of 128 for the yellow
                window.draw.fill_curve(my_list,"{255,255,0}",pen_size=6)        # Another way to express yellow.
                window.draw.fill_curve(my_list,"{255,255,0,128}",pen_size=6)    # Another way to express yellow with opacity = 128

            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen", or 3-4 element arrays such as [0,255,255]. 

            Opacity values may also be used on most functions, which can be specified in text by adding (opacity), e.g. "cyan(170)" for an opacity of 170
            (opacity ranges from 0-255)                       
            """
            _pybox.WindowDrawPolygon(self.__id,Loc,color,7,**kwargs)   

        def closed_curve(self, Loc : list,color,**kwargs) :
            """
            Draws an closed open/wireframe Spline Curve of connected points. See curve() function to draw non-closed spline curve.
            
            A cardinal spline is a sequence of individual curves joined to form a larger curve. The spline is specified 
            by an array of points and a tension parameter. A cardinal spline passes smoothly through each point in the array; 
            there are no sharp corners and no abrupt changes in the tightness of the curve.
        
            - See beziers() and quad_beziers() for bezier-type curves.
            - See fill_closed_curve() function to draw a filled closed spline curve. vs. open/wireframe closed spline curve.
            - See curve() function to draw a non-closed spline curve.
            
            Example (Draws a sideways figure-8/infinity symbol curve with 4 curve points):
            
            my_list = [(441,510),(432,377),(218,510),(227,377)]
            window.draw.closed_curve(my_list,"green",pen_size=5) # draws a green curve with a pen size of 5. 
           
            This drawing function responds to current opacity and transformations and will anti-alias output results.
            
            Parameters

            - pos           \t -- List or array of spline curve points.
            - color         \t -- Color of the spline curve

            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - tension       \t - Sets the tension. By default the tension is .5.  
                            \t - Using smaller numbers (e.g. .1) makes the curves appear more and more like bent straight lines.
                            \t - Using numbers > .5, e.g. 1.5, 2.0, etc. make the 'tension' on the curve higher, causing the curves to take longer to bend around to fit the curve.
            - pen_size      \t - Sets the thickness of the spline curve.  Otherwise defaults to current Pen Size (which is usually 1)  
                                
            Other useful keywords: angle, join_type, gradient_angle, set_gradient, set_center, opacity
            
            Examples:

                window.draw.closed_curve(my_list,"yellow")
                window.draw.closed_curve(my_list,"yellow(128)",pen_size=6)        # Sets an opacity of 128 for the yellow
                window.draw.closed_curve(my_list,"{255,255,0}",pen_size=6)        # Another way to express yellow.
                window.draw.closed_curve(my_list,"{255,255,0,128}",pen_size=6)    # Another way to express yellow with opacity = 128
                window.draw.closed_curve(my_list,"yellow",line_caps="anchor round, anchor arrow")   # Adds a round circle and arrow to beginning & end

            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen", or 3-4 element arrays such as [0,255,255]. 

            Opacity values may also be used on most functions, which can be specified in text by adding (opacity), e.g. "cyan(170)" for an opacity of 170
            (opacity ranges from 0-255)                       
            """
            _pybox.WindowDrawPolygon(self.__id,Loc,color,8,**kwargs)   

        def fill_closed_curve(self, Loc : list,color,**kwargs) :
            """
            Draws a closed filled Spline Curve of connected points.  See fill_curve() to draw non-closed spline curve.
            
            A cardinal spline is a sequence of individual curves joined to form a larger curve. The spline is specified 
            by an array of points and a tension parameter. A cardinal spline passes smoothly through each point in the array; 
            there are no sharp corners and no abrupt changes in the tightness of the curve.
        
            - The filled area is generally along the axis line between the first and last points.
            - See fill_beziers() and fill_quad_beziers() for bezier-type curves.
            - See closed_curve() function to draw an open/wireframe spline curve. vs. a filled spline curve.
            - See fill_curve() function to draw a non-closed spline curve
            
            Example (Draws a sideways figure-8/infinity symbol curve with 4 curve points, with a green/blue gradient):
            
            my_list = [(200,500),(278,333),(386,640),(465,486)]
            window.draw.fill_closed_curve(my_list,"green,blue",pen_size=5,pen_color="yellow") # draws a filled green-to-blue curve with a yellow border of size of 5. 
           
            This drawing function responds to current opacity and transformations and will anti-alias output results.
            
            Parameters

            - pos           \t -- List or array of spline curve points.
            - color         \t -- Color of the spline curve

            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - tension       \t - Sets the tension. By default the tension is .5.  
                            \t - Using smaller numbers (e.g. .1) makes the curves appear more and more like bent straight lines.
                            \t - Using numbers > .5, e.g. 1.5, 2.0, etc. make the 'tension' on the curve higher, causing the curves to take longer to bend around to fit the curve.
            - pen_size      \t - Sets the thickness of the spline curve.  Otherwise defaults to current Pen Size (which is usually 1)
            - pen_color     \t -- Sets the  color of the border pen.  If no pen size is specified, the default/current pen size is used.
                                
            Other useful keywords: angle, join_type, gradient_angle, set_gradient, set_center, opacity
            
            Examples:

                window.draw.fill_closed_curve(my_list,"yellow")
                window.draw.fill_closed_curve(my_list,"yellow,blue")
                window.draw.fill_closed_curve(my_list,"yellow(128)",pen_size=6)        # Sets an opacity of 128 for the yellow
                window.draw.fill_closed_curve(my_list,"{255,255,0}",pen_size=6)        # Another way to express yellow.
                window.draw.fill_closed_curve(my_list,"{255,255,0,128}",pen_size=6)    # Another way to express yellow with opacity = 128

            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen", or 3-4 element arrays such as [0,255,255]. 

            Opacity values may also be used on most functions, which can be specified in text by adding (opacity), e.g. "cyan(170)" for an opacity of 170
            (opacity ranges from 0-255)                       
            """
            _pybox.WindowDrawPolygon(self.__id,Loc,color,9,**kwargs)   

        def bezier(self,p1 : list, p2 : list, p3 : list,p4 : list,color,**kwargs) :
            """
            Draws an open/wireframe simple 4-point Cubic Bezier curve.  
            
            See fill_bezier() to draw a simple 4-point filled bezier curve vs. open/wireframe
            
            ** This function is included for compatibility with Windows GDI functions.
            ** See: beziers() function for information on usage of bezier functions.
            
            Example (Draws a simple 4-point Cubic Bezier Curve in the shape of a horse-shoe curve)
          
            window.draw.bezier((200,500),(200,225),(500,225),(500,500),"green",pen_size=5) # draws a green set of lines with a pen size of 5. 
            """
            return _pybox.WindowDrawBezier(self.__id,p1,p2,p3,p4,color,True,**kwargs)

        def fill_bezier(self,p1 : list, p2 : list, p3 : list,p4 : list,color,**kwargs) :
            """
            Draws a filled simple 4-point Cubic Bezier curve.  
            
            See bezier() to draw a simple 4-point open/wireframe bezier curve vs. filled
            
            ** This function is included for compatibility with Windows GDI functions.
            ** See: fill_beziers() function for information on usage of bezier functions.
            
            Example (Draws a simple filled 4-point Cubic Bezier Curve in the shape of a horse-shoe curve)
          
            window.draw.fill_bezier((200,500),(200,225),(500,225),(500,500),"green,blue",pen_size=5,pen_color="yellow")
            
            --> The above draws a curve with a green and blue gradient, and a yellow border of 5 pixels.
            """
            return _pybox.WindowDrawBezier(self.__id,p1,p2,p3,p4,color,False,**kwargs)

        def quad_bezier(self,p1 : list, p2 : list, p3 : list,color,**kwargs) :
            """
            Draws an open/wireframe simple 3-point Quadratic Bezier curve.  
            
            See fill_quad_bezier() to draw a simple 4-point filled quadratic Bezier curve vs. open/wireframe
            
            ** This function is included for compatibility with Windows GDI functions.
            ** See: quad_beziers() function for information on usage of bezier functions.
            
            Example (Draws a simple 3-point Qaudratic Bezier Curve)
          
            window.draw.quad_bezier((200,500),(296,247),(400,500),"green",pen_size=5) # draws a green set of lines with a pen size of 5.  
            """
            return _pybox.WindowDrawQuadBezier(self.__id,p1,p2,p3,color,True,**kwargs)

        def fill_quad_bezier(self,p1 : list, p2 : list, p3 : list,color,**kwargs) :
            """
            Draws a filled simple 3-point Quadratic Bezier curve.  
            
            See quad_bezier() to draw a simple 4-point open/wireframe bezier curve vs. filled
            
            ** This function is included for compatibility with Windows GDI functions.
            ** See: fill_quad_beziers() function for information on usage of bezier functions.
            
            Example (Draws a simple filled 3-point Quadratic Bezier Curve in the shape of a horse-shoe curve)
          
            window.draw.fill_quad_bezier((200,500),(296,247),(400,500),"green,blue",pen_size=5,pen_color="yellow")
            
            --> The above draws a curve with a green and blue gradient, and a yellow border of 5 pixels.
            """
            return _pybox.WindowDrawQuadBezier(self.__id,p1,p2,p3,color,False,**kwargs)

        #
        # Arc and Pie Functions
        #
        
        def arc(self,x ,y , radius_x, radius_y, start_angle, sweep_angle , arc_color, **kwargs) :
            """
            Draws an open/wireframe Arc in the window.  An 'Arc' is a partial ellipse.  
            The same parameters of Width and Height (or RadiusX and RadiusY) are given. Input angles are in degrees. 
            
            - See arc_l() to use list/array/tuple for (x,y) and (radiusx,radiusy) values.            
            - See fill_arc() to draw filled arc. vs. an open/wireframe
            
            Parameters: 
         
            - x,y           \t -- Location of the center of the ellipse in the window
            - radius_x      \t -- Width/Radius (in pixels) of the ellipse in the X direction
            - radius_y      \t -- Height/Radius (in pixels) of the ellipse in the Y direction
            - start_angle   \t -- Where to start drawing the ellipse.   0 degrees is directly right on the X-Axis, with a counter-clockwise rotation (i.e. 90 degrees is top, -90 is bottom)
            - sweep_angle   \t -- How many degrees in a circle to draw the ellipse. 
    
          
            Keywords and/or Pybox options can be included.  Some various options are as follows:
         
            - pen_size      \t - Sets the thickness of the arc.  Otherwise defaults to current Pen Size (which is usually 1), e.g. arc(x,y,rx,ry,"red",pen_size=10)
            - join_type     \t - Used to set how angles on lines are joined.  Default is "miter" can be sharp.  Setting join_type="round" (or "bevel") can make edges softer.
            - line_caps      \t - Sets the 'cap' type for the arc.  By default these are round and the size of the arc line itself.
                            
                            \t Possible linecap values are "flat" (no caps),"round","diamond","square" and "arrow".  use "default" to set default cap type.
                            \t Add "anchor" to make caps larger, e.g. "round anchor","arrow anchor", etc.  ("flat" has no "anchor")
                            
                            \t This sets both cap types unless a ',' is used, such as "round,square anchor".  
                            \t using a blank for the cap type sets the default, such as ",arrow anchor" or "arrow anchor,", which sets only the
                            \t end cap and beginning cap to "anchor arrow", respectively, leaving the other cap type as the default. 
                              
            Example: 
            
            draw.arc(200,200,400,50,90,-180,"red") -- Draws an arc based on an ellipse of RadiusX=400, RadiusY = 400.  The 90 starts at the top of the axis. The -180 sweeps from
            this point, creating an arc from the top of the ellipse, rotating clockwise (because the sweep angle is negative) to draw the ellipse down to the bottom of the ellipse.
            """               
            return _pybox.WindowDrawArc(self.__id,x,y,radius_x,radius_y,start_angle,sweep_angle,arc_color,0,**kwargs)

        def arc_l(self,pos : list, size : list, start_angle, sweep_angle, arc_color, **kwargs) :
            """
            Draws an open/wireframe Arc in the window.  An 'Arc' is a partial ellipse.  The same parameters of Width and Height (or RadiusX and RadiusY) are given. Input angles are in degrees. 
            
            - See arc() to use individual x,y,radius_x and radius_y values instead of list/array/tuple.            
            - See fill_arc() to draw filled arc. vs. an open/wireframe

            Parameters: 
          
            - pos           \t -- (x,y) Location of the center of the ellipse in the window
            - size          \t -- (Width, Height), in pixels, of the ellipse
            - start_angle   \t -- Where to start drawing the ellipse.   0 degrees is directly right on the X-Axis, with a counter-clockwise rotation (i.e. 90 degrees is top, -90 is bottom)
            - sweep_angle   \t -- How many degrees in a circle to draw the ellipse. 
    
          
            Keywords and/or Pybox options can be included.  Some various options are as follows:
         
            - pen_size      \t - Sets the thickness of the arc.  Otherwise defaults to current Pen Size (which is usually 1), e.g. arc(x,y,rx,ry,"red",pen_size=10)
            - join_type     \t - Used to set how angles on lines are joined.  Default is "miter" can be sharp.  Setting join_type="round" (or "bevel") can make edges softer.
            - line_caps     \t - Sets the 'cap' type for the arc.  By default these are round and the size of the arc line itself.
                            
                            \t Possible linecap values are "flat" (no caps),"round","diamond","square" and "arrow".  use "default" to set default cap type.
                            \t Add "anchor" to make caps larger, e.g. "round anchor","arrow anchor", etc.  ("flat" has no "anchor")
                            
                            \t This sets both cap types unless a ',' is used, such as "round,square anchor".  
                            \t using a blank for the cap type sets the default, such as ",arrow anchor" or "arrow anchor,", which sets only the
                            \t end cap and beginning cap to "anchor arrow", respectively, leaving the other cap type as the default. 
 
                              
            Example: 
            
            draw.arc_l((200,200),(400,50),90,-180,"red") -- Draws an arc based on an ellipse of RadiusX=400, RadiusY = 400.  The 90 starts at the top of the axis. The -180 sweeps from
            this point, creating an arc from the top of the ellipse, rotating clockwise (because the sweep angle is negative) to draw the ellipse down to the bottom of the ellipse.
            """               
            return _pybox.WindowDrawArc(self.__id,pos[0],pos[1],size[0],size[1],start_angle,sweep_angle,arc_color,0,**kwargs)
        
        def fill_arc(self,x , y , radius_x, radius_y, start_angle, sweep_angle , arc_color, **kwargs) :
            """
            Draws an filled Arc in the window.  An 'Arc' is a partial ellipse.  
            The same parameters of Width and Height (or RadiusX and RadiusY) are given. Input angles are in degrees. 
            
            - The filled area is the area between the ends of the arc.
            - See fill_arc_l() to use list/array/tuple for (x,y) and (radiusx,radiusy) values.            
            - See arc() to draw an open/wireframe arc vs. a filled arc.
            
            Parameters: 
         
            - x,y           \t -- Location of the center of the ellipse in the window
            - radius_x      \t -- Width/Radius (in pixels) of the ellipse in the X direction
            - radius_y      \t -- Height/Radius (in pixels) of the ellipse in the Y direction
            - start_angle   \t -- Where to start drawing the ellipse.   0 degrees is directly right on the X-Axis, with a counter-clockwise rotation (i.e. 90 degrees is top, -90 is bottom)
            - sweep_angle   \t -- How many degrees in a circle to draw the ellipse. 
    
          
            Keywords and/or Pybox options can be included.  Some various options are as follows:
         
            - pen_size      \t - Sets the thickness of the arc.  Otherwise defaults to current Pen Size (which is usually 1), e.g. arc(x,y,rx,ry,"red",pen_size=10)
            - join_type     \t - Used to set how angles on lines are joined (if a border/pen is used).  
                            \t   Default is "miter" can be sharp.  Setting join_type="round" (or "bevel") can make edges softer.
            - line_caps     \t - Line caps may be used when a pen is used as a border.  See arc() for more information.
                              
            Example: 
            
            draw.fill_arc(200,200,400,50,90,-180,"red") -- Draws an arc based on an ellipse of RadiusX=400, RadiusY = 400.  The 90 starts at the top of the axis. The -180 sweeps from
            this point, creating an arc from the top of the ellipse, rotating clockwise (because the sweep angle is negative) to draw the ellipse down to the bottom of the ellipse.
            """               
            return _pybox.WindowDrawArc(self.__id,x,y,radius_x,radius_y,start_angle,sweep_angle,arc_color,1,**kwargs)
        
        def fill_arc_l(self,pos : list, size : list, start_angle, sweep_angle, arc_color, **kwargs) :
            """
            Draws a filled arc in the window.  An 'Arc' is a partial ellipse.  The same parameters of Width and Height (or RadiusX and RadiusY) are given. Input angles are in degrees. 
            
            - The filled area is the area between the ends of the arc.
            - See fill_arc() individual values for x,y,radius_x and radius_y, instead of list/array/tuple.           
            - See arc_l() to draw an open/wireframe arc vs. a filled arc.
            
            Parameters: 
          
            - pos           \t -- (x,y) Location of the center of the ellipse in the window
            - size          \t -- (Width, Height), in pixels, of the ellipse
            - start_angle   \t -- Where to start drawing the ellipse.   0 degrees is directly right on the X-Axis, with a counter-clockwise rotation (i.e. 90 degrees is top, -90 is bottom)
            - sweep_angle   \t -- How many degrees in a circle to draw the ellipse. 
    
          
            Keywords and/or Pybox options can be included.  Some various options are as follows:
         
            - pen_size      \t - Sets the thickness of the arc.  Otherwise defaults to current Pen Size (which is usually 1), e.g. arc(x,y,rx,ry,"red",pen_size=10)
            - join_type     \t - Used to set how angles on lines are joined (if a border/pen is used).  
                            \t   Default is "miter" can be sharp.  Setting join_type="round" (or "bevel") can make edges softer.
            - line_caps     \t - Line caps may be used when a pen is used as a border.  See arc() for more information.
 
                              
            Example: 
            
            draw.fill_arc_l((200,200),(400,50),90,-180,"red") -- Draws an arc based on an ellipse of RadiusX=400, RadiusY = 400.  The 90 starts at the top of the axis. The -180 sweeps from
            this point, creating an arc from the top of the ellipse, rotating clockwise (because the sweep angle is negative) to draw the ellipse down to the bottom of the ellipse.
            """               
            return _pybox.WindowDrawArc(self.__id,pos[0],pos[1],size[0],size[1],start_angle,sweep_angle,arc_color,1,**kwargs)
        
        def pie(self,x , y , radius_x, radius_y, start_angle, sweep_angle , arc_color, **kwargs) :
            """
            Draws an open/wireframe pie chart slice, from the center of the ellipse described by RadiusX and RadiusY, from the start angle, for duration of the sweep angle.

            - See pie_l() to use list/array/tuple for (x,y) and (radiusx,radiusy) values.            
            - See fill_pie() to draw filled pie slice. vs. an open/wireframe
            
            Example:
            
            window.draw.pie(200,300,400,400,-75,150,"red") 
            
            This example draws a Pie-Chart slice centered at (200,200), with radius_x and radius_y of 400 (i.e. a circle),
            with a start angle of -75 degrees, for a duration of 150 degrees.

            0 Degrees starts directly to the right of the center of the ellipse/circle and moves in a clockwise direction.  
            In the example above, this will draw a pie slice from the center of the circle, to the upper-right starting at -75 degrees, extending 
            the same amount below the Y axis (since it is 150 degrees in length). 
            
            Parameters: 
         
            - x,y           \t -- Location of the center of the ellipse in the window
            - radius_x      \t -- Width/Radius (in pixels) of the ellipse in the X direction
            - radius_y      \t -- Height/Radius (in pixels) of the ellipse in the Y direction
            - start_angle   \t -- Where to start drawing the ellipse.   0 degrees is directly right on the X-Axis, with a counter-clockwise rotation (i.e. 90 degrees is top, -90 is bottom)
            - sweep_angle   \t -- How many degrees in a circle to draw the ellipse. 
    
          
            Keywords and/or Pybox options can be included.  Some various options are as follows:
         
            - pen_size      \t - Sets the thickness of the pie slice.  Otherwise defaults to current Pen Size (which is usually 1).
            - join_type     \t - Used to set how angles on lines are joined.  Default is "miter" can be sharp.  Setting join_type="round" (or "bevel") can make edges softer.
            - line_caps      \t - Sets the 'cap' type for the pie slice.  By default these are round and the size of the pie slice line itself.
                            
                            \t Possible linecap values are "flat" (no caps),"round","diamond","square" and "arrow".  use "default" to set default cap type.
                            \t Add "anchor" to make caps larger, e.g. "round anchor","arrow anchor", etc.  ("flat" has no "anchor")
                            
                            \t This sets both cap types unless a ',' is used, such as "round,square anchor".  
                            \t using a blank for the cap type sets the default, such as ",arrow anchor" or "arrow anchor,", which sets only the
                            \t end cap and beginning cap to "anchor arrow", respectively, leaving the other cap type as the default. 
              """               
            return _pybox.WindowDrawArc(self.__id,x,y,radius_x,radius_y,start_angle,sweep_angle,arc_color,2,**kwargs)
        
        def pie_l(self,pos : list, size : list, start_angle, sweep_angle, arc_color, **kwargs) :
            """
            Draws an open/wireframe pie chart slice, from the center of the ellipse described by RadiusX and RadiusY, from the start angle, for duration of the sweep angle.

            - See pie() to use individual values for x,y,radius_x, and radius_y, instead of list/array/tuple.       
            - See fill_pie_l() to draw filled pie slice. vs. an open/wireframe
            
            Example:
            
            window.draw.pie_l((200,300),(400,400),-75,150,"red") 
            
            This example draws a Pie-Chart slice centered at (200,200), with radius_x and radius_y of 400 (i.e. a circle),
            with a start angle of -75 degrees, for a duration of 150 degrees.

            0 Degrees starts directly to the right of the center of the ellipse/circle and moves in a clockwise direction.  
            In the example above, this will draw a pie slice from the center of the circle, to the upper-right starting at -75 degrees, extending 
            the same amount below the Y axis (since it is 150 degrees in length). 
            
            Parameters: 
         
            - pos           \t -- (x,y) Location of the center of the ellipse in the window
            - size          \t -- (Width, Height), in pixels, of the ellipse
            - start_angle   \t -- Where to start drawing the ellipse.   0 degrees is directly right on the X-Axis, with a counter-clockwise rotation (i.e. 90 degrees is top, -90 is bottom)
            - sweep_angle   \t -- How many degrees in a circle to draw the ellipse. 
    
          
            Keywords and/or Pybox options can be included.  Some various options are as follows:
         
            - pen_size      \t - Sets the thickness of the pie slice.  Otherwise defaults to current Pen Size (which is usually 1).
            - join_type     \t - Used to set how angles on lines are joined.  Default is "miter" can be sharp.  Setting join_type="round" (or "bevel") can make edges softer.
            - line_caps      \t - Sets the 'cap' type for the pie slice.  By default these are round and the size of the pie slice line itself.
                            
                            \t Possible linecap values are "flat" (no caps),"round","diamond","square" and "arrow".  use "default" to set default cap type.
                            \t Add "anchor" to make caps larger, e.g. "round anchor","arrow anchor", etc.  ("flat" has no "anchor")
                            
                            \t This sets both cap types unless a ',' is used, such as "round,square anchor".  
                            \t using a blank for the cap type sets the default, such as ",arrow anchor" or "arrow anchor,", which sets only the
                            \t end cap and beginning cap to "anchor arrow", respectively, leaving the other cap type as the default. 
            """               
            return _pybox.WindowDrawArc(self.__id,pos[0],pos[1],size[0],size[1],start_angle,sweep_angle,arc_color,2,**kwargs)
        
        def fill_pie(self,x , y , radius_x, radius_y, start_angle, sweep_angle , arc_color, **kwargs) :
            """
            Draws an filled pie chart slice, from the center of the ellipse described by RadiusX and RadiusY, from the start angle, for duration of the sweep angle.

            - See fill_pie() to use list/array/tuple for x,y,radius_x, and radius_y, rather than invidual values.       
            - See pie() to draw an open/wireframe pie slice vs. a filled pie slice.
            
            Example:
            
            window.draw.fill_pie(200,300,400,400,-75,150,"red") 
            
            This example draws a Pie-Chart slice centered at (200,200), with radius_x and radius_y of 400 (i.e. a circle),
            with a start angle of -75 degrees, for a duration of 150 degrees.

            0 Degrees starts directly to the right of the center of the ellipse/circle and moves in a clockwise direction.  
            In the example above, this will draw a pie slice from the center of the circle, to the upper-right starting at -75 degrees, extending 
            the same amount below the Y axis (since it is 150 degrees in length). 
            
            Parameters: 
         
            - x,y           \t -- Location of the center of the ellipse in the window
            - radius_x      \t -- Width/Radius (in pixels) of the ellipse in the X direction
            - radius_y      \t -- Height/Radius (in pixels) of the ellipse in the Y direction
            - start_angle   \t -- Where to start drawing the ellipse.   0 degrees is directly right on the X-Axis, with a counter-clockwise rotation (i.e. 90 degrees is top, -90 is bottom)
            - sweep_angle   \t -- How many degrees in a circle to draw the ellipse. 
            
            Keywords and/or Pybox options can be included.  Some various options are as follows:
         
            - pen_size      \t - Sets the thickness of the pie slice.  Otherwise defaults to current Pen Size (which is usually 1).
            - join_type     \t - Used to set how angles on lines are joined (if a border/pen is used).  
                            \t   Default is "miter" can be sharp.  Setting join_type="round" (or "bevel") can make edges softer.
            - line_caps     \t - Line caps may be used when a pen is used as a border.  See pie() for more information.
            """               
            return _pybox.WindowDrawArc(self.__id,x,y,radius_x,radius_y,start_angle,sweep_angle,arc_color,3,**kwargs)
        
        def fill_pie_l(self,pos : list, size : list, start_angle, sweep_angle, arc_color, **kwargs) :
            """
            Draws an filled pie chart slice, from the center of the ellipse described by RadiusX and RadiusY, from the start angle, for duration of the sweep angle.

            - See fill_pie() to use individual values for x,y,radius_x, and radius_y, rather than list/array/tuple values     
            - See pie_l() to draw an open/wireframe pie slice vs. a filled pie slice.
            
            Example:
            
            window.draw.fill_pie_l((200,300),(400,400),-75,150,"red") 
            
            This example draws a Pie-Chart slice centered at (200,200), with radius_x and radius_y of 400 (i.e. a circle),
            with a start angle of -75 degrees, for a duration of 150 degrees.

            0 Degrees starts directly to the right of the center of the ellipse/circle and moves in a clockwise direction.  
            In the example above, this will draw a pie slice from the center of the circle, to the upper-right starting at -75 degrees, extending 
            the same amount below the Y axis (since it is 150 degrees in length). 
            
            Parameters: 
         
            - pos           \t -- (x,y) Location of the center of the ellipse in the window
            - size          \t -- (Width, Height), in pixels, of the ellipse
            - start_angle   \t -- Where to start drawing the ellipse.   0 degrees is directly right on the X-Axis, with a counter-clockwise rotation (i.e. 90 degrees is top, -90 is bottom)
            - sweep_angle   \t -- How many degrees in a circle to draw the ellipse. 
            
            Keywords and/or Pybox options can be included.  Some various options are as follows:
         
            - pen_size      \t - Sets the thickness of the pie slice.  Otherwise defaults to current Pen Size (which is usually 1).
            - join_type     \t - Used to set how angles on lines are joined (if a border/pen is used).  
                            \t   Default is "miter" can be sharp.  Setting join_type="round" (or "bevel") can make edges softer.
            - line_caps     \t - Line caps may be used when a pen is used as a border.  See pie() for more information.
            """               
            return _pybox.WindowDrawArc(self.__id,pos[0],pos[1],size[0],size[1],start_angle,sweep_angle,arc_color,3,**kwargs)
 

        #
        # Draw Line Functions
        #

        def line_fast(self,x1 : int,y1 : int,x2 : int,y2 : int,color,pen_size : int = 0) : 
            """
            Draws a 'fast' line in the window from (x1,y1) to (x2,y2).  See DrawLine_l() to use list/array/tuple for (x,y) coordinates. 

            This drawing function is a 'fast' function that does not use anti-aliasing and is about 10x faster than
            non-fast drawing functions.  These functions are useful for general drawing and do not respond to opacity or transformations.

            Parameters:

            - color         \t -- Color to use for drawing the line

            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()
            """
            return _pybox.WindowDrawLineFast(self.__id,int(x1),int(y1),int(x2),int(y2),color,pen_size)    

        def line_fast_l(self,p1 : list, p2 : list,color,pen_size : int = 0) : 
            """
            Draws a 'fast' line in the window from (x1,y1) to (x2,y2).  See DrawLine() to use individual x,y coordinates.

            This drawing function is a 'fast' function that does not use anti-aliasing and is about 10x faster than
            non-fast drawing functions.  These functions are useful for general drawing and do not respond to opacity or transformations.

            Parameters:

            - color         \t -- Color to use for drawing the line

            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()
            """
            return _pybox.WindowDrawLineFast(self.__id,int(p1[0]),int(p1[1]),int(p2[0]),int(p2[1]),color,pen_size)
    

        def lineto_fast(self,x1 : int,y1 : int,color,pen_size : int = 0) : 
            """
            Draws a 'fast' line in the window from the current point (last line or Set Point).  See DrawLineToL() to use list, tuple, or array for x,y starting point.

            This drawing function is a 'fast' function that does not use anti-aliasing and is about 10x faster than
            non-fast drawing functions.  These functions are useful for general drawing and do not respond to opacity or transformations.

            Parameters:

            - color         \t -- Color to use for drawing the line

            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()
            """
            return _pybox.WindowDrawLineToFast(self.__id,int(x1),int(y1),color,pen_size)

        def lineto_fast_l(self,p1 : list,color,pen_size : int = 0) : 
            """
            Draws a 'fast' line in the window from the current point (last line or Set Point).  See DrawLineTo() to use individual x,y coordinates.

            This drawing function is a 'fast' function that does not use anti-aliasing and is about 10x faster than
            non-fast drawing functions.  These functions are useful for general drawing and do not respond to opacity or transformations.

            Parameters:

            - color         \t -- Color to use for drawing the line

            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()
            """        
            return _pybox.WindowDrawLineToFast(self.__id,int(p1[0]),int(p1[1]),color,pen_size)

        # HR Draw Line Functions

        def line_segments(self,Loc : list, color, pen_size = None,array_size : int = 0) -> bool : 
            """
            Draws multiple line segments with one color or one color for each line segment.

            - There must be at least two line segments to draw
            - There can be 0 and 1 line segments specified.  If so, the function is ignored.
            
            Parameters

            - Loc           \t -- A list or array of line segments in (x,y) form.  x and y values may be integer or floating-point values.
            - color         \t -- A single color of color for each line segment (endpoint segment color is used)
            - array_size     \t -- [optional] When given, this is the size of the array to use.  color and Loc must be of at least ArraySize (when ArraySize is specified).
                            \t - When ArraySize is specified, the size of Loc and Color are used (Loc and Color must be of the exact same size when ArraySize is not specified).
            - pen_size       \t - [optional] Pen Size to use for every line.  This is a static value and does not currently support arrays. When omitted, the current pen size is used.
                                \t -See draw.set_pen_size() to set a general pen size rather than specifying it in the function.

            """
            _pybox.WindowDrawLineSegments(self.__id,Loc,color,array_size,pen_size)

        def line(self,x1,y1,x2,y2,color,**kwargs) : 
            """
            Draws a line in the window from (x1,y1) to (x2,y2).  See DrawLineL() to use list/array/tuple for (x,y) coordinates. 

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            Hint: use an odd-size pen_size for sharper edges.

            Parameters:

            - x1,y1         \t -- x,y start (x,y) point
            - x2,y2         \t -- x,y end (x,y) point
            - color         \t -- Color to use for drawing the line
            
            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_size      \t - Pen Size to use for every line. When omitted, the current pen size is used. See draw.set_pen_size() to set a general pen size rather than specifying it in the function. This value may be integer or floating-point.
            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()
            """
            return _pybox.WindowDrawLine(self.__id,x1,y1,x2,y2,color,**kwargs)    

        def line_l(self,p1 : list, p2 : list,color,**kwargs) : 
            """
            Draws a line in the window from (x1,y1) to (x2,y2).  See DrawLine() to use individual x,y coordinates.

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            Hint: use an odd-size pen_size for sharper edges.

            Parameters:

            - p1            \t -- list, array, or tuple of start (x,y) point
            - p2            \t -- list, array, or tuple of end (x,y) point
            - color         \t -- Color to use for drawing the line
            
            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_size      \t - Pen Size to use for every line. When omitted, the current pen size is used. See draw.set_pen_size() to set a general pen size rather than specifying it in the function. This value may be integer or floating-point.

            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()
            """
            return _pybox.WindowDrawLine(self.__id,p1[0],p1[1],p2[0],p2[1],color,**kwargs)
   
        def lineto(self,x1,y1,color,**kwargs) : 
            """
            Draws a line in the window from the current point (last line or Set Point).  See DrawLineToL() to use list, tuple, or array for x,y starting point.

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            Hint: use an odd-size pen_size for sharper edges.

            Parameters:

            - x1,y1         \t -- x,y end point of line.
            - color         \t -- Color to use for drawing the line

            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_size      \t - Pen Size to use for every line. When omitted, the current pen size is used. See draw.set_pen_size() to set a general pen size rather than specifying it in the function. This value may be integer or floating-point.

            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()
            """
            return _pybox.WindowDrawLineTo(self.__id,x1,y1,color,**kwargs)

        def lineto_l(self,p1 : list,color,**kwargs) : 
            """
            Draws a line in the window from the current point (last line or Set Point).  See DrawLineTo() to use individual x,y coordinates.

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            Hint: use an odd-size pen_size for sharper edges.

            Parameters:

            - p1            \t -- list, array, or tuple of end (x,y) point
            - color         \t -- Color to use for drawing the line

            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_size      \t - Pen Size to use for every line. When omitted, the current pen size is used. See draw.set_pen_size() to set a general pen size rather than specifying it in the function. This value may be integer or floating-point.

            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()
            """        
            return _pybox.WindowDrawLineTo(self.__id,p1[0],p1[1],color,**kwargs)

        def lineto_ex(self,first,x1,y1,color,**kwargs) : 
            """
            Draws a line in the window from the current point (last line or Set Point).  See DrawLineToL() to use list, tuple, or array for x,y starting point.

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            Hint: use an odd-size pen_size for sharper edges.

            Parameters:

            - first         \t -- [int or bool] When false (or 0 when an integer), the Line is drawn as a LineTo to the point given
                                \t - when true (or non-zero when an integer), the point is set as the first point, but not drawn.
            - x1,y1         \t -- x,y end point of line.
            - color         \t -- Color to use for drawing the line

            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_size      \t - Pen Size to use for every line. When omitted, the current pen size is used. See draw.set_pen_size() to set a general pen size rather than specifying it in the function. This value may be integer or floating-point.

            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()
            """
            return _pybox.WindowDrawLineToEx(self.__id,first,x1,y1,color,**kwargs)

        def lineto_ex_l(self,first,p1 : list,color,**kwargs) : 
            """
            Draws a line in the window from the current point (last line or Set Point).  See DrawLineTo() to use individual x,y coordinates.

            This drawing function responds to current opacity and transformations and will anti-alias output results.
            Hint: use an odd-size pen_size for sharper edges.

            Parameters:

            - first         \t -- [int or bool] When false (or 0 when an integer), the Line is drawn as a LineTo to the point given
                                \t - when true (or non-zero when an integer), the point is set as the first point, but not drawn.
            - p1            \t -- list, array, or tuple of end (x,y) point
            - color         \t -- Color to use for drawing the line

            Keywords and/or Pybox options can be included.  Some various options are as follows:

            - pen_size      \t - Pen Size to use for every line. When omitted, the current pen size is used. See draw.set_pen_size() to set a general pen size rather than specifying it in the function. This value may be integer or floating-point.

            About Colors

            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()
            """        
            return _pybox.WindowDrawLineToEx(self.__id,first,p1[0],p1[1],color,**kwargs)
        
        def draw_grid(self,spacing : int = 25,**kwargs) -> bool :
            """
            Draws a grid of lines in the X and Y axis to create a graph on the screen.

            The "spacing" parameter controls how many pixels are between each set of lines.
        
            Keywords and Pybox options can be included.  Some various options are as follows:

            - color                       \t -Sets the color of the grid, i.e. "white","red","45,67,123", etc. Default color is RGB(42,42,42) (i.e. dark gray)

            The default for the "spacing" parameter is 25 pixels.

            Examples:
     
            \t -MyWindow.draw_grid()                \t -- Draws default grid
            \t -MyWindow.write(50)                  \t -- Draws a grid with spacing of 50 pixels 
            \t -MyWindow.write("green")             \t -- Draws a grid with the color green
            \t -MyWindow.write(50,"0,255,255")      \t -- Draws a grid with spacing of 50 and an RGB color of (0,255,255) or "cyan"
            """
            return _pybox.WindowDrawGrid(self.__id,spacing,**kwargs)

        def vector(self,p1 : list, p2 : list,line_size,color,**kwargs) : 
            """
            Draws a vector from point p1 to p2.  A vector is the same thing as a line, but with some differences and a number of controls that 
            can be used to modify its behavior and appearance.
        
            The vector also has beginning and end 'caps'.  The default is for the beginning of the line to have a round shape (e.g. round cap), and
            the end of the line to have a larger arrow shape (known as an 'arrow' cap, but because it's larger it's known as an 'arrow anchor')
        
            The default behavior for draw_vector is to draw the vector in a white color, with a round beginning cap and an 'arrow anchor' ending cap.
        
            Input
        
            - p1,p2             - Beginning and End Points of the line, such as (100,400),(600,700) or (x1,y1),(x2,y2), etc.
            - line_size         -size of the line in pixels.
            - color             - color of vector line.
        
            Example of simple usage: window.draw_vector(p1,p2,10) or draw_vector((x1,y1),(x2,y2),10)
        
            Text, colors, and many others may be assign through the following keywords

            - title         - Sets the title to display on the vector line, e.g. title="This is a vector.  Default behavior is no title.
            - opacity       - Sets the opacity to draw the line.  Range is 0-255, with 0 transparent and 255 fully opaque. Default is 255 (fully opaque).
            - angle         - Rotates the vector at its center by the angle specified.  "angle" is in degrees.  "AngleDeg" may also be used to specify degrees
            - angle_rad     - Same as "angle", but uses radians instead of degrees, e.g. angle_rad = 1.57 (for 90 degrees)
            - text_size     - Sets the relative font size of the label.  The default font varies in size based on line thickness. 
                              text_size values can me "xxsmall","xsmall","small","medium","large,"xlarge", "xxlarge".  Default is "small".  "default" may also be used as an option.
        
            - label_font (or "font")    - Sets a specific font size or type for the vector line.  The font will not change based on line thickness when set in this manner.
                                          Fonts may be set with just a size, such as a number, e.g. font=25 (for default font Arial at 25 points), or a full font name, e.g. font="time new roman,25"
        
            - label_just (or "just")    - Sets the justification of the vector label text.  Default is "top-left".  
                                          Options are: "top-left","top-left-center","top-center","top-right-center","top-right".  "bottom" and "middle" may be used instead of top to specify the 
                                          bottom of the vector line or middle of the line (vertically), respectively.  Example: just="bottom-right"

            - capsize       - Sets the beginning and end cap of the vector to a multiple of the capsize specified.  This is useful only for 'anchor' cap types
                              such as 'round achor', 'arrow anchor',etc.  The anchor types grow and shrink based on line thickness.
                              using "capsize" can make the beginning and end caps smaller or larger.
                              example capize=2 makes any anchor cap 2x larger.  see "begcapsize" and "endcapsize" to control cap sizes individually.

            - begcap_size (or "begcap")   - Sets the begininng cap size if the begnining cap is an 'anchor' cap type.  See documentation on 'capsize', which will set both
                                            beginning and end cap together.
                          
            - endcap_size (or "endcap")  - Sets the end cap size if the end cap is an 'anchor' cap type.  See documentation on 'capsize', which will set both
                                           beginning and end cap together.
 
            - begcap_type       - Sets the beginning cap type.  by default, the cap type for the begining of the vector is "round"
                                  possible types are "round","diamond","arrow","square","flat","round anchor","diamond anchor","arrow anchor","diamond anchor"
                                  "anchor" types are larger and can be made smaller or larger with "capsize" or "begcap_size"
                                       
            - endcap_type       - Sets the ending cap type.  by default, the cap type for the enf of the vector is "arrow anchor"
                                  possible types are "round","diamond","arrow","square","flat","round anchor","diamond anchor","arrow anchor","diamond anchor"
                                  "anchor" types are larger and can be made smaller or larger with "capsize" or "begcap_size"
            - begcap_color      - Sets the color of the beginning cap of the vector.  This is useful for "anchor" cap types which are larger.  
                                  Example: begcap_color="yellow"                             
            - endcap_color      - Sets the color of the ending cap of the vector.  This is useful for "anchor" cap types which are larger.  
                                  By default, the begining and end caps are the same color as the vector line itself.  Example: endcap_color="red"  
            - label_pad_x (or "pad_x")  - Sets extra spacing on the left or right of the label on the vector.  Positive values move the title to the right
                                          (as formed by p1-p2), with negative values moving the title to the left.
            - label_pad_y (or "pad_y")  - Sets extra spacing on the top or bottom of the label on the vector.  Positive values move the title upwards
                                          (as formed by p1-p2), with negative values moving the title downward.
            - label_opacity     - Sets the opacity of the vector's label.  By default, the opacity of the vector label is the same as the line, either by default or
                                  when the line opacity is specifically specified.  Using label_opacity will cause the label's opacity to use this value.
            - label_color   - Sets the color of the vector label, e.g. label_color="red".  By default, the label's color is white, regardless of the line color.
            - label_angle   - Sets the label of the angle with 3 options: "horizontal" (default), "vertical", or "vertical 180".  "vertical" and vertical 180" make the label
                              appear sideways on the line, with "vertial 180" reversing it's direction, with the start of the text appearing away from the line.
                              Add the term "static" to keep the label the exact orientation regardless of line angle, e.g. 'label_angle="horizontal,static"' will cause
                              the text to display at 0 degrees relative to the screen rather than the line itself.
                          
            - label_up      - Keeps the vector's label right-side up. As the vector rotates and the label's orientation, using "label_up=True" will keep the label
                              right-side up when the label's angle is such that the label would otherwise appear upside-down.
            - set_center    - Sets the center of the vector, regardless of p1 and p2.  This calculates the relative center of the vector (i.e. (p1+p2)/2-p1), and
                              places the center of the vector at the new (x,y) coordinates.  Example set_center=(500,200) or set_center=(x,y)
                              This is useful in simply specifying a length in the draw_vector call as p1 and p2, such as draw_vector((0,0),(0,x),...) then
                              setting the center and angle of the vector with "set_canter" and "angle" keywords, respectively/
            - show_center   - puts a circle in the center of the vector.  This is for purely diagnostic purposes, showing the center is where it should be based on 
                              the calling's functions calculation.  Use "show_center=True" to show the circle in cyan.  
                              Use "show_center=<color>" to set the color, e.g. 'show_center="black"'
            """
            return _pybox.WindowDrawVector(self.__id,p1[0],p1[1],p2[0],p2[1],line_size,color,**kwargs)
    
        def set_pixel(self,x : int, y : int, color : any) :
            """
            Draws a single RGB pixel in the window at point specified by x,y
  
            see: set_pixel_l() to use list, tuples, or arrays for the x,y location
            
            Parameters

            x,y   \t- location to place pixel inside of window
            color \t- RGB color of pixel 
            
            Color may be 3-value integer or float in a list, tuple, or array,
            e.g. (255,255,0) for yellow, etc.
            
            note: Colors using strings such as "yellow", "green", etc. may cause slowness when outputting numerous pixels.
            """
            return _pybox.WindowDrawPixel(self.__id,x,y,color)
           
        def set_pixel_l(self,at, color : any) :
            """
            Draws a single RGB pixel in the window at point specified by x,y
  
            see: set_pixel() to use individual x,y values instead of tuple/list/array
            
            Parameters

            at  \t- location to place pixel inside of window
            color \t- RGB color of pixel 
            
            About Colors

            Color may be 3-value integer or float in a list, tuple, or array, e.g. (255,255,0) for yellow, etc.
            
            Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
            Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()
            
            note: Colors using strings such as "yellow", "green", etc. may cause slowness when outputting numerous pixels.
            """
            return _pybox.WindowDrawPixel(self.__id,at[0],at[1],color)
           
          
        

    #
    # Main Window Class Functions
    #

    def exit_button(self,text : str = None) -> bool : 
        """
        exit_button() puts a button at the bottom of the window and waits for the user to press it or the Return Key.
    
        exit_button() is quick way to let the user know that the program has ended.

        See pybox.exit_button() to bring up an exit button in a separate window with a message.
        Parameters

        - text       \t -- [optional].  Message to put in the window above the button.  If not specified, a default "program is finished" message is place in the window.

        About exit_button() and Displays using Windows and Graphics

        The exit_button() gives a way to pause the program before it ends so that the Windows and Graphics displaying don't suddenly disappear. 

        Whether Python, C++, or other languages, the Console Window is not part of the running application.  It is a separate application to which the running program is a client.
        When the program closes down, this other application (a separate process entirely) simply lets you know the program has ended.

        When windows and graphics are displayed in your program, and the program ends, it all disappears suddenly.  In a program with a Console Mode box, this will show a "program has ended"
        message in the box.  In a Windows application, the program will just "disappear"

        You can use exit_button() as a nice, quick method to pause and let the user know the program is ending in a GUI/graphical method.
    
        """
        return _pybox.WindowExitButton(self.__id,text)

    def set_write_indent(self,indent) -> bool :
        """
        Sets the horizontal Write Indent when writing to the window.

        When set to a value, every newline (\n) will set the write position to the next line at the indent given.
        This function can be useful when writing multiple lines of text indented into the window.

        For example,

        \t -MyWindow.set_write_indent(20)

        will set all new lines at position 20. 

        Use set_write_indent(0) to reset the indent. 

        """
        return _pybox.WindowSetWriteIndent(self.__id,indent)

    def set_write_padding(self,padding) -> bool :    
        """
        Sets the vertical padding between lines (i.e. "\n") when writing to the window.

        The default setting is to start a new line a position in the next line just underneath the last line, based on the size of the font.

        When the write padding is a non-zero value, this value is added to each line.

        For example,

        \t -MyWindow.set_write_padding(5)

        will add 5 extra pixels for every newline on top of the size of the font.

        Use set_write_padding(0) to reset the vertical write padding.
        """
        return _pybox.WindowSetWritePadding(self.__id,padding)

 

    def set_write_pos(self,x,y) -> bool :
        """
        See set_write_pos_l() to use a list, tuple, or array to set the write position. 

        Sets the next write position in the window when using the Window.write() function.

        For example,

        \t -MyWindow.set_write_pos(50,100)

        will cause the next Window.Write() output to start at (50,100). 

        Note: the next newline ("\n") seen will reset the horizontal value to the beginning of the line or current Indent setting.

        See set_write_indent() to sent an indent.  For example, set_write_indent(50) would set each newline column to 50.
        """
        return _pybox.WindowSetWritePos(self.__id,int(x),int(y))     

    def set_write_pos_l(self,at : list) -> bool :
        """
        See set_write_pos() to use independent values to set the write position instead of a list, tuple, or array to set the write position. 

        Sets the next write position in the window when using the Window.write() function.

        For example,

        \t -MyWindow.set_write_pos_l((50,100))

        will cause the next Window.Write() output to start at (50,100). 

        Note: the next newline ("\n") seen will reset the horizontal value to the beginning of the line or current Indent setting.

        See set_write_indent() to sent an indent.  For example, set_write_indent(50) would set each newline column to 50.
        """        
        return _pybox.WindowSetWritePos(self.__id,int(at[0]),int(at[1]))
    
    def set_write_pos_x(self,x) -> bool :
        """
        Sets the next horizontal write position while keeping the current vertical write position.

        After using set_write_pos_x(), the next output from Window.write() will be at this horizonal position (at the same current vertical position).
        """
        return _pybox.WindowSetWritePosX(self.__id,int(x))

    def set_bg_color(self,color) -> bool :
        """
        Sets the background color of the window.  This will set the next text to display at the color specified.

        See Cls() to clear and change the entire background.
        After using set_bg_color(), the next cls() will clear the background to this color, unless a clsbitmap() has been set.

        Note: The Window must be set as Opaque.  Otherwise the set_bg_color will not have an effect until a cls() is used.
        
        Parameters

        - color         \t -- Background color to set next text output 
        
        About Colors

        Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
        Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

        Examples:

        Window.set_bg_color("red")                      \t -- Sets the window's background color to the color red
        Window.set_bg_color(SageColor.Red())            \t -- Sets the window's background color to red, also
        Window.set_bg_color(PanColor.ForestGreen())     \t -- Sets the window's background color to PanColor.ForestGreen
        Window.set_bg_color(MyColor)                    \t -- Sets the window's background color to a defined "MyColor", such as MyColor = pybox.RgbColor(0,255,0)
        """
        return _pybox.WindowSetBgColor(self.__id,color)

    def set_fg_color(self,color) -> bool :
        """
        Sets the foreground/text color of the text written to the window.

        This only affects subsequent text written to the window with the write() or other window write functions.
        This will not affect any current display on the window
       
        Note: set_fg_color() and set_text_color() are the same function.
        
        Parameters

        - color         \t -- Foreground/Text color to set next output 
        
        About Colors

        Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
        Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

        Examples:

        Window.set_fg_color("red")                      \t -- Sets the window's text color to the color red
        Window.set_fg_color(SageColor.Red())            \t -- Sets the window's text color to red, also
        Window.set_fg_color(PanColor.ForestGreen())     \t -- Sets the window's text color to PanColor.ForestGreen
        Window.set_fg_color(MyColor)                    \t -- Sets the window's text color to a defined "MyColor", such as MyColor = pybox.RgbColor(0,255,0)
        """        
        return _pybox.WindowSetFgColor(self.__id,color)

    def set_text_color(self,color) -> bool :
        """
        Sets the foreground/text color of the text written to the window.

        This only affects subsequent text written to the window with the Write() or other window write functions.
        This will not affect any current display on the window
       
        Note: set_fg_color() and set_text_color() are the same function.
        
        Parameters

        - color         \t -- Foreground/Text color to set next output 
        
        About Colors

        Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
        Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

        Examples:

        Window.set_text_color("red")                      \t -- Sets the window's text color to the color red
        Window.set_text_color(SageColor.Red())            \t -- Sets the window's text color to red, also
        Window.set_text_color(PanColor.ForestGreen())     \t -- Sets the window's text color to PanColor.ForestGreen
        Window.set_text_color(MyColor)                    \t -- Sets the window's text color to a defined "MyColor", such as MyColor = pybox.RgbColor(0,255,0)
        """
        return _pybox.WindowSetFgColor(self.__id,color)

    def vsync_wait(self) -> bool :
        """
        Waits for the vertical sync to occur before returning. 

        This function can be useful for real-time graphics to sync on the vertical refresh.

        See the pybox GPU/SDL functions (TBD, but being worked on) for accurate and more flexible GPU graphics.
        """
        return _pybox.WindowVSyncWait(self.__id)

    def vsync_ready(self) -> bool :
        """
        Returns True if the vertical retrace has occured. 

        When this function is used once  (or VsynStartThread()) has been called, Sagebox will return with GetEvent() with 
        VsyncReady as an event, which can be checked with VsyncReady(). 

        - Use VsyncEndThread() to stop the thread that looks for the vertical sync. 
    
        When GetEvent() returns, it may return from any sort of event, so VsyncReady() must be called to ensure a Vsync has occured.
   
        - Use VsyncWait() to stop the thread and wake it up every Vsync period (usually every 60ms, but dependent on monitor settings).
            \t -if the code between VsyncWait() calls takes longer then the vertical sync, VsyncWait() will come back when the next vertical sync is triggered.
 
        See the pybox GPU/SDL functions (TBD, but being worked on) for accurate and more flexible GPU graphics.

            --> This function an EVENT function: This function will only return a True value ONE TIME PER EVENT 
            --> and will return False after the first call until the event occurs again. 

                In most events, you can specify "peek=true" as a parameter so that the event will not be reset.

        """
        return _pybox.WindowVSyncReady(self.__id)
    
    def new_listbox(self,x : int, y : int = None,text=None,width=200,height=400,*args,**kwargs) -> Listbox :
        """
        Creates a list box at location x,y. See: new_listbox_l() to specifically use a list/tuple for the (X,Y) position.

        Optional Input parameters:

        - text      \t -- Initial listbox text.  This can be empty.  Multiple entries can be set separated by newlines (i.e. "Item 1\Item 2") listbox.AddItem() can also be used to add text items.
        - width     \t -- Sets the width of the listbox in the window.  This has a default of 200
        - height    \t -- Sets the Height of of the listbox in the window.  This has a default of 400

        Keywords and/or Pybox options can be included.  Some various options are as follows:

        - fgColor   \t -- Sets the foreground color of items in the list box
        - bgColor   \t -- Sets the background color of items in the list box
        - Defalut   \t -- Sets the default selected item (assuming text is set in the initilization).  See: listbox.SetSelection()
        - Font      \t -- Sets the font of the listbox text.   The default is about 12 points. 

        Note: The list box height is automatically adjusted to the nearest font size that will fit into the window. 

        Examples:   \t -MyListbox = Window.new_listbox(10,10)    \t - - Open new listbox at (10,10) in the window
                    \t -MyListbox = Window.new_listbox(PosX,PosY,"Item 1\\nItem 2",fgcolor="Red")  
        """
        return Listbox(_pybox.WindowNewListbox(self.__id,int(x),int(y),text,opt.size(width,height),*args,**kwargs))

    def new_listbox_l(self,loc : list,text=None,width=200,height=400,*args,**kwargs) -> Listbox :
        """
        Creates a list box at location loc. See: new_listbox() to specifically use a (x,y) values to create a listbox.

        Optional Input parameters:

        - text      \t -- Initial listbox text.  This can be empty.  Multiple entries can be set separated by newlines (i.e. "Item 1\Item 2") listbox.AddItem() can also be used to add text items.
        - width     \t -- Sets the width of the listbox in the window.  This has a default of 200
        - height    \t -- Sets the Height of of the listbox in the window.  This has a default of 400

        Pybox options can be included.  Some various options are as follows:

        - fgColor   \t -- Sets the foreground color of items in the list box
        - bgColor   \t -- Sets the background color of items in the list box
        - Defalut   \t -- Sets the default selected item (assuming text is set in the initilization).  See: listbox.SetSelection()
        - Font      \t -- Sets the font of the listbox text.   The default is about 12 points. 

        Note: The list box height is automatically adjusted to the nearest font size that will fit into the window. 

        Examples:   \t -MyListbox = Window.new_listbox_l((10,10))                                          \t - - Open new listbox at (10,10) in the window
                    \t -MyListbox = Window.new_listbox_l(MyLocation,"Item 1\\nItem 2",opt.fgcolor("Red"))  
                    \t -MyListbox = Window.new_listbox_l(MyLocation,"Item 1\\nItem 2",height=300,fgcolor="Red")  
        """        
        return Listbox(_pybox.WindowNewListbox(self.__id,int(loc[0]),int(loc[1]),text,opt.size(width,height),*args,**kwargs))

    def new_button(self,x : int, y : int,title : str,*args,**kwargs) -> Button :
        """
        Create a Button at (x,y) in the Window.  See new_button_l() to use a list/tuple for to set the location.

        A Button type object is returned so the button can be used and events retrieved.

        Parameters:

        title       \t -- Sets the text of the button. 

        Keywords and Pybox options can be included.  Some various options are as follows:

        - fgColor   \t -- Sets the foreground color of items in the list box
        - font      \t -- Sets the font of the button text.   The default is about 12 points. 
        - style     \t -- Style("large") will create a larger button
                    \t -- Style("Windows") will create a windows-style rectangular button
                    \t -- Style("Panel") will create a rectangular button that blends with the window
                    \t -- Style("Panel2") will create a rectangular button that blends with no depth when pressing.
                    \t -- Style("<mystyle>") will create a button of a style that has been created by the program with CreateButtonStyle()

                    \t -With "Windows","Panel" and "Panel2" styles, setting the text color and background color (with opt.fgcolor() and opt.bgcolor()
                    \t -can make a big difference.

        Examples:   \t -MyWindow.new_button(40,100,"This is a button")
                    \t -MyWindow.new_button(40,100,"This is a larger button",opt.font(20),opt.style("Windows"))
                    \t -MyWindow.new_button(40,100,"This is a larger button with red foreground",opt.bgcolor("Red"),opt.style("Panel"))
        """
        return Button(_pybox.WindowNewButton(self.__id,title,int(x),int(y),*args,**kwargs))

    def new_button_l(self,at : list,title : str, *args, **kwargs) -> Button :
        """
        Create a Button at (at) in the Window, where 'at' is a list, tuple or array.  See new_button to use (x,y) values to set the location.

        A Button type object is returned so the button can be used and events retrieved.

        Parameters:

        title       \t -- Sets the text of the button. 

        Keywords and Pybox options can be included.  Some various options are as follows:

        - fgColor   \t -- Sets the foreground color of items in the list box
        - Font      \t -- Sets the font of the button text.   The default is about 12 points. 
        - Style     \t -- Style("large") will create a larger button
                    \t -- Style("Windows") will create a windows-style rectangular button
                    \t -- Style("Panel") will create a rectangular button that blends with the window
                    \t -- Style("Panel2") will create a rectangular button that blends with no depth when pressing.
                    \t -- Style("<mystyle>") will create a button of a style that has been created by the program with CreateButtonStyle()

                    \t -With "Windows","Panel" and "Panel2" styles, setting the text color and background color (with opt.fgcolor() and opt.bgcolor()
                    \t -can make a big difference.

        Examples:   \t -MyWindow.new_button_l(40,100,"This is a button")
                    \t -MyWindow.new_button_l(40,100,"This is a larger button",opt.font(20),opt.style("Windows"))
                    \t -MyWindow.new_button_l(40,100,"This is a larger button with red foreground",opt.bgcolor("Red"),opt.style("Panel"))
        """
        return Button(_pybox.WindowNewButton(self.__id,title,int(at[0]),int(at[1]),*args,**kwargs))

    def new_slider(self,x : int, y : int,title : str,width : int = None,*args,**kwargs) -> Slider :
        """
        Creates a slider at the (x,y) position in the Window. See: new_slider_l() to use a list/tuple for the (x,y) position.

        A Slider class object is returned where the slider can be accessed and controlled. 

        Parameters:

        - title     \t -- Sets the title of the Slider
        - width     \t -- [optional] Sets the width of the slider.  This defaults to about 200 pixels in width.

        Keywords and Pybox options can be included.  Some various options are as follows:

        - Range             \t -- Set the range of the slider.  The default range is (1,100)          
        - Default           \t -- Set the default value of the slider.  The edfault is (0)
        - TextColor         \t -- Sets the color of the label of the slider.
        - ValueColor        \t -- Sets the text color of the value (same as fgColor()
        - Style("small")    \t -- Sets a smaller slider handle

        Examples:       \t -window.new_slider(10,10,"This is a slider")
                        \t -window.new_slider(x,y,"This is a slider",range=(100,500),default=200)
                        \t -window.new_slider(10,10,"This is a slider",opt.textcolor("Yellow"),opt.valuecolor("red"),opt.style("small"))
                        \t -window.new_slider(10,10,"This is a slider",textcolor=Yellow,valuecolor=red,Style="small")        \t - - (same as previous example)
        """
        return Slider(_pybox.WindowNewSlider(self.__id,title,int(x),int(y),width,*args,**kwargs))

    def new_slider_f(self,x : int, y : int,title : str,width : int = None,*args,**kwargs) -> Slider :
        """
        Creates a floating-point slider at the (x,y) position in the Window. See: new_slider_fl() to use a list/tuple for the (x,y) position.

        A Slider class object is returned where the slider can be accessed and controlled. 
        A floating-point slider sets a default range of 0-1.0

        User slider.get_pos_f() and slider.set_pos_f() to set and retrieve values.

        Range may be either direction (i.e. min,max or max, min). 

        Parameters:

        - title     \t -- Sets the title of the Slider
        - width     \t -- [optional] Sets the width of the slider.  This defaults to about 200 pixels in width.

        Pybox options can be included.  Some various options are as follows:

        - Range             \t -- Set the range of the slider.  The default range is (1,1.0)          
        - Default           \t -- Set the default value of the slider.  The edfault is (0)
        - TextColor         \t -- Sets the color of the label of the slider.
        - ValueColor        \t -- Sets the text color of the value (same as fgColor()
        - Style("small")    \t -- Sets a smaller slider handle

        Examples:       \t -window.new_slider_f(10,10,"This is a slider")
                        \t -window.new_slider_f(x,y,"This is a slider",range=(1,5),default=2.5)
                        \t -window.new_slider_f(10,10,"This is a slider",opt.textcolor("Yellow"),opt.valuecolor("red"),opt.style("small"))
                        \t -window.new_slider_f(10,10,"This is a slider",textcolor=Yellow,valuecolor=red,Style="small")        \t - - (same as previous example)

        """
        return Slider(_pybox.WindowNewSlider(self.__id,title,int(x),int(y),width,opt._opt__as_float(),*args,**kwargs))

    def new_slider_l(self,at : list, title : str,width : int = None,*args,**kwargs) -> Slider :
        """
        Creates a slider at the (at) position in the Window. See: new_slider() to use a (x,y) values to set the location of the slider

        A Slider class object is returned where the slider can be accessed and controlled. 

        Parameters:

        - title     \t -- Sets the title of the Slider
        - width     \t -- [optional] Sets the width of the slider.  This defaults to about 200 pixels in width.

        Keywords and Pybox options can be included.  Some various options are as follows:

        - Range             \t -- Set the range of the slider.  The default range is (1,100)          
        - Default           \t -- Set the default value of the slider.  The edfault is (0)
        - TextColor         \t -- Sets the color of the label of the slider.
        - ValueColor        \t -- Sets the text color of the value (same as fgColor()
        - Style("small")    \t -- Sets a smaller slider handle

        Examples:       \t -window.new_slider_l((10,10),"This is a slider")
                        \t -window.new_slider_l(MyLocation,"This is a slider",range=(100,500),default=200)
                        \t -window.new_slider_l((10,10),"This is a slider",opt.textcolor("Yellow"),opt.valuecolor("red"),opt.style("small"))
                        \t -window.new_slider_l((10,10),"This is a slider",textcolor=Yellow,valuecolor=red,Style="small")        \t - - (same as previous example)
        """        
        return Slider(_pybox.WindowNewSlider(self.__id,title,at[0],at[1],width,*args,**kwargs))

    def new_slider_fl(self,at : list, title : str,width : int = None,*args,**kwargs) -> Slider :
        """
        Creates a floating-point slider at the (at) position in the Window. 
        See: new_slider_f() to use a (x,y) values to set the location of the slider

        A Slider class object is returned where the slider can be accessed and controlled. 
        A floating-point slider sets a default range of 0-1.0

        User slider.get_pos_f() and slider.set_pos_f() to set and retrieve values.

        Range may be either direction (i.e. min,max or max, min). 

        Parameters:

        - title     \t -- Sets the title of the Slider
        - width     \t -- [optional] Sets the width of the slider.  This defaults to about 200 pixels in width.

        Keywords and Pybox options can be included.  Some various options are as follows:

        - Range             \t -- Set the range of the slider.  The default range is (1,1.0)          
        - Default           \t -- Set the default value of the slider.  The edfault is (0)
        - TextColor         \t -- Sets the color of the label of the slider.
        - ValueColor        \t -- Sets the text color of the value (same as fgColor()
        - Style("small")    \t -- Sets a smaller slider handle

        Examples:       \t -window.new_slider_fl((10,10),"This is a slider")
                        \t -window.new_slider_fl(MyLocation,"This is a slider",range=(1,2),default=2.5)
                        \t -window.new_slider_fl((10,10),"This is a slider",opt.textcolor("Yellow"),opt.valuecolor("red"),opt.style("small"))
                        \t -window.new_slider_fl((10,10),"This is a slider",textcolor=Yellow,valuecolor=red,Style="small")        \t - - (same as previous example)
        """        
        return Slider(_pybox.WindowNewSlider(self.__id,title,at[0],at[1],width,*args,**kwargs))
    
    def text_widget(self, x : int = 0, y: int = 0,text : str = None,width : int = 0, height : int = 0, *args, **kwargs ) -> CTextWidget :
        """
        Create a text widget in the window at (x,y).   See: text_widget_l() to create a text widget using a list or tuple for the (x,y) position.

        Parameters:

        - text          \t -- [optional] Sets the text of the widget.  This can be set later with textwidget.Write()
                        \t - When text is entered, the text widget is created to the width of the text.  Use the width() parameter to set a width or pad
                        \t - the text with spaces to reserve width.
        - width         \t - [optional] Sets the width of the text widget in pixels.  The default is 200 pixels.
        - height        \t - [optional] Sets the height of the text widget in pixels.  The default is the height of the current font or specified font (when opt.font() is used)

        Keywords and Pybox options can be included.  Some various options are as follows:

        - TextColor         \t - Sets the text color of the widget (default is current window text color).  Same as opt.fgcolor()
        - bgColor           \t - Sets the background color of the widget.  The default blends with the window
        - Font              \t - Sets the font of the text in the text widget
        - CenterX,CenterY   \t - Centers the text widget in the window horizontally or vertically, respectively.
        - TextCenter        \t - Centers the text inside of the widget (which can be longer than the text itself).
                                \t - Use TextCenterX() and CenterX() together to make sure text is centered in the window. This is only needed if the Width of the
                                \t - Text Widget and the text have been specificed separately.

        - JustBottomCenter, JustBottomLeft, JustBottomRight, JustTopCenter, JustTopLeft, JustTopRight
        - PadX,PadY     \t - Use thse with the above positioning to move the widget left,right,up, down from automatic placement.
                        \t - For example, using JustBottomCenter() with PadY(-10) will move the text widget away from the bottom,

        Examples:   \t -window.text_widget(10,10,"This is a text Widget",font=(20))
                    \t -window.text_widget(0,50,"This is a text widget",centerx=true) \t - Centers Text Widget horizontally
                    \t -window.text_widget(0,0,width=400,textcenter=True,just_bottomcenter=True,pady=-10,font=20)
                    \t -window.text_widget(0,0,width=400,opt.textcenter(),opt.justbottomcenter(),opt.pady(-10),opt.font(20))    \t --> Same as previous example.
        """
        return CTextWidget(_pybox.WindowTextWidget(self.__id,int(x),int(y),text,width,height,*args,**kwargs))

    def text_widget_l(self, at = (0,0),text : str = None,size : list = (0,0) , *args, **kwargs ) -> CTextWidget :
        """
        Create a text widget in the window at (at), where at is a tuple, list or array.   See: text_widget() to create a text widget using separate (x,y) values.

        Parameters:

        - text          \t -- [optional] Sets the text of the widget.  This can be set later with textwidget.Write()
                        \t - When text is entered, the text widget is created to the width of the text.  Use the width() parameter to set a width or pad
                        \t - the text with spaces to reserve width.
        - width         \t - [optional] Sets the width of the text widget in pixels.  The default is 200 pixels.
        - height        \t - [optional] Sets the height of the text widget in pixels.  The default is the height of the current font or specified font (when opt.font() is used)

        Keywords and Pybox options can be included.  Some various options are as follows:

        - TextColor         \t - Sets the text color of the widget (default is current window text color).  Same as opt.fgcolor()
        - bgColor           \t - Sets the background color of the widget.  The default blends with the window
        - Font              \t - Sets the font of the text in the text widget
        - CenterX,CenterY   \t - Centers the text widget in the window horizontally or vertically, respectively.
        - TextCenter        \t - Centers the text inside of the widget (which can be longer than the text itself).
                                \t - Use TextCenterX() and CenterX() together to make sure text is centered in the window. This is only needed if the Width of the
                                \t - Text Widget and the text have been specificed separately.

        - JustBottomCenter, JustBottomLeft, JustBottomRight, JustTopCenter, JustTopLeft, JustTopRight
        - PadX,PadY         \t - Use thse with the above positioning to move the widget left,right,up, down from automatic placement.
                            \t - For example, using JustBottomCenter() with PadY(-10) will move the text widget away from the bottom,

        Examples:   \t -window.text_widget_l((10,10),"This is a text Widget",font=(20))
                    \t -window.text_widget_l((0,50),"This is a text widget",centerx=true) \t - Centers Text Widget horizontally
                    \t -window.text_widget_l(my_location,width=400,textcenter=True,just_bottomcenter=True,pady=-10,font=20)
                    \t -window.text_widget_l((0,0),width=400,opt.textcenter(),opt.justbottomcenter(),opt.pady(-10),opt.font(20))    \t --> Same as previous example.
        """
        return CTextWidget(_pybox.WindowTextWidget(self.__id,at[0],at[1],text,size[0],size[1],*args,**kwargs))

    def new_inputbox(self,x : int, y : int,width : int = 200, height : int = 0, text : str = None,*args,**kwargs) -> InputBox :
        """
        Creates a new Input Box (also known as an "Edit Box") where you can enter text data as simple as a few characters are entire paragraphs. 

        The Input box is placed in the window at the (x,y) position.  See: new_inputbox_l() to use a tuple/list for the window position.

        Optional Parameters:

        - width         \t -Sets the width of the input box in pixels.  The default is 250 pixels.
        - height        \t -Sets the height of the input box in pixels.  The default is set to the default Font for 1 line of text. 
        - text          \t -This sets the starting text for the input box.  Otheriwse the input box is left blank at first. 

        Keywords and Pybox options can be included.  Some various options are as follows:

        - font          \t -Sets the font for the input box.  The default is the current font of the window
        - numbersonly   \t -Causes the input box to only accept numbers. 
        - readonly      \t -Sets the input box as read only so it can be used as a way to place a large amount of text that can be copied.
        - textcolor     \t -Sets the color of the text in the input box
        - bgcolor       \t -Sets the background color of the text in the input box
        - label         \t -Sets a label to the right of the input box
                        \t -LabelRight, LabelLeft, LabelBottom, and LabelTop can be used to set the location of the label.
        - label_color    \t -Sets the color of the label (i.e. opt.label_color("Red"))
        - multiline     \t -Sets the input box as a multi-line input box.  This allows more than one line to be entered.
                        \t -A button or some method to end input must be used unless "WantReturn" is specified
        - wantreturn    \t -For multi-line boxes, this sends a "return pressed" message when the return key is pressed.
        - password      \t -Causes the input box to display '*' for all text.
        - noborder      \t -Causes the input box to not use a border so it will blend into the window more seamlessly.
        - thickborder,Recessed      \t -These are two different border styles that can be used.
        - vscroll, hscroll          \t -Adds a vertical scrollbar (useful for multi-line boxes) and horizontal scroll bar, respectively
        - wincolors     \t -Sets the background input box color and text color to the current window color instead of the default white-and-black colors. 

        Examples:   \t -window.new_inputbox(40,50)             \t -- create input box at location 40,50
                    \t -window.new_inputbox(40,50,height=500)  \t -- create an input box of height 500 pixels
                    \t -Window.new_inputbox(40,50,opt.font(20),opt.label("Enter Data"))
                    \t -Window.new_inputbox(40,50,text="This is the default text")
        """
        return InputBox(_pybox.WindowNewInputBox(self.__id,int(x),int(y),int(width),int(height),text,*args,**kwargs))

    def new_inputbox_l(self,at,width : int = 200, height : int = 0, text : str = None,*args,**kwargs) -> InputBox :
        """
        Creates a new Input Box (also known as an "Edit Box") where you can enter text data as simple as a few characters are entire paragraphs. 

        The Input box is placed in the window at the (at) position, which can be a list, tuple or array.  See: new_inputbox() to use a individual (x,y) values.

        Optional Parameters:

        - width         \t -Sets the width of the input box in pixels.  The default is 250 pixels.
        - height        \t -Sets the height of the input box in pixels.  The default is set to the default Font for 1 line of text. 
        - text          \t -This sets the starting text for the input box.  Otheriwse the input box is left blank at first. 

        Keywords and Pybox options can be included.  Some various options are as follows:

        - font          \t -Sets the font for the input box.  The default is the current font of the window
        - numbersonly   \t -Causes the input box to only accept numbers. 
        - readonly      \t -Sets the input box as read only so it can be used as a way to place a large amount of text that can be copied.
        - textcolor     \t -Sets the color of the text in the input box
        - bgcolor       \t -Sets the background color of the text in the input box
        - label         \t -Sets a label to the right of the input box
                        \t -LabelRight, LabelLeft, LabelBottom, and LabelTop can be used to set the location of the label.
        - label_color    \t -Sets the color of the label (i.e. opt.label_color("Red"))
        - multiline     \t -Sets the input box as a multi-line input box.  This allows more than one line to be entered.
                        \t -A button or some method to end input must be used unless "WantReturn" is specified
        - wantreturn    \t -For multi-line boxes, this sends a "return pressed" message when the return key is pressed.
        - password      \t -Causes the input box to display '*' for all text.
        - noborder      \t -Causes the input box to not use a border so it will blend into the window more seamlessly.
        - thickborder,Recessed      \t -These are two different border styles that can be used.
        - vscroll, hscroll          \t -Adds a vertical scrollbar (useful for multi-line boxes) and horizontal scroll bar, respectively
        - wincolors     \t -Sets the background input box color and text color to the current window color instead of the default white-and-black colors. 

        Examples:   \t -window.new_inputbox_l(40,50)             \t -- create input box at location 40,50
                    \t -window.new_inputbox_l(40,50,height=500)  \t -- create an input box of height 500 pixels
                    \t -Window.new_inputbox_l(40,50,opt.font(20),opt.label("Enter Data"))
                    \t -Window.new_inputbox_l(40,50,text="This is the default text")
        """
        return InputBox(_pybox.WindowNewInputBox(self.__id,int(at[0]),int(at[1]),int(width),int(height),text,*args,**kwargs))

    def write(self,outstring : str = "", *args,**kwargs) -> bool :
        """
        Write Text out to the window. 

        The write() function will write text to the window and can be used with many options.

        A basic example is: window.write("Hello World"), window.write("Hello World"), as well as window.write(f"My Variable is: {MyVariable") 

        Keywords and Pybox options can be included.  Some various options are as follows:

        - font                          \t -Set the font to be used for the text
        - center_x, center_x, center_xy    \t -Center the text in various ways (i.e. CenterX centers in the X-axis, etc.)
        - textcolor                     \t -Set the text color for the text.
        - bgcolor                       \t -Set the background color for the text
        - at                            \t -Set the position in the window of the text, i.e. Write("Hello World",opt.at(x,y))

        Controls can be embedded in the text line to change colors and font sizes:

        For example:    \t -window.write("This {r}word{} is in the color red").
                        \t -Note the {} to close.  With Python formatted strings, an extra "{}" is needed, such as f"MyValue {{r}}{myvalue}{{}} is in red". 

        More than one control can be used such as: write("This is in {r}Red{} and this is in {b}Blue". 
        You do not need the closing {} if it is as the end of the line.

        - {<color>}     \t -Where the color is a defined color such as {red} (or {r}), {blue}, {skyblue}, etc.   You can use abbreviations for most primary colors, such as
                            \t - {y} = {yellow}, etc.
        - {font size}   \t -i.e. "This is in the normal font, and {30}this is in a 30-point font"
        - {font name}   \t -i.e. "This is in the normal font, and {Courier New,20}This is in a 20-point Courier New font"
        - {bitmap}      \t -This is TBD in a coming version, and will accept bitmap names to print in the output window.
       
        Examples:   \t -MyWindow.write("Hello World",opt.font(40),opt.center_xy())     \t -- Writes a big "Hello World" in the center of the screen
                    \t -MyWindow.write("Hello World",opt.fgcolor("red")               \t -- Writes "Hello World" in red
                    \t -MyWindow.write("{r}Hello World")                              \t - - Also writes "Hello World" in red
                    \t -MyWindow.write("Hello World",opt.font(50))                    \t - - Writes "Hello World" in a 50-point font size.
        """
        return _pybox.WindowWrite(self.__id,outstring,*args,**kwargs)

    def writeln(self,outstring : str = "", *args, **kwargs) -> bool :
        "Same as the write() function, but adds a newline after the Write().  See Write() for more information"
        return _pybox.WindowWriteln(self.__id,outstring,*args,**kwargs)

    def write_xy(self,x,y,text,*args ,**kwargs) -> bool :
        """
        Same as write() but puts the text at the (x,y) position given. 
        See write_xy_l() to use list, tuple, or array for (x,y) instead of independent values.

        See write() for more information
        """
        return _pybox.WindowWriteXY(self.__id,int(x),int(y),text,*args,**kwargs)

    def write_xy_l(self,at,text,*args,**kwargs) -> bool :
        """
        Same as write() but puts the text at the (x,y) position given. 
        See write_xy() to use independent values for (x,y) instead of list, tuple, or array.

        See write() for more information
        """
        return _pybox.WindowWriteXY(self.__id,int(at[0]),int([1]),text,*args,**kwargs)

    def set_font(self,font,*args) -> bool :
        """
        Sets the current font of the window.  The font may be a simple number, a font name and size, or a created font using CreateFont()

        Examples:  
            \t -MyWindow.set_font(40)                      \t -- Sets font size 40 of the default font (Arial)
            \t -MyWindow.set_font("Times New Roman")      \t -- Sets "Times New Roman" as the font
            \t -MyWindow.set_font("italic")               \t -- Sets an italic version of the current font
            \t -MyWindow.set_font("bold")                 \t -- Sets a bold version of the current font
            \t -MyWindow.set_font("Verdana,italic,30")     \t -- Sets a Veriana, italic, 30-point font
            \t -MyWindow.set_font("MyFont")                \t -- Sets a previously created font named "MyFont"

        """
        return _pybox.WindowSetFont(self.__id,opt.font(font),*args)
    def get_window_size(self,bFrameSize : bool = False) -> list :
        """
        Returns the canvas size of the window (i.e. the interior size of the window) as an array (width,height)

        Note: size() and get_window_size() are the same function

        Use get_window_size(True) to return the size of the window including the frame.

        The size is returned as a list.

        Example:

        \t -size = MyWindow.get_window_size()
        \t -
        \t -width = size[0]
        \t -height = size[1]

        Example:

        center = MyWindow.get_window_size()/2
        """
 #       return numpy.array(_pybox.WindowGetWindowSize(self.__id,bFrameSize))
        return _pybox.WindowGetWindowSize(self.__id,bFrameSize)
        
    def get_window_center(self,bFrameSize : bool = False) -> list :
        """
        Returns center coordinates of the Window's client (visible) area. 
        """
        return _pybox.WindowGetWindowCenter(self.__id,bFrameSize)

    def size(self,bFrameSize : bool = False) -> numpy.array :
        """
        Returns the canvas size of the window (i.e. the interior size of the window) as an array (width,height)

        Note: size() and get_window_size() are the same function

        Use size(True) to return the size of the window including the frame.

        The size is returned as a list.

        Example:

        \t -size = MyWindow.size()
        \t -
        \t -width = size[0]
        \t -height = size[1]

        Example:

        center = MyWindow.size()/2
        """
 #       return numpy.array(_pybox.WindowGetWindowSize(self.__id,bFrameSize))
        return _pybox.WindowGetWindowSize(self.__id,bFrameSize)


    def get_window_width(self,frameSize : bool = False) -> int :
        """
        Returns the width of the window. Note: get_window_width() and width() are the same function

        By default, the interior width of the window is returned. 

        Parameters:

        - frameSize     \t -- When 'True', the width of the window including the frame is returned.  Otherwise only the interior width is returned.

        Example:

        WinWidth = Win.get_window_width()        \t - - Return Window interior width.
        WinWidth = Win.get_window_width(True)     \t - - Return Window frame width

        """
        return _pybox.WindowGetWindowWidth(self.__id,frameSize)

    def width(self,frameSize : bool = False) -> int :
        """
        Returns the width of the window. Note: get_window_width() and width() are the same function

        By default, the interior width of the window is returned. 

        Parameters:

        - frameSize     \t -- When 'True', the width of the window including the frame is returned.  Otherwise only the interior width is returned.

        Example:

        WinWidth = Win.width()        \t - - Return Window interior width.
        WinWidth = Win.width(True)     \t - - Return Window frame width

        """
        return _pybox.WindowGetWindowWidth(self.__id,frameSize)

    def get_window_height(self,frameSize : bool = False) -> int :
        """
        Returns the height of the window. Note: height() and get_window_height() are the same function

        By default, the interior height of the window is returned. 

        Parameters:

        - frameSize     \t -- When 'True', the height of the window including the frame is returned.  Otherwise only the interior height is returned.

        Example:

        WinWidth = Win.get_window_height()        \t - - Return Window interior height.
        WinWidth = Win.get_window_height(True)     \t - - Return Window frame height

        """
        return _pybox.WindowGetWindowHeight(self.__id,frameSize)

    def height(self,frameSize : bool = False) -> int :
        """
        Returns the height of the window. Note: height() and get_window_height() are the same function

        By default, the interior height of the window is returned. 

        Parameters:

        - frameSize     \t -- When 'True', the height of the window including the frame is returned.  Otherwise only the interior height is returned.

        Example:

        WinWidth = Win.height()        \t - - Return Window interior height.
        WinWidth = Win.height(True)     \t - - Return Window frame height

        """
        return _pybox.WindowGetWindowHeight(self.__id,frameSize)    

    def set_window_size(self,width : int, height : int,bInnerSize : bool = True) -> bool :
        "Sets the width and height of the window.  See set_window_size_l() to use a list, tuple, or array instead of (width,height)"
        return _pybox.WindowSetWindowSize(self.__id,int(width),int(height),bInnerSize)

    def set_window_size_l(self,size : list,bInnerSize : bool = True) -> bool :
        "Sets the width and height of the window with the incoming list, array, or tuple, i.e. (Width,Height).  See set_window_size() to use individual width, height parameters."
        return _pybox.WindowSetWindowSize(self.__id,int(size[0]),int(size[1]),bInnerSize)

    def get_event(self) -> bool :
        """
        GetEvent waits for an event to occur in your main body of code. 

        - Events are any events such as a mouse move, click, keyboard press, etc. 
        - Events are also caused by any control change such as moving a slider, pressing a button, or pressing return in an input box. 
        - Events can also be a window closing, a window moving or changing size -- basically anything happening in the system sends a message

        Until an event occurs, the program is sleeping and not using any CPU time.  Pybox wakes up the program when an event happens. 

        In the event loop, you can check for events.  

        get_event() returns true until all main windows are closed. 

        Example:

                my_button = pybox.dev_button("Press Me")
                my_slider = pybox.def_slider()

                while pybox.get_event() :
                    if my_button.pressed() : print("My Button was Pressed")
                    if my_slider.moved()   : print("Range Slider is now at position",my_slider.get_pos())


        In this example, the program sleeps until an event occurs, and then the program checks to see if an event occured with a button or a slider movement. 

        Events are typically one-time:  They report "True" on the first call, and then fals afterwards until another event of the same type happens. 
        
        You can also use a callback to retrieve events.  Though this is not recommended or useful for most programs, it can be useful for some specific purposes.
        See set_event_callback() for more information.
        """
        return _pybox.GetEvent()           # probably deprecated -> _pybox.WindowGetEvent(self.__id) 

    def display_bitmap(self,x : int, y : int,bitmap,size=None,*args,**kwargs) :
        """
        Displays a bitmap on the screen at the (x,y) position given.  See display_bitmap_l() to use a list, array, or tuple for the (x,y) location

        Optional Parameters

        - size      - Sets the size of the bitmap -- the default is the same size as the bitmap. 
                    \t -note: leaving one value at 0 will cause the bitmap to be scaled proportionally.

                       For example, "window.display_bitmap(MyBitmap,Size=(500,0))" will cause the bitmap to be displayed at a width of 500 pixels 
                       and height to be proportional to the width and display correctly.
        - Reversed  \t - This will cause the bitmap to be displayed upside-down, since bitmaps can vary.  Also use display_bitmap_r() to display the bitmaps upside-down

        About Bitmaps: 
        
        Bitmaps can be a Pybox CBitmap-type bitmap or an unsigned char numpy array in the form [height][width][3] (i.e. compatible with SciPy, etc.), 
        where the [3] is Blue, Red, Green unsigned character values.
        """
        return _pybox.WindowDisplayBitmap(self.__id,bitmap,opt.at(x,y),opt.size(size),*args,**kwargs)

    def display_bitmap_l(self,at : list,bitmap,size=None,*args,**kwargs) :
        """
        Displays a bitmap on the screen at the (x,y) position given. See display_bitmap() to use a (x,y) as independent values.

        Optional Keywords and Parameters

        - size      - Sets the size of the bitmap -- the default is the same size as the bitmap. 
                    \t -note: leaving one value at 0 will cause the bitmap to be scaled proportionally.

                     for Example, "window.display_bitmap_l(MyBitmap,Size=(500,0))" will cause the bitmap to be displayed at a width of 500 pixels 
                     and height to be proportional to the width and display correctly.

        - Reversed   - This will cause the bitmap to be displayed upside-down, since bitmaps can vary.  Also use display_bitmap_r_l() to display the bitmaps upside-down

        About Bitmaps: 
        
        Bitmaps can be a Pybox CBitmap-type bitmap or an unsigned char numpy array in the form [height][width][3] (i.e. compatible with SciPy, etc.), 
        where the [3] is Blue, Red, Green unsigned character values.
        """
        return _pybox.WindowDisplayBitmap(self.__id,bitmap,opt.at(int(at[0]),int(at[1])),opt.size(size),*args,**kwargs)

    def display_bitmap_r(self,x : int, y : int, bitmap, size=None,*args,**kwargs) :
        """
        Displays a bitmap upside-down on the screen at the (x,y) position given. See display_bitmap_r_l() to use a list, array, or tuple for the (x,y) location

        For a bitmap that is not displayed upside-down, see display_bitmap()

        Optional Keywords and Parameters

        - size      - Sets the size of the bitmap -- the default is the same size as the bitmap. 
                    \t -note: leaving one value at 0 will cause the bitmap to be scaled proportionally.

                       For example, "window.display_bitmap_r(MyBitmap,Size=(500,0))" will cause the bitmap to be displayed at a width of 500 pixels and 
                       height to be proportional to the width and display correctly.

        About Bitmaps: 
        
        Bitmaps can be a Pybox CBitmap-type bitmap or an unsigned char numpy array in the form [height][width][3] (i.e. compatible with SciPy, etc.), 
        where the [3] is Blue, Red, Green unsigned character values.
        """        
        return _pybox.WindowDisplayBitmapR(self.__id,bitmap,opt.at(int(x),int(y)),opt.size(size),*args,**kwargs)

    def display_bitmap_r_l(self,at : list, bitmap,size=None,*args,**kwargs) :
        """
        Displays a bitmap upside-down on the screen at the (x,y) position given. See display_bitmap_r() to use independent x,y values.

        For a bitmap that is not displayed upside-down, see display_bitmap()

        Optional Parameters

        - size      - Sets the size of the bitmap -- the default is the same size as the bitmap. 
                    \t -note: leaving one value at 0 will cause the bitmap to be scaled proportionally.

                       For Example, "window.DisplayBitmapR(MyBitmap,size=(500,0))" will cause the bitmap to be displayed at a width of 500 pixels and 
                       height to be proportional to the width and display correctly.

        About Bitmaps: 
        
        Bitmaps can be a Pybox CBitmap-type bitmap or an unsigned char numpy array in the form [height][width][3] (i.e. compatible with SciPy, etc.), 
        where the [3] is Blue, Red, Green unsigned character values.
        """        
        return _pybox.WindowDisplayBitmapR(self.__id,bitmap,opt.at(int(at[0]),int(at[1])),opt.size(size),*args,**kwargs)

    def transform_bitmap(self,x : int, y : int,bitmap,angle : float = 0,zoom : float = 1.0) :
        """
        Transform Bitmap will display a bitmap at the (x,y) positon in the window rotated at a specified angle and with a specified zoom. 

        See transform_bitmap_l() to use a list,tuple, or array to specify the location.

        Options:

        - x,y       \t -- Location of the bitmap in the window
        - bitmap    \t -- The bitmap.  The bitmap may be a pybox bitmap (CBitmap) or an RGB array bitmap (i.e. SciPy -- See DisplayBitmap() for more details.
        - angle     \t -- The angle in radians to display the bitmap.  The default is 0 (no rotation).  
        - Zoom      \t -- The zoom factor to display the bitmap.  The default is 1.0 -- for example, 2.0 is 2x the size, etc.

        note: If the bitmap is displayed upside down, add 3.14159 to the angle (i.e. 180 degrees)

        Masks

        If the bitmap has a mask associated with it (i.e. it is a PNG or 32-bit BMP) the mask will be used to create the transparency mask and blend with the window background.

        Example: window.transform_bitmap(50,50,MyBitmap,30*3.14159/180,.5)  - Display a bitmap at 50,50 rotated at 30 degrees at half its size (.5x)
        """
        return _pybox.WindowTransformBitmap(self.__id,int(x),int(y),bitmap,float(angle),float(zoom),False)

    def transform_bitmap_l(self,at : list,bitmap,angle : float = 0,zoom : float = 1.0) :
        """
        Transform Bitmap will display a bitmap at the (x,y) positon in the window rotated at a specified angle and with a specified zoom. 

        See transform_bitmap() to use a independent x,y values for the location of the bitmap.

        note: If the bitmap is displayed upside down, add 3.14159 to the angle (i.e. 180 degrees)

        Options:

        - x,y       \t -- Location of the bitmap in the window
        - bitmap    \t -- The bitmap.  The bitmap may be a pybox bitmap (CBitmap) or an RGB array bitmap (i.e. SciPy -- See DisplayBitmap() for more details.
        - angle     \t -- The angle in radians to display the bitmap.  The default is 0 (no rotation).  
        - Zoom      \t -- The zoom factor to display the bitmap.  The default is 1.0 -- for example, 2.0 is 2x the size, etc.

        Masks

        If the bitmap has a mask associated with it (i.e. it is a PNG or 32-bit BMP) the mask will be used to create the transparency mask and blend with the window background.

        Example: window.transform_bitmap_l((50,50),MyBitmap,30*3.14159/180,.5)  - Display a bitmap at 50,50 rotated at 30 degrees at half its size (.5x)
        """
        return _pybox.WindowTransformBitmap(self.__id,int(at[0]),int(at[1]),bitmap,float(angle),float(zoom),False)

    def get_integer(self,text=None,*args, **kwargs)   -> int :
        """
        Gets an integer value from a window that pops up with an input box.  The return value is the integer entered or default value.
        Call pybox.was_canceled() to determine if the user canceled the input box (opt.nocancel() will disallow the ability to cancel)

        Options:

        text        \t - [optional] The text to put as a header in the box.  You can use multiple lines.
                    \t - if the first line starts with '+' that line becomes the title in the title bar and subsquent lines are printed in the description.

        Keywords and Pybox options can be included.  Some various options are as follows:

        - Range         \t -Set a range for the input.  This will not allow an input outside of the range, but can allow the user to press return
        - Default       \t -Sets the default value.  This is placed in the input box when the box first comes up.  If the user presses return on a blank line, the default is returned.
        - NoCancel      \t -By defaut, there is a cancel button to allow the user to cancel.  You can call pybox.was_canceled() which returns True if the last input box was canceled.
                        \t -When NoCancel is specified, the user cannot cancel or press return on an empty line and must enter a value (a control-C may be pressed to stop the program.

        Examples:       \t -My Value = window.get_integer("Enter a number")
                        \t -My Value = window.get_integer("+This is the title bar title\\nEnter a number",range=(1,100),nocancel=True)
                        \t -My Value = window.get_integer("Enter a number\nNumber should be between 1 and 100,opt.range(1,100),opt.default(10))
        """
        return _pybox.WindowGetInteger(self.__id,text,*args, **kwargs)

    def get_float(self,text=None,*args,**kwargs)   -> float :
        """
        Gets an floating-point value from a window that pops up with an input box.  The return value is the integer entered or default value.
        Call pybox.was_canceled() to determine if the user canceled the input box (opt.nocancel() will disallow the ability to cancel)

        Options:

        text        \t - [optional] The text to put as a header in the box.  You can use multiple lines.
                    \t - if the first line starts with '+' that line becomes the title in the title bar and subsquent lines are printed in the description.

        Keywords and Pybox options can be included.  Some various options are as follows:

        - range         \t -Set a range for the input.  This will not allow an input outside of the range, but can allow the user to press return
        - default       \t -Sets the default value.  This is placed in the input box when the box first comes up.  If the user presses return on a blank line, the default is returned.
        - noCancel     \t -By defaut, there is a cancel button to allow the user to cancel.  You can call pybox.was_canceled() which returns True if the last input box was canceled.
                        \t -When NoCancel is specified, the user cannot cancel or press return on an empty line and must enter a value (a control-C may be pressed to stop the program.

        Examples:       \t -My Value = window.get_float("Enter a number")
                        \t -My Value = window.get_float("+This is the title bar title\\nEnter a number",range=(1,100),nocancel)
                        \t -My Value = window.get_float("Enter a number\nNumber should be between 1 and 100,opt.range(1,100),opt.default(10))
        """
        return _pybox.WindowGetFloat(self.__id,text,*args,**kwargs)

    def set_cls_bitmap(self,bitmap,cls_now : bool = False) -> bool : 
        """
        Sets the bitmap to use as the background bitmap when cls() clears the window. 
        The Bitmap is placed at (0,0) -- options will be added in a future release to center and size the image 

        A bitmap can be a Pybox/Sagebox bitmap or an array-based bitmap compatible with packages such as SciPy, etc. 

        About Bitmaps: Bitmaps can be a pybox bitmap or a general RGB array bitmap (i.e. numpy array) in the form [height][width][3], where the [3] is Blue, Green, and Red,
        or an RGB32 bitmap array of [height][width][4] where the 4 values are Red, Green, Blue, and Mask, in that order.
    
        The bitmap format can be unsigned char, float, double, mono, mono float, and half-float. 

        Note: The bitmap is copied and stored privately.  The bitmap given to the SetClsBitmap() function does not need to be saved or maintained.
        """
        return _pybox.WindowSetClsBitmap(self.__id,bitmap,cls_now)

    def set_realtime(self) :
        """
        Sets RealTime status for Window.
        
        This sets the status of the Window for real-time drawing, includes setting the high-resolution timer and turning off Auto Updates to the Window.
        
        This can be used when drawing real-time graphics to a window for smoother graphics using the vertical resync. 
        
        Also See: vsync_wait()
        """
        return _pybox.WindowSetBool(self.__id,0,True)
      
    def cls(self,color1 = None,color2 = None) :
        """
        Clears the window to a blank canvas.

        Example: window.Cls()       \t -- this clears the window to the current color(s) or bitmap set for Cls()

        Also see: ClsHold() to clear the window but also stop the window from updating until Update is called (or ClsHold() is called again)

        Parameters

            color1      \t -- [optional] This is the color to clear the screen
            color2      \t -- [optional] When two colors are used, the window is cleared with a gradient of the two colors

        About Colors

        Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
        Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

        Examples:

        cls()                           \t -- Clear the window with the current background color of the window
        cls("red")                      \t -- Clear the window with the color red
        cls(SageColor.Red())            \t -- Clears the color with red, also
        cls(PanColor.ForestGreen())     \t -- Clears the window with PanColor.ForestGreen
        cls(MyColor)                    \t -- Clears the window with a defined "MyColor", such as MyColor = pybox.RgbColor(0,255,0)
        cls("black,blue")             \t -- Clears the window with a gradient from black to blue
        """
        return _pybox.WindowCls(self.__id,color1,color2,False)
    
    def cls_radial(self,color1 = None,color2 = None) :
        return _pybox.WindowCls(self.__id,color1,color2,True)

    def draw_grid(self,spacing : int = 25,**kwargs) -> bool :
        """
        Draws a grid of lines in the X and Y axis to create a graph on the screen.

        The "spacing" parameter controls how many pixels are between each set of lines.
        
        Keywords and Pybox options can be included.  Some various options are as follows:

        - color                       \t -Sets the color of the grid, i.e. "white","red","45,67,123", etc. Default color is RGB(42,42,42) (i.e. dark gray)

        The default for the "spacing" parameter is 25 pixels.

        Examples:
     
        \t -MyWindow.draw_grid()                \t -- Draws default grid
        \t -MyWindow.write(50)                  \t -- Draws a grid with spacing of 50 pixels 
        \t -MyWindow.write("green")             \t -- Draws a grid with the color green
        \t -MyWindow.write(50,"0,255,255")      \t -- Draws a grid with spacing of 50 and an RGB color of (0,255,255) or "cyan"
        """
        return _pybox.WindowDrawGrid(self.__id,spacing,**kwargs)
    
    def draw_vector(self,p1 : list, p2 : list,line_size,color,**kwargs) : 
        """
        Draws a vector from point p1 to p2.  A vector is the same thing as a line, but with some differences and a number of controls that 
        can be used to modify its behavior and appearance.
        
        The vector also has beginning and end 'caps'.  The default is for the beginning of the line to have a round shape (e.g. round cap), and
        the end of the line to have a larger arrow shape (known as an 'arrow' cap, but because it's larger it's known as an 'arrow anchor')
        
        The default behavior for draw_vector is to draw the vector in a white color, with a round beginning cap and an 'arrow anchor' ending cap.
        
        Input
        
        - p1,p2             - Beginning and End Points of the line, such as (100,400),(600,700) or (x1,y1),(x2,y2), etc.
        - line_size         -size of the line in pixels.
        - color             - color of vector line.
        
        Example of simple usage: window.draw_vector(p1,p2,10) or draw_vector((x1,y1),(x2,y2),10)
        
        Text, colors, and many others may be assign through the following keywords

        - title         - Sets the title to display on the vector line, e.g. title="This is a vector.  Default behavior is no title.
        - opacity       - Sets the opacity to draw the line.  Range is 0-255, with 0 transparent and 255 fully opaque. Default is 255 (fully opaque).
        - angle         - Rotates the vector at its center by the angle specified.  "angle" is in degrees.  "AngleDeg" may also be used to specify degrees
        - angle_rad     - Same as "angle", but uses radians instead of degrees, e.g. angle_rad = 1.57 (for 90 degrees)
        - text_size     - Sets the relative font size of the label.  The default font varies in size based on line thickness. 
                          text_size values can me "xxsmall","xsmall","small","medium","large,"xlarge", "xxlarge".  Default is "small".  "default" may also be used as an option.
        
        - label_font (or "font")    - Sets a specific font size or type for the vector line.  The font will not change based on line thickness when set in this manner.
                                      Fonts may be set with just a size, such as a number, e.g. font=25 (for default font Arial at 25 points), or a full font name, e.g. font="time new roman,25"
        
        - label_just (or "just")    - Sets the justification of the vector label text.  Default is "top-left".  
                                      Options are: "top-left","top-left-center","top-center","top-right-center","top-right".  "bottom" and "middle" may be used instead of top to specify the 
                                      bottom of the vector line or middle of the line (vertically), respectively.  Example: just="bottom-right"

        - capsize       - Sets the beginning and end cap of the vector to a multiple of the capsize specified.  This is useful only for 'anchor' cap types
                          such as 'round achor', 'arrow anchor',etc.  The anchor types grow and shrink based on line thickness.
                          using "capsize" can make the beginning and end caps smaller or larger.
                          example capize=2 makes any anchor cap 2x larger.  see "begcapsize" and "endcapsize" to control cap sizes individually.

        - begcap_size (or "begcap")   - Sets the begininng cap size if the begnining cap is an 'anchor' cap type.  See documentation on 'capsize', which will set both
                                        beginning and end cap together.
                          
        - endcap_size (or "endcap")  - Sets the end cap size if the end cap is an 'anchor' cap type.  See documentation on 'capsize', which will set both
                                       beginning and end cap together.
 
        - begcap_type       - Sets the beginning cap type.  by default, the cap type for the begining of the vector is "round"
                              possible types are "round","diamond","arrow","square","flat","round anchor","diamond anchor","arrow anchor","diamond anchor"
                              "anchor" types are larger and can be made smaller or larger with "capsize" or "begcap_size"
                                       
        - endcap_type       - Sets the ending cap type.  by default, the cap type for the enf of the vector is "arrow anchor"
                              possible types are "round","diamond","arrow","square","flat","round anchor","diamond anchor","arrow anchor","diamond anchor"
                              "anchor" types are larger and can be made smaller or larger with "capsize" or "begcap_size"
        - begcap_color      - Sets the color of the beginning cap of the vector.  This is useful for "anchor" cap types which are larger.  
                              Example: begcap_color="yellow"                             
        - endcap_color      - Sets the color of the ending cap of the vector.  This is useful for "anchor" cap types which are larger.  
                              By default, the begining and end caps are the same color as the vector line itself.  Example: endcap_color="red"  
        - label_pad_x (or "pad_x")  - Sets extra spacing on the left or right of the label on the vector.  Positive values move the title to the right
                                      (as formed by p1-p2), with negative values moving the title to the left.
        - label_pad_y (or "pad_y")  - Sets extra spacing on the top or bottom of the label on the vector.  Positive values move the title upwards
                                      (as formed by p1-p2), with negative values moving the title downward.
        - label_opacity     - Sets the opacity of the vector's label.  By default, the opacity of the vector label is the same as the line, either by default or
                              when the line opacity is specifically specified.  Using label_opacity will cause the label's opacity to use this value.
        - label_color   - Sets the color of the vector label, e.g. label_color="red".  By default, the label's color is white, regardless of the line color.
        - label_angle   - Sets the label of the angle with 3 options: "horizontal" (default), "vertical", or "vertical 180".  "vertical" and vertical 180" make the label
                          appear sideways on the line, with "vertial 180" reversing it's direction, with the start of the text appearing away from the line.
                          Add the term "static" to keep the label the exact orientation regardless of line angle, e.g. 'label_angle="horizontal,static"' will cause
                          the text to display at 0 degrees relative to the screen rather than the line itself.
                          
        - label_up      - Keeps the vector's label right-side up. As the vector rotates and the label's orientation, using "label_up=True" will keep the label
                          right-side up when the label's angle is such that the label would otherwise appear upside-down.
        - set_center    - Sets the center of the vector, regardless of p1 and p2.  This calculates the relative center of the vector (i.e. (p1+p2)/2-p1), and
                          places the center of the vector at the new (x,y) coordinates.  Example set_center=(500,200) or set_center=(x,y)
                          This is useful in simply specifying a length in the draw_vector call as p1 and p2, such as draw_vector((0,0),(0,x),...) then
                          setting the center and angle of the vector with "set_canter" and "angle" keywords, respectively/
        - show_center   - puts a circle in the center of the vector.  This is for purely diagnostic purposes, showing the center is where it should be based on 
                          the calling's functions calculation.  Use "show_center=True" to show the circle in cyan.  
                          Use "show_center=<color>" to set the color, e.g. 'show_center="black"'
        """
        return _pybox.WindowDrawVector(self.__id,p1[0],p1[1],p2[0],p2[1],line_size,color,**kwargs)
    
    def new_turtle_graphics(self,**kwargs) :
        """
        Gets a new TurtleShell object for Turtle Graphics-type drawing.
        
        - Returns a TurtleShell object for drawing to the window in turtle-graphics style.
        - This incldes real-time Turtle Graphics.
        
        TurtleShell is still in development. 
        
        This section will be filled out more in future releases.
        
        See various TurtleShell examples and function descriptions in the returned TurtleShell object
        
        Some Notes:
        -----------
        
        TurtleShell operates the same as Turtle Graphics in most ways.  The functions are the same, with some additions for opacities and gradients, as well as other functions.
    
        - TurtleShell does not display each segment drawing, showing each segment after it is drawn.  
        - As with Turtle Graphics, the speed can be set to show each element drawing.
        
        - Setting a speed to zero will allow for real-time graphics. 
        - TurtleShell is meant to be a Turtle Graphics environmemt with some additions to allow more functionality than original turtle graphics.
        - TurtleShell is a prototype at the moment, and the idea is to bring more functions into it, including GPU-based and 3-D Turtle Graphics.
    
        See various examples and documentation on TurtleShell functions for more information.
        """
        return TurtleShell(_pybox.WindowNewTurtleShell(self.__id,**kwargs))
    
    def get_mouse_region(self,**kwargs) -> MouseRegion :
        """
        Returns a reference to the Window's Mouse Region object.  Each window has one Mouse Region object that it maintains.        <para></para>
        
        Mouse Regions can be used to easily highlight, select, and move various 'mouse region' areas, allowing the window to maintain
        a number of selectable objects for the main program.
        
        For example, if you have a curve with a number of selectable points, the Mouse Region object can maintain (and display) these points so the
        main program does not have to get the mouse input and determine which area is being highlighted, selected, moved, etc.
        
        - Keywords can be added for control of the mouse region, notably kw::AutoDraw() to set any drawing characteristics when MouseRegion::AutoDraw() is called.
        - ** Important Note **. Don't call MouseRegion::UpdatePoints() with the Mouse Region obtained through this function.  UpdatePoints() is automatically called.
        
        Keywords usable with mouse_region:
        
        - auto_draw           \t - Set auto_draw characteristics for all new regions/points added. See auto_draw() function in returns MouseRegion object.
        - bound_box()          \t - Sets a bounding region for all new regions/points added.      
         """ 
        return MouseRegion(_pybox.WindowGetMouseRegion(self.__id,**kwargs))

    def use_win_as_cls(self,use_bitmap : bool = True) :
        """
        Sets the current display in the window as the bitmap to display when the Cls() function is used.
        
        - Use cls() with any color or bitmap to clear the bitmap usage.
        - This function may also be called to remove the bitmap as the Cls Bitmap by setting use_bitmap to False, e.g. use_win_as_cls(False)

        Input Parameters :
        
        - use_bitmap        \t- [optional] When true, this sets the current window display as the cls() bitmap.  
                                \t When False, this returns cls() to its normative state that simply clears the window canvas.
        """
        return _pybox.WindowUseWinasCls(self.__id,use_bitmap)
    
    def clip_window(self,x : int,y : int, width : int, height : int) :
        """
        Clips the window in the given rectangle, restricting output and drawing to that region.
        
        This can be used to restrict write areas, cls(), drawing, etc. 
        
        For example, a graph can be drawn with the clip and will not exceed the clip area.  This can be very useful and 
        allow such drawing and output in place of creating a child window to perform the same task.
        
        - Use  reset_clip() or clip_window() (with no paramaters) to remove the clipping region
        - see clip_window_l() to use a list for x,y and w,h input (respectively), e.g. clip_window_l(pos,size)
        - see clip_window_r() to use a list for input x,y, width height, e.g. clip_window_r((x,y,w,h))
        
        Input Parameters:
        
        - x,y                   -\t x,y position of upper-left of clip rectangle
        - width, height         -\t width and height of rectangle from upper-left (x,y)
        """
        return _pybox.WindowClipWindow(self.__id,x,y,width,height)

    def clip_window_l(self,pos : list,size : list) :
        """
        Clips the window in the given rectangle, restricting output and drawing to that region.
        
        This can be used to restrict write areas, cls(), drawing, etc. 
        
        For example, a graph can be drawn with the clip and will not exceed the clip area.  This can be very useful and 
        allow such drawing and output in place of creating a child window to perform the same task.
        
        - Use  reset_clip() or clip_window() (with no paramaters) to remove the clipping region
        - see clip_window() to use independent values for x,y, and width,height, e.g. clip_window(x,y,width,height)
        - see clip_window_r() to use a list for input x,y, width height, e.g. clip_window_r((x,y,w,h))
        
        Input Parameters:
        
        - pos                   -\t x,y position of upper-left of clip rectangle
        - size                  -\t width and height of rectangle from upper-left (x,y)
        """
        return _pybox.WindowClipWindow(self.__id,size_rect[0],size_rect[1],size_rect[2],size_rect[3])
   
    def clip_window_r(self,size_rect : list) :
        """
        Clips the window in the given rectangle, restricting output and drawing to that region.
        
        This can be used to restrict write areas, cls(), drawing, etc. 
        
        For example, a graph can be drawn with the clip and will not exceed the clip area.  This can be very useful and 
        allow such drawing and output in place of creating a child window to perform the same task.
        
        - Use  reset_clip() or clip_window() (with no paramaters) to remove the clipping region
        - see clip_window() to use independent values for x,y, and width,height, e.g. clip_window(x,y,width,height)
        - see clip_window_l() to use a list for x,y and w,h input (respectively), e.g. clip_window_l(pos,size)
        
        Input Parameters:
        
        - size_rect             -\t list/array with 4 values: x,y, width and height (x,y position of upper-left of clip rectangle, and width, height)
        """
        return _pybox.WindowClipWindow(self.__id,size_rect[0],size_rect[1],size_rect[2],size_rect[3])

    def reset_clip(self) :
        """
        Resets any clipping region active for the current window. 
        
        See clip_window() for more information
        """
        return _pybox.WindowResetClip(self.__id)

    def update(self) :
        """
        Updates the window. 

        With Pybox in Python, this is usually not needed.  Pybox is set to update the window automatically from 10-25ms.  However, for real-time uses,
        setting the udpates to passively "On" means that update() may be needed in some loops, as it better to turn off updates when displaying real-time data. 

        The default for Updates in Pybox is "on_time", where setting Updates to simple "On" gives more control over updating, but also must be managed a little -- Any window that needs updated 
        (i.e. has been written to since the last udpate) is still updated every 10-20ms, but in a passive manner when Pybox functions are called.

        When Updates are not completely automatic, pybox updates the window whenever most display, event or other function are called.  Pybox only updates windows that need it.
        However, when a pybox function is not called for a while (such as being in a long loop), the Update may lag.  Update() can be called to ensure the window is updated.

        Even when Updates are simple "on" i.e. passive, get_event() updates any window that needs it.  If you're in an event loop, the Window will only not be updated (as needed) when
        Updates are completel turned "off:

        See set_auto_update() for more information.
        """
        return _pybox.WindowUpdate(self.__id)
    
    def dont_update(self) :
        """
        Tells Pybox not to update any window until the next pdate() is called manually by the program. 
        Pybox will stop updating completely -- even on Window repaints -- until pdate() is once again called by the program. 

        This can be useful when generating real-time displays to avoid flickering and partial information being displayed before it is ready.
        """
        return _pybox.WindowDontUpdate(self.__id)

    def set_auto_update(self,updateType : str) :
        """
        Sets the auto update type in pybox. See Update() for more information.

        The default for pybox is "Immediate".  The default for C++ Sagebox is "On"

        on -    The window will auto passively update every 10-20ms.  This means when any pybox display or GetEvent function is called and a window needs
                Updating, pybox will do it, but it is not guaranteed for code that lingers/loops after the last display function.  
            
                For most applications, pybox will update the window when necessary, since any waiting (i.e. exit_button() or get_event()) function or
                display function (i.e. Write()) will update the window if the window needs it. 

                In loops that can take time, or without a pybox call of some sort, sometimes a pybox.Update() may
                be necessary to ensure the window is updated.

        off -   The window will not be updated, and it is the program's responsibility to do so.
                This can be useful when redrawing the screen in a real-time setting, to avoid flashing.

        immediate - Updates the screen after every single display operation.  This can be slow when a lot of data is put out to the screen, but it is
                    guaranteed and the update status never needs to be managed.  This can be useful for putting out data from equipment, etc. 
                    Also see 'OnTime'

        on_time - The update is mixed with 'On' (which updates when a Pybox function see the window needs it) and a timer in the 25ms range.
                    If Pybox has not updated the window on its own within 25ms, the timer set will instruct Pybox to do it immediately behind the scenes.
                    This can be a good mode because it is fast and guaranteed, because the window is only updated every 10-20ms, with a follow-up if
                    no Pybox functon was called in that time. 

                    This mode can interfere with real-time displays, so setting the Update to either On or Off can be more streamlined in this type of application.

        """
        return _pybox.WindowSetAutoUpdate(self.__id,updateType)

    def closing(self) :
        """
        Returns true if the Window is closing due to a button press or some other action.

        Use close_button_pressed() (which sets closing status) to determine if the user pressed the button specifically.

        --> This function an EVENT function: This function will only return a True value ONE TIME PER EVENT 
        --> and will return False after the first call until the event occurs again. 

            In most events, you can specify "peek=true" as a parameter so that the event will not be reset.
        """
        return _pybox.WindowClosing(self.__id)

    def closed(self) :
        """
        Returns true if the Window is closing due to a button press or some other action.

        Use close_button_pressed() (which sets closing status) to determine if the user pressed the button specifically.

        --> This function an EVENT function: This function will only return a True value ONE TIME PER EVENT 
        --> and will return False after the first call until the event occurs again. 

            In most events, you can specify "peek=true" as a parameter so that the event will not be reset.
        """
        return _pybox.WindowClosing(self.__id)

    def close_button_pressed(self) -> bool:
        """
        Returns true if the user pressed the close button on the window (upper-right-hand X or pressed ALT-F4). 
        Pressing the close button sets the Window Closing status.

        You can also use Closing() to determine if the Window wants to close for any reason (i.e. pressing the close button or some system action)

        --> This function an EVENT function: This function will only return a True value ONE TIME PER EVENT 
        --> and will return False after the first call until the event occurs again. 

            In most events, you can specify "peek=true" as a parameter so that the event will not be reset.
        """
        return _pybox.WindowButtonClosing(self.__id)

    def mouse_moved(self) -> bool :
        """
        Returns true if a mouse move event has occured.  

        Use get_mouse_pos() to get the current mouse position in the window. 

        --> This function an EVENT function: This function will only return a True value ONE TIME PER EVENT 
        --> and will return False after the first call until the event occurs again. 

            In most events, you can specify "peek=true" as a parameter so that the event will not be reset.
        """
        return _pybox.WindowMouseMoved(self.__id)

    def mouse_drag_event(self,*args) -> bool :
        """
        Returns True if a Mouse Drag Event has occured in the window.

        A Mouse Drag Event is when the mouse is moved while the mouse button is pressed.

        Optional Parameters: 

        1. True - a value of True (i.e. MouseDragEvent(True)) will return true for a Drag Event if the mouse button is simply clicked
        \t -(but not moved).  Otherwise, you can use a MouseButtonDown() call

        2. pybox.peek -- Since this is an event, this function will return true only once until the event occurs again.
        \t -using Peek (i.e. MouseDragEvent(Peek)) will keep the event status as True so it may be called again to receive the
        \t -same event (True) status.

        Examples: 

        Win.mouse_drag_event()          \t\t --- Returns True if the mouse is being dragged (does not include initial click)
        Win.mouse_drag_event(True,peek) \t --- Include the initial mouse button click, and do not reset the event

        See also MouseDragPos() and MouseDragPrev() to get the mouse coordinates of the Mouse Drag Event.
 
        --> This function an EVENT function: This function will only return a True value ONE TIME PER EVENT 
        --> and will return False after the first call until the event occurs again. 

            In most events, you can specify "peek=true" as a parameter so that the event will not be reset.
        """
        return _pybox.WindowMouseDragEvent(self.__id,*args)

    def mouse_drag_ended(self,*args) -> bool :
        """
        This event occurs when a mouse drag event is active and the left mouse button is released. 
        This is essentially the same as a MouseButtonUp event. 

        Use mouse_drag_last() to get the last mouse drag position. 

        --> This function an EVENT function: This function will only return a True value ONE TIME PER EVENT 
        --> and will return False after the first call until the event occurs again. 

            In most events, you can specify "peek=true" as a parameter so that the event will not be reset.
        """
        return _pybox.WindowMouseDragEnded(self.__id,*args)

    def mouse_drag_pos(self) -> list :
        """
        Returns the last mouse drag mouse coordinates.  When the mouse is moving and a mouse drag event occurs, this function
        will retrieve the mouse coordinates associated with the event.
        
        get__mouse_pos() will return the current mouse coordinates (which should be essentially the same point as the last mouse drag point)
        """
        return _pybox.WindowMouseDragPos(self.__id)

    def mouse_drag_prev(self) -> list :
        """
        Returns the previous mouse drag points before the current mouse drag points (defined in MouseDragPos()).

        Using mouse_drag_prev() with mouse_drag_last() allows determining the points between the current point and previous point. 

        For example, in response to a mouse_drag_event(), mouse_drag_prev() and mouse_drag_last() will be the two points between the current point and the last point, 
        such as drawing a line.

        If there has only been one mouse drag event (such as the initial mouse click, when set as an option), mouse_drag_prev() and mouse_drag_last() will return the same point.

        """
        return _pybox.WindowMouseDragPrev(self.__id)

    def mouse_clicked(self,*args) -> bool :
        """
        Returns True if the Left Mouse Button was clicked, False if not and for subsequent events until the next mouse click.

        --> This function an EVENT function: This function will only return a True value ONE TIME PER EVENT 
        --> and will return False after the first call until the event occurs again. 

            In most events, you can specify "peek=true" as a parameter so that the event will not be reset.
        """
        return _pybox.WindowMouseClicked(self.__id,*args)

    def mouse_button_down(self) -> bool :
        """
        Returns True if the Left Mouse button is currently pressed False if it is not pressed.
        """
        return _pybox.WindowMouseButtonDown(self.__id)

    def mouse_r_clicked(self,*args) -> bool :
        """
        Returns True if the Right Mouse Button was clicked, False if not and for subsequent calls until the next mouse click.

        --> This function an EVENT function: This function will only return a True value ONE TIME PER EVENT 
        --> and will return False after the first call until the event occurs again. 

            In most events, you can specify "peek=true" as a parameter so that the event will not be reset.
        """
        return _pybox.WindowMouseRClicked(self.__id)
    def mouse_r_button_down(self) -> bool :
        """
        Returns True if the Right Mouse button is currently pressed False if it is not pressed.
        """
        return _pybox.WindowMouseRButtonDown(self.__id)

    def get_mouse_pos(self) -> list :
        "Returns the current Mouse Position.  See get_mouse_click_pos() to retrieve the last clicked position."
        return _pybox.WindowGetMousePos(self.__id)

    def get_mouse_click_pos(self) -> list :
        """
        Returns the last mouse clicked position (Left mouse button click)

        This can be useful for responding to a MouseClick event in obtaining the point where the mouse was clicked as opposed
        to the current mouse position (GetMousePos()), which can be different.  In this case, GetMouseClickPos() can be an exact location of
        where the mouse was clicked.
        """
        return _pybox.WindowGetMouseClickPos(self.__id)

    def mouse_wheel_moved(self) -> bool :
        """
        Returns True if the mouse wheel was moved, False if not or for subequent calls until the next time the MouseWheel is moved (i.e. a new event)

        See: get_mousewheel_value() to get the value and direction of the MouseWheel movement.

        --> This function an EVENT function: This function will only return a True value ONE TIME PER EVENT 
        --> and will return False after the first call until the event occurs again. 

            In most events, you can specify "peek=true" as a parameter so that the event will not be reset.
        """
        return _pybox.WindowMouseWheelMoved(self.__id)

    def get_mouse_wheel_value(self) -> int :
        """
        Returns the value of the last mousewheel movement (-1 or 1 usually).  See MouseWheelMoved() to check when the event occurs.

        This returns the results of the last event and will return the same value until a new event occurs. 

        Usually the value is -1 or 1 to indicate direction, and can be higher (such as -2 or 2) to reflect a mousewheel that has moved very quickly.

        This value can be used to multiply against an increase or decrease in value, such as:

        if MyInputBox.mouse_wheel_moved() : MyValue += Increment*get_mouse_wheel_value()
        """
        return _pybox.WindowGetMouseWheelMove(self.__id)

    def capture_mouse(self) :
        """
        capture_mouse() will allow the mouse to be moved and pass events to the window even when the mouse is outside the window.
        This can occur only when the mouse button is down and the capture is released once the left mouse button is released.

        While the left mouse button is pressed, the mouse movements will be reported as events no matter where the mouse is located.
        Without the mouse capture, the mouse movements (even with the mouse button down) are no longer reported or seen as events once the mouse is
        outside the window.

        This function is useful for drawing routines where the mouse can move outside of the window.
        """
        return _pybox.WindowCaptureMouse(self.__id)

    def capture_release(self) :
        """
        Release the mouse capture.  See capture_mouse()

        Usually the mouse capture is released automatically when the left mouse button is released.
        capture_release() will release the capture even if the mouse button is down, and can be a good way to ensure
        the mouse capture is no longer active.

        See: capture_released() to respond to a release-capture event.
        """
        return _pybox.WindowCaptureRelease(self.__id)

    def capture_released(self,*args) :
        """
        Returns True if the Capture was released, False if not or for subsequent calls until the next Capture Release event.

        --> This function an EVENT function: This function will only return a True value ONE TIME PER EVENT 
        --> and will return False after the first call until the event occurs again. 

            In most events, you can specify "peek=true" as a parameter so that the event will not be reset.
        """
        return _pybox.WindowCaptureReleased(self.__id,*args)

    def create_menu(self,menuString : str) -> bool :
        """
        Creates a standard menu bar in the window with the menu items in the menuString.

        - The menu string can contain simple items such as: window.create_menu("Help,About,Exit")
        - Menu string can also contain submenu items, such as: window.create_menu("File[Open,Save,SaveAs],About,Exit")
        - Menu items can be retrieved by name, such as "File","About", or in the case of sub-menu items, "File:Open"
        - Menu items can be retrieved by value as well.

        To set a value in a menu, enter a number for each top-level item, such as "File=100[Open,Save,Save As],About=200,Exit=300"

        The submenu values will be the value of the parent + 1 + its position. 
        For example, "File:Open", "File:Save", and "File:Save As" are numbered 101,102,103, respectively. 

        To use the symbolic names, the menu items must appear in the same manner, such as "File:Save As", but not "File:SaveAs". 
        "file:save as" and "FILE:SAVE AS" are also ok as the names are not case-sensitive.

        See other menu functions such as get_menu_id(),is_menu_id_selected(), etc. 

        Menu items may be enabled, disabled, checked and unchecked. 

        You can also hide the main menu from view and make it reappear. 

        note: CreateMenu() and QuickMenu() are the same function.  The naming convention hasn't quite been decided.

        Examples: 

        window.create_menu("Help,About,Exit")   - create a simple menu
        window.create_menu("File[Open,Save,Save As,Exit],About,Help") - create a little more complex menu with sub items
        window.create_menu("File=100[Open,Save,Save As,Exit],About=200,Help=200") - create a little more complex menu with sub items and user-defined ID values


        The menu will appear in the window when it is first created.  Use ShowMenu() and HideMenu() to show/hide the menu.
        """
        return _pybox.WindowCreateMenuString(self.__id,menuString)

    def quick_menu(self,menu_string : str) -> bool :
        """
        Creates a standard menu bar in the window with the menu items in the menuString.

        - The menu string can contain simple items such as: window.quick_menu("Help,About,Exit")
        - Menu string can also contain submenu items, such as: window.quick_menu("File[Open,Save,SaveAs],About,Exit")
        - Menu items can be retrieved by name, such as "File","About", or in the case of sub-menu items, "File:Open"
        - Menu items can be retrieved by value as well.

        To set a value in a menu, enter a number for each top-level item, such as "File=100[Open,Save,Save As],About=200,Exit=300"

        The submenu values will be the value of the parent + 1 + its position. 
        For example, "File:Open", "File:Save", and "File:Save As" are numbered 101,102,103, respectively. 

        To use the symbolic names, the menu items must appear in the same manner, such as "File:Save As", but not "File:SaveAs". 
        "file:save as" and "FILE:SAVE AS" are also ok as the names are not case-sensitive.

        See other menu functions such as get_menu_id(),is_menu_id_selected(), etc. 

        Menu items may be enabled, disabled, checked and unchecked. 

        You can also hide the main menu from view and make it reappear. 

        note: CreateMenu() and QuickMenu() are the same function.  The naming convention hasn't quite been decided.

        Examples: 

        window.quick_menu("Help,About,Exit")   - create a simple menu
        window.quick_menu("File[Open,Save,Save As,Exit],About,Help") - create a little more complex menu with sub items
        window.quick_menu("File=100[Open,Save,Save As,Exit],About=200,Help=200") - create a little more complex menu with sub items and user-defined ID values


        The menu will appear in the window when it is first created.  Use ShowMenu() and HideMenu() to show/hide the menu.
        """
        return _pybox.WindowCreateMenuString(self.__id,menu_string)

    def is_menu_id_selected(self,menu_item) -> bool :
        """
        Returns true of a Menu Item has been selected in response to a menu_item_selected() event returning true.

        menu_item_selected() must be called to determine a menu event has been triggerred (i.e. a menu item was selected). 
        is_menu_id_selected() will return true if the menu item requested was selected. 

        Also see: get_selected_menu_item() to get the numerical ID value of the item selected.

        Parameters:

        - menu_item      \t -- this can be the numerical ID of the menu item or the menu item's name (i.e. "File", "File:Save As", etc.)

        note: This function will always return the value of the last menu item selected.  Use MenuItemSelected() to determine when a menu item is selected.
        """
        return _pybox.WindowisMenuIDSelected(self.__id,menu_item)

    def enable_menu_item(self,menu_item,enable : bool = True) -> bool :
        """
        Enables (or disables) a menu item.  When disabled, the menu item is grayed-out. 
        Also see: DisableMenuItem()

        Parameters:

        - menu_item      \t -- this can be the numerical ID of the menu item or the menu item's name (i.e. "File", "File:Save As", etc.)
        - enable         \t -- when True (default), the menu item is enabled.  Othewise it is disabled.

        """
        return _pybox.WindowEnableMenuItem(self.__id,menu_item,enable)

    def disable_menu_item(self,menu_item,disable : bool = True) -> bool :
        """
        Disables (or enables) a menu item.  When disabled, the menu item is grayed-out. 
        Also see: EnableMenuItem()

        Parameters:

        - menu_item      \t -- this can be the numerical ID of the menu item or the menu item's name (i.e. "File", "File:Save As", etc.)
        - bDisable         \t -- when True (default), the menu item is disabled.  Othewise it is enabled.

        """        
        return _pybox.WindowDisableMenuItem(self.__id,menu_item,disable)

    def set_menu_item_check(self,menu_item,checked : bool = True) -> bool :
        """
        Sets or unchecks a menu item.  Note that only sub-menu items can be checked or unchecked.

        Parameters:

        - menu_item     \t -- this can be the numerical ID of the menu item or the menu item's name (i.e. "File", "File:Save As", etc.)
        - checked           \t -- when True, the menu item is checked.  When False, the menu item is unchecked.

        """                
        return _pybox.WindowSetMenuItemCheck(self.__id,menu_item,checked)

    def show_menu(self,show_menu : bool = True) -> bool :
        """
        Shows (or hides) the menu bar in the window.
        Also see: hide_menu()

        Parameters:

        - show_menu         \t -- when True (default), the menu is shown in the window.  When False, the menu is hidden.

        """        
        return _pybox.WindowShowMenu(self.__id,show_menu)

    def hide_menu(self,hide_menu : bool = True) -> bool :
        """
        Hides (or shows) the menu bar in the window.
        Also see: show_menu()

        Parameters:

        - hide_menu         \t -- when True (default), the menu is hidden from the window display.  When False, the menu appears in the window.

        """        
        return _pybox.WindowHideMenu(self.__id,hide_menu)

    def get_menu_id(self,menu_string : str) -> bool :
        """
        Returns the menu ID of the menu string. 

        When a menu is created, such as "File[Save, Save As],Help,About", ID numbers are automatically assigned for each element. 

        In cases where the numbers are assigned in the CreateMenu call, such as "File=100[Save, Save As],Help=200,About=300", the numbers are specified by the program.

        When numbers aren't specified, or to be sure of a number, get_menu_id() will return the value assigned to the menu item.

        Example: window.GetMenuID("File") or window.get_menu_id("File:Save As")

        The latter returns the value assigned to "File:Save As" which can be used later in functions instead of the names. 
        """
        return _pybox.WindowGetMenuItemID(self.__id,menu_string)

    def menu_item_selected(self) -> bool :
        """
        Returns True of a menu item was selected, False if not or afterwards until another menu item is selected.

        Once a menu item is selected, GetSelectedMenuItem() can be used to retreive the menu item ID of the menu selected.
        isMenuIDSelected() can be used with a menu ID value or string name to query if a specific menu item was selected.

        Example:
            if window.menu_item_selected() : 
                menuID = window.get_selected_menu_item()
                ... <deal with menuID> ...

            or

            if window.menu_item_selected() : 
                menuID = window.get_selected_menu_item()
                if window.is_menu_id_selected("File:Save as") : <do something>
                if window.is_menu_id_selected("About") : <do something> 
                etc.

        window.is_menu_id_selected(<menu item ID number) may also be used.

        --> This function an EVENT function: This function will only return a True value ONE TIME PER EVENT 
        --> and will return False after the first call until the event occurs again. 

            In most events, you can specify "peek=true" as a parameter so that the event will not be reset.

        """
        return _pybox.WindowMenuItemSelected(self.__id)

    def get_selected_menu_item(self) -> int :
        """
        Returns the menu item selected.  This function is called in response to a True value return from WindowItemSelected() call, which
        tells of a menu selection event.

        get_selected_menu_item() returns the menu ID number of the selected item.  Therefore, the menu ID number of the menu item must be known to use the
        value.

        See: get_menu_id() to retrieve the menu id number of a string text menu item, such as "File:Save As"

        See: is_menu_id_selected() to determine if a specific menu item ID has been selected.  This function will accept menu strings, such as:
        \t -iis_menu_id_selected("File:Save as") 
        """
        return _pybox.WindowGetSelectedMenuItem(self.__id)

    def print_menu_items(self) -> bool :
        """
        Prints a list of all menu item strings with their IDs to the console window and Sagebox Process Window

        This function is helpful in making sure the numbers of the menu items align with expectations. 

        After creating a menu with create_menu()  (i.e. "File[Open, Save, Save As, Exit],Help,About"), print_menu_items() can be used
        to show the numbers of each item. 

        Menu numbers can be assigned by the program, such as: "File=100[Open, Save, Save As, Exit],Help=200,About"

        --> Basically, print_menu_items() performs a sanity-check to understand and confirm the menu ID values of each menu item and their string values as well.
        """
        return _pybox.WindowPrintMenuItems(self.__id)

    def color_selector(self,at=None,**kwargs) -> _ColorSelector :
        """
        Opens a Color Selector widget, either in the current window or as a popup window. 
        
        With the color selector, you can select an RGB color using the wheel or input boxes next to the wheel itself. 
        A color rectangle is shown with the currently selected color.
        
        color_selector returns a _ColorSelector object which can be used to look at changes in the color wheel in the window's main event loop. 
        
        See the _ColorSelector object functions for more information.
        
        Parameters:
        
        - at          \t - Where to put the Color Selector (in the window or as a popup).  If this is not used, the Color Selector is placed automatically.

        Keywords usable when creating the Color Selector:

        - Popup         \t - When true (i.e. Popup=True), the window pops up as a separate window.  Otherwise, it is placed in the current window at the location specified
        - x,y           \t - 'x' and 'y' keywords can be used in place of using the 'at' parameter, i.e. x=500, y=200 instead of (500,200) or at=(500,200)
  
        examples:\t - color_sel = mywin.color_selector(at=(500,200),popup=True)     --> Opens a Color Selector window as an individual window on the screen at x=500 and y=200
        - color_sel = mywin.color_selector(at=(500,200))     --> Opens a Color Selector window inside the window 'mywin, at window location x=500 and y=200
        - color_sel = pybox.color_selector(at=500,200)  --> Opens the same type of window, but as a pybox function without a parent window.
        
        - while mywin.GetEvent() : if (color_sel.value_changed()) print("Color value = ",color_sel.get_rgb_value()) --> prints values as the wheel is moved.
        """
        return _ColorSelector(_pybox.WindowColorSelector(self.__id,opt.at(at),**kwargs))

    def color_wheel(self,at=None,**kwargs) -> _ColorWheel :
        """    
        Creates a Color Wheel widget, put into the existing window as a single color wheel with no other controls but the wheel itself.
        
        With the color selector, you can select an RGB color using the wheel or input boxes next to the wheel itself. 
        A color rectangle is shown with the currently selected color.
            
        color_wheel returns a _ColorWheel object which can be used to look at changes in the color wheel in the window's main event loop. 
            
        See the _ColorWheel object functions for more information.
            
        Parameters:
            
        - at          \t - Where to put the Color Selector (in the window or as a popup).  If this is not used, the Color Selector is placed automatically.

        Keywords usable when creating the Color Selector:

        - x,y           \t - 'x' and 'y' keywords can be used in place of using the 'at' parameter, i.e. x=500, y=200 instead of (500,200) or at=(500,200)
  
        example:\t - color_wheel = mywin.color_wheel((500,200))     --> Opens a Color Wheel window in the window at (500,200)
            
        - while mywin.GetEvent() : if (color_wheel.value_changed()) print("Color value = ",color_wheel.get_rgb_value()) --> prints values as the wheel is moved.
        """
        return _ColorWheel(_pybox.WindowColorWheel(self.__id,opt.at(at),**kwargs))
    
class DevControl :
    "--comment--"
    def __init__(self,_id) : self.id = _id

    def set_config(*args,**kwargs) -> bool :
        """
        Sets various configuration values for the Dev Window.  Note: autoclose, closeable, and topbar only work for Dev Window that are separate windows
        (i.e. not embedded in QuickForm or other windows)

        Most values can be set through various Dev Window function.  set_config() is a way to set multiple options at 
        once, as well as setting values that don't have a specific functions.

        set_config() works with the following keywords:

        - bgcolor         \t -Sets the background color of the dev window.  This can be a single color or a string with one or two colors (for a gradient)
                          \t -note: this should be used before any controls are placed in the dev window. Also see set_bg_color() for more options

        - bgbitmap        \t -Sets the bitmap of the dev window background.  This can be a pybox Cbitmap type, and bitmap array (i.e. opencv, etc.),
                          \t -or a text string with the location of the bitmap.
                          \t -note: this should be used before any controls are placed in the dev window. Also see set_bgbitmap() for more options.

        - ypos            \t -Sets the position of the next control.  This can be used to set the location of the first control when setting bgbitmap when the bitmap contains a top header.

        - autoclose_x     \t -Sets the auto close 'x' button on or off.  By default, an 'x' is placed on the window to allow the user to close it.
                          \t -autoclose_x=false will turn this 'x' off and also prevent the 'x' from appearing when the Dev Window is the only window open during get_event() calls.
                          \t -see the 'allowclose' option to set the 'x' visibility in other ways

        - autoclose       \t -When set to true, this will cause the Dev Window to close automatically when no other non-dev (or other primary) windows are open.
                          \t - otherwise, when set to false (default) the Dev Window will remain open when other windows are closed (with an 'x' placed for closure).

        - closeable       \t -Sets the 'x' button on or off when multiple windows are open.  By default, the 'x' appears in all Dev Windows to allow the user
                          \t -to close it, at which time the window will automatically close. closeable=True will force the 'x' on the window.

                          \t -setting closeable=false will remove the 'x' when there are non-Dev windows open. the 'x' will appear when no other windows are open
                          \t -to allow the user to close the window. See 'autoclose_x' option to disable the 'x' permanently.

        - topbar          \t -Turns the topbar off (when false). When topbar=false, the top title bar will not appear in the dev window.
                            \t -this is used for setting the background color and bgbitmap to help personalize the dev window.
                             \t -note --> topbar must be used before the bgbitmap or bgcolor option, otherwise it will have no effect.
                           \t -see set_bgbitmap() and set_bg_color() for more information
        """
        return _pybox.DevControlSetConfig(*args,**kwargs)

    def closed(self,add_closebutton : bool = False) -> bool :
        """
        Returns True if the dev window was closed.  This is not an event and will return True continuously once the dev window is closed.

        Note: When closed() is called, an 'x' will be added to the upper-right part of the window.

        Parameters:

            - add_closebutton      \t -- When 'true', a close button will be added as a control at the bottom of the dev window
        """
        return _pybox.DevControlWindowClosed(self.id,add_closebutton)

    def set_nexty(self,y : int) -> bool :
        """
        Sets the Y position in the Dev Window for the next control.
        This can be useful in setting a top header bitmap, or moving controls
        down when setting a header bitmap. 

        As with setting the background color or bitmap, set_nexty() should be used
        before any controls are added to the dev window.
        """
        return _pybox.DevControlSetNextY(self.id,y)

    def set_bg_color(self,color1,color2 = None,display_bar : bool = True) -> bool :
        """
        Sets the background color of the dev window. 

        Note: This only works if it is called before any controls are added to the Dev Window. 

        Parameters:

            - color1      \t -- Color of the background 
            - color2      \t -- [optional] When given, this sets a gradient from color 1 to color 2
            - display_bar \t -- [optional] When set to True (default) the top display bar is kept and the bitmap is displayed underneath
                          \t - when set to False, the top display bar is removed and the bitmap starts at the top of the window.
        About Colors

        Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
        Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

        Examples:

            my_dev.set_bg_color("black"); 
            my_dev.set_bg_color("black","blue");
            my_dev.set_bg_color(PanColor.ForestGreen())

        """
        return _pybox.DevControlSetBgColor(self.id,color1,color2,display_bar)

    def set_bgbitmap(self,bitmap,display_bar : bool = True,*args,**kwargs) -> bool :
        """
        Sets the background bitmap of the Dev Window

        Note: This only works if it is called before any controls are added to the Dev Window. 

        This bitmap should cover the width and height the Dev Window will be at its maximum.
        Dev Windows grow vertically when controls are added, and the bitmap should cover this space.

        Parameters:

            - bitmap      \t -- The bitmap to display.  This can be a path to the bitmap or a loaded bitmap.
            - display_bar \t -- [optional] When set to True (default) the top display bar is kept and the bitmap is displayed underneath

        Keywords and other options

            - pady      \t -- opt.pady() or pady=True can be used to set the position of the next control relative to the bottom of the bitmap.
                        \t - For example, pady(20) will add 20 pixels to the bottom of the bitmap for the next control

                        This can be useful when a background bitmap has a header, so the first control can start underneath it.

        Examples:

            my_dev.set_bgbitmap("c:\\bitmaps\\mybitmap.jpg")
            my_dev.set_bgbitmap(MyBitmap,pady=(20))

        """
        return _pybox.DevControlSetBgBitmap(self.id,bitmap,display_bar,*args,**kwargs)

    def new_bitmap(self,bitmap,text = None,*args,**kwargs) -> bool :
        """
        Puts a bitmap in the dev window at the current place for the next control. 

        The bitmap can contain a transparency (as a .png or 32-bit bitmap) to blend into the background.

        Bitmaps in the Dev Window are meant to be either icons or header-style bitmaps, and are usually small vertically to keep
        space for the controls.

        Parameters:

            - bitmap      \t -- The bitmap to display.  This can be a path to the bitmap or a loaded bitmap.
            - text        \t -- [optional] Text to place directly to the right of the bitmap.  Pybox options can be used
                            \t - to set the font and text color

                            The center of the text is aligned to be at the center vertical center of the bitmap. 

        Keywords and other options

            - font,textcolor       \t -- These can set the font and color of the text. i.e. opt.textcolor("green") or opt.font(20)
            - pady                 \t -- this will add to the Y value of the next control relative to the bottom of the bitmap or text
                                    \t - (whichever hangs over more).  For example, pady(20) will add 20 pixels to the start of the next control.

                                    \t -This can be useful when the bitmap (and text) is a header, to add space before the next control starts

        Examples:

            my_dev.new_bitmap("c:\\bitmaps\\mybitmap.png")
            my_dev.new_bitmap("c:\\bitmaps\\mybitmap.png"," Project Controls")      -- note the space to add space between the image and text
            my_dev.new_bitmap("c:\\bitmaps\\mybitmap.png"," Project Controls",font=20,textcolor=green)
        """
        return _pybox.DevControlBitmap(self.id,bitmap,text,*args,**kwargs)

    def new_text(self,text = None,*args,**kwargs)          : 
        """
        Create a text widget int the Dev Window.    This is the same type of Text Widget that can be created in a regular
        window with window.TextWidget(), but automatically placed and sized in the Dev Window. 

        Since the Text Widget is automatically placed and sized in the window, fewer options are needed. 

        new_text() returns a CTextWidget object where you can write out to the text widget.

        The Text Widget can be used to create static or dynamic text of any font size in the Dev Window.
        Parameters:

        - text          \t -- [optional] Sets the text of the widget.  This can be set later with textwidget.Write()
                        \t - When text is entered, the text widget is created to the width of the text.  Use the width() parameter to set a width or pad
                        \t - the text with spaces to reserve width.

        Keywords and Pybox options can be included.  Some various options are as follows:

        - TextColor         \t - Sets the text color of the widget (default is current window text color).  Same as opt.fgcolor()
        - Font              \t - Sets the font of the text in the text widget
        - TextCenter        \t - Centers the text inside of the widget (which can be longer than the text itself).
                                \t - Use TextCenterX() and CenterX() together to make sure text is centered in the window. This is only needed if the Width of the
                                \t - Text Widget and the text have been specificed separately.


        Examples:   
                    \t -my_dev.new_text(This is a text Widget)
                    \t -my_dev.new_text(This is a text Widget",font=20,textcolor="Yellow")
        """        
        return CTextWidget(_pybox.DevControlTextWidget(self.id,text,*args,**kwargs))

    def new_slider(self,title : str = None,*args,**kwargs) : 
        """
        Creates a slider in the Dev Window. The slider is automatically placed.

        A Slider class object is returned where the slider can be accessed and controlled. 

        Parameters:

        - title     \t -- Sets the title of the Slider

        Keywords and Pybox options can be included.  Some various options are as follows:

        - Range             \t -- Set the range of the slider.  The default range is (1,100)          
        - Default           \t -- Set the default value of the slider.  The edfault is (0)
        - TextColor         \t -- Sets the color of the label of the slider.
        - Style("small")    \t -- Sets a smaller slider handle

        Examples:       \t -MyDevWindow.new_slider("This is a slider")
                        \t -MyDevWindow.new_slider("This is a slider",range=100,500,default=200)
                        \t -MyDevWindow.new_slider("This is a slider",textcolor="Yellow",valuecolor="red",style="small")
                        \t -MyDevWindow.new_slider("This is a slider",opt.textcolor("Yellow"),opt.valuecolor("red"),opt.style("small))        \t - - (same as previous example)
        """
        return Slider(_pybox.DevControlSlider(self.id,title,*args,**kwargs))

    def new_slider_f(self,title : str = None,*args,**kwargs) : 
        """
        Creates a floating-point slider in the Dev Window. The slider is automatically placed.

        A Slider class object is returned where the slider can be accessed and controlled. 
        A floating-point slider sets a default range of 0-1.0

        User slider.get_pos_f() and slider.set_pos_f() to set and retrieve values.

        Range may be either direction (i.e. min,max or max, min). 

       Parameters:

        - title     \t -- Sets the title of the Slider

        Keywords and Pybox options can be included.  Some various options are as follows:

        - Range             \t -- Set the range of the slider.  The default range is (1,100)          
        - Default           \t -- Set the default value of the slider.  The edfault is (0)
        - TextColor         \t -- Sets the color of the label of the slider.
        - Style("small")    \t -- Sets a smaller slider handle

        Examples:       \t -MyDevWindow.new_slider_f("This is a slider")
                        \t -MyDevWindow.new_slider_f("This is a slider",range=100,500,default=200)
                        \t -MyDevWindow.new_slider_f("This is a slider",textcolor="Yellow",valuecolor="red",style="small")
        """
        return Slider(_pybox.DevControlSlider(self.id,title,opt._opt__as_float(),*args,**kwargs))

    def new_checkbox(self,title : str = None,*args,**kwargs) -> Button :
        """
        Create a checkbox in the Dev Window.  The Checkbox is automatically placed. 
        The checkbox is unchecked by default.  Use opt.default(True) to default to checked.

        Parameters:

        - title    \t -- Sets the title of the checkbox 

        Keywords and Pybox options can be included.  Some various options are as follows:

        - Default    \t -- Default(True) sets the check in the checkbox.  Default(False) leaves the checkbox unchecked.

        Examples:
                    \t -MyDevWindow.new_checkbox("Check me!")
                    \t -MyDevWindow.new_checkbox("Check me!",default=True)
                    \t -MyDevWindow.new_checkbox("Check me!",opt.default(True))
        """
        return Button(_pybox.DevControlCheckbox(self.id,title,*args,**kwargs))

    def new_button(self,text : str,*args,**kwargs) -> Button :
        """
        Create a Button in the DevWindow.  The Button is automtically placed.

        A Button type object is returned so the button can be used and events retrieved.

        Parameters:
        
        text        \t -- Sets the text of the button. 

        Keywords and Pybox options can be included.  Some various options are as follows:

        - Font     \t -- Sets the font for the button text 
        - Style    \t -- This can be a style of the default button or the name of a created button style.

        Example:   
                    \t -MyDevWindow.new_button("This is a button")
                    \t -MyDevWindow.new_button("This is a button",font=18,style="red"))
        """
        return Button(_pybox.DevControlButton(self.id,text,*args,**kwargs))

    def new_combobox(self,text : str = None,title_cell : str = None,*args,**kwargs) -> Combobox :
        """
        Creates a Combobox in the DevWindow.  The Combobox is automatically placed. 

        A Combobox is like a list box except that it consists of a single tab that expands when activated, 
        and rolls back up when released. 

        This allows multiple listbox-style entries to take only the space of the height of one text line. 

        NewCombobox returns a Combobox type object so that items may be added and deleted, and user selections retrieved. 

        Parameters:

        - text          \t -- [optional] Initial text in the combobox.  This text can be one line or multiple lines representing multiple entries.  See examples.
        - titlecell     \t -- [optional] Tells the combobox to display this string int the combobox tab when no item is selected.  Otherwise the first added item is displayed.

        Keywords and Pybox options can be included.  Some various options are as follows:

        - Default    \t -- Default selection.  This is the index to the default selection (0 is the first selection, 1 the second, etc.)

        Examples:

                    \t -MyDevWindow.new_combobox() 
                    \t -MyDevWindow.new_combobox("First Item") 
                    \t -MyDevWindow.new_combobox("First Item\\nSecond Item\\nThird Item") 
                    \t -MyDevWindow.new_combobox(titlecell="This is a combobox") 
                    \t -MyDevWindow.new_combobox("First Item\\nSecond Item\\nThird Item",default=2) 
        """
        return Combobox(_pybox.DevControlCombobox(self.id,text,opt.cb_titlecell(title_cell),*args,**kwargs))

    def new_inputbox(self,title : str = None,text : str = None,*args,**kwargs) -> InputBox :
        """
        Creates a new Input Box in the Dev Window.  The Inputbox is automatically placed.

        Optional Parameters:

        - title         \t -- [optional] Label of the input box (displays to the left), but can shorten the input box itself.
        - text          \t -- [optional] This sets the starting text for the input box.  Otheriwse the input box is left blank at first. 

        Keywords and Pybox options can be included.  Some various options are as follows:

        - NumbersOnly   \t -- Causes the input box to only accept numbers. 
        - ReadOnly      \t -- Sets the input box as read only so it can be used as a way to place a large amount of text that can be copied.
        - TextColor     \t -- Sets the color of the text in the input box
        - bgColor       \t -- Sets the background color of the text in the input box
        - Password      \t -- Causes the input box to display '*' for all text.
        - WinColors     \t -- Sets the background input box color and text color to the current window color instead of the default white-and-black colors. 
        - ThickBorder,Recessed      \t -These are two different border styles that can be used.

        Examples:   \t -MyDevWindow.new_inputbox("This is the title)          
                    \t -MyDevWindow.new_inputbox(text="This is the default text")
                    \t -MyDevWindow.new_inputbox("this is the title,"This is the default text",wincolors=True,thickborder=True)
        """
        return InputBox(_pybox.DevControlInputBox(self.id,title,opt.default(text),*args,**kwargs))

    def new_window(self,title : str = None,numlines : int = 0,*args,**kwargs) -> Window :
        """
        Creates a new Window in the Dev Window.  The window is placed automatically and may be used to put out text and 
        other data. 

        The window defaults to 10 lines but can be set to any number of lines.

        Optional Parameters:

        - title         \t -- [optional] Title of the window.  This displays above the window. The default is no title.
        - numlines      \t -- [optional] Sets the number of lines for the default font in the window.  The default is 10 lines

        Keywords and Pybox options can be included.  Some various options are as follows:

        - Font          \t -- Set the font for the window
        - TextColor     \t -- Set the text/foreground color for the window
        - bgColor       \t -- Set the background color for the window. 
        """
        return Window(_pybox.DevControlWindow(self.id,title,int(numlines),*args,**kwargs))

    def new_radiobuttons(self,label : str,buttons : str,*args,**kwargs) -> RadioButtonGroup   : 
        """
        Creates a group of Radio Buttons with an optional outer border and label.  

        The Radio Button group is placed in the window automatically.

        new_radio_buttons() returns a RadioButtonGroup object class where the buttons may be queried to see when pressed, and which 
        button was pressed.

        Parameters

        - title                 \t - - The title/label of the radio button group.  A box is drawn around the radio buttons with the title name.
        - buttons       \t - - The buttons to place in the checkbox group.  This can be one more more buttons, each button name separated by a a newline,
                                    \t -for example, "button" for just one button, or "button 1\\nbutton 2\\nbutton 3" for 3 radio buttons.

        Keywords and Pybox options can be included.  Some various options are as follows:

        - Default       \t -- Sets the default index for the highlighted button.  There can only be one active radio button.  Default sets the
                            \t - index of the active/highlighted button (i.e. 0 = first button, 1 = second button, etc.)

        Examples:        
                        \t -MyDevWindow.new_radio_buttons("These are radio buttons","This is the button")
                        \t -MyDevWindow.new_radio_buttons("These are radio buttons","button 1\\nbutton2\\nbutton 3")
                        \t -MyDevWindow.new_radio_buttons("These are radio buttons","button 1\\nbutton2\\nbutton 3",default=1)

        """
        return RadioButtonGroup(_pybox.DevControlRadioButtons(self.id,buttons,opt.label(label),*args,**kwargs))

class TurtleShell :
    """
    TurtleShell operates the same as Turtle Graphics in most ways.  The functions are the same, with some additions for opacities and gradients, as well as other functions.
    
    - TurtleShell does not display each segment drawing, showing each segment after it is drawn.  
    - As with Turtle Graphics, the speed can be set to show each element drawing.
    
    - Setting a speed to zero will allow for real-time graphics. 
    - TurtleShell is meant to be a Turtle Graphics environmemt with some additions to allow more functionality than original turtle graphics.
    - TurtleShell is a prototype at the moment, and the idea is to bring more functions into it, including GPU-based and 3-D Turtle Graphics.
    
    See various examples and documentation on TurtleShell functions for more information.
    """
    def __init__(self,_id) : self.id = _id
    def pen_up(self) -> bool :
        """
        Lifts the pen up.  Any actions performed with the pen up will not draw..
        When the pen is up, no graphics are drawn the the screen, allowing for positioning without graphic output.
        Use pen_down() to put graphic output to the window (lines, circles, etc.) 
        """
        return _pybox.WinTurtleGenBool(self.id,0)

    def pen_down(self) -> bool :
        """
        the pen down.  This causes any graphic output function (e.g. circle, forward, etc.) to draw grahics to the screen.
        the pen is up (e.g. pen_up() function), no graphics are drawn the the screen, allowing for positioning without graphic output.
        """
        return _pybox.WinTurtleGenBool(self.id,1)

    def end_fill(self) -> bool :
        """
        When a fill is in-progress after starting it with begin_fill(), calling end_fill() fills the area defined by all drawing calls called after begin_fill().
        See begin_fill() for more information.
        """
        return _pybox.WinTurtleGenBool(self.id,3)

    def right(self,angle) -> bool :
        """
        Rotates the current heading clockwise (i.e. right) the number of degrees in input angle.

        Angle is in degrees.
        """
        return _pybox.WinTurtleGenMixedValue(self.id,0,angle)
    
    def left(self,angle) -> bool :
        """
        Rotates the current heading counter-clockwise (i.e. left) the number of degrees in input angle.

        Angle is in degrees.
        """
        return _pybox.WinTurtleGenMixedValue(self.id,1,angle)
    
    def pen_size(self,pen_size) -> bool :
        """
        Sets the pen radius size for all drawing operations.  The default is 2 pixels.
        
        Example: 
        
        pen_size(10) sets the thickness for all drawing functions to a radius of 10 pixels.
        
        Input Parameters:
        
        - pen_size  \t- New pen radius
        """
        return _pybox.WinTurtleGenMixedValue(self.id,2,pen_size)
    
    def set_heading(self,heading) -> bool :
        """
        Sets the current heading for draw operations (i.e. heading of the turtle).

        Functions such as right(), left(), circle(), etc. adjust the heading accordingly.

        set_heading() sets a specific heading (value is in degrees)
        
        Input Parameters:
        
        -angle      \t - Angle (in degrees) of new heading.
        """
        return _pybox.WinTurtleGenMixedValue(self.id,3,heading)
    
    def set_speed(self,speed) -> bool :
        """
        Sets the speed of drawing operations.  Unlike classical Turtle Graphics, Turtle Shell currently draws entire elements at a time, such as a line, circle, etc.

        The input value sets the delay between showing drawn values in milliseconds.

        For example, setting speed(20) sets 20ms between showing drawn output.

        Setting speed(.5) sets half a millisecond.
        
        - note: speed(0) is a special case and will not show any drawing operations, relying on the program to update the window itself.  
        - This can be used for real-time drawing, to display the entirety of the results all at one time, not using time to display partial results.
        - Use window.set_realtime() (or set kw::Realtime() as a keyword when creating a window) to set Realtime() status for a window, for smoother real-time output. 
        """
        return _pybox.WinTurtleGenMixedValue(self.id,4,speed)
    
    def forward(self,num_pixels) -> bool :
        """
        Moves the current location forward at the angle of the current heading, the number of pixels specified.
        
        If the pen is down, a line is drawn from the current point to the next point.
        
        See pen_up() to move forward without using the pen.
        
        Also see: move_to(), which moves directly to a specified point.
        """
        return _pybox.WinTurtleGenMixedValue(self.id,5,num_pixels)
    
    def begin_fill(self,color,opacity : int = None) -> bool :
        """
        Starts a filled area enclosed by subsequent drawing functions.
        After begin_fill() is called, drawing functions are drawn and remembered.
        When end_fill() is called, the area enclosed by the drawing functions is filled with the color.
        the 'color' value sets the color for the fill. This color may jave an opacity, e.g. "red" (full opacity, the same as "red(255)") or "red(128)" (half-transparent)

        Input Parameters
        
        - Color         \t - Color to fill the enclosed area when end_fill() is called, e.g. "green", "green(128)", MyColor value, etc.
        - opacity       \t - [optional] opacity of color.  This can be used to add an opacity to a color if it doesn't already have an opacity value.
                              \t For example, "red(128)" already has an opacity value of 128.  However, for a calculated color, it can be easier to add an opacity with this parameter.
        """
        return _pybox.WinTurtleGenColorValue(self.id,0,color,opacity)
    
    def set_color(self,color) -> bool :
        """
        Sets the color for subsequent drawing operations. 
        
        Example:
        
        t.forward(100)  # draw 100 pixels in current heading in current color
        t.color("red")  # Set color to "red"
        t.forward(100)  # draws 100 pixels in current heading in color "red"
        
        ** note: color() and set_color() are the same function
        """
        return _pybox.WinTurtleGenColorValue(self.id,1,color,0)
    
    def color(self,color) -> bool :
        """
        Sets the color for subsequent drawing operations. 
        
        Example:
        
        t.forward(100)  # draw 100 pixels in current heading in current color
        t.color("red")  # Set color to "red"
        t.forward(100)  # draws 100 pixels in current heading in color "red"
        
        ** note: color() and set_color() are the same function
        """
        return _pybox.WinTurtleGenColorValue(self.id,1,color,0)
    
    def set_pos(self,x : int,y : int) -> bool :
        """
        Sets the position of the current pointer (or turtle).
        
        The if the pen is down, a line will be drawn from the current position to the new position. The heading will not change.
        
        - See set_pos_l() to use a list or array for (x,y) values.
        - note: move_to() and set_pos() are the same function.
        
        Use pen_up() to move to a position without drawing a line. 
        
        Input Parameters:
        
        - x         \t- x position of new location
        - y         \t- y position of new location
        """
        return _pybox.WinTurtleSetPos(self.id,x,y)
    
    def set_pos_l(self,pos : list) -> bool :
        """
        Sets the position of the current pointer (or turtle).
        
        The if the pen is down, a line will be drawn from the current position to the new position. The heading will not change.
        
        - See set_pos() to use individual values for position (i.e. x and y vs. a list)
        - note: move_to_l() and set_pos_l() are the same function.
        
        Use pen_up() to move to a position without drawing a line. 
        
        This function is the same as move_to().
        
        Input Parameters:
        
        - pos         \t- position of new location
        """
        return _pybox.WinTurtleSetPos(self.id,pos[0],pos[1])
    
    def move_to(self,x : int,y : int) -> bool :
        """
        Sets the position of the current pointer (or turtle).
        
        The if the pen is down, a line will be drawn from the current position to the new position. The heading will not change.
        
        - See move_to_l() to use a list or array for (x,y) values.
        - note: move_to() and set_pos() are the same function.
        
        Use pen_up() to move to a position without drawing a line. 
        
        Input Parameters:
        
        - x         \t- x position of new location
        - y         \t- y position of new location
        """
        return _pybox.WinTurtleSetPos(self.id,x,y)
    
    def move_to_l(self,pos : list) -> bool :
        """
        Sets the position of the current pointer (or turtle).
        
        The if the pen is down, a line will be drawn from the current position to the new position. The heading will not change.
        
        - See move_to() to use individual values for position (i.e. x and y vs. a list)
        - note: move_to_l() and set_pos_l() are the same function.
        
        Use pen_up() to move to a position without drawing a line. 
        
        This function is the same as move_to().
        
        Input Parameters:
        
        - pos         \t- position of new location
        """
        return _pybox.WinTurtleSetPos(self.id,pos[0],pos[1])
    
    def circle(self,radius,sweep_angle = 360,steps : int = 0) -> bool :
        """
        Draws a circle, arc, polygon or polygonal-arc, depending on input values.
        
        The heading is change from the current heading to the angle of the output of the circle or last polygonal line.
        
        If no Sweep Angle is entered, a full circle is drawn. Otherwise in arc is drawn.
        
        The "Steps" value, draws the circle as a polygon with sides equal to the "Steps" value, drawing lines from point to point, rather than a circle.

        Input Parameters:
        
        - radius        \t- Radius of Circle (or partial circle/arc)
        - sweep_angle   \t- Angle to cover in circle (blank is 360, or a full circle)
        - steps         \t- Number of segments to draw for circle or arc (no value or 0 draws a circle or arc without segment lines)        """
        return _pybox.WinTurtleCircle(self.id,radius,sweep_angle,steps)
    
    def get_heading(self) -> float :
        """
        Returns the current heading of the 'turtle'
        """
        return _pybox.WinTurtleGetFloat(self.id,0)
    
    def get_pos(self) -> list :
        """
        Returns the current position of the 'turtle' relative to the center of the window.
        """
        return _pybox.WinTurtleGetFloatList(self.id,0)
    

class _ImageBeforeAfter :
    "ImageBeforeAfter class.  This class allows you to control a window popped up with pybox.ImageBeforeAfter()"
    def __init__(self,_id) : self.id = _id
#    def __del__(self) : TBD
    def closed(self) -> bool :
        """
        Returns True if the Window has been closed by the user (or some othe process).  Returns False if the window is open or hidden.

        See closed_event() to get the event at the time the window is closed. 
        """
        return _pybox.ImgBeforeAfterWindowClosed(self.id)
    def close_window(self) -> bool :
        "Closes the Before & After window."
        return _pybox.ImgBeforeAfterCloseWindow(self.id)

    def close_event(self) -> bool :
        """
        Returns True once (i.e. as an event) if the ImageView Window has been closed, and false after the first call.  See closed() for non-event version.
       
        Also see closed() --> Once the window is closed, closed() will return True continuously, and not just once.

        This is used as an event so a message loop can react to it just once.  See Closed() for a non-event version.
        --> This function an EVENT function: This function will only return a True value ONE TIME PER EVENT 
        --> and will return False after the first call until the event occurs again. 

            In most events, you can specify "peek=true" as a parameter so that the event will not be reset.
        """
        return _pybox.ImgBeforeAfterWindowCloseEvent(self.id)

    def wait_for_close(self) -> bool : 
        """
        Waits for the window to close (by the user or some other process)

        See wait_close_all() and wait_close_any()
        """
        return _pybox.ImgBeforeAfterWaitforClose(self.id)
    def show_instructions(self) -> None :
        """
        Shows the Image_view() and img_before_after() instructions in a window on the screen. 
        The window has an OK button that will close when pressed.

        This is the same window that appears when "show instructions" is chosen from the
        system menu im the image_view() window.
        """
        return _pybox.ShowImgViewInstructions()
   

class _ImageView :
    "--comment--"
    def __init__(self,_id) : self.id = _id
#    def __del__(self) : TBD
    def closed(self) -> bool :
        """
        Returns True if the Window has been closed by the user (or some othe process).  Returns False if the window is open or hidden.

        See closed_event() to get the event at the time the window is closed. 
        """
        return _pybox.ImgViewWindowClosed(self.id)

    def window_count(self = None) -> int :
        "Returns the number of open ImageView windows on the desktop."
        return _pybox.ImgViewWindowWindowCount(0)

    def close_event(self) -> bool :
        """
        Returns True once (i.e. as an event) if the ImageView Window has been closed, and false after the first call.  See closed() for non-event version.
       
        Also see closed() --> Once the window is closed, closed() will return True continuously, and not just once.

        This is used as an event so a message loop can react to it just once.  See Closed() for a non-event version.
        --> This function an EVENT function: This function will only return a True value ONE TIME PER EVENT 
        --> and will return False after the first call until the event occurs again. 

            In most events, you can specify "peek=true" as a parameter so that the event will not be reset.
        """
        return _pybox.ImgViewWindowCloseEvent(self.id)

    def wait_close(self) -> bool : 
        """
        Waits for the window to close. Other open ImageView windows are not affected.

        See wait_close_all() and wait_close_any()
        """
        return _pybox.ImgViewWaitforClose(self.id)
        
    def wait_close_all(self = None) -> bool : 
        """
        Waits for the user to close all visible ImageView type windows. 

        If there are no visible ImageView Windows, WaitforCloseAll() returns immediately.
        """
        return _pybox.ImgViewWaitforCloseAll(self.id)

    def wait_close_any(self = None) -> bool : 
        """
        Waits for the user to close any open ImageView Window and returns.
        This is useful when assuming any closure represents closing all windows.

        If there are no open or visible windows WaiforCloseAny() returns immediately.
        """
        return _pybox.ImgViewWaitforCloseAny(self.id)

    def close_all(self = None) -> bool :
         """
         Closes and deletes all open ImageView Windows.
         """
         return _pybox.ImgViewCloseAll(0)
    def show_instructions(self) -> None :
        """
        Shows the Image_view() and image_before_after() instructions in a window on the screen. 
        The window has an OK button that will close when pressed.

        This is the same window that appears when "show instructions" is chosen from the
        system menu im the image_view() window.
        """
        return _pybox.ShowImgViewInstructions()
    def close_window(self) -> bool :
        "Closes the image view window."
        return _pybox.ImgViewCloseWindow(self.id)


class dialog :
    """
    pybox dialog class.

    The pybox dialog class is a collection of windows-based dialog functions. 

    These functions are available through the regular pybox interface, but are collected in the dialog class for
    better visibility. 

    When you enter "pybox.dialog", a list of funtions will appear.  You can use these functions int the dialog class, or
    remove the ".dialog" and use them directly through the pybox class. 
    
    """
    def img_view(bitmap,title=None,at=None,size=None,percent=None,zoombox=None,*args,**kwargs) -> _ImageView :
        """
        Creates an ImageView window where you can zoom and and out of the displayed image and move it around for inspection. 
        The window can be resized and maximized.  See img_view_r() to display the image upside-down.

        - This function returns an _ImageView class object where you can control the ImageView window that is created.  However, it is not
        necessary to keep the return object or assign it to a variable. 
        - The system menu (upper-left corner) has a number of options to bring up a Zoom Box, reset the image, etc.
        - Use ImgZoom() to bring up a Zoom Box that can be used to navigate through the image. 

        About the Zoom Box

        The Zoom box as a small window that works with all ImgView images.  Multiple images can be displayed, and the Zoom Box will update to the currently selected image.

        Also see: img_zoom() -- brings up an ImageView Window with a zoom box (otherwise it can be selected from the upper-left system menu)
        Also see: img_before_after() -- brings up a window with two images, such as before and after images, for comparison.

        Parameters:

        - bitmap        \t - The bitmap to display.  This can be a pybox bitmap, a general RGB array, or a text string with the path to the bitmap
        - title         \t - This is the title of the image that will display in the title bar
        - at            \t - Where to put the window.  If this is not used, the window is placed automatically.
        - size          \t - Size of the window box.  The Image will be adjust accordingly based on the size given.  The default is for ImgView() to choose automatically.
        - percent       \t - Desired size of the image in percent to show on initial launch.  This can be useful for specifying thumbnail images with a smaller size.

        Keywords and Pybox options can be included.  Some various options are as follows:

        - reverse       \t -- Displays the bitmap upside-down.  Bitmaps often come updside-down. "reverse" corrects this.  Also see: img_view_r()
        - normalize     \t -- Use this when the bitmap ranges from 0.0-1.0.  Normalize=True will convert the image to a displayable bitmap i.e. 0-255 on each channel)
        - label         \t -- This will put a text label underneath the image in a larger font for better labeling display.
                            \t -If no Label is given with no Title, the title bar text will also be the label text.
                          
        About Bitmaps: Bitmaps can be a pybox bitmap or a general RGB array bitmap (i.e. numpy array) in the form [height][width][3], where the [3] is Blue, Green, and Red,
        or an RGB32 bitmap array of [height][width][4] where the 4 values are Red, Green, Blue, and Mask, in that order.
    
        The bitmap format can be unsigned char, float, double, mono, mono float, and half-float. 
        """        
        return _ImageView(_pybox.ImgView(bitmap,opt.title(title),opt.at(at),opt.size(size),opt.percent(percent),opt.zoombox(zoombox),*args,**kwargs))

    def img_view_r(bitmap,title=None,at=None,size=None,percent=None,zoombox=None,*args,**kwargs) -> _ImageView :
        """
        Creates an ImageView window where you can zoom and and out of the displayed image and move it around for inspection. 
        The window can be resized and maximized.  This image is displayed upside-down in relation to the bitmap.
        See img_view() to display the image non-upside-down. 

        - This function returns an _ImageView class object where you can control the ImageView window that is created.  However, it is not
        necessary to keep the return object or assign it to a variable. 
        - The system menu (upper-left corner) has a number of options to bring up a Zoom Box, reset the image, etc.
        - Use img_zoom() to bring up a Zoom Box that can be used to navigate through the image. 

        About the Zoom Box

        The Zoom box as a small window that works with all ImgView images.  Multiple images can be displayed, and the Zoom Box will update to the currently selected image.

        Also see: img_zoom() -- brings up an ImageView Window with a zoom box (otherwise it can be selected from the upper-left system menu)
        Also see: img_before_after() -- brings up a window with two images, such as before and after images, for comparison.

        Parameters:

        - bitmap        \t - The bitmap to display.  This can be a pybox bitmap, a general RGB array, or a text string with the path to the bitmap
        - title         \t - This is the title of the image that will display in the title bar
        - at            \t - Where to put the window.  If this is not used, the window is placed automatically.
        - size          \t - Size of the window box.  The Image will be adjust accordingly based on the size given.  The default is for ImgView() to choose automatically.
        - percent       \t - Desired size of the image in percent to show on initial launch.  This can be useful for specifying thumbnail images with a smaller size.

        Keywords and Pybox options can be included.  Some various options are as follows:

        - normalize     \t -- Use this when the bitmap ranges from 0.0-1.0.  normalize=True will convert the image to a displayable bitmap i.e. 0-255 on each channel)
        - label         \t -- This will put a text label underneath the image in a larger font for better labeling display.
                            \t -If no Label is given with no Title, the title bar text will also be the label text.
                          
        About Bitmaps: Bitmaps can be a pybox bitmap or a general RGB array bitmap (i.e. numpy array) in the form [height][width][3], where the [3] is Blue, Green, and Red,
        or an RGB32 bitmap array of [height][width][4] where the 4 values are Red, Green, Blue, and Mask, in that order.
    
        The bitmap format can be unsigned char, float, double, mono, mono float, and half-float. 
        """
        return _ImageView(_pybox.ImgViewR(bitmap,opt.title(title),opt.at(at),opt.size(size),opt.percent(percent),opt.zoombox(zoombox),*args,**kwargs))

    def img_zoom(bitmap,title=None,at=None,size=None,percent=None,*args,**kwargs) -> _ImageView :
        """
        Creates an ImageView and Zoom Box window where you can zoom and and out of the displayed image and move it around for inspection. 
        The window can be resized and maximized.  See img_zoom_r() to display the image upside-down.

        - This function is the same as ImgView() except that it creates a ZoomBox as a small window to make navigating the image easier. 
        - This function returns an _ImageView class object where you can control the ImageView window that is created.  However, it is not
        necessary to keep the return object or assign it to a variable. 
        - The system menu (upper-left corner) has a number of options to bring up a Zoom Box, reset the image, etc.
        - Use ImgZoom() to bring up a Zoom Box that can be used to navigate through the image. 

        About the Zoom Box

        The Zoom box as a small window that works with all ImgView images.  Multiple images can be displayed, and the Zoom Box will update to the currently selected image.

        Also see: img_zoom() -- brings up an ImageView Window with a zoom box (otherwise it can be selected from the upper-left system menu)
        Also see: img_before_after() -- brings up a window with two images, such as before and after images, for comparison.

        Parameters:

        - bitmap        \t - The bitmap to display.  This can be a pybox bitmap, a general RGB array, or a text string with the path to the bitmap
        - title         \t - This is the title of the image that will display in the title bar
        - at            \t - Where to put the window.  If this is not used, the window is placed automatically.
        - size          \t - Size of the window box.  The Image will be adjust accordingly based on the size given.  The default is for ImgView() to choose automatically.
        - percent       \t - Desired size of the image in percent to show on initial launch.  This can be useful for specifying thumbnail images with a smaller size.

        Keywords and Pybox options can be included.  Some various options are as follows:

        - reverse       \t -- Displays the bitmap upside-down.  Bitmaps often come updside-down. "reverse" corrects this.  Also see: ImgZoomR()
        - normalize     \t -- Use this when the bitmap ranges from 0.0-1.0.  normalize=True will convert the image to a displayable bitmap i.e. 0-255 on each channel)
        - label         \t -- This will put a text label underneath the image in a larger font for better labeling display.
                            \t -If no Label is given with no Title, the title bar text will also be the label text.
                          
        About Bitmaps: Bitmaps can be a pybox bitmap or a general RGB array bitmap (i.e. numpy array) in the form [height][width][3], where the [3] is Blue, Green, and Red,
        or an RGB32 bitmap array of [height][width][4] where the 4 values are Red, Green, Blue, and Mask, in that order.
    
        The bitmap format can be unsigned char, float, double, mono, mono float, and half-float. 
        """                
        return _ImageView(_pybox.ImgView(bitmap,opt.title(title),opt.at(at),opt.size(size),opt.percent(percent),opt.zoombox(True),*args,**kwargs))

    def img_zoom_r(bitmap,title=None,at=None,size=None,percent=None,*args,**kwargs) -> _ImageView :
        """
        Creates an ImageView and Zoom Box window where you can zoom and and out of the displayed image and move it around for inspection. 
        The window can be resized and maximized. This displays the bitmap upside-down. See img_zoom() to display the image non-upside-down.

        - This function is the same as img_view() except that it creates a ZoomBox as a small window to make navigating the image easier. 
        - This function returns an _ImageView class object where you can control the ImageView window that is created.  However, it is not
        necessary to keep the return object or assign it to a variable. 
        - The system menu (upper-left corner) has a number of options to bring up a Zoom Box, reset the image, etc.
        - Use img_zoom() to bring up a Zoom Box that can be used to navigate through the image. 

        About the Zoom Box

        The Zoom box as a small window that works with all ImgView images.  Multiple images can be displayed, and the Zoom Box will update to the currently selected image.

        Also see: img_zoom() -- brings up an ImageView Window with a zoom box (otherwise it can be selected from the upper-left system menu)
        Also see: img_before_after() -- brings up a window with two images, such as before and after images, for comparison.

        Keywords and Pybox options can be included.  Some various options are as follows:

        - bitmap        \t - The bitmap to display.  This can be a pybox bitmap, a general RGB array, or a text string with the path to the bitmap
        - title         \t - [optional] This is the title of the image that will display in the title bar
        - at            \t - [optional] Where to put the window.  If this is not used, the window is placed automatically.
        - size          \t - [optional] Size of the window box.  The Image will be adjust accordingly based on the size given.  The default is for ImgView() to choose automatically.
        - percent       \t - [optional] Desired size of the image in percent to show on initial launch.  This can be useful for specifying thumbnail images with a smaller size.

        Keywords and Pybox options can be included.  Some various options are as follows:

        - normalize     \t -- Use this when the bitmap ranges from 0.0-1.0.  normalize=True will convert the image to a displayable bitmap i.e. 0-255 on each channel)
        - label         \t -- This will put a text label underneath the image in a larger font for better labeling display.
                            \t -If no Label is given with no Title, the title bar text will also be the label text.
                          
        About Bitmaps: Bitmaps can be a pybox bitmap or a general RGB array bitmap (i.e. numpy array) in the form [height][width][3], where the [3] is Blue, Green, and Red,
        or an RGB32 bitmap array of [height][width][4] where the 4 values are Red, Green, Blue, and Mask, in that order.
    
        The bitmap format can be unsigned char, float, double, mono, mono float, and half-float. 
        """                        
        return _ImageView(_pybox.ImgViewR(bitmap,opt.title(title),opt.at(at),opt.size(size),opt.percent(percent),opt.zoombox(True),*args,**kwargs))

    def img_before_after(bitmap1,bitmap2,title=None,label=None,before_title=None,after_title=None,at=None,size=None,percent=None,*args,**kwargs) -> _ImageBeforeAfter :
        """
        Creates an ImageView window with a Before and After image, and Zoom Box window where you can zoom and and out of the displayed images and easily move them
        around for inspection.  The window can be resized and maximized.  See img_before_after_r() to display the images upside-down.

        - The system menu (upper-left corner) has a number of options.
        - This returns an _ImageBeforeAfter class object that can be used to control the window. However, it is not necessary to save the return object. 
            \t -with the return object, you can determine when the window is closed and can also close all open ImageView Windows, as well as many other functions.

        About the Zoom Box

        The Zoom box as a small window that works with all ImgView images.  Multiple images can be displayed, and the Zoom Box will update to the currently selected image.

        Parameters:

        - bitmap1       \t - The 'before' bitmap to display.  This can be a pybox bitmap or a general RGB array.
        - bitmap2       \t - The 'after' bitmap to display.  The bitmaps must be the same size, but can be different formats.
        - title         \t - This is the title of the image that will display in the title bar
        - before_title   \t - title/label for the 'before' bitmap.  If not specified, a default label is used
        - after_title    \t - title/label for the 'after' bitmap.  If not specified, a default label is used
        - at            \t - Where to put the window.  If this is not used, the window is placed automatically.
        - size          \t - Size of the window box.  The Image will be adjust accordingly based on the size given.  The default is for ImgView() to choose automatically.
        - percent       \t - Desired size of the image in percent to show on initial launch.  This can be useful for specifying thumbnail images with a smaller size.

        Keywords and Pybox options can be included.  Some various options are as follows:

        - normalize     \t -- Use this when the bitmap ranges from 0.0-1.0.  normalize=True will convert the image to a displayable bitmap i.e. 0-255 on each channel)
        - label         \t -- This will put a text label above both images.
                            \t -If no Label is given with no Title, the title bar text will also be the label text.
                                                
        About Bitmaps: Bitmaps can be a pybox bitmap or a general RGB array bitmap (i.e. numpy array) in the form [height][width][3], where the [3] is Blue, Green, and Red,
        or an RGB32 bitmap array of [height][width][4] where the 4 values are Red, Green, Blue, and Mask, in that order.
    
        The bitmap format can be unsigned char, float, double, mono, mono float, and half-float. 
        """                        
        return _ImageBeforeAfter(_pybox.ImgBeforeAfter(bitmap1,bitmap2,opt.title(title),opt.str_str("BeforeTitle",before_title),opt.str_str("AfterTitle",after_title),opt.label(label),
                                                       opt.at(at),opt.size(size),opt.percent(percent),*args,**kwargs))

    def img_before_after_r(bitmap1,bitmap2,title=None,label=None,before_title=None,after_title=None,at=None,size=None,percent=None,*args,**kwargs) -> _ImageBeforeAfter :
        """
        Creates an ImageView window with a Before and After image, and Zoom Box window where you can zoom and and out of the displayed images and easily move them
        around for inspection.  The window can be resized and maximized.  The images are displayed upside-down. See img_before_after() to display the images non-upside-down.

        - The system menu (upper-left corner) has a number of options.
        - This returns an _ImageBeforeAfter class object that can be used to control the window. However, it is not necessary to save the return object. 
            \t -with the return object, you can determine when the window is closed and can also close all open ImageView Windows, as well as many other functions.

        About the Zoom Box

        The Zoom box as a small window that works with all ImgView images.  Multiple images can be displayed, and the Zoom Box will update to the currently selected image.

        Parameters:

        - bitmap1       \t - The 'before' bitmap to display.  This can be a pybox bitmap or a general RGB array.
        - bitmap2       \t - The 'after' bitmap to display.  The bitmaps must be the same size, but can be different formats.
        - title         \t - This is the title of the image that will display in the title bar
        - before_title   \t - title/label for the 'before' bitmap.  If not specified, a default label is used
        - after_title    \t - title/label for the 'after' bitmap.  If not specified, a default label is used
        - at            \t - Where to put the window.  If this is not used, the window is placed automatically.
        - size          \t - Size of the window box.  The Image will be adjust accordingly based on the size given.  The default is for ImgView() to choose automatically.
        - percent       \t - Desired size of the image in percent to show on initial launch.  This can be useful for specifying thumbnail images with a smaller size.

        Keywords and Pybox options can be included.  Some various options are as follows:

        - normalize     \t -- Use this when the bitmap ranges from 0.0-1.0.  normalize=True will convert the image to a displayable bitmap i.e. 0-255 on each channel)
        - label         \t -- This will put a text label above both images.
                            \t -If no Label is given with no Title, the title bar text will also be the label text.
                          
        About Bitmaps: Bitmaps can be a pybox bitmap or a general RGB array bitmap (i.e. numpy array) in the form [height][width][3], where the [3] is Blue, Green, and Red,
        or an RGB32 bitmap array of [height][width][4] where the 4 values are Red, Green, Blue, and Mask, in that order.
    
        The bitmap format can be unsigned char, float, double, mono, mono float, and half-float. 
        """                                
        return _ImageBeforeAfter(_pybox.ImgBeforeAfterR(bitmap1,bitmap2,opt.title(title),opt.str_str("BeforeTitle",before_title),opt.str_str("AfterTitle",after_title),opt.label(label),
                                                        opt.at(at),opt.size(size),opt.percent(percent),*args,**kwargs))


    def info(text : str,*args,**kwargs) -> bool :
        """
        Displays a window with the given text and an "OK" button. Note: InfoWindow() and QuickButton() are the same function.

        This is used to present general information in a window box. 

        Parameters: 

        - text          \t -- text to put into the window. 

        About Dialog Box Text

        The text for the dialog box can contain multiple lines.  The first line will be displayed in a larger font, with subsequent lines displayed in a smaller font. 
        If the first line in the text starts with a '+' the text line becomes the text in the title bar window and is not placed in the dialog box itself. 

        Examples:

                \t -pybox.dialog.info("Press OK to continue")
                \t -pybox.dialog.info("+Information Window\nPress OK to continue")
                \t -pybox.dialog.info("Finished Processing\nPress OK to continue")
                \t -pybox.dialog.info("+My Process\nFinished Processing\nPress OK to continue")
        """
        return _pybox.InfoWindow(text,str,*args,**kwargs)

    def msgbox(text : str,*args,**kwargs) -> bool :
        """
        Displays a window with the given text and an "OK" button. Note: InfoWindow() and QuickButton() are the same function.

        This is used to present general information in a window box. 

        Parameters: 

        - text          \t -- text to put into the window. 

        About Dialog Box Text

        The text for the dialog box can contain multiple lines.  The first line will be displayed in a larger font, with subsequent lines displayed in a smaller font. 
        If the first line in the text starts with a '+' the text line becomes the text in the title bar window and is not placed in the dialog box itself. 

        Examples:

                \t -pybox.dialog.msgbox("Press OK to continue")
                \t -pybox.dialog.msgbox("+Information Window\nPress OK to continue")
                \t -pybox.dialog.msgbox("Finished Processing\nPress OK to continue")
                \t -pybox.dialog.msgbox("+My Process\nFinished Processing\nPress OK to continue")
        """
        return _pybox.InfoWindow(text,str,*args,**kwargs)

    def msgbox_yesno(text : str,*args,**kwargs) -> bool :
        """
        Displays a window with the given text and an "yes" button and a "no" button.

        Parameters: 

        - text          \t -- text to put into the window. 

        Returns: True if "Yes" was input, or False if the No was pressed. 

        About Dialog Box Text

        The text for the dialog box can contain multiple lines.  The first line will be displayed in a larger font, with subsequent lines displayed in a smaller font. 
        If the first line in the text starts with a '+' the text line becomes the text in the title bar window and is not placed in the dialog box itself. 

        Examples:

                \t -pybox.dialog.msgbox_yesno("Would you like to continue?")
                \t -pybox.dialog.msgbox_yesno("+Yes No Window\nWould you like to continue?")
                \t -pybox.dialog.msgbox_yesno("Finished Processing\nWould you like to continue?")
                \t -pybox.dialog.msgbox_yesno("+My Process\nWould you like to Continue?\nPress Yes to continue, No to quit.")

        """
        return _pybox.YesNoWindow(text,str,*args,**kwargs)

    def msgbox_yesnocancel(text : str,*args,**kwargs) -> bool :
        """
        Displays a window with the given text and an "yes" button, "no" button, and "Cancel" button

        Parameters: 

        - text          \t -- text to put into the window. 

        Returns: True if "Yes" was input, or False if the No was pressed. 
                 Use "pybox.dialog.WasCancelled() or pybox.WasCancelled() to determine if the Cancel button was pressed.

        About Dialog Box Text

        The text for the dialog box can contain multiple lines.  The first line will be displayed in a larger font, with subsequent lines displayed in a smaller font. 
        If the first line in the text starts with a '+' the text line becomes the text in the title bar window and is not placed in the dialog box itself. 

        Examples:

                \t -pybox.dialog.msgbox_yesnocancel("Would you like to continue?")
                \t -pybox.dialog.msgbox_yesnocancel("+Yes No Window\nWould you like to continue?")
                \t -pybox.dialog.msgbox_yesnocancel("Finished Processing\nWould you like to continue?")
                \t -pybox.dialog.msgbox_yesnocancel("+My Process\nWould you like to Continue?\nPress Yes to continue, No to quit,Cancel to Exit.")

        """        
        return _pybox.YesNoCancelWindow(text,str,*args,**kwargs)

    def msgbox_okcancel(text : str,*args,**kwargs) -> bool :
        """
        Displays a window with the given text and an "Ok" button, and "Cancel" button

        Parameters: 

        - text          \t -- text to put into the window. 

        Returns: True if "Ok" was input, or False if the Cancel was pressed. 
                 Use "pybox.dialog.WasCancelled() or pybox.WasCancelled() to determine if the Cancel button was pressed.

        About Dialog Box Text

        The text for the dialog box can contain multiple lines.  The first line will be displayed in a larger font, with subsequent lines displayed in a smaller font. 
        If the first line in the text starts with a '+' the text line becomes the text in the title bar window and is not placed in the dialog box itself. 

        Examples:

                \t -pybox.dialog.msgbox_okcancel("Would you like to continue?")
                \t -pybox.dialog.msgbox_okcancel("+Yes No Window\nWould you like to continue?")
                \t -pybox.dialog.msgbox_okcancel("Finished Processing\nWould you like to continue?")
                \t -pybox.dialog.msgbox_okcancel("+My Process\nWould you like to Continue?\nPress Yes to continue or Cancel to quit.")

        """                
        return _pybox.OkCancelWindow(text,str,*args,**kwargs)

    def quick_button(text : str,title : str = "Quick Button",*args) -> bool :
        """
        Displays a window with the given text and an "OK" button. Note: InfoWindow() and QuickButton() are the same function.

        This is used to present general information in a window box. 

        Parameters: 

        - text          \t -- text to put into the window. 

        About Dialog Box Text

        The text for the dialog box can contain multiple lines.  The first line will be displayed in a larger font, with subsequent lines displayed in a smaller font. 
        If the first line in the text starts with a '+' the text line becomes the text in the title bar window and is not placed in the dialog box itself. 

        Examples:

                \t -pybox.dialog.quick_button("Press OK to continue")
                \t -pybox.dialog.quick_button("+Information Window\nPress OK to continue")
                \t -pybox.dialog.quick_button("Finished Processing\nPress OK to continue")
                \t -pybox.dialog.quick_button("+My Process\nFinished Processing\nPress OK to continue")
        """        
        return _pybox.InfoWindow(text,title,*args)

    def please_wait(text = None,cancelok : bool = False,*args,**kwargs) -> bool :
        """
        Displays a please wait window in the center of the screen.
        
        Parameters:

        - text          \t - - [optional] text to display in the Please Wait Window. If multiple lines are used, the first line displays in a larger font.
        - cancelok      \t - - [optional] if specified, a "cancel" button.  This can be checked with PleaseWaitCanceled() in the event loop.

        Pybox options can be included.  Some various options are as follows:

        - ProgressBar         \t -- Adds a progress bar to the please wait window.  This can be set from 0-100% with PleaseWaitSetProgress()

        Examples:

                \t -pybox.dialog.please_wait()
                \t -pybox.dialog.please_wait("Wait for process to finish")
                \t -pybox.dialog.please_wait("Wait for process to finish\\nPress cancel to abort",True,opt.progresbar())
        """
        return _pybox.PleaseWaitWindow(text,opt.cancelok(cancelok),*args,**kwargs)

    def close_please_wait() -> bool :
        """
        Closes the Please Wait window if it is open.
        """
        return _pybox.ClosePleaseWait()

    def please_wait_set_progress(percent : int) -> bool :
        """
        If a Please Wait Window is open and has a progress bar, please_wait_set_progress() will set the percent complete of the progress bar.
        
        Parameters:

        - percent          \t - - Percent (0-100) complete.

        """
        return _pybox.PleaseWaitSetProgress(percent)

    def please_wait_canceled() -> bool :
        """
        Returns True if the "Cancel" button was pressed in a Please Wait Window, False if not or after the first True return (because it is an event)
        
        note: Even when the Cancel button is pressed, the program must still close the Please Wait window with close_please_wait().

        --> This function an EVENT function: This function will only return a True value ONE TIME PER EVENT 
        --> and will return False after the first call until the event occurs again. 

            In most events, you can specify "peek=true" as a parameter so that the event will not be reset.
        """
        return _pybox.PleaseWaitCanceled()

    def was_canceled() -> bool :
        """
        Returns true of the last dialog box that contains a 'cancel' button was canceled. 

        This can be useful in handling dialog boxes that return numbers and strings.  was_canceled() can confirm the user canceled the dialog box and is not
        returning information.

        If was_canceled() returns False, then it can be assumed that the return data is ok.

        was_canceled() applies to dialog functions like GetInteger(), GetFloat(), GetString(), YesNocancel(), and other functions.
        """
        return _pybox.Canceled()

    def get_integer(text=None,*args,**kwargs) -> int  :
        """
        Gets an integer value from a window that pops up with an input box.  The return value is the integer entered or default value.
        Call pybox.was_canceled() to determine if the user canceled the input box (opt.nocancel() will disallow the ability to cancel)

        Options:

        text        \t - [optional] The text to put as a header in the box.  You can use multiple lines.
                    \t - if the first line starts with '+' that line becomes the title in the title bar and subsquent lines are printed in the description.

        Keywords and Pybox options can be included.  Some various options are as follows:

        - Range         \t -Set a range for the input.  This will not allow an input outside of the range, but can allow the user to press return
        - Default       \t -Sets the default value.  This is placed in the input box when the box first comes up.  If the user presses return on a blank line, the default is returned.
        - NoCancel      \t -By defaut, there is a cancel button to allow the user to cancel.  You can call pybox.was_canceled() which returns True if the last input box was canceled.
                        \t -When NoCancel is specified, the user cannot cancel or press return on an empty line and must enter a value (a control-C may be pressed to stop the program.

        Examples:       \t -My Value = pybox.get_integer("Enter a number")
                        \t -My Value = pybox.get_integer("+This is the title bar title\\nEnter a number",range=(1,100),nocancel=True)
                        \t -My Value = pybox.get_integer("Enter a number\nNumber should be between 1 and 100,range=(1,100),default=10)
        """    
        return _pybox.GetInteger(text,*args,**kwargs)

    def get_float(text=None,*args,**kwargs) -> float  :
        """
        Gets an floating-point value from a window that pops up with an input box.  The return value is the integer entered or default value.
        Call pybox.was_canceled() to determine if the user canceled the input box (opt.nocancel() will disallow the ability to cancel)

        Parameters:

        - text          \t - [optional] The text to put as a header in the box.  You can use multiple lines.
                        \t - if the first line starts with '+' that line becomes the title in the title bar and subsquent lines are printed in the description.

        Keywords and Pybox options can be included.  Some various options are as follows:

        - Range         \t -Set a range for the input.  This will not allow an input outside of the range, but can allow the user to press return
        - Default       \t -Sets the default value.  This is placed in the input box when the box first comes up.  If the user presses return on a blank line, the default is returned.
        - NoCancel      \t -By defaut, there is a cancel button to allow the user to cancel.  You can call pybox.was_canceled() which returns True if the last input box was canceled.
                        \t -When NoCancel is specified, the user cannot cancel or press return on an empty line and must enter a value (a control-C may be pressed to stop the program.

        Examples:       \t -My Value = pybox.get_float("Enter a number")
                        \t -My Value = pybox.get_float("+This is the title bar title\\nEnter a number",range=(1,100),nocancel=True)
                        \t -My Value = pybox.get_float("Enter a number\nNumber should be between 1 and 100,range=(1,100),default=10)
        """        
        return _pybox.GetFloat(text,*args,**kwargs)

    def get_string(text=None,*args,**kwargs) -> str  :
        """
        Creates a window with an OK button to get a string from the user, displaying the text message above the input box. 

        This function returns a string of the user-inputted text, or a blank string if nothing was entered or the input was canceled.

        Use pybox.was_canceled() to determine of the input box was canceled by the user. 

        Parameters:

        - text          \t - [optional] The text to put as a header in the box.  You can use multiple lines.
                        \t - if the first line starts with '+' that line becomes the title in the title bar and subsquent lines are printed in the description.

        Keywords and Pybox options can be included.  Some various options are as follows:

        - Default       \t -Sets the default text.  This is placed in the input box when the box first comes up.  If the user presses return on a blank line, the default is returned.
        - NoCancel      \t -By defaut, there is a cancel button to allow the user to cancel.  You can call pybox.was_canceled() which returns True if the last input box was canceled.
                        \t -When NoCancel is specified, the user cannot cancel or press return on an empty line and must enter some text (a control-C may be pressed to stop the program.
        """
        return _pybox.GetString(text,*args,**kwargs)

    def get_open_file(filetypes : str = None) -> str     : 
        """
        Brings up the standard OS file selection menu where the user can select a file. 
        See get_save_file() for a 'save' file name so that the system prompts for "overwrite" permission on existing names.

        This function returns a string with the name of the file selected, or an empty string if the input was canceled.
        Use pybox.was_canceled() to determine if the input was canceled (or check for an emptystring)

        Parameters:

        - filetypes     \t -- [optional] filetypes to limit display to, such as "*.bmp", "*.bmp;*.jpg", etc.  Default is no filter and will display all files

        Examples: 
                \t -pybox.get_open_file()
                \t -pybox.get_open_file("*.bmp")
                \t -pybox.get_open_file("*.bmp;*.png;*.jpg")

        """
        return _pybox.GetOpenFile(filetypes)

    def get_save_file(filetypes : str = None) -> str     : 
        """
        Brings up the standard OS file selection menu where the user can select a file to save.
        The system will prompt for "overwrite" permission for existing names, but will not alter the file.  
        The function only returns the name selected, or an empty string.

        This function returns a string with the name of the file selected, or an empty string if the input was canceled.
        Use pybox.was_canceled() to determine if the input was canceled (or check for an emptystring)

        Parameters:

        - filetypes     \t -- [optional] filetypes to limit display to, such as "*.bmp", "*.bmp;*.jpg", etc.  Default is no filter and will display all files

        Examples: 
                \t -pybox.get_save_file()
                \t -pybox.get_save_file("*.bmp")
                \t -pybox.get_save_file("*.bmp;*.png;*.jpg")

        """
        return _pybox.GetSaveFile(filetypes)
                       
class CQuickForm :
    """
    Pybox Quick Form Class

    This class provices the windows for the Quick Form Window. 

    A Quick form Window is a set of 3 windows to allow controls and a canvas-style window to function together in an organized, unifed window. 

    The Windows provided are as follows: 

    - main      \t -- The main window is the top-level window that hold the two (or more) innerwindows, label window, etc. 
                    \t - The main window can be used to check for window closure (of the main window), or to move and set the size of the overall window, as
                    \t - as well as other functions.

    - win       \t -- This is the main 'blank' or 'canvas' window that acts as a normal window.  Items can be drawn in this window, and other window can be embedded within
                    \t - this window (i.e. ChildWindow()).  Any regular window function is available in this window -- it's simply a regular window embedded into the Main window

    - dev       \t -- This is a Dev Controls Window that is embedded in the main window, typically to the left of the 'Win' window.   With this window, you can easily add controls
                    \t - such as buttons, sliders, small window, list boxes, text widgets, etc. -- all with one line of code. 

    See: pybox.QuickForm() to start a Quick Form Window.  Also see pybox.NewWindow() to create a standalone window, as well as the pybox Dev functions to create standalone controls
    pybox.DevButton("Press Me!")

    """
    def __init__(self,MainID,WinID,DevID) :
        self.main = Window(MainID)
        self.win = Window(WinID)
        self.dev = DevControl(DevID)

#
# Top-Level Pybox Functions
#

def was_canceled() -> bool :
    """
    Returns true of the last dialog box that contains a 'cancel' button was canceled. 

    This can be useful in handling dialog boxes that return numbers and strings.  was_canceled() can confirm the user canceled the dialog box and is not
    returning information.

    If was_canceled() returns False, then it can be assumed that the return data is ok.

    was_canceled() applies to dialog functions like GetInteger(), GetFloat(), GetString(), YesNocancel(), and other functions.
    """    
    return _pybox.Canceled()

def get_hue_color(deg : int) -> RgbColor :
    """
    Returns a bright, primary color based on the input value. 

    GetHueColor() is a quick way to grab a bright color as specific value or in a random manner. 

    For example, get_hue_color(0) returns a bright red, where get_hue_color(60) returns a bright magenta, and get_hue_color(120) returns a bright Blue, and so-forth.

    Parameters

    - deg      \t -- Input degrees, from 0-360. 

    Notable Values:

    - 0     \t --Red.  Same as GetHueColor(360)
    - 60    \t --Purple / Magenta
    - 120   \t --Blue
    - 180   \t --Cyan
    - 240   \t --Green
    - 300   \t --Yellow

    Returns: A pybox RgbColor object consisting of a Red, Green, and Blue value
    """
    color = _pybox.FromHSL(deg)
    return RgbColor(color[0],color[1],color[2])

#def set_debug(mode : int = 3) -> bool :
#    """
#    Sets the debug mode for pybox and all pybox widgets.
#
#    When ON, debug messages will appear in the console window showing the module, function and informational or debug message.
#    
#    Debug Modes:
#    
#    - 0     \t -- Debug Off (default)
#    - 1     \t -- Info -> Prints informational items to know about, but not errors per-se.
#    - 2     \t -- Error -> In addition to informational messages, this will also show internal error messages if a call fails and aborts the program.
#    - 3     \t -- Debug -> (experimental) Shows all Info & Error messages, as well as internal development debug messages. 
#
#    Any debug level will also show Fatal errors (errors such as parameter errors that cause program termination).
#
#    Examples:
#
#    pybox.set_debug(2)  --> Show all Info and Error messages
#    pybox.set_debug(0)  --> Set debug OFF (default)
#    """
#    _pybox.SetDebug(mode)

def set_debug(mode : str) -> bool :
    """
    Sets the debug mode for pybox and all pybox widgets.

    When ON, debug messages will appear in the console window showing the module, function and informational or debug message.
    
    Debug Modes:
    
    - "off"         \t - Debug Off (default)
    - "Info"        \t - Info -> Prints informational items to know about, but not errors per-se.
    - "Verbose"     \t - Info -> Prints informational items to know about, with more details.
    - "Warnings"    \t - Warnings -> In addition to informational messages, this will also show warning messages if a call fails and aborts the program.
    - "Error"       \t - Error -> In addition to informational messages, this will also show internal error messages if a call fails and aborts the program.
    - "_debug"      \t - Debug (note the "_" in "_debug) -> (experimental) Shows all Info & Error messages, as well as internal development debug messages. 

    Any debug level will also show Fatal errors (errors such as parameter errors that cause program termination).

    Examples:

    pybox.set_debug("Info")  --> Show all Info and Error messages
    pybox.set_debug("off")  --> Set debug OFF (default)
    pybox.set_debug("_debug")  --> Set debug to "_debug", which prints everything, including internal debug information.
    """
    _pybox.SetDebugStr(mode)

def dev_set_config(*args,**kwargs) -> bool :
    """
    Sets various configuration values for the Dev Window. 

    Most values can be set through various Dev Window function.  dev_set_config() is a way to set multiple options at 
    once, as well as setting values that don't have a specific functions.

    set_config() works with the following keywords:

    - bgcolor         \t -Sets the background color of the dev window.  This can be a single color or a string with one or two colors (for a gradient)
                      \t -note: this should be used before any controls are placed in the dev window. Also see dev_set_bgcolor() for more options

    - bgbitmap        \t -Sets the bitmap of the dev window background.  This can be a pybox Cbitmap type, and bitmap array (i.e. opencv, etc.),
                      \t -or a text string with the location of the bitmap.
                      \t -note: this should be used before any controls are placed in the dev window. Also see dev_set_bgbitmap() for more options.

    - ypos            \t -Sets the position of the next control.  This can be used to set the location of the first control when setting bgbitmap when the bitmap contains a top header.

    - autoclose_x     \t -Sets the auto close 'x' button on or off.  By default, an 'x' is placed on the window to allow the user to close it.
                      \autoclose_x=false will turn this 'x' off and also prevent the 'x' from appearing when the Dev Window is the only window open during get_event() calls.
                      \t -see the 'allowclose' option to set the 'x' visibility in other ways
  
    - autoclose       \t -When set to true, this will cause the Dev Window to close automatically when no other non-dev (or other primary) windows are open.
                        \t - otherwise, when set to false (default) the Dev Window will remain open when other windows are closed (with an 'x' placed for closure).

    - closeable       \t -Sets the 'x' button on or off when multiple windows are open.  By default, the 'x' appears in all Dev Windows to allow the user
                      \t -to close it, at which time the window will automatically close. closeable=True will force the 'x' on the window.

                      \t -setting closeable=false will remove the 'x' when there are non-Dev windows open. the 'x' will appear when no other windows are open
                      \t -to allow the user to close the window. See 'autoclose_x' option to disable the 'x' permanently.

    - topbar          \t -Turns the topbar off (when false). When topbar=false, the top title bar will not appear in the dev window.
                        \t -this is used for setting the background color and bgbitmap to help personalize the dev window.
                         \t -note --> topbar must be used before the bgbitmap or bgcolor option, otherwise it will have no effect.
                       \t -see dev_set_bgbitmap() and dev_set_bgcolor() for more information
    """
    return _pybox.DevSetConfig(*args,**kwargs)

def dev_set_nexty(y : int) -> bool :
    """
    Sets the Y position in the Dev Window for the next control.
    This can be useful in setting a top header bitmap, or moving controls
    down when setting a header bitmap. 

    As with setting the background color or bitmap, set_nexty() should be used
    before any controls are added to the dev window.
    """
    return _pybox.DevSetNextY(y)

def dev_closed(add_closebutton : bool = False) -> bool :
    """
    Returns True if the dev window was closed.  This is not an event and will return True continuously once the dev window is closed.

    Note: When dev_closed() is called, an 'x' will be added to the upper-right part of the window.

    Parameters:

        - add_closebutton      \t -- When 'true', a close button will be added as a control at the bottom of the dev window
    """
    return _pybox.DevWindowClosed(add_closebutton)

def dev_set_bgcolor(color1,color2 = None,display_bar : bool = True) -> bool :
    """
    Sets the background color of the dev window. 

    Note: This only works if it is called before any controls are added to the Dev Window. 

    Parameters:

        - color1      \t -- Color of the background 
        - color2      \t -- [optional] When given, this sets a gradient from color 1 to color 2
        - display_bar \t -- [optional] When set to True (default) the top display bar is kept and the bitmap is displayed underneath
                      \t - when set to False, the top display bar is removed and the bitmap starts at the top of the window.
    About Colors

    Colors may be text colors, such as "red" or "forestgreen" or "PanColor:forestgreen" or pybox.RgbColors, such as "0,255,0" for green.
    Colors may also be symbolic SageColor or PanColor colors, such as SageColor.SkyBlue() or PanColor.Blue()

    Examples:

        pybox.dev_set_bgcolor("black"); 
        pybox.dev_set_bgcolor("black","blue");
        pybox.dev_set_bgcolor(PanColor.ForestGreen())

    """
    return _pybox.DevSetBgColor(color1,color2,display_bar)

def dev_set_bgbitmap(bitmap,display_bar : bool = True,*args,**kwargs) -> bool :
    """
    Sets the background bitmap of the Dev Window

    Note: This only works if it is called before any controls are added to the Dev Window. 

    This bitmap should cover the width and height the Dev Window will be at its maximum.
    Dev Windows grow vertically when controls are added, and the bitmap should cover this space.

    Parameters:

        - bitmap      \t -- The bitmap to display.  This can be a path to the bitmap or a loaded bitmap.
        - display_bar \t -- [optional] When set to True (default) the top display bar is kept and the bitmap is displayed underneath

    Other options

        - Pady      \t -- opt.pady() or pady= can be used to set the position of the next control relative to the bottom of the bitmap.
                    \t - For example, pady(20) will add 20 pixels to the bottom of the bitmap for the next control

                    This can be useful when a background bitmap has a header, so the first control can start underneath it.

    Examples:

        dev_set_bgbitmap("c:\\bitmaps\\mybitmap.jpg")
        dev_set_bgbitmap(MyBitmap,pady=20)

    """
    return _pybox.DevSetBgBitmap(bitmap,display_bar,*args,**kwargs)

def dev_bitmap(bitmap,text = None,*args,**kwargs) -> bool :
    """
    Puts a bitmap in the dev window at the current place for the next control. 

    The bitmap can contain a transparency (as a .png or 32-bit bitmap) to blend into the background.

    Bitmaps in the Dev Window are meant to be either icons or header-style bitmaps, and are usually small vertically to keep
    space for the controls.

    Parameters:

        - bitmap      \t -- The bitmap to display.  This can be a path to the bitmap or a loaded bitmap.
        - text        \t -- [optional] Text to place directly to the right of the bitmap.  Pybox options can be used
                        \t - to set the font and text color

                        The center of the text is aligned to be at the center vertical center of the bitmap. 

    Other options

        - font,textcolor       \t -- These can set the font and color of the text. i.e. opt.textcolor("green") or opt.font(20)
        - pady                 \t -- this will add to the Y value of the next control relative to the bottom of the bitmap or text
                                \t - (whichever hangs over more).  For example, pady(20) will add 20 pixels to the start of the next control.

                                \t -This can be useful when the bitmap (and text) is a header, to add space before the next control starts

    Examples:

        dev_bitmap("c:\\bitmaps\\mybitmap.png")
        dev_bitmap("c:\\bitmaps\\mybitmap.png"," Project Controls")      -- note the space to add space between the image and text
        dev_bitmap("c:\\bitmaps\\mybitmap.png"," Project Controls",font=20,textcolor="green")
    """
    return _pybox.DevBitmap(bitmap,text,*args,**kwargs)

def dev_text(text = None,height=None,**kwargs) :
    """
    *** To be filled in ***
    """
    return Window(_pybox.DevText(text,height,**kwargs))

def dev_text_widget(text = None,*args,**kwargs) :
    """
    Create a text widget int the Dev Window.    This is the same type of Text Widget that can be created in a regular
    window with window.text_widget(), but automatically placed and sized in the Dev Window. 

    Since the Text Widget is automatically placed and sized in the window, fewer options are needed. 

    dev_text() returns a CTextWidget object where you can write out to the text widget.

    The Text Widget can be used to create static or dynamic text of any font size in the Dev Window.
    Parameters:

    - text          \t -- [optional] Sets the text of the widget.  This can be set later with textwidget.Write()
                    \t - When text is entered, the text widget is created to the width of the text.  Use the width() parameter to set a width or pad
                    \t - the text with spaces to reserve width.

    Pybox options can be included.  Some various options are as follows:

    - textColor         \t - Sets the text color of the widget (default is current window text color).  Same as opt.fgcolor()
    - font              \t - Sets the font of the text in the text widget
    - textCenter        \t - Centers the text inside of the widget (which can be longer than the text itself).
                            \t - Use TextCenterX() and CenterX() together to make sure text is centered in the window. This is only needed if the Width of the
                            \t - Text Widget and the text have been specificed separately.


    Examples:   
                \t -pybox.DevText(This is a text Widget)
                \t -pybox.DevText(This is a text Widget",opt.font(20),opt.textcolor("Yellow"))
    """
    return CTextWidget(_pybox.DevTextWidget(text,*args,**kwargs))

def dev_slider(title : str = None,*args,**kwargs) : 
    """
    Creates a slider in the Dev Window. The slider is automatically placed.

    A Slider class object is returned where the slider can be accessed and controlled. 

    Parameters:

    - title     \t -- Sets the title of the Slider

    Pybox options can be included.  Some various options are as follows:

    - range             \t -- Set the range of the slider.  The default range is (1,100)          
    - default           \t -- Set the default value of the slider.  The edfault is (0)
    - textColor         \t -- Sets the color of the label of the slider.
    - style("small")    \t -- Sets a smaller slider handle

    Examples:       \t -pybox.dev_slider("This is a slider")
                    \t -pybox.dev_slider("This is a slider",opt.range(100,500),opt.default(200))
                    \t -pybox.dev_slider("This is a slider",opt.textColor("Yellow"),opt.valuecolor("red"),opt.style("small"))
                    \t -pybox.dev_slider("This is a slider",textColor=Yellow,valueColor=red,Style="small"        \t - - (same as previous example)
    """
    return Slider(_pybox.DevSlider(title,*args,**kwargs))

def dev_slider_f(title : str = None,*args,**kwargs) : 
    """
    Creates a floating-point slider in the Dev Window. The slider is automatically placed.

    A Slider class object is returned where the slider can be accessed and controlled. 
    A floating-point slider sets a default range of 0-1.0

    User slider.get_pos_f() and slider.set_pos_f() to set and retrieve values.

    Range may be either direction (i.e. min,max or max, min). 

    Parameters:

    - title     \t -- Sets the title of the Slider

    Pybox options can be included.  Some various options are as follows:

    - range             \t -- Set the range of the slider.  The default range is (1,1.0)          
    - default           \t -- Set the default value of the slider.  The edfault is (0)
    - textColor         \t -- Sets the color of the label of the slider.
    - style("small")    \t -- Sets a smaller slider handle

    Examples:       \t -pybox.dev_slider_f("This is a slider")
                    \t -pybox.dev_slider_f("This is a slider",opt.range(100,500),opt.default(200))
                    \t -pybox.dev_slider_f("This is a slider",opt.textColor("Yellow"),opt.valuecolor("red"),opt.style("small"))
                    \t -pybox.dev_slider_f("This is a slider",textColor="yellow",valueColor="red",Style="small")        \t - - (same as previous example)
    """
    return Slider(_pybox.DevSlider(title,asfloat=True,*args,**kwargs))

def dev_checkbox(title : str = None,*args,**kwargs) -> Button :
    """
    Create a checkbox in the Dev Window.  The Checkbox is automatically placed. 
    The checkbox is unchecked by default.  Use opt.default(True) to default to checked.

    Parameters:

    - title    \t -- Sets the title of the checkbox 

    Pybox options can be included.  Some various options are as follows:

    - Default    \t -- Default(True) sets the check in the checkbox.  Default(False) leaves the checkbox unchecked.

    Examples:
                \t -Mypybox.dev_checkbox("Check me!")
                \t -Mypybox.dev_checkbox("Check me!",opt.default(True))
                \t -Mypybox.dev_checkbox("Check me!",default=True)
    """
    return Button(_pybox.DevCheckbox(title,*args,**kwargs))

def dev_button(text : str,*args,**kwargs) -> Button :
    """
    Create a Button in the DevWindow.  The Button is automtically placed.

    A Button type object is returned so the button can be used and events retrieved.

    Parameters:
        
    text        \t -- Sets the text of the button. 

    Keywords and Pybox options can be included.  Some various options are as follows:

    - Font     \t -- Sets the font for the button text 
    - Style    \t -- This can be a style of the default button or the name of a created button style.


    Example:   \t -pybox.dev_button("This is a button")
                \t -pybox.dev_button("This is a button",style="red")
    """
    return Button(_pybox.DevButton(text,*args,**kwargs))

def dev_combobox(text : str = None,titlecell : str = None,*args,**kwargs) -> Combobox :
    """
    Creates a Combobox in the DevWindow.  The Combobox is automatically placed. 

    A Combobox is like a list box except that it consists of a single tab that expands when activated, 
    and rolls back up when released. 

    This allows multiple listbox-style entries to take only the space of the height of one text line. 

    NewCombobox returns a Combobox type object so that items may be added and deleted, and user selections retrieved. 

    Parameters:

    - text          \t -- [optional] Initial text in the combobox.  This text can be one line or multiple lines representing multiple entries.  See examples.
    - titlecell     \t -- [optional] Tells the combobox to display this string int the combobox tab when no item is selected.  Otherwise the first added item is displayed.

    Keywords and Pybox options can be included.  Some various options are as follows:

    - Default    \t -- Default selection.  This is the index to the default selection (0 is the first selection, 1 the second, etc.)

    Examples:

                \t -Mypybox.dev_combobox() 
                \t -Mypybox.dev_combobox("First Item") 
                \t -Mypybox.dev_combobox("First Item\\nSecond Item\\nThird Item") 
                \t -Mypybox.dev_combobox(titlecell="This is a combobox") 
                \t -Mypybox.dev_combobox("First Item\\nSecond Item\\nThird Item",default=2) 
                \t -Mypybox.dev_combobox("First Item\\nSecond Item\\nThird Item",opt.default(2)) 
    """
    return Combobox(_pybox.DevCombobox(text,opt.cb_titlecell(titlecell),*args,**kwargs))

def dev_inputbox(title : str = None,text : str = None,*args,**kwargs) -> InputBox :
    """
    Creates a new Input Box in the Dev Window.  The Inputbox is automatically placed.

    Optional Parameters:

    - title         \t -- [optional] Label of the input box (displays to the left), but can shorten the input box itself.
    - text          \t -- [optional] This sets the starting text for the input box.  Otheriwse the input box is left blank at first. 

    Keywords and Pybox options can be included.  Some various options are as follows:

    - numbersOnly   \t -- Causes the input box to only accept numbers. 
    - readOnly      \t -- Sets the input box as read only so it can be used as a way to place a large amount of text that can be copied.
    - textColor     \t -- Sets the color of the text in the input box
    - bgColor       \t -- Sets the background color of the text in the input box
    - password      \t -- Causes the input box to display '*' for all text.
    - winColors     \t -- Sets the background input box color and text color to the current window color instead of the default white-and-black colors. 
    - thickBorder,recessed      \t -These are two different border styles that can be used.

    Examples:   \t -MyDevWindow.dev_inputbox("This is the title)          
                \t -MyDevWindow.dev_inputbox(text="This is the default text")
                \t -MyDevWindow.dev_inputbox("this is the title,"This is the default text",wincolors=True,thickborder=True())
    """
    return InputBox(_pybox.DevInputBox(title,opt.default(text),*args,**kwargs))

def dev_window(title : str = None,numlines : int = None,*args,**kwargs) -> Window :
    """
    Creates a new Window in the Dev Window.  The window is placed automatically and may be used to put out text and 
    other data. 

    The window defaults to 10 lines but can be set to any number of lines.

    Optional Parameters:

    - title         \t -- [optional] Title of the window.  This displays above the window. The default is no title.
    - numlines      \t -- [optional] Sets the number of lines for the default font in the window.  The default is 10 lines

    Keywords and Pybox options can be included.  Some various options are as follows:

    - font          \t -- Set the font for the window
    - textColor     \t -- Set the text/foreground color for the window
    - bgColor       \t -- Set the background color for the window. 
    """
    return Window(_pybox.DevWindow(title,numlines,*args,**kwargs))

def dev_radiobuttons(label : str,buttons : str,*args,**kwargs)  -> RadioButtonGroup  : 
    """
    Creates a group of Radio Buttons with an optional outer border and label.  

    The Radio Button group is placed in the window automatically.

    NewRadioButtons() returns a RadioButtonGroup object class where the buttons may be queried to see when pressed, and which 
    button was pressed.

    Parameters

    - title                 \t - - The title/label of the radio button group.  A box is drawn around the radio buttons with the title name.
    - buttons       \t - - The buttons to place in the checkbox group.  This can be one more more buttons, each button name separated by a a newline,
                                \t -for example, "button" for just one button, or "button 1\\nbutton 2\\nbutton 3" for 3 radio buttons.

    Keywords and Pybox options can be included.  Some various options are as follows:

    - Default       \t -- Sets the default index for the highlighted button.  There can only be one active radio button.  Default sets the
                        \t - index of the active/highlighted button (i.e. 0 = first button, 1 = second button, etc.)

    Examples:        
                    \t -pybox.dev_radio_buttons("These are radio buttons","This is the button")
                    \t -pybox.dev_radio_buttons("These are radio buttons","button 1\\nbutton2\\nbutton 3")
                    \t -pybox.dev_radio_buttons("These are radio buttons","button 1\\nbutton2\\nbutton 3",opt.default(1))

    """
    return RadioButtonGroup(_pybox.DevRadioButtons(buttons,opt.label(label),*args,**kwargs))

def dev_auto_close(auto_close : bool = True) -> bool :
    """
    *** This function is deprecated ***\n
    Sets the window to close automatically when there are no other windows open.
    By default, the Dev Window is a 'primary' window and won't close when
    functions such as WaitPending() or GetEvent() are used.

    When set to false (default), the window won't close until it is closed by the user. 
    or the program exits.
    """
    return _pybox.DevAutoClose(auto_close)


def dev_allow_auto_close(auto_close : bool = True) -> bool :
    """
    When set to False (e.g. dev_allow_auto_close(False), this will prevent the dev window closing when there are no other
    window open.
    
    By Default, when the last primary window is closed, the program will exit even if a Dev Window is open.   When this is set to False \
The dev window is left open until it is closed by the program or user.

    - note: If there a dev window is open when there are no other windows open, this function is not needed. In this case, the Dev Window \
will set itself to not close automatically since it recognized no other primary windows were open when created.
    """
    return _pybox.DevAllowAutoClose(auto_close)

def dev_set_location(x,y) -> bool :
    """
    Sets the location of the Dev Window.  See dev_set_location_l() to use a list, tuple or array for the location.

    Parameters

    - x,y                 \t - - New location of the Dev Window

    """
    return _pybox.DevSetLocation(int(x),int(y))

def dev_set_location_l(at : list) -> bool :
    """
    Sets the location of the Dev Window from a list, tuple or array.  See dev_set_location() to using independent x,y values.
    
    Parameters

    - x,y                 \t - - New location of the Dev Window

    """
    return _pybox.DevSetLocation(int(at[0]),int(at[1]))

def event_pending(peek = None) :
    """
    """
    return _pybox.EventPending(peek)
def get_event() : 
    """
    GetEvent waits for an event to occur in your main body of code. 

    - Events are any events such as a mouse move, click, keyboard press, etc. 
    - Events are also caused by any control change such as moving a slider, pressing a button, or pressing return in an input box. 
    - Events can also be a window closing, a window moving or changing size -- basically anything happening in the system sends a message

    Until an event occurs, the program is sleeping and not using any CPU time.  Pybox wakes up the program when an event happens. 

    In the event loop, you can check for events.  

    GetEvent() returns true until all main windows are closed. 

    Example:


            my_button = pybox.dev_button("Press Me")
            my_slider = pybox.def_slider()

            while pybox.get_event() :
                if my_button.pressed() : print("My Button was Pressed")
                if my_slider.moved()   : print("Range Slider is now at position",my_slider.get_pos())

    In this example, the program sleeps until an event occurs, and then the program checks to see if an event occured with a button or a slider movement. 

    Events are typically one-time:  Event-based functions report "True" on the first call, and then fals afterwards until another event of the same type happens. 
        
    You can also use a callback to retrieve events.  Though this is not recommended or useful for most programs, it can be useful for some specific purposes.
    See set_event_callback() for more information.
    """
    return _pybox.GetEvent()

def set_event_callback(callback : Callable[[None],None]) -> bool :
    """
    Use set_event_callback() to have a function called for every pybox event that occurs. See: reset_event_callback() to remove the callback.

        The callback will received all events that cause GetEvent() to wake up, such as mouse movement, button presses, or any control movement, window size changes, etc.
        The code inside of the EventCallback() can act the same as the code in the get_event() loop. 

        Note: The code in the Event Callback is in the main Windows/OS message loop and, therefore, can't take a lot of time with loops or processing -- this type of code needs to be in the main,
        procedural loop or as a new thread.  The code in the Event Callback is meant to process data and return, as it is holding up the window messaging while it is processing.

        The get_event() loop is passive and does not share the same concern. 

    - How to define the EventCallback   \t -- Define the EventCallback as a simple function with no parameters and no return value, i.e. "MyFunction()". See example below.     
    - Handle Events Where you Want      \t -- You can choose which events to handle in the Event Callback.  For example, handle only those necessary, and the rest in the GetEventLoop().
    - Using the GetEvent() loop is easier and is not less efficient than using a callback.

    When to use the Event Callback vs. the get_event() loop

        However, there are times when using an Event Callback can be useful.
        An example may be to set a signal for another process, such as responding to a button press and cancelling a process in the main GetEvent() loop.
        
        Any event that you want to handle while the main process is occupied (such as in a loop, dialog box etc.) can be handled in the EventCallback, and you don't
        have to worry about where the code will be excuted.

        While the code in the GetEvent() loop must be handled consciously by the program, the Event Callback is *always* called no matter what is happening in the system (unless it's alread in the Event Callback)

    Example:

        def event_calback() : 
            global button
            if button.pressed()     : qf.win.write("{y}Button Pressed\\ n")

        button = pybox.dev_button("Press me")
        pybox.set_event_callback(MyCallback)

        while pybox.get_event() : pass      # You can still handle events here when a callback is established (this example ignores them and wait for window close)
    """
    return _pybox.SetEventCallback(callback)

def reset_event_callback() -> bool : 
    "Removes a pybox EventCallback if one has been set up with SetEventCallback()"
    return _pybox.ResetEventCallback()

def exit_button(Message = None) : 
    """
    exit_button() comes up with a message and an "OK" button. 
    
    exit_button() is quick way to let the user know that the program has ended.

    See win.exit_button() to put an exit button at the bottom of a window.
    Parameters

    - Message       \t -- [optional].  Message to put in the window above the button.  If not specified, a default "program is finished" message is place in the window.

    About exit_button() and Displays using Windows and Graphics

    The exit_button() gives a way to pause the program before it ends so that the Windows and Graphics displaying don't suddenly disappear. 

    Whether Python, C++, or other languages, the Console Window is not part of the running application.  It is a separate application to which the running program is a client.
    When the program closes down, this other application (a separate process entirely) simply lets you know the program has ended.

    When windows and graphics are displayed in your program, and the program ends, it all disappears suddenly.  In a program with a Console Mode box, this will show a "program has ended"
    message in the box.  In a Windows application, the program will just "disappear"

    You can use exit_button() as a nice, quick method to pause and let the user know the program is ending in a GUI/graphical method.
    
    """
    _pybox.ExitButton(Message)                      
def wait_pending() : 
    """
    Waits for all open windows to close before continuing. 

    wait_pending() only waits for 'main' windows, such as program-created windows, ImageViewWindows, and DevWindows. 
    wait_pending() does not wait for widget windows to close, such as color selections windows, or any other windows classified as a widget.
    """
    return _pybox.WaitPending()

def wait_close_any() : 
    """
    Waits for any main window to close and returns. 

    wait_close_any() only waits for 'main' windows, such as program-created windows, ImageViewWindows, and DevWindows. 
    wait_close_any() does not wait for widget windows to close, such as color selections windows, or any other windows classified as a widget.
    """
    return _pybox.WaitCloseAny()

def debug_write(string : str) -> bool :
    """
    Write a message out to the sagebox debug window. The SageboxDebug window is in the Sagebox Process Window.

    When writing to the debug window, the debug window will come up automatically the first time it is written to.
    The debug window can be manually hidden (it will not come up automatically after that)

    The Sagebox debug window is a good place to put debug information so it won't clutter up the console window.
    Each line has a line number and you can scroll through the debug output. 

    --> To hide and show the debug/Sagebox process window, move the mouse to the upper-right of the monitor and hold for
        1/4 of a second.

    As with the console output functions, you can use colors to set the color of the output:

        - Use {color} to start a color and {} to end the color. 
            Example: pybox.DebugWrite("This is {red}in the color red{}")
        - You can use the first lett of the color, and do not need the closing {} if its at the end of the line:
            Example: pybox.DebugWrite("This is {r}in the color red")
        - Multiple colors can be used.
            \t -Example: pybox.DebugWrite("This {c}is in cyan{} and this {r}is in the color red")
        - "{x=<number>}" to set a column (does not use closing {}): Example: pybox.debug.Write("This {x=40}is at column 40")
        - "{bg=<color>"} to set the background color: Example: pybox.debug.Write("This {bg=r}background{} is in red") 
        - "{lbg=<color>} at the begining of the line to make the entire line the background color: 
            \t -Example: pybox.debug.Write("{lbg=blue}This entire line is in a blue background")
        - {bold} or {bld} for bold
        - {italic} or {i} for italic
        - {bolditalic} or {bi} for bold and italic
        - {div} for dividing line (i.e. DebugWrite("{div}\n") 

        Available Colors: Black, White, Gray, red, green, yellow, blue, cyan, purple/magenta,

        Abbreviation for Colors: w (white), r, g, y, b, c, p, m (magenta)
    """
    return _pybox.DebugWrite(string)
def debug_show(show : bool) -> bool :
    """
    Shows the pybox Process Window. 

    This window can be used to terminate a program and is a good place to put debug
    information.

    use debug.write() or debug_write() to send text to the debug window.
    """
    _pybox.DebugShow(show)
def debug_hide(hide : bool) -> bool :
    """
    Hides the pybox Process Window. 

    This window can be used to terminate a program and is a good place to put debug
    information.

    use debug.write() or debug_write() to send text to the debug window.
    """
    _pybox.DebugShow(not hide)

def get_color(color : str) -> RgbColor :
    """
    Returns a pybox RgbColor type with the color string specified.

    This function returns white if the color is not found.

    Examples:

    blue = get_color("blue")
    my_color = get_color("forestgreen");
    my_color = get_color("Pancolor:forestgreen")

    Pantone and Sagebox colors can also be used symblically by importing PanColor and SageColor from pybox, such as:

    my_color = SageColor.SkyBlue()
    my_color = PanColor.ForestGreen()

    """
    c = _pybox.GetColor(color)
    return RgbColor(c[0],c[1],c[2])

def set_defaults_file(file : str) -> bool :
    """
    ** This function to be documented in more detail at a later time **

    The default file can set the clear screen style, colors, or bitmap; the dev window bitmap backhground, as well as a number of other
    settings that can change the default display and behavior as Sagebox initializes windows and controls.
    
    This function sets the primary default file. If Sagebox has not yet been initialized, this filename is placed as the first
    file search as the default ini file.

    If Sagebox has already been initialized, the new file is read immediately and replaces any current defaults.
    
    ** note: file must contain path to ini file including the ini file name, e.g. "c:\mypath\subdir\defaults.ini", etc.
    
    Paramaters: 
    
    file - full-path name of file to use as defaults file.
    """
    return _pybox.SetDefaultsFile(file)
    
def disable_defaults() -> None :
    """
    Disables processing of any default files that Sagebox may load. 
    
    ** note:  That can be called at any time, but should be performed before opening any windows or controls. 
    """
    return _pybox.DisableDefaults()
    
def quick_form(type : str = None, title : str = None, size=None,*args,**kwargs) -> CQuickForm :
    """
    Creates a "QuickForm" window consisting of a Main Window, Application Window (i.e. Canvas), and a Dev Controls window for controls. 

    - A QuickForm Window puts a Dev Window and General Window together in a unified window to organize using controls and using graphics in the main window. 
    - this functions returns a CQuickForm object that can be used to access and control the created windows.
    - The functions pybox.NewWindow() and pybox.NewDevWindow() are effectively called with each window blended in the upper-main window. 
    - Note: Other QuickForm-type windows with user-designed controls will be available when the "UI Designer" is released to provide a forms-like interface for more up-front, intentional design.

    Windows Created 

        - main      \t -- The main window is the top-level window that hold the two (or more) innerwindows, label window, etc. 
        - win       \t -- This is the main 'blank' or 'canvas' window that acts as a normal window.  Items can be drawn in this window, and other window can be embedded within
                        \t - this window (i.e. ChildWindow()).  Any regular window function is available in this window -- it's simply a regular window embedded into the Main window
        - dev       \t -- This is a Dev Controls Window that is embedded in the main window, typically to the left of the 'Win' window.   With this window, you can easily add controls
                        \t - such as buttons, sliders, small window, list boxes, text widgets, etc. -- all with one line of code. 
    Parameters:

        - type      \t -- [optional] A String with type information about the QuickForm. Separate different values with ','
                        \t -- Filled      \t - (default) Sets the Window and Dev Window next to each other with no borders
                        \t -- Borders     \t - Puts a border around the application window
                        \t -- Plain       \t - Does not include the Dev Window.  When a title is not used, this is the same as using NewWindow()

    Additional Keyword parameters (i.e. QuickForm("label='MyLabel',ResizeOk") or QuickForm(label="MyLabel",resizeok=true)

        - Label     \t -- Sets a label that will appear in the Main Window above the application window. i.e. (Label="this is my program")
        - ResizeOk  \t -- [optional] Allows the Main window to be resized by dragging the borders.  It can also be maximized. Otherwise, the window cannot be resized by the user.
        - RealTime  \t -- [optional] Sets the main Quick form canvas window as a Realtime window intended to be used for real-time graphics. 
                        \t - see opt.realtime() for more information
        - Hidden    \t -- [optional] Tells QuickForm() to keep the window hidden when it is created.  The program then must call Main.Show() to show the window.  
                        \t -The default is to show the window on creation.
        - NoPadding \t -- [optional] for "filled" (default) window type, this removes the few pixels of space between the Win and Dev windows to merge them together with no break.
                        \t - This can be useful when changing the Win background color to a color other than the Main window background color.
        - NoAutoUpdate  \t - This will cause the Application Window (i.e. Win) to not update.  The program must then use the Win.Update() function to update any graphics sent to the window.    
        - <more options>    \t - See QuickForm documentation for more options available.

    Examples: 
         
        \t -qf = pybox.quick_form()
        \my_button = qf.dev.new_button("Press Me")
        \t -qf.win.Write("Hello World")
        \t -qf.main.create_menu("File,Save,About,Save")

        qf = pybox.quick_form(opt.label("This is the label in the window"))
        qf = pybox.quick_form("resizeok,grayblue","This is the window title",hidden=True)

    """
    qf = _pybox.QuickForm(type,opt.title(title),opt.size(size),*args,**kwargs)
    return CQuickForm(qf[0],qf[1],qf[2])


def vsync_startthread() -> bool :
    """
    Starts a vertical sync thread that is triggered on the vertical resync, allowing pybox to send vertical sync events to the message thread or event loop.

    Use vsync_ready() to determine of the vertical sync has occured. 
    """
    return _pybox.VSyncStartThread()

def vsync_endthread() -> bool :
    """
    If a vertical sync thread has been started, VsyncEndThread() will end the thread.
    """
    return _pybox.VSyncEndThread()


def new_devwindow(at = None,*args,**kwargs) :
    """
    Creates a new Dev Controls window where you can add automatically-placed controls with one line of code. 

    A Dev Window is a window made for creating, managing, adding, and deleting controls very easily and quickly. 

    Sagebox has a pre-defined Dev Window that you can access with the set of Dev functions, such as Sagebox::DevButton()

    new_dev_window() will create a new window where you can add more controls if the main Dev Window becomes too populated. 

    Parameters:

    - at            \t - [optional] Where to place the Dev Window.  When omitted, the new Dev Window is automatically placed in the window.

    """
    return DevControl(_pybox.NewDevWindow(opt.at(at),*args,**kwargs))

def new_window(title : str=None,size=None,at=None,*args,**kwargs) -> Window       :
    """
    Creates a new window on the desktop and returns a window object where you can perform window-based functions on that window.

    Parameters:
    
    - title             \t\t - -[optional] Title of window (in title bar)
    - at                \t\t - -[optional] X,Y location of window
    - size              \t\t - -[optional] Size of Window, i.e. size=(1000,4000)

    Keywords and Pybox options can be included.  Some various options are as follows:

    - Font          \t -- Sets the default font for the window, i.e. "Font(40)" or "Font("Arial,40")"
    - bgColor       \t -- Sets the background color of the window (i.e. "bgColor("Red")" or "bgColor(PanColor.ForestGreen())")
    - bgGradient    \t -- Sets a gradient background color of the window. Such as "bgGradient("black","blue").  You can also use Cls() to clear the window.
    - TextColor     \t -- Sets the text/foreground color of the window
    - NoAutoUpdate  \t -- Tells the window to not update automatically when graphics are placed in the window.  The program must call Update().  This can prevent flashing in real-time drawing.
    - ResizeOk      \t -- Allows the window to be resized by the user. 

    Examples:

        myWindow = new_window()
        mWindow.write("Hello World\\n")

        myWindow = new_window("This is the Title",Size=(500,200),at=(50,100),opt.bgcolor("PanColor:Blue"))
        myWindow = new_window(opt.bgcolor("PanColor:Blue"))  # This just sets the background color to blue.  Pybox chooses everything else.
    """
    return Window(_pybox.NewWindow(title,opt.at(at),opt.size(size),*args,**kwargs))

def get_integer(text=None,*args,**kwargs) -> int  :
    """
    Gets an integer value from a window that pops up with an input box.  The return value is the integer entered or default value.
    Call pybox.was_canceled() to determine if the user canceled the input box (opt.nocancel() will disallow the ability to cancel)

    Options:

    text        \t - [optional] The text to put as a header in the box.  You can use multiple lines.
                \t - if the first line starts with '+' that line becomes the title in the title bar and subsquent lines are printed in the description.

    Keywords Pybox options can be included.  Some various options are as follows:

    - Range         \t -Set a range for the input.  This will not allow an input outside of the range, but can allow the user to press return
    - Default       \t -Sets the default value.  This is placed in the input box when the box first comes up.  If the user presses return on a blank line, the default is returned.
    - NoCancel      \t -By defaut, there is a cancel button to allow the user to cancel.  You can call pybox.was_canceled() which returns True if the last input box was canceled.
                    \t -When NoCancel is specified, the user cannot cancel or press return on an empty line and must enter a value (a control-C may be pressed to stop the program.

    Examples:       \t -My Value = pybox.GetInteger("Enter a number")
                    \t -My Value = pybox.GetInteger("+This is the title bar title\\nEnter a number",range=(1,100),nocancel=True)
                    \t -My Value = pybox.GetInteger("Enter a number\nNumber should be between 1 and 100,range=(1,100),default=10)
    """    
    return _pybox.GetInteger(text,*args,**kwargs)

def get_float(text=None,*args,**kwargs) -> float  :
    """
    Gets an floating-point value from a window that pops up with an input box.  The return value is the integer entered or default value.
    Call pybox.was_canceled() to determine if the user canceled the input box (opt.nocancel() will disallow the ability to cancel)

    Parameters:

    - text          \t - [optional] The text to put as a header in the box.  You can use multiple lines.
                    \t - if the first line starts with '+' that line becomes the title in the title bar and subsquent lines are printed in the description.

    Keywords Pybox options can be included.  Some various options are as follows:

    - Range         \t -Set a range for the input.  This will not allow an input outside of the range, but can allow the user to press return
    - Default       \t -Sets the default value.  This is placed in the input box when the box first comes up.  If the user presses return on a blank line, the default is returned.
    - NoCancel      \t -By defaut, there is a cancel button to allow the user to cancel.  You can call pybox.was_canceled() which returns True if the last input box was canceled.
                    \t -When NoCancel is specified, the user cannot cancel or press return on an empty line and must enter a value (a control-C may be pressed to stop the program.

    Examples:       \t -My Value = pybox.GetFloat("Enter a number")
                    \t -My Value = pybox.GetFloat("+This is the title bar title\\nEnter a number",range=(1,100),nocancel=True)
                    \t -My Value = pybox.GetFloat("Enter a number\nNumber should be between 1 and 100,range=(1,100),default=10)
    """        
    return _pybox.GetFloat(text,*args,**kwargs)

def get_string(text=None,*args,**kwargs) -> str  :
    """
    Creates a window with an OK button to get a string from the user, displaying the text message above the input box. 

    This function returns a string of the user-inputted text, or a blank string if nothing was entered or the input was canceled.

    Use pybox.was_canceled() to determine of the input box was canceled by the user. 

    Parameters:

    - text          \t - [optional] The text to put as a header in the box.  You can use multiple lines.
                    \t - if the first line starts with '+' that line becomes the title in the title bar and subsquent lines are printed in the description.

    Keywords Pybox options can be included.  Some various options are as follows:

    - Default       \t -Sets the default text.  This is placed in the input box when the box first comes up.  If the user presses return on a blank line, the default is returned.
    - NoCancel      \t -By defaut, there is a cancel button to allow the user to cancel.  You can call pybox.was_canceled() which returns True if the last input box was canceled.
                    \t -When NoCancel is specified, the user cannot cancel or press return on an empty line and must enter some text (a control-C may be pressed to stop the program.
    """
    return _pybox.GetString(text,*args,**kwargs)

def get_open_file(filetypes : str = None) -> str     : 
    """
    Brings up the standard OS file selection menu where the user can select a file. 
    See get_save_file() for a 'save' file name so that the system prompts for "overwrite" permission on existing names.

    This function returns a string with the name of the file selected, or an empty string if the input was canceled.
    Use pybox.was_canceled() to determine if the input was canceled (or check for an emptystring)

    Parameters:

    - filetypes     \t -- [optional] filetypes to limit display to, such as "*.bmp", "*.bmp;*.jpg", etc.  Default is no filter and will display all files

    Examples: 
            \t -pybox.get_open_file()
            \t -pybox.get_open_file("*.bmp")
            \t -pybox.get_open_file("*.bmp;*.png;*.jpg")

    """
    return _pybox.GetOpenFile(filetypes)

def get_save_file(filetypes : str = None) -> str     : 
    """
    Brings up the standard OS file selection menu where the user can select a file to save.
    The system will prompt for "overwrite" permission for existing names, but will not alter the file.  
    The function only returns the name selected, or an empty string.

    This function returns a string with the name of the file selected, or an empty string if the input was canceled.
    Use pybox.was_canceled() to determine if the input was canceled (or check for an emptystring)

    Parameters:

    - filetypes     \t -- [optional] filetypes to limit display to, such as "*.bmp", "*.bmp;*.jpg", etc.  Default is no filter and will display all files

    Examples: 
            \t -pybox.get_save_file()
            \t -pybox.get_save_file("*.bmp")
            \t -pybox.get_save_file("*.bmp;*.png;*.jpg")

    """
    return _pybox.GetSaveFile(filetypes)


def read_image_file(filename,**kwargs)  -> Bitmap  : 
    """
    Reads an image file and returns a bitmap. 

    Currently, files may be of type .bmp,jpeg, or .png.  Other types will be added in the future. 
    For other types, packages such as SciPy can be used.

    Parameters

    - filename      \t -- Filename of the image

    Returns:

    This function returns a 24-Bit Bitmap object with the bitmap.  If the file was not found, the bitmap will be empty.
    If the image has a mask, such as a PNG or 32-bit bitmap, this will be attached to the bitmap. 

    The Bitmap can be converted to a numpy array with the bitmap's get_array() function.  See examples.

    Use the Bitmap's is_valid() function to determine if the bitmap was read ok.  You can also use pybox.was_canceled() to determine if the 
    function could not find the bitmap

    """
    return Bitmap(_pybox.ReadImageFile(filename,**kwargs))

def create_bitmap(width : int,height : int) -> Bitmap :
    """
    Creates a Bitmap object with a bitmap of the width and height specified.

    The Bitmap object may then be used as a bitmap.  The Bitmap's get_array() function will return the data as a numpy array in the
    form unsigned char: [height][width][3], where the [3] are the unsigned char Blue, Green, and Red values, respectively.

    If the function fails the Bitmap's is_valid() function will return True
    Also use was_canceled() to determine if there was an error

    """
    return Bitmap(_pybox.CreateBitmap(width,height))

def copy_bitmap(bitmap : Bitmap) -> Bitmap :
    """
    Copies a bitmap ito a new bitmap and returns a Bitmap object.

    This function can be useful for copying array-based bitmaps into pybox bitmap for pybox function use. 

    Most pybox functions will use pybox Bitmaps or array-based bitmaps created by packages such as SciPy.

    Creating a pybox bitmap can be faster, as it is stored separately and does not need to be translated or copied when used.

    If the function fails, the Bitmap's is_valid() function will return true.
    Also use was_canceled() to determine if there was an error

    """
    return Bitmap(_pybox.CopyBitmap(bitmap._Bitmap__id))

def img_view(bitmap,title=None,at=None,size=None,percent=None,zoombox=None,*args,**kwargs) -> _ImageView :
    """
    Creates an ImageView window where you can zoom and and out of the displayed image and move it around for inspection. 
    The window can be resized and maximized.  See img_view_r() to display the image upside-down.

    - This function returns an _ImageView class object where you can control the ImageView window that is created.  However, it is not
        \t -necessary to keep the return object or assign it to a variable. 
    - The system menu (upper-left corner) has a number of options to bring up a Zoom Box, reset the image, etc.
    - Use img_zoom() to bring up a Zoom Box that can be used to navigate through the image. 

    About the Zoom Box

    The Zoom box as a small window that works with all ImgView images.  Multiple images can be displayed, and the Zoom Box will update to the currently selected image.

    Also see: img_zoom() -- brings up an ImageView Window with a zoom box (otherwise it can be selected from the upper-left system menu)
    Also see: img_before_after() -- brings up a window with two images, such as before and after images, for comparison.

    Parameters:

    - bitmap        \t - The bitmap to display.  This can be a pybox bitmap, a general RGB array, or a text string with the path to the bitmap
    - title         \t - This is the title of the image that will display in the title bar
    - at            \t - Where to put the window.  If this is not used, the window is placed automatically.
    - size          \t - Size of the window box.  The Image will be adjust accordingly based on the size given.  The default is for ImgView() to choose automatically.
    - percent       \t - Desired size of the image in percent to show on initial launch.  This can be useful for specifying thumbnail images with a smaller size.

    Pybox options can be included.  Some various options are as follows:

    - reverse       \t -- Displays the bitmap upside-down.  Bitmaps often come updside-down. "reverse" corrects this.  Also see: image_view_r
    - normalize     \t -- Use this when the bitmap ranges from 0.0-1.0.  normalize=True will convert the image to a displayable bitmap i.e. 0-255 on each channel)
    - label         \t -- This will put a text label underneath the image in a larger font for better labeling display.
                        \t -If no Label is given with no Title, the title bar text will also be the label text.
                          
    About Bitmaps: Bitmaps can be a pybox bitmap or a general RGB array bitmap (i.e. numpy array) in the form [height][width][3], where the [3] is Blue, Green, and Red,
    or an RGB32 bitmap array of [height][width][4] where the 4 values are Red, Green, Blue, and Mask, in that order.
    
    The bitmap format can be unsigned char, float, double, mono, mono float, and half-float. 
    """
    return _ImageView(_pybox.ImgView(bitmap,opt.title(title),opt.at(at),opt.size(size),opt.percent(percent),opt.zoombox(zoombox),*args,**kwargs))

def img_view_r(bitmap,title=None,at=None,size=None,percent=None,zoombox=None,*args,**kwargs) -> _ImageView :
    """
    Creates an ImageView window where you can zoom and and out of the displayed image and move it around for inspection. 
    The window can be resized and maximized.  This image is displayed upside-down in relation to the bitmap.
    See img_view() to display the image non-upside-down. 

    - This function returns an _ImageView class object where you can control the ImageView window that is created.  However, it is not
    necessary to keep the return object or assign it to a variable. 
    - The system menu (upper-left corner) has a number of options to bring up a Zoom Box, reset the image, etc.
    - Use img_zoom() to bring up a Zoom Box that can be used to navigate through the image. 

    About the Zoom Box

    The Zoom box as a small window that works with all ImgView images.  Multiple images can be displayed, and the Zoom Box will update to the currently selected image.

    Also see: img_zoom() -- brings up an ImageView Window with a zoom box (otherwise it can be selected from the upper-left system menu)
    Also see: img_before_after() -- brings up a window with two images, such as before and after images, for comparison.

    Parameters:

    - bitmap        \t - The bitmap to display.  This can be a pybox bitmap, a general RGB array, or a text string with the path to the bitmap
    - title         \t - This is the title of the image that will display in the title bar
    - at            \t - Where to put the window.  If this is not used, the window is placed automatically.
    - size          \t - Size of the window box.  The Image will be adjust accordingly based on the size given.  The default is for ImgView() to choose automatically.
    - percent       \t - Desired size of the image in percent to show on initial launch.  This can be useful for specifying thumbnail images with a smaller size.

    Pybox options can be included.  Some various options are as follows:

    - normalize     \t -- Use this when the bitmap ranges from 0.0-1.0.  normalize=True will convert the image to a displayable bitmap i.e. 0-255 on each channel)
    - label         \t -- This will put a text label underneath the image in a larger font for better labeling display.
                        \t -If no Label is given with no Title, the title bar text will also be the label text.
                          
    About Bitmaps: Bitmaps can be a pybox bitmap or a general RGB array bitmap (i.e. numpy array) in the form [height][width][3], where the [3] is Blue, Green, and Red,
    or an RGB32 bitmap array of [height][width][4] where the 4 values are Red, Green, Blue, and Mask, in that order.
    
    The bitmap format can be unsigned char, float, double, mono, mono float, and half-float. 
    """    
    return _ImageView(_pybox.ImgViewR(bitmap,opt.title(title),opt.at(at),opt.size(size),opt.percent(percent),opt.zoombox(zoombox),*args,**kwargs))

def img_zoom(bitmap,title=None,at=None,size=None,percent=None,*args,**kwargs) -> _ImageView :
    """
    Creates an ImageView and Zoom Box window where you can zoom and and out of the displayed image and move it around for inspection. 
    The window can be resized and maximized.  See img_zoom_r() to display the image upside-down.

    - This function is the same as img_view() except that it creates a ZoomBox as a small window to make navigating the image easier. 
    - This function returns an _ImageView class object where you can control the ImageView window that is created.  However, it is not
    necessary to keep the return object or assign it to a variable. 
    - The system menu (upper-left corner) has a number of options to bring up a Zoom Box, reset the image, etc.
    - Use img_zoom() to bring up a Zoom Box that can be used to navigate through the image. 

    About the Zoom Box

    The Zoom box as a small window that works with all ImgView images.  Multiple images can be displayed, and the Zoom Box will update to the currently selected image.

    Also see: img_zoom() -- brings up an ImageView Window with a zoom box (otherwise it can be selected from the upper-left system menu)
    Also see: img_before_after() -- brings up a window with two images, such as before and after images, for comparison.

    Parameters:

    - bitmap        \t - The bitmap to display.  This can be a pybox bitmap, a general RGB array, or a text string with the path to the bitmap
    - title         \t - This is the title of the image that will display in the title bar
    - at            \t - Where to put the window.  If this is not used, the window is placed automatically.
    - size          \t - Size of the window box.  The Image will be adjust accordingly based on the size given.  The default is for ImgView() to choose automatically.
    - percent       \t - Desired size of the image in percent to show on initial launch.  This can be useful for specifying thumbnail images with a smaller size.

    Pybox options can be included.  Some various options are as follows:

    - normalize     \t -- Use this when the bitmap ranges from 0.0-1.0.  normalize=True will convert the image to a displayable bitmap i.e. 0-255 on each channel)
    - reverse       \t -- Displays the bitmap upside-down.  Bitmaps often come updside-down. "reverse" corrects this.  Also see: ImgZoomR()
    - label         \t -- This will put a text label underneath the image in a larger font for better labeling display.
                        \t -If no Label is given with no Title, the title bar text will also be the label text.
                          
    About Bitmaps: Bitmaps can be a pybox bitmap or a general RGB array bitmap (i.e. numpy array) in the form [height][width][3], where the [3] is Blue, Green, and Red,
    or an RGB32 bitmap array of [height][width][4] where the 4 values are Red, Green, Blue, and Mask, in that order.
    
    The bitmap format can be unsigned char, float, double, mono, mono float, and half-float. 
    """      
    return _ImageView(_pybox.ImgView(bitmap,opt.title(title),opt.at(at),opt.size(size),opt.percent(percent),opt.zoombox(True),*args,**kwargs))

def img_zoom_r(bitmap,title=None,at=None,size=None,percent=None,*args,**kwargs) -> _ImageView :
    """
    Creates an ImageView and Zoom Box window where you can zoom and and out of the displayed image and move it around for inspection. 
    The window can be resized and maximized. This displays the bitmap upside-down. See img_zoom() to display the image non-upside-down.

    - This function is the same as img_view() except that it creates a ZoomBox as a small window to make navigating the image easier. 
    - This function returns an _ImageView class object where you can control the ImageView window that is created.  However, it is not
    necessary to keep the return object or assign it to a variable. 
    - The system menu (upper-left corner) has a number of options to bring up a Zoom Box, reset the image, etc.
    - Use img_zoom() to bring up a Zoom Box that can be used to navigate through the image. 

    About the Zoom Box

    The Zoom box as a small window that works with all ImgView images.  Multiple images can be displayed, and the Zoom Box will update to the currently selected image.

    Also see: img_zoom() -- brings up an ImageView Window with a zoom box (otherwise it can be selected from the upper-left system menu)
    Also see: img_before_after() -- brings up a window with two images, such as before and after images, for comparison.

    Parameters:

    - bitmap        \t - The bitmap to display.  This can be a pybox bitmap, a general RGB array, or a text string with the path to the bitmap
    - title         \t - [optional] This is the title of the image that will display in the title bar
    - at            \t - [optional] Where to put the window.  If this is not used, the window is placed automatically.
    - size          \t - [optional] Size of the window box.  The Image will be adjust accordingly based on the size given.  The default is for ImgView() to choose automatically.
    - percent       \t - [optional] Desired size of the image in percent to show on initial launch.  This can be useful for specifying thumbnail images with a smaller size.

    Pybox options can be included.  Some various options are as follows:

    - normalize     \t -- Use this when the bitmap ranges from 0.0-1.0.  normalize=True will convert the image to a displayable bitmap i.e. 0-255 on each channel)
    - label         \t -- This will put a text label underneath the image in a larger font for better labeling display.
                        \t -If no Label is given with no Title, the title bar text will also be the label text.
                          
    About Bitmaps: Bitmaps can be a pybox bitmap or a general RGB array bitmap (i.e. numpy array) in the form [height][width][3], where the [3] is Blue, Green, and Red,
    or an RGB32 bitmap array of [height][width][4] where the 4 values are Red, Green, Blue, and Mask, in that order.
    
    The bitmap format can be unsigned char, float, double, mono, mono float, and half-float. 
    """    
    return _ImageView(_pybox.ImgViewR(bitmap,opt.title(title),opt.at(at),opt.size(size),opt.percent(percent),opt.zoombox(True),*args,**kwargs))

def img_before_after(bitmap1,bitmap2,title=None,label=None,before_title=None,after_title=None,at=None,size=None,percent=None,*args,**kwargs) -> _ImageView :
    """
    Creates an ImageView window with a Before and After image, and Zoom Box window where you can zoom and and out of the displayed images and easily move them
    around for inspection.  The window can be resized and maximized.  See img_before_after_r() to display the images upside-down.

    - The system menu (upper-left corner) has a number of options.
    - This returns an _ImageBeforeAfter class object that can be used to control the window. However, it is not necessary to save the return object. 
        \t -with the return object, you can determine when the window is closed and can also close all open ImageView Windows, as well as many other functions.

    About the Zoom Box

    The Zoom box as a small window that works with all ImgView images.  Multiple images can be displayed, and the Zoom Box will update to the currently selected image.

    Parameters:

    - bitmap1       \t - The 'before' bitmap to display.  This can be a pybox bitmap or a general RGB array.
    - bitmap2       \t - The 'after' bitmap to display.  The bitmaps must be the same size, but can be different formats.
    - title         \t - This is the title of the image that will display in the title bar
    - before_title   \t - title/label for the 'before' bitmap.  If not specified, a default label is used
    - after_title    \t - title/label for the 'after' bitmap.  If not specified, a default label is used
    - at            \t - Where to put the window.  If this is not used, the window is placed automatically.
    - size          \t - Size of the window box.  The Image will be adjust accordingly based on the size given.  The default is for ImgView() to choose automatically.
    - percent       \t - Desired size of the image in percent to show on initial launch.  This can be useful for specifying thumbnail images with a smaller size.

    Pybox options can be included.  Some various options are as follows:

    - normalize     \t -- Use this when the bitmap ranges from 0.0-1.0.  normalize=True will convert the image to a displayable bitmap i.e. 0-255 on each channel)
    - label         \t -- This will put a text label above both images.
                        \t -If no Label is given with no Title, the title bar text will also be the label text.
                                                
    About Bitmaps: Bitmaps can be a pybox bitmap or a general RGB array bitmap (i.e. numpy array) in the form [height][width][3], where the [3] is Blue, Green, and Red,
    or an RGB32 bitmap array of [height][width][4] where the 4 values are Red, Green, Blue, and Mask, in that order.
    
    The bitmap format can be unsigned char, float, double, mono, mono float, and half-float. 
    """
    return _ImageBeforeAfter(_pybox.ImgBeforeAfter(bitmap1,bitmap2,opt.title(title),opt.str_str("BeforeTitle",before_title),opt.str_str("AfterTitle",after_title),opt.label(label),
                                                   opt.at(at),opt.size(size),opt.percent(percent),*args,**kwargs))
def img_before_after_r(bitmap1,bitmap2,title=None,label=None,before_title=None,after_title=None,at=None,size=None,percent=None,*args,**kwargs) -> _ImageView :
    """
    Creates an ImageView window with a Before and After image, and Zoom Box window where you can zoom and and out of the displayed images and easily move them
    around for inspection.  The window can be resized and maximized.  The images are displayed upside-down. See img_before_after() to display the images non-upside-down.

    - The system menu (upper-left corner) has a number of options.
    - This returns an _ImageBeforeAfter class object that can be used to control the window. However, it is not necessary to save the return object. 
        \t -with the return object, you can determine when the window is closed and can also close all open ImageView Windows, as well as many other functions.

    About the Zoom Box

    The Zoom box as a small window that works with all ImgView images.  Multiple images can be displayed, and the Zoom Box will update to the currently selected image.

    Parameters:

    - bitmap1       \t - The 'before' bitmap to display.  This can be a pybox bitmap or a general RGB array.
    - bitmap2       \t - The 'after' bitmap to display.  The bitmaps must be the same size, but can be different formats.
    - title         \t - This is the title of the image that will display in the title bar
    - before_title   \t - title/label for the 'before' bitmap.  If not specified, a default label is used
    - after_title    \t - title/label for the 'after' bitmap.  If not specified, a default label is used
    - at            \t - Where to put the window.  If this is not used, the window is placed automatically.
    - size          \t - Size of the window box.  The Image will be adjust accordingly based on the size given.  The default is for ImgView() to choose automatically.
    - percent       \t - Desired size of the image in percent to show on initial launch.  This can be useful for specifying thumbnail images with a smaller size.

    Pybox options can be included.  Some various options are as follows:

    - normalize     \t -- Use this when the bitmap ranges from 0.0-1.0.  normalize=True will convert the image to a displayable bitmap i.e. 0-255 on each channel)
    - label         \t -- This will put a text label above both images.
                        \t -If no Label is given with no Title, the title bar text will also be the label text.
                          
    About Bitmaps: Bitmaps can be a pybox bitmap or a general RGB array bitmap (i.e. numpy array) in the form [height][width][3], where the [3] is Blue, Green, and Red,
    or an RGB32 bitmap array of [height][width][4] where the 4 values are Red, Green, Blue, and Mask, in that order.
    
    The bitmap format can be unsigned char, float, double, mono, mono float, and half-float. 
    """    
    return _ImageBeforeAfter(_pybox.ImgBeforeAfterR(bitmap1,bitmap2,opt.title(title),opt.str_str("BeforeTitle",before_title),opt.str_str("AfterTitle",after_title),opt.label(label),
                                                    opt.at(at),opt.size(size),opt.percent(percent),*args,**kwargs))


def msgbox(text : str,*args,**kwargs) -> bool :
    """
    Displays a window with the given text and an "OK" button. Note: InfoWindow() and QuickButton() are the same function.

    This is used to present general information in a window box. 

    Parameters: 

    - text          \t -- text to put into the window. 

    About Dialog Box Text

    The text for the dialog box can contain multiple lines.  The first line will be displayed in a larger font, with subsequent lines displayed in a smaller font. 
    If the first line in the text starts with a '+' the text line becomes the text in the title bar window and is not placed in the dialog box itself. 

    Examples:

            \t -pybox.msgbox("Press OK to continue")
            \t -pybox.msgbox("+Information Window\nPress OK to continue")
            \t -pybox.msgbox("Finished Processing\nPress OK to continue")
            \t -pybox.msgbox("+My Process\nFinished Processing\nPress OK to continue")
    """    
    return _pybox.InfoWindow(text,str,*args,**kwargs)

def msgbox_info(text : str,*args,**kwargs) -> bool :
    """
    Displays a window with the given text and an "OK" button. Note: InfoWindow() and QuickButton() are the same function.

    This is used to present general information in a window box. 

    Parameters: 

    - text          \t -- text to put into the window. 

    About Dialog Box Text

    The text for the dialog box can contain multiple lines.  The first line will be displayed in a larger font, with subsequent lines displayed in a smaller font. 
    If the first line in the text starts with a '+' the text line becomes the text in the title bar window and is not placed in the dialog box itself. 

    Examples:

            \t -pybox.msgbox_info("Press OK to continue")
            \t -pybox.msgbox_info("+Information Window\nPress OK to continue")
            \t -pybox.msgbox_info("Finished Processing\nPress OK to continue")
            \t -pybox.msgbox_info("+My Process\nFinished Processing\nPress OK to continue")
    """    
    return _pybox.InfoWindow(text,str,*args,**kwargs)

def msgbox_yesno(text : str,*args,**kwargs) -> bool :
    """
    Displays a window with the given text and an "yes" button and a "no" button.

    Parameters: 

    - text          \t -- text to put into the window. 

    Returns: True if "Yes" was input, or False if the No was pressed. 

    About Dialog Box Text

    The text for the dialog box can contain multiple lines.  The first line will be displayed in a larger font, with subsequent lines displayed in a smaller font. 
    If the first line in the text starts with a '+' the text line becomes the text in the title bar window and is not placed in the dialog box itself. 

    Examples:

            \t -pybox.msgbox_yesno("Would you like to continue?")
            \t -pybox.msgbox_yesno("+Yes No Window\nWould you like to continue?")
            \t -pybox.msgbox_yesno("Finished Processing\nWould you like to continue?")
            \t -pybox.msgbox_yesno("+My Process\nWould you like to Continue?\nPress Yes to continue, No to quit.")

    """    
    return _pybox.YesNoWindow(text,str,*args,**kwargs)

def msgbox_yesnocancel(text : str,*args,**kwargs) -> bool :
    """
    Displays a window with the given text and an "yes" button, "no" button, and "Cancel" button

    Parameters: 

    - text          \t -- text to put into the window. 

    Returns: True if "Yes" was input, or False if the No was pressed. 
                Use "pybox.dialog.WasCancelled() or pybox.WasCancelled() to determine if the Cancel button was pressed.

    About Dialog Box Text

    The text for the dialog box can contain multiple lines.  The first line will be displayed in a larger font, with subsequent lines displayed in a smaller font. 
    If the first line in the text starts with a '+' the text line becomes the text in the title bar window and is not placed in the dialog box itself. 

    Examples:

            \t -pybox.msgbox_yesnocancel("Would you like to continue?")
            \t -pybox.msgbox_yesnocancel("+Yes No Window\nWould you like to continue?")
            \t -pybox.msgbox_yesnocancel("Finished Processing\nWould you like to continue?")
            \t -pybox.msgbox_yesnocancel("+My Process\nWould you like to Continue?\nPress Yes to continue, No to quit,Cancel to Exit.")

    """    
    return _pybox.YesNoCancelWindow(text,str,*args,**kwargs)

def msgbox_okcancel(text : str,*args,**kwargs) -> bool :
    """
    Displays a window with the given text and an "Ok" button, and "Cancel" button

    Parameters: 

    - text          \t -- text to put into the window. 

    Returns: True if "Ok" was input, or False if the Cancel was pressed. 
                Use "pybox.dialog.WasCancelled() or pybox.WasCancelled() to determine if the Cancel button was pressed.

    About Dialog Box Text

    The text for the dialog box can contain multiple lines.  The first line will be displayed in a larger font, with subsequent lines displayed in a smaller font. 
    If the first line in the text starts with a '+' the text line becomes the text in the title bar window and is not placed in the dialog box itself. 

    Examples:

            \t -pybox.msgbox_okcancel("Would you like to continue?")
            \t -pybox.msgbox_okcancel("+Yes No Window\nWould you like to continue?")
            \t -pybox.msgbox_okcancel("Finished Processing\nWould you like to continue?")
            \t -pybox.msgbox_okcancel("+My Process\nWould you like to Continue?\nPress Yes to continue or Cancel to quit.")

    """
    return _pybox.OkCancelWindow(text,str,*args,**kwargs)

def quick_button(text : str,title : str = "Quick Button",*args,**kwargs) -> bool :
    """
    Displays a window with the given text and an "OK" button. Note: InfoWindow() and QuickButton() are the same function.

    This is used to present general information in a window box. 

    Parameters: 

    - text          \t -- text to put into the window. 

    About Dialog Box Text

    The text for the dialog box can contain multiple lines.  The first line will be displayed in a larger font, with subsequent lines displayed in a smaller font. 
    If the first line in the text starts with a '+' the text line becomes the text in the title bar window and is not placed in the dialog box itself. 

    Examples:

            \t -pybox.quick_button("Press OK to continue")
            \t -pybox.quick_button("+Information Window\nPress OK to continue")
            \t -pybox.quick_button("Finished Processing\nPress OK to continue")
            \t -pybox.quick_button("+My Process\nFinished Processing\nPress OK to continue")
    """
    return _pybox.InfoWindow(text,title,*args,**kwargs)

def please_wait(text = None,cancelok : bool = False,*args,**kwargs) -> bool :
    """
    Displays a please wait window in the center of the screen.
        
    Parameters:

    - text         \t - - [optional] text to display in the Please Wait Window. If multiple lines are used, the first line displays in a larger font.
    - cancelok    \t - - [optional] if specified, a "cancel" button.  This can be checked with please_wait_canceled() in the event loop.

    Keywords Pybox options can be included.  Some various options are as follows:

    - ProgressBar         \t -- Adds a progress bar to the please wait window.  This can be set from 0-100% with please_wait_set_progress()

    Examples:

            \t -pybox.please_wait()
            \t -pybox.please_wait("Wait for process to finish")
            \t -pybox.please_wait("Wait for process to finish\\nPress cancel to abort",True,opt.progresbar())
    """
    return _pybox.PleaseWaitWindow(text,opt.cancelok(cancelok),*args,**kwargs)

def close_please_wait() -> bool :
    """
    Closes the Please Wait window if it is open.
    """
    return _pybox.ClosePleaseWait()

def please_wait_set_progress(percent : int) -> bool :
    """
    If a Please Wait Window is open and has a progress bar, please_wait_set_progress() will set the percent complete of the progress bar.
        
    Parameters:

    - percent          \t - - Percent (0-100) complete.

    """
    return _pybox.PleaseWaitSetProgress(percent)

def please_wait_canceled() -> bool :
    """
    Returns True if the "Cancel" button was pressed in a Please Wait Window, False if not or after the first True return (because it is an event)
        
    note: Even when the Cancel button is pressed, the program must still close the Please Wait window with close_please_wait().

    --> This function an EVENT function: This function will only return a True value ONE TIME PER EVENT 
    --> and will return False after the first call until the event occurs again. 

        In most events, you can specify "peek=true" as a parameter so that the event will not be reset.
    """
    return _pybox.PleaseWaitCanceled()

def show_imgview_instructions() -> None :
    """
    Shows the Image_view() and image_before_after() instructions in a window on the screen. 
    The window has an OK button that will close when pressed.

    This is the same window that appears when "show instructions" is chosen from the
    system menu im the image_view() window.
    """
    return _pybox.ShowImgViewInstructions()

def color_selector(at=None,**kwargs) -> _ColorSelector :
    """
    Opens a Color Selector widget, as a popup window.    
    - note: This is a standalone function and does not require creation of a window.  In this case, pybox.get_event() can be use to poll for color_selector events \
e.g. color_selector::value_changed(), etc.

    - See Window.color_selector() for use with an existing window.
        
    With the color selector, you can select an RGB color using the wheel or input boxes next to the wheel itself. 
    A color rectangle is shown with the currently selected color.
        
    color_selector() returns a _ColorSelector object which can be used to look at changes in the color wheel in the window's main event loop. 
        
    See the _ColorSelector object functions for more information.
        
    Parameters:
        
    - at          \t - Where to put the Color Selector Window.  If this is not used, the Color Selector Window is placed automatically.

    Keywords usable when creating the Color Selector:

    - Title         \t - Sets a title displayed in the window's top bar area, such as title="This is the window title".  Otherwise a default title is used.
    - x,y           \t - 'x' and 'y' keywords can be used in place of using the 'at' parameter, i.e. x=500, y=200 instead of (500,200) or at=(500,200)
  
    examples:\t - color_sel = color_selector(at=(500,200))     --> Opens a Color Selector window as an individual window on the screen at x=500 and y=200
        
    - while pybox.GetEvent() : if (color_sel.value_changed()) print("Color value = ",color_sel.get_rgb_value()) --> prints values as the wheel is moved.
    """
    return _ColorSelector(_pybox.ColorSelector(opt.at(at),**kwargs))

def display_default_paths() :
    """
    Displays to the console window the default paths that Sagebox will search for Sagebox Defaults Ini information.

    The default filename is "SageDefaults.ini", which can be explicitly specified with SetDefaultFile()
    
    Sagebox will search any explicit directories set, and added by a subsystem (such as C#), the current directory, module/executable directory, in this order. 
    
    --> Use disable_defaults() to disable any loading of default .ini files. 
    """
    _pybox.DisplayDefaultPaths()
        
def set_win_timer_update_ms(update_ms : int) -> bool :
    """
    Sets the timer delay on "timer" or "ontime" window updates, which update any needed windows on a timer set through the OS, instead of
    the default update, which is performed when graphics functions are used and it is time to update the window.
    
    --> This can be set to a value between 22ms (default) and 10000 (10 seconds). 
    --> This function can be useful to set a longer delay on update with buys graphics routines, to show constant updates but also 
    slow the updates down (e.g. 50ms, 1000ms, etc.) to keep the refresh rate lower, using less cpu time.

    Parameters:
    
    update_ms - milliseconds to set for update frequency for "ontime"/"timer" auto-update type
    
    Returns:
   
    True if successful.  False is returned if the millisecond value is out of range.
    """
    return _pybox.SetWinTimerUpdateMs(update_ms)


class opt :
    def __init__(self,text) : self.__text = "{}".format(text)
    def __add__(self,other) : return opt("{}{}".format(self.__text,other.__text))
    def interact() : 
        "Add this to a pybox.NewWindow() call in interactive mode for a window that comes up to the right and stays on top of the interactive session."
        return opt(",Interactive,")
    def fgcolor(color)      :
        "Sets the foreground or text color of a control or object"
        return opt(",fgColor={},".format(color))
    def bgcolor(color)      :
        "Sets the background or text color of a control or object"
        return opt(",bgColor={},".format(color))
    def textcolor(color)    :
        "Sets the foreground or text color of a control or object"
        return opt(",TextColor={},".format(color))
    def valuecolor(color)    :
        "Sets the foreground or text color of the value of a control (i.e. a slider)"
        return opt(",ValueColor={},".format(color))
    def color(color)        :
        "Sets the color of an object.  Usually the textcolor, but depends on context.  See fgColor() and TextColor() for more specific options."
        return opt(",Color={},".format(color))
    def font(font)          :
        """
        Sets the font.  If a number is used, it sets the font to the font size in the default font.
        Otherwise, specific fonts may be given, such as:
            Font("Arial,40)
            Font("Arial,35,italic")
        
        Always include the font size.
        """
        if isinstance(font,opt) : return font
        return opt(",Font=\"{}\",".format(font))
    def labelfont(font)          :
        """
        Sets the label font.  If a number is used, it sets the font to the font size in the default font.
        Otherwise, specific fonts may be given, such as:
            labelfont("Arial,40)
            labelfont("Arial,35,italic")
        
        Always include the font size.
        """
        if isinstance(font,opt) : return font
        return opt(",LabelFont=\"{}\",".format(font))
    def title(title)        :
        "Sets the title of the control or window being created."
        if isinstance(title,opt) : return title                                 # return width as itself it is already an option
        if not isinstance(title,str) : return
        return opt(",Title=\"{}\",".format(title))

    def label(label)        :
        "Sets the label of the control or window being created."
        if isinstance(label,opt) : return label                                 # return width as itself it is already an option
        if not isinstance(label,str) : return
        return opt(",Label=\"{}\",".format(label))
    def label_right(label)        :
        "--comment--"
        if isinstance(label,opt) : return label                                 # return width as itself it is already an option
        if not isinstance(label,str) : return
        return opt(",LabelRight=\"{}\",".format(label))
    def label_left(label)        :
        "--comment--"
        if isinstance(label,opt) : return label                                 # return width as itself it is already an option
        if not isinstance(label,str) : return
        return opt(",LabelLeft=\"{}\",".format(label))
    def label_top(label)        :
        "--comment--"
        if isinstance(label,opt) : return label                                 # return width as itself it is already an option
        if not isinstance(label,str) : return
        return opt(",LabelTop=\"{}\",".format(label))
    def label_bottom(label)        :
        "--comment--"
        if isinstance(label,opt) : return label                                 # return width as itself it is already an option
        if not isinstance(label,str) : return
        return opt(",LabelBottom=\"{}\",".format(label))
    def label_color(color)    :
        "Sets the foreground or text color of a label of a control"
        return opt(",LabelColor={},".format(color))
    def horz()        :
        "Sets the title of the control or window being created."
        "--comment--"
        return opt(",Horz,")

    def textcenter_x()   :
        "--comment--"
        return opt(",TextCenterX,")
    def textcenter()   :
        "--comment--"
        return opt(",TextCenterX,")
    def textcenter_y()   :
        "--comment--"
        return opt(",TextCenteYX,")
    def just_bottom_center() :
        "--comment--"
        return opt(",JustBottomCenter,")
    def just_bottom_left() :
        "--comment--"
        return opt(",JustBottomLeft,")
    def just_bottom_right() :
        "--comment--"
        return opt(",JustBottomRight,")
    def just_top_center() :
        "--comment--"
        return opt(",JustTopCenter,")
    def just_top_left() :
        "--comment--"
        return opt(",JustTopLeft,")
    def just_top_right() :      
        "--comment--"
        return opt(",JustTopRight,")
    def center_x()   :
        "--comment--"
        return opt(",CenterX,")
    def center_y()   :
        "--comment--"
        return opt(",CenterY,")
    def center_xy()          :
        "Sets the text or control being created in the center of the Window."
        return opt(",CenterXY,")
    def multiline()          :
        "Sets an input box to accept multiple lines."
        return opt(",MultiLine,")
    def password()          :
        "Sets an input box to display '*' for all text."
        return opt(",Password,")
    def readonly()          :
        "Sets an input box to be read only text."
        return opt(",ReadOnly,")
    def wantreturn()          :
        "Tells a multi-line input box to send a 'Pressed Return' message when the return key is pressed.  Otherwise, returns are accepted as input into the input box."
        return opt(",WantReturn,")
    def noautoupdate()   :
        "--comment--"
        return opt(",NoAutoUpdate,")
    def noresize()   :
        "--comment--"
        return opt(",NoResize,")
    def sageicon()   :
        "--comment--"
        return opt(",SageIcon=0,")
    def __as_float() :
        "Sets a slider as a floating-point slider.   Internal use."
        return opt(",AsFloat,")

    def wait_for_close() :
        """
        Tells a windowed function (such as img_view()) to not return until the user closes the window.

        This allows the function to pause until completed.

        For example:
            
            img_view(my_image)      - this will display the image and return immediately
            img_view(my_image,opt.wait_for_close())     - this will wait for the user to close the window
            img_view(my_image,wait_for_close=True))   - this is the same thing using keyword format
        """
        return opt(",wait_for_close,")

    def realtime()   :
        """
        When creating a Window with NewWindow() the "RealTime" option sets the window for real-time display usage, typically
        on the Vertical Resync. 

        This sets the high-resolution timer and other factors to help the display run as fast and smooth as possible.

        Also see DirectDraw(), which sets the same values and also draws directly to the window rather than a buffer.

        - This will set auto updates off.  Update() must be used manually to update the window.
        - This does not need to be used with the vertical resync.  However, see pybox.VSyncWait() for more information
        - This is prelminary and will also work with GPU functions and components of Sagebox & Pybox when ready.

        """
        return opt(",RealTime,")
    def direct_draw()   :
        """
        When creating a Window with NewWindow() the "DirectDraw" option sets the window for direction, real-time display usage, typically
        on the Vertical Resync. 

        About Direct Draw

        - Direct Draw will draw directly to the screen instead of a buffer.  Default usage (i.e. without DirectDraw)
            \t -is to write to a separate bitmap and then send the bitmap to the window when an update occurs.
        - With Direct Draw On, output to the window will be written to the window immediately.  This can be faster and
            \t -work better with real-time display. 

        This sets the high-resolution timer and other factors to help the display run as fast and smooth as possible.

        Also see DirectDraw(), which sets the same values and also draws directly to the window rather than a buffer.

        Other notes:

        - All output will immediately display to the window.
        - The Window will not repaint when the system sends a PAINT event.  This must be taken care of by the program
            \t -However, typicaly usage is real-time, so PAINT events shouldn't matter, as the window is continuously updating.
        - This will set auto updates off, since output is now directly written to the window immediately.
        - This does not need to be used with the vertical resync.  However, see pybox.VSyncWait() for more information
        - This is prelminary and will also work with GPU functions and components of Sagebox & Pybox when ready.

        """
        return opt(",DirectDraw,")
    def resizeok()   :
        "--comment--"
        return opt(",ResizeOK,")
    def numbersonly(numbersonly : bool = True)          :
        "Tells an input box control to only accept numbers."
        if numbersonly : return opt(f",NumbersOnly,")


    def border()          :
        "Sets a border for a control such as an Input box, Listbox, etc."
        return opt(",Border,")
    def noborder()          :
        "Turns off a border for a control with a default border, such as an Input box or Listbox so it will blend into the window more seamlessly."
        return opt(",NoBorder,")
    def thickborder()          :
        "Sets a thicker border for controls such as Input Boxes, List Boxes, etc."
        return opt(",ThickBorder,")
    def recessed()          :
        "Sets a Recessed border for controls such as Input Boxes, List Boxes, etc.  This is the same as RecessedBorder()."
        return opt(",Recessed,")
    def recessedborder()          :
        "Sets a Recessed border for controls such as Input Boxes, List Boxes, etc.  This is the same as Recessed()."
        return opt(",Recessed,")
    def vscroll()          :
        "Adds a vertical scroll bar on controls such as Input Boxes and List Boxes"
        return opt(",VScroll,")
    def hscroll()          :
        "Adds a horizontal Control for controls such as Input Boxes and List Boxes"
        return opt(",HScroll,")
    def wincolors() :
        """
        Sets colors for a control to either use the current window color for background and text colors, or to use brigher 'Windows-default colors. 
        This is dependent on the control.  See the documentation for specific controls.
        """
        return opt(",WinColors,")

    def iconinfo()          :
        "--comment--"
        return opt(",IconInfo,")
    def iconstop()          :
        "--comment--"
        return opt(",IconStop,")
    def iconwarning()          :
        "--comment--"
        return opt(",IconWarning,")

    def str(litstr) :
        "--comment--"
        if (isinstance(litstr,str)) : return opt(",{},".format(litstr))      # Convert to option
        if (isinstance(litstr,opt)) : return litstr                        # Return as is
        return                                                              # do nothing 
    def str_str(string,definition) :
        "--comment--"
        if not isinstance(string,str) or not isinstance(definition,str) : return
        if isinstance(string,opt) : return string
        return opt(",{}=\"{}\",".format(string,definition))


    def range(_min,_max=None)      :
        "Sets the range of a control, such as a slider."
        if isinstance(_min,opt) : return _min                                 # return min as itself it is already an option
        if isinstance(_min,list) or isinstance(_min,tuple) :
            return opt(",MinValue={},MaxValue={},".format(_min[0],_min[1]))    # list or tuple
        if isinstance(_min,numpy.ndarray) and _min.ndim >= 1 and _min.shape[0] >= 2 : # min is an array
            return opt(",MinValue={},MaxValue={},".format(_min[0],_min[1]))
        return opt(",MinValue={},MaxValue={},".format(_min,_max))
    def default(default)    :
        "Sets the default value for a control or widget.  i.e. Default(true), in the case of on/off, or Default(<value>), etc."      
        if isinstance(default,opt) : return default         # return default as itself it is already an option
        if isinstance(default,str) : return opt(",Default=\"{}\",".format(default)) 
        if default is not None : return opt(",Default={},".format(default))
    def percent(percent)    :
        "--comment--"
        if isinstance(percent,opt) : return percent
        if percent is not None : return opt(",Percent={},".format(int(percent)))

    def padx(pad)    :
        "--comment--"
        if isinstance(pad,opt) : return pad
        if pad is not None : return opt(",PadX={},".format(int(pad)))
    def pady(pad)    :
        "--comment--"
        if isinstance(pad,opt) : return pad
        if pad is not None : return opt(",PadY={},".format(int(pad)))
    def zoombox(zoomBox : bool = True)    :
        "--comment--"
        if zoomBox is None : return
        if isinstance(zoomBox,opt) : return zoomBox
        return opt(",ZoomBox={},".format(zoomBox))

    def cb_titlecell(titlecell : str)    :
        "--comment--"
        if titlecell is None : return
        if isinstance(titlecell,opt) : return titlecell
        return opt(f",cbTitleCell=\"{titlecell}\"")

    def style(style : str)    :
        "--comment--"
        if style is None : return
        if isinstance(style,opt) : return style
        return opt(f",Style=\"{style}\"")
    def arrowbox(arrowbox : bool = True) :
        "--comment--"
        return opt(f",ArrowBox={arrowbox}")
    def reversed(reversed : bool = True)    :
        "--comment--"
        if reversed is None : return
        if isinstance(reversed,opt) : return reversed
        return opt(",Reversed={},".format(reversed))
    def reverse(reversed : bool = True)    :
        "--comment--"
        if reversed is None : return
        if isinstance(reversed,opt) : return reversed
        return opt(",Reversed={},".format(reversed))
    def noblanks(noblanks : bool = True)    :
        "--comment--"
        if noblanks is None : return
        if isinstance(noblanks,opt) : return noblanks
        return opt(",noblanks={},".format(noblanks))
    def nocancel(nocancel : bool = True)    :
        "--comment--"
        if nocancel is None : return
        if isinstance(nocancel,opt) : return nocancel
        return opt(",nocancel={},".format(nocancel))
    def cancelok(cancelok : bool = True)    :
        "--comment--"
        if cancelok is None : return
        if isinstance(cancelok,opt) : return cancelok
        return opt(",CancelOk={},".format(cancelok))
    def progresbar(progressbar : bool = True)    :
        "--comment--"
        if progressbar is None : return
        if isinstance(progressbar,opt) : return progressbar
        return opt(",ProgressBar={},".format(progressbar))
    def maximize(maximize : bool = True)    :
        "--comment--"
        if maximize is None : return
        if isinstance(maximize,opt) : return maximize
        return opt(",Maximize={},".format(maximize))

    def size(width = None,height : int = None)  :
        """
        Set size of a control or window.

        Input:

        width,height\t\t -- Width & Height (both must be integers)
        list\t\t -- Use a list with 2 values as width,height
        tuple\t -- Use a tuple as 2 values as width,height

        Examples: 

        opt.size(10,100)\t -- Set 10,100 as size

        size=(10,100)
        opt.size(size)\t -- Set tuple loc as size (i.e. 10x100)
        """
        if isinstance(width,opt) : return width                                 # return width as itself it is already an option
        if isinstance(width,list) or isinstance(width,tuple) or isinstance(width,numpy.ndarray):
            return opt(",SizeX={},SizeY={},".format(int(width[0]),int(width[1])))         # list or tuple

        if height is None : height = 0
        if width is not None :                   # width & height are integers
            return opt(",SizeX={},SizeY={},".format(int(width),int(height)))
        return                                                      # if all fails, pass through and do nothing
    def at(x = None,y : int = None)  :                              # convert various types to option format
        """
        Set (X,Y) location of a control or window.

        Input:

        x,y\t\t -- X,Y location (both must be integers)
        list\t\t -- Use a list with 2 values as X,Y
        tuple\t -- Use a tuple as 2 values as X,Y

        Examples: 

        opt.at(10,100)\t -- Set 10,100 as location

        loc=(10,100)
        opt.at(loc)\t -- Set tuple loc as location (i.e. 10,100)
        """
        if isinstance(x,opt) : return x                             # return x as itself it is already an option
        if isinstance(x,list) or isinstance(x,tuple) :
            return opt(",LocX={},LocY={},".format(x[0],x[1]))        # list or tuple
        if isinstance(x,int) and isinstance(y,int) :                # x & y are integers
            return opt(",LocX={},LocY={},".format(x,y))
        if isinstance(x,float) and isinstance(y,float) :            # x & y are float
            return opt(",LocX={},LocY={},".format(x,y))
        if isinstance(x,numpy.ndarray) and x.ndim >= 1 and x.shape[0] >= 2 : # x is an array
            return opt(",LocX={},LocY={},".format(x[0],x[1]))
        return                                                      # if all fails, pass through and do nothing
    def hide() :
        return opt(",Hide,")
    def best_fit(width,height) :
        "--comment--"
        return opt(",FitWidth={},FitHeight={},".format(width,height))
    def best_fit_exact(width,height) :
        "--comment--"
        return opt(",FitExact,FitWidth={},FitHeight={},".format(width,height))
    def width(width) :
        "--comment--"
        return opt(",SizeX={},".format(width))
    def height(height) :
        "--comment--"
        return opt(",SizeY={},".format(height))
    def fullscreen() :
        "--comment--"
        return opt(",Fullscreen,")
    def popup() :
        "--comment--"
        return opt(",Popup,")
    def normalized() : 
        """
        When displaying bitmaps in img_view() and img_before_after(), this will let the functions know that
        a floating-point-based image is normalized to 0-1.0

        Otherwise the image is assumed to have values between 0.0-255.0
        """
        return opt(",Normalized,")
    def noerror() :
        """
        Tells a function to not print errors and stop the program. 
        The program than can check if the function succeeded.

        For example, when reading a bitmap with read_image_file, the default
        behavior is to stop the program if the bitmap did not exist or otherwis
        did not load.

        using "noerror" will cause the function to continue, and the returns bitmap can be
        checked for an error, such as

        my_image = read_image_file("test.jpg",'noerror')

        if my_image.is_empty() : 
                << handle error case here >>
        """
        return opt(",NoError,")

class PanColor :
    def AliceBlue            () -> RgbColor : return RgbColor(0xF0,0xF8,0xFF)
    def AntiqueWhite         () -> RgbColor : return RgbColor(0xFA,0xEB,0xD7)
    def Aqua                 () -> RgbColor : return RgbColor(0x00,0xFF,0xFF)
    def Aquamarine           () -> RgbColor : return RgbColor(0x7F,0xFF,0xD4)
    def Azure                () -> RgbColor : return RgbColor(0xF0,0xFF,0xFF)
    def Beige                () -> RgbColor : return RgbColor(0xF5,0xF5,0xDC)
    def Bisque               () -> RgbColor : return RgbColor(0xFF,0xE4,0xC4)
    def Black                () -> RgbColor : return RgbColor(0x00,0x00,0x00)
    def BlanchedAlmond       () -> RgbColor : return RgbColor(0xFF,0xEB,0xCD)
    def Blue                 () -> RgbColor : return RgbColor(0x00,0x00,0xFF)
    def BlueViolet           () -> RgbColor : return RgbColor(0x8A,0x2B,0xE2)
    def Brown                () -> RgbColor : return RgbColor(0xA5,0x2A,0x2A)
    def BurlyWood            () -> RgbColor : return RgbColor(0xDE,0xB8,0x87)
    def CadetBlue            () -> RgbColor : return RgbColor(0x5F,0x9E,0xA0)
    def Chartreuse           () -> RgbColor : return RgbColor(0x7F,0xFF,0x00)
    def Chocolate            () -> RgbColor : return RgbColor(0xD2,0x69,0x1E)
    def Coral                () -> RgbColor : return RgbColor(0xFF,0x7F,0x50)
    def CornflowerBlue       () -> RgbColor : return RgbColor(0x64,0x95,0xED)
    def Cornsilk             () -> RgbColor : return RgbColor(0xFF,0xF8,0xDC)
    def Crimson              () -> RgbColor : return RgbColor(0xDC,0x14,0x3C)
    def Cyan                 () -> RgbColor : return RgbColor(0x00,0xFF,0xFF)
    def DarkBlue             () -> RgbColor : return RgbColor(0x00,0x00,0x8B)
    def DarkCyan             () -> RgbColor : return RgbColor(0x00,0x8B,0x8B)
    def DarkGoldenrod        () -> RgbColor : return RgbColor(0xB8,0x86,0x0B)
    def DarkGray             () -> RgbColor : return RgbColor(0xA9,0xA9,0xA9)
    def DarkGreen            () -> RgbColor : return RgbColor(0x00,0x64,0x00)
    def DarkKhaki            () -> RgbColor : return RgbColor(0xBD,0xB7,0x6B)
    def DarkMagenta          () -> RgbColor : return RgbColor(0x8B,0x00,0x8B)
    def DarkOliveGreen       () -> RgbColor : return RgbColor(0x55,0x6B,0x2F)
    def DarkOrange           () -> RgbColor : return RgbColor(0xFF,0x8C,0x00)
    def DarkOrchid           () -> RgbColor : return RgbColor(0x99,0x32,0xCC)
    def DarkRed              () -> RgbColor : return RgbColor(0x8B,0x00,0x00)
    def DarkSalmon           () -> RgbColor : return RgbColor(0xE9,0x96,0x7A)
    def DarkSeaGreen         () -> RgbColor : return RgbColor(0x8F,0xBC,0x8B)
    def DarkSlateBlue        () -> RgbColor : return RgbColor(0x48,0x3D,0x8B)
    def DarkSlateGray        () -> RgbColor : return RgbColor(0x2F,0x4F,0x4F)
    def DarkTurquoise        () -> RgbColor : return RgbColor(0x00,0xCE,0xD1)
    def DarkViolet           () -> RgbColor : return RgbColor(0x94,0x00,0xD3)
    def DeepPink             () -> RgbColor : return RgbColor(0xFF,0x14,0x93)
    def DeepSkyBlue          () -> RgbColor : return RgbColor(0x00,0xBF,0xFF)
    def DimGray              () -> RgbColor : return RgbColor(0x69,0x69,0x69)
    def DodgerBlue           () -> RgbColor : return RgbColor(0x1E,0x90,0xFF)
    def Firebrick            () -> RgbColor : return RgbColor(0xB2,0x22,0x22)
    def FloralWhite          () -> RgbColor : return RgbColor(0xFF,0xFA,0xF0)
    def ForestGreen          () -> RgbColor : return RgbColor(0x22,0x8B,0x22)
    def Fuchsia              () -> RgbColor : return RgbColor(0xFF,0x00,0xFF)
    def Gainsboro            () -> RgbColor : return RgbColor(0xDC,0xDC,0xDC)
    def GhostWhite           () -> RgbColor : return RgbColor(0xF8,0xF8,0xFF)
    def Gold                 () -> RgbColor : return RgbColor(0xFF,0xD7,0x00)
    def Goldenrod            () -> RgbColor : return RgbColor(0xDA,0xA5,0x20)
    def Gray                 () -> RgbColor : return RgbColor(0x80,0x80,0x80)
    def Green                () -> RgbColor : return RgbColor(0x00,0x80,0x00)
    def GreenYellow          () -> RgbColor : return RgbColor(0xAD,0xFF,0x2F)
    def Honeydew             () -> RgbColor : return RgbColor(0xF0,0xFF,0xF0)
    def HotPink              () -> RgbColor : return RgbColor(0xFF,0x69,0xB4)
    def IndianRed            () -> RgbColor : return RgbColor(0xCD,0x5C,0x5C)
    def Indigo               () -> RgbColor : return RgbColor(0x4B,0x00,0x82)
    def Ivory                () -> RgbColor : return RgbColor(0xFF,0xFF,0xF0)
    def Khaki                () -> RgbColor : return RgbColor(0xF0,0xE6,0x8C)
    def Lavender             () -> RgbColor : return RgbColor(0xE6,0xE6,0xFA)
    def LavenderBlush        () -> RgbColor : return RgbColor(0xFF,0xF0,0xF5)
    def LawnGreen            () -> RgbColor : return RgbColor(0x7C,0xFC,0x00)
    def LemonChiffon         () -> RgbColor : return RgbColor(0xFF,0xFA,0xCD)
    def LightBlue            () -> RgbColor : return RgbColor(0xAD,0xD8,0xE6)
    def LightCoral           () -> RgbColor : return RgbColor(0xF0,0x80,0x80)
    def LightCyan            () -> RgbColor : return RgbColor(0xE0,0xFF,0xFF)
    def LightGoldenrodYellow () -> RgbColor : return RgbColor(0xFA,0xFA,0xD2)
    def LightGray            () -> RgbColor : return RgbColor(0xD3,0xD3,0xD3)
    def LightGreen           () -> RgbColor : return RgbColor(0x90,0xEE,0x90)
    def LightPink            () -> RgbColor : return RgbColor(0xFF,0xB6,0xC1)
    def LightSalmon          () -> RgbColor : return RgbColor(0xFF,0xA0,0x7A)
    def LightSeaGreen        () -> RgbColor : return RgbColor(0x20,0xB2,0xAA)
    def LightSkyBlue         () -> RgbColor : return RgbColor(0x87,0xCE,0xFA)
    def LightSlateGray       () -> RgbColor : return RgbColor(0x77,0x88,0x99)
    def LightSteelBlue       () -> RgbColor : return RgbColor(0xB0,0xC4,0xDE)
    def LightYellow          () -> RgbColor : return RgbColor(0xFF,0xFF,0xE0)
    def Lime                 () -> RgbColor : return RgbColor(0x00,0xFF,0x00)
    def LimeGreen            () -> RgbColor : return RgbColor(0x32,0xCD,0x32)
    def Linen                () -> RgbColor : return RgbColor(0xFA,0xF0,0xE6)
    def Magenta              () -> RgbColor : return RgbColor(0xFF,0x00,0xFF)
    def Maroon               () -> RgbColor : return RgbColor(0x80,0x00,0x00)
    def MediumAquamarine     () -> RgbColor : return RgbColor(0x66,0xCD,0xAA)
    def MediumBlue           () -> RgbColor : return RgbColor(0x00,0x00,0xCD)
    def MediumOrchid         () -> RgbColor : return RgbColor(0xBA,0x55,0xD3)
    def MediumPurple         () -> RgbColor : return RgbColor(0x93,0x70,0xDB)
    def MediumSeaGreen       () -> RgbColor : return RgbColor(0x3C,0xB3,0x71)
    def MediumSlateBlue      () -> RgbColor : return RgbColor(0x7B,0x68,0xEE)
    def MediumSpringGreen    () -> RgbColor : return RgbColor(0x00,0xFA,0x9A)
    def MediumTurquoise      () -> RgbColor : return RgbColor(0x48,0xD1,0xCC)
    def MediumVioletRed      () -> RgbColor : return RgbColor(0xC7,0x15,0x85)
    def MidnightBlue         () -> RgbColor : return RgbColor(0x19,0x19,0x70)
    def MintCream            () -> RgbColor : return RgbColor(0xF5,0xFF,0xFA)
    def MistyRose            () -> RgbColor : return RgbColor(0xFF,0xE4,0xE1)
    def Moccasin             () -> RgbColor : return RgbColor(0xFF,0xE4,0xB5)
    def NavajoWhite          () -> RgbColor : return RgbColor(0xFF,0xDE,0xAD)
    def Navy                 () -> RgbColor : return RgbColor(0x00,0x00,0x80)
    def OldLace              () -> RgbColor : return RgbColor(0xFD,0xF5,0xE6)
    def Olive                () -> RgbColor : return RgbColor(0x80,0x80,0x00)
    def OliveDrab            () -> RgbColor : return RgbColor(0x6B,0x8E,0x23)
    def Orange               () -> RgbColor : return RgbColor(0xFF,0xA5,0x00)
    def OrangeRed            () -> RgbColor : return RgbColor(0xFF,0x45,0x00)
    def Orchid               () -> RgbColor : return RgbColor(0xDA,0x70,0xD6)
    def PaleGoldenrod        () -> RgbColor : return RgbColor(0xEE,0xE8,0xAA)
    def PaleGreen            () -> RgbColor : return RgbColor(0x98,0xFB,0x98)
    def PaleTurquoise        () -> RgbColor : return RgbColor(0xAF,0xEE,0xEE)
    def PaleVioletRed        () -> RgbColor : return RgbColor(0xDB,0x70,0x93)
    def PapayaWhip           () -> RgbColor : return RgbColor(0xFF,0xEF,0xD5)
    def PeachPuff            () -> RgbColor : return RgbColor(0xFF,0xDA,0xB9)
    def Peru                 () -> RgbColor : return RgbColor(0xCD,0x85,0x3F)
    def Pink                 () -> RgbColor : return RgbColor(0xFF,0xC0,0xCB)
    def Plum                 () -> RgbColor : return RgbColor(0xDD,0xA0,0xDD)
    def PowderBlue           () -> RgbColor : return RgbColor(0xB0,0xE0,0xE6)
    def Purple               () -> RgbColor : return RgbColor(0x80,0x00,0x80)
    def Red                  () -> RgbColor : return RgbColor(0xFF,0x00,0x00)
    def RosyBrown            () -> RgbColor : return RgbColor(0xBC,0x8F,0x8F)
    def RoyalBlue            () -> RgbColor : return RgbColor(0x41,0x69,0xE1)
    def SaddleBrown          () -> RgbColor : return RgbColor(0x8B,0x45,0x13)
    def Salmon               () -> RgbColor : return RgbColor(0xFA,0x80,0x72)
    def SandyBrown           () -> RgbColor : return RgbColor(0xF4,0xA4,0x60)
    def SeaGreen             () -> RgbColor : return RgbColor(0x2E,0x8B,0x57)
    def SeaShell             () -> RgbColor : return RgbColor(0xFF,0xF5,0xEE)
    def Sienna               () -> RgbColor : return RgbColor(0xA0,0x52,0x2D)
    def Silver               () -> RgbColor : return RgbColor(0xC0,0xC0,0xC0)
    def SkyBlue              () -> RgbColor : return RgbColor(0x87,0xCE,0xEB)
    def SlateBlue            () -> RgbColor : return RgbColor(0x6A,0x5A,0xCD)
    def SlateGray            () -> RgbColor : return RgbColor(0x70,0x80,0x90)
    def Snow                 () -> RgbColor : return RgbColor(0xFF,0xFA,0xFA)
    def SpringGreen          () -> RgbColor : return RgbColor(0x00,0xFF,0x7F)
    def SteelBlue            () -> RgbColor : return RgbColor(0x46,0x82,0xB4)
    def Tan                  () -> RgbColor : return RgbColor(0xD2,0xB4,0x8C)
    def Teal                 () -> RgbColor : return RgbColor(0x00,0x80,0x80)
    def Thistle              () -> RgbColor : return RgbColor(0xD8,0xBF,0xD8)
    def Tomato               () -> RgbColor : return RgbColor(0xFF,0x63,0x47)
    def Turquoise            () -> RgbColor : return RgbColor(0x40,0xE0,0xD0)
    def Violet               () -> RgbColor : return RgbColor(0xEE,0x82,0xEE)
    def Wheat                () -> RgbColor : return RgbColor(0xF5,0xDE,0xB3)
    def White                () -> RgbColor : return RgbColor(0xFF,0xFF,0xFF)
    def WhiteSmoke           () -> RgbColor : return RgbColor(0xF5,0xF5,0xF5)
    def Yellow               () -> RgbColor : return RgbColor(0xFF,0xFF,0x00)
    def YellowGreen          () -> RgbColor : return RgbColor(0x9A,0xCD,0x32)

class SageColor :
    def DefaultBgColor                  () -> RgbColor : return RgbColor(20,40,121)
    def DefaultFgColor                  () -> RgbColor : return RgbColor(255,255,255)
    def SliderTextColor                 () -> RgbColor : return RgbColor(128,128,128)
    def Green                           () -> RgbColor : return RgbColor(0,255,0)
    def DarkGreen                       () -> RgbColor : return RgbColor(0,128,0)
    def LightGreen                      () -> RgbColor : return RgbColor(128,255,128)
    def Blue                            () -> RgbColor : return RgbColor(0,0,255)
    def DarkBlue                        () -> RgbColor : return RgbColor(0,0,92)
    def MidBlue                         () -> RgbColor : return RgbColor(0,0,128)
    def LightBlue                       () -> RgbColor : return RgbColor(128,128,255)
    def SkyBlue                         () -> RgbColor : return RgbColor(40,145,255)
    def SkyBlueDark                     () -> RgbColor : return RgbColor(0,30,128)
    def SkyBlueLight                    () -> RgbColor : return RgbColor(75,165,255)
    def Cyan                            () -> RgbColor : return RgbColor(0,255,255) 
    def Red                             () -> RgbColor : return RgbColor(255,0,0)
    def LightRed                        () -> RgbColor : return RgbColor(255,128,128)
    def LightYellow                     () -> RgbColor : return RgbColor(255,255,128)
    def Yellow                          () -> RgbColor : return RgbColor(255,255,0)
    def Magenta                         () -> RgbColor : return RgbColor(255,0,255)
    def MediumMagenta                   () -> RgbColor : return RgbColor(255,92,255)
    def LightMagenta                    () -> RgbColor : return RgbColor(255,128,255)
    def Purple                          () -> RgbColor : return RgbColor(255,0,255)
    def LightPurple                     () -> RgbColor : return RgbColor(255,128,255)
    def MediumPurple                    () -> RgbColor : return RgbColor(255,92,255)
    def White                           () -> RgbColor : return RgbColor(255,255,255) 
    def Gray172                         () -> RgbColor : return RgbColor(172,172,172) 
    def Gray192                         () -> RgbColor : return RgbColor(192,192,192) 
    def Gray220                         () -> RgbColor : return RgbColor(220,220,220) 
    def Gray128                         () -> RgbColor : return RgbColor(128,128,128) 
    def Gray32                          () -> RgbColor : return RgbColor(32,32,32) 
    def Gray42                          () -> RgbColor : return RgbColor(42,42,42) 
    def Gray64                          () -> RgbColor : return RgbColor(64,64,64) 
    def Gray72                          () -> RgbColor : return RgbColor(72,72,72) 
    def Gray92                          () -> RgbColor : return RgbColor(92,92,92) 
    def Black                           () -> RgbColor : return RgbColor(0,0,0) 
    def LightGray                       () -> RgbColor : return RgbColor(200,200,200)
    def LightGrey                       () -> RgbColor : return RgbColor(200,200,200)
    def MidGray                         () -> RgbColor : return RgbColor(64,64,64)
    def MidGrey                         () -> RgbColor : return RgbColor(64,64,64)
    def DarkGray                        () -> RgbColor : return RgbColor(32,32,32)
    def DarkGrey                        () -> RgbColor : return RgbColor(32,32,32)
    def Gray                            () -> RgbColor : return RgbColor(128,128,128)
    def Grey                            () -> RgbColor : return RgbColor(128,128,128)
    def NearWhite                       () -> RgbColor : return RgbColor(220,220,220)
    def ButtonTextColorNormal           () -> RgbColor : return RgbColor(220,220,220)
    def ButtonTextColorHighlighted      () -> RgbColor : return RgbColor(255,255,255)
    def ButtonTextColorPressed          () -> RgbColor : return RgbColor(255,255,255)
    def ButtonTextColorDisabled         () -> RgbColor : return RgbColor(170,170,170)
    def CheckboxTextColorNormal         () -> RgbColor : return RgbColor(220,220,220)
    def CheckboxTextColorHighlighted    () -> RgbColor : return RgbColor(255,255,255)
    def CheckboxTextColorChecked        () -> RgbColor : return RgbColor(220,220,220)
    def CheckboxTextColorCheckedHigh    () -> RgbColor : return RgbColor(220,220,220)
    def CheckboxTextColorDisabled       () -> RgbColor : return RgbColor(170,170,170)

def sysConvertInt32(val) : return int(val)

__temp = numpy.array([123,123],dtype=numpy.int32)
_pybox.SysSubmitTypes(RgbColor(0,0,0),peek,__temp[0])
_pybox.SysSetEventCallback(sysConvertInt32)

if __name__ == "__main__" :
    print("Error: This is the pybox module (pybox.py) and is not meant to be run as a main program.")
    quit()
    
