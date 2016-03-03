#!/usr/bin/python
# This is a somewhat equivalent of custom1 from the XRCed examples.

# This is to answer the question: Suppose you had a control such as
# wx.gizmos.LEDNumberCtrl, with no support in the library -- what
# would be needed to fit it in?

import sys
sys.path.insert(0, '../src')
import wx.gizmos
import wize as iz

class LEDNumberCtrl(iz.Window):
    props = iz.Window.props | set(['style','value'])
    style = 0
    value = '123'
    def create_wxwindow(self):
        from wx import gizmos
        w = gizmos.LEDNumberCtrl(self.parent,
                                 self.id,
                                 self.pos,
                                 self.size,
                                 self.style)
        align = self.style & 7
        if align: w.SetAlignment(align)
        w.SetValue(self.value)
        return w

if __name__=='__main__':
    from wx import gizmos
    app = wx.App()
    with iz.Frame() as fr:
        with iz.Panel():
            with iz.StaticBox(u"Countdown", wx.VERTICAL):
                LEDNumberCtrl(value='10', style=wx.gizmos.LED_ALIGN_CENTER|wx.gizmos.LED_DRAW_FADED,
                        fgcolour='#FF0000', bgcolour='#303030', size=(200,100))
    fr.Fit()
    fr.Show()
    app.MainLoop()

