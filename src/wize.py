import sys, contextlib
import wx

try:
    basestring
except NameError:
    basestring = str
_phoenix = wx.VERSION[0] >= 4
    
######################################################################
# Entity, the base class.

_zparent = None
class Entity(object):
    # props: the set of valid __init__ arguments
    props = set([
        # sizer.Add arguments, for how this entity is added to the containing sizer
        'proportion',
        'flag',
        'border', # /outer/ border, between self and others, not /inner/ border between contained elements

        # parent argument to wx.Window's
        'parent',
        
        # GridBagSizer position and size
        'x','y','xspan','yspan',
        
        # For composite entities, the orientation of children: wx.VERTICAL or wx.HORIZONTAL
        'orient',

        # set to skip creation entirely
        'w',
        ])
    # positional: __init__ optional positional arguments; (an ordered subset of props)
    positional = []

    # Default values, intended to be overwritten by __init__ settings:
    parent = None
    orient = wx.HORIZONTAL
    proportion = 0
    flag = 0
    border = 0
    x = None
    y = None
    xspan = 1
    yspan = 1
    _defaults = dict()

    def __init__(self, *args, **kwargs):
        # Set by the subclass in create_preorder/create_postorder
        self.w = None # the wx.Window, if any, being created
        self.sized = None # the wx.Sizer or wx.Window which the parent Entity must put in its component sizer
        self._events = []
        self._queue = []
        if _zparent is not None:
            _zparent._queue.append(self)

        # Set attributes in accordance with the rules for the class set out in 'props', the list of allowed
        #  __init__ arguments, and 'positional', the subset that can be passed as positional parameters.
        if len(args) > len(self.positional):
            raise TypeError("%s takes positional arguments %s, %d more given" % (self, self.positional, len(args)-len(self.positional)))
        if 'kwargs' in self.props:
            self.kwargs = {}
        for k,v in dict(self._defaults, **kwargs).items():
            if k in self.props:
                setattr(self, k, v)
            else:
                if k.startswith('EVT_') and isinstance(self, Window):
                    self._events.append((k, v))
                elif 'kwargs' in self.props:
                    self.kwargs[k] = v
                else:
                    raise TypeError("%s does not have a writable '%s' attribute" % (type(self), k))
        for argname,arg in zip(self.positional, args):
            if argname in kwargs:
                raise TypeError("%s passed both by keyword and as positional argument %d" % (argname,self.positional.index(argname)+1))
            assert argname in self.props
            setattr(self, argname, arg)

        # Hierarchy management:
        self._entered = False # has __enter__/__exit__, which sets .w and .sized, been done yet?
        self.zparent = _zparent # above Entity
        self.zchildren = [] # Entity's nested below
        if self.zparent is not None:
            self.zparent.zchildren.append(self)

        if self.parent is None and self.zparent is None:
            assert isinstance(self, (TopLevelWindow,TopLevelMenu,Sizer)), '%s does not have a parent' % (self,)

    def __enter__(self):
        self._entered = True
        _flush_implicit_with()
        global _zparent
        self.__saved_zparent = _zparent
        _zparent = self
        try:
            self.create_preorder()
        except:
            _zparent = self.__saved_zparent
            raise
        return self.w

    def __exit__(self, bla, blah, blargh):
        try:
            if bla is None:
                _flush_implicit_with()
                self.create_postorder()
        finally:
            global _zparent
            _zparent = self.__saved_zparent
            del self.__saved_zparent

    def as_parent(self):
        u"""Returns the wx.Window for child windows to use as a parent."""
        return self.get_parent() # overridden for windows

    def get_parent(self):
        u"""Returns a suitable wx.Window for the parent argument."""
        if self.parent is not None:
            return self.parent
        elif self.zparent is not None:
            return self.zparent.as_parent()

    @property
    def wx(self):
        if not self._entered:
            with self: pass
        return self.w

    def __getattr__(self, att):
        if self.w is not None and hasattr(self.w, att):
            # A common error is to forget the trailing .wx; be forgiving, but warn
            import warnings
            warnings.warn('wize.%s has no attribute %s: substituting .wx.%s' % (
                type(self).__name__, att, att), stacklevel=2)
            return getattr(self.w, att)
        else:
            raise AttributeError('wize.%s has no attribute %s' % (type(self).__name__, att))
    
    @classmethod
    @contextlib.contextmanager
    def Default(cls, **kwargs):
        original = cls._defaults
        cls._defaults = original.copy()
        cls._defaults.update(kwargs)
        try:
            yield None
        finally:
            _flush_implicit_with() 
            cls._defaults = original
        
    def create_preorder(self):
        u"""Code to be run from __enter__, before child windows are processed."""
        raise NotImplementedError

    def create_postorder(self):
        u"""Code to be run from __exit__, after child windows are processed."""
        raise NotImplementedError


