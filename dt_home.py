#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 23 sept. 2014

@author: epelorce
'''
from time import sleep
from storageCtrl import storageCtrl
from utils import utils
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
            #print("try to stop thread lvl1")
            i.stop()
            #print("try to stop thread lvl2")
        utils_c.echo("waiting "+str(storageCtrl.getStopAcheived()),True)
        sleep(1)
    storageCtrl.setStopRequested(True)
    utils_c.echo("EXIT",True)

try:
    utils_c = utils()
    storageCtrl.init()
    storageCtrl.setUtils(utils_c)
    storageCtrl.loadExternalDatas()
    from senderCtrl import senderCtrl
    senderCtrl_t = senderCtrl(utils_c)
    senderCtrl_t.start()
    
    utils_c.echo("************************************************************************",True)
    try:
        if platform.python_version().find("3.") != -1:
            raw_input = input
    except:
        pass
    #inputKeyb = raw_input('Press "q" to Quit: ')
    #FileMode = None
    while True and storageCtrl.getStopRequested()==False:
        sleep(1)
    
except KeyboardInterrupt:
    quitApp()