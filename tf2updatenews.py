import filecmp
import urllib.request
import urllib.parse
import time
import os
import sys
import ctypes


#creates a first html file of the news page for reference later in the code
url2 = 'http://www.teamfortress.com/?tab=news' #editable to any page on the site (or any site really)
headers = {}
headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
req = urllib.request.Request(url2, headers = headers)
resp = urllib.request.urlopen(req)
respData = resp.read()

with open('news1.html', 'w') as saveFile:

    saveFile.write(str(respData))



loop = 1
version = 2

while loop == 1:
    print('looking for updates to tf2 news')

    try:
        version2 = version - 1         #
        title1 = 'news'+str(version)   #sets new name each time around for comparing two .html files
        title2 = 'news'+str(version2)  #
        url = 'http://www.teamfortress.com/?tab=news'
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        req = urllib.request.Request(url, headers = headers)
        resp = urllib.request.urlopen(req) #
        respData = resp.read()             #pulls the .html file

        saveFile = open('news'+str(version)+'.html', 'w') #writes latest .html file
        saveFile.write(str(respData))
        saveFile.close
        time.sleep(10) #subject to a lot of change, just for quick testing
        filesame = filecmp.cmp(str(title1)+'.html',str(title2)+'.html',shallow=False) #compares the latest and second latest .html files of the page, checking for updates
        if filesame: #if they're the same, nothing changed
            print('nothing found yet')
            os.remove(str(title2)+'.html')
        else:                                    #if they're different, the page has changed and therefore something has happened, usually a news blog post
            print("new update found to the tf2 news blog.")
            loop = 2
            ctypes.windll.user32.MessageBoxA(0, "An update has been found!", "TF2 news blog update", 1)
        version = version + 1
    except Exception as e:
        print(str(e))    #error testing
