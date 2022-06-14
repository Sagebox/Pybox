import pybox;
from pybox import opt
import _lcd_widget

class LcdWidget :
    """
    Creates an LCDWidget in a window or as a popup window if not window is provided

    LcdWidget(window : pybox.Window = None,At=None,*args)

    Window\t - pybox Window to place LCD widget.  When None, a new popup window is created.
    At\t\t - Location of LCD widget in pybox Window (or where to put new window on screen when no pybox window is specified)
    *args\t\t - additional pybox options, such as opt.Default(1234) or opt.Title("LCD Emulation Widget")
    
    --> Note: opt.Title() only works when creating a new window (i.e. not specifying an existing window)
    --> For titling when creating a new window, use "+" as a first line to set the window title, such as: 
    \topt.Title("+Window Title\\nLCD Emulation Widget") to set the window's titlebar title  in addition to displayed text.

    Examples:

    MyWidget = LcdWidget() - (pops up in new window)
    MyWidget = LcdWidget(At=(100,200),opt.Title("LCD Widget"),opt.Default(1234)) - (pops up in new window)
    MyWidget = LcdWidget(MyWindow,At=(100,200) - (places Widget in MyWindow pybox window)

    """
    def __init__(self,window : pybox.Window = None,at=None,*args) :
        """
        LcdWidget(window : pybox.Window = None,At=None,*args)

        Hover mouse over LcdWidget for more details
        """
        self.__id = _lcd_widget.CreateWidget(window,opt.at(at),*args)

    def set_value(self,value : int) -> bool :
        "Set the LCD value.  Negative numbers also work."
        return _lcd_widget.SetValue(self.__id,value)

    def get_value(self) -> int :
        "Get the current value of the LCD Display"
        return _lcd_widget.GetValue(self.__id)

    def set_fast_mode(self,fast_mode : bool) -> bool :
        """
        Set a much faster mode where the LCD only updates every 10ms or so.
        When off (default), the LCD is updated and redisplated on every call

        Using Fast Mode can reflect more accurate realtime information, using much less time for updating.

        See update_last() -- this must be used as one more updated when finished.
        Use set_fast_mode(False) to turn off Fast Mode
        """
        return _lcd_widget.SetFastMode(self.__id,fast_mode)

    def show(self,show : bool = True) -> bool :
        "Show the LCD Display Window (if it is hidden)"
        return _lcd_widget.Show(self.__id,show)

    def hide(self,hide : bool = True) -> bool :
        "Hides the LCD display window, removing it from the screen (it is still active, but hidden). See Show()"
        return _lcd_widget.Hide(self.__id,hide)

    def update_laset(self) -> bool :
        """
        Updates the LCD immediately.  This is used for SetFastMode(), which updates every 10 ms or so, and may miss the last update.
        Use UpdateLast() to make sure the last output is updated (i.e. at the end of a loop). 
        """
        return _lcd_widget.UpdateLast(self.__id)

    def get_window_size(self) -> list :
        "Get the size of the LCD Display Window.  Returns a list with two elements, (Width, Height)."
        return _lcd_widget.GetWindowSize(self.__id)

    def get_win_location(self) -> list :
        "Get the location of the LCD Display (or the entire window if it was created as a new window).  Returns a list with to elements, (X,Y)."
        return _lcd_widget.GetWinLocation(self.__id)

    def set_led_mode(self,led_mode : bool = True) -> bool :
        "Sets an LED mode with a blue BLUE LED instead of a basic LCD Display.  Use SetLedMode(False) to go back to the LCD mode."
        return _lcd_widget.SetLedMode(self.__id,led_mode)

    def allow_drag(self,allow_drag : bool = True) -> bool :
        "Allows the window be dragged around with the mouse inside of the window.  Use AllowDrag(False) to disable  (the default is False)"
        return _lcd_widget.AllowDrag(self.__id,allow_drag)

    def update_bg(self) -> bool :
        "Updates the background behind the LCD Display Window.  If the window contents change, UpdateBg() will update the transparent areas of the LCD Display Widget."
        return _lcd_widget.UpdateBg(self.__id)

    def set_win_location(self,*args) :
        """
        Sets the location of the LCD Display, either inside of the window it is placed within or the overall window if it was created as a popup window

        Forms: 

        set_win_location(x,y) - Integer pair
        set_win_location(tuple) - a tuple, such as "(x,y)", i.e. myTyuple = (100,5)
        set_win_location(list) - a list, such as "(x,y)"
        set_win_location(opt.At(x,y)) - pybox option format  (opt.At can also use tuples and lists)
        """
        return _lcd_widget.set_win_location(self.__id,*args)

    def close_event(self) -> int :
        "Returns true of the Window was closed by the user (when the LCD Widget launched its own window)."
        return _lcd_widget.WindowClosed(self.__id)

    def __del__(self):
        return _lcd_widget.Delete(self.__id)


def create(window : pybox.Window = None,at=None,opts = None,*args) -> LcdWidget :
    return LcdWidget(window,at,opt.str(opts),*args)

def popup(at=None,opts = None,*args) -> LcdWidget :
    return LcdWidget(at,opt.str(opts),*args)