def _flush_implicit_with():
    if _zparent is not None:
        process = _zparent._queue
        _zparent._queue = []
        for c in process:
            if not c._entered:
                with c: pass


class Isolate(object):
    def __enter__(self):
        global _zparent
        self._saved_zparent = _zparent
        _zparent = None
    def __exit__(self, huey, dewey, louie):
        global _zparent
        _zparent = self._saved_zparent
    
######################################################################
# Sizers.

def _add_to_sizer(sizer, zchild):
    if isinstance(zchild, MenuEntity):
        return
    else:
        if isinstance(zchild, Spacer):
            item = (zchild.width, zchild.height)
        else:
            item = zchild.sized
        if zchild.border > 0 and (zchild.flag & wx.ALL)==0:
            zchild.flag |= wx.ALL
        zchild.sizer_item = sizer.Add(item, zchild.proportion, zchild.flag, zchild.border)

class Sizer(Entity):
    # flag=wx.EXPAND instead of flag=0 is a delibrate deviation from the wxPython Sizer.Add default
    # it's only for sizers, though, Window's still default to flag=0
    flag = wx.EXPAND
    proportion = 0
    def create_preorder(self):
        self.sized = self.w
    def create_postorder(self):
        pass

class BoxSizer(Sizer):
    positional = ['orient']
    orient = wx.HORIZONTAL
    def create_preorder(self):
        self.w = self.sized = (self.w or wx.BoxSizer(self.orient))
    def create_postorder(self):
        for c in self.zchildren:
            _add_to_sizer(self.sized, c)

class StdDialogButtonSizer(BoxSizer):
    positional = []
    def create_preorder(self):
        self.w = self.sized = (self.w or wx.StdDialogButtonSizer())
    def create_postorder(self):
        for c in self.zchildren:
            self.sized.AddButton(c.w)
        self.sized.Realize()

class GridBagSizer(Sizer):
    props = Sizer.props | set(['vgap', 'hgap'])
    vgap = 0
    hgap = 0
    def create_preorder(self):
        self.w = self.sized = (self.w or wx.GridBagSizer(self.vgap, self.hgap))
    def create_postorder(self):
        prev_x = prev_y = prev_xspan = prev_yspan = 0
        for c in self.zchildren:
            x,y = c.x,c.y
            if x is None and y is None:
                x,y = prev_x,prev_y
                if self.orient == wx.HORIZONTAL:
                    x += prev_xspan
                elif self.orient == wx.VERTICAL:
                    y += prev_yspan
                else:
                    raise TypeError('%s position unspecified' % (c,))
            elif x is None:
                x = prev_x
                if y < prev_y + prev_yspan:
                    x += 1
            elif y is None:
                y = prev_y
                if x < prev_x + prev_xspan:
                    y += 1
            if c.border > 0 and (c.flag & wx.ALL)==0:
                c.flag |= wx.ALL
            c.sizer_item = self.w.Add(c.sized, (y,x), (c.yspan,c.xspan), c.flag, c.border)
            prev_x, prev_y, prev_xspan, prev_yspan = x,y,c.xspan,c.yspan

