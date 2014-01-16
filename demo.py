import wx

app = wx.App()
win = wx.Frame(None, title = "Client", size = (600, 480))
win.Show()

contents = wx.TextCtrl(win, pos = (10, 10), size = (580, 400), style = wx.TE_MULTILINE | wx.HSCROLL)
message = wx.TextCtrl(win, pos = (10, 425), size = (400, 25))
send = wx.Button(win, label = "Send", pos = (410, 420), size = (80, 25))
check = wx.Button(win, label = "History", pos = (500, 420), size = (80, 25))

app.MainLoop()
