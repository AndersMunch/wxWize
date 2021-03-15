wxWize - a wxPython object builder library
==========================================

What? Why?
+++++++++++

wxWize is a GUI builder library that supplements wxPython.
wxPython is very powerful and very flexible, but creating windows,
sizers and events can be a bit cumbersone.

This is where wxWize comes in, providing a simple way of creating
sophisticated wxPython designs in fewer lines of code, with vastly
improved readability, and without sacrifising any of the expressive
power of programmatic GUI building.

It's a shallow wrapper, intended to be easily picked up by anyone
who's written wxPython applications before. Things are called the same
as in wxPython/wxWidgets where possible.

Once frames and dialogs are created, wxWize steps out of the way, and
the wxPython objects are all yours. You use them exactly the same as
you've always done, using familiar methods like Bind, SetValue,
GetValue, SetBackgroundColour etc.


How?
++++

* wxWize uses the Python ``with`` statement to express object nesting.
* Sizers and windows are integrated in a single hierarchy, meaning that
  you no longer need to type in all those sizer.Add calls -- wxWize
  does that for you, based on relative positions in the
  with-statement hierarchy.
* ``parent`` and ``id`` parameters are gone as required parameters for
  controls. parent is computed from the hierarchy position. They can
  still be set where needed using named parameters.
  

Installation
++++++++++++

``$ pip install wxWize``

Or copy wize.py to your site-packages directory.



Usage
+++++

Sizers
------

Use the with statement to create sizers.  Sizers and windows that are
created within the scope of the with-statement, become children of the
sizer, and automatically added.


Simple windows
--------------


To create a wx.Window control, use the identically named wize class.
The \_\_init\_\_ parameters are the same as for the wxPython object, except for this:

* There are only a 1-2 (or an occasional 3) positional
  parameters. ``parent``, ``id``, ``pos``, ``size``
  and ``style`` have been relegated to keyword-only.
* ``parent`` can and should be
  omitted entirely (except for the top-level item).
* ``flag`` and ``proportion`` parameters
  provide parent sizer Add arguments.
* ``x``, ``y``, ``xspan``
  and ``yspan`` provide additional parent sizer Add
  arguments, for when the parent sizer is a GridBagSizer.
* ``EVT_*`` parameters provide an event binding
  shorthand.
* ``init`` or ``cls`` are useful for subclassing.


Container windows
-----------------

For windows that can have sub-windows (wize.Frame, wize.Dialog, wize.Panel,
wize.StaticBox), use the with statement and nest other windows or sizers
below it.

If needed, a BoxSizer is created automatically and passed to
SetSizer. Use  the ``orient`` parameter
to set the direction.

If there is only one child and that child is a sizer, then
no BoxSizer is created and the child is used instead.


Interfacing with ordinary wxPython code
---------------------------------------

wx.Frame/wx.Dialog implemented with wxWize
..........................................

When implementing the whole of a top-level window using wxWize,
define the wxWize hierarchy (of nested with-statements) in the
\_\_init\_\_ of your wx.Frame/wx.Dialog subclass. Use
the ``init`` parameter for the top-level call to
wize.Frame/wize.Dialog.


Nesting a wxWize hierarchy within an existing structure
..............................................................

When implementing only a part of the frame/dialog using wxWize,
  provide a ``parent`` argument to the top-level wxWize
  object, and the object returned from ``with .. as``
  will be ready to put into a sizer in your own plain wxPython code.

Nesting an wxPython window
..........................

wxPython objects - windows and sizers - can be inserted into a
wxWize hierarchy using ordinary Sizer.Add method calls - using the
``with .. as`` value from e.g. a wize.BoxSizer or wize.GridSizer.
The wize.Parent function returns a suitable parent value for
windows.


For windows, an alternative is to create a wize.Window with
a ``w`` parameter, and sizer parameters (flag,proportion)
as needed. Then, wxWize handles the sizer Add.  So you'd write e.g.:

.. code-block:: python

    my_win = CreateWindowSomeOtherWay(parent=wize.Parent(),...)
    wize.Window(w=my_win, flag=wx.EXPAND, proportion=1)


Nesting a wxPython sizer
........................