class FlexGridSizer(Sizer):
    props = Sizer.props | set(['rows', 'cols', 'vgap', 'hgap'])
    vgap = hgap = 0
    rows = cols = 0
    positional = ['rows']
    def create_preorder(self):
        self.w = self.sized = (self.w or wx.FlexGridSizer(self.rows, self.cols, self.vgap, self.hgap))
    def create_postorder(self):
        for c in self.zchildren:
            _add_to_sizer(self.w, c)

class StaticBox(BoxSizer):
    props = BoxSizer.props | set(['id','label','style','size','name'])
    positional = ['label', 'orient']
    id = wx.ID_ANY
    label = ''
    style = 0
    size = wx.DefaultSize
    pos = wx.DefaultPosition # deliberately not in props
    name = u'groupBox'
    proportion = 0
    flag = wx.EXPAND
    def create_preorder(self):
        self.w = wx.StaticBox(self.get_parent(), self.id, self.label, self.pos, self.size, self.style, self.name)
        self.sized = wx.StaticBoxSizer(self.w, self.orient)
    def as_parent(self):
        return self.w

class Spacer(Entity):
    props = set(['size','width','height','proportion'])
    positional = ['size']
    size = None
    width = None
    height = None
    def create_preorder(self):
        if not isinstance(self.zparent, Sizer):
            raise TypeError('Spacer parent %s is not a Sizer' % (self.zparent,))
        if self.size is not None:
            assert self.width is None and self.height is None
            self.width = self.height = self.size
    def create_postorder(self):
        pass

def StretchSpacer(proportion=1):
    return Spacer(size=0, proportion=proportion)


######################################################################
# Simple widgets.

def Parent():
    return None if _zparent is None else _zparent.as_parent()

class Window(Entity):
    props = Entity.props | set([
        'cls',   # can be set to a subclass with an identical __init__ signature 
        'init',  # use init=self to perform base class initialisation in __init__ of a wx.Window subclass
        'id', 'size', 'style', 'name',
        'fgcolour', 'bgcolour', # .SetForegroundColour, .SetBackgroundColour
        'toolTip',  # .SetToolTip
        ])
    positional = ['w']
    w = None
    init = None
    cls = None
    id = wx.ID_ANY
    size = wx.DefaultSize
    pos = wx.DefaultPosition # deliberately not in props, but can be set after __init__, if need be
    style = 0
    # name omitted -- cannot be None, subclasses *must* set
    fgcolour = bgcolour = None
    toolTip = None
    def create_preorder(self):
        if self.parent is None:
            self.parent = self.get_parent()
        if self.w is None:
            self.w = self.create_wxwindow()
            if self.init is not None: self.w = self.init
            assert self.w is not None, self
        self.sized = self.w
        if self.bgcolour is not None: self.w.SetBackgroundColour(self.bgcolour)
        if self.fgcolour is not None: self.w.SetForegroundColour(self.fgcolour)
        if self.toolTip is not None:
            if not _phoenix and isinstance(self.toolTip, basestring):
                self.w.SetToolTipString(self.toolTip)
            else:
                self.w.SetToolTip(self.toolTip)
        for eventname,callback in self._events:
            for mod in self._event_module_candidates():
                try:
                    event = getattr(mod, eventname)
                except AttributeError:
                    pass
                else:
                    self.w.Bind(event, callback)
                    break
            else:
                raise AttributeError('%s not found (in %s)' % (eventname, ','.join(m.__name__ for m in self._event_module_candidates())))
                
    def _event_module_candidates(self):
        # Yield modules so search for an EVT_* name -- besides wx, the module in which the class of .w is
        # defined, and whatever packages that module is contained in.
        yield wx
        modname = self.w.__module__
        mod = __import__(modname)
        for submodname in modname.split('.')[1:]:
            mod = getattr(mod, submodname)
            yield mod

    def create_postorder(self):
        if len(self.zchildren)==0:
            # non-container wx.Window's: TextCtrl, StaticText, Choice, ...
            self.zchildren_sizer = None
        else:
            # Container: Frame, Dialog, Panel
            c0 = self.zchildren[0]
            if len(self.zchildren)==1 and isinstance(c0, Sizer) and c0.border==0 and c0.flag==wx.EXPAND and c0.proportion>0:
                # Promote an explicitly created sizer, provided it doesn't have settings (such as border>0)
                # which require a surrounding sizer to accomodate.
                self.zchildren_sizer = self.zchildren[0].sized
            else:
                # Supply a sizer created from Frame/Dialog/Panel arguments.
                self.zchildren_sizer = wx.BoxSizer(self.orient)
                for c in self.zchildren:
                    _add_to_sizer(self.zchildren_sizer, c)
            self.w.SetSizer(self.zchildren_sizer)
    def initfn(self, cls, compatible_types=None):
        if self.init is not None:
            assert self.cls is None
            assert isinstance(self.init, cls) and type(self.init) is not cls, 'expected init=object of %r subclass' % (cls,)
            return super(type(self.init), self.init).__init__
        elif self.cls is not None:
            if isinstance(self.cls, type):
                assert issubclass(self.cls, compatible_types or cls)
            else:
                assert callable(self.cls)
            return self.cls
        else:
            return cls
    def create_wxwindow(self):
        raise NotImplementedError
    def as_parent(self):
        return self.w

