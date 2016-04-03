#!/usr/bin/python
# Showing off lots of different wxWize-wrapped stuff.

import sys
sys.path.insert(0, '../src')
import wx
from wx.lib.inspection import InspectionTool
import wize as iz

class DemoFrame(wx.Frame):
    def __init__(self, parent=None):
        with iz.Frame(init=self, parent=parent, title=u'Hello world',
                      size=(-1, 400)) as fr, iz.Panel(orient=wx.VERTICAL):
            iz.Choice(list('abcdef'))
            iz.ComboBox('g', list('abcdef'))
            try:
                iz.DatePickerCtrl
            except AttributeError:
                pass
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
            with iz.Panel(bgcolour='#FFFFBB'):
                with iz.StaticLine.Default(thickness=3), iz.StaticText.Default(border=5):
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
