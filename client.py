import ssl
import socket
import wx
import time


app = wx.App()
win = wx.Frame(None, title = "Client", size = (600, 480))
win.Show()
contents = wx.TextCtrl(win, pos = (10, 10), size = (580, 400), style = wx.TE_MULTILINE | wx.HSCROLL)
contents.SetValue('sdfsdfsdf\n')
message = wx.TextCtrl(win, pos = (10, 425), size = (400, 25))
send = wx.Button(win, label = "Send", pos = (410, 420), size = (80, 25))
check = wx.Button(win, label = "History", pos = (500, 420), size = (80, 25))
#app.MainLoop()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = ssl.wrap_socket(s)
s.connect(('localhost', 8080))
print(s.cipher())
while True:
        data = s.read(1024)
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        if data:
            contents.SetValue('[' + now + '] Server say: ' + data)

app.MainLoop()
s.close()
