'''
Created on 15 dec. 2015
@author: epelorce
'''

import random
import uuid
import time
from storageCtrl import storageCtrl
from kbSrv import kbSrv
from string import Template
import subprocess, threading

class DeltaTemplate(Template):
    delimiter = "%"

class utils(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.storageCtrl_t = storageCtrl

    def execute_cmd(self, _cmd):
        print("EXECUTE CMD %s", _cmd)
        #command = Command("echo 'Process started' & ping -n 2 127.0.0.1 >nul & echo 'Process finished'")
        command = Command(_cmd)
        command.run(timeout=2)

    def echo(self, _txt, _force=False, _verboseLvl=0):
        if  len(_txt) > 0 and self.storageCtrl_t.DEBUG == True and self.storageCtrl_t.verboseLevel >= _verboseLvl:
            print("Debug-> "+_txt)
        elif  len(_txt) > 0 and _force == True:
            print(_txt)

    def generateTimeStamp(self):
        return int(time.time())

    def strfdelta(self, tdelta, fmt):
        d = {"D": tdelta.days}
        d["H"], rem = divmod(tdelta.seconds, 3600)
        d["M"], d["S"] = divmod(rem, 60)
        t = DeltaTemplate(fmt)
        return t.substitute(**d)
             
    def randTimer(self, baseTimer=0.0 , delta = 3):
        return random.uniform(baseTimer, baseTimer+delta)
    
    def generateUID(self):
        return str(uuid.uuid1())
    
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            pass
     
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
     
        return False
    
    def saveFile(self, _datas, _filename):
        length = len(_datas)
        with open(self.storageCtrl_t.getStorePath()+_filename, 'wb') as fh:
            fh.write(_datas)

class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def run(self, timeout):
        def target():
            print('Thread started '+str(self.cmd))
            self.process = subprocess.Popen(self.cmd, shell=True)
            self.process.communicate()
            print('Thread finished')

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            print('Terminating process')
            self.process.terminate()
            thread.join()
        print(self.process.returncode)

            
            