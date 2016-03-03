<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<html> <head>
<title>wxWize - a wxPython object builder library</title>
  <style>
  </style>
</head>
<body>
<h1>wxWize</h1>


<h2>What? Why?</h2>

<p>The purpose of wxWize is to create sizer-based wxPython designs in
fewer lines of code, with improved readability, without sacrifising
any of the expressive power of programmatic GUI building.
</p>

<p>It's a shallow wrapper, intended to be easily picked up by anyone
who's written wxPython applications before. Things are called the same as in
wxPython/wxWidgets where possible.
</p>

<p>Once created, wxWize steps out of the way, and the wxWindow objects
are all yours. You use them exactly the same as you've always done,
using familiar methods like Bind, SetValue, GetValue,
SetBackgroundColour etc.
</p>

<h2>How?</h2>

<ul>
  <li>wxWize uses the Python <code>with</code> statement to express object nesting.</li>

  <li>Sizers and windows are integrated in a single hierarchy, meaning that
    you no longer need to type in all those sizer.Add calls -- wxWize
    does that for you, based on relative positions in the
  with-statement hierarchy.</li>

  <li><code>parent</code> and <code>id</code> parameters are gone as required parameters for
  controls. parent is computed from the hierarchy position. They can
  still be set where needed using named parameters.</li>
</ul>
  

<h2>Installation</h2>

<p>Copy wize.py to your site-packages directory.
</p>


<h2>Usage</h2>

<h3>Sizers</h3>

<p>Use the with statement to create sizers.  Sizers and windows that are
created within the scope of the with-statement, become children of the
sizer, and automatically added.
</p>

<h3>Simple windows</h3>

<p>
  To create a wx.Window control, use the identically named wize class.
  The __init__ parameters are the same as for the wxPython object, except for this:

  <ul>
    <li>There are only a 1-2 (or an occasional 3) positional
      parameters. <code>parent</code>, <code>id</code>, <code>pos</code>, <code>size</code>
      and <code>style</code> have been relegated to keyword-only.</li>

    <li><code>parent</code> can and should be
      omitted entirely (except for the top-level item).
    </li>

    <li><code>flag</code> and <code>proportion</code> parameters
      provide parent sizer Add arguments.</li>

    <li><code>x</code>, <code>y</code>, <code>xspan</code>
      and <code>yspan</code> provide additional parent sizer Add
      arguments, for when the parent sizer is a GridBagSizer.</li>

  <li><code>EVT_*</code> parameters provide an event binding
    shorthand.</li>

    <li><code>init</code> or <code>cls</code> are useful for subclassing.</li>
  </ul>
</p>

<h3>Container windows</h3>

<p>For windows that can have sub-windows (wize.Frame, wize.Dialog, wize.Panel,
  wize.StaticBox), use the with statement and nest other windows or sizers
  below it.
</p>

<p>If needed, a BoxSizer is created automatically and passed to
  SetSizer. Use  the <code>orient</code> parameter
  to set the direction.</p>

<p>If there is only one child and that child is a sizer, then
  use no BoxSizer is created and the child is used instead.</p>


<h3>Interfacing with ordinary wxPython code</h3>

<h4>wx.Frame/wx.Dialog implemented with wxWize</h4>

<p>When implementing the whole of a top-level window using wxWize,
define the wxWize hierarchy (of nested with-statements) in the
__init__ of your wx.Frame/wx.Dialog subclass. Use
 the <code>init</code> parameter for the top-level call to
  wize.Frame/wize.Dialog.
</p>

<h4>Nesting a wxWize hierarchy within an existing structure</h4>

<p>When implementing only a part of the frame/dialog using wxWize,
  provide a <code>parent</code> argument to the top-level wxWize
  object, and the object returned from <code>with .. as</code>
  will be ready to put into a sizer in your own plain wxPython code.</p>

<h4>Nesting an wxPython window</h4>

<p>wxPython objects - windows and sizers - can be inserted into a
  wxWize hierarchy using ordinary Sizer.Add method calls - using the
  <code>with .. as</code> value from e.g. a wize.BoxSizer or wize.GridSizer.
    The wize.Parent function returns a suitable parent value for
  windows.
</p>

<p>For windows, an alternative is to create a wize.Window with
  a <code>w</code> parameter, and sizer parameters (flag,proportion)
  as needed. Then, wxWize handles the sizer Add.  So you'd write e.g.:</p>
<pre>
    my_win = CreateWindowSomeOtherWay(parent=wize.Parent(),...)
    wize.Window(w=my_win, flag=wx.EXPAND, proportion=1)