class Control(Window):
    props = Window.props | set(['validator'])
    validator = wx.DefaultValidator
    
class Panel(Window):
    props = Window.props
    positional = ['proportion']
    style = wx.TAB_TRAVERSAL
    name = 'panel'
    proportion = 1
    flag = wx.EXPAND
    def create_wxwindow(self):
        return self.initfn(wx.Panel)(self.parent, self.id, self.pos, self.size, self.style, self.name)
    def create_postorder(self):
        Window.create_postorder(self)

class TextCtrl(Control):
    props = Control.props | set(['value'])
    positional = ['value']
    name = 'text'
    value = ''
    def create_wxwindow(self):
        return self.initfn(wx.TextCtrl)(self.parent, self.id, self.value, self.pos,
                           self.size, self.style, self.validator, self.name)

class StaticText(Window):
    # going with Window instead of Control because wx.StaticText.__init__ takes no validator
    props = Window.props | set(['label'])
    positional = ['label']
    name = 'staticText'
    label = ''
    def create_wxwindow(self):
        return self.initfn(wx.StaticText)(self.parent, self.id, self.label, self.pos,
                             self.size, self.style, self.name)

class Button(Control):
    props = Control.props | set(['label'])
    positional = ['label']
    name = 'button'
    def create_wxwindow(self):
        return self.initfn(wx.Button, [wx.Button,wx.ToggleButton])(
            self.parent, self.id, self.label, self.pos, self.size, self.style, self.validator, self.name)

class CommandLinkButton(Button):
    props = Control.props | set(['mainLabel', 'note'])
    positional = ['mainLabel', 'note']
    note = ''
    def create_wxwindow(self):
        try:
            from wx.adv import CommandLinkButton # Phoenix
        except ImportError:
            CommandLinkButton = wx.CommandLinkButton # Classic
        return self.initfn(CommandLinkButton)(self.parent, self.id, self.mainLabel, self.note, self.pos, self.size, self.style, self.validator, self.name)

class CheckBox(Control):
    props = Control.props | set(['label'])
    positional = ['label']
    name = 'check'
    def create_wxwindow(self):
        return self.initfn(wx.CheckBox)(self.parent, self.id, self.label, self.pos, self.size, self.style, self.validator, self.name)

class Choice(Control):
    props = Control.props | set(['choices'])
    positional = ['choices']
    name = 'choice'
    choices = []
    def create_wxwindow(self):
        return self.initfn(wx.Choice)(self.parent, self.id, self.pos, self.size, self.choices, self.style, self.validator, self.name)

