'''
Created on 15 dec. 2015
@author: epelorce
'''

import os
from time import sleep
from threading import Thread
from KBHit import KBHit
from storageCtrl import storageCtrl

'''
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
'''

class kbSrv(Thread):
    '''
    classdocs
    '''
    def out(self, _txt):
        self.utils_c.echo("kbSrv:> "+_txt)
        
    def __init__(self, _utils_c, _refresh=1):
        super(kbSrv,self).__init__()
        #self.storageCtrl_t = _storageCtrl
        self.utils_c = _utils_c
        self.refreshRate = _refresh
        
        self.out("init kbSrv")
        
    def stop(self):
        self.out("stop kbSrv")
        storageCtrl.removeThreadToStop(self)
    
    def run(self):
        self.out("start kbSrv")
        storageCtrl.addThreadToStop(self)
        
        my_kb = KBHit()
        while storageCtrl.getStopRequested() == False:
            c = ""
            try:
                if my_kb.get_kbhit():
                    c = my_kb.getch()
                    if ord(c) == 27: # ESC
                        break
                    self.out(str(ord(c)) + "=" + c)
                allKWandCommands = storageCtrl.getkeywordsAndCommands()
                for [kw, kb, command] in allKWandCommands:
                    if c == kb:
                        storageCtrl.pushWebRequest(command)
            except:
                self.out("Error on keypressed")
            sleep(self.refreshRate)
        my_kb.set_normal_term()
        storageCtrl.stopAcheived = storageCtrl.getStopAcheived() - 1