There's no similar setup for inserting a sizer. But you can always 


Getting at the wxPython objects
-------------------------------

The sizers and windows created are ordinary wx.Sizer and wx.Window
objects. ``with wize. as *variable*`` binds the
wrapped  wxPython object to *variable*.

All the wxWize classes are intended to be used in a Python with
statement.   The value bound with ``with .. as`` is the
wrapped wxPython object, a wx.Window or a wx.Sizer.

For simple objects with no sub-objects -- StaticText, TextCtrl,
Choice etc. -- the with statement can be omitted. In that case, to get
at the wrapped wxPython object, use the ``wx`` property.

E.g. instead of writing:

.. code-block:: python

    with wize.BoxSizer(wx.HORIZONTAL):
        with wize.StaticText(u'Enter name: '): pass
        with wize.TextCtrl() as name_input: pass

you can write, to the same effect:

.. code-block:: python

    with wize.BoxSizer(wx.HORIZONTAL):
        wize.StaticText(u'Enter name: ')
        name_input = wize.TextCtrl().wx


Menus
-----

Just like the with statement and indentation is used to place controls into the sizer
hierarchy, the with statement and indentation can be used to create
menus and submenus. See the example in ``demo_pallette.py``.

Start with a ``wize.MenuBar`` or ``wize.PopupMenu`` at the top level. Nested within
that, use ``wize.MenuItem``'s to create simple menu entries, and ``wize.Menu``'s to
create submenus.

For an application-global menu bar, use ``wize.MenuBar``, with the main
frame of application as the parent. That is to say, either nest
``wize.MenuBar`` within a ``wize.Frame``, or provide the ``wx.Frame`` in the
``parent`` parameter. The immediate children must be ``wize.Menu``'s, not
MenuItem's.

For a pop-up menu, use ``wize.PopupMenu`` as the top-level item, nesting
``wize.MenuItem`` and ``wize.Menu`` objects as desired.

``wize.MenuCheck`` and ``wize.MenuRadio`` are shortcuts for
``wize.MenuItem`` with parameters to create a menu item with a checkbox
or a radio button.

Also there's ``wize.MenuSeparator`` which adds a separator line between
menu items.

Specific features
+++++++++++++++++

EVT\_\* binding
---------------

Bind an event callback by using the event name as a named parameter,
with the callback as its value. I.e. ``EVT_FOO=self.OnFoo``
is a shorthand for ``.Bind(wx.EVT_FOO, self.OnFoo)``.


Mixing in a window not created using wxWize
-------------------------------------------

If for whatever reason you don't want wxWize to create a window, but
you still wxWize to handle the sizers, then create the window yourself
and pass it to the ``w`` parameter. wxWize will then use the
w-value you provided instead of creating a new window.


You can do this even if there's no precise wxWize equivalent to the
  type of window created. Use a superclass such as wize.Window or wize.Panel
  instead.

Automatic wx.ALL if border>0
-------------------------------

If ``border`` is set, and none of the border flags
(wx.TOP,wx.BOTTOM,wx.LEFT,wx.RIGHT) are set, then wx.ALL is assumed.


fgcolour, bgcolour and toolTip
------------------------------

Pass a ``fgcolour``, ``bgcolour`` or ``toolTip`` parameter as a shorthand
for  ``.SetForegroundColour``, ``.SetBackgroundColour`` or ``.SetToolTip``.


wx.EXPAND and proportion=1 for sizers and panels
------------------------------------------------

Sizers and panels have ``flag=wx.EXPAND`` as the default. (Controls have ``flag=0``.)
Additionally, panels have proportion=1 as the default.

wx.EXPAND and proportion>0 help sizers and panels be neutral
intermediaries: If you e.g have a ListCtrl on a Frame, and you change
that to be a ListCtrl on a Panel on a Frame, then the ListCtrl will
resize with the frame if it did before.

Panels include wize.Panel and wize.SplitterWindow. 

Changing defaults with Default
------------------------------

The Default classmethod temporarily changes the default value of one or
more attributes. It's a with-statement expression, and takes keyword
parameters which are the new defaults for the class for anything
created within the scope of the with statement.