class ComboBox(Control):
    props = Control.props | set(['choices','value'])
    positional = ['value', 'choices']
    name = 'comboBox'
    value = ''
    choices = []
    def create_wxwindow(self):
        return self.initfn(wx.ComboBox)(self.parent, self.id, self.value, self.pos, self.size, self.choices, self.style, self.validator, self.name)

class DatePickerCtrl(Control):
    props = Control.props | set(['dt'])
    positional = ['dt']
    name = 'datectrl'
    style = 4 # 4==wx.adv.DP_DEFAULT|wx.adv.DP_SHOWCENTURY -- don't want to import wx.adv at top-level, som symbolic names are unavailable
    dt = wx.DefaultDateTime
    def create_wxwindow(self):
        try:
            from wx.adv import DatePickerCtrl
        except ImportError:
            DatePickerCtrl = wx.DatePickerCtrl
        return self.initfn(DatePickerCtrl)(self.parent, self.id, self.dt, self.pos, self.size, self.style, self.validator, self.name)

class Grid(Window):
    props = Window.props | set(['name', 'numRows', 'numCols', 'selmode'])
    positional = ['numRows', 'numCols']
    name = 'grid'
    style = wx.WANTS_CHARS
    numRows = numCols = selmode = None
    def create_wxwindow(self):
        from wx import grid
        res = self.initfn(grid.Grid)(self.parent, self.id, self.pos, self.size, self.style, self.name)
        if self.numRows is not None and self.numCols is not None:
            res.CreateGrid(self.numRows, self.numCols, self.selmode if self.selmode is not None else grid.Grid.SelectCells)
        return res

class ListBox(Control):
    props = Control.props | set(['choices'])
    positional = ['choices']
    name = 'listbox'
    choices = []
    def create_wxwindow(self):
        return self.initfn(wx.ListBox)(self.parent, self.id, self.pos, self.size, self.choices, self.style, self.validator, self.name)

class ListCtrl(Control):
    props = Control.props | set(['name'])
    name = 'listCtrl'
    style = wx.LC_ICON
    def create_wxwindow(self):
        return self.initfn(wx.ListCtrl)(self.parent, self.id, self.pos, self.size, self.style, self.validator, self.name)

class PropertyGrid(Window):
    props = Window.props
    name = 'propertygrid'
    def create_wxwindow(self):
        import wx.propgrid
        return self.initfn(wx.propgrid.PropertyGrid)(self.parent, self.id, self.pos, self.size, self.style, self.name)

class Shell(Window):
    props = Window.props | set(['kwargs'])
    name = 'shell'
    style = wx.CLIP_CHILDREN
    introText = ''
    locals = None
    InterpClass = None
    startupScript = None
    execStartupScript = True
    showInterpIntro = True
    InterpClass_args = ()
    InterpClass_kwargs = {}
    def create_wxwindow(self):
        import wx.py.shell
        return self.initfn(wx.py.shell.Shell)(self.parent, self.id, self.pos, self.size, self.style,
                                 introText=self.introText, locals=self.locals, InterpClass=self.InterpClass,
                                 startupScript=self.startupScript, execStartupScript=self.execStartupScript,
                                 **self.kwargs)

class RadioButton(Control):
    props = Control.props | set(['label'])
    positional = ['label']
    name = 'radioButton'
    def create_wxwindow(self):
        return self.initfn(wx.RadioButton)(self.parent, self.id, self.label, self.pos, self.size, self.style, self.validator, self.name)

class ScrolledPanel(Window):
    props = Window.props
    name = 'scrolledpanel'
    style = wx.TAB_TRAVERSAL
    def create_wxwindow(self):
        return self.initfn(wx.lib.scrolledpanel.ScrolledPanel)(self.parent, self.id, self.pos, self.size, self.style, self.name)

