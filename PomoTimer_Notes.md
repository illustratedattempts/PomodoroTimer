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
# Git Philosophy
## Branching
It has just come to my attention that all and any changes should have its own separate branch. <b>I will do so immediately.</b>
## Committing
It has also come to my attention that it is best practice to commit any changes often <b>even if they suck</b>. <b>I will do so immediately.</b>
# Threads
## Daemon Threads
Threads that are expected to immediately terminate as soon as the program shuts down. Resources may not be properly released.

## Thread Events
"set" equals <b>True</b><br>
"not set" equals <b>False</b><br>
<b>wait() method</b> blocks the thread until the flag is <b>set</b> or <b>True</b><br>
<b>clear() method</b> resets the flag to <b>False</b><br>
<br>
## Sleep Function
<b>Using the time.sleep() function is a terrible idea</b><br>
We live and learn I suppose! :)

## Pause Timer
Needed to implement the forced delay and pause detection before decrementing timer. This was due to the timer decrementing even though the pause button was pushed. Normal behavioural expectation dictates that users expect the pause button to immediately pause the functionality.


# Settings Window

## Tkinter Variables
Apparently Tkinter has their own custom variables that they use to store values that are consistently modified in widgets.
> var = tk.IntVar()<br>
> var = tk.StringVar()<br>
> ...

### Combobox Widget
There are keyword arguments called: textvariable, state, values<br>
<b>textvariable:</b> Changes the value stored in this variable<br>
<b>state:</b> Defines the state of the widget, the expected values are described as "normal", "readonly", or "disabled". There are also additional tkinter values<br>
<b>values:</b> Stores the list of Combobox selection items

## Widget Binding
For Combobox:<br>
>obj.bind('&lt;&lt;ComboboxSelected&gt;&gt;', function_name)

## Changing the Timer
For now it is my intention that when the timer is changed in any way, the timer will reset

## Changing Timer Types
Having it reset requires it to grab the Semaphore which locks the whole application when another method requires the Semaphore to manipulate the timer variable.

