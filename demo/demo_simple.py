#!/usr/bin/python
# A simple example.
import sys
sys.path.insert(0, '../src')
import wx
import wize as iz

def OnClick(event):
    wx.SafeShowMessage('Message','You clicked')
def main():
    app = wx.App(redirect=0)
    with iz.Frame(title=u'Hello world') as fr, iz.Panel():
        with iz.StaticBox(label=u"All of them", orient=wx.VERTICAL):
            for i in xrange(5):
                with iz.BoxSizer(orient=wx.HORIZONTAL, border=10):
                    iz.StaticText(label=u"Enter value #%d:" % (i,),
                                  EVT_LEFT_DOWN=OnClick)
                    iz.TextCtrl(value=u"<initial value>", proportion=1)
    fr.Show(True)
    app.MainLoop()

if __name__=='__main__':
    main()
