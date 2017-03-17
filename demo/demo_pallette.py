#!/usr/bin/python
# Showing off lots of different wxWize-wrapped stuff.

import sys
sys.path.insert(0, '../src')
import wx
from wx.lib import inspection, itemspicker
import wize as iz

class DemoFrame(wx.Frame):
    def __init__(self, parent=None):
        with iz.Frame(init=self, parent=parent, title=u'Hello world',
                      size=(-1, 600)) as fr, iz.Panel(orient=wx.VERTICAL):
            iz.Choice(list('abcdef'))
            iz.ComboBox('g', list('abcdef'))
            try:
                iz.DatePickerCtrl
            except AttributeError:
                pass # Phoenix may not have DatePickerCtrl yet
            else:
                iz.DatePickerCtrl()
            with iz.StaticBox(label=u"checkbox and button", orient=wx.HORIZONTAL):
                iz.CheckBox('checkbox')
                iz.Button(u'Show context menu', EVT_BUTTON=self.OnButton)
            try:
                wx.CommandLinkButton
            except AttributeError:
                pass
            else:
                iz.CommandLinkButton(u'A Command Link Button', u'(Native to Win7, emulated elsewhere.)', EVT_BUTTON=self.OnButton)
            with iz.TextCtrl('TextCtrl', flag=wx.EXPAND):
                pass
            with iz.BoxSizer(wx.HORIZONTAL):
                iz.StaticText('MaskedNumCtrl:')
                iz.MaskedNumCtrl(42)
            with iz.Panel(bgcolour='#FFFFBB', proportion=1):
                with iz.StaticLine.Default(thickness=3, border=5):
                    with iz.BoxSizer(wx.VERTICAL):
                        iz.StaticLine(10)
                        iz.StaticText("Space 5")
                        iz.StaticLine() # thickness argument from Default above
                        iz.Spacer(5)
                        iz.StaticLine()
                        iz.StaticText("Space 20")
                        iz.StaticLine()
                        iz.Spacer(20)
                        iz.StaticLine()
                        iz.StaticText("End space panel")
                        iz.StaticLine(10)

                        
            with iz.SplitterWindow(wx.HORIZONTAL, sashGravity=0.5, proportion=0, sashPosition=50):
                iz.StaticText('SplitterWindow left is lilac and only 50 pixels initially', bgcolour='#c8a2c8')
                iz.StaticText('<=SASH   SplitterWindow right is red.', bgcolour='RED')
            with iz.SplitterWindow(wx.VERTICAL, sashGravity=0.25, proportion=2):
                with iz.Panel(bgcolour='#008080', orient=wx.VERTICAL):
                    iz.StaticText('SplitterWindow top is teal. Move the sash to show the whole thing.')
                    iz.ListBox("This ListBox doesn't fit unless you move the sash".split(), proportion=1)

                with iz.Panel(bgcolour='BROWN', orient=wx.VERTICAL):
                    iz.StaticText('(SASH RIGHT ABOVE.) SplitterWindow bottom is brown.')
                    iz.ItemsPicker(['fast','cheap','good'], 'Pick two', ipStyle=itemspicker.IP_REMOVE_FROM_CHOICES)

            with iz.PopupMenu(fr) as self.button_menu:
                iz.MenuItem('&Disable radio button 2', lambda event:rb2.Enable(False))
                iz.MenuItem('&Select radio button 3', lambda event:rb3.Check(True))
                iz.MenuCheck('&Checkbox item')
                iz.MenuSeparator()
                rb1 = iz.MenuRadio('&Radio button 1').wx
                rb2 = iz.MenuRadio('&Radio button 2').wx
                rb3 = iz.MenuRadio('&Radio button 3').wx
        with iz.MenuBar(fr) as a:
            with iz.Menu(u'&File'):
                iz.MenuItem(u'&Open')
                iz.MenuItem(u'&Pop up', self.OnButton)
                with iz.Menu(u'&Submenu'):
                    iz.MenuItem(u'Item in submenu')
                iz.MenuItem(u'&Close')
            with iz.Menu(u'&Help'):
                iz.MenuItem(u'&About')

    def OnButton(self, event):
        self.PopupMenu(self.button_menu)
            
def main():
    app = wx.App(redirect=0)
    inputs = []
    fr = DemoFrame()
    fr.Show()
    # InspectionTool().Show()
    app.MainLoop()
                    
if __name__=='__main__':
    main()
