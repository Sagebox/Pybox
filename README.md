

<h1 align="center">Pybox for Python</h1>


<p align="center">
    <img src="https://user-images.githubusercontent.com/70604831/174466253-c4310d66-c687-4864-9893-8f0f70dd4084.png">
</p>

<h2 align="center">
  Non-Event-Driven GUI-based tools for Python
</h2>



Pybox is a set of GUI-based tools to help you add GUI components to your program, all without adding a lot of event-driven or GUI-specific code just to have
graphics and controls in your program.  
<br />
Pybox is useful for adding onto current packages and other UIs such as MatplotLib, Tkinter, SciPy, etc. giving easy access 
to GUI-based controls and other functions with an average of two coding lines per addition -- one line to declare a control or widget, and one line to use it.
<br /><br />
Pybox is also very useful for learning and students, hobbyist, and general creative, freeform development & rapid prototyping without the 
need to write a lot of interface code just to add a button, slider, or other control -- or to remove them.
<br /><br />


### Table of Contents
- [Fun with Coding (the real reason for Pybox) - Creative Development and Freeform Programming](#fun-with-coding-the-real-reason-for-pybox---creative-development-and-freeform-programming)
- [Easy-to-Use Library GUI Tools](#easy-to-use-library-gui-tools)
  - [Using Pybox in Console Mode](#using-pybox-in-console-mode)
- [Pybox is also a GUI](#pybox-is-also-a-gui)
  - [A Simple Example](#a-simple-example)
- [Standalone and External 3rd-Party Widgets](#standalone-and-3rd-party-widgets)
  - [Embedding Widgets into Windows](#embedding-widgets-into-windows)
- [Using Pybox with Other Packages like MatplotLib, Tkinter, SciPy, PyTorch, etc.](#using-pybox-with-other-packages-like-matplotlib-tkinter-scipy-pytorch-etc)
- [3D Graphics Primitives](#using-pybox-with-other-packages-like-matplotlib-tkinter-scipy-pytorch-etc)
- [Fast Real-Time 3-D GPU Graphics](#fast-real-time-3-d-gpu-graphics)
- [Super-Fast Open-Source AVX, Multi-Threading Functions](#super-fast-open-source-avx-multi-threading-functions)


### Other Things
- [A Project Based on Community Input](#a-project-based-on-community-input)
- [Making Pybox Useful for Everyone](#making-pybox-useful-for-everyone)
- [Requirements](#requirements)
- [Installation](#installation)
- [Support and Donations](#support-and-donations)
- [Tip of the Iceberg - Alpha Version and Your Input](#tip-of-the-iceberg---alpha-version-and-your-input)
- [Coming Soon](#coming-soon)


<br />

## Fun with Coding (the real reason for Pybox) - Creative Development and Freeform Programming

![output-hello-world-from-python](https://user-images.githubusercontent.com/70604831/174466465-81a3dde8-cbc8-4bbb-b287-28352ef037af.png)

Like many programmers, I like to program creatively as I design whatever I am doing, and Pybox was written as a powerful toolset to quickly add 
(and just as easily remove) controls, widgets and other elements without having to create a lot of event-driven programming or deal with a GUI.
<br /><br />
Pybox originally came from my consulting career so I could produce prototypes and finished products quickly, sometimes within hours, without sacrificing quality
of programming or structure.  Pyboxs scale as you go, to the point so you can keep it and expand it in your release program or simply use it as a development tool
that can be compiled-out for run-time (such as when you aren't writing a program with any GUI elements at all, but use them just for development).
<br /><br />
For me, this is what makes programming fun -- the ability to program in a more freeform, extemporaneous fashion, where I can concentrate on the code I want 
to write rather than the interface code just to have a button, slider, color selector, or whatever I need.

<br />

# Easy-to-Use Library GUI Tools

![collage-generic-sized-flat](https://user-images.githubusercontent.com/70604831/174466534-1a56e6d6-174d-4035-8003-d0d3208c20dd.png)

One of the main ideas behind Pybox is to provide a set of powerful GUI-based tools that are not a GUI per-se, but individual library calls that you 
don't need to manage.  Pybox manages its own environment, so you don't have to keep track of any of the controls or widgets that are launched (unless you want to).

Pybox provides a set of GUI-based functions that you can put in your code in just one or two lines, and can just as easily remove when you want to change things around.
Pybox isn't used a GUI in this sense, and is just a set of function calls.

If you want some quick controls such as buttons, sliders, or some text widgets, etc.,  you can add these with just one line of code, and access them in another line of code.

For example, if you want a slider and a button, all you need are these two lines:

```python
my_slider = pybox.dev_slider("box size")
my_button = pybox.dev_button("Press me")
```

![output-dev-slider-box-0](https://user-images.githubusercontent.com/70604831/174466571-6d968e7b-3e87-4cfa-8060-602137041084.png)

which creates a slider labeled ***"box size"***, with a default range of 0-100 and default value of 100, followed by a button.
Pybox puts these in a window for you, and will delete them later when the program ends or the window is dismissed.
When you want to use the controls, you can just call `my_slider.get_pos()` and `my_button.pressed()`.  You can also use `my_slider.moved()` to determine if the slider has been moved since the last time checked.

For example,

```python
if my_slider.moved() : update_size(my_slider.get_pos())
if my_button.pressed() : print("Button was pressed!")
```

If you want to add a range to the slider with a default, you can add to the original line:

```python
my_slider = pybox.dev_slider("Box Size",range=(10,500),default=150)
```

![output-dev-slider-box-150](https://user-images.githubusercontent.com/70604831/174466616-fed9d593-d165-458f-9c55-84ba93524adf.png)

which sets the slider with a range of 10-500 and a default value of 150.  You can also use floating-point sliders.
Sliders, radio buttons, checkboxes, combo-boxes, list-boxes, text widgets, and other controls are this easy to use.

You can also create quick dialogs or call many different functions to help develop and use your program.

![output-matplotlib2-75-dark](https://user-images.githubusercontent.com/70604831/174466640-0554ccf5-e00a-4108-86da-d7eb1636ebaf.png#gh-dark-mode-only)
![output-matplotlib2-75-light](https://user-images.githubusercontent.com/70604831/174472529-632f0aa9-51e3-4413-ab4d-99a0725ec6a0.png#gh-light-mode-only)

This is an example of making a program using MatplotLib more interactive by providing controls that can be used to change the nature of the two graphs while animating in real-time. 

With various widgets, you can call up color selectors, date pickers, formatted message boxes, image view & img before/after windows, and so-forth.
<br />

### Using Pybox in Console Mode

![output-console-mode](https://user-images.githubusercontent.com/70604831/174466676-d8cec449-a241-4402-9b7e-0e354a4d0777.png)

Pybox can be used with GUI/Windows based programs or regular console mode programs.  In console mode, you can use Pybox functions to help with the program
user-interface, such as bringing up entry boxes and other dialogs, as well as before & after windows, color selectors, etc.
<br /><br />
Since these are called as simple functions, you can just put them in your code without changing your style or interfering with the rest of your code.
<br /><br />
Console-based programs can use Pybox for development even when the end-product doesn't have any UI or GUI components, or can use some of the GUI-based library
calls to help with user input and program flow while developing and debugging. 
<br /><br />


# Pybox is also a GUI

![output-collage-graphics](https://user-images.githubusercontent.com/70604831/174466730-86c6f38a-e743-4f97-be99-8d84be64d39f.png)

Pybox can also be used as a full GUI when you want.  Pybox has a lot of graphics and other functions to allow building GUI-based applications.

You can place specific controls, create graphic buttons, as well as use many drawing graphics functions. 

Pybox can also be used as a full GUI when you want, staying out of the way when you don't.

Pybox has a lot of graphics and other functions to allow building GUI-based applications, the above collage showing some programs using the Pybox graphics
functions.  For most of these programs,  the Pybox usage is just a few lines of code, outputting the results of whatever the code is generating.
<br /><br />

### A Simple Example

You can place specific controls, create graphic buttons, as well as use many drawing graphics functions.

Windows can be created with one line, such as

```python
my_window = pybox.new_window()
```

which will create a default window that you can then write text, draw graphics, or create controls. 
With various keywords, you can control the size, location, background colors, and even create real-time graphics windows.

For example, this program:

```python
my_window = pybox.new_window()
my_window.write("Hello World!",font=150,center_xy = True)
```
![output-hello-world-plain](https://user-images.githubusercontent.com/70604831/174466797-fdab1bdc-e4e4-4dff-a673-6afc2c0126a0.png)

Creates the above window (size reduced for display) with ***"Hello World"*** written in a font size of 150 points.
<br /><br />
You can also just write to the window as a regular text window, and can place widgets and other windows embedded in the window itself to create and
control the look and feel of the program.

![output-pinwheels](https://user-images.githubusercontent.com/70604831/174466809-892b520c-b216-4bbc-9868-ecf817400bf6.png)

With other functions, fun and simple programs can be created using the GPU in real-time, such as the above example. 
<br/><br/>

# Standalone and 3rd-Party Widgets

![output-collage-widgets](https://user-images.githubusercontent.com/70604831/174466845-3b17fbe1-85bc-43f8-9f38-6dd1e248f8af.png)

Pybox has a lot of support for writing widgets, with many pre-made widgets coming soon now that the Alpha release is out. 
<br /><br />
Widgets can be completely standalone and used on their own with just a call, and do not need a GUI interface.  Anyone can write a widget that can be
used as a standalone object for use with any program. 
<br /><br/>
The above examples are the Color Selector, Dial Example Widget, LCD Example Widget, and Spline Widget.

### Embedding Widgets into Windows

![output-emulation](https://user-images.githubusercontent.com/70604831/174466885-1ac37379-5cb0-4538-83c5-1cefeab58dea.png)

Widgets can be embedded seamlessly into a window to create a larger GUI-based interface with little code. 
<br />

The above is an example of using two widgets together to emulate or control an Arduino or other hardware.
<br />

When the dial is moved by the user, the LCD reflects the Dial value, which is also printed to the window using different colors to highlight the values.  The LCD widget is placed on a circuit board image, and the Dial Widget is placed on a stucco background to emulate a wall. 
A smaller child window is created to show the display, and two buttons are added to start/stop the emulation and quit the program.   
There is also a nice rounded title bar on top. 
<br /><br />

## Using Pybox with Other Packages like MatplotLib, Tkinter, SciPy, PyTorch, etc.

![output-collage-other-packages-dark](https://user-images.githubusercontent.com/70604831/174466958-6d26d8a7-5a15-4dd5-a2fa-5b85730c49e2.png#gh-dark-mode-only)
![output-collage-other-packages-light](https://user-images.githubusercontent.com/70604831/174472638-d8c57120-a782-4ad2-b137-2e51689aff12.png#gh-light-mode-only)

Pybox is written to be self-managed and to operate as a set of library calls rather than an environment that must be maintained and managed by the program. 
<br /><br />
This allows Pybox to co-exist with other packages without interfering with their operation.  While Pybox has an environment that it creates, it
is an opt-in environment, where you only use it when you want to.  Otherwise, it stays out of the way. 
<br /><br />
For example, if you're in an event loop with MatplotLib, Tkinter, PyGame, etc., you can simply call out to Pybox to see if it has anything for you
and react accordingly, without having to pump its events.   In other cases, you can use Pybox's environment to wait and look for events. 
<br /><br />
The above examples show using MatplotLib, OpenCV/SciPy and using graphics to output the results of neural networking applications such as PyTorch. 
<br /><br />

# 3D Graphics Primitives

![output-collage-graphics-primitives](https://user-images.githubusercontent.com/70604831/174466989-1449305a-723c-45f1-b1ae-6a6e226889d7.png)

Circles, Squares, Triangles, and Polygons -- a few of the graphics primitives that we can play with and have fun with in programming, whether we're just learning
or thinking creatively, available in just about all languages that support graphics.
<br /><br />
With a simple GUI interface, Pybox also has 3D graphics primitives:  Sphere/Spheroid, Cube/Cuboid, Pyramids, N-sided cone sections (shown above), 
Dodecahedrons and more.
<br /><br />
Objects show the right color diffusion,reflectivity, and can be animated with different sizes, angles and lighting at 60fps and higher. 
<br /><br />
These can be used on a usual 2-D surface (x and y position relative to the window) by just drawing them, or through (x,y,z) positioning that will draw them
in their proper size, lighting, and orientation depending on the object and viewer position relative to the 3-D camera position.
<br /><br />
These 3-D graphics primitives are fairly simple and do not require GPU programming or orientation (and can also be used with the GPU where applicable).
They are created specifically to enjoy playing around with 3-D object in a 2-D or 3-D space and learning graphics basics -- the same purpose
for 2-D primitives such as circles and squares, but with the added technology and abilities we have today in the 2020's. 
<br /><br />
The examples above are stills from a 60-fps (non-GPU) program that moves the objects and viewer around in the image, creating an impressive 3-D animated display. 
<br /><br />
Since they are stills, not shown is the _360-degree equirectangular Pybox module_ used in the background, which rotates the background in the proper
spatial perspective when the viewer position is changed. 
<br /><br />
You can also create your own 3-DPolygonal shapes which can be used with non-GPU graphics and GPU graphics alike.   
<br /><br />
***See the 3D primitives examples -- they will be released shortly as part of the Github project. ***
<br /><br />
Many more 3-D graphics primitives and functions will be added in the next few updates of Pybox.
<br /><br />

# Fast Real-Time 3-D GPU Graphics

![output-collage-gpu](https://user-images.githubusercontent.com/70604831/174467047-dda08078-cf76-4d76-af24-7689271d5a56.png)

Soon to be released, Pybox features fast, real-time 3-D GPU functions.  Shown above are some examples of real-time 60fps+, high-resolution graphics using the GPU.
These are taking roughly 30us of microprocessor time when rendering over 1 million pixels. 
<br /><br />
To render 1 million changing pixels in real-time can also be done in just a few milliseconds with the multi-threading AVX functions written for
Pybox (most of which are expected to be released into open-source). 
<br /><br />
These functions will be released soon, with more coming in the next few months for creating programs with GPU-based real-time graphics. 
<br /><br />

# Super-Fast Open-Source AVX, Multi-Threading Functions

![output-collage-avx-dark](https://user-images.githubusercontent.com/70604831/174467063-7ebb5407-b5d5-41eb-ba9a-5193f1955417.png#gh-dark-mode-only)
![output-collage-avx-light](https://user-images.githubusercontent.com/70604831/174472686-f35a254d-64c2-4c8a-8ca1-edf4b2c99bd1.png#gh-light-mode-only)

Sagebox and Pybox was originally started as a platform to develop and explore a number of different projects, such as GPU-based projects, neural networking
and so-forth. 
<br /><br />
With Sagelight Image Editor and other projects, a lot of multi-threading AVX/SIMD code was written for very fast processing. 
<br /><br />
Now that Pybox is released, these functions will follow shortly, mostly released as open source. 
<br /><br />
Some examples are shown above, all multi-threaded AVX/SIMD functionality, such as the Gaussian/Sinc/Kernel Blur shown above, transferred from Sagelight
Image Editor and other source code, with more coming. 
<br /><br />
The example to the right shows a still from a real-time, constantly re-generated texture with 1 million polygons that is actually created on the CPU and transferred
to the GPU twice as fast as sending it directly to the GPU due to the AVX it uses  -- it's actually a 2D image where it is much faster to process
the polygons, lighting, and reflections on the CPU than it is to have the GPU do it, thanks to AVX.  This adds a lot of power to creating quick, easy, and
generic functions with the GPU. 
<br /><br />
Look for releases in the next few weeks after this initial Pybox release.
<br /><br />


# A Project Based on Community Input

Some elements of Pybox were left open, awaiting community feedback.   As community feedback is received, more functionality and ideas can be added to Pybox
that work for everyone, rather than just one person's idea of it all.   The ultimate goal for Pybox is a cross-platform solution that gives
easy-to-use, powerful functionality that enables more freeform, creative development. 
<br /><br />
Much like a C compiler is written in C, at this point, most of Sagebox/Pybox is written in Sagebox/Pybox.  As Pybox grows, I will start
releasing most of it as open source.  The only reason I haven't done it yet is because I want to refactor some of it
(some of the earlier code is not in the format it needs to be.. aka programmer language for "the earlier code is awful code in comparison to my standards,
and I want to refactor it before the public sees it!"
<br /><br />

# Making Pybox Useful for Everyone

Pybox has one guiding principle: ***"Make it useful for everyone"***, meaning that it should be useful for beginners, students, hobbyists,
professional, researchers, and so-forth.  This is important, so when new functions and ideas are added to Pybox, this is the first and
foremost thought process with new code.  The main principle is that Pybox should always be easy to use, but also very powerful for those that want more out of it.
<br /><br />
The main principle is to start simply with a path to get more creative and comprehensively useful as you want to get more out of your program, in 
an easy-to-understand step-wise manner.
<br /><br />
For example, all Pybox functions start off very easy, such as `"pybox.new_window()"`, and then adding more as you want more, such as 
`"pybox.new_window(at=(x,y),size=(500,400),realtime=true,font=40,hidden=true,bgcolor="black,"blue",resize=ok)'`, and so-forth.  
<br /><br />
Another example is `pybox.img_before_after()`, where you can then add a number of options to personalize and control the window -- you can
also call it as a function or use the return class to control and monitor window events, but only if you want to.   
<br /><br />
On the other hand, if you just want a before & after window with simple code, you can simply call `"pybox.img_before_after(image1,image2)"` and you're done. 
<br /><br />

# Requirements

Sagebox/Pybox has just been released.  It was originally started and used as a library package written for professional consulting applications to
dynamically emulate and control real-time systems.
<br /><br />
As a first release, it supports Windows-based Python and C++. 
<br /><br />
Pybox Alpha Release currently supports Python 3.7, 3.9, and 3.10 on Windows Platforms
<br /><br />
VS Code, Visual Studio 2019 and Visual Studio 2022 work perfectly with Pybox -- I recommend VS Code, with Visual 2019 as a good option. Visual Studio 2022 still seems to have some issues -- it works, but I recommend VS Code instead.
<br /><br />

### WINE on Linux

 A Linux version is the next item on the agenda.  Since Sagelight Editor was written in Sagebox, which works well with WINE on Linux,
 Pybox should also work with WINE under Linux (though the real-time graphics elements have not been tested with WINE yet).

<br /><br />

# Installation

Pybox has just been released and doesn't have a way to install through 'pip' just yet. 

To install, simply pick the correct Python directory (i.e. Python37, Python9, Python 10) and copy the `pybox.py` and `_pybox.pyd` files to the common
module directory for that Python version.

The only files needed are `pybox.py` and `_pybox.pyd`, where the other .py and .pyd modules are needed for some examples and can be useful for widgets usage, such as the color selector widget.

### VS-Code and .env file

With VS Code, you can also create a .env file with `PYTHONPATH=` set to a specific or relative directory contaning the modules &ndash; see the examples directories,
all of which have a `.env` file specifying a relative location for the pybox modules.

### Visual Studio

With Visual Studio, you can add a `Search Path` with a direct or relative path.

Once Pybox has been released for a while and community feedbacks starts coming in, a pip install version will be created.

<br /><br />

# Support and Donations
<br /><br />

# Tip of the Iceberg - Alpha Version and Your Input

Sagebox and Pybox is a very large project with a lot of functions, widgets, GPU algorithms, and more coming.
<br /><br />
I use the term ***'tip of the iceberg'*** because Pybox is a large, comprehensive, highly cohesive and optimized kernel &ndash; and the current release shows a small portion its capabilities. 
<br /><br />
With your feedback and support, Pybox will grow much larger with more functions, controls, designs, as well as more graphics, GPU, and fast, multi-threaded AVX functions.
<br /><br />

# Coming Soon

Pybox is based on community support -- donations, grants, and other financial support.  And, of course, your ideas. 

Here is a list of items currently in-progress and expected to be finished in the next year (most in the next few months, with some releases in the next few weeks), with your support:

- `Widgets and more Widgets` - Widgets are a powerful aspect to Pybox, such as the Color Selector, Date Picker, and the Dial  & LCD emulation example.
	- Other widgets are easily added, such as more Arduino emulations (i.e. 3-D Compass, more detailed LCDs, other hardware),  more color selectors, dual sliders, pop up menus, and so-forth.
	- Most widgets are completely standalone (i.e. color picker, spline curves, etc.) and can be called with a simple function call only (i.e. Pybox does not need to be instantiated or otherwise invoked)
- `Linux version` - The current version started on Windows for alpha release, and the next step is Linux
- `UI Designer` - The UI designer is like using forms (for larger, less ad-hoc-style programs) but much easier, more free-form based, and with more widgets and ability to use personalized controls.  
  - The UI designer has already been designed, and will be finished as community input helps shape it. 
- `Real-Time Graphics` -  Already present in Pybox, more real-time graphics are in-progress.
- `3-D Graphics` -  Functions for 3-D graphics primitives in 2D space as well as 3-D spatial graphics are nearly complete and will be available shortly.  These functions work with and without GPU-based graphics.  3-D GPU-only based functions are also coming.
- `GPU Functions` - Already midway in-progress, these functions provide a very powerful set of easy-to-use tools with the GPU for much more real-time graphics
- `Your Input` - As mentioned, I wrote Pybox for what I do, and now that it is released, I want to write it for what you do and want to see.
	- Just some ideas are controls such as many different types of sliders, control motifs,  Arduino Hardware emulation, etc., whatever the community wants.  It's all fun to write, and since most of Sagebox/Pybox is written in itself, much of it is just about getting the right ideas.

