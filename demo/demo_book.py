#!/usr/bin/python
# Showing off lots of different wxWize-wrapped stuff.

import sys
sys.path.insert(0, '../src')
import wx
import wize as iz

class DemoFrame(wx.Frame):
    def __init__(self, parent=None):
        with iz.Frame(init=self, parent=parent, title=u'Notebooks', size=(-1, 600)) as fr, iz.Panel(orient=wx.VERTICAL, proportion=1):
            with iz.Notebook(proportion=1):
                for title in [
                        'This',
                        'is',
                        'a',
                        'Notebook',
                        ]:
                    with iz.Page(title):
                        with iz.Panel():
                            iz.StaticText("The wx.Notebook page with the title '%s'" % (title,))

            with iz.LabelBook():
                for title in [
                        'This',
                        'is',
                        'a',
                        'LabelBook',
                        ]:
                    with iz.Page(title):
                        iz.StaticText("The wx.lib.agw.labelbook.LabelBook page with the title '%s'" % (title,))

        self.Layout()
            
def main():
    app = wx.App(redirect=0)
    inputs = []
    fr = DemoFrame()
    fr.Show()
    # InspectionTool().Show()
    app.MainLoop()
                    
if __name__=='__main__':
    main()
