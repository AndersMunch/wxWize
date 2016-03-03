#!/usr/bin/python
# Like demo_logon.py but implemented in straight up wxPython
import wx
from wx.lib.inspection import InspectionTool

class LogonDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, title=u"Logon", style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        vsizer = wx.BoxSizer(orient=wx.VERTICAL)
        gb = wx.GridBagSizer()
        gb.Add(wx.StaticText(self, -1, u"Username"), flag=wx.ALL|wx.EXPAND, border=10, pos=(0,0))
        self._name = wx.TextCtrl(self, -1)
        gb.Add(self._name, flag=wx.ALL|wx.EXPAND, border=10, pos=(0,1))
        gb.Add(wx.StaticText(self, -1, u"Password"), flag=wx.ALL|wx.EXPAND, pos=(1,0), border=10)
        self._pass = wx.TextCtrl(self, -1, style=wx.TE_PASSWORD)
        gb.Add(self._pass, border=10, flag=wx.EXPAND|wx.ALL, pos=(1,1))
        gb.AddGrowableCol(1)
        butsz = wx.StdDialogButtonSizer()
        okbut = wx.Button(self, wx.ID_OK, u"OK")
        butsz.AddButton(okbut)
        cbut = wx.Button(self, wx.ID_CANCEL, u"Cancel")
        butsz.AddButton(cbut)
        insp = wx.Button(self, wx.ID_HELP, u"Help")
        butsz.AddButton(insp)
        insp.Bind(wx.EVT_BUTTON, InspectionTool().Show)
        butsz.Realize()
        okbut.SetDefault()
        vsizer.Add(gb, 0, wx.EXPAND)
        vsizer.Add(butsz, 0, wx.EXPAND)
        self.SetSizer(vsizer)
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
        
