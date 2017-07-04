'''
Created on 23 sept. 2014

@author: epelorce
'''

import os
from time import sleep
from threading import Thread
from webSrv import webSrv
from storageCtrl import storageCtrl
from gpioEx import gpioEx
#from pprint import pprint

class gpioCtrl(Thread):
    '''
    classdocs
    '''

    def out(self, _txt):
        self.utils_c.echo("gpioCtrl:> "+_txt)
        
    def __init__(self, _utils_c):
        super(gpioCtrl,self).__init__()
        #self.storageCtrl_t = _storageCtrl
        self.utils_c = _utils_c
        self.gpio_c = gpioEx()
        self.refreshRate = 1
        self.out("init gpioCtrl")
        
    def stop(self):
        self.out("stop gpioCtrl")
        self.webSrv_t.stop()
        storageCtrl.removeThreadToStop(self)
    
    def run(self):
        self.out("start gpioCtrl")
        
        storageCtrl.addThreadToStop(self)
        while storageCtrl.getStopRequested() == False:
            newWebReq = storageCtrl.getGpioRequest()
            if newWebReq != None:
                splittedReq = newWebReq.split("|")
                if splittedReq.length == 2:
                    self.gpio_c.move_servo(splittedReq[0], splittedReq[1])
            sleep(self.refreshRate)
        storageCtrl.stopAcheived = storageCtrl.getStopAcheived() - 1