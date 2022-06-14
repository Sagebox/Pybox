
import pybox
from pybox import opt
import numpy

import _dial_widget

class DialWidget :
  
    def __init__(self,window : pybox.Window = None,At=None,Default=None,Range=None,*args) :
        self.__id = _dial_widget.CreateWidget(window._Window__id,At,Default,Range,*args)
    def get_value(self) -> int :
        "--comment--"
        return _dial_widget.GetValue(self.__id);

    def value_changed(self) -> bool :
        "--comment--"
        return _dial_widget.ValueChanged(self.__id);

    def set_value(self,value) -> bool :
        "---"
        return _dial_widget.SetValue(self.__id,value)

    def set_location(self,at) -> bool :
        "---"
        return _dial_widget.SetLocation(self.__id,opt.at(at))

    def get_location(self) -> numpy.ndarray :
        "---"
        return  numpy.array(_dial_widget.GetWinLocation(self.__id))
    def get_window_size(self) -> numpy.ndarray :
        "---"
        return numpy.array(_dial_widget.GetWindowSize(self.__id))
    def set_range(self,range) :
        "--comment--"
        return _dial_widget.SetRange(self.__id,opt.range(range)) # must be pybox option or some error

def create(window : pybox.Window,at=None,range=None,default=None,*args) -> DialWidget :
    return DialWidget(window,opt.at(at),opt.default(default),opt.range(range),*args)

if __name__ == "__main__" :
    print("Error: This is the Dial Widget module and is not meant to be run as a main program.")
    quit()