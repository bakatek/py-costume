'''
Created on 23 sept. 2014

@author: epelorce
'''

import os
from time import sleep
from threading import Thread
from webSrv import webSrv
from storageCtrl import storageCtrl
#from pprint import pprint

class senderCtrl(Thread):
    '''
    classdocs
    '''

    def out(self, _txt):
        self.utils_c.echo("senderCtrl:> "+_txt)
        
    def __init__(self, _utils_c):
        super(senderCtrl,self).__init__()
        #self.storageCtrl_t = _storageCtrl
        self.utils_c = _utils_c
        self.refreshRate = 1        
        self.out("init senderCtrl")
        
    def stop(self):
        self.out("stop senderCtrl")
        self.webSrv_t.stop()
        storageCtrl.removeThreadToStop(self)
    
    def run(self):
        self.out("start senderCtrl")
        
        storageCtrl.addThreadToStop(self)
        
        self.webSrv_t = webSrv(self.utils_c,8080,0.1)
        self.webSrv_t.start()
        while storageCtrl.getStopRequested() == False:
            newWebReq = storageCtrl.getWebRequest()
            if newWebReq != None:
                self.utils_c.execute_cmd(newWebReq[1])
                if newWebReq[0] == "send":
                    if len(newWebReq) == 2:
                        self.sendMail(newWebReq[1])
            sleep(self.refreshRate)
        storageCtrl.stopAcheived = storageCtrl.getStopAcheived() - 1