class ScrolledWindow(Window):
    props = Window.props
    name = 'panel'
    style = wx.HSCROLL|wx.VSCROLL
    proportion = 1
    flag = wx.EXPAND
    xrate = yrate = 10
    def create_wxwindow(self):
        res = self.initfn(wx.ScrolledWindow)(self.parent, self.id, self.pos, self.size, self.style, self.name)
        res.SetScrollRate(self.xrate, self.yrate)
        res.EnableScrolling((self.style & wx.HSCROLL) != 0, (self.style & wx.VSCROLL) != 0)
        return res

class SplitterWindow(Window):
    props = Window.props | set(['minimumPaneSize', 'sashGravity', 'sashPosition'])
    positional = ['orient', 'sashGravity']
    style = wx.TAB_TRAVERSAL
    name = 'splitter'
    proportion = 1
    flag = wx.EXPAND
    minimumPaneSize = 1 # 0 enables the misguided default behaviour of irrecoverably hiding RHS on double-click
    sashGravity = 0.5
    sashPosition = None
    def create_wxwindow(self):
        return self.initfn(wx.SplitterWindow)(self.parent, self.id, self.pos, self.size, self.style, self.name)
    def create_postorder(self):
        if len(self.zchildren)!=2 or not all(isinstance(ch.w, wx.Window) for ch in self.zchildren):
            raise TypeError('SplitterWindow must have exactly 2 wx.Window children')
        if self.sashGravity is not None: self.w.SetSashGravity(self.sashGravity)
        if self.minimumPaneSize is not None: self.w.SetMinimumPaneSize(self.minimumPaneSize)
        if self.orient == wx.VERTICAL: # strange as it sounds, SplitHorizontally stacks subwindows vertically
            self.w.SplitHorizontally(self.zchildren[0].w, self.zchildren[1].w)
        else:
            self.w.SplitVertically(self.zchildren[0].w, self.zchildren[1].w)
        if self.sashPosition is not None: self.w.SetSashPosition(self.sashPosition)

class SpinCtrl(Window):
    props = Window.props | set(['value','min','max','initial'])
    positional = ['min', 'max', 'initial'] # xx does 'value' (string) have value? check that it works as expected to use initial
    value = ''
    min = 0
    max = 100
    initial = 0
    name = 'wxSpinCtrl'
    def create_wxwindow(self):
        return self.initfn(wx.SpinCtrl)(self.parent, self.id, self.value, self.pos, self.size, self.style, self.min, self.max, self.initial, self.name)

class StaticLine(Window):
    props = Window.props | set(['name','thickness'])
    positional = ['thickness', 'style']
    style = wx.LI_HORIZONTAL
    thickness = None
    flag = wx.EXPAND
    name = 'staticline'
    def create_wxwindow(self):
        if self.thickness is not None:
            if self.style & wx.LI_HORIZONTAL:
                self.size = (-1, self.thickness)
            elif self.style & wx.LI_VERTICAL:
                self.size = (self.thickness, -1)
        return self.initfn(wx.StaticLine)(self.parent, self.id, self.pos, self.size, self.style, self.name)

class FileBrowseButton(Window):
    props = Window.props | set(['name', 'labelText', 'buttonText', 'dialogTitle', 'startDirectory',
                                 'initialValue', 'fileMask', 'fileMode', 'changeCallback', 'labelWidth'])
    style = wx.TAB_TRAVERSAL
    labelText = 'File Entry:'
    buttonText = 'Browse'
    toolTip = 'Type filename or click browse to choose file'
    dialogTitle = 'Choose a file'
    startDirectory = '.'
    initialValue = ''
    fileMask = '*.*'
    fileMode = wx.FD_OPEN
    changeCallback = lambda self,x:x
    labelWidth = 0
    name = 'fileBrowseButton'
    def create_wxwindow(self):
        import wx.lib.filebrowsebutton
        return self.initfn(wx.lib.filebrowsebutton.FileBrowseButton)(
            self.parent, self.id, self.pos, self.size, self.style,
            self.labelText, self.buttonText, self.toolTip,
            self.dialogTitle, self.startDirectory, self.initialValue,
            self.fileMask, self.fileMode, self.changeCallback,
            self.labelWidth, self.name)

