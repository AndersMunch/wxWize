#!/usr/bin/python
# A simple example.
import sys, wx
from wx.lib.inspection import InspectionTool
sys.path.insert(0, '../src')
import wize as iz

class LogonDialog(wx.Dialog):
    def __init__(self, parent):
        with iz.Dialog(init=self, title=u"Logon", orient=wx.VERTICAL, style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER):
            with iz.GridBagSizer(orient=wx.HORIZONTAL, proportion=1) as gb:
                iz.StaticText(u"Username", border=10)
                self._name = iz.TextCtrl(border=10, proportion=1, flag=wx.EXPAND).wx
                iz.StaticText(u"Password", x=0, border=10)
                self._pass = iz.TextCtrl(style=wx.TE_PASSWORD, border=10, proportion=1, flag=wx.EXPAND).wx
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
        