</pre>

<h4>Nesting a wxPython sizer</h4>

<p>There's no similar setup for inserting a sizer. But you can always 
<p></p>

<h3>Getting at the wxPython objects</h3>

<p>The sizers and windows created are ordinary wx.Sizer and wx.Window
  objects.<code>with wize. as <em>variable</em></code> binds the
wrapped  wxPython object to <em>variable</em>.
</p>

<p>All the wxWize classes are intended to be used in a Python with
statement.   The value bound with <code>with .. as</code> is the
wrapped wxPython object, a wx.Window or a wx.Sizer.
</p>

<p>For simple objects with no sub-objects -- StaticText, TextCtrl,
  Choice etc. -- the with statement can be omitted. In that case, to get
  at the wrapped wxPython object, use the <code>wx</code> property.</p>

<p>E.g. instead of writing:
<pre>
    with wize.BoxSizer(wx.HORIZONTAL):
        with wize.StaticText(u'Enter name: '): pass
        with wize.TextCtrl() as name_input: pass
</pre>
you can write, to the same effect::
<pre>
    with wize.BoxSizer(wx.HORIZONTAL):
        wize.StaticText(u'Enter name: ')
        name_input = wize.TextCtrl().wx
</pre>
</p>

<h2>Specific features</h2>

<h3>EVT_* binding</h3>

<p>Bind an event callback by using the event name as a named parameter,
with the callback as its value. I.e. <code>EVT_FOO=self.OnFoo</code>
 is a shorthand for <code>.Bind(wx.EVT_FOO, self.OnFoo)</code>.
</p>

<h3>Mixing in a window not created using wxWize</h3>

<p>If for whatever reason you don't want wxWize to create a window, but
you still wxWize to handle the sizers, then create the window yourself
and pass it to the <code>w</code> parameter. wxWize will then use the
w-value you provided instead of creating a new window.
</p>

<p>You can do this even if there's no precise wxWize equivalent to the
  type of window created. Use a superclass such as wize.Window or wize.Panel
  instead.</p>

<h3>Automatic wx.ALL if border&gt;0</h3>

<p>If <code>border</code> is set, and none of the border flags
(wx.TOP,wx.BOTTOM,wx.LEFT,wx.RIGHT) are set, then wx.ALL is assumed.
</p>

<h3>fgcolour, bgcolour and toolTip</h3>

<p>Pass
a <code>fgcolour</code>, <code>bgcolour</code>
or <code>toolTip</code>
  parameter as a shorthand for  <code>.SetForegroundColour</code>,
  <code>.SetBackgroundColour</code> or <code>.SetToolTip</code>.
</p>

<h3>wx.EXPAND is the default for sizers and Panel</h3>

<p>Sizers and wize.Panel have <code>flag=wx.EXPAND</code> as the default. (Controls have <code>flag=0</code>.)</p>

<h3>Changing defaults with Default</h3>

<p>The Default classmethod temporarily changes the default value of one or
  more attributes. It's a with-statement expression, and takes keyword
  parameters which are the new defaults for the class for anything
  created within the scope of the with statement.</p>

<p>For example, to revert the default flag value for sizers back to 0,
instead of wx.EXPAND, do this:</p>

<pre>
with wize.Sizer.Default(flag=0):
    ....
</pre>

<h3>GridBagSizer positioning</h3>

<p>Grid position in a GridBagSizer is set using
separate <code>x</code> and <code>y</code> parameters (which become
the position=wx.GBPosition(y,x) argument to wx.GridBagSizer.Add). To span over
  more than one square, there's <code>xspan</code>
  and <code>yspan</code> (which become the wx.GBSpan(yspan,xspan)
  argument to wx.GridBagSizer.Add).
</p>

<p>If both <code>x</code> and  <code>y</code> are omitted, then the
item is placed to the right of the previous item, or just below. The
value of the <code>orient</code> attribute determines which one:
wx.HORIZONTAL, and it's to the right, wx.VERTICAL, and it's below.
</p>

<p>One or both of <code>x</code> and <code>y</code> can be
  omitted, in which case the previous value is reused. Or, the
  previous value plus one.  That happens if a new x value is provided
  that isn't larger than the previous one, then y is incremented, and
  similarly, if the new y value is provided that isn't larger than the
  previous one, then x is incremented.</p>

<p>This is perhaps better shown by example:
</p>

  <pre>
