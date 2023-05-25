[comment]: # (Ctrl+Shift+V for Markdown Preview)

# Window Properties

The **Tk()** object has several functions to define its window size.<br>
Notably, the configure function does not work for statically shaping the window.<br>
However, using the **geometry()** function works.

## geometry() Parameter

It takes a single string as follows: 
"\<width>x\<height>" **OR** "\<width>x\<height>+\<x_position>+\<y_position>"<br>
For Example:<br>
>Tk().geometry("500x500")<br>
>Tk().geometry("500x500+500+350")

# Grab Widget Variables

The **cget()** method where the parameters includes a string of the variable of the widget.

# RuntimeError: main thread is not in main loop

Because the thread function actually has the state of the object the Tkinter GUI functionality moves to the added thread when exiting the foreground GUI.