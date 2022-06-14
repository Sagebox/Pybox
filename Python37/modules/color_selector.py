"""
---------------------------
Pybox Color Selector Widget
---------------------------

This is an example of a pybox widget that can be added as a separate DLL (pyd) and module.

This was written as a Sagebox C++ function and then easily transferred to Pybox with no change in the source code, 
only needing the interface code to the Python C API.

-------------------------------------------------------------------------------------------------
3rd Party Pybox Widgets for Arduino, Specific Projects, Specialize Widgets ... An Sort of Widget!
-------------------------------------------------------------------------------------------------

Widgets are a large part of Pybox and are in the process of being written.   Pybox supports writing
widgets from other code sources that can find Pybox in memory and link a widget into the current 
Pybox process.

Widgets to not need to be part of the pybox package, but can use the pybox package to become a widget. 

This allows things like this widget example or any widget you want to write.

Graphing, GPU, Utility, Controls, and many other widgets are currently being written to add to Pybox. 


------------------------
### Work In Progress ###
------------------------

Pybox was just released recently in an Alpha Stage.  Currently the widgets need to be 1:1 with the current
pybox version.  This will change soon as the DLL interfacing between external widgets and pybox is completed.

This is work in progress, so not all functions are documented and some functions may work incorrectly. 

The demos provided show how external widgets work as separate entities not directly connected to pybox. 

"""


import pybox
from pybox import opt
import numpy

import _color_selector

class ColorSelector :
  
    def __init__(self,window : pybox.Window = None,at=None,*args) :
        self.__id = _color_selector.CreateWidget(window._Window__id,opt.at(at),*args)
    def value_changed(self) -> bool :
        "--comment--"
        return _color_selector.ValueChanged(self.__id)
    def get_rgb_value(self) -> pybox.RgbColor :
        "--comment--"
        value = _color_selector.GetRGBValue(self.__id);
        return pybox.RgbColor(value[0],value[1],value[2]);
    def get_rgb_array(self) -> numpy.ndarray :
        "--comment--"
        value = _color_selector.GetRGBValue(self.__id);
        return numpy.array(value);
    def set_rgb_value(self,rgb_value) -> bool :
        "--comment--"
        return _color_selector.SetRGBValue(self.__id,rgb_value);
    def set_location(self,at = None) -> bool :
        "--comment--"
        return _color_selector.SetLocation(self.__id,opt.at(at));
    def show(self,show : bool = True) -> bool :
        "--comment--"
        return _color_selector.Show(self.__id,show);
    def hide(self,hide : bool = True) -> bool :
        "--comment--"
        return _color_selector.Hide(self.__id,hide);
    def ok_pressed(self) -> bool :
        "--comment--"
        return _color_selector.OkPressed(self.__id);
    def cancel_pressed(self) -> bool :
        "--comment--"
        return _color_selector.CancelPressed(self.__id);
    def event_active(self) -> bool :
        "--comment--"
        return _color_selector.EventActive(self.__id);

def create(window : pybox.Window = None,at=None,*args) -> ColorSelector :
    return ColorSelector(window,at,*args)

def popup(at=None,*args) -> ColorSelector :
    return ColorSelector(pybox.Window(0),at,*args)


if __name__ == "__main__" :
    print("Error: This is the Color Selector Widget module and is not meant to be run as a main program.")
    quit()