with wize.GridBagSizer():
    wize.StaticText("First", x=0, y=0)  # (x=0, y=0)
    wize.StaticText("Second", x=1)      # (x=1, y=0)
    wize.StaticText("Third", x=0)       # (x=0, y=1)
    wize.StaticText("Fourth", x=1)      # (x=1, y=1)
    wize.StaticText("Fifth", x=1)       # (x=1, y=2)
</pre>

<p>Although only the line number y=0 is explicitly given, "Third" and
"Fifth" are moved to a new line, because the x value isn't to the
right of the previous x value.
</p>

<p>Note that this could also have been written like this:</p>
  <pre>
with wize.GridBagSizer(wx.HORIZONTAL):
    wize.StaticText("First")              # (x=0, y=0) is the default
    wize.StaticText("Second")             # (x=1, y=0)
    wize.StaticText("Third", x=0)         # (x=0, y=1)
    wize.StaticText("Fourth")             # (x=1, y=1)
    wize.StaticText("Fifth", x=1)         # (x=1, y=2)
</pre>

<h3>StaticBox</h3>

<p>The wize.StaticBox control combines wx.StaticBox and wx.StaticBoxSizer
into one.
</p>

<h3>StaticLine</h3>

<p>The default sizer flag is wx.EXPAND.  A new parameter, 'thickness',
sets the size to (-1,self.thickness) if the style is wx.LI_HORIZONTAL,
or (self.thickness,-1) if wx.LI_VERTICAL. In combination, that means
that e.g. within a BoxSizer(wx.VERTICAL)
<pre>
    wize.StaticLine(3, wx.LI_HORIZONTAL)
</pre>
or, since wx.LI_HORIZONTAL is already the default, shortened to:
<pre>
    wize.StaticLine(3)
</pre>
puts a 3 pixels high line horisontal line across the full width.
</p>

<h3>Subclassing</h3>

<p>When defining a new subclass of a wxPython class, the new subclass
does not have an implementation in wxWize. The obvious fix is to
create a such a class, a wize.Control subclass to wrap your
wx.Control subclass.. 
</p>

<p>That's not at all hard to do.  If you look in wize.py, you can see how
  it's done for the standard controls and do something similar.</p>

<p>But there are other options: For wx.Frame and wx.Dialog subclasses,
define the wxWize object hierarchy by using nested with's in
  __init__. For the root of the with-hierarchy, use a wize.Frame or wize.Dialog
  with init=self.</p>

<p>Finally there's <code>cls</code>, which is an option, if the
subclass __init__ parameter list is identical to the parent
__init__.</p>

<h3>Subclassing with <code>init</code></h3>

<p>The <code>init</code> parameter provides a way to use wxWize from
within the __init__ of a wxPython window subclass. It goes like this:
</p>

<p>Instead of calling parent __init__ from within the subclass
  __init__, create a wxWize object using <code>init=self</code>
  instead. Now wxWize will call the parent __init__ with the same
  parameters it would otherwise have used to create a new object.</p>

<h3>Subclassing with <code>cls</code></h3>

<p>If the subclass __init__ takes the same parameters as the parent
  class, then you can use an existing wxWize-class
  with <code>cls=MyNewSubclass</code>. The <code>cls</code> parameter
  tells wxWize to create the window using this class instead of the normal wxPython class.
</p>


<h3>Isolating with <code>Isolate</code></h3>

<p>wxWize uses global state to track the current wxWize
parent. <code>with Isolate():</code> temporarily sets the wxWize
parent to None, so that objects created in the context do not become linked into the
current hierarchy, but stand on their own.
</p>

<h2>List of classes</h2>

