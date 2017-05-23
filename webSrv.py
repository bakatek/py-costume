'''
Created on 15 dec. 2015
@author: epelorce
'''

import os
from time import sleep
from threading import Thread
from storageCtrl import storageCtrl
if storageCtrl.getPlatformVersion() == 2:
    import SimpleHTTPServer
    import SocketServer
else:
    import http.server
    SimpleHTTPServer = http.server
    import socketserver
    SocketServer = socketserver

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        allKWandCommands = storageCtrl.getkeywordsAndCommands()
        for [kw, command] in allKWandCommands:
            if self.path.split("?")[0] == '/www/'+kw:
                storageCtrl.pushWebRequest(command)
                self.path = '/www/index.html'
        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
    
    def log_message(self, format, *args):
        pass

class webSrv(Thread):
    '''
    classdocs
    '''

    def out(self, _txt):
        self.utils_c.echo("webSrv:> "+_txt)

    def __init__(self, _utils_c, _port, _loopSleep):
        super(webSrv,self).__init__()
        self.PORT = _port
        self.utils_c = _utils_c
        self.refreshRate = _loopSleep
        self.webSrvHandler = MyRequestHandler
        self.httpd = SocketServer.TCPServer(("", self.PORT), self.webSrvHandler)
        
        self.out("init")
        
    def stop(self):
        self.httpd.server_close()
        self.out("stop")
        storageCtrl.removeThreadToStop(self)

    def run(self):
        storageCtrl.addThreadToStop(self)
        try:
            self.httpd.serve_forever()
        except:
            pass
        while storageCtrl.getStopRequested() == False:
            sleep(self.refreshRate)
        storageCtrl.stopAcheived = storageCtrl.getStopAcheived() - 1
