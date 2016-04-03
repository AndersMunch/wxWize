#!/usr/bin/python
# Same as demo_logon.py, except uses Default. This is just to show how Default works,
# it's too simple an example to carry any real benefits.

import sys, wx
from wx.lib.inspection import InspectionTool
sys.path.insert(0, '../src')
import wize as iz

class LogonDialog(wx.Dialog):
    def __init__(self, parent):
        with iz.Dialog(init=self, title=u"Logon", orient=wx.VERTICAL, style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER):
            with iz.GridBagSizer(orient=wx.HORIZONTAL, proportion=1) as gb:
                # Defaults for StaticText and TextCtrl are normally border=0,proportion=0,flag=0. Change them temporarily
                # to avoid repeating the same options for each and every control:
                with iz.StaticText.Default(border=10), iz.TextCtrl.Default(border=10, proportion=1, flag=wx.EXPAND):
                    # Now the sizer parameters can be omitted in the control definitions, since the defaults are
                    # now appropriate.
                    iz.StaticText(u"Username")
                    self._name = iz.TextCtrl().wx
                    iz.StaticText(u"Password", x=0)
                    self._pass = iz.TextCtrl(style=wx.TE_PASSWORD).wx
            gb.AddGrowableCol(1)
            with iz.StdDialogButtonSizer():
                okbut = iz.Button(u"OK", id=wx.ID_OK).wx
                iz.Button(u"Cancel", id=wx.ID_CANCEL)
                insp = iz.Button(u"Help", id=wx.ID_HELP,border=10, EVT_BUTTON=InspectionTool().Show).wx
        okbut.SetDefault()
        self.Fit()
    def GetValue(self):
        return self._name.GetValue(), self._pass.GetValue()


if __name__=='__main__':
    app = wx.App()
    dia = LogonDialog(None)
    mr = dia.ShowModal()
    if mr == wx.ID_OK:
        print("You entered username %r and password %r" % dia.GetValue())
    else:
        print("You cancelled.")
        