For example, to revert the default flag value for a BoxSizer back to 0,
instead of wx.EXPAND, do this:


.. code-block:: python

    with wize.BoxSizer.Default(flag=0):
        ....


GridBagSizer positioning
------------------------

Grid position in a GridBagSizer is set using
separate ``x`` and ``y`` parameters (which become
the position=wx.GBPosition(y,x) argument to wx.GridBagSizer.Add). To span over
more than one square, there's ``xspan``
and ``yspan`` (which become the wx.GBSpan(yspan,xspan)
argument to wx.GridBagSizer.Add).


If both ``x`` and  ``y`` are omitted, then the
item is placed to the right of the previous item, or just below. The
value of the ``orient`` attribute determines which one:
wx.HORIZONTAL, and it's to the right, wx.VERTICAL, and it's below.


One or both of ``x`` and ``y`` can be
omitted, in which case the previous value is reused. Or, the
previous value plus one.  That happens if a new x value is provided
that isn't larger than the previous one, then y is incremented, and
similarly, if the new y value is provided that isn't larger than the
previous one, then x is incremented.

This is perhaps better shown by example:

  .. code-block:: python

    with wize.GridBagSizer():
        wize.StaticText("First", x=0, y=0)  # (x=0, y=0)
        wize.StaticText("Second", x=1)      # (x=1, y=0)
        wize.StaticText("Third", x=0)       # (x=0, y=1)
        wize.StaticText("Fourth", x=1)      # (x=1, y=1)
        wize.StaticText("Fifth", x=1)       # (x=1, y=2)

Although only the line number y=0 is explicitly given, "Third" and
"Fifth" are moved to a new line, because the x value isn't to the
right of the previous x value.

Note that this could also have been written like this:

  .. code-block:: python

    with wize.GridBagSizer(wx.HORIZONTAL):
        wize.StaticText("First")              # (x=0, y=0) is the default
        wize.StaticText("Second")             # (x=1, y=0)
        wize.StaticText("Third", x=0)         # (x=0, y=1)
        wize.StaticText("Fourth")             # (x=1, y=1)
        wize.StaticText("Fifth", x=1)         # (x=1, y=2)


StaticBox
---------

The wize.StaticBox control combines wx.StaticBox and wx.StaticBoxSizer
into one.


StaticLine
----------

The default sizer flag is wx.EXPAND.  A new parameter, 'thickness',
sets the size to (-1,self.thickness) if the style is wx.LI_HORIZONTAL,
or (self.thickness,-1) if wx.LI_VERTICAL. In combination, that means
that e.g. within a BoxSizer(wx.VERTICAL)

.. code-block:: python

    wize.StaticLine(3, wx.LI_HORIZONTAL)

or, since wx.LI_HORIZONTAL is already the default, shortened to:

.. code-block:: python

    wize.StaticLine(3)

puts a 3 pixels high line horisontal line across the full width.


SplitterWindow
--------------

``SplitterWindow(wx.HORIZONTAL)`` puts the two nested windows side by side
with a resizing sash between. ``SplitterWindow(wx.VERTICAL)`` puts the two
nested windows on top of one another. (Don't call ``SplitVertically`` or
``SplitHorizontally``, it's automatic.)

The default of sashGravity=0.5 makes the subwindows equal sized, and
the default of minimumPaneSize=1 ensures that the second subwindow
doesn't disappear unexpectedly. (Use minimumPaneSize=0 to restore the
wxWidgets default behaviour that a double
click on the sash hides the second window.)

FourWaySplitter
---------------

``sashPosition=(hfraction,vfraction)`` sizes the subpanels using fractions in the 0..1 range,
for consistency with sashPosition for SplitterWindow.

Properties HSplit and VSplit are an alternative to sashPosition that uses integers in the
range 0..10000 instead, for consistency with the SetHSplit and SetVSplit methods of FourWaySplitter.

Subclassing
-----------

When defining a new subclass of a wxPython class, the new subclass
does not have an implementation in wxWize. The obvious fix is to
create a such a class, a wize.Control subclass to wrap your
wx.Control subclass.

That's not at all hard to do.  If you look in wize.py, you can see how
it's done for the standard controls and do something similar.