class MaskedNumCtrl(Control):
    props = Control.props | set(['value','kwargs'])
    positional = ['value']
    name = 'masked.num'
    style = wx.TE_PROCESS_TAB
    value = 0
    def create_wxwindow(self):
        import wx.lib.masked
        return self.initfn(wx.lib.masked.NumCtrl)(self.parent, self.id, self.value, self.pos, self.size, self.style, self.validator, self.name, **self.kwargs)

class MaskedTextCtrl(Control):
    props = Control.props | set(['value', 'setupEventHandling','kwargs'])
    positional = ['value']
    style = wx.TE_PROCESS_TAB
    setupEventHandling = True
    name = 'maskedTextCtrl'
    value = ''
    def create_wxwindow(self):
        import wx.lib.masked
        return self.initfn(wx.lib.masked.TextCtrl)(self.parent, self.id, self.value, self.pos, self.size, self.style, self.validator, self.name,
                                      self.setupEventHandling, **self.kwargs)

class GradientButton(Control):
    props = Window.props | set(['bitmap', 'label', 'name'])
    positional = ['label', 'bitmap'] # order reversed, I just don't see buttons with bitmap but no label happening, also this order is Button compatible
    bitmap = None
    style = wx.NO_BORDER
    name = 'gradientbutton'
    align = 1
    def create_wxwindow(self):
        import wx.lib.agw.gradientbutton
        return self.initfn(wx.lib.agw.gradientbutton.GradientButton)(self.parent, self.id, self.bitmap, self.label, self.pos, self.size, self.style, validator=self.validator, name=self.name)

class Notebook(Control):
    # To add pages, nest Page children.
    props = Control.props
    positional = []
    name = 'notebook'
    def create_wxwindow(self):
        return self.initfn(wx.Notebook)(self.parent, self.id, self.pos, self.size, self.style, self.name)
    def create_postorder(self):
        assert all(isinstance(c, Page) for c in self.zchildren)

class Page(Entity):
    # A Notebook page.
    props = Entity.props | set(['text','select','imageId'])
    positional = ['text']
    select = False
    imageId = -1 # to use: wx.Notebook.SetImageList
    panel = None
    def create_preorder(self):
        assert isinstance(self.zparent, Notebook)
    def create_postorder(self):
        if len(self.zchildren)==1:
            self.zparent.w.AddPage(self.zchildren[0].w, self.text, self.select, self.imageId)
        else:
            raise TypeError('Page has %d children, exactly 1 expected' % (len(self.zchildren),))
        
class ItemsPicker(Panel):
    props = Panel.props | set(['choices','label','selectedLabel','ipStyle','kwargs'])
    positional = ['choices','label','selectedLabel']
    choices = []
    label = ''
    selectedLabel = ''
    ipStyle = 0
    def create_wxwindow(self):
        from wx.lib import itemspicker
        return self.initfn(itemspicker.ItemsPicker)(self.parent, self.id, self.choices, self.label, self.selectedLabel, self.ipStyle, **self.kwargs)

class ExpandoTextCtrl(TextCtrl):
    name = 'expando'
    def create_wxwindow(self):
        from wx.lib.expando import ExpandoTextCtrl
        return self.initfn(ExpandoTextCtrl)(self.parent, self.id, self.value, self.pos, self.size, self.style, self.validator, self.name)

class PlotCanvas(Panel):
    name = 'plotCanvas'
    style = 0
    def create_wxwindow(self):
        from wx.lib import plot
        return self.initfn(plot.PlotCanvas)(self.parent, self.id, self.pos, self.style, self.name)