<table border=1>
  <theader><th>Class name</th><th>Positional parameters</th></theader>
  <tbody>
     <tr><td>BoxSizer</td> <td>orient</td> </tr> 
     <tr><td>Button</td> <td>label</td> </tr> 
     <tr><td>CheckBox</td> <td>label</td> </tr> 
     <tr><td>Choice</td> <td>choices</td> </tr> 
     <tr><td>CommandLinkButton</td> <td>mainLabel, note</td> </tr> 
     <tr><td>Control</td> <td>w</td> </tr> 
     <tr><td>DatePickerCtrl</td> <td>dt</td> </tr> 
     <tr><td>Dialog</td> <td>title</td> </tr> 
     <tr><td>FileBrowseButton</td> <td></td> </tr> 
     <tr><td>FlexGridSizer</td> <td>rows</td> </tr> 
     <tr><td>Frame</td> <td>title</td> </tr> 
     <tr><td>GradientButton</td> <td>label, bitmap</td> </tr> 
     <tr><td>Grid</td> <td></td> </tr> 
     <tr><td>GridBagSizer</td> <td></td> </tr>
     <tr><td>Isolate</td> <td></td> </tr>
     <tr><td>ListBox</td> <td>choices</td> </tr> 
     <tr><td>ListCtrl</td> <td></td> </tr> 
     <tr><td>MaskedNumCtrl</td> <td>value</td> </tr> 
     <tr><td>MaskedTextCtrl</td> <td>value</td> </tr> 
     <tr><td>Menu</td> <td>label</td> </tr> 
     <tr><td>MenuBar</td> <td>parent</td> </tr> 
     <tr><td>MenuCheck</td> <td>text, callback</td> </tr> 
     <tr><td>MenuItem</td> <td>text, callback</td> </tr> 
     <tr><td>MenuRadio</td> <td>text, callback</td> </tr> 
     <tr><td>MenuSeparator</td> <td>text, callback</td> </tr> 
     <tr><td>Notebook</td> <td></td> </tr> 
     <tr><td>Page</td> <td>text</td> </tr> 
     <tr><td>Panel</td> <td>proportion</td> </tr> 
     <tr><td>PopupMenu</td> <td>parent</td> </tr> 
     <tr><td>PropertyGrid</td> <td></td> </tr> 
     <tr><td>RadioButton</td> <td>label</td> </tr> 
     <tr><td>ScrolledPanel</td> <td></td> </tr> 
     <tr><td>ScrolledWindow</td> <td></td> </tr> 
     <tr><td>Shell</td> <td></td> </tr> 
     <tr><td>Spacer</td> <td>size</td> </tr> 
     <tr><td>SpinCtrl</td> <td>min, max, initial</td> </tr> 
     <tr><td>StaticBox</td> <td>label, orient</td> </tr> 
     <tr><td>StaticLine</td> <td>thickness, style</td> </tr> 
     <tr><td>StaticText</td> <td>label</td> </tr> 
     <tr><td>StdDialogButtonSizer</td> <td></td> </tr> 
     <tr><td>TextCtrl</td> <td>value</td> </tr> 
     <tr><td>TopLevelWindow</td> <td>title</td> </tr> 
     <tr><td>Window</td> <td>w</td> </tr> 
   </tbody>
   </table>

<h2>Parameters not in the wxWidgets docs</h2>

   <p>The wxPython/wxWidgets documentation for creating objects can be
   used with wxWize as well, since all the documented __init__
   parameters are available.</p>
<p>Here's an overview of the additional parameters that are specific to wxWize:</p>

   <table border=1>
  <theader><th>Parameter name</th><th>Description</th></theader>
  <tbody>

    <tr><td>w</td> <td>Pre-created wxPython object.</td></tr>
    <tr><td>cls</td> <td>Subclass of the wrapped wxPython class to use.</td></tr>
    <tr><td>init</td> <td>init=self if using wxWize to initialise the parent class in__init__</td></tr>
    <tr><td>proportion</td> <td>Sizer Add parameter.</td></tr>
    <tr><td>flag</td> <td>Sizer Add parameter.</td></tr>
    <tr><td>border</td> <td>Sizer Add parameter.</td></tr>
    <tr><td>orient</td> <td>Panels and top-level windows can also take this BoxSizer parameter.</td></tr>
    <tr><td>fgcolour</td> <td>Triggers a SetForegroundColour method call.</td></tr>
    <tr><td>fgcolour</td> <td>Triggers a SetBackgroundColour method call.</td></tr>
    <tr><td>toolTip</td> <td>Triggers a SetToolTipString method call.</td></tr>
    <tr><td>x</td> <td>GridBagSizer column number.</td></tr>
    <tr><td>y</td> <td>GridBagSizer row number.</td></tr>
    <tr><td>xspan</td> <td>GridBagSizer column span.</td></tr>
    <tr><td>yspan</td> <td>GridBagSizer row span.</td></tr>
    <tr><td>orient</td> <td>Layout of children, wx.VERTICAL or wx.HORIZONTAL</td></tr>
    <tr><td>callback</td> <td>EVT_MENU action for MenuItem's</td></tr>
    <tr><td>thickness</td> <td>StaticLine line width.</td></tr>
    <tr><td>InterpClass_args</td> <td>*args for Shell to pass to InterpClass </td></tr>
    <tr><td>InterpClass_kwargs</td> <td>**kwargs for Shell to pass to InterpClass </td></tr>
    <tr><td>EVT_*</td> <td>Set an event callback.</td></tr>
  </tbody>
  </table>
    
</body>
</html>
