#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 23 sept. 2014

@author: epelorce
'''
from time import sleep
from storageCtrl import storageCtrl
from utils import utils
from kbSrv import kbSrv
from inputSrv import inputSrv
from gpioCtrl import gpioCtrl
#from pprint import pprint

if __name__ == '__main__':
    pass

def quitApp():
    storageCtrl.setStopRequested(True)
    #print("KILL REQ")
    
    # storageCtrl.setStopRequested(True)
    # storageCtrl.keyboardManagerThread.stop()
    #pprint(storageCtrl.getStopAcheived)
    while storageCtrl.getStopAcheived() > 0:    
        for i in storageCtrl.getThreadsToStop():
            print("try to stop thread lvl1")
            i.stop()
            print("try to stop thread lvl2")
        utils_c.echo("waiting "+str(storageCtrl.getStopAcheived()),True)
        sleep(1)
        # print(".10")
    storageCtrl.setStopRequested(True)
    utils_c.echo("EXIT",True)

try:
    utils_c = utils()
    storageCtrl.init()
    storageCtrl.setUtils(utils_c)
    storageCtrl.loadExternalDatas()
    gpioCtrl_t = gpioCtrl(utils_c)
    gpioCtrl_t.start()
    from senderCtrl import senderCtrl
    senderCtrl_t = senderCtrl(utils_c)
    senderCtrl_t.start()
    inputSrv_t = inputSrv(utils_c,0.5)
    inputSrv_t.start()
    
    kbSrv_t = kbSrv(utils_c,0.5)
    kbSrv_t.start()
    
    try:
        if platform.python_version().find("3.") != -1:
            raw_input = input
    except:
        pass

    while True and storageCtrl.getStopRequested()==False:
        # print(".3")
        sleep(1)
    
except KeyboardInterrupt:
    quitApp()