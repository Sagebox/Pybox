# About Pybox Examples

The examples in different Python directories are exactly the same, the only difference being
the project setups.

## Operating Platforms

The current Pybox Beta release works on Windows platforms, and should work with any Python
platform that supports Python 3.7-3.12

The examples have workspaces and projects in each directory oriented around VS Code and
Visual Studio. 

## Python Directories in GitHub and using `pip install pybox-gui`

### Using `pip install pybox-gui` and the examples

For Python 3.9 or greater, you can use use any of the examples in the Github Python39-312 directories. 
The separate example directories are only to support downloading the Pybox module outside of using `pip install`

> note: Python 3.7 has some code differences.  For Python 3.7, use the examples in the Python37 directory specifically.


### Using Python37-Python312 directories for local downloads (outside of `pip install`)

Now that the Pybox project is checked in with PyPI and can be installed through pip as `pybox-gui`, these directories will probably be turned into a single `examples` directory, with a separate `examples37` directory for Python 3.7. 

These directories exist to provide an easy way to use <i>VsCode</i> and <i>Visual Studio</i> with any Python version supported, using relative paths to th
.pyd files.  As mentioned, with `pip install`, this is no longer needed and any examples from Python39-Python312 directores will work (unless using Python 3.7, in which case the Python37 directory examples should be used)

## VS Code 

All example directories have a workspace for VS Code.   You can choose the python version with 
VS Code (via the "Command Palette: Python: Select Interpreter" command, which will list the 
versions of Python on your system.

## Visual Studio 2019

Visual Studio solutions have the Python environment for that example pre-selected.  For example, 
examples in the Python39 directory structure have Python 3.9 selected as the Python environment. 

Make sure the directory coincides with a python version installed on your system.

## Visual Studio 2022

Visual Studio 2022 works the same as 2019, but it does not work with the intellisense for modules 
that are not in the environment path. 

For external modules set in the Python path for the project, the intellisense will state that 
there is an error and fail to find the pybox module (or any external module) and show the 
documentation for each function when the cursor is moved over the function text. 

Until resolved, it is suggested to use VS Code or Visual Studio 2019.

## SciPy, MatplotLib, OpenCV

Most examples only use the Pybox module.  Some also use SciPy, MatplotLib, or Open CV. 

These may need to be installed to run some of the example programs. 