class Gauge(Control):
    name = wx.GaugeNameStr
    props = Control.props | set(['range','style'])
    positional = ['range']
    range = 100
    style = wx.GA_HORIZONTAL
    def create_wxwindow(self):
        return self.initfn(wx.Gauge)(self.parent, self.id, self.range, self.pos, self.size, self.style, self.validator, self.name)

######################################################################
# Top-level windows.

class TopLevelWindow(Window):
    props = Window.props | set(['size','pos','title'])
    positional = ['title']
    title = ''
    proportion = 1
    flag = wx.EXPAND

class Frame(TopLevelWindow):
    name = wx.FrameNameStr
    style = wx.DEFAULT_FRAME_STYLE
    def create_wxwindow(self):
        return self.initfn(wx.Frame)(self.parent, self.id, self.title, self.pos,
                        self.size, self.style, self.name)

class Dialog(TopLevelWindow):
    name = wx.DialogNameStr
    style = wx.DEFAULT_DIALOG_STYLE
    def create_wxwindow(self):
        return self.initfn(wx.Dialog)(self.parent, self.id, self.title, self.pos,
                        self.size, self.style, self.name)

    
######################################################################
# Menus.

class MenuEntity(Entity):
    def create_postorder(self):
        pass
class TopLevelMenu(MenuEntity):
    def as_parent(self):
        look_in = self
        while look_in is not None:
            if isinstance(look_in.parent, wx.TopLevelWindow):
                return look_in.parent
            look_in = look_in.zparent
        raise TypeError('%s parent must be set to top-level window' % (self,))

class MenuEntry(MenuEntity):
    pass

class MenuBar(TopLevelMenu):
    props = set(['parent','style'])
    positional = ['parent']
    style = 0
    parent = None
    def create_preorder(self):
        self.w = wx.MenuBar(self.style)
    def create_postorder(self):
        if self.parent is not None:
            self.parent.SetMenuBar(self.w)

class PopupMenu(TopLevelMenu):
    props = set(['parent'])
    positional = ['parent']
    def create_preorder(self):
        self.w = self.menu = wx.Menu()

class Menu(MenuEntry):
    props = ['menu', 'label', 'help']
    positional = ['label']
    toolTip = None
    menu = None
    help = ""
    def create_preorder(self):
        if self.menu is None:
            self.menu = wx.Menu()
        if not isinstance(self.zparent, (TopLevelMenu,Menu)):
            raise TypeError('wize.Menu nests under wize.MenuBar,wize.PopupMenu and wize.Menu, not %s' % (type(self.zparent,)))
        if isinstance(self.zparent, MenuBar):
            self.zparent.w.Append(self.menu, self.label)
            self.w = self.menu # there's no way to Enable/Disable wx.MenuBar top-level menus?!
        else:
            self.w = self.zparent.menu.AppendSubMenu(self.menu, self.label, self.help)
    def Enable(self, enabled=True):
        self.zparent.w.Enable(self.item.GetId(), enabled)
    def Disable(self):
        self.Enable(False)

class MenuItem(MenuEntry):
    # Ideally,
    #     iz.MenuItem(u"do something", EVT_MENU=self.OnDoSomething)
    # should 'just work', but sadly, wx.MenuItem objects do not have a Bind method.
    props = ['text', 'id', 'help', 'callback']
    positional = ['text', 'callback']
    callback = None
    help = ""
    kind = wx.ITEM_NORMAL
    id = -1
    def create_preorder(self):
        self.w = self.zparent.menu.Append(self.id, self.text, self.help, self.kind)
        if self.callback is not None:
            self.get_parent().Bind(wx.EVT_MENU, self.callback, id=self.w.GetId())

class MenuCheck(MenuItem):
    kind = wx.ITEM_CHECK

class MenuRadio(MenuItem):
    kind = wx.ITEM_RADIO

class MenuSeparator(MenuEntry):
    kind = wx.ITEM_SEPARATOR
    def create_preorder(self):
        self.w = self.zparent.menu.AppendSeparator()
