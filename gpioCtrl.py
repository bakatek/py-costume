'''
Created on 23 sept. 2014

@author: epelorce
'''

import os
from time import sleep
from threading import Thread
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
        storageCtrl.removeThreadToStop(self)
    
    def run(self):
        self.out("start gpioCtrl")
        storageCtrl.addThreadToStop(self)
        while storageCtrl.getStopRequested() == False:
            newWebReq = storageCtrl.getGpioRequest()
            if newWebReq != None:
                everyActions = newWebReq.split(";")
                for action in everyActions:
                    [chan, pos, delay] = action.split("|")
                    pos = int(pos)
                    delay = float(delay)
                    if chan[:3] == "pwm" and pos:
                        self.gpio_c.move_servo(int(chan[3:]), pos)
                    elif chan[:3] != "pwm" and pos != None:
                        self.gpio_c.set_gpio(chan, pos)
                    else:
                        print("ERROR no rules chan:%s pos:%s delay:%s",chan, pos, delay)
                    if delay:
                        while delay > 0 and storageCtrl.getStopRequested() == False:
                            sleep(0.1)
                            delay = delay - 0.1
            sleep(self.refreshRate)
        storageCtrl.stopAcheived = storageCtrl.getStopAcheived() - 1