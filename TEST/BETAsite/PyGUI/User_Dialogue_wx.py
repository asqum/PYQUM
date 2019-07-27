# import wx
 
# app = wx.App()
 
# frame = wx.Frame(None, -1)
 
# # Create text input
# dlg = wx.TextEntryDialog(frame, 'Enter some text','Text Entry')
# dlg.SetSize(0,0,200,50)
# dlg.SetWindowStyle(wx.STAY_ON_TOP )
# dlg.SetValue("Default")
# if dlg.ShowModal() == wx.ID_OK:
#     print('You entered: %s\n' % dlg.GetValue())
# dlg.Destroy()

import wx
 
########################################################################
class StayOnTopFrame(wx.Frame):
    """
    A frame that stays on top of all the others
    """
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        on_top = wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP
        wx.Frame.__init__(self, None, title="Stay on top", style=on_top)
        panel = wx.Panel(self)
        self.Show()
 
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = StayOnTopFrame()
    app.MainLoop()