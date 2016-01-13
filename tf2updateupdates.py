import filecmp
import urllib.request
import urllib.parse
import time
import os
import sys
import winsound
from win32api import *
from win32gui import *
import win32con
import struct

class WindowsBalloonTip:
    def __init__(self, title, msg):
        message_map = {
                win32con.WM_DESTROY: self.OnDestroy,
        }
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = message_map 
        classAtom = RegisterClass(wc)
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = CreateWindow( classAtom, "Taskbar", style, \
                0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
                0, 0, hinst, None)
        UpdateWindow(self.hwnd)
        iconPathName = os.path.abspath(os.path.join( sys.path[0], "balloontip.ico" ))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
           hicon = LoadImage(hinst, iconPathName, \
                    win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
          hicon = LoadIcon(0, win32con.IDI_APPLICATION)
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "tooltip")
        Shell_NotifyIcon(NIM_ADD, nid)
        Shell_NotifyIcon(NIM_MODIFY, \
                         (self.hwnd, 0, NIF_INFO, win32con.WM_USER+20,\
                          hicon, "Balloon  tooltip",msg,200,title))
        # self.show_balloon(title, msg)
        time.sleep(10)
        DestroyWindow(self.hwnd)
    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0) # Terminate the app.

def balloon_tip(title, msg):
    w=WindowsBalloonTip(title, msg)

#creates a first html file of the news page for reference later in the code
url2 = 'http://www.teamfortress.com/?tab=updates' #editable to any page on the site (or any site really)
headers = {}
headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
req = urllib.request.Request(url2, headers = headers)
resp = urllib.request.urlopen(req)
respData = resp.read()

with open('updates1.html', 'w') as saveFile:

    saveFile.write(str(respData))



loop = 1
version = 2

while loop == 1:
    print('looking for new tf2 updates')

    try:
        version2 = version - 1         #
        title1 = 'updates'+str(version)   #sets new name each time around for comparing two .html files
        title2 = 'updates'+str(version2)  #
        url = 'http://www.teamfortress.com/?tab=updates'
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        req = urllib.request.Request(url, headers = headers)
        resp = urllib.request.urlopen(req) #
        respData = resp.read()             #pulls the .html file

        saveFile = open('updates'+str(version)+'.html', 'w') #writes latest .html file
        saveFile.write(str(respData))
        saveFile.close
        time.sleep(10) #subject to a lot of change, just for quick testing
        filesame = filecmp.cmp(str(title1)+'.html',str(title2)+'.html',shallow=False) #compares the latest and second latest .html files of the page, checking for updates
        if filesame: #if they're the same, nothing changed
            print('nothing found yet')
            os.remove(str(title2)+'.html')
        else:                                    #if they're different, the page has changed and therefore something has happened, usually a news blog post
            print("new update found to the tf2 update blog.")
            loop = 2
            winsound.PlaySound("!", winsound.SND_ALIAS)
            balloon_tip("TF2 update found", "there has been an update to the /updates page, probably a new tf2 update")
        version = version + 1
    except Exception as e:
        print(str(e))    #error testing
