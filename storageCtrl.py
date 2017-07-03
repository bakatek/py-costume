'''
Created on 15 dec. 2015
@author: epelorce
'''

import os
import platform
import json
from pprint import pprint
#import utils
#from requestDatas import requestDatas

class storageCtrl(object):
    '''
    classdocs
    '''
    @staticmethod
    def init():
        '''
        Constructor
        '''
        #storageCtrl.utils_c = utils.utils()
        #super(storageCtrl,self).__init__()
        storageCtrl.Version = "0.0.0.1"
        storageCtrl.DEBUG = True
        storageCtrl.verboseLevel = 0
        storageCtrl.platformVersion = -1
        storageCtrl.dataFile = "datas.json"
        
        storageCtrl.authorizedCommands = []
        storageCtrl.keywordsAndCmds =[]
        # storageCtrl.keywordsAndCmds =[
        # ["ventilation", "sh /root/cmds/fan.sh"],
        # ["voixlive", "sh /root/cmds/voice_live.sh"],
        # ["videoproj_f1", "sh /root/cmds/video_f1.sh"],
        # ["videoproj_f2", "sh /root/cmds/video_f2.sh"],
        # ["cooldown", "sh /root/cmds/cooldown.sh"],
        # ["laser", "sh /root/cmds/laser.sh"]]
        for elem in storageCtrl.keywordsAndCmds:
            storageCtrl.authorizedCommands.append(elem[0])

        storageCtrl.WebRequests = []
        
        storageCtrl.LocalPath = os.getcwd()
        
        storageCtrl.GPIO_IN = ["P8_12"]
        storageCtrl.GPIO_OUT = ["P8_10","P8_11"]
        
        storageCtrl.GPIO_OUT_state = [None]
        storageCtrl.GPIO_IN_state = [None]

        storageCtrl.keyboardManagerThread = None
        storageCtrl.threadToStop = []
        storageCtrl.LedReq = []
        storageCtrl.mailReq = []
        storageCtrl.stopAcheived = 0
        storageCtrl.stopRequested = False
        #storageCtrl.setStopAcheived = False
        
        storageCtrl.RedLight = "P8_10"
        
        if platform.python_version().find("3.") != -1:
            storageCtrl.setPlatformVersion(3)
        else:
            storageCtrl.setPlatformVersion(2)
    #-------------------------------------------------------------------------------------------------------------------
        storageCtrl.pushReq = []
    
    #-------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def loadExternalDatas():
        storageCtrl.utils_c.echo("----------------------  kw/cmd  ----------------------", True)
        if os.path.isfile(storageCtrl.dataFile):
            with open(storageCtrl.dataFile) as data_file:
                jsonContent = json.load(data_file)
                for item in jsonContent['kws_cmds']:
                    splittedCmd = item['cmd'].split(' ')
                    if len(splittedCmd) == 2 and splittedCmd[1].find(".sh") and os.path.isfile(splittedCmd[1]):
                        storageCtrl.keywordsAndCmds.append([item['kw'],item['kb'], item['cmd']])
                        storageCtrl.utils_c.echo("  OK".ljust(8) + item['kw'].ljust(15) + "   " + item['cmd'], True)
                    else:
                        storageCtrl.utils_c.echo("  F-ERR".ljust(8) + item['kw'].ljust(15) + "   " + item['cmd'], True)
        else:
            return None
        storageCtrl.utils_c.echo("------------------------------------------------------", True)
        #pprint(storageCtrl.keywordsAndCmds)
    
    @staticmethod
    def getLedRequest():
        if len(storageCtrl.LedReq) > 0:
            return storageCtrl.LedReq.pop()
        else:
            return None
    
    @staticmethod
    def addLedRequest(_commands):
        storageCtrl.LedReq.append(_commands)
        
    @staticmethod
    def addThreadToStop(_addThread):
        storageCtrl.stopAcheived += 1
        storageCtrl.threadToStop.append(_addThread)
        
    @staticmethod
    def removeThreadToStop(_addThread):
        storageCtrl.stopAcheived -= 1
        storageCtrl.threadToStop.remove(_addThread)
        
    @staticmethod
    def getThreadsToStop():
        return storageCtrl.threadToStop
            
    @staticmethod
    def getThreadToStop():
        if len(storageCtrl.threadToStop) > 0:
            return storageCtrl.threadToStop.pop()
        else:
            return None
    
    @staticmethod
    def setPlatformVersion(_platformVersion):
        storageCtrl.platformVersion = _platformVersion

    @staticmethod
    def getPlatformVersion():
        return storageCtrl.platformVersion

    @staticmethod
    def getAuthorizedCommands():
        return storageCtrl.authorizedCommands

    @staticmethod
    def getkeywordsAndCommands():
        return storageCtrl.keywordsAndCmds

    @staticmethod
    def pushWebRequest(_value):
        print("push %s ",_value)
        storageCtrl.WebRequests.append(_value)
    
    @staticmethod
    def getWebRequest():
        #print("Return %s ",storageCtrl.WebRequests)

        if len(storageCtrl.WebRequests) > 0:
            return storageCtrl.WebRequests.pop(0)
        else:
            return None
    
    @staticmethod
    def getVersion():
        return storageCtrl.Version
    
    @staticmethod
    def isWINDOWS():
        return storageCtrl.ISWINDOWS
    
    @staticmethod
    def getLocalPath():
        return storageCtrl.LocalPath
    
    @staticmethod
    def setStopAcheived(_datas):
        storageCtrl.stopAcheived = _datas

    @staticmethod
    def getStopAcheived():
        return storageCtrl.stopAcheived

    @staticmethod
    def setUtils(_utils_c):
        storageCtrl.utils_c = _utils_c

    @staticmethod
    def setStopRequested(_datas):
        storageCtrl.stopRequested = _datas
    
    @staticmethod
    def getStopRequested():
        #print("STOP %s", storageCtrl.stopRequested)
        return storageCtrl.stopRequested
    
    @staticmethod
    def getIsWindows():
        if os.name == "nt":
            return True
        else:
            return False