But there are other options: For wx.Frame and wx.Dialog subclasses,
define the wxWize object hierarchy by using nested with's in
\_\_init\_\_. For the root of the with-hierarchy, use a wize.Frame or wize.Dialog
with init=self.

Finally there's ``cls``, which is an option, if the
subclass \_\_init\_\_ parameter list is identical to the parent
\_\_init\_\_.

Subclassing with ``init``
-------------------------

The ``init`` parameter provides a way to use wxWize from
within the \_\_init\_\_ of a wxPython window subclass. It goes like this:


Instead of calling parent \_\_init\_\_ from within the subclass
\_\_init\_\_, create a wxWize object using ``init=self``
instead. Now wxWize will call the parent \_\_init\_\_ with the same
parameters it would otherwise have used to create a new object.

Subclassing with ``cls``
------------------------

If the subclass \_\_init\_\_ takes the same parameters as the parent
class, then you can use an existing wxWize-class
with ``cls=MyNewSubclass``. The ``cls`` parameter
tells wxWize to create the window using this class instead of the normal wxPython class.



Isolating with ``Isolate``
--------------------------

wxWize uses global state to track the current wxWize
parent. ``with Isolate():`` temporarily sets the wxWize
parent to None, so that objects created in the context do not become linked into the
current hierarchy, but stand on their own.


List of classes
+++++++++++++++

=======================	=========================================
Class name		Positional parameters 
=======================	=========================================  
BoxSizer		orient
Button			label
CheckBox		label
Choice			choices
ComboBox		value, choices
CommandLinkButton	mainLabel, note
Control			w
DatePickerCtrl		dt
Dialog			title
FileBrowseButton	
FlexGridSizer		rows
FourWaySplitter		sashPosition
Frame			title
Gauge			range
GradientButton		label, bitmap
Grid			
GridBagSizer		
Isolate
LabelBook		agwStyle
ListBox			choices
ListCtrl		
MaskedNumCtrl		value
MaskedTextCtrl		value
Menu			label
MenuBar			parent
MenuCheck		text, callback
MenuItem		text, callback
MenuRadio		text, callback
MenuSeparator		text, callback
Notebook		
Page			text
Panel			proportion
PopupMenu		parent
PropertyGrid		
RadioButton		label
ScrolledPanel		
ScrolledWindow	
SearchCtrl		
Shell			
Spacer			size
SpinCtrl		min, max, initial
SplitterWindow		orient, minimumPaneSize
StaticBox		label, orient
StaticLine		thickness, style
StaticText		label
StdDialogButtonSizer	
TextCtrl		value
TopLevelWindow		title
Window			w
=======================	=========================================


Parameters not in the wxWidgets docs
++++++++++++++++++++++++++++++++++++

The wxPython/wxWidgets documentation for creating objects can be
used with wxWize as well, since all the documented \_\_init\_\_
parameters are available.
   
Here's an overview of the additional parameters that are specific to wxWize:


=======================	=================================================================================
Parameter name		Description
=======================	================================================================================= 
w			Pre-created wxPython object. 
cls			Subclass of the wrapped wxPython class to use. 
init			init=self if using wxWize to initialise the parent class in \_\_init\_\_ 
proportion		Sizer Add parameter. 
flag			Sizer Add parameter.
border			Sizer Add parameter.
orient			Panels and top-level windows can also take this BoxSizer parameter.
fgcolour		Triggers a SetForegroundColour method call.
fgcolour		Triggers a SetBackgroundColour method call.
toolTip			Triggers a SetToolTipString method call.
x			GridBagSizer column number.
y			GridBagSizer row number.
xspan			GridBagSizer column span.
yspan			GridBagSizer row span.
orient			Layout of children, wx.VERTICAL or wx.HORIZONTAL
callback		EVT_MENU action for MenuItem's
thickness		StaticLine line width.
InterpClass_args	\*args for Shell to pass to InterpClass 
InterpClass_kwargs	\*\*kwargs for Shell to pass to InterpClass 
sashGravity		SplitterWindow.SetSashGravity parameter
minimumPaneSize		SplitterWindow.SetMinimumPaneSize parameter
EVT\_\*			Set an event callback.
=======================	=================================================================================
